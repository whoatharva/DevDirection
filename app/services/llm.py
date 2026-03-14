import os
import json
from typing import Dict, List, Optional, Any, TypedDict
from datetime import datetime

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langgraph.graph import StateGraph, START, END

from app.models import UserProfile, RoadmapResponse, RoadmapPhase, Milestone, SubTask, SkillGap, SkillLevel, MilestoneType

# ─── 1A. STATE DEFINITION ───────────────────────────────
class RoadmapState(TypedDict):
    user_profile: dict
    career_focus: str
    skill_analysis: dict
    phases_raw: list
    skill_gaps_raw: list
    roadmap_response: dict
    error: Optional[str]
    retry_count: int

# ─── HELPER FOR LLM GENERATION ───────────────────────────
def _invoke_llm(system_prompt: str, user_prompt: str) -> dict:
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)
    parser = JsonOutputParser()
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}")
    ])
    chain = prompt | llm | parser
    return chain.invoke({"input": user_prompt})

# ─── 1B. GRAPH NODES ─────────────────────────────────────

def analyze_profile(state: RoadmapState) -> RoadmapState:
    try:
        user_prof = state["user_profile"]
        system_prompt = """You are a career advisor. Return JSON with exactly these keys:
- career_focus (string: primary career path)
- experience_bucket ("beginner" | "intermediate" | "advanced")
- strongest_skills (list of up to 3 skills from user's current skills)
- learning_pace ("slow" | "moderate" | "fast")
- recommended_phases_count (integer 3 or 4)"""
        user_prompt = f"User Profile: {json.dumps(user_prof)}"
        result = _invoke_llm(system_prompt, user_prompt)
        state["skill_analysis"] = result
        state["career_focus"] = result.get("career_focus", "Software Engineer")
    except Exception as e:
        state["error"] = f"analyze_profile failed: {str(e)}"
    return state

def identify_skill_gaps(state: RoadmapState) -> RoadmapState:
    try:
        user_prof = state["user_profile"]
        analysis = state.get("skill_analysis", {})
        system_prompt = """You are a career advisor. Return a JSON array of 3-5 skill gap objects.
Each object MUST have exactly these keys:
- skill (string)
- current_level ("beginner" | "intermediate" | "advanced" | "expert")
- target_level ("beginner" | "intermediate" | "advanced" | "expert")
- gap_size ("small" | "medium" | "large")
- learning_path (list of 3 strings)"""
        user_prompt = f"User: {json.dumps(user_prof)}\nAnalysis: {json.dumps(analysis)}"
        result = _invoke_llm(system_prompt, user_prompt)
        state["skill_gaps_raw"] = result if isinstance(result, list) else []
    except Exception as e:
        state["error"] = f"identify_skill_gaps failed: {str(e)}"
    return state

def generate_phases(state: RoadmapState) -> RoadmapState:
    try:
        user_prof = state["user_profile"]
        analysis = state.get("skill_analysis", {})
        gaps = state.get("skill_gaps_raw", [])
        
        system_prompt = """You are a career advisor building a detailed roadmap.
Return a JSON array of phase objects.
Each phase MUST have exactly:
- name (string)
- description (string)
- duration (string e.g. "4-6 weeks")
- objectives (list of 3-4 strings)
- milestones (list of 2-4 milestone objects)

Each milestone MUST have exactly:
- id (string e.g. "p1_m1")
- title (string)
- description (string)
- type ("learning" | "project" | "certification" | "experience" | "networking" | "application")
- phase (string matching parent phase name)
- estimated_duration (string)
- prerequisites (list of milestone id strings)
- skills_developed (list of strings)
- resources (list of objects with {title, url} - url MUST be a search term or safe URL)
- difficulty ("beginner" | "intermediate" | "advanced" | "expert")
- priority (integer 1-3)
- dependencies (list of milestone id strings)
- sub_tasks (list of 2-3 sub_task objects)

Each sub_task MUST have exactly:
- task_title (string)
- description (string)
- estimated_time (string)
- resource_type ("course" | "video" | "documentation" | "project" | "practice")
- resource_title (string)
- resource_url (string)
"""
        user_prompt = (f"User: {json.dumps(user_prof)}\n"
                       f"Analysis: {json.dumps(analysis)}\n"
                       f"Gaps: {json.dumps(gaps)}")
        result = _invoke_llm(system_prompt, user_prompt)
        state["phases_raw"] = result if isinstance(result, list) else []
    except Exception as e:
        state["error"] = f"generate_phases failed: {str(e)}"
    return state

