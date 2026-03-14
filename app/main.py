"""
Career Guidance Platform - Main Application
A comprehensive platform for career assessment, AI-powered roadmaps, and custom roadmap creation.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

from app.config import API_TITLE, API_VERSION, API_DESCRIPTION, CORS_ORIGINS, CORS_CREDENTIALS, CORS_METHODS, CORS_HEADERS
from app.routers import quiz, roadmap, users, progress

# Load environment variables
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup."""
    from app.database.migrations import init_database
    init_database()
    yield


# Create FastAPI application
app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description=API_DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=CORS_CREDENTIALS,
    allow_methods=CORS_METHODS,
    allow_headers=CORS_HEADERS,
)

# Include routers
app.include_router(quiz.router, prefix="/api/v1", tags=["quiz"])
app.include_router(roadmap.router, prefix="/api/v1", tags=["roadmap"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(progress.router, prefix="/api/v1", tags=["progress"])

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Root endpoint
@app.get("/")
def root():
    """Root endpoint with API information"""
    return {
        "message": "AI Career Advisor Platform API",
        "version": API_VERSION,
        "docs": "/docs",
        "ui": "/static/index.html"
    }

# UI redirect endpoint
@app.get("/ui")
def ui_redirect():
    """Redirect to the main UI"""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/static/index.html")

# Health check endpoint
@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": API_VERSION}