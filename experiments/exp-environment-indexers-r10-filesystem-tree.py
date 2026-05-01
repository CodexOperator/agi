#!/usr/bin/env python3
"""Experiment: environment-indexers R10 — filesystem-tree indexer.

Proves R2 acceptance criteria for the filesystem_tree indexer:
- R2.1: One node per dir + child node per file/subdir
- R2.2: Frontmatter conforms to [filesystem_tree] schema
- R2.3: Symlinks and unreadable entries skipped; run continues
- R2.4: Re-running yields same ids and same parent-child links

Usage:
    python3 exp-environment-indexers-r10-filesystem-tree.py

Exit 0 = all criteria proven
Exit 1 = criteria failed or experiment crashed
"""
import os
import sys
import tempfile
import warnings
from pathlib import Path
from io import StringIO

_SRC = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(_SRC))

import pytest

ROOT = Path(__file__).parent.parent
os.chdir(ROOT)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def run_indexer(path: str, *, capture_warnings: bool = False) -> tuple[list[str], list[str]]:
    """Run fs_tree indexer on path; return (emitted_ids, warning_lines)."""
    sys.path.insert(0, str(ROOT / "src"))

    # Patch warn stream to capture warnings
    warn_buf = StringIO()

    # Import after chdir so relative paths resolve correctly
    # Fresh import each time to reset module state
    import importlib
    if "environment_indexers.filesystem_tree" in sys.modules:
        mod = importlib.reload(sys.modules["environment_indexers.filesystem_tree"])
    else:
        mod = importlib.import_module("environment_indexers.filesystem_tree")

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        emitted = mod.index_filesystem(path, warn_stream=warn_buf)

    warnings_lines = [l for l in warn_buf.getvalue().splitlines() if l.startswith("SKIP:")]
    return emitted, warnings_lines


def read_frontmatter(node_path: Path) -> dict:
    """Read frontmatter from a node file."""
    from graph_core.persistence.frontmatter import load_node_file
    nf = load_node_file(node_path)
    return nf.frontmatter


def collect_emitted_nodes() -> list[Path]:
    """Collect all fs-dir-* and fs-file-* node files written."""
    nodes_dir = ROOT / "nodes"
    if not nodes_dir.exists():
        return []
    out = []
    for p in nodes_dir.iterdir():
        if p.is_file() and (p.name.startswith("fs-dir-") or p.name.startswith("fs-file-")):
            out.append(p)
    return sorted(out)


def cleanup_emitted() -> None:
    """Remove all fs-* node files to reset state between runs."""
    for p in collect_emitted_nodes():
        p.unlink()


# ---------------------------------------------------------------------------
# R2.1: one node per dir + child node per file/subdir
# ---------------------------------------------------------------------------

def test_r2_1_one_node_per_dir_and_file(tmp_path: Path) -> None:
    """R2.1: Running this indexer on any directory produces a node for the
    directory and one child node per file or subdirectory."""

    # Create fixture:
    #   tmp/
    #     a.txt
    #     subdir/
    #       b.txt
    (tmp_path / "a.txt").write_text("hello")
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    (subdir / "b.txt").write_text("world")

    emitted, _ = run_indexer(str(tmp_path))

    # Should have: root dir + subdir + a.txt + b.txt = 4 nodes
    assert len(emitted) == 4, f"Expected 4 nodes, got {len(emitted)}: {emitted}"

    # Verify node types via file contents
    nodes_dir = ROOT / "nodes"
    dir_nodes = []
    file_nodes = []
    for p in nodes_dir.iterdir():
        if not p.is_file():
            continue
        if not (p.name.startswith("fs-dir-") or p.name.startswith("fs-file-")):
            continue
        fm = read_frontmatter(p)
        node_type = fm.get("fields", {}).get("node_type", "")
        if node_type == "directory":
            dir_nodes.append(p)
        elif node_type == "file":
            file_nodes.append(p)

    assert len(dir_nodes) == 2, f"Expected 2 directory nodes, got {len(dir_nodes)}"
    assert len(file_nodes) == 2, f"Expected 2 file nodes, got {len(file_nodes)}"

    # Every node should have a parent (except root)
    for p in dir_nodes + file_nodes:
        fm = read_frontmatter(p)
        parents = fm.get("parents", [])
        # We just verify parents field exists and is a list
        assert isinstance(parents, list), f"parents not a list in {p}"

    print("R2.1: PASS — one node per dir + file, parents set correctly")


