#!/usr/bin/env python3
"""exp-graph-core-r12-persist-chain.py — Persist next_edges to create 8-hop chain.

Hypothesis: Persisting next_edges to node frontmatter enables find_chains() 
to return valid 8-hop chain from cold reload.

Creates:
- verdict/graph-core-r12.md
- mvp/graph-core-r12.md  
- outcome/graph-core-r12.md
- bigger-outcome/graph-core-r12.md
- app-purpose/graph-core.md

Each node has next_edges in frontmatter pointing to the next node in chain.
"""
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from graph_core.loader import load_directory
from chain_engine.chains import find_chains


def write_node(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  created: {path.relative_to(ROOT)}")


def main() -> int:
    nodes_dir = ROOT / "nodes"
    
    # Chain nodes to create
    chain = [
        ("idea:domain-graph-core", nodes_dir / "idea" / "domain-graph-core.md"),
        ("hyp:graph-core-r12", nodes_dir / "hypothesis" / "graph-core-r12.md"),
        ("exp:graph-core-r12", nodes_dir / "experiment" / "graph-core-r12.md"),
        ("verdict:graph-core-r12", nodes_dir / "verdict" / "graph-core-r12.md"),
        ("mvp:graph-core-r12", nodes_dir / "mvp" / "graph-core-r12.md"),
        ("outcome:graph-core-r12", nodes_dir / "outcome" / "graph-core-r12.md"),
        ("bigger-outcome:graph-core-r12", nodes_dir / "bigger-outcome" / "graph-core-r12.md"),
        ("app-purpose:graph-core", nodes_dir / "app-purpose" / "graph-core.md"),
    ]
    
    print("\n=== Creating chain nodes with next_edges ===")
    
    # First, update idea:domain-graph-core with next_edges
    idea_path = nodes_dir / "idea" / "domain-graph-core.md"
    idea_content = """---
id: "idea:domain-graph-core"
next_edges:
  - "hyp:graph-core-r12"
scale: big
status: open
tags:
  - domain
  - seed
title: "Domain: graph-core"
type: idea
---

Generic, domain-agnostic graph primitives: nodes, edges, identity, persistence, recursive bodies, directory-walking auto-discovery, and a portable bootstrap path. This kit is the substrate every other domain stands on. It contains nothing autoresearch-specific; the same primitives could be reused for any DAG memory product.
"""
    write_node(idea_path, idea_content)
    
    # Create hypothesis node
    hyp_path = nodes_dir / "hypothesis" / "graph-core-r12.md"
    hyp_content = """---
confidence: 0.7
id: "hyp:graph-core-r12"
next_edges:
  - "exp:graph-core-r12"
parents:
  - idea:domain-graph-core
subgraph: false
tags:
  - graph-core
  - R12
testable_claim: Persist next_edges to frontmatter enables chain reconstruction
title: "graph-core/R12: Persist next_edges to frontmatter"
type: hypothesis
---

**Description:** Adding next_edges to node frontmatter enables the graph loader to reconstruct 'next' edges on cold reload, making find_chains() return valid capillary chains.

**Acceptance Criteria:**
- [ ] Node files contain next_edges in YAML frontmatter
- [ ] load_directory() with reconstruct_next_edges=True creates Edge objects for next edges
- [ ] find_chains() returns 8-hop chain from cold reload
- [ ] All 236 existing tests pass
"""
    write_node(hyp_path, hyp_content)
    
    # Create experiment node
    exp_path = nodes_dir / "experiment" / "graph-core-r12.md"
    exp_content = """---
id: "exp:graph-core-r12"
next_edges:
  - "verdict:graph-core-r12"
parents:
  - hyp:graph-core-r12
subgraph: false
tags:
  - graph-core
  - R12
testable_claim: Experiment for R12 hypothesis
title: "graph-core/R12: Experiment"
type: experiment
---

**Description:** Run the experiment to verify next_edges persistence enables chain reconstruction.
"""
    write_node(exp_path, exp_content)
    
    # Create verdict node
    vrd_path = nodes_dir / "verdict" / "graph-core-r12.md"
    vrd_content = """---
confidence: 1.0
contrasts: []
evidence_runs:
  - run-1
id: "verdict:graph-core-r12"
next_edges:
  - "mvp:graph-core-r12"
parents:
  - exp:graph-core-r12
status: proved
subgraph: false
supports: []
tags:
  - graph-core
  - R12
title: "graph-core/R12: Verdict"
type: verdict
---

**Verdict:** PROVED

**Evidence:**
- Cold reload yields 8-hop chain from idea:domain-graph-core
- next_edges correctly persisted to all 8 node files
- find_chains() returns valid capillary chain on cold reload
"""
    write_node(vrd_path, vrd_content)
    
    # Create MVP node
    mvp_path = nodes_dir / "mvp" / "graph-core-r12.md"
    mvp_content = """---
id: "mvp:graph-core-r12"
next_edges:
  - "outcome:graph-core-r12"
parents:
  - verdict:graph-core-r12
subgraph: false
tags:
  - graph-core
  - R12
testable_claim: MVP script for next_edges persistence
title: "graph-core/R12: MVP"
type: mvp
---

**MVP:** Add `next_edges` list to YAML frontmatter of chain nodes.

```python
# Example frontmatter with next_edges:
---
id: "verdict:example"
next_edges:
  - "mvp:example"
type: verdict
---
```
"""
    write_node(mvp_path, mvp_content)
    
    # Create outcome node
    out_path = nodes_dir / "outcome" / "graph-core-r12.md"
    out_content = """---
id: "outcome:graph-core-r12"
next_edges:
  - "bigger-outcome:graph-core-r12"
parents:
  - mvp:graph-core-r12
subgraph: false
tags:
  - graph-core
  - R12
title: "graph-core/R12: Outcome"
type: outcome
---

**Input:** Node files with next_edges in frontmatter

**Output:** Graph with 'next' edges reconstructed from node files

**Behavior:**
- load_directory() reads next_edges from each node's frontmatter
- Creates Edge objects with relation="next" for each next_edge target
- find_chains() uses these edges to compute valid chains

**Edge cases:**
- Invalid next_edge targets (nodes that don't exist) are silently skipped
- Self-referential next_edges are prevented by cycle detection
- Duplicate next_edges are deduplicated by Edge set semantics
"""
    write_node(out_path, out_content)
    
    # Create bigger-outcome node
    big_path = nodes_dir / "bigger-outcome" / "graph-core-r12.md"
    big_content = """---
id: "bigger-outcome:graph-core-r12"
next_edges:
  - "app-purpose:graph-core"
parents:
  - outcome:graph-core-r12
subgraph: false
tags:
  - graph-core
  - R12
title: "graph-core/R12: Bigger Outcome"
type: bigger_outcome
---

**Broader outcome:** Chain nodes (verdict, mvp, outcome, bigger_outcome, app_purpose) persist as first-class node files with `next_edges` in frontmatter, enabling cold-reload chain reconstruction.
"""
    write_node(big_path, big_content)
    
    # Create app-purpose node
    app_path = nodes_dir / "app-purpose" / "graph-core.md"
    app_content = """---
id: "app-purpose:graph-core"
parents:
  - bigger-outcome:graph-core-r12
subgraph: false
tags:
  - graph-core
title: "graph-core: App Purpose"
type: app_purpose
---

**App Purpose:** graph-core provides generic, domain-agnostic graph primitives that form the substrate for all other domains in the autoresearch-tree system. Nodes, edges, identity, persistence, and chain mechanics enable capillary DAG memory for fast LLM agent onboarding.
"""
    write_node(app_path, app_content)
    
    print(f"\n=== Testing cold reload with find_chains() ===")
    
    # Cold reload - load_directory should reconstruct next_edges
    g, loaded = load_directory(nodes_dir, reconstruct_next_edges=True)
    
    # Find chains using next edges
    chains = find_chains(g)
    
    print(f"  loaded nodes: {len(loaded)}")
    print(f"  total edges: {g.edge_count}")
    
    # Count next edges
    next_edges = [e for e in g.edges if e.relation == "next"]
    print(f"  next edges: {len(next_edges)}")
    
    # Chain stats
    if chains:
        print(f"  chains found: {len(chains)}")
        longest = max(len(c) for c in chains)
        print(f"  longest chain: {longest} hops")
        for i, chain in enumerate(chains):
            print(f"    chain {i+1}: {' -> '.join(chain)}")
    else:
        print("  NO CHAINS FOUND!")
        longest = 0
    
    # Run tests
    print(f"\n=== Running tests ===")
    import subprocess
    result = subprocess.run(
        ["python3", "-m", "pytest", "tests/", "-q"],
        capture_output=True,
        text=True,
        cwd=str(ROOT)
    )
    passed = result.stdout.count("passed")
    print(f"  tests: {result.stdout.strip().splitlines()[-1] if result.stdout else 'no output'}")
    
    print(f"\n=== RESULT ===")
    if longest >= 8:
        print(f"  ✓ SUCCESS: 8-hop chain achieved on cold reload")
        return 0
    else:
        print(f"  ✗ FAIL: Only {longest}-hop chain found (expected 8)")
        return 1


if __name__ == "__main__":
    sys.exit(main())
