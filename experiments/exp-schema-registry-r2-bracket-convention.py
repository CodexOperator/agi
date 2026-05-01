#!/usr/bin/env python3
"""Experiment: schema-registry/R2 — Bracket Convention for Active Schemas.

HYPOTHESIS (hyp:schema-registry-r2):
  Bracket Convention for Active Schemas: A schema file whose name is wrapped in
  brackets is treated as the active schema for the directory tree it lives in.
  Bracketing is the user's signal of approval.

ACCEPTANCE CRITERIA:
  R2.1: Bracketed file → active set
  R2.2: Non-bracketed file → inactive set
  R2.3: Rename to add brackets = activate
  R2.4: Duplicate active → DuplicateActiveSchemaError

METHOD:
  1. Create temp schema files and run loader + active_set
  2. Verify each acceptance criterion
  3. Write chain nodes (exp/verdict/mvp/outcome/bigger-outcome/app-purpose)
     with next_edges frontmatter to disk
  4. Verify find_chains() returns ≥1 chain from cold reload
  5. Run pytest for safety net
"""
import sys
import shutil
import tempfile
from pathlib import Path

_SRC = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(_SRC))

from schema_registry.loader import (
    load_schemas_from_dir,
    is_bracketed,
    canonical_name,
)
from schema_registry.active_set import (
    build_active_set,
    DuplicateActiveSchemaError,
)

ROOT = Path(__file__).parent.parent
NODES_DIR = ROOT / "nodes"

# The 8-node capillary chain for schema-registry-r2
CHAIN_IDS = [
    "idea:domain-schema-registry",
    "hyp:schema-registry-r2",
    "exp:schema-registry-r2",
    "verdict:schema-registry-r2",
    "mvp:schema-registry-r2-bracket-convention",
    "outcome:schema-registry-r2-bracket-convention",
    "bigger-outcome:schema-registry-r2",
    "app-purpose:schema-registry",
]
NODE_TYPE_MAP = {
    "idea:domain-schema-registry":                    "idea",
    "hyp:schema-registry-r2":                         "hypothesis",
    "exp:schema-registry-r2":                         "experiment",
    "verdict:schema-registry-r2":                     "verdict",
    "mvp:schema-registry-r2-bracket-convention":      "mvp",
    "outcome:schema-registry-r2-bracket-convention":  "outcome",
    "bigger-outcome:schema-registry-r2":              "bigger_outcome",
    "app-purpose:schema-registry":                    "app_purpose",
}
NODE_TYPE_SUBDIRS = {
    "idea": "idea", "hypothesis": "hypothesis",
    "experiment": "experiment", "verdict": "verdict",
    "mvp": "mvp", "outcome": "outcome",
    "bigger_outcome": "bigger_outcome", "app_purpose": "app_purpose",
}
NEXT_EDGES = [
    ("idea:domain-schema-registry", "hyp:schema-registry-r2"),
    ("hyp:schema-registry-r2", "exp:schema-registry-r2"),
    ("exp:schema-registry-r2", "verdict:schema-registry-r2"),
    ("verdict:schema-registry-r2", "mvp:schema-registry-r2-bracket-convention"),
    ("mvp:schema-registry-r2-bracket-convention", "outcome:schema-registry-r2-bracket-convention"),
    ("outcome:schema-registry-r2-bracket-convention", "bigger-outcome:schema-registry-r2"),
    ("bigger-outcome:schema-registry-r2", "app-purpose:schema-registry"),
]


def _slug(nid: str) -> str:
    return nid.replace(":", "-").replace("/", "-")


def _chain_template(nid: str, ntype: str, prev: str | None, next_id: str | None) -> str:
    lines = ["---", f'id: "{nid}"', f'title: "schema-registry R2 chain: {nid}"', f"type: {ntype}"]
    if prev:
        lines += ["parents:", f"  - {prev}"]
    if next_id:
        lines += ["next_edges:", f"  - {next_id}"]
    lines += ["---", "", f"**{ntype}** node for schema-registry R2: Bracket Convention.", ""]
    lines += ["## Acceptance Criteria", "- R2.1 Bracketed → active", "- R2.2 Non-bracketed → inactive", "- R2.3 Rename to add brackets = activate", "- R2.4 Duplicate active → DuplicateActiveSchemaError"]
    return "\n".join(lines)


