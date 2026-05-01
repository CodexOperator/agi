"""In-graph embedding storage (embeddings R7).

Optional persistence of per-node vectors back into node frontmatter files.
When ``store_in_graph=True``, each node file gets an ``embedding_vector`` key
in its frontmatter after embedding. When ``False`` (default), only the
in-memory vector dict is returned.

Acceptance criteria (embeddings/R7):
- R7.1: when enabled, each node carries embedding_vector after embed_and_store
- R7.2: when disabled (default), node files do not carry the field
- R7.3: toggling option does not invalidate previously stored vectors
- R7.4: backfill without rewriting unrelated frontmatter fields
"""

from __future__ import annotations

from pathlib import Path

import yaml

from .node2vec import EmbeddingConfig, embed_graph
from graph_core.graph import Graph  # noqa: F401 — used in type annotations only


def embed_and_store(
    graph: "Graph",
    config: EmbeddingConfig | None = None,
    node_dir: Path | str | None = None,
) -> dict[str, list[float]]:
    """Embed graph and optionally persist vectors to node files.

    Args:
        graph: the Graph to embed.
        config: EmbeddingConfig (must have store_in_graph=True to persist).
        node_dir: directory containing node .md files. Required when
            store_in_graph=True. Can be a Path or str.

    Returns:
        {node_id: vector} dict (always, regardless of store_in_graph setting).

    When config.store_in_graph is True and node_dir is provided, each node's
    frontmatter gets an ``embedding_vector`` key added. Existing fields are
    preserved. When False (default), node files are untouched.
    """
    cfg = config or EmbeddingConfig()
    vectors = embed_graph(graph, cfg)

    if not cfg.store_in_graph or node_dir is None:
        return vectors

    node_dir = Path(node_dir)
    if not node_dir.is_dir():
        return vectors

    # Build {node_id: path} map from node_dir
    id_to_path: dict[str, Path] = {}
    for p in node_dir.rglob("*.md"):
        try:
            text = p.read_text(encoding="utf-8")
            fm = _load_frontmatter(text)
            nid = fm.get("id")
            if nid and isinstance(nid, str):
                id_to_path[nid] = p
        except Exception:
            pass

    # Write embedding_vector to each node file that exists on disk
    for nid, vec in vectors.items():
        if nid not in id_to_path:
            continue
        p = id_to_path[nid]
        _update_node_file(p, nid, vec)

    return vectors


def _load_frontmatter(text: str) -> dict:
    """Parse YAML frontmatter from a .md node file."""
    lines = text.splitlines(keepends=False)
    if not lines or lines[0].strip() != "---":
        return {}
    close_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            close_idx = i
            break
    if close_idx is None:
        return {}
    yaml_text = "\n".join(lines[1:close_idx])
    return yaml.safe_load(yaml_text) or {}


def _update_node_file(path: Path, node_id: str, vector: list[float]) -> None:
    """Add/overwrite embedding_vector in a node's frontmatter, preserve rest."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=False)

    # Split into frontmatter, separator, body
    if not lines or lines[0].strip() != "---":
        return  # Malformed; skip

    close_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            close_idx = i
            break

    if close_idx is None:
        return  # Malformed; skip

    fm_lines = lines[1:close_idx]
    body_lines = lines[close_idx + 1:]
    # Strip leading blank line from body (common convention)
    if body_lines and body_lines[0] == "":
        body_lines = body_lines[1:]

    # Parse existing frontmatter
    yaml_text = "\n".join(fm_lines)
    fm = yaml.safe_load(yaml_text) or {}
    if not isinstance(fm, dict):
        fm = {}

    # Update embedding_vector — convert numpy/Python float types to native float for YAML serialization
    fm["embedding_vector"] = [float(x) for x in vector]

    # Re-emit frontmatter with sorted keys (consistent ordering)
    new_yaml = yaml.safe_dump(fm, sort_keys=True, default_flow_style=False).rstrip("\n")

    body = "\n".join(body_lines)
    if body:
        new_text = f"---\n{new_yaml}\n---\n\n{body}\n"
    else:
        new_text = f"---\n{new_yaml}\n---\n"

    path.write_text(new_text, encoding="utf-8", newline="\n")
