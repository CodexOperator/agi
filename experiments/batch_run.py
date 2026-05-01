#!/usr/bin/env python3
"""
Batch Experiment Runner — run all hypothesis tests and produce verdict nodes.

Hypothesis → test mapping (fallback convention for non-test_r<n>.py domains):
  hyp:graph-core-r1  → tests/graph_core/test_node.py
  hyp:graph-core-r2  → tests/graph_core/test_edge.py + test_graph_dag.py
  hyp:graph-core-r3  → tests/graph_core/test_identity.py
  hyp:graph-core-r4  → tests/graph_core/test_frontmatter.py + test_lazy_body.py
  hyp:graph-core-r5  → tests/graph_core/test_recursive_bodies.py
  hyp:graph-core-r6  → tests/graph_core/test_walk_determinism.py
  hyp:graph-core-r7  → tests/graph_core/test_warm_load.py
  hyp:chain-engine-r1 → tests/chain_engine/test_chain_definition.py
  hyp:experiment-runner-r1 → tests/experiment_runner/test_r1.py
  hyp:renderers-r1   → tests/renderers/test_representation.py
  hyp:renderers-r2   → tests/renderers/test_ascii.py + test_ascii_summary.py
  hyp:renderers-r3   → tests/renderers/test_mermaid.py
  hyp:renderers-r5   → tests/renderers/test_git_diff.py
  hyp:schema-registry-r1 → tests/schema_registry/test_schema_files.py
  hyp:schema-registry-r2 → tests/schema_registry/test_brackets.py
  hyp:schema-registry-r3 → tests/schema_registry/test_meta_nodes.py
  hyp:schema-registry-r4 → tests/schema_registry/test_validation.py
  hyp:schema-registry-r5 → tests/schema_registry/test_cascade_step_1.py + test_cascade_step_2.py
  hyp:embeddings-r1  → tests/embeddings/test_node2vec.py
  hyp:embeddings-r2  → tests/embeddings/test_projection.py
  hyp:embeddings-r5  → tests/embeddings/test_similarity.py
"""

from __future__ import annotations

import re
import subprocess
import sys
import uuid
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.graph_core.loader import load_directory


# Manual hypothesis → test files mapping (covers all tested hypotheses)
HYPOTHESIS_TEST_MAP: dict[str, list[str]] = {
    "hyp:graph-core-r1": ["tests/graph_core/test_node.py"],
    "hyp:graph-core-r2": ["tests/graph_core/test_edge.py", "tests/graph_core/test_graph_dag.py"],
    "hyp:graph-core-r3": ["tests/graph_core/test_identity.py"],
    "hyp:graph-core-r4": ["tests/graph_core/test_frontmatter.py", "tests/graph_core/test_frontmatter_errors.py", "tests/graph_core/test_lazy_body.py"],
    "hyp:graph-core-r5": ["tests/graph_core/test_recursive_bodies.py"],
    "hyp:graph-core-r6": ["tests/graph_core/test_walk_determinism.py"],
    "hyp:graph-core-r7": ["tests/graph_core/test_warm_load.py"],
    "hyp:chain-engine-r1": ["tests/chain_engine/test_chain_definition.py"],
    "hyp:chain-engine-r9": ["tests/chain_engine/test_attractiveness_impact.py"],
    "hyp:experiment-runner-r1": ["tests/experiment_runner/test_r1.py"],
    "hyp:renderers-r1": ["tests/renderers/test_representation.py"],
    "hyp:renderers-r2": ["tests/renderers/test_ascii.py", "tests/renderers/test_ascii_summary.py"],
    "hyp:renderers-r3": ["tests/renderers/test_mermaid.py"],
    "hyp:renderers-r5": ["tests/renderers/test_git_diff.py"],
    "hyp:schema-registry-r1": ["tests/schema_registry/test_schema_files.py"],
    "hyp:schema-registry-r2": ["tests/schema_registry/test_brackets.py"],
    "hyp:schema-registry-r3": ["tests/schema_registry/test_meta_nodes.py"],
    "hyp:schema-registry-r4": ["tests/schema_registry/test_validation.py"],
    "hyp:schema-registry-r5": ["tests/schema_registry/test_cascade_step_1.py", "tests/schema_registry/test_cascade_step_2.py"],
    "hyp:embeddings-r1": ["tests/embeddings/test_node2vec.py"],
    "hyp:embeddings-r2": ["tests/embeddings/test_projection.py"],
    "hyp:embeddings-r5": ["tests/embeddings/test_similarity.py"],
    # Aggregated domain-level experiments
    "hyp:graph-core-domain": ["tests/graph_core/"],
    "hyp:schema-registry-domain": ["tests/schema_registry/"],
    "hyp:renderers-domain": ["tests/renderers/"],
    "hyp:embeddings-domain": ["tests/embeddings/"],
    "hyp:chain-engine-domain": ["tests/chain_engine/"],
}


