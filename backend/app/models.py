from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime


class SkillLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class CareerPhase(str, Enum):
    STUDENT = "student"
    ENTRY_LEVEL = "entry_level"
    MID_LEVEL = "mid_level"
    SENIOR_LEVEL = "senior_level"
    LEADERSHIP = "leadership"


class MilestoneType(str, Enum):
    LEARNING = "learning"
    PROJECT = "project"
    CERTIFICATION = "certification"
    EXPERIENCE = "experience"
    NETWORKING = "networking"
    APPLICATION = "application"


class MilestoneStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class UserProfile(BaseModel):
    user_id: str
    name: str
    education: str
    skills: List[str]
    interests: List[str]
    current_role: Optional[str] = None
    experience_years: Optional[int] = 0
    career_phase: Optional[CareerPhase] = CareerPhase.STUDENT
    skill_levels: Optional[Dict[str, SkillLevel]] = Field(default_factory=dict)
    goals: Optional[List[str]] = Field(default_factory=list)
    career_goals: Optional[List[str]] = Field(default_factory=list)  # Alias for goals
    time_commitment: Optional[str] = "part-time"  # part-time, full-time
    learning_style: Optional[str] = "mixed"  # visual, hands-on, theoretical, mixed


class SubTask(BaseModel):
    task_title: str
    description: str
    estimated_time: str  # e.g., "2 hours", "1 day", "1 week"
    resource_type: str  # course, video, documentation, project, practice
    resource_title: str
    resource_url: str


class Milestone(BaseModel):
    id: str
    title: str
    description: str
    type: MilestoneType
    phase: str
    estimated_duration: str  # e.g., "2-4 weeks", "1-3 months"
    prerequisites: List[str] = Field(default_factory=list)
    skills_developed: List[str] = Field(default_factory=list)
    resources: List[Dict[str, str]] = Field(
        default_factory=list
    )  # [{"title": "...", "url": "..."}]
    sub_tasks: List[SubTask] = Field(default_factory=list)
    difficulty: SkillLevel = SkillLevel.BEGINNER
    priority: int = 1  # 1-5, higher is more important
    dependencies: List[str] = Field(
        default_factory=list
    )  # milestone IDs this depends on


class RoadmapPhase(BaseModel):
    name: str
    description: str
    duration: str
    milestones: List[Milestone]
    objectives: List[str]


class SkillGap(BaseModel):
    skill: str
    current_level: SkillLevel
    target_level: SkillLevel
    gap_size: str  # small, medium, large
    learning_path: List[str]


class RoadmapResponse(BaseModel):
    user: str
    phases: List[RoadmapPhase]
    skill_gaps: List[SkillGap]
    mermaid: str
    summary: Dict[str, Any]
    generated_at: datetime = Field(default_factory=datetime.now)
    debug: Optional[Dict[str, Any]] = None


class RoadmapRequest(BaseModel):
    user_id: Optional[str] = None
    query: Optional[str] = None
    profile: Optional[UserProfile] = None
    include_skill_assessment: bool = True
    roadmap_style: str = "comprehensive"  # quick, comprehensive, detailed


# --- Additional Enums ---
class RoadmapType(str, Enum):
    PERSONAL = "personal"
    CAREER = "career"
    SKILL = "skill"
    PROJECT = "project"


class PriorityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class DifficultyLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class ResourceType(str, Enum):
    ARTICLE = "article"
    VIDEO = "video"
    COURSE = "course"
    BOOK = "book"
    PRACTICE = "practice"
    TOOL = "tool"


# --- User Roadmap Models ---
class UserResource(BaseModel):
    id: str
    title: str
    description: str
    url: str
    type: ResourceType
    difficulty: DifficultyLevel = DifficultyLevel.BEGINNER
    cost: Optional[float] = None
    duration: Optional[str] = None


class UserMilestone(BaseModel):
    id: str
    title: str
    description: str
    status: MilestoneStatus = MilestoneStatus.NOT_STARTED
    priority: PriorityLevel = PriorityLevel.MEDIUM
    difficulty: DifficultyLevel = DifficultyLevel.BEGINNER
    estimated_duration: str
    resources: List[UserResource] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)


class UserPhase(BaseModel):
    id: str
    title: str
    description: str
    milestones: List[UserMilestone]
    status: MilestoneStatus = MilestoneStatus.NOT_STARTED


# --- Quiz Models ---
class Question(BaseModel):
    qid: str
    text: str
    options: List[str]
    category: str


class SubmitPayload(BaseModel):
    user_id: str
    answers: List[Dict[str, Any]]  # Each answer: {"qid": ..., "score": ...}


class Attempt(BaseModel):
    attempt_id: str
    user_id: str
    answers: List[Dict[str, Any]]
    scores: Dict[str, float]
    recommendations: List[str]
    submitted_at: str


# --- Roadmap/Custom Roadmap Models ---


class CustomRoadmapGenerateRequest(BaseModel):
    """Request model for generating custom roadmaps"""

    user_id: str
    custom_parameters: Dict[str, Any] = Field(
        default_factory=dict, description="Custom parameters for roadmap generation"
    )


class CustomRoadmapRequest(BaseModel):
    user_id: str
    roadmap_data: Dict[str, Any]
    ai_enhancement: bool = True
    customization_level: str = "medium"


class CustomRoadmapResponse(BaseModel):
    id: str
    user_id: str
    title: str
    description: str
    roadmap_type: str
    user_data: Dict[str, Any]
    phases: List[Any]
    total_estimated_duration: str
    total_progress: float
    tags: List[str]
    created_at: str
    updated_at: str
    is_public: bool = False
    shared_with: List[str] = Field(default_factory=list)


class RoadmapTemplate(BaseModel):
    id: str
    name: str
    description: str
    phases: List[Any] = []


class UserRoadmapData(BaseModel):
    id: str
    user_id: str
    roadmap: Any
    status: MilestoneStatus = MilestoneStatus.NOT_STARTED


class RoadmapCreationRequest(BaseModel):
    user_id: str
    title: str
    description: str
    milestones: List[Any]


class RoadmapUpdateRequest(BaseModel):
    id: str
    title: str
    description: str
    milestones: List[Any]


class UserGeneratedRoadmap(BaseModel):
    id: str
    user_id: str
    title: str
    description: str
    roadmap_type: str
    user_data: Dict[str, Any]
    phases: List[Any]
    total_estimated_duration: str
    total_progress: float
    tags: List[str]
    created_at: str
    updated_at: str
    is_public: bool
    shared_with: List[str]


class UpsertUserResponse(BaseModel):
    user_id: str
    message: str
    success: bool = True
