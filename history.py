import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any

HISTORY_FILE = "history.json"

def get_history() -> List[Dict[str, Any]]:
    """Load the diagnosis history from the JSON file."""
    if not os.path.exists(HISTORY_FILE):
        return []
    
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            history = json.load(f)
        return history
    except (json.JSONDecodeError, FileNotFoundError):
        # If file is empty or corrupted, return empty list
        return []

def save_history(history: List[Dict[str, Any]]) -> None:
    """Save the diagnosis history to the JSON file."""
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def add_record(user_description: str, 
               diagnosis: Dict[str, Any], 
               uploaded_files: List[str] = None) -> Dict[str, Any]:
    """Add a new diagnosis record to history."""
    if uploaded_files is None:
        uploaded_files = []
        
    record = {
        "id": generate_id(),
        "timestamp": datetime.now().isoformat(),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user_description": user_description,
        "uploaded_files": uploaded_files,
        "diagnosis": diagnosis,
        "feedback": None  # For storing user feedback (helpful/not helpful)
    }
    
    history = get_history()
    history.append(record)
    save_history(history)
    return record

def delete_record(record_id: str) -> bool:
    """Delete a specific record from history by ID."""
    history = get_history()
    original_length = len(history)
    
    history = [record for record in history if record.get("id") != record_id]
    
    if len(history) < original_length:
        save_history(history)
        return True
    return False

def clear_history() -> None:
    """Delete all history records."""
    save_history([])

def search_history(query: str) -> List[Dict[str, Any]]:
    """Search history for records containing the query string."""
    history = get_history()
    if not query:
        return history
    
    query = query.lower()
    results = []
    
    for record in history:
        # Search in user description
        if query in record.get("user_description", "").lower():
            results.append(record)
            continue
            
        # Search in diagnosis text
        diagnosis = record.get("diagnosis", {})
        if any(query in str(value).lower() for value in diagnosis.values()):
            results.append(record)
            
    return results

def generate_id() -> str:
    """Generate a simple unique ID based on timestamp."""
    return f"{int(datetime.now().timestamp())}"

def update_feedback(record_id: str, feedback: bool) -> bool:
    """Update the feedback for a specific record."""
    history = get_history()
    
    for record in history:
        if record.get("id") == record_id:
            record["feedback"] = feedback
            record["feedback_date"] = datetime.now().isoformat()
            save_history(history)
            return True
            
    return False

def get_feedback_stats() -> Dict[str, Any]:
    """Get statistics about feedback."""
    history = get_history()
    total = len(history)
    with_feedback = sum(1 for record in history if record.get("feedback") is not None)
    positive = sum(1 for record in history if record.get("feedback") is True)
    negative = sum(1 for record in history if record.get("feedback") is False)
    
    return {
        "total_records": total,
        "with_feedback": with_feedback,
        "positive_feedback": positive,
        "negative_feedback": negative,
        "feedback_rate": (with_feedback / total) * 100 if total > 0 else 0,
        "satisfaction_rate": (positive / with_feedback) * 100 if with_feedback > 0 else 0
    }
