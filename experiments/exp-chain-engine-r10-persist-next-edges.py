#!/usr/bin/env python3
"""Experiment: chain-engine R10+ — persist complete chain to disk with next_edges.

HYPOTHESIS (extends hyp:chain-engine-r10):
  Writing chain nodes to disk with 'next_edges' in frontmatter enables
  load_directory() to reconstruct 'next' Edge objects, so find_chains()
  returns chains on cold reload (not just in-memory).

CLAIM UNDER TEST:
  A complete chain persisted to disk with next_edges frontmatter fields
  is reconstructed by load_directory() and yields chains via find_chains().

METHOD:
  1. Build complete 8-node chain (idea → hyp → exp → verdict → mvp → outcome → bigger → app_purpose)
  2. Write each node to disk as a .md file with 'next_edges' in YAML frontmatter
  3. Call load_directory() with reconstruct_next_edges=True (default)
  4. Call find_chains() on the reloaded graph
  5. Verify: chains found = 1, chain length = 8

RESULTS:
  - Chains found on cold reload: 0 or 1
  - Chain length on cold reload: hops
  - All 8 node files written with next_edges
"""
import sys
import tempfile
import shutil
from pathlib import Path

_SRC = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(_SRC))

from graph_core.graph import Graph
from graph_core.node import Node
from chain_engine.chains import find_chains
from graph_core.loader import load_directory


# ---------------------------------------------------------------------------
# Chain definition (8 nodes matching capillary sequence)
# ---------------------------------------------------------------------------
CHAIN_NODES = [
    ("idea",   "idea:persist-test",          "idea"),
    ("hyp",    "hyp:persist-test",            "hypothesis"),
    ("exp",    "exp:persist-test",            "experiment"),
    ("verdict","verdict:persist-test",         "verdict"),
    ("mvp",    "mvp:persist-test",            "mvp"),
    ("outcome","outcome:persist-test",        "outcome"),
    ("bigger", "bigger-outcome:persist-test", "bigger_outcome"),
    ("app",    "app-purpose:persist-test",     "app_purpose"),
]

# next_edges: each node lists the next node in the chain
CHAIN_NEXT_EDGES = {
    "idea:persist-test":          ["hyp:persist-test"],
    "hyp:persist-test":            ["exp:persist-test"],
    "exp:persist-test":            ["verdict:persist-test"],
    "verdict:persist-test":         ["mvp:persist-test"],
    "mvp:persist-test":            ["outcome:persist-test"],
    "outcome:persist-test":        ["bigger-outcome:persist-test"],
    "bigger-outcome:persist-test": ["app-purpose:persist-test"],
    "app-purpose:persist-test":    [],
}

NODE_DIRS = {
    "idea": "idea", "hyp": "hypothesis", "exp": "experiment",
    "verdict": "verdict", "mvp": "mvp", "outcome": "outcome",
    "bigger": "bigger_outcome", "app": "app_purpose",
}

NODE_TITLES = {
    "idea:persist-test":          "Chain Persistence Test Idea",
    "hyp:persist-test":            "Chain Persistence Test Hypothesis",
    "exp:persist-test":            "Chain Persistence Test Experiment",
    "verdict:persist-test":         "Chain Persistence Test Verdict",
    "mvp:persist-test":            "Chain Persistence Test MVP",
    "outcome:persist-test":        "Chain Persistence Test Outcome",
    "bigger-outcome:persist-test": "Chain Persistence Test Bigger Outcome",
    "app-purpose:persist-test":     "Chain Persistence Test App Purpose",
}


def _slug(nid: str) -> str:
    return nid.replace(":", "-").replace("_", "-") + ".md"


def write_chain_to_disk(base_dir: Path) -> dict[str, Path]:
    """Write all 8 chain nodes to disk with next_edges frontmatter."""
    nodes_dir = base_dir / "nodes"
    paths = {}
    
    for prefix, nid, ntype in CHAIN_NODES:
        subdir = nodes_dir / NODE_DIRS[prefix]
        subdir.mkdir(parents=True, exist_ok=True)
        fpath = subdir / _slug(nid)
        
        next_targets = CHAIN_NEXT_EDGES.get(nid, [])
        # Parents are just the previous node (for spawns edges)
        prev_idx = CHAIN_NODES.index((prefix, nid, ntype)) - 1
        parents = [CHAIN_NODES[prev_idx][1]] if prev_idx >= 0 else []
        
        fm_lines = [
            "---",
            f'id: "{nid}"',
            f'title: "{NODE_TITLES[nid]}"',
            f'type: {ntype}',
            f'parents:',
        ]
        for p in parents:
            fm_lines.append(f'  - {p}')
        
        if next_targets:
            fm_lines.append("next_edges:")
            for t in next_targets:
                fm_lines.append(f"  - {t}")
        
        fm_lines.append("---")
        
        content = "\n".join(fm_lines) + f"\n\n{NODE_TITLES[nid]}\n"
        fpath.write_text(content)
        paths[nid] = fpath
    
    return paths


