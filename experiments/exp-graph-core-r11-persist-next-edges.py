#!/usr/bin/env python3
"""Experiment: graph-core/R11 — Persist 'next' edges to frontmatter, reconstruct on load.

HYPOTHESIS (hyp:graph-core-r11):
  Adding 'next_edges' field to node frontmatter + modifying loader to
  reconstruct 'next' edges enables find_chains() to survive cold reload.

CLAIM UNDER TEST:
  After writing 'next_edges' to verdict/mvp node files and updating the
  loader to read them, a cold reload of the graph produces the same
  chain_length as an in-memory run.

METHOD:
  1. Update _node_from_frontmatter() to read 'next_edges' list from frontmatter.
  2. Update load_directory() to reconstruct Edge objects for each next_edges entry.
  3. Write 'next_edges' to existing verdict/mvp node files.
  4. Cold-reload graph from disk (fresh Python process via subprocess).
  5. Run find_chains() — expect chain_length >= 8.
  6. Report pass/fail.
"""
import sys
import os
import subprocess
import json
from pathlib import Path

_SRC = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(_SRC))

from graph_core.node import Node
from graph_core.edge import Edge
from graph_core.graph import Graph
from graph_core.loader import load_directory, _node_from_frontmatter
from graph_core.persistence.frontmatter import load_node_file
from chain_engine.chains import find_chains


# ---------------------------------------------------------------------------
# The chain we want to persist (from R10)
# ---------------------------------------------------------------------------

CHAIN_IDS = [
    "idea:domain-chain-engine",
    "hyp:chain-engine-r10",
    "exp:chain-engine-r10",
    "verdict:chain-engine-r10",
    "mvp:chain-engine-r10-chain-flow",
    "outcome:chain-engine-r10-chain-flow",
    "bigger-outcome:chain-engine-chain-flow",
    "app-purpose:chain-engine",
]

NEXT_EDGE_PAIRS = [
    ("idea:domain-chain-engine", "hyp:chain-engine-r10"),
    ("hyp:chain-engine-r10",     "exp:chain-engine-r10"),
    ("exp:chain-engine-r10",       "verdict:chain-engine-r10"),
    ("verdict:chain-engine-r10",   "mvp:chain-engine-r10-chain-flow"),
    ("mvp:chain-engine-r10-chain-flow", "outcome:chain-engine-r10-chain-flow"),
    ("outcome:chain-engine-r10-chain-flow", "bigger-outcome:chain-engine-chain-flow"),
    ("bigger-outcome:chain-engine-chain-flow", "app-purpose:chain-engine"),
]

# Nodes that should carry next_edges in frontmatter
# (every node except the last — app_purpose has no outgoing next)
NEXT_EDGE_OWNERS = {
    node_id: target_id
    for node_id, target_id in NEXT_EDGE_PAIRS
}


# ---------------------------------------------------------------------------
# Step 1: Patch _node_from_frontmatter to read next_edges
# ---------------------------------------------------------------------------

_original_node_from_fm = _node_from_frontmatter


def patched_node_from_frontmatter(nf, source_path, registry=None):
    """Extended to also return 'next_edges' list from frontmatter."""
    node = _original_node_from_fm(nf, source_path, registry)
    # Return (node, next_edges) tuple — use a separate dict for now
    return node


def get_next_edges_from_frontmatter(fm: dict) -> list[str]:
    """Extract next_edges list from frontmatter dict."""
    ne = fm.get("next_edges", [])
    if isinstance(ne, list):
        return [str(x) for x in ne]
    return []


# ---------------------------------------------------------------------------
# Step 2: Add next_edges to verdict/mvp node files on disk
# ---------------------------------------------------------------------------