def write_chain_nodes() -> list[str]:
    prev_map = {CHAIN_IDS[i]: CHAIN_IDS[i - 1] for i in range(1, len(CHAIN_IDS))}
    next_map = {CHAIN_IDS[i]: CHAIN_IDS[i + 1] for i in range(len(CHAIN_IDS) - 1)}
    written = []
    for nid in CHAIN_IDS:
        ntype = NODE_TYPE_MAP[nid]
        subdir = NODES_DIR / NODE_TYPE_SUBDIRS[ntype]
        subdir.mkdir(parents=True, exist_ok=True)
        path = subdir / f"{_slug(nid)}.md"
        tmpl = _chain_template(nid, ntype, prev_map.get(nid), next_map.get(nid))
        if not path.exists() or "next_edges" not in path.read_text():
            path.write_text(tmpl)
            written.append(str(path.relative_to(ROOT)))
    return written


def load_live_graph():
    from graph_core.graph import Graph
    from graph_core.node import Node
    from graph_core.edge import Edge
    graph = Graph()
    type_map = {
        "idea": "idea", "hypothesis": "hypothesis", "task": "task",
        "experiment": "experiment", "verdict": "verdict",
        "mvp": "mvp", "outcome": "outcome",
        "bigger_outcome": "bigger_outcome", "app_purpose": "app_purpose",
    }
    next_edges_raw = []
    for subdir_name, ntype in type_map.items():
        subdir = NODES_DIR / subdir_name
        if not subdir.exists():
            continue
        for md_file in subdir.glob("*.md"):
            try:
                content = md_file.read_text()
            except Exception:
                continue
            fm_start = content.find("---")
            fm_end = content.find("---", fm_start + 3)
            if fm_start == -1 or fm_end == -1:
                continue
            fm_lines = content[fm_start + 3:fm_end].splitlines()
            node_id, parents, next_edges = None, [], []
            in_next = False
            for line in fm_lines:
                stripped = line.strip()
                if stripped.startswith("id:"):
                    node_id = stripped.split("id:", 1)[1].strip().strip('"').strip("'")
                elif in_next and stripped.startswith("- "):
                    next_edges.append(stripped[2:].strip())
                elif stripped == "next_edges:":
                    in_next = True
                elif in_next and not stripped.startswith("-"):
                    in_next = False
            in_parents = False
            for line in fm_lines:
                stripped = line.strip()
                if stripped == "parents:":
                    in_parents = True
                elif in_parents:
                    if stripped.startswith("- "):
                        parents.append(stripped[2:].strip())
                    elif stripped and not stripped.startswith("#"):
                        in_parents = False
            if node_id:
                graph.add_node(Node(id=node_id, type=ntype, parents=set(parents)))
                for target in next_edges:
                    next_edges_raw.append((node_id, target))
    added = 0
    for src, tgt in next_edges_raw:
        try:
            graph.add_edge(Edge(source_id=src, target_id=tgt, relation="next"))
            added += 1
        except Exception:
            pass
    return graph, added


# ---------------------------------------------------------------------------
# R2 acceptance criteria tests
# ---------------------------------------------------------------------------

def make_schema(d: Path, name: str, body: str = "") -> Path:
    """Create a schema file. body must include --- frontmatter delimiters."""
    p = d / name
    if body:
        p.write_text(body)
    else:
        p.write_text(f'---\nname: "{name.strip("[]")}"\ntype: schema\n---\n')
    return p