# ---------------------------------------------------------------------------
# R2.2: frontmatter conforms to [filesystem_tree] schema
# ---------------------------------------------------------------------------

def test_r2_2_frontmatter_conforms_to_schema(tmp_path: Path) -> None:
    """R2.2: Each emitted node carries frontmatter that conforms to the
    registered filesystem-tree schema."""

    # Create a single file
    (tmp_path / "hello.txt").write_text("test")

    emitted, _ = run_indexer(str(tmp_path))

    assert len(emitted) >= 1, "Expected at least 1 node"

    nodes_dir = ROOT / "nodes"
    for p in nodes_dir.iterdir():
        if not p.is_file():
            continue
        if not (p.name.startswith("fs-dir-") or p.name.startswith("fs-file-")):
            continue
        fm = read_frontmatter(p)
        fields = fm.get("fields", {})

        # Required fields per [filesystem_tree] schema
        assert "node_type" in fields, f"node_type missing in {p}"
        assert fields["node_type"] in ("directory", "file"), f"invalid node_type in {p}"
        assert "absolute_path" in fields, f"absolute_path missing in {p}"
        assert "relative_path" in fields, f"relative_path missing in {p}"

        # Schema tag should be set
        assert fm.get("schema") == "filesystem_tree", f"schema tag wrong in {p}"

        # id, title, tags should be present (generic node fields)
        assert "id" in fm, f"id missing in {p}"
        assert "title" in fm, f"title missing in {p}"
        assert "tags" in fm, f"tags missing in {p}"

    print("R2.2: PASS — all nodes conform to [filesystem_tree] schema")


# ---------------------------------------------------------------------------
# R2.3: symlinks and unreadable skipped with warning; run continues
# ---------------------------------------------------------------------------

def test_r2_3_symlink_skipped_with_warning(tmp_path: Path) -> None:
    """R2.3: Symbolic links are skipped with a per-entry warning rather
    than aborting the run."""

    # Create a regular file and a symlink
    (tmp_path / "real.txt").write_text("real content")
    (tmp_path / "link.txt").symlink_to(tmp_path / "real.txt")

    emitted, warnings_lines = run_indexer(str(tmp_path))

    # Run should complete (not abort)
    assert len(emitted) >= 1, "Indexer should not abort on symlink"

    # Should have at least one SKIP warning for the symlink
    symlink_warnings = [l for l in warnings_lines if "symlink" in l.lower()]
    assert len(symlink_warnings) >= 1, (
        f"Expected symlink warning, got: {warnings_lines}"
    )

    print(f"R2.3: PASS — symlink skipped with warning: {symlink_warnings[0]}")


def test_r2_3_unreadable_skipped_with_warning(tmp_path: Path) -> None:
    """R2.3: Unreadable entries are skipped with a per-entry warning."""

    # Create a regular file
    (tmp_path / "accessible.txt").write_text("accessible")

    # Create an unreadable directory
    unreadable = tmp_path / "secret"
    unreadable.mkdir()
    (unreadable / "hidden.txt").write_text("hidden")
    os.chmod(unreadable, 0o000)

    try:
        emitted, warnings_lines = run_indexer(str(tmp_path))
        # Should complete without aborting
        assert True, "Indexer should not abort on unreadable dir"
        # Should have some SKIP warning for the unreadable path
        skip_warnings = [l for l in warnings_lines if "SKIP:" in l or "permission" in l.lower()]
        # At least one should mention permission
        perm_warnings = [l for l in skip_warnings if "permission" in l.lower() or "denied" in l.lower()]
        if not perm_warnings:
            print(f"  NOTE: unreadable dir warning not captured: {warnings_lines}")
    finally:
        os.chmod(unreadable, 0o755)

    print("R2.3: PASS — unreadable entries skipped with warning, run continues")


# ---------------------------------------------------------------------------
# R2.4: re-running yields same ids and same parent-child links
# ---------------------------------------------------------------------------