def run_tests(base_dir: Path) -> dict:
    """Run all verification tests."""
    results = {}
    
    # Write chain nodes to disk
    written = write_chain_to_disk(base_dir)
    results["files_written"] = len(written)
    
    # Check all files have next_edges
    all_have_next = True
    for nid, path in written.items():
        content = path.read_text()
        has_next = "next_edges" in content
        if nid != "app-purpose:persist-test" and not has_next:
            all_have_next = False
    results["all_have_next_edges"] = all_have_next
    
    # Load directory with reconstruct_next_edges=True (default)
    nodes_dir = base_dir / "nodes"
    graph, loaded = load_directory(nodes_dir, reconstruct_next_edges=True)
    
    # Count nodes loaded
    results["nodes_loaded"] = len(list(graph.node_ids))
    
    # Count next edges in graph
    next_edges_in_graph = [
        e for e in graph.edges if e.relation == "next"
    ]
    results["next_edges_reconstructed"] = len(next_edges_in_graph)
    
    # Run find_chains()
    chains = find_chains(graph)
    results["chains_found"] = len(chains)
    results["chain_lengths"] = [len(c) for c in chains]
    results["full_chains"] = [len(c) == 8 for c in chains]
    results["max_chain_length"] = max((len(c) for c in chains), default=0)
    
    # Verify chain completeness
    if chains:
        chain = chains[0]
        chain_ids = set(chain)
        expected_ids = {n[1] for n in CHAIN_NODES}
        results["chain_ids_match"] = chain_ids == expected_ids
        
        # Check all node types in correct order
        node_types = [(graph.get_node(nid) or Node(id=nid, type="?")).type for nid in chain]
        expected_types = [n[2] for n in CHAIN_NODES]
        results["type_sequence_correct"] = node_types == expected_types
    else:
        results["chain_ids_match"] = False
        results["type_sequence_correct"] = False
    
    # Test: cold reload produces same chains
    graph2, _ = load_directory(nodes_dir, reconstruct_next_edges=True)
    chains2 = find_chains(graph2)
    results["cold_reload_idempotent"] = len(chains) == len(chains2)
    
    return results


def main():
    print("=" * 70)
    print("EXPERIMENT: chain-engine R10+ — persist chain with next_edges")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        base_dir = Path(tmpdir)
        
        print("\n## Running persistence + cold-reload tests")
        results = run_tests(base_dir)
        
        print(f"\n  Files written: {results['files_written']}/8")
        print(f"  Nodes loaded: {results['nodes_loaded']}")
        print(f"  next_edges reconstructed: {results['next_edges_reconstructed']}")
        print(f"  Chains found: {results['chains_found']}")
        print(f"  Chain lengths: {results['chain_lengths']}")
        print(f"  Max chain length: {results['max_chain_length']}")
        print(f"  Cold-reload idempotent: {results['cold_reload_idempotent']}")
        
        # Determine pass/fail
        all_pass = (
            results["files_written"] == 8 and
            results["all_have_next_edges"] and
            results["next_edges_reconstructed"] == 7 and
            results["chains_found"] == 1 and
            results["max_chain_length"] == 8 and
            results.get("chain_ids_match", False) and
            results.get("type_sequence_correct", False) and
            results["cold_reload_idempotent"]
        )
        
        print(f"\n  All tests passed: {all_pass}")
        
        # Acceptance criteria
        print("\n## Acceptance Criteria")
        print(f"  [R10+] 8 node files written with next_edges: {'PASS' if results['files_written']==8 else 'FAIL'}")
        print(f"  [R10+] load_directory reconstructs next edges: {'PASS' if results['next_edges_reconstructed']==7 else 'FAIL'}")
        print(f"  [R10+] find_chains returns chain on cold reload: {'PASS' if results['chains_found']==1 else 'FAIL'}")
        print(f"  [R10+] Chain length = 8 hops: {'PASS' if results['max_chain_length']==8 else 'FAIL'}")
        print(f"  [R10+] Cold-reload idempotent: {'PASS' if results['cold_reload_idempotent'] else 'FAIL'}")
        
        verdict_str = "PROVED" if all_pass else "FAIL"
        print(f"\n## Verdict: {verdict_str}")
        
        print(f"\nMETRIC exp_passed={'all' if all_pass else 'partial'}")
        print(f"METRIC chains_found={results['chains_found']}")
        print(f"METRIC next_edges_reconstructed={results['next_edges_reconstructed']}")
        print(f"METRIC chain_length={results['max_chain_length']}")
        
        return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
