# AI-Powered Chatbot Assistant

A professional-grade, modular Artificial Intelligence course project in Python that combines conversational AI, expert systems, search algorithms, heuristic decision-making, knowledge representation, and explainable logic reasoning.

This project is built as a **mini AI framework**, not just a basic chatbot, and is designed for:
- university AI/software engineering submissions,
- portfolio showcasing on GitHub,
- resume-ready technical demonstrations.

## Features

### Core Chatbot
- Interactive CLI chatbot.
- Intent matching + keyword extraction.
- Heuristic confidence scoring.
- FAQ and educational concept responses.
- Troubleshooting and help workflows.
- Context memory for current session.
- Fallback handling with logic-based explanation.
- Simple learning from user feedback (confidence tuning).

### Expert System (Forward Chaining)
- IF-THEN production rules.
- Question-based fact gathering.
- Rule engine + inference engine + knowledge base separation.
- Inference explanations (which rule fired and why).
- Recommendation output for detected conditions.

### Search Algorithms Module
- Breadth-First Search (BFS).
- Depth-First Search (DFS).
- User-selectable start and goal nodes.
- Output includes traversal, path, nodes explored, path cost, and execution time.
- BFS vs DFS shortest-path analysis.
- Graph visualizations saved as PNG.

### Heuristic AI Module
- Weighted scoring model for decision-making.
- Ranks multiple options by utility score.
- Transparent rationale for each score.

### Knowledge Representation + Logic Reasoning
- Entity and relationship storage via symbolic structures.
- Graph-like relationships and semantic query explanation.
- Logic reasoner for symbolic conclusions and WHY explanations.

### Professional Terminal UI
- Uses `rich` + `colorama`.
- Menu dashboards, panels, status spinners.
- Clear module outputs and reasoning logs.

## Project Architecture

```text
AI-Powered-Chatbot-Assistant/
├── main.py
├── requirements.txt
├── README.md
├── data/
│   ├── faq.json
│   └── knowledge_graph.json
├── rules/
│   └── expert_rules.json
├── chatbot/
│   ├── __init__.py
│   ├── assistant.py
│   ├── intent_classifier.py
│   ├── memory.py
│   └── response_generator.py
├── expert_system/
│   ├── __init__.py
│   ├── models.py
│   ├── knowledge_base.py
│   ├── rule_engine.py
│   ├── inference_engine.py
│   └── session.py
├── search_algorithms/
│   ├── __init__.py
│   ├── graph_data.py
│   ├── search_engine.py
│   └── visualization.py
├── heuristics/
│   ├── __init__.py
│   └── recommender.py
├── knowledge_base/
│   ├── __init__.py
│   ├── knowledge_store.py
│   └── logic_reasoner.py
├── utils/
│   ├── __init__.py
│   ├── ui.py
│   ├── loader.py
│   └── logger.py
└── examples/
    └── demo_transcripts.md
```

## AI Concepts Demonstrated

- Rule-based conversational AI
- Heuristic decision-making
- State-space search (BFS, DFS)
- Knowledge representation
- Inference and expert systems (forward chaining)
- Logic-based reasoning and explanation generation
- Confidence scoring and intent classification

## Installation Guide

1. Clone or download this repository.
2. Open terminal in project root.
3. Create and activate virtual environment (recommended).
4. Install dependencies:

```bash
pip install -r requirements.txt
```

## How to Run

### Terminal UI

```bash
python main.py
```

Use the interactive dashboard to launch:
- Chatbot mode
- Expert system mode
- BFS/DFS search lab
- Heuristic recommendation engine
- Knowledge representation explorer

### Desktop GUI

```bash
python main.py --gui
```

The GUI includes dedicated tabs for:
- Chatbot conversation + feedback controls
- Expert-system diagnosis workflow
- BFS/DFS comparison with in-app graph visualization
- Heuristic recommendation results
- Knowledge graph querying
- Session conversation history

## BFS/DFS Demonstration

In `Search Algorithms` mode:
1. Enter start node (e.g., `A`)
2. Enter goal node (e.g., `J`)
3. View BFS and DFS comparison:
   - traversal order
   - explored nodes
   - path and path cost
   - execution time
   - shortest-path reasoning

Visual outputs are generated in `outputs/`, such as:
- `outputs/bfs_A_J.png`
- `outputs/dfs_A_J.png`

## Expert System Demonstration

In `Expert System` mode:
1. Answer yes/no diagnostic questions.
2. Facts are collected as knowledge.
3. Forward chaining infers conclusions.
4. System shows:
   - fired rules,
   - inference explanation,
   - final recommendations.

## Example Rule File

`rules/expert_rules.json` includes:
- question set,
- facts,
- production rules (`if -> then`),
- domain-specific recommendations.

You can create additional domains (medical, career, study planning) by adding new rule files with the same schema.

## Knowledge Representation Design

- Entities are stored as symbolic nodes in `data/knowledge_graph.json`.
- Semantic relationships are stored as triplets `(subject, relation, object)`.
- Query mode explains entity descriptions and linked relationships.

## Code Quality and Engineering Practices

- Object-oriented design across all modules.
- Reusable and decoupled components.
- Type hints and docstrings.
- Error handling for invalid input and missing files.
- Clear separation of concerns.

## Sample Outputs

See:
- `examples/demo_transcripts.md` for interaction samples.

## Future Improvements

- Add NLP pipeline with `nltk` or transformer intent model.
- Add persistent user memory (database-backed).
- Add A* search and weighted graphs.
- Add confidence calibration and evaluation metrics.
- Add unit/integration tests with `pytest`.
- Add REST API and web dashboard (FastAPI + frontend).

## Resume Value

This project demonstrates practical AI and software engineering skills:
- symbolic AI and reasoning,
- expert systems and rule engines,
- algorithmic search and visualization,
- modular architecture and clean code,
- explainable AI-style outputs for decision transparency.