def enrich_resources(state: RoadmapState) -> RoadmapState:
    try:
        phases = state.get("phases_raw", [])
        # We process phases directly instead of an LLM call for time/cost unless requested.
        # However, the instruction asks to use LLM to enrich milestones with < 2 sub_tasks.
        
        needs_enrichment = []
        for p_idx, p in enumerate(phases):
            for m_idx, m in enumerate(p.get("milestones", [])):
                if len(m.get("sub_tasks", [])) < 2:
                    needs_enrichment.append((p_idx, m_idx, m))
                    
        if needs_enrichment:
            system_prompt = """For the provided milestones, generate additional sub_tasks with real, well-known resources (freeCodeCamp, NPTEL, Coursera, official docs, YouTube channels).
Return a JSON object where keys are milestone IDs and values are lists of fully formed sub_task objects (same format as original sub_tasks)."""
            user_prompt = json.dumps([{"id": x[2].get("id"), "title": x[2].get("title")} for x in needs_enrichment])
            enrich_result = _invoke_llm(system_prompt, user_prompt)
            
            for p_idx, m_idx, m in needs_enrichment:
                m_id = str(m.get("id", ""))
                if m_id in enrich_result:
                    phases[p_idx]["milestones"][m_idx]["sub_tasks"].extend(enrich_result[m_id])
                    
        state["phases_raw"] = phases
    except Exception as e:
        state["error"] = f"enrich_resources failed: {str(e)}"
    return state

