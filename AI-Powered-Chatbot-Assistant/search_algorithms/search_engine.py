"""BFS and DFS implementations for state-space search."""

from __future__ import annotations

from dataclasses import dataclass
from queue import Queue
from time import perf_counter
from typing import Dict, List, Optional


@dataclass
class SearchResult:
    """Contains traversal and path analytics."""

    algorithm: str
    traversal_order: List[str]
    path: List[str]
    nodes_explored: int
    path_cost: int
    elapsed_ms: float
    is_shortest_path_guaranteed: bool


class GraphSearchEngine:
    """Graph search implementation with BFS and DFS."""

    def __init__(self, graph: Dict[str, List[str]]) -> None:
        self.graph = graph

    def bfs(self, start: str, goal: str) -> SearchResult:
        start_time = perf_counter()
        queue: Queue[str] = Queue()
        queue.put(start)
        visited = {start}
        parent: Dict[str, Optional[str]] = {start: None}
        traversal_order: List[str] = []

        while not queue.empty():
            current = queue.get()
            traversal_order.append(current)
            if current == goal:
                break

            for neighbor in self.graph.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.put(neighbor)

        path = self._reconstruct_path(parent, start, goal)
        elapsed_ms = (perf_counter() - start_time) * 1000
        return SearchResult(
            algorithm="BFS",
            traversal_order=traversal_order,
            path=path,
            nodes_explored=len(traversal_order),
            path_cost=max(len(path) - 1, 0),
            elapsed_ms=round(elapsed_ms, 3),
            is_shortest_path_guaranteed=True,
        )

    def dfs(self, start: str, goal: str) -> SearchResult:
        start_time = perf_counter()
        stack = [start]
        visited = set()
        parent: Dict[str, Optional[str]] = {start: None}
        traversal_order: List[str] = []

        while stack:
            current = stack.pop()
            if current in visited:
                continue

            visited.add(current)
            traversal_order.append(current)
            if current == goal:
                break

            for neighbor in reversed(self.graph.get(current, [])):
                if neighbor not in visited:
                    if neighbor not in parent:
                        parent[neighbor] = current
                    stack.append(neighbor)

        path = self._reconstruct_path(parent, start, goal)
        elapsed_ms = (perf_counter() - start_time) * 1000
        return SearchResult(
            algorithm="DFS",
            traversal_order=traversal_order,
            path=path,
            nodes_explored=len(traversal_order),
            path_cost=max(len(path) - 1, 0),
            elapsed_ms=round(elapsed_ms, 3),
            is_shortest_path_guaranteed=False,
        )

    @staticmethod
    def _reconstruct_path(parent: Dict[str, Optional[str]], start: str, goal: str) -> List[str]:
        if goal not in parent:
            return []
        path = [goal]
        while path[-1] != start:
            previous = parent.get(path[-1])
            if previous is None:
                return []
            path.append(previous)
        path.reverse()
        return path

