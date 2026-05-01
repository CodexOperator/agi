"""Unit tests for Edge primitive (T-003 / R2.2, R2.3)."""
from __future__ import annotations

import pytest

from graph_core.edge import Edge


class TestEdgeFields:
    """R2.2: edge exposes source_id, target_id, relation, optional tags."""

    def test_fields_accessible(self):
        e = Edge("a", "b", "links")
        assert e.source_id == "a"
        assert e.target_id == "b"
        assert e.relation == "links"
        assert e.tags == set()

    def test_tags_default_empty(self):
        e = Edge("x", "y", "owns")
        assert e.tags == set()

    def test_tags_custom(self):
        e = Edge("x", "y", "owns", tags={"auto", "nfa"})
        assert e.tags == {"auto", "nfa"}

    def test_triple_property(self):
        e = Edge("s", "t", "rel")
        assert e.triple == ("s", "t", "rel")


class TestEdgeEqualityAndHash:
    """R2.3: idempotent insert for same (source, target, relation) triple."""

    def test_equal_same_triple(self):
        e1 = Edge("a", "b", "links")
        e2 = Edge("a", "b", "links")
        assert e1 == e2

    def test_not_equal_different_source(self):
        e1 = Edge("a", "b", "links")
        e2 = Edge("x", "b", "links")
        assert e1 != e2

    def test_not_equal_different_target(self):
        e1 = Edge("a", "b", "links")
        e2 = Edge("a", "x", "links")
        assert e1 != e2

    def test_not_equal_different_relation(self):
        e1 = Edge("a", "b", "links")
        e2 = Edge("a", "b", "owns")
        assert e1 != e2

    def test_different_tags_same_triple_equal(self):
        """Tags are out-of-band; don't affect identity."""
        e1 = Edge("a", "b", "links", tags={"auto"})
        e2 = Edge("a", "b", "links", tags={"manual"})
        assert e1 == e2

    def test_hash_same_triple(self):
        e1 = Edge("a", "b", "links")
        e2 = Edge("a", "b", "links")
        assert hash(e1) == hash(e2)

    def test_different_tags_same_triple_same_hash(self):
        e1 = Edge("a", "b", "links", tags={"auto"})
        e2 = Edge("a", "b", "links", tags={"manual"})
        assert hash(e1) == hash(e2)


class TestEdgeDeduplication:
    """R2.3: set of edges deduplicates same-triple inserts."""

    def test_set_deduplicates_same_triple(self):
        edges = {
            Edge("s", "t", "depends_on"),
            Edge("s", "t", "depends_on"),  # duplicate
        }
        assert len(edges) == 1

    def test_set_different_triples_unique(self):
        edges = {
            Edge("a", "b", "x"),
            Edge("a", "b", "y"),
            Edge("b", "a", "x"),
        }
        assert len(edges) == 3
