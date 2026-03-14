import os
from typing import Dict, List, Literal
from pydantic import BaseModel, Field

try:
    import google.generativeai as genai
    from google.generativeai import types
    GOOGLE_GENAI_AVAILABLE = True
except ImportError:
    try:
        from google import genai
        from google.genai import types
        GOOGLE_GENAI_AVAILABLE = True
    except ImportError:
        GOOGLE_GENAI_AVAILABLE = False
        genai = None
        types = None
except Exception as e:
    GOOGLE_GENAI_AVAILABLE = False
    genai = None
    types = None

Stream = Literal["Science", "Commerce", "Arts", "Vocational"]

# ---------- Structured Output schema ----------
class SubjectPlan(BaseModel):
    stream: Stream
    subjects: List[str]
    why: str

class ActionItem(BaseModel):
    title: str
    detail: str

class AiAdvice(BaseModel):
    summary: str                          # 2–3 lines summary
    recommended_stream: Stream            # one of the 4
    confidence: float = Field(ge=0, le=1) # 0–1
    subject_plan: SubjectPlan
    next_steps: List[ActionItem]          # 3–6 items
    exams_or_paths: List[str]             # GUJCET, Diploma->LE, etc.

_client = None

MODEL = "gemini-2.5-flash"

def get_client():
    if not GOOGLE_GENAI_AVAILABLE:
        raise ValueError("Google GenAI package not available. Please install: pip install google-genai")
    
    global _client
    if _client is not None:
        return _client

    # Read API key from environment (support common var names)
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(
            "Missing Google GenAI API key. Set GEMINI_API_KEY or GOOGLE_API_KEY in environment/.env"
        )

    _client = genai.Client(api_key=api_key)
    return _client

def build_prompt(user: dict, scores: Dict[Stream, float], planning_for: str = "") -> str:
    return f"""
You are a career and education advisor for Indian students (Gujarat context).
Given the user profile and stream scores, produce actionable guidance.

USER PROFILE (JSON):
{user}

STREAM SCORES (higher is better):
{scores}

PLANNING FOR: {planning_for}

Rules:
- Choose ONE recommended_stream from: Science, Commerce, Arts, Vocational.
- Keep advice practical and supportive; avoid over-claiming.
- Tailor lightly for Gujarat state context when relevant.
- Be consistent with the scores and don't contradict them.

CRITICAL PLANNING PREFERENCE RULES:
- If planning for "Diploma (Polytechnic)" or "ITI / Vocational": STRONGLY prioritize Vocational stream
- If planning for "11-12 (Science/Commerce/Arts)": Consider Science/Commerce/Arts based on scores
- If planning for "Degree (after 12th)": Consider all streams but align with preference

VOCATIONAL FOCUS (when Diploma/ITI selected):
- MANDATORY: Set recommended_stream to "Vocational" 
- MANDATORY: Use ONLY these subjects: ["IT/Networking", "Automobile", "Electrical", "Healthcare Assistant"]
- NEVER suggest: Physics, Chemistry, Mathematics, Computer Science, Literature, History, etc.
- Focus on 1-2 specific vocational fields maximum
- Emphasize immediate job readiness and hands-on skills
- Suggest specific ITI courses, polytechnic programs, or skill certifications
- Make subject_plan.subjects match the vocational subjects exactly
"""

def get_ai_advice(user: dict, scores: Dict[Stream, float], subjects_by_stream: Dict[Stream, List[str]], planning_for: str = "") -> AiAdvice:
    if not GOOGLE_GENAI_AVAILABLE:
        # Fallback to basic advice without AI
        top_stream = max(scores, key=scores.get)
        return AiAdvice(
            summary=f"Based on your quiz scores, {top_stream} stream is recommended for your career path.",
            recommended_stream=top_stream,
            confidence=0.7,
            subject_plan=SubjectPlan(
                stream=top_stream,
                subjects=subjects_by_stream.get(top_stream, []),
                why=f"Your quiz responses show strong alignment with {top_stream} stream preferences."
            ),
            next_steps=[
                ActionItem(title="Research Programs", detail=f"Look into {top_stream} programs and courses"),
                ActionItem(title="Connect with Professionals", detail="Network with people in your chosen field"),
                ActionItem(title="Start Learning", detail="Begin with foundational subjects in your stream")
            ],
            exams_or_paths=["Standard entrance exams", "Direct admission programs"]
        )

    prompt = build_prompt(user, scores, planning_for) + f"\nReference subjects by stream (context): {subjects_by_stream}"

    try:
        client = get_client()
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=AiAdvice,
                thinking_config=types.ThinkingConfig(thinking_budget=0)
            ),
        )
        return AiAdvice.model_validate_json(response.text)
    except Exception as e:
        # Fallback to basic advice if LLM call fails or response is not valid JSON
        top_stream = max(scores, key=scores.get)
        return AiAdvice(
            summary=f"Based on your quiz scores, {top_stream} stream is recommended for your career path.",
            recommended_stream=top_stream,
            confidence=0.7,
            subject_plan=SubjectPlan(
                stream=top_stream,
                subjects=subjects_by_stream.get(top_stream, []),
                why=f"Your quiz responses show strong alignment with {top_stream} stream preferences."
            ),
            next_steps=[
                ActionItem(title="Research Programs", detail=f"Look into {top_stream} programs and courses"),
                ActionItem(title="Connect with Professionals", detail="Network with people in your chosen field"),
                ActionItem(title="Start Learning", detail="Begin with foundational subjects in your stream")
            ],
            exams_or_paths=["Standard entrance exams", "Direct admission programs"]
        )