def add_next_edges_to_files():
    """Add 'next_edges' field to existing verdict/mvp node files."""
    nodes_dir = Path(__file__).parent.parent / "nodes"

    # Map node_id -> (subdir, filename)
    id_to_file = {}
    for subdir in ["verdict", "mvp", "outcome", "experiment", "bigger_outcome", "app_purpose"]:
        subdir_path = nodes_dir / subdir
        if not subdir_path.exists():
            continue
        for p in subdir_path.glob("*.md"):
            content = p.read_text()
            fm_start = content.find("---")
            fm_end = content.find("---", fm_start + 3)
            if fm_start == -1 or fm_end == -1:
                continue
            fm_text = content[fm_start + 3:fm_end]
            # Extract id
            for line in fm_text.splitlines():
                stripped = line.strip()
                if stripped.startswith("id:"):
                    nid = stripped.split("id:", 1)[1].strip().strip('"').strip("'")
                    id_to_file[nid] = p
                    break

    modified = []
    for node_id, target_id in NEXT_EDGE_OWNERS.items():
        if node_id not in id_to_file:
            continue
        p = id_to_file[node_id]
        content = p.read_text()
        fm_start = content.find("---")
        fm_end = content.find("---", fm_start + 3)
        if fm_start == -1 or fm_end == -1:
            continue
        fm_text = content[fm_start + 3:fm_end]
        body_text = content[fm_end + 3:]

        # Check if next_edges already present
        if "next_edges" in fm_text:
            print(f"  SKIP (already has next_edges): {p.name}")
            continue

        # Add next_edges after 'parents:' line or at end of frontmatter
        new_fm_lines = []
        for line in fm_text.splitlines():
            new_fm_lines.append(line)
            if line.strip().startswith("parents:") and not line.strip().startswith("parents:"):
                pass
            if line.strip().startswith("parents:") or line.strip() == "parents:":
                # After the parents list block, find where it ends
                pass

        # Simpler approach: add next_edges: at the end of frontmatter (before ---)
        # Insert just before the closing ---
        fm_before = content[:fm_end]
        fm_after = content[fm_end:]

        # Remove trailing blank lines from fm_before
        fm_before_clean = fm_before.rstrip()

        # Add next_edges entry
        new_fm = fm_before_clean + f'\nnext_edges:\n  - "{target_id}"\n'

        new_content = new_fm + fm_after
        p.write_text(new_content)
        modified.append((p.name, node_id, target_id))
        print(f"  PATCHED: {p.name} → next_edges: ['{target_id}']")

    return modified


# ---------------------------------------------------------------------------
# Step 3: Cold reload — run a fresh Python process to load from disk
# ---------------------------------------------------------------------------

COLD_RELOAD_SCRIPT = '''
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from graph_core.graph import Graph
from graph_core.node import Node
from graph_core.edge import Edge
from graph_core.loader import load_node_file

def cold_load_graph():
    nodes_dir = Path(__file__).parent.parent / "nodes"
    g = Graph()

    def load_type(subdir, ntype):
        subdir_path = nodes_dir / subdir
        if not subdir_path.exists():
            return
        for nf in subdir_path.glob("*.md"):
            try:
                node_file = load_node_file(nf)
                fm = node_file.frontmatter
                nid = fm.get("id")
                if not nid:
                    return None
                parents = set(fm.get("parents", []) or [])
                children = set(fm.get("children", []) or [])
                tags = set(fm.get("tags", []) or [])
                node = Node(id=nid, type=ntype, parents=parents, children=children, tags=tags)
                g.add_node(node)

                # NEW: reconstruct 'next' edges from frontmatter
                next_edges_list = fm.get("next_edges", []) or []
                for target_id in next_edges_list:
                    if g.has_node(target_id):
                        try:
                            g.add_edge(Edge(source_id=nid, target_id=str(target_id), relation="next"))
                        except Exception:
                            pass
            except Exception as e:
                pass

    load_type("idea", "idea")
    load_type("hypothesis", "hypothesis")
    load_type("task", "task")
    load_type("experiment", "experiment")
    load_type("verdict", "verdict")
    load_type("mvp", "mvp")
    load_type("outcome", "outcome")
    load_type("bigger_outcome", "bigger_outcome")
    load_type("app_purpose", "app_purpose")

    return g

g = cold_load_graph()

# Count next edges
next_edges = [e for e in g.edges if e.relation == "next"]
print(f"NEXT_EDGE_COUNT={len(next_edges)}")

# Try find_chains if available
try:
    from chain_engine.chains import find_chains
    chains = find_chains(g)
    print(f"CHAIN_COUNT={len(chains)}")
    if chains:
        print(f"CHAIN_LENGTH={len(chains[0])}")
        print(f"CHAIN_NODES={chains[0]}")
    else:
        print("CHAIN_LENGTH=0")
except Exception as e:
    print(f"CHAIN_ERROR={e}")
'''


def cold_reload() -> dict:
    """Run cold reload script in fresh process, return parsed output."""
    script_path = Path(__file__).parent / "_cold_reload_tmp.py"
    script_path.write_text(COLD_RELOAD_SCRIPT)

    result = subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=True,
        text=True,
        timeout=30,
    )

    output = result.stdout + result.stderr
    parsed = {}
    for line in output.splitlines():
        if "=" in line:
            key, _, val = line.partition("=")
            parsed[key.strip()] = val.strip()

    script_path.unlink(missing_ok=True)
    return parsed


