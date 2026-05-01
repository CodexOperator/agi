#!/usr/bin/env python3
"""
Experiment Runner — experiment-automation/R1 MVP

Takes a hypothesis node id, finds corresponding tests, runs them,
and produces a verdict + optional MVP node.

Usage:
    python -m engines.experiment_runner.runner hyp:graph-core-r1
    python -m engines.experiment_runner.runner exp:experiment-runner-pattern
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

# Project root for imports
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from src.graph_core.loader import load_directory
from src.graph_core.node import Node
from src.graph_core.identity import IdRegistry, mint_id


@dataclass
class ExperimentResult:
    """Result of running an experiment."""
    hypothesis_id: str
    run_id: str
    passed: int
    failed: int
    skipped: int
    verdict: str  # proved | disproved | inconclusive | pending
    confidence: float
    source_files: list[str]


def load_hypothesis(hypothesis_id: str) -> Optional[Node]:
    """Load a hypothesis node by id."""
    graph, loaded = load_directory(str(PROJECT_ROOT / "nodes"))
    return graph.get_node(hypothesis_id)


def hypothesis_to_test_path(hypothesis_id: str) -> Optional[str]:
    """Map hypothesis id to test file path.
    
    Convention: hyp:<domain>-r<n> -> tests/<domain>/test_r<n>.py
    Example: hyp:graph-core-r1 -> tests/graph_core/test_r1.py
    Example: hyp:experiment-automation-r1 -> tests/experiment_runner/test_r1.py
    """
    # Extract domain and r-number (allow hyphens in domain)
    match = re.match(r'hyp:([\w-]+)-r(\d+)', hypothesis_id)
    if not match:
        return None
    
    domain = match.group(1)
    r_num = match.group(2)
    
    # Convert domain separators (experiment-automation -> experiment_runner)
    domain_path = domain.replace('-', '_')
    # Special case: experiment-automation maps to experiment_runner tests
    if domain_path == 'experiment_automation':
        domain_path = 'experiment_runner'
    
    # Build test path: test_r<n>.py
    test_path = PROJECT_ROOT / "tests" / domain_path / f"test_r{r_num}.py"
    if test_path.exists():
        return str(test_path)
    
    # Fallback: try test_<domain>.py pattern
    test_path = PROJECT_ROOT / "tests" / domain_path / f"test_{domain_path}.py"
    if test_path.exists():
        return str(test_path)
    
    return None


def run_tests(test_path: str) -> tuple[int, int, int]:
    """Run pytest on a test file. Returns (passed, failed, skipped)."""
    try:
        result = subprocess.run(
            ["python", "-m", "pytest", test_path, "-v", "--tb=short", "--no-header"],
            capture_output=True,
            text=True,
            cwd=str(PROJECT_ROOT),
            timeout=120
        )
        
        output = result.stdout + result.stderr
        
        # Parse pytest output
        passed = len(re.findall(r'PASSED', output))
        failed = len(re.findall(r'FAILED', output))
        skipped = len(re.findall(r'SKIPPED', output))
        
        # If no explicit counts, try to parse summary line
        if not (passed or failed or skipped):
            summary_match = re.search(r'(\d+) passed.*?(\d+) failed.*?(\d+) skipped', output)
            if summary_match:
                passed = int(summary_match.group(1))
                failed = int(summary_match.group(2))
                skipped = int(summary_match.group(3))
        
        return passed, failed, skipped
        
    except subprocess.TimeoutExpired:
        return 0, 0, 0
    except Exception as e:
        print(f"Error running tests: {e}", file=sys.stderr)
        return 0, 0, 0


def compute_verdict(passed: int, failed: int, skipped: int) -> tuple[str, float]:
    """Compute verdict from test results.
    
    Rules:
    - All pass + no skipped = proved (confidence 1.0)
    - All fail = disproved (confidence 1.0)
    - Mix = inconclusive_lean_proved:N or inconclusive_lean_disproved:N
    - No tests = pending (confidence 0.0)
    """
    total = passed + failed + skipped
    
    if total == 0:
        return "pending", 0.0
    
    if failed == 0 and skipped == 0:
        return "proved", 1.0
    
    if passed == 0 and skipped == 0:
        return "disproved", 1.0
    
    # Mixed results
    if failed == 0:  # Some passed, rest skipped
        lean = int((passed / total) * 100)
        return f"inconclusive_lean_proved:{lean}", 0.5 + (lean / 200)
    
    if passed == 0:  # Some failed, rest skipped
        lean = int((failed / total) * 100)
        return f"inconclusive_lean_disproved:{lean}", 0.5 + (lean / 200)
    
    # True mix
    pass_ratio = passed / total
    if pass_ratio >= 0.7:
        lean = int(pass_ratio * 100)
        return f"inconclusive_lean_proved:{lean}", 0.6
    elif pass_ratio >= 0.3:
        lean = int(pass_ratio * 100)
        return f"inconclusive_lean_proved:{lean}", 0.4
    else:
        lean = int((failed / total) * 100)
        return f"inconclusive_lean_disproved:{lean}", 0.6


def run_experiment(hypothesis_id: str) -> ExperimentResult:
    """Run an experiment for a hypothesis."""
    hypothesis = load_hypothesis(hypothesis_id)
    
    if not hypothesis:
        print(f"Hypothesis not found: {hypothesis_id}")
        return ExperimentResult(
            hypothesis_id=hypothesis_id,
            run_id="",
            passed=0,
            failed=0,
            skipped=0,
            verdict="pending",
            confidence=0.0,
            source_files=[]
        )
    
    run_id = f"run-{uuid.uuid4().hex[:8]}"
    test_path = hypothesis_to_test_path(hypothesis_id)
    
    if not test_path:
        print(f"No test file found for {hypothesis_id}")
        return ExperimentResult(
            hypothesis_id=hypothesis_id,
            run_id=run_id,
            passed=0,
            failed=0,
            skipped=0,
            verdict="pending",
            confidence=0.0,
            source_files=[]
        )
    
    print(f"Running tests: {test_path}")
    passed, failed, skipped = run_tests(test_path)
    verdict, confidence = compute_verdict(passed, failed, skipped)
    
    # Find corresponding source files
    source_files = []
    match = re.match(r'hyp:(\w+)-r(\d+)', hypothesis_id)
    if match:
        domain = match.group(1).replace('-', '_')
        r_num = match.group(2)
        src_path = PROJECT_ROOT / "src" / domain / f"r{r_num}.py"
        if src_path.exists():
            source_files.append(str(src_path))
    
    return ExperimentResult(
        hypothesis_id=hypothesis_id,
        run_id=run_id,
        passed=passed,
        failed=failed,
        skipped=skipped,
        verdict=verdict,
        confidence=confidence,
        source_files=source_files
    )


def create_verdict_node(result: ExperimentResult) -> dict:
    """Create verdict node content."""
    verdict_id = f"verdict:{result.run_id}"
    
    node = {
        "id": verdict_id,
        "parents": [result.hypothesis_id],
        "children": [],
        "status": result.verdict.split(":")[0],  # 'proved', 'disproved', 'inconclusive', 'pending'
        "verdict": result.verdict,
        "confidence": result.confidence,
        "evidence_runs": [result.run_id],
        "tags": ["verdict", "experiment"],
        "date": datetime.now().isoformat(),
        "passed": result.passed,
        "failed": result.failed,
        "skipped": result.skipped
    }
    
    return node


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m engines.experiment_runner.runner <hypothesis_id>")
        sys.exit(1)
    
    hypothesis_id = sys.argv[1]
    print(f"=== Experiment Runner ===")
    print(f"Hypothesis: {hypothesis_id}")
    
    result = run_experiment(hypothesis_id)
    
    print(f"\n=== Results ===")
    print(f"Run ID: {result.run_id}")
    print(f"Tests: {result.passed} passed, {result.failed} failed, {result.skipped} skipped")
    print(f"Verdict: {result.verdict}")
    print(f"Confidence: {result.confidence:.2f}")
    
    if result.source_files:
        print(f"Source files: {result.source_files}")
    
    # Create verdict node
    verdict = create_verdict_node(result)
    print(f"\n=== Verdict Node ===")
    print(f"ID: {verdict['id']}")
    print(f"Parents: {verdict['parents']}")
    print(f"Verdict: {verdict['verdict']}")
    
    # Output METRIC lines for autoresearch
    print(f"\nMETRIC experiment_passed={result.passed}")
    print(f"METRIC experiment_failed={result.failed}")
    print(f"METRIC experiment_skipped={result.skipped}")
    print(f"METRIC experiment_confidence={result.confidence}")
    print(f"METRIC experiment_verdict={verdict['status']}")
    
    return verdict


if __name__ == "__main__":
    main()
