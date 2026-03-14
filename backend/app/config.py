"""
Configuration settings for the Career Guidance Platform
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Data directory
DATA_DIR = BASE_DIR / "data"

# File paths
USERS_FILE = DATA_DIR / "users.json"
CAREERS_FILE = DATA_DIR / "careers.json"
QUESTIONS_FILE = DATA_DIR / "questions.json"
ATTEMPTS_FILE = DATA_DIR / "attempts.json"
USER_ROADMAPS_FILE = DATA_DIR / "user_roadmaps.json"

# Database
DATABASE_URL = f"sqlite:///{DATA_DIR / 'career_advisor.db'}"

# API Configuration
API_TITLE = "Career Guidance Platform"
API_VERSION = "1.0.0"
API_DESCRIPTION = "AI-powered career guidance and roadmap generation platform"

# CORS Configuration
CORS_ORIGINS = ["*"]
CORS_CREDENTIALS = True
CORS_METHODS = ["*"]
CORS_HEADERS = ["*"]
