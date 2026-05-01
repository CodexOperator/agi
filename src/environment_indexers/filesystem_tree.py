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
from typing import Iterator, TextIO

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

# Where nodes are written (relative to project root)
NODES_DIR = "nodes"

# Schema name for emitted nodes
SCHEMA_NAME = "filesystem_tree"

# Type prefix for minted ids
_TYPE_PREFIX_DIR = "fs-dir"
_TYPE_PREFIX_FILE = "fs-file"


def _file_node_id(root: Path, file_path: Path, registry: IdRegistry) -> str:
    rel = file_path.resolve().relative_to(root.resolve())
    return registry.mint(_TYPE_PREFIX_FILE, str(rel))


def _dir_node_id(root: Path, dir_path: Path, registry: IdRegistry) -> str:
    rel = dir_path.resolve().relative_to(root.resolve())
    return registry.mint(_TYPE_PREFIX_DIR, str(rel))


def _write_node(
    node_id: str,
    node_type: str,
    root: Path,
    abs_path: Path,
    rel_path: Path,
    size_bytes: int | None = None,
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
    if skipped and skipped_reason:
        msg = f"SKIP: {abs_path} ({skipped_reason})"
        print(msg, file=warn_stream or sys.stderr)
        return

    fm: dict[str, object] = {
        "id": node_id,
        "type": "node",  # generic node type; schema is [filesystem_tree]
        "title": rel_path.name or str(rel_path),
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

    # Determine write location: nodes/<type>/<id>.md
    type_dir = NODES_DIR
    out_path = Path(type_dir) / f"{node_id.replace(':', '-')}.md"
    # Write relative to project root
    save_node_file(out_path, nf)


def walk_sorted(root: Path) -> Iterator[tuple[Path, list[str]]]:
    """Walk root top-down, yielding (dir_path, [sorted subdirs, sorted files]).

    Uses os.walk with topdown=True but sorts entries within each level for
    deterministic ordering required by R2.4.
    """
    # os.walk already yields top-down; we sort each level
    for dir_path, subdirs, files in os.walk(root):
        subdirs.sort()
        files.sort()
        yield Path(dir_path), sorted(files)


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
        List of emitted node ids.

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
    root_rel = Path(".")  # root is always "."

    # Emit root directory node
    root_id = _dir_node_id(root, root, registry)
    _write_node(
        root_id,
        "directory",
        root,
        root,
        root_rel,
        size_bytes=0,
        parent_ids=[],
        warn_stream=warn_stream,
    )
    emitted.append(root_id)

    for dir_path, files in walk_sorted(root):
        dir_rel = dir_path.relative_to(root) if dir_path != root else root_rel
        dir_id = _dir_node_id(root, dir_path, registry)

        # Emit child nodes for each subdirectory
        subdirs_found = sorted(d for d in dir_path.iterdir() if d.is_dir() and not d.is_symlink())
        for subdir in subdirs_found:
            try:
                subdir_resolved = subdir.resolve()
                subdir_rel = subdir_resolved.relative_to(root)
                subdir_id = _dir_node_id(root, subdir_resolved, subdir_rel)
                _write_node(
                    subdir_id,
                    "directory",
                    root,
                    subdir_resolved,
                    subdir_rel,
                    size_bytes=0,
                    parent_ids=[dir_id],
                    warn_stream=warn_stream,
                )
                emitted.append(subdir_id)
            except PermissionError as e:
                _write_node(
                    "",
                    "directory",
                    root,
                    subdir,
                    Path(""),
                    skipped=True,
                    skipped_reason=f"permission denied: {e}",
                    parent_ids=[dir_id],
                    warn_stream=warn_stream,
                )
            except Exception as e:
                msg = f"SKIP: {subdir} ({type(e).__name__}: {e})"
                print(msg, file=warn_stream or sys.stderr)

        # Emit child nodes for each file
        for fname in files:
            fpath = dir_path / fname
            try:
                fpath_resolved = fpath.resolve()
                if fpath.is_symlink():
                    _write_node(
                        "",
                        "file",
                        root,
                        fpath,
                        fpath_resolved.relative_to(root),
                        skipped=True,
                        skipped_reason="symlink",
                        parent_ids=[dir_id],
                        warn_stream=warn_stream,
                    )
                    continue
                fpath_stat = fpath.stat()
                frel = fpath_resolved.relative_to(root)
                file_id = _file_node_id(root, fpath_resolved, registry)
                _write_node(
                    file_id,
                    "file",
                    root,
                    fpath_resolved,
                    frel,
                    size_bytes=fpath_stat.st_size,
                    parent_ids=[dir_id],
                    warn_stream=warn_stream,
                )
                emitted.append(file_id)
            except PermissionError as e:
                msg = f"SKIP: {fpath} (permission denied: {e})"
                print(msg, file=warn_stream or sys.stderr)
            except OSError as e:
                msg = f"SKIP: {fpath} ({type(e).__name__}: {e})"
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
