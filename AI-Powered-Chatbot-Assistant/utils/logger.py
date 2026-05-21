"""Reasoning log helper."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class ReasoningLogger:
    """Collects explainable AI reasoning steps."""

    steps: List[str] = field(default_factory=list)

    def add(self, message: str) -> None:
        self.steps.append(message)

    def clear(self) -> None:
        self.steps.clear()

    def render(self) -> str:
        if not self.steps:
            return "No reasoning steps recorded."
        return "\n".join(f"- {step}" for step in self.steps)

