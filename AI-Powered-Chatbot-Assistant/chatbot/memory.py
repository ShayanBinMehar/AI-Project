"""Conversation memory and lightweight feedback learning."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Tuple


@dataclass
class ConversationMemory:
    """Stores in-session conversational context."""

    history: List[Tuple[str, str]] = field(default_factory=list)
    user_preferences: Dict[str, str] = field(default_factory=dict)
    feedback_weights: Dict[str, float] = field(default_factory=lambda: defaultdict(float))

    def remember_exchange(self, user_message: str, assistant_message: str) -> None:
        self.history.append((user_message, assistant_message))
        if len(self.history) > 20:
            self.history.pop(0)

    def set_preference(self, key: str, value: str) -> None:
        self.user_preferences[key] = value

    def get_recent_context(self) -> str:
        if not self.history:
            return "No prior context in this session."
        recent = self.history[-3:]
        return "\n".join(f"User: {u}\nAssistant: {a}" for u, a in recent)

    def apply_feedback(self, intent: str, helpful: bool) -> None:
        delta = 0.05 if helpful else -0.05
        self.feedback_weights[intent] += delta

