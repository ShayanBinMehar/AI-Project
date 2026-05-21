"""Interactive expert system runner."""

from __future__ import annotations

from typing import Set

from utils.ui import TerminalUI

from .inference_engine import ForwardChainingEngine, InferenceResult
from .knowledge_base import ExpertKnowledgeBase
from .rule_engine import RuleEngine


class ExpertSystemSession:
    """Handles Q&A and diagnostic inference."""

    def __init__(self, knowledge_base: ExpertKnowledgeBase, ui: TerminalUI) -> None:
        self.knowledge_base = knowledge_base
        self.ui = ui
        self.engine = ForwardChainingEngine(RuleEngine(knowledge_base.rules))

    def run(self) -> InferenceResult:
        self.ui.panel(
            "Expert System",
            f"Domain: {self.knowledge_base.domain}\nAnswer each question with yes or no.",
            style="cyan",
        )
        facts: Set[str] = set()
        for question in self.knowledge_base.questions:
            response = self.ui.ask(question.question).lower()
            if response in {"yes", "y"}:
                facts.add(question.fact)

        with self.ui.spinner("Running forward-chaining inference..."):
            result = self.engine.infer(facts)

        explanation = "\n".join(result.explanation)
        recommendations = "\n".join(f"- {item}" for item in result.recommendations) or "- No recommendation available."
        self.ui.panel(
            "Inference Report",
            f"Fired Rules: {result.fired_rules or 'None'}\n\nReasoning:\n{explanation}\n\nRecommendations:\n{recommendations}",
            style="green",
        )
        return result

