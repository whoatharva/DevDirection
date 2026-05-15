"""
Quiz Router - Handles career assessment quiz functionality
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from datetime import datetime

from app.config import QUESTIONS_FILE, ATTEMPTS_FILE
from app.utils import load_json, save_json, generate_id
from app.models import Question, SubmitPayload, Attempt, UserProfile

router = APIRouter()

# Load quiz questions
questions_data = load_json(QUESTIONS_FILE, [])
attempts_data = load_json(ATTEMPTS_FILE, [])


@router.get("/quiz/questions", response_model=List[Question])
def get_questions():
    """Get all quiz questions"""
    return [Question(**q) for q in questions_data]


@router.post("/quiz/submit", response_model=Dict[str, Any])
def submit_quiz(payload: SubmitPayload):
    """Submit quiz answers and get results"""
    try:
        from app.services.scoring import score_answers
        
        # Convert payload.answers to Dict[str, int]
        answers_dict = {}
        for ans in payload.answers:
            qid = ans.get("qid") if isinstance(ans, dict) else ans.qid
            score = ans.get("score") if isinstance(ans, dict) else ans.score
            answers_dict[qid] = int(score)
            
        scores, top_stream, suggested_subjects, rationale = score_answers(answers_dict)
        
        # Generate career recommendations based on top stream
        recommendations = []
        if top_stream == "Science":
            recommendations.extend(["Software Engineer", "Data Scientist", "Research Scientist"])
        elif top_stream == "Commerce":
            recommendations.extend(["Business Analyst", "Financial Analyst", "Accountant"])
        elif top_stream == "Arts":
            recommendations.extend(["Content Creator", "HR Specialist", "Writer"])
        elif top_stream == "Vocational":
            recommendations.extend(["Technician", "Mechanic", "Electrician"])
        
        # Create attempt record
        attempt = Attempt(
            attempt_id=generate_id("attempt_"),
            user_id=payload.user_id,
            answers=payload.answers,
            scores=scores,
            recommendations=recommendations,
            submitted_at=datetime.utcnow().isoformat()
        )
        
        # Save attempt
        attempts_data.append(attempt.model_dump())
        save_json(ATTEMPTS_FILE, attempts_data)
        
        # Generate AI advice
        ai_advice = {
            "summary": f"Your profile suggests a strong inclination towards {top_stream} fields.",
            "next_steps": [
                {"title": "Focus Areas", "detail": f"Concentrate on {top_stream} subjects and related activities"},
                {"title": "Skill Development", "detail": "Engage in hands-on projects and practical applications"},
                {"title": "Career Exploration", "detail": "Research careers in your top scoring areas"}
            ],
            "exams_or_paths": ["JEE", "NEET"] if top_stream == "Science" else (
                              ["CA", "CS", "CMA"] if top_stream == "Commerce" else (
                              ["UPSC", "BA"] if top_stream == "Arts" else ["ITI", "Diploma"]))
        }
        
        return {
            "attempt_id": attempt.attempt_id,
            "scores": scores,
            "recommendations": recommendations,
            "top_stream": top_stream,
            "suggested_subjects": suggested_subjects[:5],  # Top 5 unique subjects
            "rationale": rationale,
            "ai_advice": ai_advice,
            "message": "Quiz submitted successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit quiz: {str(e)}")


@router.get("/quiz/attempts/{user_id}", response_model=List[Attempt])
def get_user_attempts(user_id: str):
    """Get all quiz attempts for a user"""
    user_attempts = [a for a in attempts_data if a.get("user_id") == user_id]
    return [Attempt(**attempt) for attempt in user_attempts]
