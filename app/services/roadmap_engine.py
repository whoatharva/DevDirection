"""
Roadmap Engine - Handles AI-powered roadmap generation
"""

from datetime import datetime
from typing import Dict, Any, List
from app.models import UserProfile, Milestone, SubTask, RoadmapPhase, SkillGap, MilestoneType, SkillLevel
from app.services.subtask_resources import get_subtasks_for_milestone


class RoadmapEngine:
    """Engine for generating AI-powered career roadmaps"""
    
    def generate_roadmap(self, user: UserProfile) -> Dict[str, Any]:
        """Generate a comprehensive career roadmap for a user"""
        # Determine career focus based on user profile
        career_focus = self._determine_career_focus(user)
        
        # Create comprehensive milestones for each phase
        milestones_phase1 = self._create_foundation_milestones(career_focus)
        milestones_phase2 = self._create_development_milestones(career_focus)
        milestones_phase3 = self._create_advanced_milestones(career_focus)
        milestones_phase4 = self._create_specialization_milestones(career_focus)

        # Attach sub-tasks with real learning resources to every milestone
        all_milestones = milestones_phase1 + milestones_phase2 + milestones_phase3 + milestones_phase4
        for ms in all_milestones:
            raw_tasks = get_subtasks_for_milestone(ms.id, career_focus)
            ms.sub_tasks = [SubTask(**st) for st in raw_tasks]
        
        # Create phases with proper structure
        phases = [
            RoadmapPhase(
                name="Foundation & Fundamentals",
                description="Build strong foundational knowledge and core skills",
                duration="4-6 weeks",
                milestones=milestones_phase1,
                objectives=[
                    "Master fundamental concepts",
                    "Set up professional development environment",
                    "Build strong theoretical foundation",
                    "Develop learning habits and study routines"
                ]
            ),
            RoadmapPhase(
                name="Core Development",
                description="Develop practical skills through hands-on projects",
                duration="6-8 weeks",
                milestones=milestones_phase2,
                objectives=[
                    "Apply concepts through practical projects",
                    "Build problem-solving capabilities",
                    "Develop technical proficiency",
                    "Create initial portfolio pieces"
                ]
            ),
            RoadmapPhase(
                name="Advanced Skills",
                description="Master advanced concepts and build complex projects",
                duration="8-10 weeks",
                milestones=milestones_phase3,
                objectives=[
                    "Master advanced techniques",
                    "Build complex, real-world projects",
                    "Develop expertise in chosen specialization",
                    "Create comprehensive portfolio"
                ]
            ),
            RoadmapPhase(
                name="Specialization & Mastery",
                description="Achieve mastery in specific areas and prepare for career",
                duration="6-8 weeks",
                milestones=milestones_phase4,
                objectives=[
                    "Achieve expert-level proficiency",
                    "Build industry-ready projects",
                    "Develop professional network",
                    "Prepare for job applications and interviews"
                ]
            )
        ]
        
        # Create skill gaps
        skill_gaps = [
            SkillGap(
                skill="Communication",
                current_level=SkillLevel.BEGINNER,
                target_level=SkillLevel.INTERMEDIATE,
                gap_size="medium",
                learning_path=["Practice presentations", "Join discussion groups", "Write technical blogs"]
            ),
            SkillGap(
                skill="Problem Solving",
                current_level=SkillLevel.BEGINNER,
                target_level=SkillLevel.INTERMEDIATE,
                gap_size="medium",
                learning_path=["Solve coding challenges", "Work on real projects", "Study algorithms"]
            )
        ]
        
        # Generate hierarchical structure for D3.js visualization
        hierarchical_structure = self._generate_hierarchical_structure(user, phases)
        
        result = {
            "user": user.user_id,  # Changed from user.model_dump() to just user_id
            "phases": [phase.model_dump() for phase in phases],
            "skill_gaps": [gap.model_dump() for gap in skill_gaps],
            "mermaid": self._generate_mermaid_diagram(phases),
            "summary": {
                "title": f"Career Roadmap for {user.name}",
                "description": f"Personalized career roadmap focusing on {', '.join(user.career_goals[:3]) if user.career_goals else 'career development'}",
                "total_duration": "6-12 weeks",
                "phases_count": len(phases),
                "milestones_count": sum(len(phase.milestones) for phase in phases)
            },
            "generated_at": datetime.utcnow().isoformat(),
            "debug": {
                "engine": "RoadmapEngine", 
                "version": "2.0.0",
                "hierarchical_structure": hierarchical_structure
            }
        }

        # Post-process: inject sub-tasks with real resources into serialized phases
        for phase_dict in result["phases"]:
            for ms_dict in phase_dict.get("milestones", []):
                raw_tasks = get_subtasks_for_milestone(ms_dict["id"], career_focus)
                ms_dict["sub_tasks"] = raw_tasks

        return result
    
    def _generate_mermaid_diagram(self, phases: List[RoadmapPhase]) -> str:
        """Generate Mermaid diagram for roadmap visualization"""
        import re
        def sanitize_id(s):
            return re.sub(r'[^a-zA-Z0-9]', '_', str(s))

        type_emoji = {
            "learning": "📚", "project": "🔨", "certification": "🏆",
            "experience": "💼", "networking": "🤝", "application": "📝",
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

        for pi, ph in enumerate(phases):
            safe_phase = sanitize_id(ph.name)
            diagram += f'  subgraph {safe_phase}["{ph.name} ({ph.duration})"]\n'
            
            for m in ph.milestones:
                safe_id = sanitize_id(m.id)
                m_type_str = str(m.type.value if hasattr(m.type, 'value') else m.type).lower()
                emoji = type_emoji.get(m_type_str, "📋")
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
            if pi < len(phases) - 1:
                next_phase = sanitize_id(phases[pi+1].name)
                diagram += f'  {safe_phase} --> {next_phase}\n'
                
        return diagram
    
    def _generate_hierarchical_structure(self, user: UserProfile, phases: List[RoadmapPhase]) -> Dict[str, Any]:
        """Generate hierarchical structure for D3.js visualization"""
        nodes = [
            {
                "id": "root",
                "name": f"{user.name}'s Career Roadmap",
                "description": f"Career roadmap for {user.name}",
                "type": "root",
                "level": 0,
                "data": {"user_id": user.user_id}
            }
        ]
        
        links = []
        
        # Add phases as nodes
        for phase_idx, phase in enumerate(phases):
            phase_id = f"phase_{phase_idx + 1}"
            nodes.append({
                "id": phase_id,
                "name": phase.name,
                "description": phase.description,
                "type": "phase",
                "level": 1,
                "data": {"duration": phase.duration}
            })
            links.append({"source": "root", "target": phase_id})
            
            # Add milestones as nodes
            for milestone in phase.milestones:
                milestone_id = milestone.id
                nodes.append({
                    "id": milestone_id,
                    "name": milestone.title,
                    "description": milestone.description,
                    "type": "milestone",
                    "level": 2,
                    "data": {"duration": milestone.estimated_duration, "difficulty": milestone.difficulty.value}
                })
                links.append({"source": phase_id, "target": milestone_id})
                
                # Add skills as nodes
                for skill in milestone.skills_developed:
                    skill_id = f"{milestone_id}_{skill.replace(' ', '_').lower()}"
                    nodes.append({
                        "id": skill_id,
                        "name": skill,
                        "description": f"Develop {skill.lower()}",
                        "type": "skill",
                        "level": 3,
                        "data": {}
                    })
                    links.append({"source": milestone_id, "target": skill_id})
        
        return {
            "nodes": nodes,
            "links": links
        }
    
    def _determine_career_focus(self, user: UserProfile) -> str:
        """Determine career focus based on user profile"""
        if user.skills and any(skill.lower() in ['python', 'javascript', 'java', 'programming'] for skill in user.skills):
            return "software_development"
        elif user.skills and any(skill.lower() in ['data', 'analysis', 'statistics', 'machine learning'] for skill in user.skills):
            return "data_science"
        elif user.skills and any(skill.lower() in ['design', 'ui', 'ux', 'graphic'] for skill in user.skills):
            return "design"
        elif user.skills and any(skill.lower() in ['business', 'management', 'marketing'] for skill in user.skills):
            return "business"
        else:
            return "general_tech"
    
    def _create_foundation_milestones(self, career_focus: str) -> List[Milestone]:
        """Create foundation phase milestones based on career focus"""
        if career_focus == "software_development":
            return [
                Milestone(
                    id="milestone_1",
                    title="Programming Fundamentals",
                    description="Master core programming concepts, data structures, and algorithms",
                    type=MilestoneType.LEARNING,
                    phase="Foundation",
                    estimated_duration="2-3 weeks",
                    prerequisites=[],
                    skills_developed=["Programming logic", "Data structures", "Algorithms", "Problem solving"],
                    difficulty=SkillLevel.BEGINNER,
                    priority=1
                ),
                Milestone(
                    id="milestone_2",
                    title="Development Environment Setup",
                    description="Set up professional development environment with version control",
                    type=MilestoneType.LEARNING,
                    phase="Foundation",
                    estimated_duration="1 week",
                    prerequisites=[],
                    skills_developed=["Git/GitHub", "IDE setup", "Debugging tools", "Package management"],
                    difficulty=SkillLevel.BEGINNER,
                    priority=1
                ),
                Milestone(
                    id="milestone_3",
                    title="Version Control & Collaboration",
                    description="Learn Git, GitHub, and collaborative development practices",
                    type=MilestoneType.LEARNING,
                    phase="Foundation",
                    estimated_duration="1-2 weeks",
                    prerequisites=["milestone_2"],
                    skills_developed=["Git workflow", "Code review", "Branching strategies", "Documentation"],
                    difficulty=SkillLevel.BEGINNER,
                    priority=2
                )
            ]
        elif career_focus == "data_science":
            return [
                Milestone(
                    id="milestone_1",
                    title="Mathematics & Statistics Foundation",
                    description="Build strong foundation in linear algebra, calculus, and statistics",
                    type=MilestoneType.LEARNING,
                    phase="Foundation",
                    estimated_duration="3-4 weeks",
                    prerequisites=[],
                    skills_developed=["Linear algebra", "Calculus", "Statistics", "Probability"],
                    difficulty=SkillLevel.BEGINNER,
                    priority=1
                ),
                Milestone(
                    id="milestone_2",
                    title="Python for Data Science",
                    description="Master Python programming with focus on data manipulation libraries",
                    type=MilestoneType.LEARNING,
                    phase="Foundation",
                    estimated_duration="2-3 weeks",
                    prerequisites=[],
                    skills_developed=["Python basics", "NumPy", "Pandas", "Matplotlib"],
                    difficulty=SkillLevel.BEGINNER,
                    priority=1
                ),
                Milestone(
                    id="milestone_3",
                    title="Data Analysis Tools",
                    description="Learn Jupyter notebooks, SQL, and data visualization tools",
                    type=MilestoneType.LEARNING,
                    phase="Foundation",
                    estimated_duration="2 weeks",
                    prerequisites=["milestone_2"],
                    skills_developed=["Jupyter", "SQL", "Data visualization", "Data cleaning"],
                    difficulty=SkillLevel.BEGINNER,
                    priority=2
                )
            ]
        else:  # general_tech
            return [
                Milestone(
                    id="milestone_1",
                    title="Technology Fundamentals",
                    description="Understand core technology concepts and digital literacy",
                    type=MilestoneType.LEARNING,
                    phase="Foundation",
                    estimated_duration="2-3 weeks",
                    prerequisites=[],
                    skills_developed=["Computer basics", "Internet literacy", "Digital tools", "Online learning"],
                    difficulty=SkillLevel.BEGINNER,
                    priority=1
                ),
                Milestone(
                    id="milestone_2",
                    title="Problem-Solving Skills",
                    description="Develop analytical thinking and problem-solving methodologies",
                    type=MilestoneType.LEARNING,
                    phase="Foundation",
                    estimated_duration="2 weeks",
                    prerequisites=[],
                    skills_developed=["Critical thinking", "Logical reasoning", "Research skills", "Documentation"],
                    difficulty=SkillLevel.BEGINNER,
                    priority=1
                )
            ]
    
    def _create_development_milestones(self, career_focus: str) -> List[Milestone]:
        """Create development phase milestones based on career focus"""
        if career_focus == "software_development":
            return [
                Milestone(
                    id="milestone_4",
                    title="Web Development Basics",
                    description="Learn HTML, CSS, and JavaScript fundamentals",
                    type=MilestoneType.PROJECT,
                    phase="Development",
                    estimated_duration="3-4 weeks",
                    prerequisites=["milestone_1", "milestone_2"],
                    skills_developed=["HTML5", "CSS3", "JavaScript", "Responsive design"],
                    difficulty=SkillLevel.INTERMEDIATE,
                    priority=1
                ),
                Milestone(
                    id="milestone_5",
                    title="Backend Development",
                    description="Learn server-side programming and database management",
                    type=MilestoneType.PROJECT,
                    phase="Development",
                    estimated_duration="4-5 weeks",
                    prerequisites=["milestone_4"],
                    skills_developed=["Server programming", "Database design", "API development", "Authentication"],
                    difficulty=SkillLevel.INTERMEDIATE,
                    priority=1
                ),
                Milestone(
                    id="milestone_6",
                    title="First Full-Stack Project",
                    description="Build a complete web application from frontend to backend",
                    type=MilestoneType.PROJECT,
                    phase="Development",
                    estimated_duration="3-4 weeks",
                    prerequisites=["milestone_5"],
                    skills_developed=["Full-stack development", "Project management", "Testing", "Deployment"],
                    difficulty=SkillLevel.INTERMEDIATE,
                    priority=2
                )
            ]
        elif career_focus == "data_science":
            return [
                Milestone(
                    id="milestone_4",
                    title="Machine Learning Fundamentals",
                    description="Learn core ML algorithms and implementation",
                    type=MilestoneType.PROJECT,
                    phase="Development",
                    estimated_duration="4-5 weeks",
                    prerequisites=["milestone_1", "milestone_2"],
                    skills_developed=["ML algorithms", "Scikit-learn", "Model evaluation", "Feature engineering"],
                    difficulty=SkillLevel.INTERMEDIATE,
                    priority=1
                ),
                Milestone(
                    id="milestone_5",
                    title="Data Visualization & Analysis",
                    description="Master data visualization and exploratory data analysis",
                    type=MilestoneType.PROJECT,
                    phase="Development",
                    estimated_duration="3-4 weeks",
                    prerequisites=["milestone_3"],
                    skills_developed=["Data visualization", "EDA", "Statistical analysis", "Storytelling"],
                    difficulty=SkillLevel.INTERMEDIATE,
                    priority=1
                ),
                Milestone(
                    id="milestone_6",
                    title="First Data Science Project",
                    description="Complete end-to-end data science project with real data",
                    type=MilestoneType.PROJECT,
                    phase="Development",
                    estimated_duration="4-5 weeks",
                    prerequisites=["milestone_4", "milestone_5"],
                    skills_developed=["Project lifecycle", "Data pipeline", "Model deployment", "Results presentation"],
                    difficulty=SkillLevel.INTERMEDIATE,
                    priority=2
                )
            ]
        else:  # general_tech
            return [
                Milestone(
                    id="milestone_3",
                    title="Digital Skills Development",
                    description="Develop practical digital skills and tools proficiency",
                    type=MilestoneType.PROJECT,
                    phase="Development",
                    estimated_duration="3-4 weeks",
                    prerequisites=["milestone_1", "milestone_2"],
                    skills_developed=["Digital tools", "Online collaboration", "Content creation", "Project management"],
                    difficulty=SkillLevel.INTERMEDIATE,
                    priority=1
                ),
                Milestone(
                    id="milestone_4",
                    title="First Digital Project",
                    description="Create a complete digital project showcasing learned skills",
                    type=MilestoneType.PROJECT,
                    phase="Development",
                    estimated_duration="2-3 weeks",
                    prerequisites=["milestone_3"],
                    skills_developed=["Project execution", "Quality assurance", "Documentation", "Presentation"],
                    difficulty=SkillLevel.INTERMEDIATE,
                    priority=2
                )
            ]
    
    def _create_advanced_milestones(self, career_focus: str) -> List[Milestone]:
        """Create advanced phase milestones based on career focus"""
        if career_focus == "software_development":
            return [
                Milestone(
                    id="milestone_7",
                    title="Advanced Programming Concepts",
                    description="Master design patterns, software architecture, and advanced programming techniques",
                    type=MilestoneType.LEARNING,
                    phase="Advanced",
                    estimated_duration="4-5 weeks",
                    prerequisites=["milestone_6"],
                    skills_developed=["Design patterns", "Software architecture", "Performance optimization", "Code quality"],
                    difficulty=SkillLevel.ADVANCED,
                    priority=1
                ),
                Milestone(
                    id="milestone_8",
                    title="Cloud & DevOps",
                    description="Learn cloud platforms, containerization, and DevOps practices",
                    type=MilestoneType.LEARNING,
                    phase="Advanced",
                    estimated_duration="3-4 weeks",
                    prerequisites=["milestone_6"],
                    skills_developed=["Cloud platforms", "Docker", "CI/CD", "Infrastructure as code"],
                    difficulty=SkillLevel.ADVANCED,
                    priority=1
                ),
                Milestone(
                    id="milestone_9",
                    title="Advanced Project Portfolio",
                    description="Build complex, production-ready applications for portfolio",
                    type=MilestoneType.PROJECT,
                    phase="Advanced",
                    estimated_duration="6-8 weeks",
                    prerequisites=["milestone_7", "milestone_8"],
                    skills_developed=["Complex systems", "Performance optimization", "Security", "Scalability"],
                    difficulty=SkillLevel.ADVANCED,
                    priority=2
                )
            ]
        elif career_focus == "data_science":
            return [
                Milestone(
                    id="milestone_7",
                    title="Deep Learning & AI",
                    description="Master deep learning frameworks and advanced AI techniques",
                    type=MilestoneType.LEARNING,
                    phase="Advanced",
                    estimated_duration="5-6 weeks",
                    prerequisites=["milestone_6"],
                    skills_developed=["Deep learning", "Neural networks", "TensorFlow/PyTorch", "AI ethics"],
                    difficulty=SkillLevel.ADVANCED,
                    priority=1
                ),
                Milestone(
                    id="milestone_8",
                    title="Big Data & Cloud Platforms",
                    description="Learn big data processing and cloud-based ML platforms",
                    type=MilestoneType.LEARNING,
                    phase="Advanced",
                    estimated_duration="4-5 weeks",
                    prerequisites=["milestone_6"],
                    skills_developed=["Big data tools", "Cloud ML", "Distributed computing", "Data pipelines"],
                    difficulty=SkillLevel.ADVANCED,
                    priority=1
                ),
                Milestone(
                    id="milestone_9",
                    title="Advanced Data Science Portfolio",
                    description="Create sophisticated data science projects and case studies",
                    type=MilestoneType.PROJECT,
                    phase="Advanced",
                    estimated_duration="6-8 weeks",
                    prerequisites=["milestone_7", "milestone_8"],
                    skills_developed=["Complex modeling", "Business impact", "Stakeholder communication", "Research skills"],
                    difficulty=SkillLevel.ADVANCED,
                    priority=2
                )
            ]
        else:  # general_tech
            return [
                Milestone(
                    id="milestone_5",
                    title="Specialized Skills Development",
                    description="Develop expertise in chosen technology specialization",
                    type=MilestoneType.LEARNING,
                    phase="Advanced",
                    estimated_duration="4-5 weeks",
                    prerequisites=["milestone_4"],
                    skills_developed=["Specialized tools", "Advanced techniques", "Industry knowledge", "Best practices"],
                    difficulty=SkillLevel.ADVANCED,
                    priority=1
                ),
                Milestone(
                    id="milestone_6",
                    title="Advanced Project Portfolio",
                    description="Build comprehensive portfolio of advanced projects",
                    type=MilestoneType.PROJECT,
                    phase="Advanced",
                    estimated_duration="4-6 weeks",
                    prerequisites=["milestone_5"],
                    skills_developed=["Complex projects", "Quality standards", "Innovation", "Leadership"],
                    difficulty=SkillLevel.ADVANCED,
                    priority=2
                )
            ]
    
    def _create_specialization_milestones(self, career_focus: str) -> List[Milestone]:
        """Create specialization phase milestones based on career focus"""
        if career_focus == "software_development":
            return [
                Milestone(
                    id="milestone_10",
                    title="System Design & Architecture",
                    description="Master large-scale system design and architectural patterns",
                    type=MilestoneType.LEARNING,
                    phase="Specialization",
                    estimated_duration="4-5 weeks",
                    prerequisites=["milestone_9"],
                    skills_developed=["System design", "Microservices", "Scalability", "Performance"],
                    difficulty=SkillLevel.EXPERT,
                    priority=1
                ),
                Milestone(
                    id="milestone_11",
                    title="Open Source Contribution",
                    description="Contribute to open source projects and build professional network",
                    type=MilestoneType.NETWORKING,
                    phase="Specialization",
                    estimated_duration="3-4 weeks",
                    prerequisites=["milestone_9"],
                    skills_developed=["Open source", "Community engagement", "Code review", "Mentoring"],
                    difficulty=SkillLevel.ADVANCED,
                    priority=2
                ),
                Milestone(
                    id="milestone_12",
                    title="Industry-Ready Portfolio",
                    description="Create production-quality portfolio and prepare for job applications",
                    type=MilestoneType.APPLICATION,
                    phase="Specialization",
                    estimated_duration="3-4 weeks",
                    prerequisites=["milestone_10", "milestone_11"],
                    skills_developed=["Portfolio development", "Resume building", "Interview prep", "Networking"],
                    difficulty=SkillLevel.ADVANCED,
                    priority=1
                )
            ]
        elif career_focus == "data_science":
            return [
                Milestone(
                    id="milestone_10",
                    title="MLOps & Production Systems",
                    description="Learn machine learning operations and production deployment",
                    type=MilestoneType.LEARNING,
                    phase="Specialization",
                    estimated_duration="4-5 weeks",
                    prerequisites=["milestone_9"],
                    skills_developed=["MLOps", "Model deployment", "Monitoring", "A/B testing"],
                    difficulty=SkillLevel.EXPERT,
                    priority=1
                ),
                Milestone(
                    id="milestone_11",
                    title="Research & Publications",
                    description="Engage in research, write technical articles, and build thought leadership",
                    type=MilestoneType.NETWORKING,
                    phase="Specialization",
                    estimated_duration="4-5 weeks",
                    prerequisites=["milestone_9"],
                    skills_developed=["Research skills", "Technical writing", "Conference speaking", "Thought leadership"],
                    difficulty=SkillLevel.ADVANCED,
                    priority=2
                ),
                Milestone(
                    id="milestone_12",
                    title="Data Science Portfolio & Career Prep",
                    description="Create comprehensive portfolio and prepare for data science roles",
                    type=MilestoneType.APPLICATION,
                    phase="Specialization",
                    estimated_duration="3-4 weeks",
                    prerequisites=["milestone_10", "milestone_11"],
                    skills_developed=["Portfolio development", "Case study creation", "Interview prep", "Industry networking"],
                    difficulty=SkillLevel.ADVANCED,
                    priority=1
                )
            ]
        else:  # general_tech
            return [
                Milestone(
                    id="milestone_7",
                    title="Leadership & Mentoring",
                    description="Develop leadership skills and ability to mentor others",
                    type=MilestoneType.LEARNING,
                    phase="Specialization",
                    estimated_duration="3-4 weeks",
                    prerequisites=["milestone_6"],
                    skills_developed=["Leadership", "Mentoring", "Team management", "Communication"],
                    difficulty=SkillLevel.ADVANCED,
                    priority=1
                ),
                Milestone(
                    id="milestone_8",
                    title="Professional Network & Brand",
                    description="Build professional network and personal brand in chosen field",
                    type=MilestoneType.NETWORKING,
                    phase="Specialization",
                    estimated_duration="3-4 weeks",
                    prerequisites=["milestone_6"],
                    skills_developed=["Networking", "Personal branding", "Industry engagement", "Community building"],
                    difficulty=SkillLevel.ADVANCED,
                    priority=2
                ),
                Milestone(
                    id="milestone_9",
                    title="Career Transition & Job Search",
                    description="Prepare for career transition and job search in chosen field",
                    type=MilestoneType.APPLICATION,
                    phase="Specialization",
                    estimated_duration="3-4 weeks",
                    prerequisites=["milestone_7", "milestone_8"],
                    skills_developed=["Job search", "Interview skills", "Resume building", "Career planning"],
                    difficulty=SkillLevel.ADVANCED,
                    priority=1
                )
            ]
