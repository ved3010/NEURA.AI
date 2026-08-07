"""
E.D.I.T.H. Persistent Tactical Memory Core
Saves and recalls user preferences, tactical notes, and task lists.
"""

import json
import os
import logging
from typing import Dict, List, Any

logger = logging.getLogger("edith.memory")
MEMORY_FILE = os.path.expanduser("~/.edith_memory.json")


def _load_memory() -> Dict[str, Any]:
    if not os.path.exists(MEMORY_FILE):
        return {"notes": {}, "tasks": [], "history": []}
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load memory file: {e}")
        return {"notes": {}, "tasks": [], "history": []}


def _save_memory(data: Dict[str, Any]) -> bool:
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        logger.error(f"Failed to save memory file: {e}")
        return False


def remember_fact(key: str, value: str) -> str:
    """Store a fact or note in E.D.I.T.H. memory core."""
    data = _load_memory()
    data["notes"][key.strip().lower()] = value.strip()
    _save_memory(data)
    return f"Tactical note recorded: [{key}] -> '{value}'"


def recall_memory(key: str = "") -> str:
    """Recall stored facts or notes from E.D.I.T.H. memory core."""
    data = _load_memory()
    notes = data.get("notes", {})
    if not notes:
        return "E.D.I.T.H. memory core is currently empty."
    
    if key:
        key_lower = key.strip().lower()
        if key_lower in notes:
            return f"E.D.I.T.H. Memory [{key}]: {notes[key_lower]}"
        matches = {k: v for k, v in notes.items() if key_lower in k}
        if matches:
            return f"E.D.I.T.H. Memory Matches: {json.dumps(matches, indent=2)}"
        return f"No tactical memory entry found for '{key}'."
    
    return f"E.D.I.T.H. All Memory Notes: {json.dumps(notes, indent=2)}"


def add_task(task_description: str) -> str:
    """Add a new task to E.D.I.T.H. task roster."""
    data = _load_memory()
    tasks = data.get("tasks", [])
    task_item = {"id": len(tasks) + 1, "task": task_description, "status": "pending"}
    tasks.append(task_item)
    data["tasks"] = tasks
    _save_memory(data)
    return f"Task #{task_item['id']} added to roster: '{task_description}'"


def get_tasks() -> str:
    """Get all current pending and completed tasks."""
    data = _load_memory()
    tasks = data.get("tasks", [])
    if not tasks:
        return "No tasks currently registered in E.D.I.T.H. roster."
    return f"E.D.I.T.H. Task Roster: {json.dumps(tasks, indent=2)}"
