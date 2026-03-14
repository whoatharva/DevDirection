"""
Hierarchical Roadmap Engine - Handles hierarchical roadmap generation
"""

from datetime import datetime
from typing import Dict, Any
from app.models import UserProfile, SkillGap


class HierarchicalRoadmapEngine:
    """Engine for generating hierarchical career roadmaps"""
    
    def generate_hierarchical_roadmap(self, user: UserProfile) -> Dict[str, Any]:
        """Generate a hierarchical career roadmap for a user"""
        phases = [
            {
                "id": "phase_1",
                "name": "Foundation Level",
                "description": "Build foundational knowledge and skills",
                "duration": "2-4 weeks",
                "level": 1,
                "milestones": [
                    {
                        "id": "milestone_1",
                        "title": "Learn Basic Concepts",
                        "description": "Understand fundamental concepts",
                        "duration": "1-2 weeks",
                        "status": "not_started",
                        "level": 1
                    }
                ]
            },
            {
                "id": "phase_2",
                "name": "Intermediate Level",
                "description": "Develop intermediate skills",
                "duration": "4-8 weeks",
                "level": 2,
                "milestones": [
                    {
                        "id": "milestone_2",
                        "title": "Practice Skills",
                        "description": "Practice through exercises",
                        "duration": "2-4 weeks",
                        "status": "not_started",
                        "level": 2
                    }
                ]
            },
            {
                "id": "phase_3",
                "name": "Advanced Level",
                "description": "Master advanced concepts",
                "duration": "6-12 weeks",
                "level": 3,
                "milestones": [
                    {
                        "id": "milestone_3",
                        "title": "Build Advanced Project",
                        "description": "Create comprehensive project",
                        "duration": "4-6 weeks",
                        "status": "not_started",
                        "level": 3
                    }
                ]
            }
        ]
        
        gaps = [
            SkillGap(skill="Communication", current_level="intermediate", target_level="advanced", gap_size="small", learning_path=["Join toastmasters"]),
            SkillGap(skill="Problem Solving", current_level="beginner", target_level="intermediate", gap_size="medium", learning_path=["Algorithm practice"]),
            SkillGap(skill="Leadership", current_level="beginner", target_level="advanced", gap_size="large", learning_path=["Lead small projects"])
        ]
        
        return {
            "user": user.name,
            "phases": phases,
            "skill_gaps": [g.model_dump() for g in gaps],
            "mermaid": "",
            "summary": {
                "title": f"Hierarchical Roadmap for {user.name}",
                "description": "Progressive learning path built linearly.",
                "total_duration": "12-24 weeks",
                "phases_count": len(phases),
                "milestones_count": sum(len(p.get("milestones", [])) for p in phases)
            },
            "generated_at": datetime.utcnow().isoformat(),
            "debug": {"engine": "HierarchicalRoadmapEngine", "version": "1.0.0"}
        }
