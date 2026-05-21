"""Forward-chaining inference engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Set

from .rule_engine import RuleEngine


@dataclass
class InferenceResult:
    """Inference output details."""

    inferred_facts: Set[str] = field(default_factory=set)
    fired_rules: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    explanation: List[str] = field(default_factory=list)


class ForwardChainingEngine:
    """Executes forward chaining over rule base."""

    def __init__(self, rule_engine: RuleEngine) -> None:
        self.rule_engine = rule_engine

    def infer(self, initial_facts: Set[str]) -> InferenceResult:
        known_facts = set(initial_facts)
        result = InferenceResult(inferred_facts=set(initial_facts))
        changed = True

        while changed:
            changed = False
            for rule in self.rule_engine.applicable_rules(known_facts):
                if rule.conclusion in known_facts:
                    continue
                known_facts.add(rule.conclusion)
                result.inferred_facts.add(rule.conclusion)
                result.fired_rules.append(rule.id)
                result.recommendations.append(rule.recommendation)
                result.explanation.append(
                    f"Rule {rule.id} fired because {rule.conditions} were satisfied -> {rule.conclusion}"
                )
                changed = True

        if not result.fired_rules:
            result.explanation.append("No rules fired. Insufficient evidence from provided facts.")
        return result

