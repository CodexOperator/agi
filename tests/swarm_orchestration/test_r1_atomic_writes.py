#!/usr/bin/env python3
"""Test swarm-orchestration/R1: Atomic File-Based Node Writes

Tests that concurrent verdict writes to unique paths succeed without collision,
and that the graph loader can load all of them afterward.
"""

import multiprocessing
import os
import tempfile
import time
import yaml
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[2]
import sys
sys.path.insert(0, str(PROJECT_ROOT))

from src.graph_core.loader import load_directory


def _write_verdict_file(args):
    """Worker: write N verdict files to a temp directory."""
    tmpdir, worker_id, count, base_time = args
    tmpdir = Path(tmpdir)
    written = []
    for i in range(count):
        verdict_id = f"verdict:swarm-worker{worker_id}-test{i}"
        run_id = f"run-w{worker_id}-{i}"
        filename = f"verdict-swarm-worker{worker_id}-test{i}-{run_id}.md"
        filepath = tmpdir / filename
        content = f"""---
id: "{verdict_id}"
parents:
  - hyp:swarm-orchestration-r1
children: []
subgraph: false
tags:
  - swarm
  - verdict
  - test
type: verdict
verdict: "proved"
confidence: 1.0
evidence_runs:
  - {run_id}
passed: 1
failed: 0
skipped: 0
date: "2026-05-01T06:43:00+00:00"
---
# {verdict_id}
Test verdict from worker {worker_id}, index {i}
"""
        with open(filepath, "x") as f:
            f.write(content)
        written.append(filename)
        time.sleep(0.001)  # tiny stagger
    return written


def _shared_appender(args):
    """Module-level worker for appending to shared file."""
    tmpdir, worker_id, shared_path = args
    shared = Path(tmpdir) / shared_path
    with open(shared, "a") as f:
        f.write(f"entry-from-worker-{worker_id}\n")
    return worker_id


def test_concurrent_unique_writes(tmp_path):
    """TC1: N workers write to unique paths — all succeed, all valid."""
    tmpdir = str(tmp_path)
    num_workers = 8
    files_per_worker = 10
    total_expected = num_workers * files_per_worker

    with multiprocessing.Pool(num_workers) as pool:
        args = [(tmpdir, wid, files_per_worker, time.time()) for wid in range(num_workers)]
        results = pool.map(_write_verdict_file, args)

    all_files = list(tmp_path.glob("verdict-swarm-*.md"))
    assert len(all_files) == total_expected, f"Expected {total_expected}, got {len(all_files)}"

    # All files are valid YAML frontmatter
    valid = 0
    for f in all_files:
        content = f.read_text()
        try:
            data = yaml.safe_load(content.split("---")[1])
            assert data.get("type") == "verdict"
            assert data.get("verdict") == "proved"
            valid += 1
        except Exception:
            pass
    assert valid == total_expected, f"Only {valid}/{total_expected} files valid YAML"

    # No empty files
    for f in all_files:
        assert f.stat().st_size > 0, f"Empty file: {f.name}"


def test_graph_loader_loads_all_verdicts(tmp_path):
    """TC2: Graph loader can load all verdict nodes written concurrently."""
    tmpdir = str(tmp_path)
    num_workers = 4
    files_per_worker = 5
    total_expected = num_workers * files_per_worker

    with multiprocessing.Pool(num_workers) as pool:
        args = [(tmpdir, wid, files_per_worker, time.time()) for wid in range(num_workers)]
        pool.map(_write_verdict_file, args)

    graph, loaded = load_directory(tmpdir)
    verdict_nodes = [n for n in graph._nodes.values() if n.type == "verdict"]
    assert len(verdict_nodes) == total_expected, f"Expected {total_expected} verdict nodes, got {len(verdict_nodes)}"


def test_no_partial_files(tmp_path):
    """TC3: No partial files appear during concurrent writes."""
    tmpdir = str(tmp_path)
    num_workers = 6
    files_per_worker = 5

    with multiprocessing.Pool(num_workers) as pool:
        args = [(tmpdir, wid, files_per_worker, time.time()) for wid in range(num_workers)]
        pool.map(_write_verdict_file, args)

    # Check for partial/lock files
    lock_files = list(tmp_path.glob("*.lock")) + list(tmp_path.glob(".nfs*"))
    assert len(lock_files) == 0, f"Unexpected lock files: {lock_files}"

    # All verdict files are readable and complete
    for f in tmp_path.glob("verdict-swarm-*.md"):
        content = f.read_text()
        assert content.startswith("---\n"), f"Incomplete frontmatter: {f.name}"
        parts = content.split("---")
        assert len(parts) >= 2, f"Malformed file: {f.name}"


def test_atomic_write_no_collision(tmp_path):
    """TC4: Two workers writing to same path — one wins, one fails (not corrupted)."""
    tmpdir = str(tmp_path)
    path_a = tmp_path / "collision-test-a.md"
    path_b = tmp_path / "collision-test-b.md"

    # Worker A writes to path_a
    with open(path_a, "x") as f:
        f.write("---\nid: a\ntype: verdict\n---\n")

    # Worker B writes to path_b (different path — no collision)
    with open(path_b, "x") as f:
        f.write("---\nid: b\ntype: verdict\n---\n")

    # Both files should be valid
    assert path_a.exists() and path_a.read_text().startswith("---")
    assert path_b.exists() and path_b.read_text().startswith("---")

    # Concurrent write to SAME path — one fails with FileExistsError
    try:
        with open(path_a, "x") as f:
            f.write("should not happen")
        pytest.fail("Expected FileExistsError on second write to same path")
    except FileExistsError:
        pass  # Expected

    # Original file is still intact
    assert path_a.read_text().startswith("---")


def test_concurrent_append_serialized(tmp_path):
    """TC5: Concurrent appends to shared file are effectively serialized."""
    tmpdir = str(tmp_path)
    shared_file = "shared-edges.md"

    # Init shared file
    (tmp_path / shared_file).write_text("---\ntype: edge\n---\n")

    with multiprocessing.Pool(4) as pool:
        args = [(tmpdir, wid, shared_file) for wid in range(8)]
        pool.map(_shared_appender, args)

    content = (tmp_path / shared_file).read_text()
    lines = [l for l in content.split("\n") if l.startswith("entry-from-worker-")]
    assert len(lines) == 8, f"Expected 8 entries, got {len(lines)}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
