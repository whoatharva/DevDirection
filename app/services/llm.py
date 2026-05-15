import os
import json
from typing import Dict, List, Optional, Any, TypedDict
from datetime import datetime

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langgraph.graph import StateGraph, START, END

from app.models import UserProfile, RoadmapResponse, RoadmapPhase, Milestone, SubTask, SkillGap, SkillLevel, MilestoneType

from langgraph.checkpoint.memory import MemorySaver

# ─── 1A. STATE DEFINITION ───────────────────────────────
class RoadmapState(TypedDict):
    user_profile: dict
    career_focus: str
    skill_analysis: dict
    phases_raw: list
    skill_gaps_raw: list
    roadmap_response: dict
    error: Optional[str]
    critique_feedback: Optional[str]
    score: int
    retry_count: int

# ─── HELPER FOR LLM GENERATION ───────────────────────────
def _invoke_llm(system_prompt: str, user_prompt: str) -> dict:
    # Try Azure OpenAI first (High Quota)
    try:
        azure_llm = AzureChatOpenAI(
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-5-chat-1"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01-preview"),
            temperature=0.3
        )
        parser = JsonOutputParser()
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}")
        ])
        chain = prompt | azure_llm | parser
        return chain.invoke({"input": user_prompt})
    except Exception as az_e:
        print(f"Azure OpenAI failed: {az_e}. Falling back to Gemini...")
        
    # Fallback to Gemini
    models_to_try = [
        "gemini-1.5-flash", 
        "gemini-1.5-flash-latest", 
        "gemini-1.5-flash-8b",
        "gemini-1.5-pro", 
        "gemini-pro"
    ]
    parser = JsonOutputParser()
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}")
    ])
    
    last_error = None
    for model_name in models_to_try:
        try:
            llm = ChatGoogleGenerativeAI(model=model_name, temperature=0.3)
            chain = prompt | llm | parser
            return chain.invoke({"input": user_prompt})
        except Exception as e:
            last_error = e
            err_msg = str(e)
            if any(x in err_msg for x in ["404", "NotFound", "429", "ResourceExhausted", "quota"]):
                print(f"Model {model_name} failed. Trying next...")
                continue 
            raise 
    
    raise last_error 

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
        
        system_prompt = """You are a Curriculum Agent building a detailed roadmap skeleton.
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
- difficulty ("beginner" | "intermediate" | "advanced" | "expert")
- priority (integer 1-3)
- dependencies (list of milestone id strings)
"""
        user_prompt = (f"User: {json.dumps(user_prof)}\n"
                       f"Analysis: {json.dumps(analysis)}\n"
                       f"Gaps: {json.dumps(gaps)}")
                       
        critique = state.get("critique_feedback")
        if critique and state.get("phases_raw"):
            previous_phases = json.dumps(state.get("phases_raw"))
            user_prompt += f"\n\nPREVIOUS GENERATION THAT FAILED:\n{previous_phases}\n\nCRITIQUE TO IMPROVE UPON: {critique}"
            
        result = _invoke_llm(system_prompt, user_prompt)
        state["phases_raw"] = result if isinstance(result, list) else []
    except Exception as e:
        state["error"] = f"generate_phases failed: {str(e)}"
    return state

def critique_roadmap(state: RoadmapState) -> RoadmapState:
    try:
        phases = state.get("phases_raw", [])
        if not phases:
            state["score"] = 0
            state["critique_feedback"] = "No phases generated."
            return state

        system_prompt = """You are an expert career roadmap evaluator. 
Score the provided roadmap phases from 1-10 based on logical progression, completeness, and realism.
Return JSON exactly like:
{{
  "score": 8,
  "feedback": "Missing real-world project in Phase 2."
}}"""
        user_prompt = json.dumps(phases)
        result = _invoke_llm(system_prompt, user_prompt)
        
        state["score"] = int(result.get("score", 0))
        state["critique_feedback"] = result.get("feedback", "")
        
        # If score is failing, increment retry count here in the node, not the edge!
        if state["score"] < 8:
            state["retry_count"] = state.get("retry_count", 0) + 1
            
    except Exception as e:
        state["error"] = f"critique_roadmap failed: {str(e)}"
        state["score"] = 10 # fail open
    return state