def fallback_node(state: RoadmapState) -> RoadmapState:
    """Fallback if any LLM node fails. Constructs hardcoded valid data."""
    state["error"] = None
    state["career_focus"] = "Technology Professional"
    state["skill_gaps_raw"] = [
        {
            "skill": "Core Programming",
            "current_level": "beginner",
            "target_level": "advanced",
            "gap_size": "medium",
            "learning_path": ["Basic Syntax", "Data Structures", "Algorithms"]
        },
        {
            "skill": "System Design",
            "current_level": "beginner",
            "target_level": "intermediate",
            "gap_size": "large",
            "learning_path": ["Architecture Patterns", "Databases", "Scalability"]
        }
    ]
    state["phases_raw"] = [
        {
            "name": "Phase 1: Foundations",
            "description": "Build core technical skills.",
            "duration": "4 weeks",
            "objectives": ["Understand basics", "Setup environment", "Write simple scripts"],
            "milestones": [
                {
                    "id": "p1_m1",
                    "title": "Programming Basics",
                    "description": "Learn syntax and control structures.",
                    "type": "learning",
                    "phase": "Phase 1: Foundations",
                    "estimated_duration": "2 weeks",
                    "prerequisites": [],
                    "skills_developed": ["Coding"],
                    "resources": [{"title": "Official Docs", "url": "https://docs.python.org/"}],
                    "difficulty": "beginner",
                    "priority": 1,
                    "dependencies": [],
                    "sub_tasks": [
                        {
                            "task_title": "Hello World",
                            "description": "Write first program",
                            "estimated_time": "2 hours",
                            "resource_type": "documentation",
                            "resource_title": "Python Setup",
                            "resource_url": "python setup"
                        },
                        {
                            "task_title": "Variables and Loops",
                            "description": "Practice basic logic",
                            "estimated_time": "5 hours",
                            "resource_type": "practice",
                            "resource_title": "HackerRank basics",
                            "resource_url": "hackerrank"
                        }
                    ]
                },
                {
                    "id": "p1_m2",
                    "title": "Basic Project",
                    "description": "Apply foundations to a small project.",
                    "type": "project",
                    "phase": "Phase 1: Foundations",
                    "estimated_duration": "2 weeks",
                    "prerequisites": ["p1_m1"],
                    "skills_developed": ["Problem Solving"],
                    "resources": [{"title": "GitHub", "url": "github"}],
                    "difficulty": "beginner",
                    "priority": 2,
                    "dependencies": ["p1_m1"],
                    "sub_tasks": [
                        {
                            "task_title": "Project Setup",
                            "description": "Initialize repository",
                            "estimated_time": "1 hour",
                            "resource_type": "documentation",
                            "resource_title": "Git Guide",
                            "resource_url": "git init"
                        },
                        {
                            "task_title": "Implementation",
                            "description": "Code the logic",
                            "estimated_time": "10 hours",
                            "resource_type": "project",
                            "resource_title": "Project Coding",
                            "resource_url": "vscode"
                        }
                    ]
                }
            ]
        },
        {
            "name": "Phase 2: Intermediate",
            "description": "Deepen technical expertise.",
            "duration": "6 weeks",
            "objectives": ["Build real app", "Learn frameworks"],
            "milestones": [
                {
                    "id": "p2_m1",
                    "title": "Web Frameworks",
                    "description": "Learn backend tools.",
                    "type": "learning",
                    "phase": "Phase 2: Intermediate",
                    "estimated_duration": "3 weeks",
                    "prerequisites": ["p1_m2"],
                    "skills_developed": ["Backend"],
                    "resources": [],
                    "difficulty": "intermediate",
                    "priority": 2,
                    "dependencies": [],
                    "sub_tasks": [
                        {
                            "task_title": "API Basics",
                            "description": "REST APIs",
                            "estimated_time": "10 hours",
                            "resource_type": "course",
                            "resource_title": "FastAPI Course",
                            "resource_url": "fastapi tutorial"
                        },
                        {
                            "task_title": "Database Integration",
                            "description": "Connect to SQL",
                            "estimated_time": "15 hours",
                            "resource_type": "documentation",
                            "resource_title": "SQLAlchemy",
                            "resource_url": "sqlalchemy docs"
                        }
                    ]
                }
            ]
        },
        {
            "name": "Phase 3: Career Ready",
            "description": "Prepare for the job market.",
            "duration": "4 weeks",
            "objectives": ["Portfolio", "Interviews"],
            "milestones": [
                {
                    "id": "p3_m1",
                    "title": "Portfolio Polish",
                    "description": "Host projects.",
                    "type": "application",
                    "phase": "Phase 3: Career Ready",
                    "estimated_duration": "2 weeks",
                    "prerequisites": ["p2_m1"],
                    "skills_developed": ["Deployment"],
                    "resources": [],
                    "difficulty": "advanced",
                    "priority": 1,
                    "dependencies": [],
                    "sub_tasks": [
                        {
                            "task_title": "Deploy App",
                            "description": "Host on Cloud",
                            "estimated_time": "5 hours",
                            "resource_type": "video",
                            "resource_title": "Deployment guide",
                            "resource_url": "vercel deploy"
                        },
                        {
                            "task_title": "Resume Writing",
                            "description": "Format resume",
                            "estimated_time": "3 hours",
                            "resource_type": "documentation",
                            "resource_title": "Resume tips",
                            "resource_url": "resume templates"
                        }
                    ]
                }
            ]
        }
    ]
    return state

