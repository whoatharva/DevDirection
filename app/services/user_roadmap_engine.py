"""
User Roadmap Engine - Handles custom roadmap generation and management
"""

from datetime import datetime
from typing import List, Dict, Any
from app.models import (
    UserRoadmapData, UserGeneratedRoadmap, UserPhase, UserMilestone,
    UserResource, RoadmapType, MilestoneStatus, PriorityLevel, 
    DifficultyLevel, ResourceType, RoadmapTemplate, RoadmapCreationRequest
)
from app.utils import generate_id


class UserRoadmapEngine:
    """Engine for creating and managing user-generated roadmaps"""
    
    def __init__(self):
        self.templates_db = self._load_roadmap_templates()
        self.resource_database = self._load_resource_database()
        self.skill_database = self._load_skill_database()
    
    def _load_roadmap_templates(self) -> List[RoadmapTemplate]:
        """Load roadmap templates from database"""
        return [
            RoadmapTemplate(
                id="web_development",
                name="Full-Stack Web Development",
                description="Complete roadmap for becoming a full-stack web developer",
                roadmap_type=RoadmapType.CAREER,
                category="Technology",
                difficulty="intermediate",
                estimated_duration="6-12 months",
                phases=[],
                tags=["web development", "programming", "frontend", "backend"],
                popularity=0,
                rating=4.5,
                created_by="system",
                is_official=True
            ),
            RoadmapTemplate(
                id="data_science",
                name="Data Science Career Path",
                description="Complete roadmap for becoming a data scientist",
                roadmap_type=RoadmapType.CAREER,
                category="Technology",
                difficulty="advanced",
                estimated_duration="12-18 months",
                phases=[],
                tags=["data science", "machine learning", "python", "statistics"],
                popularity=0,
                rating=4.7,
                created_by="system",
                is_official=True
            )
        ]
    
    def _load_resource_database(self) -> List[UserResource]:
        """Load resource database"""
        return [
            UserResource(
                id="res_1",
                title="Python for Data Science",
                url="https://example.com/python-course",
                type=ResourceType.COURSE,
                description="Comprehensive Python course for data science",
                cost=99.99,
                duration="8 weeks",
                difficulty=DifficultyLevel.INTERMEDIATE
            ),
            UserResource(
                id="res_2",
                title="Machine Learning Book",
                url="https://example.com/ml-book",
                type=ResourceType.BOOK,
                description="Introduction to Machine Learning",
                cost=49.99,
                duration="4 weeks",
                difficulty=DifficultyLevel.ADVANCED
            )
        ]
    
    def _load_skill_database(self) -> List[str]:
        """Load skill database"""
        return [
            "Python", "JavaScript", "React", "Node.js", "SQL", "Machine Learning",
            "Data Analysis", "Project Management", "Communication", "Leadership"
        ]
    
    async def create_user_roadmap(self, request: RoadmapCreationRequest) -> UserGeneratedRoadmap:
        """Create a custom user roadmap"""
        try:
            # Generate roadmap phases based on user data
            phases = self._generate_phases(request.roadmap_data)
            
            # Calculate total duration
            total_duration = self._calculate_total_duration(phases)
            
            # Generate tags
            tags = self._generate_tags(request.roadmap_data)
            
            # Create roadmap
            roadmap = UserGeneratedRoadmap(
                id=generate_id("roadmap_"),
                user_id=request.user_id,
                title=request.roadmap_data.title,
                description=request.roadmap_data.description,
                roadmap_type=request.roadmap_data.roadmap_type,
                user_data=request.roadmap_data,
                phases=phases,
                total_estimated_duration=total_duration,
                total_progress=0.0,
                tags=tags,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                is_public=False,
                shared_with=[]
            )
            
            return roadmap
            
        except Exception as e:
            raise Exception(f"Failed to create user roadmap: {str(e)}")
    
    def _generate_phases(self, roadmap_data: UserRoadmapData) -> List[UserPhase]:
        """Generate phases based on roadmap data"""
        phases = []
        
        # Phase 1: Foundation
        foundation_phase = UserPhase(
            id=generate_id("phase_"),
            name="Foundation",
            description="Build foundational knowledge and skills",
            order=1,
            milestones=self._generate_foundation_milestones(roadmap_data),
            estimated_duration="2-4 weeks",
            progress_percentage=0.0
        )
        phases.append(foundation_phase)
        
        # Phase 2: Intermediate
        intermediate_phase = UserPhase(
            id=generate_id("phase_"),
            name="Intermediate Development",
            description="Develop intermediate skills and practical experience",
            order=2,
            milestones=self._generate_intermediate_milestones(roadmap_data),
            estimated_duration="4-8 weeks",
            progress_percentage=0.0
        )
        phases.append(intermediate_phase)
        
        # Phase 3: Advanced
        advanced_phase = UserPhase(
            id=generate_id("phase_"),
            name="Advanced Mastery",
            description="Master advanced concepts and build projects",
            order=3,
            milestones=self._generate_advanced_milestones(roadmap_data),
            estimated_duration="6-12 weeks",
            progress_percentage=0.0
        )
        phases.append(advanced_phase)
        
        return phases
    
    def _generate_foundation_milestones(self, roadmap_data: UserRoadmapData) -> List[UserMilestone]:
        """Generate foundation milestones"""
        milestones = []
        
        # Basic concepts milestone
        milestones.append(UserMilestone(
            id=generate_id("milestone_"),
            title="Learn Basic Concepts",
            description=f"Understand fundamental concepts of {roadmap_data.roadmap_type}",
            status=MilestoneStatus.NOT_STARTED,
            priority=PriorityLevel.HIGH,
            difficulty=DifficultyLevel.BEGINNER,
            estimated_duration="1-2 weeks",
            skills_developed=["Basic understanding", "Conceptual knowledge"],
            tags=["foundation", "basics"]
        ))
        
        # Setup environment milestone
        milestones.append(UserMilestone(
            id=generate_id("milestone_"),
            title="Setup Development Environment",
            description="Set up necessary tools and development environment",
            status=MilestoneStatus.NOT_STARTED,
            priority=PriorityLevel.HIGH,
            difficulty=DifficultyLevel.BEGINNER,
            estimated_duration="1 week",
            skills_developed=["Environment setup", "Tool configuration"],
            tags=["setup", "tools"]
        ))
        
        return milestones
    
    def _generate_intermediate_milestones(self, roadmap_data: UserRoadmapData) -> List[UserMilestone]:
        """Generate intermediate milestones"""
        milestones = []
        
        # Practice milestone
        milestones.append(UserMilestone(
            id=generate_id("milestone_"),
            title="Practice Core Skills",
            description=f"Practice and apply {roadmap_data.roadmap_type} skills through exercises",
            status=MilestoneStatus.NOT_STARTED,
            priority=PriorityLevel.HIGH,
            difficulty=DifficultyLevel.INTERMEDIATE,
            estimated_duration="2-4 weeks",
            skills_developed=roadmap_data.target_skills[:3],
            tags=["practice", "skills"]
        ))
        
        # Build project milestone
        milestones.append(UserMilestone(
            id=generate_id("milestone_"),
            title="Build First Project",
            description="Create your first project to apply learned skills",
            status=MilestoneStatus.NOT_STARTED,
            priority=PriorityLevel.MEDIUM,
            difficulty=DifficultyLevel.INTERMEDIATE,
            estimated_duration="2-3 weeks",
            skills_developed=["Project development", "Problem solving"],
            tags=["project", "application"]
        ))
        
        return milestones
    
    def _generate_advanced_milestones(self, roadmap_data: UserRoadmapData) -> List[UserMilestone]:
        """Generate advanced milestones"""
        milestones = []
        
        # Advanced project milestone
        milestones.append(UserMilestone(
            id=generate_id("milestone_"),
            title="Build Advanced Project",
            description="Create a comprehensive project showcasing advanced skills",
            status=MilestoneStatus.NOT_STARTED,
            priority=PriorityLevel.HIGH,
            difficulty=DifficultyLevel.ADVANCED,
            estimated_duration="4-6 weeks",
            skills_developed=roadmap_data.target_skills,
            tags=["advanced", "project", "portfolio"]
        ))
        
        # Portfolio milestone
        milestones.append(UserMilestone(
            id=generate_id("milestone_"),
            title="Create Portfolio",
            description="Build a portfolio showcasing your work and skills",
            status=MilestoneStatus.NOT_STARTED,
            priority=PriorityLevel.MEDIUM,
            difficulty=DifficultyLevel.INTERMEDIATE,
            estimated_duration="1-2 weeks",
            skills_developed=["Portfolio development", "Presentation"],
            tags=["portfolio", "presentation"]
        ))
        
        return milestones
    
    def _calculate_total_duration(self, phases: List[UserPhase]) -> str:
        """Calculate total estimated duration"""
        # Simple calculation - can be enhanced
        total_weeks = 0
        for phase in phases:
            duration_str = phase.estimated_duration
            if "weeks" in duration_str:
                # Extract number of weeks
                import re
                numbers = re.findall(r'\d+', duration_str)
                if numbers:
                    total_weeks += int(numbers[0])
        
        if total_weeks <= 4:
            return f"{total_weeks} weeks"
        elif total_weeks <= 12:
            months = total_weeks // 4
            return f"{months} months"
        else:
            years = total_weeks // 52
            return f"{years} year{'s' if years > 1 else ''}"
    
    def _generate_tags(self, roadmap_data: UserRoadmapData) -> List[str]:
        """Generate tags for the roadmap"""
        tags = [roadmap_data.roadmap_type.value]
        tags.extend(roadmap_data.target_skills[:3])
        tags.extend(roadmap_data.preferred_learning_style[:2])
        return list(set(tags))[:5]  # Return unique tags, max 5