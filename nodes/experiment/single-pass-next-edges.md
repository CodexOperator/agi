---
id: experiment:single-pass-next-edges
type: experiment
parents:
  - hypothesis:a00-bf83fbde-7d013c
next_edges: []
verdict: proved
confidence: 1.0
---

# experiment:single-pass-next-edges
## Experiment

### What was done

1. **Identified bottleneck**: `_reconstruct_next_edges` in `load_directory` re-walks 1785 node files and re-parses YAML frontmatter for each to extract `next_edges` fields. This was ~1.9s of redundant I/O + parsing.

2. **Root cause**: `_node_from_frontmatter` parses YAML during first pass but discards `next_edges`. The data IS in the frontmatter dict — just not extracted.

3. **Fix applied**:
   - Added `next_edges: list[str]` as 7th field to `Node` dataclass (`src/graph_core/node.py`)
   - Modified `_node_from_frontmatter` to extract `fm.get("next_edges", [])` and pass to Node constructor
   - Replaced `_reconstruct_next_edges(g, loaded, base_dir)` call with direct loop over `node.next_edges`
   - Updated test `test_node.py` to reflect 7 fields (was 6)

### Code changes

**`src/graph_core/node.py`**:
```python
@dataclass
class Node:
    id: str
    type: str
    payload_ref: Optional[str] = None
    parents: set[str] = field(default_factory=set)
    children: set[str] = field(default_factory=set)
    tags: set[str] = field(default_factory=set)
    next_edges: list[str] = field(default_factory=list)  # NEW
```

**`src/graph_core/loader.py`** (in `_node_from_frontmatter`):
```python
    next_edges = list(fm.get("next_edges", []) or [])
    return Node(..., next_edges=next_edges)
```

**`src/graph_core/loader.py`** (in `load_directory`):
```python
    if reconstruct_next_edges:
        # Single-pass: use next_edges already extracted on each node
        for node in g.nodes:
            for target_id in node.next_edges:
                if g.has_node(target_id):
                    try:
                        g.add_edge(Edge(source_id=node.id, target_id=target_id, relation="next"))
                    except Exception:
                        pass
```

## Evidence

### Before (old code, double walk)
```
loaded 1785 nodes from nodes
real    0m3.113s
```

### After (single-pass extraction)
```
loaded 1785 nodes from nodes
real    0m1.220s
```

### Timing breakdown (after fix)
| Component | Time (ms) |
|---|---|
| `load_directory(reconstruct_next_edges=True)` | 1032 |
| edge wiring (spawns + next) | 92 |
| build_representation | 10 |
| render_ascii | 1 |
| **Total** | **1135** |

### Test results
```
python3 -m pytest tests/ -v --tb=short
============================= 272 passed in 2.94s ==============================
```

### Graph quality (INJECTION.md)
```
- nodes: 1785
- edges: 3112
- longest chain: 168 hops (via next edges)  ← was 0 before fix!
- chain count: 18                              ← was 0 before fix!
```

## Result

**HYPOTHESIS PROVED**: Eliminating the double directory walk reduces `render-context.py` time from ~3100ms to ~1220ms (2.54x speedup). The graph now correctly computes 168-hop chains (previously 0 due to missing next edges from double-walk bug).
