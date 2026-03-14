"""
Users Router - Handles user management functionality
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

from app.config import USERS_FILE
from app.utils import load_json, save_json, generate_id, validate_required_fields
from app.models import UserProfile, UpsertUserResponse

router = APIRouter()

# Load users data
users_data = load_json(USERS_FILE, [])


@router.get("/users", response_model=List[UserProfile])
def get_users():
    """Get all users"""
    return [UserProfile(**user) for user in users_data]


@router.get("/users/{user_id}", response_model=UserProfile)
def get_user(user_id: str):
    """Get a specific user by ID"""
    user = next((u for u in users_data if u["user_id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserProfile(**user)


@router.post("/users", response_model=UpsertUserResponse)
def create_user(user: UserProfile):
    """Create a new user"""
    # Check if user already exists
    existing_user = next((u for u in users_data if u["user_id"] == user.user_id), None)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    try:
        # Add user
        user_data = user.model_dump()
        users_data.append(user_data)
        save_json(USERS_FILE, users_data)
        
        return UpsertUserResponse(
            user_id=user.user_id,
            message="User created successfully",
            success=True
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create user: {str(e)}")


@router.post("/users/profile", response_model=Dict[str, Any])
def create_user_profile(user_data: Dict[str, Any]):
    """Create a user profile from frontend data"""
    try:
        # Convert frontend data to UserProfile format
        user_profile = UserProfile(
            user_id=user_data.get("user_id", generate_id("user_")),
            name=user_data.get("name", ""),
            education=user_data.get("highest_qualification", ""),
            skills=[],
            interests=[],
            career_goals=[],
            location=user_data.get("location"),
            experience_level="beginner",
            preferred_learning_style=[],
            time_commitment="5 hours per week",
            budget=None
        )
        
        # Check if user already exists
        existing_user = next((u for u in users_data if u["user_id"] == user_profile.user_id), None)
        if existing_user:
            # Update existing user
            user_index = next((i for i, u in enumerate(users_data) if u["user_id"] == user_profile.user_id), None)
            users_data[user_index] = user_profile.model_dump()
            message = "Profile updated successfully"
        else:
            # Add new user
            users_data.append(user_profile.model_dump())
            message = "Profile created successfully"
        
        save_json(USERS_FILE, users_data)
        
        return {
            "user": user_profile.model_dump(),
            "message": message,
            "success": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create/update profile: {str(e)}")


@router.put("/users/{user_id}", response_model=UpsertUserResponse)
def update_user(user_id: str, user: UserProfile):
    """Update an existing user"""
    try:
        # Find user
        user_index = next((i for i, u in enumerate(users_data) if u["user_id"] == user_id), None)
        if user_index is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Update user
        user_data = user.model_dump()
        users_data[user_index] = user_data
        save_json(USERS_FILE, users_data)
        
        return UpsertUserResponse(
            user_id=user_id,
            message="User updated successfully",
            success=True
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update user: {str(e)}")


@router.delete("/users/{user_id}")
def delete_user(user_id: str):
    """Delete a user"""
    try:
        # Find user
        user_index = next((i for i, u in enumerate(users_data) if u["user_id"] == user_id), None)
        if user_index is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Remove user
        users_data.pop(user_index)
        save_json(USERS_FILE, users_data)
        
        return {"message": "User deleted successfully", "success": True}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete user: {str(e)}")