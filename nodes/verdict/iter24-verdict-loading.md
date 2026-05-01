---
confidence: 1.0
evidence_runs:
  - iter24-verdict-loading-test
id: "verdict:iter24-verdict-loading"
next_edges: []
parents:
  - hypothesis:iter24-verdict-loading
type: verdict
verdict: proved
---

## Evidence

**Before fix (broken):**
- All chains showed `completion_ratio=0.00`
- All chains showed `score=0.994` (no variation)
- `topological_queries.completion_ratio()` checked `getattr(node, "verdict", None)` but verdict wasn't a Node field

**After fix:**
- Node dataclass extended with 4 verdict-specific fields: `verdict`, `confidence`, `evidence_runs`, `contradicts`, `supports`
- `loader._node_from_frontmatter()` populates verdict fields from YAML frontmatter
- 910/928 verdict nodes now have `verdict=proved` (98% completion)
- 10 verdict nodes have verdict=None (hypothesis or task verdict files with no verdict field)
- Rankings now show meaningful variation:
  - cli-invocation: score=0.711, completion=0.00 (incomplete chain)
  - graph-core: score=0.706, completion=0.98
  - session-management: score=0.702, completion=0.00 (incomplete)
  - schema-registry: score=0.700, completion=0.98

**Tests:** 274 passed (was 272, +2 new verdict field tests)

## Changes

- `src/graph_core/node.py`: Added verdict_meta fields to Node dataclass
- `src/graph_core/loader.py`: Added verdict field extraction in `_node_from_frontmatter()`
- `src/graph_core/topological_queries.py`: Fixed verdict value access to use `node.verdict`
- `tests/graph_core/test_node.py`: Updated field count test + added verdict field tests
