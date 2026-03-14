"""
SQLAlchemy ORM models for the AI Career Advisor Platform
"""

from sqlalchemy import Column, String, Integer, Float, Text, Boolean, DateTime, JSON
from sqlalchemy.sql import func

from app.database import Base


class DBUser(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(64), unique=True, nullable=False, index=True)
    name = Column(String(128), nullable=False)
    education = Column(String(256), default="")
    skills = Column(JSON, default=list)
    interests = Column(JSON, default=list)
    career_goals = Column(JSON, default=list)
    goals = Column(JSON, default=list)
    current_role = Column(String(128), nullable=True)
    experience_years = Column(Integer, default=0)
    career_phase = Column(String(64), default="student")
    skill_levels = Column(JSON, default=dict)
    time_commitment = Column(String(64), default="part-time")
    learning_style = Column(String(64), default="mixed")
    location = Column(String(128), nullable=True)
    budget = Column(Float, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class DBQuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    attempt_id = Column(String(64), unique=True, nullable=False, index=True)
    user_id = Column(String(64), nullable=False, index=True)
    answers = Column(JSON, default=list)
    scores = Column(JSON, default=dict)
    top_stream = Column(String(64), default="")
    recommendations = Column(JSON, default=list)
    suggested_subjects = Column(JSON, default=list)
    rationale = Column(Text, default="")
    created_at = Column(DateTime, server_default=func.now())


class DBRoadmap(Base):
    __tablename__ = "roadmaps"

    id = Column(Integer, primary_key=True, autoincrement=True)
    roadmap_id = Column(String(64), unique=True, nullable=False, index=True)
    user_id = Column(String(64), nullable=False, index=True)
    title = Column(String(256), default="")
    description = Column(Text, default="")
    roadmap_type = Column(String(64), default="custom")
    user_data = Column(JSON, default=dict)
    phases = Column(JSON, default=list)
    total_estimated_duration = Column(String(64), default="")
    total_progress = Column(Float, default=0.0)
    tags = Column(JSON, default=list)
    is_public = Column(Boolean, default=False)
    shared_with = Column(JSON, default=list)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class DBProgress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(64), nullable=False, index=True)
    roadmap_id = Column(String(64), nullable=False, index=True)
    milestone_id = Column(String(64), nullable=False)
    status = Column(String(32), default="not_started")  # not_started, in_progress, completed
    progress_percentage = Column(Float, default=0.0)
    notes = Column(Text, default="")
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
