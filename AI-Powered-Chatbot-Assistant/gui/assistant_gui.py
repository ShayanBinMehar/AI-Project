"""Desktop GUI for the AI-Powered Chatbot Assistant."""

from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import messagebox, scrolledtext, ttk
from typing import Dict, List

import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from chatbot import ChatbotAssistant, ResponseGenerator
from expert_system import ExpertKnowledgeBase
from expert_system.inference_engine import ForwardChainingEngine
from expert_system.rule_engine import RuleEngine
from heuristics import HeuristicRecommender
from knowledge_base import KnowledgeStore, LogicReasoner
from search_algorithms import GraphSearchEngine, default_graph
from utils import load_json


class AssistantGUI(tk.Tk):
    """Main GUI application with tabbed modules."""

    def __init__(self) -> None:
        super().__init__()
        self.title("AI-Powered Chatbot Assistant | Professional GUI")
        self.geometry("1280x820")
        self.configure(bg="#f4f7fb")

        self.root_dir = Path(__file__).resolve().parent.parent
        faq_data = load_json(self.root_dir / "data" / "faq.json")
        self.knowledge = KnowledgeStore(self.root_dir / "data" / "knowledge_graph.json")
        self.chatbot = ChatbotAssistant(
            ResponseGenerator(
                faq=faq_data,
                knowledge=self.knowledge,
                reasoner=LogicReasoner(),
            )
        )
        self.expert_knowledge = ExpertKnowledgeBase(self.root_dir / "rules" / "expert_rules.json")
        self.forward_engine = ForwardChainingEngine(RuleEngine(self.expert_knowledge.rules))
        self.search_engine = GraphSearchEngine(default_graph())
        self.heuristics = HeuristicRecommender()

        self._build_header()
        self._build_tabs()

    def _build_header(self) -> None:
        header = ttk.Frame(self, padding=14)
        header.pack(fill=tk.X)

        title = ttk.Label(
            header,
            text="AI-Powered Chatbot Assistant",
            font=("Segoe UI", 20, "bold"),
        )
        title.pack(anchor=tk.W)
        subtitle = ttk.Label(
            header,
            text="Rule-Based AI | Expert System | BFS/DFS Search | Heuristics | Knowledge Reasoning",
            font=("Segoe UI", 10),
        )
        subtitle.pack(anchor=tk.W)

    def _build_tabs(self) -> None:
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)

        self.chat_tab = ttk.Frame(notebook, padding=10)
        self.expert_tab = ttk.Frame(notebook, padding=10)
        self.search_tab = ttk.Frame(notebook, padding=10)
        self.heuristic_tab = ttk.Frame(notebook, padding=10)
        self.knowledge_tab = ttk.Frame(notebook, padding=10)
        self.history_tab = ttk.Frame(notebook, padding=10)

        notebook.add(self.chat_tab, text="Chatbot")
        notebook.add(self.expert_tab, text="Expert System")
        notebook.add(self.search_tab, text="BFS/DFS Lab")
        notebook.add(self.heuristic_tab, text="Heuristic Recommender")
        notebook.add(self.knowledge_tab, text="Knowledge Graph")
        notebook.add(self.history_tab, text="Conversation History")

        self._build_chatbot_tab()
        self._build_expert_tab()
        self._build_search_tab()
        self._build_heuristics_tab()
        self._build_knowledge_tab()
        self._build_history_tab()

    def _build_chatbot_tab(self) -> None:
        top = ttk.Frame(self.chat_tab)
        top.pack(fill=tk.X, pady=(0, 8))
        ttk.Label(top, text="Enter message:", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT)

        self.chat_entry = ttk.Entry(top, width=95)
        self.chat_entry.pack(side=tk.LEFT, padx=8, fill=tk.X, expand=True)
        self.chat_entry.bind("<Return>", lambda _: self._send_chat_message())

        send_btn = ttk.Button(top, text="Send", command=self._send_chat_message)
        send_btn.pack(side=tk.LEFT, padx=4)

        self.chat_output = scrolledtext.ScrolledText(self.chat_tab, wrap=tk.WORD, height=28, font=("Consolas", 10))
        self.chat_output.pack(fill=tk.BOTH, expand=True)
        self.chat_output.insert(
            tk.END,
            "Assistant ready. Ask about AI, BFS/DFS, troubleshooting, or expert recommendations.\n\n",
        )

        feedback_frame = ttk.Frame(self.chat_tab)
        feedback_frame.pack(fill=tk.X, pady=8)
        ttk.Label(feedback_frame, text="Feedback for last response:", font=("Segoe UI", 10)).pack(side=tk.LEFT)
        ttk.Button(feedback_frame, text="Helpful", command=lambda: self._submit_feedback(True)).pack(side=tk.LEFT, padx=6)
        ttk.Button(feedback_frame, text="Not Helpful", command=lambda: self._submit_feedback(False)).pack(side=tk.LEFT)
        self.last_intent = "fallback"

    def _send_chat_message(self) -> None:
        message = self.chat_entry.get().strip()
        if not message:
            return

        reply = self.chatbot.process(message)
        self.last_intent = reply.intent
        self.chat_output.insert(tk.END, f"User: {message}\n")
        self.chat_output.insert(
            tk.END,
            f"Assistant: {reply.response}\n"
            f"[Intent={reply.intent} | Confidence={reply.confidence:.2f}]\n"
            f"Keywords={', '.join(reply.keywords[:10]) or 'None'}\n\n",
        )
        self.chat_output.see(tk.END)
        self.chat_entry.delete(0, tk.END)
        self._refresh_history()

    def _submit_feedback(self, helpful: bool) -> None:
        self.chatbot.submit_feedback(self.last_intent, helpful=helpful)
        status = "positive" if helpful else "negative"
        self.chat_output.insert(tk.END, f"[Feedback recorded: {status} for intent '{self.last_intent}']\n\n")
        self.chat_output.see(tk.END)

    def _build_expert_tab(self) -> None:
        prompt = ttk.Label(
            self.expert_tab,
            text="Answer diagnostic questions and run forward-chaining inference.",
            font=("Segoe UI", 10),
        )
        prompt.pack(anchor=tk.W, pady=(0, 8))

        self.expert_answers: Dict[str, tk.StringVar] = {}
        question_frame = ttk.Frame(self.expert_tab)
        question_frame.pack(fill=tk.X)
        for question in self.expert_knowledge.questions:
            row = ttk.Frame(question_frame)
            row.pack(fill=tk.X, pady=3)
            ttk.Label(row, text=question.question, width=72).pack(side=tk.LEFT, anchor=tk.W)
            var = tk.StringVar(value="no")
            self.expert_answers[question.fact] = var
            ttk.Combobox(row, textvariable=var, values=["yes", "no"], width=8, state="readonly").pack(side=tk.LEFT, padx=6)

        ttk.Button(self.expert_tab, text="Run Inference", command=self._run_expert_inference).pack(anchor=tk.W, pady=8)

        self.expert_output = scrolledtext.ScrolledText(self.expert_tab, wrap=tk.WORD, height=22, font=("Consolas", 10))
        self.expert_output.pack(fill=tk.BOTH, expand=True)

    def _run_expert_inference(self) -> None:
        facts = {fact for fact, var in self.expert_answers.items() if var.get().lower() == "yes"}
        result = self.forward_engine.infer(facts)

        self.expert_output.delete("1.0", tk.END)
        self.expert_output.insert(tk.END, f"Input facts: {sorted(facts) if facts else 'None'}\n")
        self.expert_output.insert(tk.END, f"Fired rules: {result.fired_rules or 'None'}\n")
        self.expert_output.insert(tk.END, f"Inferred facts: {sorted(result.inferred_facts)}\n\n")
        self.expert_output.insert(tk.END, "Reasoning trace:\n")
        for step in result.explanation:
            self.expert_output.insert(tk.END, f"- {step}\n")
        self.expert_output.insert(tk.END, "\nRecommendations:\n")
        if result.recommendations:
            for rec in result.recommendations:
                self.expert_output.insert(tk.END, f"- {rec}\n")
        else:
            self.expert_output.insert(tk.END, "- No recommendation available.\n")

    def _build_search_tab(self) -> None:
        control = ttk.Frame(self.search_tab)
        control.pack(fill=tk.X, pady=(0, 8))

        ttk.Label(control, text="Start Node:").pack(side=tk.LEFT)
        self.search_start = ttk.Entry(control, width=6)
        self.search_start.insert(0, "A")
        self.search_start.pack(side=tk.LEFT, padx=6)

        ttk.Label(control, text="Goal Node:").pack(side=tk.LEFT)
        self.search_goal = ttk.Entry(control, width=6)
        self.search_goal.insert(0, "J")
        self.search_goal.pack(side=tk.LEFT, padx=6)

        ttk.Button(control, text="Compare BFS/DFS", command=self._run_search).pack(side=tk.LEFT, padx=8)
        ttk.Label(control, text="Available: A-J", foreground="#555").pack(side=tk.LEFT, padx=8)

        self.search_output = scrolledtext.ScrolledText(self.search_tab, wrap=tk.WORD, height=13, font=("Consolas", 10))
        self.search_output.pack(fill=tk.X, pady=(0, 6))

        self.search_plot_frame = ttk.Frame(self.search_tab)
        self.search_plot_frame.pack(fill=tk.BOTH, expand=True)
        self.search_canvas = None

    def _run_search(self) -> None:
        start = self.search_start.get().strip().upper()
        goal = self.search_goal.get().strip().upper()
        if start not in self.search_engine.graph or goal not in self.search_engine.graph:
            messagebox.showerror("Invalid nodes", "Please use valid node names from A to J.")
            return

        bfs = self.search_engine.bfs(start, goal)
        dfs = self.search_engine.dfs(start, goal)
        shortest_note = (
            "BFS guarantees shortest path in this unweighted graph."
            if len(bfs.path) <= len(dfs.path)
            else "DFS found shorter/equal path in this run, but not guaranteed globally."
        )

        self.search_output.delete("1.0", tk.END)
        self.search_output.insert(
            tk.END,
            f"BFS Path: {bfs.path}\n"
            f"BFS Traversal: {bfs.traversal_order}\n"
            f"BFS Nodes Explored: {bfs.nodes_explored} | Cost: {bfs.path_cost} | Time: {bfs.elapsed_ms} ms\n\n"
            f"DFS Path: {dfs.path}\n"
            f"DFS Traversal: {dfs.traversal_order}\n"
            f"DFS Nodes Explored: {dfs.nodes_explored} | Cost: {dfs.path_cost} | Time: {dfs.elapsed_ms} ms\n\n"
            f"Shortest Path Analysis: {shortest_note}\n",
        )

        self._render_search_plot(path=bfs.path, traversal=bfs.traversal_order)

    def _render_search_plot(self, path: List[str], traversal: List[str]) -> None:
        graph = nx.DiGraph()
        for src, neighbors in self.search_engine.graph.items():
            for dst in neighbors:
                graph.add_edge(src, dst)
            if not neighbors:
                graph.add_node(src)

        fig, ax = plt.subplots(figsize=(7, 4.2), dpi=100)
        positions = nx.spring_layout(graph, seed=7)
        path_set = set(path)
        path_edges = {(path[index], path[index + 1]) for index in range(len(path) - 1)}

        node_colors = [
            "#16a34a" if node in path_set else "#facc15" if node in traversal else "#93c5fd"
            for node in graph.nodes()
        ]
        edge_colors = ["#16a34a" if edge in path_edges else "#64748b" for edge in graph.edges()]

        nx.draw(
            graph,
            positions,
            ax=ax,
            with_labels=True,
            node_color=node_colors,
            edge_color=edge_colors,
            node_size=1300,
            font_size=10,
            font_weight="bold",
            arrows=True,
        )
        ax.set_title("Search Traversal and Path Visualization")
        ax.axis("off")

        if self.search_canvas is not None:
            self.search_canvas.get_tk_widget().destroy()

        self.search_canvas = FigureCanvasTkAgg(fig, master=self.search_plot_frame)
        self.search_canvas.draw()
        self.search_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        plt.close(fig)

    def _build_heuristics_tab(self) -> None:
        ttk.Label(
            self.heuristic_tab,
            text="Weighted recommendation engine (study strategy demo).",
            font=("Segoe UI", 10),
        ).pack(anchor=tk.W, pady=(0, 8))
        ttk.Button(self.heuristic_tab, text="Generate Recommendation", command=self._run_heuristics).pack(anchor=tk.W)

        self.heuristics_output = scrolledtext.ScrolledText(
            self.heuristic_tab, wrap=tk.WORD, height=30, font=("Consolas", 10)
        )
        self.heuristics_output.pack(fill=tk.BOTH, expand=True, pady=8)

    def _run_heuristics(self) -> None:
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
        self.heuristics_output.delete("1.0", tk.END)
        self.heuristics_output.insert(tk.END, "Heuristic Ranking Result\n========================\n\n")
        for idx, item in enumerate(ranked, start=1):
            self.heuristics_output.insert(
                tk.END,
                f"{idx}. {item.name}\n   Score: {item.score:.3f}\n   Feature values: {item.rationale}\n\n",
            )
        self.heuristics_output.insert(tk.END, "Top option selected based on weighted utility score.\n")

    def _build_knowledge_tab(self) -> None:
        top = ttk.Frame(self.knowledge_tab)
        top.pack(fill=tk.X, pady=(0, 8))
        ttk.Label(top, text="Entity:").pack(side=tk.LEFT)
        self.entity_entry = ttk.Entry(top, width=20)
        self.entity_entry.insert(0, "ai")
        self.entity_entry.pack(side=tk.LEFT, padx=6)
        ttk.Button(top, text="Query", command=self._query_entity).pack(side=tk.LEFT)

        self.knowledge_output = scrolledtext.ScrolledText(
            self.knowledge_tab, wrap=tk.WORD, height=30, font=("Consolas", 10)
        )
        self.knowledge_output.pack(fill=tk.BOTH, expand=True)

    def _query_entity(self) -> None:
        entity = self.entity_entry.get().strip().lower()
        if not entity:
            return
        explanation = self.knowledge.explain_entity(entity)
        self.knowledge_output.delete("1.0", tk.END)
        self.knowledge_output.insert(tk.END, explanation)

    def _build_history_tab(self) -> None:
        top = ttk.Frame(self.history_tab)
        top.pack(fill=tk.X, pady=(0, 8))
        ttk.Button(top, text="Refresh History", command=self._refresh_history).pack(side=tk.LEFT)
        ttk.Button(top, text="Clear Chat View", command=self._clear_history_view).pack(side=tk.LEFT, padx=6)

        self.history_output = scrolledtext.ScrolledText(self.history_tab, wrap=tk.WORD, height=31, font=("Consolas", 10))
        self.history_output.pack(fill=tk.BOTH, expand=True)
        self._refresh_history()

    def _refresh_history(self) -> None:
        self.history_output.delete("1.0", tk.END)
        if not self.chatbot.memory.history:
            self.history_output.insert(tk.END, "No conversation history yet.")
            return

        for idx, (user_text, assistant_text) in enumerate(self.chatbot.memory.history, start=1):
            self.history_output.insert(tk.END, f"Exchange {idx}\n")
            self.history_output.insert(tk.END, f"User: {user_text}\n")
            self.history_output.insert(tk.END, f"Assistant: {assistant_text}\n")
            self.history_output.insert(tk.END, "-" * 70 + "\n")

    def _clear_history_view(self) -> None:
        self.history_output.delete("1.0", tk.END)
        self.history_output.insert(tk.END, "History panel cleared (session data still stored in chatbot memory).")


def run_gui() -> None:
    """Launch the GUI application."""
    app = AssistantGUI()
    app.mainloop()

