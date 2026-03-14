"""
Utility functions for the Career Guidance Platform
"""
import json
from pathlib import Path
from typing import Any, List, Dict, Optional


def load_json(file_path: Path, default: Any = None) -> Any:
    """Load JSON data from file with error handling"""
    try:
        if not file_path.exists():
            return default if default is not None else []
        
        with file_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error loading {file_path}: {e}")
        return default if default is not None else []


def save_json(file_path: Path, data: Any) -> bool:
    """Save data to JSON file with error handling"""
    try:
        # Ensure directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with file_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)
        return True
    except Exception as e:
        print(f"Error saving {file_path}: {e}")
        return False


def generate_id(prefix: str = "") -> str:
    """Generate a unique ID"""
    import uuid
    return f"{prefix}{str(uuid.uuid4())[:8]}" if prefix else str(uuid.uuid4())[:8]


def validate_required_fields(data: Dict, required_fields: List[str]) -> List[str]:
    """Validate that required fields are present in data"""
    missing_fields = []
    for field in required_fields:
        if field not in data or data[field] is None or data[field] == "":
            missing_fields.append(field)
    return missing_fields