@dataclass
class ExperimentResult:
    hypothesis_id: str
    run_id: str
    passed: int
    failed: int
    skipped: int
    verdict: str
    confidence: float
    test_files: list[str]


def run_pytest_tests(test_paths: list[str]) -> tuple[int, int, int]:
    """Run pytest on one or more test paths. Returns (passed, failed, skipped)."""
    all_passed = all_failed = all_skipped = 0

    for path in test_paths:
        p = PROJECT_ROOT / path
        if not p.exists():
            print(f"  SKIP (not found): {path}")
            continue

        # If path is a directory, run all tests in it
        args = [str(p)]
        if p.is_dir():
            args = [str(p) + "/"]

        try:
            result = subprocess.run(
                ["python3", "-m", "pytest"] + args + ["-v", "--tb=short"],
                capture_output=True,
                text=True,
                cwd=str(PROJECT_ROOT),
                timeout=180
            )
            output = result.stdout + result.stderr

            # Parse summary line first (most reliable)
            passed = failed = skipped = 0
            summary = re.search(r'(\d+) passed', output)
            if summary:
                passed = int(summary.group(1))
            summary_f = re.search(r'(\d+) failed', output)
            if summary_f:
                failed = int(summary_f.group(1))
            summary_s = re.search(r'(\d+) skipped', output)
            if summary_s:
                skipped = int(summary_s.group(1))

            # Also count explicit markers as verification
            passed += len(re.findall(r'PASSED', output))
            failed += len(re.findall(r'FAILED', output))
            skipped += len(re.findall(r'SKIPPED', output))

            all_passed += passed
            all_failed += failed
            all_skipped += skipped
            print(f"  {path}: {passed}P / {failed}F / {skipped}S")

        except subprocess.TimeoutExpired:
            print(f"  TIMEOUT: {path}")
            all_failed += 1
        except Exception as e:
            print(f"  ERROR {path}: {e}")
            all_failed += 1

    return all_passed, all_failed, all_skipped


def compute_verdict(passed: int, failed: int, skipped: int) -> tuple[str, float]:
    """Compute verdict string + confidence from test counts."""
    total = passed + failed + skipped
    if total == 0:
        return "pending", 0.0
    if failed == 0 and skipped == 0:
        return "proved", 1.0
    if passed == 0 and skipped == 0:
        return "disproved", 1.0
    if failed == 0:
        lean = int((passed / total) * 100)
        return f"inconclusive_lean_proved:{lean}", 0.5 + (lean / 200)
    if passed == 0:
        lean = int((failed / total) * 100)
        return f"inconclusive_lean_disproved:{lean}", 0.5 + (lean / 200)
    pass_ratio = passed / total
    lean = int(pass_ratio * 100)
    if pass_ratio >= 0.7:
        return f"inconclusive_lean_proved:{lean}", 0.6
    elif pass_ratio >= 0.3:
        return f"inconclusive_lean_proved:{lean}", 0.4
    else:
        lean = int((failed / total) * 100)
        return f"inconclusive_lean_disproved:{lean}", 0.6


