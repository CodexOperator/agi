"""Filesystem Tree Indexer.

Implements environment-indexers/R2 (T-033).

Walks a directory tree and emits one node per directory and one node per file
into the graph. Nodes are written as `.md` files under `nodes/<type>/`.

Acceptance Criteria (R2):
- R2.1: One node per dir + child node per file/subdir
- R2.2: Frontmatter conforms to the [filesystem_tree] schema
- R2.3: Symlinks and unreadable entries skipped with per-entry warning; run continues
- R2.4: Re-running yields same ids and same parent-child links (deterministic walk)
"""

from __future__ import annotations

import os
import sys
import warnings
from pathlib import Path
from typing import TextIO

_SRC = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(_SRC))

try:
    from graph_core.identity import IdRegistry
    from graph_core.paths import set_project_root
    from graph_core.persistence.frontmatter import NodeFile, save_node_file
except ImportError as e:
    raise ImportError(
        "filesystem_tree indexer requires graph-core: ensure "
        "src/graph_core is on PYTHONPATH"
    ) from e

# Where nodes are written (relative to project root / cwd)
NODES_DIR = "nodes"
SCHEMA_NAME = "filesystem_tree"
_TYPE_PREFIX_DIR = "fs-dir"
_TYPE_PREFIX_FILE = "fs-file"


def _resolve_relative(abs_path: Path, root: Path) -> Path:
    """Return path relative to root. For root itself returns Path('.')"""
    if abs_path == root:
        return Path(".")
    return abs_path.relative_to(root)


def _write_node(
    node_id: str,
    node_type: str,
    root: Path,
    abs_path: Path,
    rel_path: Path,
    size_bytes: int | None,
    *,
    skipped: bool = False,
    skipped_reason: str | None = None,
    parent_ids: list[str],
    warn_stream: TextIO | None = None,
) -> None:
    """Write a filesystem-tree node to disk.

    Args:
        node_id: Stable id for this node.
        node_type: 'directory' or 'file'.
        root: The indexed root (used for relative path computation).
        abs_path: Absolute path of this entry.
        rel_path: Relative path from root.
        size_bytes: Byte size (0 or None for directories).
        skipped: If True, this entry was skipped.
        skipped_reason: Human-readable reason for skipping.
        parent_ids: List of parent node ids.
        warn_stream: Where to write per-entry warnings (default: sys.stderr).
    """
    if skipped:
        if skipped_reason:
            msg = f"SKIP: {abs_path} ({skipped_reason})"
            print(msg, file=warn_stream or sys.stderr)
        return

    fm: dict[str, object] = {
        "id": node_id,
        "type": "node",
        "title": rel_path.name if str(rel_path) != "." else str(rel_path),
        "tags": [node_type, "indexed", "filesystem-tree"],
        "schema": SCHEMA_NAME,
        "fields": {
            "node_type": node_type,
            "absolute_path": str(abs_path.resolve()),
            "relative_path": str(rel_path),
        },
    }
    if size_bytes is not None:
        fm["fields"]["size_bytes"] = size_bytes
    if parent_ids:
        fm["parents"] = parent_ids

    nf = NodeFile(frontmatter=fm, body="", suffix=".md")

    # Write to nodes/<node_id>.md (id colons replaced with hyphens)
    safe_id = node_id.replace(":", "-")
    out_path = Path(NODES_DIR) / f"{safe_id}.md"
    save_node_file(out_path, nf)


def _walk(root: Path):
    """Sorted top-down walk yielding (dir_abs, [sorted_files]).

    os.walk with topdown=True already visits each directory once.
    We sort each level for deterministic ordering (R2.4).
    """
    for dir_abs, subdirs, files in os.walk(root):
        subdirs.sort()
        files.sort()
        yield Path(dir_abs), sorted(files)


def index_filesystem(
    root: str | Path,
    *,
    warn_stream: TextIO | None = None,
) -> list[str]:
    """Index a filesystem tree and emit nodes into the graph.

    Args:
        root: Root directory to index.
        warn_stream: Stream for per-entry warnings (default: sys.stderr).

    Returns:
        List of emitted node ids (excludes skipped entries).

    Raises:
        FileNotFoundError: If root does not exist.
        NotADirectoryError: If root is not a directory.
    """
    root = Path(root).resolve()
    if not root.exists():
        raise FileNotFoundError(f"Path does not exist: {root}")
    if not root.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {root}")

    # Ensure project root is set so path validation works
    project_root = Path(__file__).parent.parent.parent
    set_project_root(project_root)

    registry = IdRegistry()
    emitted: list[str] = []

    for dir_abs, files in _walk(root):
        # Emit the directory node (one node per directory — R2.1)
        dir_rel = _resolve_relative(dir_abs, root)
        dir_id = registry.mint(_TYPE_PREFIX_DIR, str(dir_rel))
        _write_node(
            dir_id,
            "directory",
            root,
            dir_abs,
            dir_rel,
            size_bytes=0,
            parent_ids=[],  # root has no parent; subdirs have parents set via parent's iteration
            warn_stream=warn_stream,
        )
        emitted.append(dir_id)

        # For files in this dir, use this dir as parent
        parent_ids_for_files = [dir_id]

        for fname in files:
            f_abs = dir_abs / fname
            try:
                if f_abs.is_symlink():
                    _write_node(
                        "",
                        "file",
                        root,
                        f_abs,
                        f_abs.relative_to(root),
                        skipped=True,
                        skipped_reason="symlink",
                        parent_ids=parent_ids_for_files,
                        warn_stream=warn_stream,
                    )
                    continue

                f_stat = f_abs.stat()
                f_rel = f_abs.relative_to(root)
                file_id = registry.mint(_TYPE_PREFIX_FILE, str(f_rel))

                _write_node(
                    file_id,
                    "file",
                    root,
                    f_abs,
                    f_rel,
                    size_bytes=f_stat.st_size,
                    parent_ids=parent_ids_for_files,
                    warn_stream=warn_stream,
                )
                emitted.append(file_id)

            except PermissionError as e:
                msg = f"SKIP: {f_abs} (permission denied)"
                print(msg, file=warn_stream or sys.stderr)
            except OSError as e:
                msg = f"SKIP: {f_abs} ({type(e).__name__}: {e})"
                print(msg, file=warn_stream or sys.stderr)

    return emitted


# ---------------------------------------------------------------------------
# Registry integration
# ---------------------------------------------------------------------------

from environment_indexers.registry import register_indexer  # noqa: E402


@register_indexer(
    "fs_tree",
    "Walk a filesystem and emit directory/file nodes into the graph",
    tags=["filesystem", "tree", "walk"],
)
def fs_tree_indexer(path: str) -> None:
    """Entry point registered with the indexer registry.

    Args:
        path: Root directory to index.

    Raises:
        IndexerExecutionError: On failure to emit nodes.
    """
    from environment_indexers.errors import IndexerExecutionError

    try:
        emitted = index_filesystem(path)
    except Exception as e:
        raise IndexerExecutionError("fs_tree", str(e)) from e

    if not emitted:
        warnings.warn(
            "fs_tree indexer emitted no nodes; check that the target path is valid",
            UserWarning,
        )
