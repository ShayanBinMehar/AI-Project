# Demo Transcripts

## 1) Chatbot Conversation (Intent + Logic Reasoning)

**User:** `What is heuristic in AI?`  
**Assistant:** Explains the concept from FAQ knowledge and adds structured educational response.

**User:** `My laptop is slow and apps crash often. What should I do?`  
**Assistant:** Detects troubleshooting intent, suggests diagnostic strategy, and recommends opening Expert System module.

**User:** `Can you explain bfs and dfs?`  
**Assistant:** Detects search intent and returns algorithm comparison guidance.

## 2) Expert System (Forward Chaining)

**Facts captured from user answers:**  
`overheating = yes`, `system_slow = yes`, `app_crashes = yes`

**Rules fired:** `r2`, `r4`, `r5`  
**Conclusions inferred:** thermal throttling, resource/software conflict, performance-related instability  
**Recommendations:** cooling checks, software updates, workload reduction, conflict analysis.

## 3) Search Module Output

Input:
- Start: `A`
- Goal: `J`

Typical comparison:
- **BFS path:** `A -> B -> D -> G -> J` (shortest path guarantee in unweighted graph)
- **DFS path:** depends on branch ordering (may or may not be shortest)
- Metrics shown: traversal order, nodes explored, path cost, execution time.

Generated visuals:
- `outputs/bfs_A_J.png`
- `outputs/dfs_A_J.png`

## 4) Heuristic Recommendation Example

Study strategy candidates are scored with weighted features:
- difficulty fit
- time efficiency
- expected impact
- resource availability

The tool ranks candidates and explains the score components per option.

