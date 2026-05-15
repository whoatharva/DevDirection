from typing import Dict, List, Tuple, Literal

Stream = Literal["Science", "Commerce", "Arts", "Vocational"]

# Positive likes add to these streams (all questions are positive statements, 0–3 scale)
LIKE_MAP: Dict[str, Stream] = {
    "q1": "Science",
    "q2": "Science",
    "q3": "Arts",
    "q4": "Commerce",
    "q5": "Vocational",
    "q6": "Vocational",
    "q7": "Commerce",
    "q8": "Science",
    "q9": "Commerce",
    "q10": "Arts"
}

SUGGESTED_SUBJECTS: Dict[Stream, List[str]] = {
    "Science": ["Physics", "Chemistry", "Mathematics", "Computer Science"],
    "Commerce": ["Accountancy", "Business Studies", "Economics", "Mathematics"],
    "Arts": ["History", "Political Science", "Psychology", "Literature"],
    "Vocational": ["IT/Networking", "Automobile", "Electrical", "Healthcare Assistant"]
}

def score_answers(answers: Dict[str, int]) -> Tuple[Dict[Stream, float], Stream, List[str], str]:
    scores: Dict[Stream, float] = { "Science": 0.0, "Commerce": 0.0, "Arts": 0.0, "Vocational": 0.0 }

    # Likes (0–3 scale)
    for qid, stream in LIKE_MAP.items():
        if qid in answers:
            scores[stream] += float(answers[qid])

    # No penalties; only positive additions

    max_scores = { "Science": 9.0, "Commerce": 9.0, "Arts": 6.0, "Vocational": 6.0 }

    # Floor at 0 and convert to percentages
    for st in scores:
        if scores[st] < 0:
            scores[st] = 0.0
        scores[st] = (scores[st] / max_scores[st]) * 100.0 if max_scores[st] > 0 else 0.0

    top_stream: Stream = max(scores, key=scores.get)  # type: ignore
    subjects = SUGGESTED_SUBJECTS[top_stream]

    rationale = {
        "Science":   "High logical/analytical inclination and comfort with problem-solving/tech.",
        "Commerce":  "Interest in business/markets with tolerance for quantitative reasoning.",
        "Arts":      "Strength in communication, reading/writing, and idea expression.",
        "Vocational":"Preference for practical, hands-on work over theory; applied learning fit."
    }[top_stream]

    return scores, top_stream, subjects, rationale

def mermaid_for_attempt(top_stream: Stream) -> str:
    return (
        "graph TD\n"
        "  User[User Profile] --> Quiz[10Q Quiz]\n"
        "  Quiz --> Traits[Score Calculation]\n"
        f"  Traits --> Stream[Top Stream Suggestion: {top_stream}]\n"
        "  Stream --> Subjects[Subjects Suggested]\n"
    )
