"""
Progress Router — Track milestone completion and roadmap progress
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from app.database import get_db
from app.database.db_models import DBProgress, DBRoadmap

router = APIRouter()


# ─── Request/Response Models ────────────────────────────────────────────────────

class ProgressUpdate(BaseModel):
    roadmap_id: str
    milestone_id: str
    status: str = "in_progress"  # not_started, in_progress, completed
    progress_percentage: float = 0.0
    notes: Optional[str] = ""


class ProgressResponse(BaseModel):
    id: int
    user_id: str
    roadmap_id: str
    milestone_id: str
    status: str
    progress_percentage: float
    notes: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    updated_at: Optional[str] = None


class RoadmapProgressSummary(BaseModel):
    roadmap_id: str
    total_milestones: int
    completed: int
    in_progress: int
    not_started: int
    overall_percentage: float


# ─── Endpoints ──────────────────────────────────────────────────────────────────


@router.post("/progress/{user_id}", response_model=ProgressResponse)
def update_progress(user_id: str, update: ProgressUpdate, db: Session = Depends(get_db)):
    """Update or create milestone progress for a user."""
    # Find existing progress record
    progress = db.query(DBProgress).filter(
        DBProgress.user_id == user_id,
        DBProgress.roadmap_id == update.roadmap_id,
        DBProgress.milestone_id == update.milestone_id,
    ).first()

    now = datetime.utcnow()

    if progress:
        progress.status = update.status
        progress.progress_percentage = update.progress_percentage
        progress.notes = update.notes or ""
        if update.status == "in_progress" and not progress.started_at:
            progress.started_at = now
        if update.status == "completed":
            progress.completed_at = now
            progress.progress_percentage = 100.0
    else:
        progress = DBProgress(
            user_id=user_id,
            roadmap_id=update.roadmap_id,
            milestone_id=update.milestone_id,
            status=update.status,
            progress_percentage=update.progress_percentage,
            notes=update.notes or "",
            started_at=now if update.status != "not_started" else None,
            completed_at=now if update.status == "completed" else None,
        )
        db.add(progress)

    db.commit()
    db.refresh(progress)

    return _to_response(progress)


@router.get("/progress/{user_id}/{roadmap_id}", response_model=List[ProgressResponse])
def get_milestone_progress(user_id: str, roadmap_id: str, db: Session = Depends(get_db)):
    """Get all milestone progress for a user's roadmap."""
    records = db.query(DBProgress).filter(
        DBProgress.user_id == user_id,
        DBProgress.roadmap_id == roadmap_id,
    ).all()
    return [_to_response(r) for r in records]


@router.get("/progress/{user_id}/{roadmap_id}/summary", response_model=RoadmapProgressSummary)
def get_roadmap_progress_summary(user_id: str, roadmap_id: str, db: Session = Depends(get_db)):
    """Get overall progress summary for a roadmap."""
    records = db.query(DBProgress).filter(
        DBProgress.user_id == user_id,
        DBProgress.roadmap_id == roadmap_id,
    ).all()

    # Also try to get total milestones from stored roadmap
    roadmap = db.query(DBRoadmap).filter(DBRoadmap.roadmap_id == roadmap_id).first()
    total_from_roadmap = 0
    if roadmap and roadmap.phases:
        for phase in roadmap.phases:
            total_from_roadmap += len(phase.get("milestones", []))

    completed = sum(1 for r in records if r.status == "completed")
    in_progress = sum(1 for r in records if r.status == "in_progress")
    not_started_tracked = sum(1 for r in records if r.status == "not_started")

    total = max(total_from_roadmap, len(records))
    not_started = total - completed - in_progress

    overall = (completed / total * 100) if total > 0 else 0

    return RoadmapProgressSummary(
        roadmap_id=roadmap_id,
        total_milestones=total,
        completed=completed,
        in_progress=in_progress,
        not_started=not_started,
        overall_percentage=round(overall, 1),
    )


@router.delete("/progress/{user_id}/{roadmap_id}/{milestone_id}")
def reset_milestone_progress(user_id: str, roadmap_id: str, milestone_id: str, db: Session = Depends(get_db)):
    """Reset progress for a specific milestone."""
    progress = db.query(DBProgress).filter(
        DBProgress.user_id == user_id,
        DBProgress.roadmap_id == roadmap_id,
        DBProgress.milestone_id == milestone_id,
    ).first()

    if not progress:
        raise HTTPException(status_code=404, detail="Progress record not found")

    db.delete(progress)
    db.commit()
    return {"message": "Progress reset", "milestone_id": milestone_id}


# ─── Helpers ────────────────────────────────────────────────────────────────────

def _to_response(p: DBProgress) -> ProgressResponse:
    return ProgressResponse(
        id=p.id,
        user_id=p.user_id,
        roadmap_id=p.roadmap_id,
        milestone_id=p.milestone_id,
        status=p.status,
        progress_percentage=p.progress_percentage,
        notes=p.notes or "",
        started_at=p.started_at.isoformat() if p.started_at else None,
        completed_at=p.completed_at.isoformat() if p.completed_at else None,
        updated_at=p.updated_at.isoformat() if p.updated_at else None,
    )
