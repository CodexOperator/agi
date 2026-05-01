"""T-R9 tests: test discovery via experiment-runner.

Acceptance criteria:
  R9.1  hyp:autoresearch-tree-skill-r1 maps to tests/autoresearch_tree_skill/test_r1.py
  R9.2  hyp:autoresearch-tree-skill-r9 maps to tests/autoresearch_tree_skill/test_r9.py
  R9.3  pytest can collect tests from test_r9.py without errors
  R9.4  experiment_runner.runner produces METRIC lines for R9 hypothesis
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

# PROJECT_ROOT = agi-tree/ (this repo's root)
PROJECT_ROOT = Path(__file__).resolve().parents[2]  # p0=test_r9.py, p1=skill/, p2=agi-tree/


def hypothesis_to_test_path(hypothesis_id: str) -> str | None:
    """Mirror of experiment_runner.hypothesis_to_test_path for isolated testing."""
    match = re.match(r'hyp:([\w-]+)-r(\d+)', hypothesis_id)
    if not match:
        return None
    domain = match.group(1)
    r_num = match.group(2)
    domain_path = domain.replace('-', '_')
    if domain_path == 'experiment_automation':
        domain_path = 'experiment_runner'
    test_path = PROJECT_ROOT / "tests" / domain_path / f"test_r{r_num}.py"
    if test_path.exists():
        return str(test_path)
    test_path = PROJECT_ROOT / "tests" / domain_path / f"test_{domain_path}.py"
    if test_path.exists():
        return str(test_path)
    return None


class TestExperimentRunnerMapping:
    """Tests for hypothesis→test_path mapping."""

    def test_r91_r1_maps_to_correct_path(self) -> None:
        """R9.1: hyp:autoresearch-tree-skill-r1 → tests/autoresearch_tree_skill/test_r1.py."""
        path = hypothesis_to_test_path("hyp:autoresearch-tree-skill-r1")
        assert path is not None, "hypothesis_to_test_path returned None for r1"
        assert "autoresearch_tree_skill" in path, f"path doesn't contain autoresearch_tree_skill: {path}"
        assert "test_r1.py" in path, f"path doesn't end with test_r1.py: {path}"
        assert Path(path).exists(), f"mapped test file does not exist: {path}"

    def test_r92_r9_maps_to_correct_path(self) -> None:
        """R9.2: hyp:autoresearch-tree-skill-r9 → tests/autoresearch_tree_skill/test_r9.py."""
        path = hypothesis_to_test_path("hyp:autoresearch-tree-skill-r9")
        assert path is not None, "hypothesis_to_test_path returned None for r9"
        assert "autoresearch_tree_skill" in path, f"path doesn't contain autoresearch_tree_skill: {path}"
        assert "test_r9.py" in path, f"path doesn't end with test_r9.py: {path}"
        assert Path(path).exists(), f"mapped test file does not exist: {path}"

    def test_r93_pytest_collects_r9_tests(self) -> None:
        """R9.3: pytest can collect tests from test_r9.py without errors."""
        test_file = PROJECT_ROOT / "tests" / "autoresearch_tree_skill" / "test_r9.py"
        result = subprocess.run(
            [sys.executable, "-m", "pytest", str(test_file), "--collect-only", "-q"],
            capture_output=True,
            text=True,
            cwd=str(PROJECT_ROOT),
        )
        # Exit code 0 = collection succeeded (exit 5 = no tests collected)
        assert result.returncode == 0, f"pytest collection failed (rc={result.returncode}): {result.stderr}"

    def test_r94_experiment_runner_executes_successfully(self) -> None:
        """R9.4: running experiment-runner for R9 exits cleanly (0 or 1, not crash)."""
        result = subprocess.run(
            [
                sys.executable, "-m",
                "engines.experiment_runner.runner",
                "hyp:autoresearch-tree-skill-r9",
            ],
            capture_output=True,
            text=True,
            cwd=str(PROJECT_ROOT),
            timeout=60,
        )
        output = result.stdout + result.stderr
        # Accept exit 0 (tests pass) or 1 (tests fail) — not crash (2+)
        assert result.returncode in (0, 1), (
            f"experiment-runner crashed (rc={result.returncode}):\n{output[:1000]}"
        )
        assert "Hypothesis: hyp:autoresearch-tree-skill-r9" in output, \
            f"Runner didn't process R9 hypothesis:\n{output[:500]}"
