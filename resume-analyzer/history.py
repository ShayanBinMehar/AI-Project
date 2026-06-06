"""Persist analysis history to JSON files."""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

HISTORY_DIR = Path(__file__).parent / "data" / "history"


def save_analysis(result: dict[str, Any], resume_filename: str = "") -> str:
    """Save an analysis result and return its ID."""
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    analysis_id = str(uuid.uuid4())[:8]
    record = {
        "id": analysis_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "resume_filename": resume_filename,
        **result,
    }
    path = HISTORY_DIR / f"{analysis_id}.json"
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    return analysis_id


def list_analyses(limit: int = 20) -> list[dict[str, Any]]:
    """List recent analyses, newest first."""
    if not HISTORY_DIR.exists():
        return []

    files = sorted(HISTORY_DIR.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    records = []
    for path in files[:limit]:
        try:
            records.append(json.loads(path.read_text(encoding="utf-8")))
        except (json.JSONDecodeError, OSError):
            continue
    return records


def get_analysis(analysis_id: str) -> dict[str, Any] | None:
    """Retrieve a single analysis by ID."""
    path = HISTORY_DIR / f"{analysis_id}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))