def enrich_resources(state: RoadmapState) -> RoadmapState:
    try:
        phases = state.get("phases_raw", [])
        
        all_milestones = []
        for p_idx, p in enumerate(phases):
            for m_idx, m in enumerate(p.get("milestones", [])):
                all_milestones.append((p_idx, m_idx, m))
                
        if all_milestones:
            system_prompt = """You are a Resource Generation Agent. For the provided milestones, generate granular sub_tasks with real, well-known resources (freeCodeCamp, NPTEL, Coursera, official docs, YouTube channels).
Return a JSON object where keys are milestone IDs and values are lists of 2-3 sub_task objects.
Each sub_task MUST have exactly:
- task_title (string)
- description (string)
- estimated_time (string)
- resource_type ("course" | "video" | "documentation" | "project" | "practice")
- resource_title (string)
- resource_url (string)"""
            user_prompt = json.dumps([{"id": x[2].get("id"), "title": x[2].get("title")} for x in all_milestones])
            enrich_result = _invoke_llm(system_prompt, user_prompt)
            
            for p_idx, m_idx, m in all_milestones:
                m_id = str(m.get("id", ""))
                if m_id in enrich_result:
                    m["sub_tasks"] = enrich_result[m_id]
                    phases[p_idx]["milestones"][m_idx] = m
                    
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
                    sub_tasks_out.append(SubTask(
                        task_title=st.get("task_title", "Task"),
                        description=st.get("description", "Task description"),
                        estimated_time=st.get("estimated_time", "Unknown"),
                        resource_type=st.get("resource_type", "documentation"),
                        resource_title=st.get("resource_title", "Resource"),
                        resource_url=st.get("resource_url", "#")
                    ))
                
                diff_val = str(m.get("difficulty", "beginner")).lower()
                if diff_val not in ["beginner", "intermediate", "advanced", "expert"]:
                    diff_val = "beginner"
                
                type_val = str(m.get("type", "learning")).lower()
                if type_val not in ["learning", "project", "certification", "experience", "networking", "application"]:
                    type_val = "learning"
                    
                milestones_out.append(Milestone(
                    id=str(m.get("id", "m1")),
                    title=str(m.get("title", "Milestone")),
                    description=str(m.get("description", "Milestone description")),
                    type=type_val,
                    phase=str(m.get("phase", p.get("name", "Phase"))),
                    estimated_duration=str(m.get("estimated_duration", "1 week")),
                    prerequisites=m.get("prerequisites", []),
                    skills_developed=m.get("skills_developed", []),
                    resources=m.get("resources", []),
                    sub_tasks=sub_tasks_out,
                    difficulty=diff_val,
                    priority=int(m.get("priority", 1) or 1),
                    dependencies=m.get("dependencies", [])
                ))
                total_milestones += 1
            
            phases_out.append(RoadmapPhase(
                name=str(p.get("name", "Phase")),
                description=str(p.get("description", "Phase description")),
                duration=str(p.get("duration", "4 weeks")),
                milestones=milestones_out,
                objectives=p.get("objectives", [])
            ))

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
            "title": f"{state.get('career_focus', 'Career')} Roadmap",
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
    workflow.add_node("critique_roadmap", critique_roadmap)
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
    
    workflow.add_edge("generate_phases", "critique_roadmap")

    def route_critique(state: RoadmapState):
        if state.get("error"):
            return "fallback_node"
        # Since retry_count was incremented in critique_roadmap, we just check its current value
        if state.get("score", 0) < 8 and state.get("retry_count", 0) <= 2:
            return "generate_phases"
        return "enrich_resources"
    workflow.add_conditional_edges("critique_roadmap", route_critique)

    def condition_enrich(state: RoadmapState):
        return "assemble_response"
    workflow.add_conditional_edges("enrich_resources", condition_enrich)
    
    # Fallback always goes to assemble
    workflow.add_edge("fallback_node", "assemble_response")
    workflow.add_edge("assemble_response", END)
    
    memory = MemorySaver()
    return workflow.compile(checkpointer=memory, interrupt_before=["assemble_response"])

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
    
    import uuid
    session_id = f"{user.user_id}_{uuid.uuid4().hex[:8]}"
    config = {"configurable": {"thread_id": session_id}}
    
    try:
        # Run graph until interrupt or end
        final_state = graph.invoke(initial_state, config=config)
        
        # Human-in-the-loop pause handling: If it stopped before assemble_response, resume it.
        # In a real app, you'd wait for user input here before resuming.
        state_snapshot = graph.get_state(config)
        if state_snapshot.next:
            final_state = graph.invoke(None, config=config)

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

