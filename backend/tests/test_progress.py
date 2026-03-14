"""
Tests for the progress tracking endpoints.
"""

import pytest


class TestProgressAPI:
    """Test progress tracking CRUD endpoints."""

    def test_create_progress(self, client):
        """Test creating a new progress record."""
        response = client.post("/api/v1/progress/u1", json={
            "roadmap_id": "test_roadmap_1",
            "milestone_id": "milestone_1",
            "status": "in_progress",
            "progress_percentage": 25.0,
            "notes": "Started learning Python basics",
        })
        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == "u1"
        assert data["roadmap_id"] == "test_roadmap_1"
        assert data["milestone_id"] == "milestone_1"
        assert data["status"] == "in_progress"
        assert data["progress_percentage"] == 25.0
        assert data["started_at"] is not None

    def test_update_progress(self, client):
        """Test updating an existing progress record."""
        # Create first
        client.post("/api/v1/progress/u1", json={
            "roadmap_id": "test_roadmap_2",
            "milestone_id": "milestone_2",
            "status": "in_progress",
            "progress_percentage": 50.0,
        })

        # Update to completed
        response = client.post("/api/v1/progress/u1", json={
            "roadmap_id": "test_roadmap_2",
            "milestone_id": "milestone_2",
            "status": "completed",
            "progress_percentage": 100.0,
            "notes": "Done!",
        })
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "completed"
        assert data["progress_percentage"] == 100.0
        assert data["completed_at"] is not None

    def test_get_milestone_progress(self, client):
        """Test getting all progress for a roadmap."""
        # Create some progress records
        for i in range(3):
            client.post("/api/v1/progress/u1", json={
                "roadmap_id": "test_roadmap_3",
                "milestone_id": f"ms_{i}",
                "status": "in_progress" if i < 2 else "completed",
                "progress_percentage": 50.0 if i < 2 else 100.0,
            })

        response = client.get("/api/v1/progress/u1/test_roadmap_3")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 3

    def test_get_progress_summary(self, client):
        """Test getting progress summary for a roadmap."""
        # Create mixed progress
        for i, status in enumerate(["completed", "in_progress", "not_started"]):
            client.post("/api/v1/progress/u2", json={
                "roadmap_id": "test_roadmap_4",
                "milestone_id": f"sum_ms_{i}",
                "status": status,
                "progress_percentage": 100.0 if status == "completed" else 0.0,
            })

        response = client.get("/api/v1/progress/u2/test_roadmap_4/summary")
        assert response.status_code == 200
        data = response.json()
        assert data["roadmap_id"] == "test_roadmap_4"
        assert data["total_milestones"] >= 3
        assert data["completed"] >= 1
        assert "overall_percentage" in data

    def test_reset_milestone_progress(self, client):
        """Test resetting a milestone's progress."""
        # Create a record first
        client.post("/api/v1/progress/u3", json={
            "roadmap_id": "test_roadmap_5",
            "milestone_id": "del_ms_1",
            "status": "completed",
            "progress_percentage": 100.0,
        })

        # Reset it
        response = client.delete("/api/v1/progress/u3/test_roadmap_5/del_ms_1")
        assert response.status_code == 200
        assert "reset" in response.json()["message"].lower()

    def test_reset_nonexistent_progress(self, client):
        """Test resetting a non-existent progress record."""
        response = client.delete("/api/v1/progress/no_user/no_roadmap/no_milestone")
        assert response.status_code == 404

    def test_empty_progress_list(self, client):
        """Test getting progress for a roadmap with no records."""
        response = client.get("/api/v1/progress/nobody/no_roadmap")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0
