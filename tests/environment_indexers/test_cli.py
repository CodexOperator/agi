"""Tests for environment_indexers CLI.

Covers R1 acceptance criteria:
- R1.1: Command accepts target path and indexer name; runs only that indexer
- R1.2: Listing without invocation produces summary with name + one-line description
- R1.3: Unknown indexer name returns structured error, runs nothing
- R1.4: Non-zero exit when failure prevented node emission
"""

from __future__ import annotations

import argparse
import json
import sys
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import pytest

from environment_indexers.cli import list_indexers, run_indexer
from environment_indexers.errors import IndexerExecutionError, UnknownIndexerError
from environment_indexers.registry import IndexerRegistry, get_registry


@pytest.fixture
def fresh_registry() -> IndexerRegistry:
    """Provide a fresh registry for each test."""
    # Create a test registry by patching the global
    registry = IndexerRegistry()
    return registry


@pytest.fixture
def mock_registry(fresh_registry: IndexerRegistry, monkeypatch: pytest.MonkeyPatch) -> IndexerRegistry:
    """Patch get_registry to return the fresh registry."""
    monkeypatch.setattr("environment_indexers.cli.get_registry", lambda: fresh_registry)
    return fresh_registry


class TestListIndexers:
    """Tests for --list functionality (R1.2)."""

    def test_list_empty(self, mock_registry: IndexerRegistry) -> None:
        """Listing with no indexers shows empty message."""
        args = argparse.Namespace(json=False)
        stdout = StringIO()
        with patch("sys.stdout", stdout):
            code = list_indexers(args)
        assert code == 0
        assert "No indexers registered" in stdout.getvalue()

    def test_list_with_indexers(
        self,
        mock_registry: IndexerRegistry,
    ) -> None:
        """Listing shows each indexer's name and description."""
        @mock_registry.register("fs_tree", "Walk filesystem and emit nodes")
        def fs_tree(path: str) -> None:
            pass

        @mock_registry.register("py_deps", "Index Python dependencies", tags=["python"])
        def py_deps(path: str) -> None:
            pass

        args = argparse.Namespace(json=False)
        stdout = StringIO()
        with patch("sys.stdout", stdout):
            code = list_indexers(args)
        assert code == 0
        output = stdout.getvalue()
        assert "fs_tree" in output
        assert "Walk filesystem" in output
        assert "py_deps" in output
        assert "python" in output

    def test_list_json_format(
        self,
        mock_registry: IndexerRegistry,
    ) -> None:
        """--json outputs machine-readable format."""
        @mock_registry.register("test_idx", "A test indexer")
        def test_idx(path: str) -> None:
            pass

        args = argparse.Namespace(json=True)
        stdout = StringIO()
        with patch("sys.stdout", stdout):
            code = list_indexers(args)
        assert code == 0
        data = json.loads(stdout.getvalue())
        assert len(data) == 1
        assert data[0]["name"] == "test_idx"
        assert data[0]["description"] == "A test indexer"


class TestRunIndexer:
    """Tests for indexer invocation (R1.1, R1.3, R1.4)."""

    def test_unknown_indexer_returns_error(
        self,
        mock_registry: IndexerRegistry,
    ) -> None:
        """Unknown indexer name produces structured error (R1.3)."""
        args = argparse.Namespace(name="nonexistent", path="/tmp")
        stderr = StringIO()
        with patch("sys.stderr", stderr):
            code = run_indexer(args)
        assert code == 1
        error_output = stderr.getvalue()
        assert "nonexistent" in error_output
        assert "Unknown indexer" in error_output
        assert "--list" in error_output

    def test_runs_only_specified_indexer(
        self,
        mock_registry: IndexerRegistry,
    ) -> None:
        """Only the named indexer is executed (R1.1)."""
        call_order: list[str] = []

        @mock_registry.register("first", "First indexer")
        def first(path: str) -> None:
            call_order.append("first")

        @mock_registry.register("second", "Second indexer")
        def second(path: str) -> None:
            call_order.append("second")

        with TemporaryDirectory() as tmpdir:
            args = argparse.Namespace(name="first", path=tmpdir)
            code = run_indexer(args)

        assert code == 0
        assert call_order == ["first"]

    def test_failure_returns_nonzero(
        self,
        mock_registry: IndexerRegistry,
    ) -> None:
        """Indexer failure exits non-zero (R1.4)."""
        @mock_registry.register("failing", "Always fails")
        def failing(path: str) -> None:
            raise IndexerExecutionError("failing", "deliberate test failure")

        with TemporaryDirectory() as tmpdir:
            args = argparse.Namespace(name="failing", path=tmpdir)
            stderr = StringIO()
            with patch("sys.stderr", stderr):
                code = run_indexer(args)

        assert code == 1
        assert "failing" in stderr.getvalue()
        assert "deliberate test failure" in stderr.getvalue()

    def test_unexpected_error_returns_nonzero(
        self,
        mock_registry: IndexerRegistry,
    ) -> None:
        """Unexpected exceptions exit non-zero (R1.4)."""
        @mock_registry.register("crash", "Crashes unexpectedly")
        def crash(path: str) -> None:
            raise RuntimeError("unexpected error")

        with TemporaryDirectory() as tmpdir:
            args = argparse.Namespace(name="crash", path=tmpdir)
            stderr = StringIO()
            with patch("sys.stderr", stderr):
                code = run_indexer(args)

        assert code == 1
        assert "crash" in stderr.getvalue()
        assert "unexpected" in stderr.getvalue()


class TestCliIntegration:
    """Integration tests for the full CLI entry point."""

    def test_list_command(self, mock_registry: IndexerRegistry) -> None:
        """CLI --list works end-to-end."""
        from environment_indexers.cli import main

        @mock_registry.register("integration_test", "Test indexer")
        def integration_test(path: str) -> None:
            pass

        stdout = StringIO()
        with patch("sys.stdout", stdout):
            code = main(["--list"])
        assert code == 0
        assert "integration_test" in stdout.getvalue()

    def test_run_command(self, mock_registry: IndexerRegistry) -> None:
        """CLI run works end-to-end."""
        from environment_indexers.cli import main

        executed = []

        @mock_registry.register("exec_test", "Execution test")
        def exec_test(path: str) -> None:
            executed.append(path)

        with TemporaryDirectory() as tmpdir:
            code = main(["run", "exec_test", tmpdir])

        assert code == 0
        assert len(executed) == 1
        assert executed[0] == tmpdir

    def test_run_unknown_exits_nonzero(self, mock_registry: IndexerRegistry) -> None:
        """CLI run with unknown indexer exits 1."""
        from environment_indexers.cli import main

        stderr = StringIO()
        with patch("sys.stderr", stderr):
            code = main(["run", "does_not_exist", "/tmp"])

        assert code == 1