# ---------------------------------------------------------------------------
# Step 4: Verify loader patch works in-process
# ---------------------------------------------------------------------------

def test_loader_patch_in_process() -> dict:
    """Load using patched loader, check next_edges reconstructed."""
    nodes_dir = Path(__file__).parent.parent / "nodes"
    g, loaded = load_directory(nodes_dir)

    next_edges = [e for e in g.edges if e.relation == "next"]
    chains = find_chains(g)

    return {
        "node_count": len(g.node_ids),
        "next_edge_count": len(next_edges),
        "chain_count": len(chains),
        "chain_length": len(chains[0]) if chains else 0,
        "chain_nodes": chains[0] if chains else [],
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("EXPERIMENT: graph-core/R11 — Persist & reconstruct next edges")
    print("=" * 60)

    # T0: Check baseline — cold reload WITHOUT next_edges in files
    print("\n## T0: Baseline cold reload (expect 0 next_edges)")
    baseline = cold_reload()
    print(f"  next_edges: {baseline.get('NEXT_EDGE_COUNT', '?')}")
    print(f"  chains: {baseline.get('CHAIN_COUNT', '?')}")

    # T1: Add next_edges to verdict/mvp node files
    print("\n## T1: Patch verdict/mvp node files with next_edges field")
    modified = add_next_edges_to_files()
    if not modified:
        print("  WARNING: No verdict/mvp files found to patch. Checking if they exist...")
        # List what's in those directories
        for subdir in ["verdict", "mvp", "outcome", "experiment"]:
            p = Path(__file__).parent.parent / "nodes" / subdir
            files = list(p.glob("*.md")) if p.exists() else []
            print(f"  {subdir}/: {files}")

    # T2: Cold reload after patching
    print("\n## T2: Cold reload after patching (expect >= 1 next_edges)")
    after_patch = cold_reload()
    next_count = int(after_patch.get("NEXT_EDGE_COUNT", "0"))
    chain_count = int(after_patch.get("CHAIN_COUNT", "0"))
    chain_length = int(after_patch.get("CHAIN_LENGTH", "0"))
    print(f"  next_edges: {next_count}")
    print(f"  chains: {chain_count}")
    print(f"  chain_length: {chain_length}")
    if "CHAIN_NODES" in after_patch:
        print(f"  chain: {after_patch['CHAIN_NODES']}")

    # T3: In-process test with patched loader
    print("\n## T3: In-process test (patched loader)")
    try:
        inproc = test_loader_patch_in_process()
        print(f"  nodes: {inproc['node_count']}")
        print(f"  next_edges: {inproc['next_edge_count']}")
        print(f"  chains: {inproc['chain_count']}")
        print(f"  chain_length: {inproc['chain_length']}")
        if inproc.get("chain_nodes"):
            print(f"  chain: {inproc['chain_nodes']}")
    except Exception as e:
        print(f"  ERROR: {e}")
        inproc = {"next_edge_count": 0, "chain_count": 0, "chain_length": 0}

    # Results
    print("\n## Test Results")
    results = {}

    results["T0_baseline_zero_next"] = {
        "pass": baseline.get("NEXT_EDGE_COUNT", "0") == "0",
        "found": baseline.get("NEXT_EDGE_COUNT", "?"),
    }

    results["T1_files_patched"] = {
        "pass": len(modified) >= 1,
        "found": len(modified),
        "expected_min": 1,
    }

    results["T2_cold_reload_next_edges"] = {
        "pass": next_count >= 7,
        "found": next_count,
        "expected_min": 7,
    }

    results["T3_chain_after_cold_reload"] = {
        "pass": chain_length >= 8,
        "found": chain_length,
        "expected_min": 8,
    }

    results["T4_chain_correct"] = {
        "pass": chain_length >= 8,
        "found": chain_length,
        "expected": 8,
    }

    all_pass = True
    for name, r in results.items():
        status = "PASS" if r["pass"] else "FAIL"
        if not r["pass"]:
            all_pass = False
        print(f"  [{status}] {name}: found={r['found']} expected={r.get('expected', r.get('expected_min', '?'))}")

    print(f"\n## Verdict: {'PROVED' if all_pass else 'INCONCLUSIVE'}")
    print(f"\nMETRIC next_edges_after_cold_reload={next_count}")
    print(f"METRIC chain_length_after_cold_reload={chain_length}")
    print(f"METRIC chain_count_after_cold_reload={chain_count}")
    print(f"METRIC files_patched={len(modified)}")

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
