"""
Database migrations — auto-create tables and seed initial data from JSON files.
"""

import json
from pathlib import Path

from app.database import engine, Base, SessionLocal
from app.database.db_models import DBUser, DBQuizAttempt, DBRoadmap
from app.config import USERS_FILE, ATTEMPTS_FILE, USER_ROADMAPS_FILE


def create_tables():
    """Create all tables if they don't exist."""
    Base.metadata.create_all(bind=engine)
    print("[OK] Database tables created")


def seed_from_json():
    """Import existing JSON data into the database (idempotent — skips duplicates)."""
    db = SessionLocal()
    try:
        _seed_users(db)
        _seed_attempts(db)
        _seed_roadmaps(db)
        db.commit()
        print("[OK] JSON data seeded into database")
    except Exception as e:
        db.rollback()
        print(f"[WARN] Seed error (non-fatal): {e}")
    finally:
        db.close()


def _load_json(path: Path):
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def _seed_users(db):
    users = _load_json(USERS_FILE)
    for u in users:
        exists = db.query(DBUser).filter(DBUser.user_id == u.get("user_id")).first()
        if not exists:
            db.add(DBUser(
                user_id=u.get("user_id", ""),
                name=u.get("name", ""),
                education=u.get("education", ""),
                skills=u.get("skills", []),
                interests=u.get("interests", []),
                career_goals=u.get("career_goals", []),
                goals=u.get("goals", []),
                current_role=u.get("current_role"),
                experience_years=u.get("experience_years", 0),
                career_phase=u.get("career_phase", "student"),
                skill_levels=u.get("skill_levels", {}),
                time_commitment=u.get("time_commitment", "part-time"),
                learning_style=u.get("learning_style", "mixed"),
            ))
    db.flush()


def _seed_attempts(db):
    attempts = _load_json(ATTEMPTS_FILE)
    for a in attempts:
        aid = a.get("attempt_id", a.get("id", ""))
        if not aid:
            continue
        exists = db.query(DBQuizAttempt).filter(DBQuizAttempt.attempt_id == aid).first()
        if not exists:
            db.add(DBQuizAttempt(
                attempt_id=aid,
                user_id=a.get("user_id", ""),
                answers=a.get("answers", []),
                scores=a.get("scores", {}),
                top_stream=a.get("top_stream", ""),
                recommendations=a.get("recommendations", []),
                suggested_subjects=a.get("suggested_subjects", []),
                rationale=a.get("rationale", ""),
            ))
    db.flush()


def _seed_roadmaps(db):
    roadmaps = _load_json(USER_ROADMAPS_FILE)
    for r in roadmaps:
        rid = r.get("id", "")
        if not rid:
            continue
        exists = db.query(DBRoadmap).filter(DBRoadmap.roadmap_id == rid).first()
        if not exists:
            db.add(DBRoadmap(
                roadmap_id=rid,
                user_id=r.get("user_id", ""),
                title=r.get("title", ""),
                description=r.get("description", ""),
                roadmap_type=r.get("roadmap_type", "custom"),
                user_data=r.get("user_data", {}),
                phases=r.get("phases", []),
                total_estimated_duration=r.get("total_estimated_duration", ""),
                total_progress=r.get("total_progress", 0.0),
                tags=r.get("tags", []),
                is_public=r.get("is_public", False),
                shared_with=r.get("shared_with", []),
            ))
    db.flush()


def init_database():
    """Full initialization: create tables + seed data."""
    create_tables()
    seed_from_json()