def assemble_response(state: RoadmapState) -> RoadmapState:
    try:
        user_name = state["user_profile"].get("name", "User")
        
        # Build phases
        phases_out = []
        total_milestones = 0
        raw_phases = state.get("phases_raw", [])
        for p in raw_phases:
            milestones_out = []
            for m in p.get("milestones", []):
                sub_tasks_out = []
                for st in m.get("sub_tasks", []):
                    try:
                        sub_tasks_out.append(SubTask(
                            task_title=st.get("task_title", "Task"),
                            description=st.get("description", ""),
                            estimated_time=st.get("estimated_time", "Unknown"),
                            resource_type=st.get("resource_type", "documentation"),
                            resource_title=st.get("resource_title", ""),
                            resource_url=st.get("resource_url", "")
                        ))
                    except Exception:
                        pass
                
                try:
                    diff_val = str(m.get("difficulty", "beginner")).lower()
                    if diff_val not in ["beginner", "intermediate", "advanced", "expert"]:
                        diff_val = "beginner"
                    
                    type_val = str(m.get("type", "learning")).lower()
                    if type_val not in ["learning", "project", "certification", "experience", "networking", "application"]:
                        type_val = "learning"
                        
                    milestones_out.append(Milestone(
                        id=str(m.get("id", "m1")),
                        title=str(m.get("title", "Milestone")),
                        description=str(m.get("description", "")),
                        type=type_val,
                        phase=str(m.get("phase", p.get("name", ""))),
                        estimated_duration=str(m.get("estimated_duration", "1 week")),
                        prerequisites=m.get("prerequisites", []),
                        skills_developed=m.get("skills_developed", []),
                        resources=m.get("resources", []),
                        sub_tasks=sub_tasks_out,
                        difficulty=diff_val,
                        priority=int(m.get("priority", 1)),
                        dependencies=m.get("dependencies", [])
                    ))
                    total_milestones += 1
                except Exception:
                    pass
            
            try:
                phases_out.append(RoadmapPhase(
                    name=str(p.get("name", "Phase")),
                    description=str(p.get("description", "")),
                    duration=str(p.get("duration", "")),
                    milestones=milestones_out,
                    objectives=p.get("objectives", [])
                ))
            except Exception:
                pass

        # Build skill gaps
        gaps_out = []
        for g in state.get("skill_gaps_raw", []):
            try:
                curr_level = str(g.get("current_level", "beginner")).lower()
                tar_level = str(g.get("target_level", "intermediate")).lower()
                for lvl in [curr_level, tar_level]:
                    if lvl not in ["beginner", "intermediate", "advanced", "expert"]:
                        lvl = "beginner"
                        
                gaps_out.append(SkillGap(
                    skill=str(g.get("skill", "Skill")),
                    current_level=curr_level,
                    target_level=tar_level,
                    gap_size=str(g.get("gap_size", "medium")),
                    learning_path=g.get("learning_path", [])
                ))
            except Exception:
                pass
                
        # Generate Mermaid
        import re
        def sanitize_id(s):
            return re.sub(r'[^a-zA-Z0-9]', '_', str(s))

        type_emoji = {
            "learning": "📚", "project": "🔨", "certification": "🏆",
            "experience": "💼", "networking": "🤝", "application": "📝"
        }
        
        diagram = "%%{init: {'theme': 'base', 'themeVariables': {\n"
        diagram += "  'primaryColor': '#EEF2FF',\n"
        diagram += "  'primaryTextColor': '#1A1A1A',\n"
        diagram += "  'primaryBorderColor': '#2D5BE3',\n"
        diagram += "  'lineColor': '#2D5BE3',\n"
        diagram += "  'secondaryColor': '#F5F4F0',\n"
        diagram += "  'tertiaryColor': '#ECEAE4',\n"
        diagram += "  'fontFamily': '-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif',\n"
        diagram += "  'fontSize': '14px'\n"
        diagram += "}}}%%\ngraph TD\n"

        for pi, ph in enumerate(phases_out):
            safe_phase = sanitize_id(ph.name)
            diagram += f'  subgraph {safe_phase}["{ph.name} ({ph.duration})"]\n'
            
            for m in ph.milestones:
                safe_id = sanitize_id(m.id)
                emoji = type_emoji.get(str(m.type).lower() if m.type else "", "📋")
                clean_title = m.title.replace('"', "'")
                clean_dur = m.estimated_duration.replace('"', "'")
                diagram += f'    {safe_id}["{emoji} {clean_title}\\n{clean_dur}"]\n'
            
            for i, m in enumerate(ph.milestones):
                safe_id = sanitize_id(m.id)
                if m.prerequisites and len(m.prerequisites) > 0:
                    for prereq in m.prerequisites:
                        safe_prereq = sanitize_id(prereq)
                        diagram += f'    {safe_prereq} --> {safe_id}\n'
                elif i > 0:
                    prev_id = sanitize_id(ph.milestones[i-1].id)
                    diagram += f'    {prev_id} --> {safe_id}\n'
            
            diagram += "  end\n"
            if pi < len(phases_out) - 1:
                next_phase = sanitize_id(phases_out[pi+1].name)
                diagram += f'  {safe_phase} --> {next_phase}\n'
                
        mermaid_str = diagram
        
        # Summary
        summary = {
            "title": f"{target_focus} Roadmap",
            "description": "Your customized career path.",
            "total_duration": f"{len(phases_out) * 4} weeks approx",
            "phases_count": len(phases_out),
            "milestones_count": total_milestones
        }
        
        state["roadmap_response"] = {
            "user": user_name,
            "phases": [p.model_dump() for p in phases_out],
            "skill_gaps": [g.model_dump() for g in gaps_out],
            "mermaid": mermaid_str,
            "summary": summary,
            "generated_at": datetime.now().isoformat(),
            "debug": {"mode": "langgraph"}
        }
    except Exception as e:
        state["error"] = f"assemble_response failed: {str(e)}"
    return state

