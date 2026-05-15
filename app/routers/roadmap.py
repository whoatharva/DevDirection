"""
Roadmap Router - Handles AI-powered and custom roadmap generation
"""

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from typing import List, Dict, Any
from datetime import datetime

from app.config import USERS_FILE, CAREERS_FILE, USER_ROADMAPS_FILE
from app.utils import load_json, save_json, generate_id
from app.models import (
    RoadmapRequest,
    RoadmapResponse,
    UserProfile,
    UserGeneratedRoadmap,
    RoadmapUpdateRequest,
    RoadmapTemplate,
    MilestoneStatus,
    CustomRoadmapRequest,
)
from pydantic import BaseModel
from app.services.roadmap_engine import RoadmapEngine
from app.services.hierarchical_roadmap import HierarchicalRoadmapEngine
from app.services.user_roadmap_engine import UserRoadmapEngine
from app.services.llm import generate_roadmap_stream, resume_roadmap_stream

router = APIRouter()

# Load data
users_data = load_json(USERS_FILE, [])
careers_data = load_json(CAREERS_FILE, [])
user_roadmaps_data = load_json(USER_ROADMAPS_FILE, [])

# Initialize engines
roadmap_engine = RoadmapEngine()
hierarchical_engine = HierarchicalRoadmapEngine()
user_roadmap_engine = UserRoadmapEngine()


# ─── AI Roadmap Generation ───────────────────────────────────────────────────

class ResumeRequest(BaseModel):
    thread_id: str

@router.post("/roadmap/generate-stream")
def generate_roadmap_stream_endpoint(request: RoadmapRequest):
    """Generate AI-powered career roadmap using SSE to stream agent updates"""
    try:
        user = next((u for u in users_data if u["user_id"] == request.user_id), None)
        if not user:
            user = {
                "user_id": request.user_id,
                "name": "Quiz User",
                "education": "Not specified",
                "skills": [],
                "interests": [],
                "career_goals": [],
                "time_commitment": "part-time",
                "learning_style": "mixed"
            }
            users_data.append(user)
            save_json(USERS_FILE, users_data)
            
        user_profile = UserProfile(**user)
        return StreamingResponse(generate_roadmap_stream(user_profile), media_type="text/event-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/roadmap/resume-stream")
def resume_roadmap_stream_endpoint(request: ResumeRequest):
    """Resume a paused human-in-the-loop roadmap generation"""
    try:
        return StreamingResponse(resume_roadmap_stream(request.thread_id), media_type="text/event-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



class ChatRequest(BaseModel):
    user_id: str
    message: str

@router.post("/roadmap/chat")
def roadmap_chat_endpoint(request: ChatRequest):
    """Contextual Chatbot answering questions about the generated roadmap"""
    try:
        from app.services.llm import answer_roadmap_question
        reply = answer_roadmap_question(request.user_id, request.message)
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/roadmap/generate")
def generate_roadmap(request: RoadmapRequest):
    """Generate AI-powered career roadmap"""
    try:
        user = next((u for u in users_data if u["user_id"] == request.user_id), None)
        if not user:
            # Auto-create minimal user profile instead of raising 404
            user = {
                "user_id": request.user_id,
                "name": "Quiz User",
                "education": "Not specified",
                "skills": [],
                "interests": [],
                "career_goals": [],
                "time_commitment": "part-time",
                "learning_style": "mixed"
            }
            users_data.append(user)
            save_json(USERS_FILE, users_data)

        user_profile = UserProfile(**user)
        roadmap_data = roadmap_engine.generate_roadmap(user_profile)
        return roadmap_data

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to generate roadmap: {str(e)}"
        )


