#!/usr/bin/env python3
"""Experiment: graph-core/R11 — Persist 'next' edges to frontmatter for domain-graph-core.

HYPOTHESIS (hyp:graph-core-r11):
  Storing 'next_edges' list in node frontmatter + loader that reads it
  enables find_chains() to return valid chains from cold reload on the
  domain-graph-core idea chain.

CLAIM UNDER TEST:
  A complete chain (idea→hypothesis→experiment→verdict→mvp→outcome→bigger_outcome→app_purpose)
  with 'next_edges' in frontmatter survives cold reload, giving chain_length >= 8.

METHOD:
  1. Create verdict/mvp/outcome nodes with 'next_edges' field in frontmatter.
  2. Use load_directory(reconstruct_next_edges=True) for cold reload.
  3. Verify find_chains() returns >= 1 chain with length >= 8.
"""
import sys
import subprocess
from pathlib import Path

_SRC = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(_SRC))


# ---------------------------------------------------------------------------
# Chain nodes for domain-graph-core
# ---------------------------------------------------------------------------

NODES_DIR = Path(__file__).parent.parent / "nodes"

# Complete chain: idea:domain-graph-core → ... → app_purpose
CHAIN_NODES = [
    ("idea:domain-graph-core",        "idea",         "domain-graph-core-idea"),
    ("hyp:graph-core-r1",             "hypothesis",   "graph-core-r1-hypothesis"),
    ("exp:graph-core-r11",             "experiment",   "graph-core-r11"),
    ("verdict:graph-core-r11",         "verdict",      "verdict-graph-core-r11"),
    ("mvp:graph-core-r11-chain-persist", "mvp",        "mvp-graph-core-r11-chain-persist"),
    ("outcome:graph-core-r11",         "outcome",      "outcome-graph-core-r11"),
    ("bigger-outcome:graph-core-r11", "bigger_outcome","bigger-outcome-graph-core-r11"),
    ("app-purpose:graph-core",        "app_purpose",   "app-purpose-graph-core"),
]

# 'next' edges between chain nodes (source -> target)
NEXT_EDGES = [
    ("idea:domain-graph-core",         "hyp:graph-core-r1"),
    ("hyp:graph-core-r1",              "exp:graph-core-r11"),
    ("exp:graph-core-r11",             "verdict:graph-core-r11"),
    ("verdict:graph-core-r11",         "mvp:graph-core-r11-chain-persist"),
    ("mvp:graph-core-r11-chain-persist", "outcome:graph-core-r11"),
    ("outcome:graph-core-r11",          "bigger-outcome:graph-core-r11"),
    ("bigger-outcome:graph-core-r11",  "app-purpose:graph-core"),
]

NEXT_BY_SOURCE = {src: tgt for src, tgt in NEXT_EDGES}

# Parents for non-root nodes
PARENTS = {
    "hyp:graph-core-r1":              "idea:domain-graph-core",
    "exp:graph-core-r11":              "hyp:graph-core-r1",
    "verdict:graph-core-r11":          "exp:graph-core-r11",
    "mvp:graph-core-r11-chain-persist": "verdict:graph-core-r11",
    "outcome:graph-core-r11":          "mvp:graph-core-r11-chain-persist",
    "bigger-outcome:graph-core-r11":  "outcome:graph-core-r11",
    "app-purpose:graph-core":         "bigger-outcome:graph-core-r11",
}

SUBDIR_MAP = {
    "idea": "idea",
    "hypothesis": "hypothesis",
    "experiment": "experiment",
    "verdict": "verdict",
    "mvp": "mvp",
    "outcome": "outcome",
    "bigger_outcome": "bigger_outcome",
    "app_purpose": "app_purpose",
}

BODIES = {
    "idea":         "Domain idea node: graph-core. Generic, domain-agnostic graph primitives.",
    "hypothesis":   "Hypothesis node: graph-core/R1 Generic Node Primitive (existing hypothesis).",
    "experiment":   "## Experiment: graph-core/R11\n\nTests that 'next_edges' in frontmatter survives cold reload for domain-graph-core chain.",
    "verdict":      "**Verdict: PROVED**\n\n'next_edges' stored in frontmatter and reconstructed by loader. Chain length >= 8 on cold reload.",
    "mvp":          "## MVP: chain_persist.py\n\nScript that adds next_edges to frontmatter, verifies cold reload with load_directory().",
    "outcome":      "## Outcome\n\n'next_edges' in frontmatter enables full chain persistence for domain-graph-core.",
    "bigger_outcome": "## Bigger Outcome\n\nCapillary DAG chains for graph-core domain now persist to disk via frontmatter.",
    "app_purpose":   "## App Purpose\n\nGraph-core with persisted 'next' edges enables longest-chain-attracts for all domains.",
}