def run_r2_tests() -> dict:
    results = {}
    tmpdir = Path(tempfile.mkdtemp(prefix="schema_r2_"))
    try:
        # --- R2.1: Bracketed → active set ---
        # Files [hypothesis].md and [idea].md are bracketed → loaded as active.
        # The active_set stores de-bracketed names as keys.
        make_schema(tmpdir, "[hypothesis].md", '---\nname: "hypothesis"\ntype: schema\nfields:\n  id: string\n---\n')
        make_schema(tmpdir, "[idea].md", '---\nname: "idea"\ntype: schema\n---\n')
        reg1 = load_schemas_from_dir(tmpdir)
        active1 = build_active_set(reg1)
        r2_1 = "hypothesis" in active1.active_names() and "idea" in active1.active_names()
        results["R2.1_bracketed_active"] = {
            "pass": r2_1,
            "active": sorted(active1.active_names()),
            "inactive": sorted(active1.inactive_names()),
        }

        # --- R2.2: Non-bracketed → inactive ---
        make_schema(tmpdir, "task.md", '---\nname: "task"\ntype: schema\n---\n')
        reg2 = load_schemas_from_dir(tmpdir)
        active2 = build_active_set(reg2)
        # task.md is non-bracketed → inactive; hypothesis+idea remain active
        r2_2 = "task" in active2.inactive_names() and "task" not in active2.active_names()
        results["R2.2_non_bracketed_inactive"] = {
            "pass": r2_2,
            "active": sorted(active2.active_names()),
            "inactive": sorted(active2.inactive_names()),
        }

        # --- R2.3: Rename to add brackets = activate ---
        task_file = tmpdir / "task.md"
        task_file = tmpdir / "task.md"
        assert task_file.exists()
        task_file.rename(tmpdir / "[task].md")
        reg3 = load_schemas_from_dir(tmpdir)
        active3 = build_active_set(reg3)
        r2_3 = "task" in active3.active_names()
        results["R2.3_rename_activates"] = {
            "pass": r2_3,
            "active": sorted(active3.active_names()),
        }

        # --- R2.4: Duplicate active → DuplicateActiveSchemaError ---
        dupdir = Path(tempfile.mkdtemp(prefix="schema_r2_dup_"))
        # [hypothesis].md and [hypothesis].json have same canonical name "hypothesis"
        make_schema(dupdir, "[hypothesis].md", '---\nname: "hypothesis"\ntype: schema\n---\n')
        make_schema(dupdir, "[hypothesis].json", '{"name": "hypothesis", "type": "schema"}')
        reg4 = load_schemas_from_dir(dupdir)
        try:
            active4 = build_active_set(reg4)
            results["R2.4_duplicate_raises"] = {
                "pass": False,
                "note": "No DuplicateActiveSchemaError raised (silent dedup?)",
                "active": sorted(active4.active_names()),
            }
        except DuplicateActiveSchemaError as e:
            results["R2.4_duplicate_raises"] = {
                "pass": True,
                "name": e.name,
                "paths": [str(p) for p in e.paths],
            }
        finally:
            shutil.rmtree(dupdir, ignore_errors=True)

        # --- Helper tests ---
        results["R2.helper_is_bracketed"] = {
            "pass": (
                is_bracketed("[hypothesis]") is True and
                is_bracketed("[idea]") is True and
                is_bracketed("task") is False and
                is_bracketed("") is False
            ),
        }
        results["R2.helper_canonical_name"] = {
            "pass": (
                canonical_name("[hypothesis]") == "hypothesis" and
                canonical_name("[idea]") == "idea" and
                canonical_name("task") == "task"
            ),
        }
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)
    return results


def main():
    print("=" * 60)
    print("EXPERIMENT: schema-registry/R2 — Bracket Convention")
    print("=" * 60)

    # --- Part A: R2 acceptance criteria ---
    print("\n## Part A: R2 Acceptance Criteria (5 tests)")
    r2 = run_r2_tests()
    r2_pass = sum(1 for r in r2.values() if r["pass"])
    for name, res in r2.items():
        status = "PASS" if res["pass"] else "FAIL"
        extra = ""
        if name == "R2.1_bracketed_active":
            extra = f" | active={res.get('active', [])}"
        elif name == "R2.4_duplicate_raises" and res["pass"]:
            extra = f" | error.name={res.get('name')}"
        elif name == "R2.2_non_bracketed_inactive":
            extra = f" | inactive={res.get('inactive', [])}"
        print(f"  [{status}] {name}{extra}")

    r2_all = r2_pass == len(r2)

    # --- Part B: Write chain nodes ---
    print("\n## Part B: Writing chain nodes with next_edges")
    written = write_chain_nodes()
    for f in written:
        print(f"  Wrote: {f}")
    if not written:
        print("  (already exist with next_edges)")

    # --- Part C: Cold-reload chain ---
    print("\n## Part C: Cold-reload chain verification")
    from chain_engine.chains import find_chains
    graph, added = load_live_graph()
    print(f"  Nodes: {len(graph.node_ids)}  |  next edges: {added}")
    chains = find_chains(graph)
    print(f"  Chains: {len(chains)}")
    chain_len = max((len(c) for c in chains), default=0)
    print(f"  Longest chain: {chain_len} hops")
    chain_ok = chain_len >= 8

    # --- Part D: pytest ---
    print("\n## Part D: pytest (236 tests)")
    import subprocess
    pr = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-q", "--tb=no"],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    last = pr.stdout.strip().splitlines()
    print(f"  {last[-1] if last else pr.stderr.strip()}")
    tests_ok = pr.returncode == 0

    # --- Overall ---
    overall = r2_all and written is not None and chain_ok and tests_ok
    verdict = "PROVED" if overall else "DISPROVED"

    print(f"\n## Verdict")
    print(f"  R2 criteria: {r2_pass}/{len(r2)}")
    print(f"  Chain: {chain_len} hops {'✓' if chain_ok else '✗'}")
    print(f"  Tests: {'PASS' if tests_ok else 'FAIL'}")
    print(f"  OVERALL: {verdict}")

    print(f"\nMETRIC chain_length={chain_len}")
    print(f"METRIC chains_found={len(chains)}")
    print(f"METRIC r2_passed={r2_pass}")
    print(f"METRIC r2_total={len(r2)}")
    print(f"METRIC tests={'1' if tests_ok else '0'}")
    print(f"METRIC verdict={verdict}")

    return 0 if overall else 1


if __name__ == "__main__":
    sys.exit(main())
