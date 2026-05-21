"""Structured response generation."""

from __future__ import annotations

from typing import Dict, List

from knowledge_base import KnowledgeStore, LogicReasoner


class ResponseGenerator:
    """Combines rule responses, knowledge lookup, and logic explanations."""

    def __init__(self, faq: Dict[str, str], knowledge: KnowledgeStore, reasoner: LogicReasoner) -> None:
        self.faq = faq
        self.knowledge = knowledge
        self.reasoner = reasoner

    def generate(self, intent: str, message: str, keywords: List[str], context: str) -> str:
        text = message.lower()

        if intent == "greeting":
            return (
                "Hello! I am your AI-Powered Chatbot Assistant.\n"
                "I can help with AI concepts, troubleshooting, search algorithms, and expert reasoning."
            )
        if intent == "help":
            return (
                "Here is how I can help:\n"
                "1) Explain AI concepts and FAQs\n"
                "2) Run BFS/DFS demonstrations\n"
                "3) Provide expert-system diagnostics\n"
                "4) Recommend best options using heuristics\n"
                "Type your question, or use the main dashboard for modules."
            )
        if intent == "faq":
            for question, answer in self.faq.items():
                if question in text:
                    return answer
            if "about" in keywords:
                target = keywords[-1]
                return self.knowledge.explain_entity(target)
            return "I can explain AI topics. Ask directly, e.g., 'What is heuristic?'"
        if intent == "troubleshoot":
            return (
                "Troubleshooting strategy:\n"
                "- Identify observable symptoms\n"
                "- Reproduce the problem\n"
                "- Isolate variables\n"
                "- Apply targeted fixes\n"
                "Would you like to run the Expert System module for a diagnosis?"
            )
        if intent == "search":
            return (
                "Search module suggestion: Use BFS for shortest path in unweighted graphs, "
                "and DFS for deep exploration with lower memory in some cases."
            )
        if intent == "expert":
            return "For expert recommendations, open the Expert System from the main menu and answer the rule-based diagnostic questions."
        if intent == "goodbye":
            return "Goodbye! Session memory will remain active until you close the program."

        facts = {
            "wants_algorithm_help": any(word in text for word in ("algorithm", "search", "bfs", "dfs")),
            "mentions_bfs_dfs": "bfs" in text or "dfs" in text,
            "wants_troubleshooting": any(word in text for word in ("error", "issue", "problem", "fix")),
            "issue_keywords": any(word in text for word in ("slow", "crash", "disconnect", "freeze")),
            "wants_definition": any(word in text for word in ("what is", "define", "meaning")),
        }
        logic_result = self.reasoner.evaluate(facts)
        return (
            "I could not match a direct intent confidently, so I used symbolic reasoning.\n"
            f"Conclusion: {logic_result.conclusion}\n"
            f"Confidence: {logic_result.confidence:.2f}\n"
            "Why:\n"
            + "\n".join(f"- {step}" for step in logic_result.explanation)
            + "\n"
            f"Session context:\n{context}"
        )

