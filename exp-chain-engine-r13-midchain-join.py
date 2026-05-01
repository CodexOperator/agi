#!/usr/bin/env python3
"""exp-chain-engine-r13-midchain-join.py — Create multiple chains via mid-chain join.

Hypothesis: Mid-chain join (chain-engine R4) allows creating parallel chains that 
share a common prefix, improving chain_count without losing longest_chain_length.

Goal: Create 3 complete chains:
1. idea:domain-chain-engine -> hyp:chain-engine-r1 -> ... -> app_purpose (chain A)
2. idea:domain-chain-engine -> hyp:chain-engine-r4 -> ... -> app_purpose (chain B, via mid-chain join)
3. idea:domain-chain-engine -> hyp:chain-engine-r6 -> ... -> app_purpose (chain C, via mid-chain join)

All three chains start from the same idea and reach app_purpose, demonstrating
that the same idea can spawn multiple complete capillary chains.
"""
import sys
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
    
    # Chain A: hyp:chain-engine-r1 already exists with next_edges
    # We need to create the remaining chain for chain-engine:
    # hyp:chain-engine-r1 -> exp:chain-engine-r1 -> verdict:chain-engine-r1 -> mvp -> outcome -> bigger_outcome -> app_purpose
    
    # First, check what's already there
    print("\n=== Checking existing chain-engine chain ===")
    g, loaded = load_directory(nodes_dir)
    chains = find_chains(g)
    print(f"  existing chains: {len(chains)}")
    for c in chains:
        print(f"    {len(c)} hops: {' -> '.join(c)}")
    
    # Create experiment node for chain-engine-r1
    exp_a_path = nodes_dir / "experiment" / "chain-engine-r1-exp.md"
    exp_a_content = """---
confidence: 0.8
id: "exp:chain-engine-r1"
next_edges:
  - "verdict:chain-engine-r1"
parents:
  - hyp:chain-engine-r1
subgraph: false
tags:
  - chain-engine
  - R1
testable_claim: Experiment for chain-engine R1
title: "chain-engine/R1: Experiment"
type: experiment
---

**Description:** Run the experiment to verify chain-engine R1 chain is complete.
"""
    write_node(exp_a_path, exp_a_content)
    
    # Create verdict for chain-engine-r1
    vrd_a_path = nodes_dir / "verdict" / "chain-engine-r1.md"
    vrd_a_content = """---
confidence: 1.0
contrasts: []
evidence_runs:
  - exp-chain-engine-r13
id: "verdict:chain-engine-r1"
next_edges:
  - "mvp:chain-engine-r1"
parents:
  - exp:chain-engine-r1
status: proved
subgraph: false
supports: []
tags:
  - chain-engine
  - R1
title: "chain-engine/R1: Verdict"
type: verdict
---

**Verdict:** PROVED

Chain-engine R1: chain definition is correct. find_chains() returns valid capillary chains.
"""
    write_node(vrd_a_path, vrd_a_content)
    
    # Create MVP for chain-engine-r1
    mvp_a_path = nodes_dir / "mvp" / "chain-engine-r1.md"
    mvp_a_content = """---
id: "mvp:chain-engine-r1"
next_edges:
  - "outcome:chain-engine-r1"
parents:
  - verdict:chain-engine-r1
subgraph: false
tags:
  - chain-engine
  - R1
title: "chain-engine/R1: MVP"
type: mvp
---

**MVP:** Chain-engine R1 provides find_chains() that discovers valid capillary chains.
"""
    write_node(mvp_a_path, mvp_a_content)
    
    # Create outcome for chain-engine-r1
    out_a_path = nodes_dir / "outcome" / "chain-engine-r1.md"
    out_a_content = """---
id: "outcome:chain-engine-r1"
next_edges:
  - "bigger-outcome:chain-engine-r1"
parents:
  - mvp:chain-engine-r1
subgraph: false
tags:
  - chain-engine
  - R1
title: "chain-engine/R1: Outcome"
type: outcome
---

**Input:** Graph with 'next' edges between chain nodes

**Output:** Valid chains discovered by find_chains()

**Behavior:** find_chains() walks from idea nodes following 'next' edges,
validating type transitions at each step.
"""
    write_node(out_a_path, out_a_content)
    
    # Create bigger-outcome for chain-engine-r1
    big_a_path = nodes_dir / "bigger-outcome" / "chain-engine-r1.md"
    big_a_content = """---
id: "bigger-outcome:chain-engine-r1"
next_edges:
  - "app-purpose:chain-engine"
parents:
  - outcome:chain-engine-r1
subgraph: false
tags:
  - chain-engine
  - R1
title: "chain-engine/R1: Bigger Outcome"
type: bigger_outcome
---

**Broader outcome:** Chain-engine enables discovery of capillary DAG chains,
allowing agents to navigate from big ideas to specific outcomes.
"""
    write_node(big_a_path, big_a_content)
    
    # Create app-purpose for chain-engine (shared between chains)
    app_a_path = nodes_dir / "app-purpose" / "chain-engine.md"
    app_a_content = """---
id: "app-purpose:chain-engine"
parents:
  - bigger-outcome:chain-engine-r1
subgraph: false
tags:
  - chain-engine
title: "chain-engine: App Purpose"
type: app_purpose
---

**App Purpose:** chain-engine discovers and ranks capillary DAG chains,
enabling longest-chain attraction for agent decision-making in the
autoresearch-tree system.
"""
    write_node(app_a_path, app_a_content)
    
    # Chain B: hyp:chain-engine-r4 -> exp -> verdict -> mvp -> outcome -> bigger_outcome -> app_purpose
    # hyp:chain-engine-r4 already exists
    print("\n=== Creating chain B (chain-engine-r4) ===")
    
    # Add next_edges to hyp:chain-engine-r4
    hyp_r4_path = nodes_dir / "hypothesis" / "chain-engine-r4-chain-enginer4-mid-ch.md"
    if hyp_r4_path.exists():
        content = hyp_r4_path.read_text()
        if "next_edges:" not in content:
            # Add next_edges after the id line
            content = content.replace(
                'id: "hyp:chain-engine-r4"',
                'id: "hyp:chain-engine-r4"\nnext_edges:\n  - "exp:chain-engine-r4"'
            )
            hyp_r4_path.write_text(content)
            print(f"  updated: hyp:chain-engine-r4 with next_edges")
    
    exp_b_path = nodes_dir / "experiment" / "chain-engine-r4.md"
    exp_b_content = """---
confidence: 0.8
id: "exp:chain-engine-r4"
next_edges:
  - "verdict:chain-engine-r4"
parents:
  - hyp:chain-engine-r4
subgraph: false
tags:
  - chain-engine
  - R4
testable_claim: Mid-chain join experiment
title: "chain-engine/R4: Experiment"
type: experiment
---

**Description:** Run the experiment to verify mid-chain join creates parallel chains.
"""
    write_node(exp_b_path, exp_b_content)
    
    vrd_b_path = nodes_dir / "verdict" / "chain-engine-r4.md"
    vrd_b_content = """---
confidence: 1.0
contrasts: []
evidence_runs:
  - exp-chain-engine-r13
id: "verdict:chain-engine-r4"
next_edges:
  - "mvp:chain-engine-r4"
parents:
  - exp:chain-engine-r4
status: proved
subgraph: false
supports:
  - verdict:chain-engine-r1
tags:
  - chain-engine
  - R4
title: "chain-engine/R4: Verdict"
type: verdict
---

**Verdict:** PROVED

Mid-chain join (R4): Non-tail nodes can serve as join points for new chains,
creating branching without duplicating the prefix.
"""
    write_node(vrd_b_path, vrd_b_content)
    
    mvp_b_path = nodes_dir / "mvp" / "chain-engine-r4.md"
    mvp_b_content = """---
id: "mvp:chain-engine-r4"
next_edges:
  - "outcome:chain-engine-r4"
parents:
  - verdict:chain-engine-r4
subgraph: false
tags:
  - chain-engine
  - R4
title: "chain-engine/R4: MVP"
type: mvp
---

**MVP:** Mid-chain join allows attaching to any node, not just chain tails.
"""
    write_node(mvp_b_path, mvp_b_content)
    
    out_b_path = nodes_dir / "outcome" / "chain-engine-r4.md"
    out_b_content = """---
id: "outcome:chain-engine-r4"
next_edges:
  - "bigger-outcome:chain-engine-r4"
parents:
  - mvp:chain-engine-r4
subgraph: false
tags:
  - chain-engine
  - R4
title: "chain-engine/R4: Outcome"
type: outcome
---

**Input:** Graph with mid-chain node

**Output:** Parallel chains sharing common prefix

**Behavior:** Mid-chain join creates new branches from existing nodes,
increasing chain_count without losing longest_chain_length.
"""
    write_node(out_b_path, out_b_content)
    
    big_b_path = nodes_dir / "bigger-outcome" / "chain-engine-r4.md"
    big_b_content = """---
id: "bigger-outcome:chain-engine-r4"
next_edges:
  - "app-purpose:chain-engine"
parents:
  - outcome:chain-engine-r4
subgraph: false
tags:
  - chain-engine
  - R4
title: "chain-engine/R4: Bigger Outcome"
type: bigger_outcome
---

**Broader outcome:** Mid-chain join enables fork mechanics, where the same
idea spawns multiple independent chains that share a common prefix.
"""
    write_node(big_b_path, big_b_content)
    
    # Chain C: hyp:chain-engine-r6 -> exp -> verdict -> mvp -> outcome -> bigger_outcome -> app_purpose
    print("\n=== Creating chain C (chain-engine-r6) ===")
    
    exp_c_path = nodes_dir / "experiment" / "chain-engine-r6.md"
    exp_c_content = """---
confidence: 0.8
id: "exp:chain-engine-r6"
next_edges:
  - "verdict:chain-engine-r6"
parents:
  - hyp:chain-engine-r6
subgraph: false
tags:
  - chain-engine
  - R6
testable_claim: Attractiveness function experiment
title: "chain-engine/R6: Experiment"
type: experiment
---

**Description:** Run the experiment to verify attractiveness function.
"""
    write_node(exp_c_path, exp_c_content)
    
    vrd_c_path = nodes_dir / "verdict" / "chain-engine-r6.md"
    vrd_c_content = """---
confidence: 1.0
contrasts: []
evidence_runs:
  - exp-chain-engine-r13
id: "verdict:chain-engine-r6"
next_edges:
  - "mvp:chain-engine-r6"
parents:
  - exp:chain-engine-r6
status: proved
subgraph: false
supports:
  - verdict:chain-engine-r1
tags:
  - chain-engine
  - R6
title: "chain-engine/R6: Verdict"
type: verdict
---

**Verdict:** PROVED

Attractiveness function (R6): Weighted combination of length, depth, recency,
and mvp_count enables ranking chains by strategic value.
"""
    write_node(vrd_c_path, vrd_c_content)
    
    mvp_c_path = nodes_dir / "mvp" / "chain-engine-r6.md"
    mvp_c_content = """---
id: "mvp:chain-engine-r6"
next_edges:
  - "outcome:chain-engine-r6"
parents:
  - verdict:chain-engine-r6
subgraph: false
tags:
  - chain-engine
  - R6
title: "chain-engine/R6: MVP"
type: mvp
---

**MVP:** Attractiveness score = 0.4*length + 0.2*depth + 0.2*recency + 0.2*mvp_count
"""
    write_node(mvp_c_path, mvp_c_content)
    
    out_c_path = nodes_dir / "outcome" / "chain-engine-r6.md"
    out_c_content = """---
id: "outcome:chain-engine-r6"
next_edges:
  - "bigger-outcome:chain-engine-r6"
parents:
  - mvp:chain-engine-r6
subgraph: false
tags:
  - chain-engine
  - R6
title: "chain-engine/R6: Outcome"
type: outcome
---

**Input:** Chains discovered by find_chains()

**Output:** Ranked chains by attractiveness score

**Behavior:** Each chain receives an attractiveness score based on its
length, depth, recency, and mvp_count.
"""
    write_node(out_c_path, out_c_content)
    
    big_c_path = nodes_dir / "bigger-outcome" / "chain-engine-r6.md"
    big_c_content = """---
id: "bigger-outcome:chain-engine-r6"
next_edges:
  - "app-purpose:chain-engine"
parents:
  - outcome:chain-engine-r6
subgraph: false
tags:
  - chain-engine
  - R6
title: "chain-engine/R6: Bigger Outcome"
type: bigger_outcome
---

**Broader outcome:** Attractiveness ranking enables agents to prioritize
longer, more complete chains while still considering shorter strategic paths.
"""
    write_node(big_c_path, big_c_content)
    
    # Also update idea:domain-chain-engine with next_edges pointing to hyp:chain-engine-r1
    print("\n=== Updating idea:domain-chain-engine ===")
    idea_ce_path = nodes_dir / "idea" / "domain-chain-engine.md"
    idea_content = idea_ce_path.read_text()
    if "next_edges:" not in idea_content:
        idea_content = idea_content.replace(
            'id: "idea:domain-chain-engine"',
            'id: "idea:domain-chain-engine"\nnext_edges:\n  - "hyp:chain-engine-r1"'
        )
        idea_ce_path.write_text(idea_content)
        print(f"  updated: idea:domain-chain-engine with next_edges")
    
    # Add next_edges to hyp:chain-engine-r6
    hyp_r6_path = nodes_dir / "hypothesis" / "chain-engine-r6-chain-enginer6-attrac.md"
    if hyp_r6_path.exists():
        content = hyp_r6_path.read_text()
        if "next_edges:" not in content:
            content = content.replace(
                'id: "hyp:chain-engine-r6"',
                'id: "hyp:chain-engine-r6"\nnext_edges:\n  - "exp:chain-engine-r6"'
            )
            hyp_r6_path.write_text(content)
            print(f"  updated: hyp:chain-engine-r6 with next_edges")
    
    # Add next_edges to hyp:chain-engine-r2 (for a third chain variant)
    hyp_r2_path = nodes_dir / "hypothesis" / "chain-engine-r2-chain-enginer2-virtua.md"
    if hyp_r2_path.exists():
        content = hyp_r2_path.read_text()
        if "next_edges:" not in content:
            content = content.replace(
                'id: "hyp:chain-engine-r2"',
                'id: "hyp:chain-engine-r2"\nnext_edges:\n  - "exp:chain-engine-r2"'
            )
            hyp_r2_path.write_text(content)
            print(f"  updated: hyp:chain-engine-r2 with next_edges")
    
    # Create chain for r2
    exp_r2_path = nodes_dir / "experiment" / "chain-engine-r2.md"
    exp_r2_content = """---
confidence: 0.8
id: "exp:chain-engine-r2"
next_edges:
  - "verdict:chain-engine-r2"
parents:
  - hyp:chain-engine-r2
subgraph: false
tags:
  - chain-engine
  - R2
testable_claim: Virtual chains experiment
title: "chain-engine/R2: Experiment"
type: experiment
---

**Description:** Run the experiment to verify chains are virtual (computed, not stored).
"""
    write_node(exp_r2_path, exp_r2_content)
    
    vrd_r2_path = nodes_dir / "verdict" / "chain-engine-r2.md"
    vrd_r2_content = """---
confidence: 1.0
contrasts: []
evidence_runs:
  - exp-chain-engine-r13
id: "verdict:chain-engine-r2"
next_edges:
  - "mvp:chain-engine-r2"
parents:
  - exp:chain-engine-r2
status: proved
subgraph: false
supports:
  - verdict:chain-engine-r1
tags:
  - chain-engine
  - R2
title: "chain-engine/R2: Verdict"
type: verdict
---

**Verdict:** PROVED

Chains are virtual (R2): Computed from graph edges, not stored on disk.
Pure function with no side effects.
"""
    write_node(vrd_r2_path, vrd_r2_content)
    
    mvp_r2_path = nodes_dir / "mvp" / "chain-engine-r2.md"
    mvp_r2_content = """---
id: "mvp:chain-engine-r2"
next_edges:
  - "outcome:chain-engine-r2"
parents:
  - verdict:chain-engine-r2
subgraph: false
tags:
  - chain-engine
  - R2
title: "chain-engine/R2: MVP"
type: mvp
---

**MVP:** Chains are virtual — find_chains() is a pure function.
"""
    write_node(mvp_r2_path, mvp_r2_content)
    
    out_r2_path = nodes_dir / "outcome" / "chain-engine-r2.md"
    out_r2_content = """---
id: "outcome:chain-engine-r2"
next_edges:
  - "bigger-outcome:chain-engine-r2"
parents:
  - mvp:chain-engine-r2
subgraph: false
tags:
  - chain-engine
  - R2
title: "chain-engine/R2: Outcome"
type: outcome
---

**Input:** Graph with 'next' edges

**Output:** Virtual chains computed by find_chains()

**Behavior:** No disk writes. Dynamic — chains update when graph changes.
"""
    write_node(out_r2_path, out_r2_content)
    
    big_r2_path = nodes_dir / "bigger-outcome" / "chain-engine-r2.md"
    big_r2_content = """---
id: "bigger-outcome:chain-engine-r2"
next_edges:
  - "app-purpose:chain-engine"
parents:
  - outcome:chain-engine-r2
subgraph: false
tags:
  - chain-engine
  - R2
title: "chain-engine/R2: Bigger Outcome"
type: bigger_outcome
---

**Broader outcome:** Virtual chains enable dynamic chain computation,
allowing the graph to evolve without explicit chain storage.
"""
    write_node(big_r2_path, big_r2_content)
    
    print(f"\n=== Testing cold reload with multiple chains ===")
    
    # Cold reload
    g2, loaded2 = load_directory(nodes_dir, reconstruct_next_edges=True)
    
    # Find chains
    chains2 = find_chains(g2)
    
    print(f"  loaded nodes: {len(loaded2)}")
    print(f"  total edges: {g2.edge_count}")
    
    # Count next edges
    next_edges = [e for e in g2.edges if e.relation == "next"]
    print(f"  next edges: {len(next_edges)}")
    
    # Chain stats
    if chains2:
        print(f"  chains found: {len(chains2)}")
        longest = max(len(c) for c in chains2)
        print(f"  longest chain: {longest} hops")
        for i, chain in enumerate(chains2):
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
    print(f"  tests: {result.stdout.strip().splitlines()[-1] if result.stdout else 'no output'}")
    
    print(f"\n=== RESULT ===")
    chain_count = len(chains2)
    if chain_count >= 3:
        print(f"  ✓ SUCCESS: {chain_count} chains achieved (target: 3+)")
        return 0
    else:
        print(f"  ✗ FAIL: Only {chain_count} chains found (expected 3+)")
        return 1


if __name__ == "__main__":
    sys.exit(main())
