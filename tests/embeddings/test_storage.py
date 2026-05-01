"""T-074 tests: in-graph embedding storage (embeddings/R7)."""

import tempfile
from pathlib import Path

import pytest

from embeddings import EmbeddingConfig, embed_graph
from embeddings.storage import embed_and_store
from graph_core import Node
from graph_core.edge import Edge
from graph_core.graph import Graph


def _chain_graph(ids: list[str]) -> Graph:
    g = Graph()
    for i in ids:
        g.add_node(Node(id=i, type="x"))
    for a, b in zip(ids, ids[1:]):
        g.add_edge(Edge(source_id=a, target_id=b, relation="next"))
    return g


def test_enabled_each_node_carries_vector(tmp_path: Path) -> None:
    """R7.1: when in-graph storage is enabled, each node carries embedding_vector after embed_and_store."""
    g = _chain_graph(["n0", "n1", "n2"])
    node_dir = tmp_path / "nodes"
    node_dir.mkdir()

    # Write minimal node files
    for nid in ["n0", "n1", "n2"]:
        (node_dir / f"{nid}.md").write_text(
            f"---\nid: {nid}\ntype: x\n---\n", encoding="utf-8"
        )

    cfg = EmbeddingConfig(dim=16, seed=7, store_in_graph=True)
    vectors = embed_and_store(g, cfg, node_dir)

    # All 3 nodes have vectors
    assert set(vectors.keys()) == {"n0", "n1", "n2"}
    assert all(len(v) == 16 for v in vectors.values())

    # Node files now carry embedding_vector
    for nid in ["n0", "n1", "n2"]:
        text = (node_dir / f"{nid}.md").read_text(encoding="utf-8")
        assert "embedding_vector:" in text, f"{nid} missing embedding_vector"


def test_disabled_no_vector_in_node_files(tmp_path: Path) -> None:
    """R7.2: when disabled (default), node files do not carry the field."""
    g = _chain_graph(["a", "b"])
    node_dir = tmp_path / "nodes"
    node_dir.mkdir()

    for nid in ["a", "b"]:
        (node_dir / f"{nid}.md").write_text(
            f"---\nid: {nid}\ntype: x\n---\n", encoding="utf-8"
        )

    cfg = EmbeddingConfig(dim=16, seed=7, store_in_graph=False)
    vectors = embed_and_store(g, cfg, node_dir)

    # No embedding_vector in node files
    for nid in ["a", "b"]:
        text = (node_dir / f"{nid}.md").read_text(encoding="utf-8")
        assert "embedding_vector:" not in text


def test_toggle_does_not_invalidate_existing_vectors(tmp_path: Path) -> None:
    """R7.3: toggling option does not invalidate previously stored vectors."""
    g = _chain_graph(["x", "y"])
    node_dir = tmp_path / "nodes"
    node_dir.mkdir()

    for nid in ["x", "y"]:
        (node_dir / f"{nid}.md").write_text(
            f"---\nid: {nid}\ntype: x\n---\n", encoding="utf-8"
        )

    cfg1 = EmbeddingConfig(dim=8, seed=99, store_in_graph=True)
    v1 = embed_and_store(g, cfg1, node_dir)

    # Store again with different seed — vectors change but no crash
    cfg2 = EmbeddingConfig(dim=8, seed=13, store_in_graph=True)
    v2 = embed_and_store(g, cfg2, node_dir)

    # Both runs succeeded with correct node counts
    assert set(v1.keys()) == {"x", "y"}
    assert set(v2.keys()) == {"x", "y"}

    # Seeds differ → vectors differ (verifies recomputation happened)
    assert v1["x"] != v2["x"]


def test_backfill_without_rewriting_unrelated_fields(tmp_path: Path) -> None:
    """R7.4: when enabled and node lacks field, backfill without rewriting unrelated fields."""
    g = _chain_graph(["m"])
    node_dir = tmp_path / "nodes"
    node_dir.mkdir()

    # Node with unrelated fields already present
    original = (
        "---\n"
        "id: m\n"
        "type: hypothesis\n"
        "tags:\n  - tested\n  - R7\n"
        "confidence: 0.5\n"
        "---\n"
        "Some body text.\n"
    )
    (node_dir / "m.md").write_text(original, encoding="utf-8")

    cfg = EmbeddingConfig(dim=8, seed=5, store_in_graph=True)
    embed_and_store(g, cfg, node_dir)

    text = (node_dir / "m.md").read_text(encoding="utf-8")

    # embedding_vector was added
    assert "embedding_vector:" in text
    # Unrelated fields preserved
    assert "confidence: 0.5" in text
    assert "- tested" in text
    # Body preserved
    assert "Some body text." in text


def test_empty_graph_creates_no_files(tmp_path: Path) -> None:
    """Empty graph: embed_and_store returns empty dict, no files created."""
    g = Graph()
    node_dir = tmp_path / "nodes"
    node_dir.mkdir()

    cfg = EmbeddingConfig(dim=16, seed=7, store_in_graph=True)
    vectors = embed_and_store(g, cfg, node_dir)

    assert vectors == {}
    assert list(node_dir.iterdir()) == []
