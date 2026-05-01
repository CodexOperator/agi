"""T-016 tests: path safety enforcement (graph-core R11)."""

import shutil
import tempfile
from pathlib import Path

import pytest

from graph_core import (
    PathOutsideProjectError,
    PathValidator,
    get_validator,
    safe_cache_path,
    safe_path,
    safe_relative_path,
    set_project_root,
)


class TestPathValidator:
    """Tests for PathValidator class."""

    def test_validate_inside_project(self, tmp_path: Path) -> None:
        """R11.1: paths inside project root are accepted."""
        v = PathValidator(tmp_path)
        inner = tmp_path / "context" / "nodes" / "test.md"
        inner.parent.mkdir(parents=True)
        inner.write_text("test")
        result = v.validate(inner)
        assert result == inner.resolve()

    def test_validate_outside_project_raises(self, tmp_path: Path) -> None:
        """R11.1: paths outside project root raise PathOutsideProjectError."""
        v = PathValidator(tmp_path)
        outside = tmp_path.parent / "outside.md"
        with pytest.raises(PathOutsideProjectError) as exc_info:
            v.validate(outside)
        assert "outside.md" in str(exc_info.value)
        assert str(tmp_path) in str(exc_info.value)

    def test_validate_relative_inside(self, tmp_path: Path) -> None:
        """R11.3: relative paths inside project are accepted."""
        v = PathValidator(tmp_path)
        result = v.validate_relative("context/nodes/test.md")
        expected = (tmp_path / "context" / "nodes" / "test.md").resolve()
        assert result == expected

    def test_validate_relative_absolute_raises(self, tmp_path: Path) -> None:
        """R11.3: absolute paths raise PathOutsideProjectError."""
        v = PathValidator(tmp_path)
        with pytest.raises(PathOutsideProjectError):
            v.validate_relative("/absolute/path")

    def test_validate_relative_escape_raises(self, tmp_path: Path) -> None:
        """R11.3: paths with .. escaping project root raise error."""
        v = PathValidator(tmp_path)
        with pytest.raises(PathOutsideProjectError):
            v.validate_relative("../escape.md")

    def test_cache_dir_under_context(self, tmp_path: Path) -> None:
        """R11.2: cache_dir is under project_root/context/ subdir."""
        v = PathValidator(tmp_path)
        cache = v.cache_dir("graph")
        # cache = project_root/context/graph
        # cache.parent = project_root/context
        assert cache.parent == tmp_path / "context"
        assert cache.parent.name == "context"
        assert cache.name == "graph"
        assert cache.exists()

    def test_cache_dir_default_subdir(self, tmp_path: Path) -> None:
        """R11.2: default cache subdir is .cache."""
        v = PathValidator(tmp_path)
        cache = v.cache_dir()
        assert cache == tmp_path / "context" / ".cache"

    def test_context_dir_creates_if_missing(self, tmp_path: Path) -> None:
        """Context directory is created if it doesn't exist."""
        v = PathValidator(tmp_path)
        ctx = v.context_dir()
        assert ctx == tmp_path / "context"
        assert ctx.exists()

    def test_project_root_resolved(self, tmp_path: Path) -> None:
        """Project root is resolved to absolute path."""
        v = PathValidator(".")
        # Should resolve to current working directory
        assert v.project_root.is_absolute()


class TestModuleLevelFunctions:
    """Tests for module-level convenience functions."""

    def test_set_and_get_validator(self, tmp_path: Path) -> None:
        """Validator can be set and retrieved."""
        v1 = set_project_root(tmp_path)
        v2 = get_validator()
        assert v1 is v2
        assert v2.project_root == tmp_path.resolve()

    def test_get_validator_without_set_raises(self) -> None:
        """Getting validator without setting raises error."""
        # Reset global state
        import graph_core.paths as paths_mod

        old_validator = paths_mod._validator
        paths_mod._validator = None
        try:
            from graph_core.errors import GraphCoreError

            with pytest.raises(GraphCoreError, match="no project root set"):
                get_validator()
        finally:
            paths_mod._validator = old_validator

    def test_safe_path_validates(self, tmp_path: Path) -> None:
        """safe_path validates using current validator."""
        set_project_root(tmp_path)
        valid = tmp_path / "test.md"
        valid.write_text("test")
        result = safe_path(valid)
        assert result == valid.resolve()

    def test_safe_path_rejects_outside(self, tmp_path: Path) -> None:
        """safe_path rejects paths outside project."""
        set_project_root(tmp_path)
        with pytest.raises(PathOutsideProjectError):
            safe_path("/etc/passwd")

    def test_safe_relative_path_validates(self, tmp_path: Path) -> None:
        """safe_relative_path validates relative paths."""
        set_project_root(tmp_path)
        result = safe_relative_path("context/test.md")
        assert result == (tmp_path / "context" / "test.md").resolve()

    def test_safe_cache_path_creates_under_context(self, tmp_path: Path) -> None:
        """safe_cache_path creates cache file under context/."""
        set_project_root(tmp_path)
        cache_file = safe_cache_path("graph.digest", "graph")
        assert cache_file.parent == tmp_path / "context" / "graph"
        assert cache_file.name == "graph.digest"

    def test_safe_cache_path_rejects_absolute_filename(self, tmp_path: Path) -> None:
        """safe_cache_path rejects absolute path in filename."""
        set_project_root(tmp_path)
        with pytest.raises(PathOutsideProjectError):
            safe_cache_path("/etc/malicious", "graph")

    def test_safe_cache_path_rejects_escape(self, tmp_path: Path) -> None:
        """safe_cache_path rejects .. in filename."""
        set_project_root(tmp_path)
        with pytest.raises(PathOutsideProjectError):
            safe_cache_path("../escape", "graph")


class TestPortabilitySelfTest:
    """R9.4: self-test verifies context directory is relocatable."""

    def test_context_copy_is_loadable(self, tmp_path: Path) -> None:
        """Copying context dir to temp and loading produces same nodes."""
        # Create a minimal context
        src_context = tmp_path / "context"
        src_nodes = src_context / "nodes"
        src_nodes.mkdir(parents=True)

        # Create test node
        node_file = src_nodes / "test-node.md"
        node_file.write_text(
            "---\nid: test:node-1\ntype: test\n---\n\nTest body content.\n"
        )

        # Copy to temp
        tmp_copy = Path(tempfile.mkdtemp())
        try:
            dest = tmp_copy / "context"
            shutil.copytree(src_context, dest)

            # Load from both
            from graph_core.loader import load_directory

            graph1, nodes1 = load_directory(src_context)
            graph2, nodes2 = load_directory(dest)

            # Compare
            assert graph1.node_ids == graph2.node_ids
            assert len(nodes1) == len(nodes2)
            assert {n.node.id for n in nodes1} == {n.node.id for n in nodes2}
        finally:
            shutil.rmtree(tmp_copy, ignore_errors=True)

    def test_cache_dir_lives_under_context(self, tmp_path: Path) -> None:
        """Cache directory is always under context/."""
        v = PathValidator(tmp_path)
        cache = v.cache_dir("graph")
        # Cache must be under context
        assert cache.relative_to(tmp_path / "context").parts[0] == "graph"
        # Cache must be under project root
        cache.relative_to(tmp_path)