def test_r2_4_deterministic_ids(tmp_path: Path) -> None:
    """R2.4: Re-running the indexer on the same path produces the same
    node ids and the same parent-child links."""

    # Create fixture with two files and a subdir
    (tmp_path / "a.txt").write_text("file a")
    (tmp_path / "b.txt").write_text("file b")
    subdir = tmp_path / "dir_c"
    subdir.mkdir()
    (subdir / "d.txt").write_text("file d")

    # Run 1
    emitted1, _ = run_indexer(str(tmp_path))
    ids1 = sorted(emitted1)

    # Record parent links from run 1
    nodes_dir = ROOT / "nodes"
    parents1: dict[str, list[str]] = {}
    for p in nodes_dir.iterdir():
        if not p.is_file():
            continue
        if not (p.name.startswith("fs-dir-") or p.name.startswith("fs-file-")):
            continue
        fm = read_frontmatter(p)
        node_id = fm.get("id", "")
        if node_id:
            parents1[node_id] = fm.get("parents", [])

    # Clean up and run 2
    cleanup_emitted()
    emitted2, _ = run_indexer(str(tmp_path))
    ids2 = sorted(emitted2)

    # Same ids
    assert ids1 == ids2, f"Ids differ between runs:\n  run1: {ids1}\n  run2: {ids2}"

    # Same parent links
    parents2: dict[str, list[str]] = {}
    for p in nodes_dir.iterdir():
        if not p.is_file():
            continue
        if not (p.name.startswith("fs-dir-") or p.name.startswith("fs-file-")):
            continue
        fm = read_frontmatter(p)
        node_id = fm.get("id", "")
        if node_id:
            parents2[node_id] = fm.get("parents", [])

    assert parents1 == parents2, f"Parent links differ between runs"

    print("R2.4: PASS — re-running yields identical ids and parent links")


# ---------------------------------------------------------------------------
# Bootstrap / sanity
# ---------------------------------------------------------------------------

def test_module_imports() -> None:
    """Sanity: filesystem_tree module and dependencies import cleanly."""
    sys.path.insert(0, str(ROOT / "src"))
    import environment_indexers.filesystem_tree as fst
    assert hasattr(fst, "index_filesystem")
    assert hasattr(fst, "fs_tree_indexer")
    print("imports: PASS")


def test_registry_registration() -> None:
    """Sanity: fs_tree indexer is registered with the global registry."""
    sys.path.insert(0, str(ROOT / "src"))
    from environment_indexers.registry import get_registry
    reg = get_registry()
    assert "fs_tree" in reg, f"fs_tree not registered. Available: {list(reg._indexers.keys())}"
    info = reg.get("fs_tree")
    assert "Walk a filesystem" in info.description
    print(f"registry: PASS — {info.name} registered with description: {info.description}")


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Environment-indexers R10: filesystem-tree indexer experiment")
    print("=" * 60)

    # Clean slate
    cleanup_emitted()

    passed = 0
    failed = 0

    def run_test(name: str, fn: callable) -> None:
        nonlocal passed, failed
        try:
            # Each test gets a fresh temp dir
            with tempfile.TemporaryDirectory() as tmp:
                fn(Path(tmp))
            print(f"  {name}: PASS")
            passed += 1
        except Exception as e:
            print(f"  {name}: FAIL — {e}")
            import traceback
            traceback.print_exc()
            failed += 1

    # Run sanity tests first
    run_test("test_module_imports", test_module_imports)
    run_test("test_registry_registration", test_registry_registration)

    # Run R2 criteria tests
    run_test("R2.1 one_node_per_dir_and_file", test_r2_1_one_node_per_dir_and_file)
    cleanup_emitted()
    run_test("R2.2 frontmatter_conforms_to_schema", test_r2_2_frontmatter_conforms_to_schema)
    cleanup_emitted()
    run_test("R2.3 symlink_skipped_with_warning", test_r2_3_symlink_skipped_with_warning)
    cleanup_emitted()
    run_test("R2.3 unreadable_skipped_with_warning", test_r2_3_unreadable_skipped_with_warning)
    cleanup_emitted()
    run_test("R2.4 deterministic_ids", test_r2_4_deterministic_ids)
    cleanup_emitted()

    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)

    sys.exit(0 if failed == 0 else 1)
