"""Heuristic recommendation engine with weighted scoring."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Recommendation:
    """Represents one scored recommendation candidate."""

    name: str
    score: float
    rationale: str


class HeuristicRecommender:
    """Scores options using weighted feature values."""

    def __init__(self) -> None:
        self.weights = {
            "difficulty_fit": 0.35,
            "time_efficiency": 0.25,
            "impact": 0.25,
            "resource_availability": 0.15,
        }

    def score_option(self, name: str, features: Dict[str, float]) -> Recommendation:
        score = sum(features.get(feature, 0.0) * weight for feature, weight in self.weights.items())
        rationale = ", ".join(f"{k}={features.get(k, 0):.2f}" for k in self.weights)
        return Recommendation(name=name, score=round(score, 3), rationale=rationale)

    def rank(self, candidates: Dict[str, Dict[str, float]]) -> List[Recommendation]:
        recommendations = [self.score_option(name, features) for name, features in candidates.items()]
        return sorted(recommendations, key=lambda item: item.score, reverse=True)

