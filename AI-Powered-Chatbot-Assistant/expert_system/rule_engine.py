"""Rule matching engine."""

from __future__ import annotations

from typing import List, Set

from .models import Rule


class RuleEngine:
    """Evaluates production rules against known facts."""

    def __init__(self, rules: List[Rule]) -> None:
        self.rules = rules

    def applicable_rules(self, facts: Set[str]) -> List[Rule]:
        return [rule for rule in self.rules if set(rule.conditions).issubset(facts)]