@router.post("/roadmap/hierarchical", response_model=RoadmapResponse)
def generate_hierarchical_roadmap(request: RoadmapRequest):
    """Generate hierarchical career roadmap"""
    try:
        user = next((u for u in users_data if u["user_id"] == request.user_id), None)
        if not user:
            # Auto-create minimal user profile instead of raising 404
            user = {
                "user_id": request.user_id,
                "name": "Quiz User",
                "education": "Not specified",
                "skills": [],
                "interests": [],
                "career_goals": [],
                "time_commitment": "part-time",
                "learning_style": "mixed"
            }
            users_data.append(user)
            save_json(USERS_FILE, users_data)

        user_profile = UserProfile(**user)
        roadmap_data = hierarchical_engine.generate_hierarchical_roadmap(user_profile)
        return RoadmapResponse(**roadmap_data)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate hierarchical roadmap: {str(e)}",
        )


# ─── Custom Roadmap CRUD ─────────────────────────────────────────────────────


@router.post("/roadmap/create-custom", response_model=Dict[str, Any])
def generate_custom_roadmap(request: CustomRoadmapRequest):
    """Generate AI-powered career roadmap from custom form data"""
    try:
        roadmap_data = request.roadmap_data
        if not roadmap_data:
            raise HTTPException(status_code=400, detail="Roadmap data is required.")

        # Map custom form data to UserProfile for the engine
        user_profile = UserProfile(
            user_id=request.user_id,
            name=roadmap_data.get("title", "Custom User"),
            education=roadmap_data.get("current_level", "Unknown"),
            skills=roadmap_data.get("current_skills", []),
            interests=roadmap_data.get("interests", []),
            career_goals=(
                [roadmap_data.get("target_goal", "")]
                if roadmap_data.get("target_goal")
                else []
            ),
            time_commitment=roadmap_data.get("time_commitment", "part-time"),
            learning_style=(
                roadmap_data.get("preferred_learning_style", ["mixed"])[0]
                if roadmap_data.get("preferred_learning_style")
                else "mixed"
            ),
        )

        generated_roadmap = roadmap_engine.generate_roadmap(user_profile)

        custom_roadmap = {
            "id": generate_id("crm_"),
            "user_id": request.user_id,
            "title": roadmap_data.get(
                "title", generated_roadmap["summary"]["title"]
            ),
            "description": roadmap_data.get(
                "description", generated_roadmap["summary"]["description"]
            ),
            "roadmap_type": roadmap_data.get("roadmap_type", "custom"),
            "user_data": roadmap_data,
            "phases": generated_roadmap["phases"],
            "total_estimated_duration": generated_roadmap["summary"]["total_duration"],
            "total_progress": 0.0,
            "tags": _generate_tags_from_data(roadmap_data),
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "is_public": False,
            "shared_with": [],
        }

        # Save to storage
        user_roadmaps_data.append(custom_roadmap)
        save_json(USER_ROADMAPS_FILE, user_roadmaps_data)

        return custom_roadmap

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create custom roadmap: {str(e)}"
        )


@router.get("/roadmap/custom/{roadmap_id}", response_model=UserGeneratedRoadmap)
def get_custom_roadmap(roadmap_id: str):
    """Get a specific custom roadmap by ID"""
    roadmap = next((r for r in user_roadmaps_data if r["id"] == roadmap_id), None)
    if not roadmap:
        raise HTTPException(status_code=404, detail="Custom roadmap not found")
    return UserGeneratedRoadmap(**roadmap)


@router.get(
    "/roadmap/custom/user/{user_id}", response_model=List[UserGeneratedRoadmap]
)
def get_user_custom_roadmaps(user_id: str):
    """Get all custom roadmaps for a specific user"""
    user_roadmaps = [r for r in user_roadmaps_data if r["user_id"] == user_id]
    return [UserGeneratedRoadmap(**r) for r in user_roadmaps]


