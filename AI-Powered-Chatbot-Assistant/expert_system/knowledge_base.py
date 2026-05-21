"""Expert system knowledge base."""

from __future__ import annotations

from pathlib import Path
from typing import List

from utils.loader import load_json

from .models import Question, Rule


class ExpertKnowledgeBase:
    """Loads and stores questions and production rules."""

    def __init__(self, rules_file: Path) -> None:
        payload = load_json(rules_file)
        self.domain = payload.get("domain", "generic")
        self.questions: List[Question] = [
            Question(id=item["id"], question=item["question"], fact=item["fact"])
            for item in payload.get("questions", [])
        ]
        self.rules: List[Rule] = [
            Rule(
                id=item["id"],
                conditions=item.get("if", []),
                conclusion=item.get("then", ""),
                recommendation=item.get("recommendation", ""),
            )
            for item in payload.get("rules", [])
        ]

