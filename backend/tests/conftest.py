"""
Pytest configuration and fixtures for the AI Career Advisor Platform tests.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db


# ─── Test database ──────────────────────────────────────────────────────────────

TEST_DATABASE_URL = "sqlite:///./test_career_advisor.db"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSession = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    db = TestSession()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Create test tables once for the entire test session."""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()  # Release file lock on Windows
    import os
    try:
        if os.path.exists("./test_career_advisor.db"):
            os.remove("./test_career_advisor.db")
    except PermissionError:
        pass  # Windows file lock, harmless


@pytest.fixture()
def client():
    """Provide a test client with overridden DB dependency."""
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
def db_session():
    """Provide a clean database session for direct DB tests."""
    session = TestSession()
    try:
        yield session
    finally:
        session.rollback()
        session.close()
