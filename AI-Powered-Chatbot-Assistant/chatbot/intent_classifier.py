"""Intent matching, keyword extraction, and confidence scoring."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List, Set


@dataclass
class IntentResult:
    """Intent classification result."""

    intent: str
    confidence: float
    keywords: List[str]
    scores: Dict[str, float]


class IntentClassifier:
    """Rule-based intent classifier with heuristic scoring."""

    def __init__(self) -> None:
        self.intent_keywords: Dict[str, Set[str]] = {
            "greeting": {"hello", "hi", "hey", "good morning"},
            "help": {"help", "assist", "guide", "support"},
            "faq": {"what is", "explain", "define", "difference"},
            "troubleshoot": {"issue", "error", "problem", "fix", "broken", "slow"},
            "search": {"bfs", "dfs", "path", "graph", "search"},
            "expert": {"diagnose", "expert", "recommendation", "symptom"},
            "goodbye": {"bye", "exit", "quit", "goodbye"},
        }

    def classify(self, message: str) -> IntentResult:
        text = message.lower()
        tokens = self.extract_keywords(text)
        scores: Dict[str, float] = {}

        for intent, keywords in self.intent_keywords.items():
            keyword_matches = sum(1 for keyword in keywords if keyword in text)
            token_overlap = sum(1 for token in tokens if token in keywords)
            base_score = keyword_matches * 0.5 + token_overlap * 0.3
            scores[intent] = base_score

        best_intent = max(scores, key=scores.get)
        max_score = max(scores.values()) if scores else 0.0
        confidence = min(0.99, 0.4 + max_score * 0.25)
        if max_score < 0.5:
            best_intent = "fallback"
            confidence = 0.42

        return IntentResult(
            intent=best_intent,
            confidence=round(confidence, 3),
            keywords=tokens,
            scores=scores,
        )

    @staticmethod
    def extract_keywords(text: str) -> List[str]:
        return re.findall(r"[a-zA-Z_]{3,}", text)

