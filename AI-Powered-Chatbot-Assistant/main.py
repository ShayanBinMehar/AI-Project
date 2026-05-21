"""AI-Powered Chatbot Assistant: mini AI framework project."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict

from chatbot import ChatbotAssistant, ResponseGenerator
from expert_system import ExpertKnowledgeBase, ExpertSystemSession
from gui import run_gui
from heuristics import HeuristicRecommender
from knowledge_base import KnowledgeStore, LogicReasoner
from search_algorithms import GraphSearchEngine, default_graph, save_search_visualization
from utils import TerminalUI, load_json


class AIPoweredAssistantApp:
    """Main application orchestrator for all AI modules."""

    def __init__(self) -> None:
        self.root = Path(__file__).resolve().parent
        self.ui = TerminalUI()

        faq_data = load_json(self.root / "data" / "faq.json")
        self.knowledge = KnowledgeStore(self.root / "data" / "knowledge_graph.json")
        reasoner = LogicReasoner()
        self.chatbot = ChatbotAssistant(ResponseGenerator(faq=faq_data, knowledge=self.knowledge, reasoner=reasoner))

        self.search_engine = GraphSearchEngine(default_graph())
        self.expert_knowledge = ExpertKnowledgeBase(self.root / "rules" / "expert_rules.json")
        self.heuristics = HeuristicRecommender()

    def run(self) -> None:
        self.ui.banner(
            "AI-Powered Chatbot Assistant",
            "Rule-Based AI | Heuristics | BFS/DFS | Expert System | Logic Reasoning",
        )
        while True:
            self.ui.show_menu(
                "Main Dashboard",
                [
                    "Interactive Chatbot",
                    "Expert System (Forward Chaining)",
                    "Search Algorithms (BFS vs DFS)",
                    "Heuristic Recommendation Engine",
                    "Knowledge Representation Explorer",
                    "Show Session Conversation History",
                    "Exit",
                ],
            )
            choice = self.ui.ask("Select an option (1-7):")
            actions = {
                "1": self.chatbot_mode,
                "2": self.expert_mode,
                "3": self.search_mode,
                "4": self.heuristic_mode,
                "5": self.knowledge_mode,
                "6": self.history_mode,
                "7": self.exit_mode,
            }
            action = actions.get(choice)
            if action:
                action()
            else:
                self.ui.warning("Invalid choice. Please select a valid menu option.")

    def chatbot_mode(self) -> None:
        self.ui.panel(
            "Chatbot Console",
            "Type messages to chat with the assistant. Type 'back' to return to dashboard.",
            style="magenta",
        )
        while True:
            user_input = self.ui.ask("You:")
            if user_input.lower() == "back":
                break

            with self.ui.spinner("Analyzing intent and generating response..."):
                reply = self.chatbot.process(user_input)
            body = (
                f"{reply.response}\n\n"
                f"[Intent: {reply.intent} | Confidence: {reply.confidence:.2f}]\n"
                f"Extracted Keywords: {', '.join(reply.keywords[:10]) or 'None'}"
            )
            self.ui.panel("Assistant", body, style="blue")

            feedback = self.ui.ask("Was this response helpful? (yes/no/skip)").lower()
            if feedback in {"yes", "y"}:
                self.chatbot.submit_feedback(reply.intent, helpful=True)
            elif feedback in {"no", "n"}:
                self.chatbot.submit_feedback(reply.intent, helpful=False)

    def expert_mode(self) -> None:
        session = ExpertSystemSession(self.expert_knowledge, self.ui)
        session.run()

    def search_mode(self) -> None:
        self.ui.panel(
            "Search Lab",
            "Nodes available: A, B, C, D, E, F, G, H, I, J\nEnter start and goal nodes to compare BFS and DFS.",
            style="yellow",
        )
        start = self.ui.ask("Start node:").upper()
        goal = self.ui.ask("Goal node:").upper()

        if start not in self.search_engine.graph or goal not in self.search_engine.graph:
            self.ui.error("Invalid nodes. Please choose nodes from the listed set.")
            return

        with self.ui.spinner("Running BFS and DFS..."):
            bfs_result = self.search_engine.bfs(start, goal)
            dfs_result = self.search_engine.dfs(start, goal)

        summary = self._format_search_comparison(bfs_result.__dict__, dfs_result.__dict__)
        self.ui.panel("Search Comparison", summary, style="green")

        visual_dir = self.root / "outputs"
        bfs_plot = visual_dir / f"bfs_{start}_{goal}.png"
        dfs_plot = visual_dir / f"dfs_{start}_{goal}.png"
        save_search_visualization(self.search_engine.graph, bfs_result.path, bfs_result.traversal_order, bfs_plot)
        save_search_visualization(self.search_engine.graph, dfs_result.path, dfs_result.traversal_order, dfs_plot)
        self.ui.info(f"Visualizations saved:\n- {bfs_plot}\n- {dfs_plot}")

    def heuristic_mode(self) -> None:
        self.ui.panel(
            "Heuristic Decision Engine",
            "Demo: Best study strategy recommendation using weighted scoring.",
            style="cyan",
        )
        candidates: Dict[str, Dict[str, float]] = {
            "Revision + Practice Problems": {
                "difficulty_fit": 0.88,
                "time_efficiency": 0.75,
                "impact": 0.93,
                "resource_availability": 0.95,
            },
            "Video Lectures + Notes": {
                "difficulty_fit": 0.72,
                "time_efficiency": 0.82,
                "impact": 0.78,
                "resource_availability": 0.9,
            },
            "Group Discussion + Mock Test": {
                "difficulty_fit": 0.8,
                "time_efficiency": 0.65,
                "impact": 0.89,
                "resource_availability": 0.7,
            },
        }
        ranked = self.heuristics.rank(candidates)
        lines = []
        for idx, item in enumerate(ranked, start=1):
            lines.append(f"{idx}. {item.name} | Score={item.score:.3f} | Features: {item.rationale}")
        lines.append("\nTop recommendation selected using weighted heuristic evaluation.")
        self.ui.panel("Recommendation Report", "\n".join(lines), style="green")

    def knowledge_mode(self) -> None:
        entity = self.ui.ask("Enter an entity to inspect (e.g., ai, bfs, chatbot):").lower()
        explanation = self.knowledge.explain_entity(entity)
        self.ui.panel("Knowledge Graph Query Result", explanation, style="blue")

    def history_mode(self) -> None:
        self.ui.panel("Conversation Memory", self.chatbot.history_summary(), style="white")

    def exit_mode(self) -> None:
        self.ui.info("Thank you for using the AI-Powered Chatbot Assistant.")
        raise SystemExit(0)

    @staticmethod
    def _format_search_comparison(bfs: Dict[str, object], dfs: Dict[str, object]) -> str:
        bfs_path = bfs["path"] if bfs["path"] else ["No path found"]
        dfs_path = dfs["path"] if dfs["path"] else ["No path found"]
        shortest_note = (
            "BFS provides shortest path guarantee in unweighted graphs."
            if len(bfs_path) <= len(dfs_path)
            else "DFS found a shorter/equal path in this run, but without global guarantee."
        )
        return (
            "BFS:\n"
            f"- Traversal: {bfs['traversal_order']}\n"
            f"- Path: {bfs_path}\n"
            f"- Nodes explored: {bfs['nodes_explored']}\n"
            f"- Path cost: {bfs['path_cost']}\n"
            f"- Execution time: {bfs['elapsed_ms']} ms\n\n"
            "DFS:\n"
            f"- Traversal: {dfs['traversal_order']}\n"
            f"- Path: {dfs_path}\n"
            f"- Nodes explored: {dfs['nodes_explored']}\n"
            f"- Path cost: {dfs['path_cost']}\n"
            f"- Execution time: {dfs['elapsed_ms']} ms\n\n"
            f"Shortest path analysis: {shortest_note}"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI-Powered Chatbot Assistant")
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Launch desktop GUI instead of terminal UI.",
    )
    args = parser.parse_args()

    if args.gui:
        run_gui()
    else:
        app = AIPoweredAssistantApp()
        app.run()

