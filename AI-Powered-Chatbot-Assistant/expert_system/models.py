"""Core expert system models."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class Question:
    """Diagnostic question model."""

    id: str
    question: str
    fact: str


@dataclass
class Rule:
    """Production rule model."""

    id: str
    conditions: List[str]
    conclusion: str
    recommendation: str