# ─── 1E. STREAMING & RESUME ENTRY POINTS (SSE) ──────────────────
def generate_roadmap_stream(user: UserProfile):
    import json
    import uuid
    import os
    if "GOOGLE_API_KEY" not in os.environ:
        yield f"data: {json.dumps({'event': 'error', 'message': 'GOOGLE_API_KEY not found.'})}\n\n"
        return

    initial_state: dict = {
        "user_profile": user.model_dump(),
        "career_focus": "",
        "skill_analysis": {},
        "phases_raw": [],
        "skill_gaps_raw": [],
        "roadmap_response": {},
        "error": None,
        "retry_count": 0
    }
    
    session_id = f"{user.user_id}_{uuid.uuid4().hex[:8]}"
    config = {"configurable": {"thread_id": session_id}}
    
    try:
        for chunk in graph.stream(initial_state, config=config, stream_mode="updates"):
            # Handle newer langgraph versions that might yield (node_name, state_dict) tuples directly
            if isinstance(chunk, tuple) and len(chunk) == 2:
                chunk = {chunk[0]: chunk[1]}
                
            for node_name, state_update in chunk.items():
                if not isinstance(state_update, dict):
                    if isinstance(state_update, tuple) and len(state_update) > 0 and isinstance(state_update[0], dict):
                        state_update = state_update[0]
                    else:
                        continue # Safely skip unparseable state chunks to prevent stream crash
                        
                event_data = {
                    "node": node_name,
                    "score": state_update.get("score", 0),
                    "retry_count": state_update.get("retry_count", 0),
                    "error": state_update.get("error", None)
                }
                yield f"data: {json.dumps(event_data)}\n\n"
        
        # When graph stops (either due to interrupt or end)
        state_snapshot = graph.get_state(config)
        if state_snapshot.next:
            # It paused at human-in-the-loop
            yield f"data: {json.dumps({'node': '__paused__', 'thread_id': session_id, 'phases_raw': state_snapshot.values.get('phases_raw', [])})}\n\n"
        else:
            # Finished normally
            yield f"data: {json.dumps({'node': '__end__', 'roadmap_response': state_snapshot.values.get('roadmap_response', {})})}\n\n"

    except Exception as e:
        yield f"data: {json.dumps({'event': 'error', 'message': str(e)})}\n\n"

def resume_roadmap_stream(thread_id: str):
    import json
    config = {"configurable": {"thread_id": thread_id}}
    try:
        for chunk in graph.stream(None, config=config):
            for node_name, state_update in chunk.items():
                event_data = {
                    "node": node_name,
                    "score": state_update.get("score", 0),
                    "retry_count": state_update.get("retry_count", 0),
                    "error": state_update.get("error", None)
                }
                yield f"data: {json.dumps(event_data)}\n\n"
                
        state_snapshot = graph.get_state(config)
        yield f"data: {json.dumps({'node': '__end__', 'roadmap_response': state_snapshot.values.get('roadmap_response', {})})}\n\n"
    except Exception as e:
        yield f"data: {json.dumps({'event': 'error', 'message': str(e)})}\n\n"

def answer_roadmap_question(user_id: str, question: str) -> str:
    """Answers a user's question about their generated roadmap using a basic Gemini chain."""
    try:
        from langchain_openai import AzureChatOpenAI
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_core.output_parsers import StrOutputParser
        
        system_prompt = """You are 'Mentor AI', an expert career advisor. 
You are currently helping a user understand a career roadmap that was just generated for them.
Answer relevant questions about career, tech, and the roadmap concisely and warmly. 
If a question is totally irrelevant (jokes, politics, etc.), politely steer the user back to their career path.
Keep response under 4 sentences. Do NOT use markdown code blocks for the entire message."""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}")
        ])
        parser = StrOutputParser()

        # Try Azure first
        try:
            azure_llm = AzureChatOpenAI(
                azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-5-chat-1"),
                api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01-preview"),
                temperature=0.7
            )
            chain = prompt | azure_llm | parser
            return chain.invoke({"input": question})
        except Exception as az_e:
            print(f"Chatbot Azure failed: {az_e}")

        # Fallback to Gemini
        models_to_try = [
            "gemini-1.5-flash", 
            "gemini-1.5-flash-latest", 
            "gemini-1.5-pro"
        ]
        
        last_error = None
        for model_name in models_to_try:
            try:
                from langchain_google_genai import ChatGoogleGenerativeAI
                llm = ChatGoogleGenerativeAI(model=model_name, temperature=0.7)
                chain = prompt | llm | parser
                return chain.invoke({"input": question})
            except Exception as e:
                last_error = e
                err_msg = str(e)
                if any(x in err_msg for x in ["404", "NotFound", "429", "ResourceExhausted", "quota"]):
                    continue
                raise
                
        if last_error:
            raise last_error
            
    except Exception as e:
        return f"I'm sorry, I'm having trouble connecting right now. ({str(e)})"