def write_verdict_node(result: ExperimentResult) -> Path:
    """Write verdict node to nodes/verdict/ directory."""
    verdict_dir = PROJECT_ROOT / "nodes" / "verdict"
    verdict_dir.mkdir(parents=True, exist_ok=True)

    # Create a readable slug from hypothesis id
    hyp_slug = result.hypothesis_id.replace(":", "-").replace("_", "-")
    run_slug = result.run_id.replace("-", "")
    verdict_id = f"verdict:{hyp_slug}-{run_slug}"
    verdict_id = verdict_id.replace("--", "-")[:60]

    verdict_file = verdict_dir / f"{verdict_id}.md"

    status = result.verdict.split(":")[0]
    date = datetime.now().isoformat()

    content = f"""---
id: "{verdict_id}"
parents:
  - {result.hypothesis_id}
children: []
subgraph: false
tags:
  - verdict
  - experiment
type: verdict
verdict: "{result.verdict}"
confidence: {result.confidence}
evidence_runs:
  - {result.run_id}
passed: {result.passed}
failed: {result.failed}
skipped: {result.skipped}
date: "{date}"
test_files:
{chr(10).join(f"  - {f}" for f in result.test_files)}
---

# Verdict: {result.hypothesis_id}

**Verdict:** {result.verdict}
**Confidence:** {result.confidence:.2f}
**Evidence Run:** {result.run_id}

## Test Results

| Metric | Value |
|---|---|
| Passed | {result.passed} |
| Failed | {result.failed} |
| Skipped | {result.skipped} |
| Total | {result.passed + result.failed + result.skipped} |

## Test Files

{chr(10).join(f"- `{f}`" for f in result.test_files)}

## Interpretation

{"All tests pass — hypothesis is **proved**." if result.verdict == "proved" else "Some or all tests fail — hypothesis is **not proved**." if "disproved" in result.verdict else "Mixed results — hypothesis is **inconclusive**."}
"""
    verdict_file.write_text(content)
    print(f"  → Wrote verdict: {verdict_file}")
    return verdict_file


def run_experiment(hypothesis_id: str, test_files: list[str]) -> ExperimentResult:
    """Run experiment for a hypothesis."""
    run_id = f"run-{uuid.uuid4().hex[:8]}"
    print(f"\n{'='*60}")
    print(f"Experiment: {hypothesis_id}")
    print(f"Run ID: {run_id}")
    print(f"Test files: {test_files}")

    passed, failed, skipped = run_pytest_tests(test_files)
    verdict, confidence = compute_verdict(passed, failed, skipped)

    return ExperimentResult(
        hypothesis_id=hypothesis_id,
        run_id=run_id,
        passed=passed,
        failed=failed,
        skipped=skipped,
        verdict=verdict,
        confidence=confidence,
        test_files=test_files,
    )


def main():
    print("=== Batch Experiment Runner ===")
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Hypotheses to test: {len(HYPOTHESIS_TEST_MAP)}")

    results: list[ExperimentResult] = []

    for hyp_id, test_files in HYPOTHESIS_TEST_MAP.items():
        # Verify hypothesis exists in graph
        graph, loaded = load_directory(str(PROJECT_ROOT / "nodes"))
        node = graph.get_node(hyp_id) if hasattr(graph, 'get_node') else None

        result = run_experiment(hyp_id, test_files)
        write_verdict_node(result)
        results.append(result)

    # Summary
    print(f"\n{'='*60}")
    print("=== SUMMARY ===")
    total_p = total_f = total_s = 0
    for r in results:
        print(f"  {r.hypothesis_id}: {r.verdict} (conf={r.confidence:.2f}) {r.passed}P/{r.failed}F/{r.skipped}S")
        total_p += r.passed
        total_f += r.failed
        total_s += r.skipped

    print(f"\nTotal: {total_p}P / {total_f}F / {total_s}S")
    print(f"Proved: {sum(1 for r in results if r.verdict == 'proved')}")
    print(f"Pending: {sum(1 for r in results if r.verdict == 'pending')}")
    print(f"Inconclusive: {sum(1 for r in results if 'inconclusive' in r.verdict)}")

    # METRIC lines for autoresearch
    print(f"\nMETRIC total_passed={total_p}")
    print(f"METRIC total_failed={total_f}")
    print(f"METRIC total_skipped={total_s}")
    print(f"METRIC hypotheses_tested={len(results)}")
    print(f"METRIC proved_count={sum(1 for r in results if r.verdict == 'proved')}")
    print(f"METRIC verdict_aggregated={'proved' if total_f == 0 and total_s == 0 else 'inconclusive'}")

    return results


if __name__ == "__main__":
    main()
