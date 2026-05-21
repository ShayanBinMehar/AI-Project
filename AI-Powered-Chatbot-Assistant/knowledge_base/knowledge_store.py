"""Knowledge representation module."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple

from utils.loader import load_json


class KnowledgeStore:
    """Stores entities and semantic relationships for symbolic reasoning."""

    def __init__(self, knowledge_file: Path) -> None:
        payload = load_json(knowledge_file)
        self.entities: Dict[str, Dict[str, str]] = payload.get("entities", {})
        self.relationships: List[Tuple[str, str, str]] = [
            tuple(item) for item in payload.get("relationships", [])
        ]

    def describe_entity(self, entity: str) -> str:
        info = self.entities.get(entity.lower())
        if not info:
            return f"I do not currently store knowledge about '{entity}'."
        return f"{entity}: {info.get('description', 'No description available.')}"

    def find_relationships(self, entity: str) -> List[Tuple[str, str, str]]:
        entity = entity.lower()
        return [
            relation
            for relation in self.relationships
            if relation[0] == entity or relation[2] == entity
        ]

    def explain_entity(self, entity: str) -> str:
        relationships = self.find_relationships(entity)
        if not relationships:
            return self.describe_entity(entity)

        lines = [self.describe_entity(entity), "Known relationships:"]
        for source, relation, target in relationships:
            lines.append(f"- {source} {relation} {target}")
        return "\n".join(lines)