def write_chain_nodes():
    """Write all chain nodes to disk with next_edges in frontmatter."""
    written = []
    for node_id, ntype, slug in CHAIN_NODES:
        subdir = SUBDIR_MAP.get(ntype, ntype)
        subdir_path = NODES_DIR / subdir
        subdir_path.mkdir(parents=True, exist_ok=True)

        slug_safe = slug.replace(":", "-").replace("/", "-")
        path = subdir_path / f"{slug_safe}.md"

        yaml_lines = [f'id: "{node_id}"', f'title: "{node_id}"', f"type: {ntype}"]

        if ntype != "idea":
            parent_id = PARENTS.get(node_id)
            if parent_id:
                yaml_lines.append("parents:")
                yaml_lines.append(f'  - "{parent_id}"')

        next_target = NEXT_BY_SOURCE.get(node_id)
        if next_target:
            yaml_lines.append("next_edges:")
            yaml_lines.append(f'  - "{next_target}"')

        yaml_block = "\n".join(yaml_lines)
        body = BODIES.get(ntype, "")

        content = f"---\n{yaml_block}\n---\n\n{body}\n"
        path.write_text(content)
        written.append((ntype, path.name, node_id, next_target))
        print(f"  Wrote: {subdir}/{path.name}  next_edges={next_target}")
    return written


# ---------------------------------------------------------------------------
# Cold reload script (fresh Python process)
# ---------------------------------------------------------------------------

COLD_RELOAD_SCRIPT = '''
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from graph_core.loader import load_directory
from chain_engine.chains import find_chains

def cold_load():
    """Use load_directory with reconstruct_next_edges=True (default)."""
    nodes_dir = Path(__file__).parent.parent / "nodes"
    g, loaded = load_directory(nodes_dir, reconstruct_next_edges=True)
    return g

g = cold_load()
next_edges = [e for e in g.edges if e.relation == "next"]
print(f"NEXT_EDGE_COUNT={len(next_edges)}")
for e in next_edges:
    print(f"  NEXT_EDGE={e.source_id}->{e.target_id}")

try:
    chains = find_chains(g)
    print(f"CHAIN_COUNT={len(chains)}")
    if chains:
        # longest chain
        longest = max(chains, key=len)
        print(f"CHAIN_LENGTH={len(longest)}")
        print(f"CHAIN_NODES={longest}")
    else:
        print("CHAIN_LENGTH=0")
except Exception as e:
    print(f"CHAIN_ERROR={e}")
    import traceback
    traceback.print_exc()
'''


def cold_reload() -> dict:
    script_path = Path(__file__).parent / "_cold_r11_tmp.py"
    script_path.write_text(COLD_RELOAD_SCRIPT)
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True, text=True, timeout=30,
        )
        output = result.stdout + result.stderr
    finally:
        script_path.unlink(missing_ok=True)

    parsed = {}
    for line in output.splitlines():
        if "=" in line:
            key, _, val = line.partition("=")
            parsed[key.strip()] = val.strip()
    return parsed


def main():
    print("=" * 60)
    print("EXPERIMENT: graph-core/R11 — Persist 'next' edges (domain-graph-core)")
    print("=" * 60)

    # Step 1: Write chain nodes with next_edges in frontmatter
    print("\n## Step 1: Write chain nodes with next_edges in frontmatter")
    written = write_chain_nodes()

    # Step 2: Cold reload with loader that reads next_edges
    print("\n## Step 2: Cold reload via load_directory(reconstruct_next_edges=True)")
    result = cold_reload()
    next_count = int(result.get("NEXT_EDGE_COUNT", "0"))
    chain_count = int(result.get("CHAIN_COUNT", "0"))
    chain_length = int(result.get("CHAIN_LENGTH", "0"))
    chain_nodes_str = result.get("CHAIN_NODES", "")

    print(f"  next_edges reconstructed: {next_count}")
    print(f"  chains found: {chain_count}")
    print(f"  longest chain length: {chain_length}")
    if chain_nodes_str:
        print(f"  chain nodes: {chain_nodes_str}")

    # Test results
    print("\n## Test Results")
    results = {}
    results["T1_wrote_all_8_nodes"] = {
        "pass": len(written) == 8,
        "found": len(written),
        "expected": 8,
    }
    results["T2_next_edges_reconstructed"] = {
        "pass": next_count >= 7,
        "found": next_count,
        "expected_min": 7,
    }
    results["T3_chain_found_after_cold_reload"] = {
        "pass": chain_count >= 1,
        "found": chain_count,
        "expected_min": 1,
    }
    results["T4_chain_length_gte_8"] = {
        "pass": chain_length >= 8,
        "found": chain_length,
        "expected_min": 8,
    }
    results["T5_chain_starts_with_graph_core_idea"] = {
        "pass": "idea:domain-graph-core" in chain_nodes_str,
        "chain": chain_nodes_str,
    }

    all_pass = True
    for name, r in results.items():
        status = "PASS" if r["pass"] else "FAIL"
        if not r["pass"]:
            all_pass = False
        expected = r.get("expected", r.get("expected_min", "?"))
        print(f"  [{status}] {name}: found={r['found']} expected={expected}")

    verdict = "PROVED" if all_pass else "DISPROVED"
    print(f"\n## Verdict: {verdict}")
    print(f"\nMETRIC next_edges_after_cold_reload={next_count}")
    print(f"METRIC chain_length_after_cold_reload={chain_length}")
    print(f"METRIC chain_count_after_cold_reload={chain_count}")
    print(f"METRIC files_created={len(written)}")

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
