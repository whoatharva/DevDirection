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
        # Calculate scores
        scores = calculate_scores(payload.answers)
        
        # Generate career recommendations
        recommendations = generate_recommendations(scores)
        
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
        
        # Determine top stream based on highest score
        top_stream = max(scores.items(), key=lambda x: x[1])[0].title()
        
        # Generate suggested subjects based on scores with improved logic
        suggested_subjects = []
        
        # Technical subjects (for high technical scores)
        if scores["technical"] >= 20:
            suggested_subjects.extend([
                "Mathematics", "Physics", "Computer Science", "Engineering", 
                "Information Technology", "Data Science", "Cybersecurity"
            ])
        elif scores["technical"] >= 15:
            suggested_subjects.extend(["Mathematics", "Physics", "Computer Science"])
        
        # Creative subjects (for high creative scores)
        if scores["creative"] >= 20:
            suggested_subjects.extend([
                "Fine Arts", "Graphic Design", "Digital Media", "Creative Writing",
                "Music", "Drama", "Visual Arts", "Architecture"
            ])
        elif scores["creative"] >= 15:
            suggested_subjects.extend(["Literature", "Arts", "Design"])
        
        # Analytical subjects (for high analytical scores)
        if scores["analytical"] >= 20:
            suggested_subjects.extend([
                "Economics", "Statistics", "Business Analytics", "Finance",
                "Accounting", "Research Methods", "Data Analysis"
            ])
        elif scores["analytical"] >= 15:
            suggested_subjects.extend(["Economics", "Statistics", "Business Studies"])
        
        # Social subjects (for high social scores)
        if scores["social"] >= 20:
            suggested_subjects.extend([
                "Psychology", "Sociology", "Communication Studies", "Social Work",
                "Human Resources", "Public Relations", "Counseling"
            ])
        elif scores["social"] >= 15:
            suggested_subjects.extend(["Psychology", "Sociology", "Communication"])
        
        # Leadership subjects (for high leadership scores)
        if scores["leadership"] >= 20:
            suggested_subjects.extend([
                "Business Administration", "Management Studies", "Leadership Development",
                "Public Administration", "Strategic Planning", "Organizational Behavior"
            ])
        elif scores["leadership"] >= 15:
            suggested_subjects.extend(["Management", "Leadership Studies", "Public Administration"])
        
        # Add interdisciplinary subjects based on combinations
        if scores["technical"] >= 15 and scores["analytical"] >= 15:
            suggested_subjects.extend(["Data Science", "Business Intelligence", "Quantitative Analysis"])
        
        if scores["creative"] >= 15 and scores["social"] >= 15:
            suggested_subjects.extend(["Digital Marketing", "User Experience Design", "Media Studies"])
        
        if scores["leadership"] >= 15 and scores["analytical"] >= 15:
            suggested_subjects.extend(["Strategic Management", "Operations Research", "Project Management"])
        
        # Generate rationale
        rationale = f"Based on your responses, you show strong aptitude in {top_stream.lower()} areas. Your scores indicate: "
        rationale += f"Technical skills ({scores['technical']:.1f}%), Creative thinking ({scores['creative']:.1f}%), "
        rationale += f"Analytical ability ({scores['analytical']:.1f}%), Social skills ({scores['social']:.1f}%), "
        rationale += f"and Leadership potential ({scores['leadership']:.1f}%)."
        
        # Generate AI advice
        ai_advice = {
            "summary": f"Your profile suggests a strong inclination towards {top_stream.lower()} fields.",
            "next_steps": [
                {"title": "Focus Areas", "detail": f"Concentrate on {top_stream.lower()} subjects and related activities"},
                {"title": "Skill Development", "detail": "Engage in hands-on projects and practical applications"},
                {"title": "Career Exploration", "detail": "Research careers in your top scoring areas"}
            ],
            "exams_or_paths": ["JEE", "NEET", "Commerce Entrance", "Arts Stream"] if top_stream == "Technical" else ["Commerce Stream", "Arts Stream"]
        }
        
        return {
            "attempt_id": attempt.attempt_id,
            "scores": scores,
            "recommendations": recommendations,
            "top_stream": top_stream,
            "suggested_subjects": list(set(suggested_subjects))[:5],  # Top 5 unique subjects
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


def calculate_scores(answers: List[Dict[str, Any]]) -> Dict[str, float]:
    """Calculate scores based on quiz answers"""
    # Simple scoring logic - can be enhanced
    scores = {
        "technical": 0,
        "creative": 0,
        "analytical": 0,
        "social": 0,
        "leadership": 0,
        "vocational": 0
    }
    
    # Enhanced question-to-category mapping based on actual question content
    question_mapping = {
        "q1": ["technical", "analytical"],  # Problem-solving with technology
        "q2": ["technical", "analytical"],  # Math and logic
        "q3": ["creative", "analytical"],   # Design and creativity
        "q4": ["creative", "social"],       # Arts and communication
        "q5": ["vocational"],               # Data analysis -> vocational
        "q6": ["vocational"],               # Strategic thinking -> vocational
        "q7": ["social", "leadership"],     # Team work and leadership
        "q8": ["social", "creative"],       # Communication and presentation
        "q9": ["leadership", "social"],     # Leadership and management
        "q10": ["leadership", "analytical"] # Decision making and planning
    }
    
    for answer in answers:
        qid = answer.get("qid") if isinstance(answer, dict) else answer.qid
        score = answer.get("score") if isinstance(answer, dict) else answer.score
        
        # Apply score to all relevant categories for this question
        if qid in question_mapping:
            for category in question_mapping[qid]:
                scores[category] += float(score)
    
    # Max score per category = number of questions mapped to it * 3
    # Count how many questions map to each category
    category_counts = {k: 0 for k in scores}
    for cats in question_mapping.values():
        for cat in cats:
            if cat in category_counts:
                category_counts[cat] += 1

    for key in scores:
        max_possible = category_counts[key] * 3
        if max_possible > 0:
            scores[key] = (scores[key] / max_possible) * 100
        else:
            scores[key] = 0
    
    return scores


def generate_recommendations(scores: Dict[str, float]) -> List[str]:
    """Generate career recommendations based on scores"""
    recommendations = []
    
    if scores["technical"] > 70:
        recommendations.extend(["Software Engineer", "Data Scientist", "AI Engineer"])
    if scores["creative"] > 70:
        recommendations.extend(["UX Designer", "Marketing Manager", "Content Creator"])
    if scores["analytical"] > 70:
        recommendations.extend(["Business Analyst", "Financial Analyst", "Research Scientist"])
    if scores["social"] > 70:
        recommendations.extend(["Sales Manager", "HR Specialist", "Community Manager"])
    if scores["leadership"] > 70:
        recommendations.extend(["Project Manager", "Team Lead", "Entrepreneur"])
    
    return list(set(recommendations))[:5]  # Return top 5 unique recommendations