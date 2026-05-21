"""Graph datasets for BFS/DFS demonstrations."""

from __future__ import annotations

from typing import Dict, List


def default_graph() -> Dict[str, List[str]]:
    """Return a connected unweighted graph."""
    return {
        "A": ["B", "C"],
        "B": ["D", "E"],
        "C": ["F"],
        "D": ["G"],
        "E": ["G", "H"],
        "F": ["I"],
        "G": ["J"],
        "H": ["J"],
        "I": ["J"],
        "J": [],
    }