# ─── 1C. GRAPH EDGES ─────────────────────────────────────
def build_graph() -> StateGraph:
    workflow = StateGraph(RoadmapState)

    workflow.add_node("analyze_profile", analyze_profile)
    workflow.add_node("identify_skill_gaps", identify_skill_gaps)
    workflow.add_node("generate_phases", generate_phases)
    workflow.add_node("enrich_resources", enrich_resources)
    workflow.add_node("assemble_response", assemble_response)
    workflow.add_node("fallback_node", fallback_node)

    workflow.add_edge(START, "analyze_profile")
    
    def condition_analyze(state: RoadmapState):
        return "fallback_node" if state.get("error") else "identify_skill_gaps"
    workflow.add_conditional_edges("analyze_profile", condition_analyze)
    
    def condition_gaps(state: RoadmapState):
        return "fallback_node" if state.get("error") else "generate_phases"
    workflow.add_conditional_edges("identify_skill_gaps", condition_gaps)
    
    def condition_phases(state: RoadmapState):
        return "fallback_node" if state.get("error") else "enrich_resources"
    workflow.add_conditional_edges("generate_phases", condition_phases)

    def condition_enrich(state: RoadmapState):
        return "assemble_response"
    workflow.add_conditional_edges("enrich_resources", condition_enrich)
    
    # Fallback always goes to assemble
    workflow.add_edge("fallback_node", "assemble_response")
    workflow.add_edge("assemble_response", END)
    
    return workflow.compile()

graph = build_graph()

# ─── 1D. PUBLIC ENTRY POINT ──────────────────────────────
def generate_roadmap(user: UserProfile, careers_map: dict) -> RoadmapResponse:
    if "GOOGLE_API_KEY" not in os.environ:
        print("GOOGLE_API_KEY not found. Using fallback immediately.")
        initial_state = {"user_profile": user.model_dump(), "error": "No API Key"}
        state = fallback_node(initial_state)
        state = assemble_response(state)
        return RoadmapResponse(**state["roadmap_response"])
        
    initial_state: RoadmapState = {
        "user_profile": user.model_dump(),
        "career_focus": "",
        "skill_analysis": {},
        "phases_raw": [],
        "skill_gaps_raw": [],
        "roadmap_response": {},
        "error": None,
        "retry_count": 0
    }
    
    try:
        final_state = graph.invoke(initial_state)
        # If assemble_response failed or error happened at the end
        if final_state.get("error"):
            raise ValueError(final_state["error"])
        
        # Pydantic validates and constructs the final objects from the dict
        return RoadmapResponse(**final_state["roadmap_response"])
    except Exception as e:
        print(f"Graph execution entirely failed: {e}. Running direct fallback.")
        state = fallback_node(initial_state)
        state = assemble_response(state)
        return RoadmapResponse(**state["roadmap_response"])