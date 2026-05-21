"""Search visualization helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import matplotlib.pyplot as plt
import networkx as nx


def save_search_visualization(
    graph: Dict[str, List[str]],
    path: List[str],
    traversal_order: List[str],
    output_file: Path,
) -> None:
    """Create and save a graph visualization highlighting selected path."""
    directed_graph = nx.DiGraph()
    for source, neighbors in graph.items():
        for target in neighbors:
            directed_graph.add_edge(source, target)
        if not neighbors:
            directed_graph.add_node(source)

    positions = nx.spring_layout(directed_graph, seed=7)
    node_colors = []
    for node in directed_graph.nodes():
        if node in path:
            node_colors.append("limegreen")
        elif node in traversal_order:
            node_colors.append("gold")
        else:
            node_colors.append("lightblue")

    edge_colors = []
    path_edges = {(path[index], path[index + 1]) for index in range(len(path) - 1)}
    for edge in directed_graph.edges():
        edge_colors.append("green" if edge in path_edges else "gray")

    plt.figure(figsize=(8, 6))
    nx.draw(
        directed_graph,
        positions,
        with_labels=True,
        node_color=node_colors,
        edge_color=edge_colors,
        node_size=1300,
        font_size=10,
        font_weight="bold",
        arrows=True,
    )
    plt.title("Search Traversal and Final Path")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_file, dpi=140)
    plt.close()