@router.put("/roadmap/custom/{roadmap_id}/milestone")
def update_custom_milestone(roadmap_id: str, request: RoadmapUpdateRequest):
    """Update a milestone in a custom roadmap"""
    roadmap = next((r for r in user_roadmaps_data if r["id"] == roadmap_id), None)
    if not roadmap:
        raise HTTPException(status_code=404, detail="Custom roadmap not found")

    milestone_updated = False
    for phase in roadmap["phases"]:
        for milestone in phase["milestones"]:
            if milestone["id"] == request.id:
                if request.title:
                    milestone["title"] = request.title
                if request.description:
                    milestone["description"] = request.description
                milestone_updated = True
                break
        if milestone_updated:
            break

    if not milestone_updated:
        raise HTTPException(status_code=404, detail="Milestone not found")

    roadmap["updated_at"] = datetime.utcnow().isoformat()
    roadmap["total_progress"] = _calculate_roadmap_progress(roadmap)
    save_json(USER_ROADMAPS_FILE, user_roadmaps_data)

    return {"message": "Milestone updated successfully", "roadmap_id": roadmap_id}


# ─── Templates ────────────────────────────────────────────────────────────────


@router.get("/roadmap/templates", response_model=List[RoadmapTemplate])
def get_roadmap_templates():
    """Get available roadmap templates"""
    templates = [
        {
            "id": "web_development",
            "name": "Full-Stack Web Development",
            "description": "Complete roadmap for becoming a full-stack web developer",
            "phases": [],
        },
        {
            "id": "data_science",
            "name": "Data Science Career Path",
            "description": "Complete roadmap for becoming a data scientist",
            "phases": [],
        },
    ]
    return [RoadmapTemplate(**t) for t in templates]


# ─── Dynamic Milestone Details ────────────────────────────────────────────────


@router.get("/milestone/{milestone_id}")
def get_milestone_details(milestone_id: str):
    """Get detailed information about a specific milestone.
    
    Searches all stored roadmaps for the milestone by ID and returns its data.
    Falls back to the roadmap engine's generated data if not found in storage.
    """
    # Search stored roadmaps first
    for roadmap in user_roadmaps_data:
        phases = roadmap.get("phases", [])
        if isinstance(phases, list):
            for phase in phases:
                milestones = phase.get("milestones", [])
                if isinstance(milestones, list):
                    for milestone in milestones:
                        if isinstance(milestone, dict) and milestone.get("id") == milestone_id:
                            return milestone

    raise HTTPException(status_code=404, detail="Milestone not found")


# ─── Helper Functions ─────────────────────────────────────────────────────────


def _generate_tags_from_data(roadmap_data: Dict[str, Any]) -> List[str]:
    """Generate tags from roadmap data"""
    tags = []
    tags.append(roadmap_data.get("roadmap_type", "custom"))
    if "target_skills" in roadmap_data:
        tags.extend(roadmap_data["target_skills"])
    if "preferred_learning_style" in roadmap_data:
        tags.extend(roadmap_data["preferred_learning_style"])
    return list(set(tags))


def _calculate_roadmap_progress(roadmap: Dict) -> float:
    """Calculate overall progress for a roadmap"""
    total_milestones = 0
    completed_milestones = 0

    for phase in roadmap.get("phases", []):
        for milestone in phase.get("milestones", []):
            total_milestones += 1
            status = milestone.get("status", "not_started")
            if status == MilestoneStatus.COMPLETED or status == "completed":
                completed_milestones += 1
            elif status == MilestoneStatus.IN_PROGRESS or status == "in_progress":
                completed_milestones += milestone.get("progress_percentage", 0) / 100

    return (
        (completed_milestones / total_milestones * 100) if total_milestones > 0 else 0
    )


async def _apply_ai_enhancement(roadmap: Dict, customization_level: str) -> Dict:
    """Apply AI enhancement to the roadmap"""
    roadmap["ai_enhanced"] = True
    roadmap["customization_level"] = customization_level
    for phase in roadmap["phases"]:
        phase["ai_notes"] = f"AI-optimized for {customization_level} level"
    return roadmap
