"""Logic-based reasoning and explanation generation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class LogicResult:
    """Reasoning result with explanation."""

    conclusion: str
    confidence: float
    explanation: List[str]


class LogicReasoner:
    """Simple symbolic reasoner over extracted user features."""

    def evaluate(self, facts: Dict[str, bool]) -> LogicResult:
        explanation: List[str] = []

        if facts.get("wants_algorithm_help") and facts.get("mentions_bfs_dfs"):
            explanation.append("Detected algorithm-learning intent.")
            explanation.append("Found explicit references to BFS/DFS concepts.")
            return LogicResult(
                conclusion="algorithm_guidance",
                confidence=0.92,
                explanation=explanation,
            )

        if facts.get("wants_troubleshooting") and facts.get("issue_keywords"):
            explanation.append("Detected troubleshooting context and issue terms.")
            return LogicResult(
                conclusion="troubleshooting_guidance",
                confidence=0.87,
                explanation=explanation,
            )

        if facts.get("wants_definition"):
            explanation.append("Detected educational query with definition intent.")
            return LogicResult(
                conclusion="educational_explanation",
                confidence=0.82,
                explanation=explanation,
            )

        explanation.append("No strong symbolic pattern matched.")
        return LogicResult(
            conclusion="general_assistance",
            confidence=0.55,
            explanation=explanation,
        )

