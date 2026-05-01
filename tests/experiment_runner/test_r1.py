"""Test experiment-automation/R1: Experiment Runner Pattern

Tests that the experiment runner can:
1. Load a hypothesis node by id
2. Find and run corresponding tests
3. Create verdict nodes based on results
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT))

from engines.experiment_runner.runner import (
    compute_verdict,
    hypothesis_to_test_path,
    load_hypothesis,
    run_tests,
)


def test_compute_verdict_all_pass():
    """All tests pass = proved with confidence 1.0."""
    verdict, confidence = compute_verdict(5, 0, 0)
    assert verdict == "proved"
    assert confidence == 1.0


def test_compute_verdict_all_fail():
    """All tests fail = disproved with confidence 1.0."""
    verdict, confidence = compute_verdict(0, 5, 0)
    assert verdict == "disproved"
    assert confidence == 1.0


def test_compute_verdict_mixed():
    """Mixed results = inconclusive."""
    verdict, confidence = compute_verdict(3, 2, 0)
    assert verdict.startswith("inconclusive_lean_proved:")
    assert 0.0 < confidence < 1.0


def test_compute_verdict_no_tests():
    """No tests = pending with confidence 0.0."""
    verdict, confidence = compute_verdict(0, 0, 0)
    assert verdict == "pending"
    assert confidence == 0.0


def test_compute_verdict_some_skipped():
    """Some skipped with all pass = inconclusive (skipped tests not proven)."""
    verdict, confidence = compute_verdict(5, 0, 3)
    assert verdict.startswith("inconclusive_lean_proved:")
    assert 0.0 < confidence < 1.0


def test_hypothesis_to_test_path():
    """Test hypothesis to test file path mapping."""
    # Valid hypothesis (experiment_runner domain has test_r1.py)
    path = hypothesis_to_test_path("hyp:experiment-automation-r1")
    assert path is not None
    assert "experiment_runner" in path
    assert "test_r1.py" in path
    
    # Invalid hypothesis (no r-number)
    path = hypothesis_to_test_path("invalid-hypothesis")
    assert path is None


def test_load_hypothesis():
    """Test loading a hypothesis node."""
    hypothesis = load_hypothesis("hyp:graph-core-r1")
    assert hypothesis is not None
    assert hypothesis.id == "hyp:graph-core-r1"
    assert hypothesis.type == "hypothesis"


def test_load_hypothesis_not_found():
    """Test loading a non-existent hypothesis."""
    hypothesis = load_hypothesis("hyp:does-not-exist")
    assert hypothesis is None
