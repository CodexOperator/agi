"""Tests for chain-engine/R10: Weighted Attractiveness Produces Measurable Selection Differences.

This test file backs experiment: exp:chain-engine-weighted-attractiveness-variance-e1.
It validates that the attractiveness function (R6) creates meaningful differentiation
in chain rankings when weight configurations vary.

Acceptance criteria validated:
- R10.1: Different weight configs produce different top-1 chains ≥60% of the time
- R10.2: Score variance across weight configs is > 0.0 for non-trivial graphs
- R10.3: All-zero weights return 0.0 for all chains (R6.3)
- R10.4: Equal weight vectors produce identical rankings (idempotence)
"""

from __future__ import annotations

import itertools
import math
import time

import pytest

from chain_engine.attractiveness import (
    AttractivenessWeights,
    attractiveness,
    score_all_chains,
)
from chain_engine.ranking import longest_n, rank_chains
from graph_core.edge import Edge
from graph_core.graph import Graph
from graph_core.node import Node


def _make_node(node_id: str, node_type: str, last_edited: float = 0.0) -> Node:
    """Helper: create a node with optional last_edited attribute."""
    node = Node(id=node_id, type=node_type)
    # Monkey-patch last_edited for recency testing
    object.__setattr__(node, "last_edited", last_edited)
    return node


def _add_chain(
    graph: Graph,
    chain_ids: list[str],
    node_types: list[str],
    last_edited: float = 0.0,
) -> None:
    """Add a complete chain with 'next' edges between consecutive nodes."""
    for nid, ntype in zip(chain_ids, node_types):
        graph.add_node(_make_node(nid, ntype, last_edited))
    for src, tgt in zip(chain_ids, chain_ids[1:]):
        graph.add_edge(Edge(source_id=src, target_id=tgt, relation="next"))


def _build_five_chain_fixture(now: float) -> tuple[Graph, list[list[str]]]:
    """Build a graph with 5 chains of varying properties for testing.

    Chain 0: short (8 nodes), old, depth=0 (independent root idea)
    Chain 1: long (9 nodes), old, depth=0 (independent root idea)
    Chain 2: medium (8 nodes), recent (delta=1h), depth=2 (shares prefix with chain 0)
    Chain 3: longest (11 nodes), very recent (delta=0.1h), depth=0 (independent root idea)
    Chain 4: medium (9 nodes), old, depth=2 (shares prefix with chain 1)

    The fork structure (chains 2 and 4 starting mid-chain) creates depth diversity:
    - Chain 0 and 2 share the same idea:a -> hyp:a1 prefix, but chain 2 is deeper
    - Chain 1 and 4 share the same idea:b -> hyp:b1 prefix, but chain 4 is deeper
    This ensures depth weights produce DIFFERENT scores across chains.
    """
    graph = Graph()

    # Chain 0 (independent, depth=0): idea:a -> hyp:a1 -> exp:a1 -> verdict:a1 -> mvp:a1 -> outcome:a1 -> bigger:a1 -> app:a
    # Chain 1 (independent, depth=0): idea:b -> hyp:b1 -> exp:b1 -> exp:b2 -> verdict:b1 -> mvp:b1 -> outcome:b1 -> bigger:b1 -> app:b
    # Chain 2 (fork from chain 0, depth=2): hyp:a2 -> exp:a2 -> verdict:a2 -> mvp:a2 -> outcome:a2 -> bigger:a2 -> app:c
    # Chain 3 (independent, depth=0): idea:d -> hyp:d1 -> exp:d1 -> exp:d2 -> exp:d3 -> verdict:d1 -> mvp:d1 -> mvp:d2 -> outcome:d1 -> bigger:d1 -> app:d
    # Chain 4 (fork from chain 1, depth=2): hyp:b2 -> exp:b3 -> verdict:b2 -> mvp:b3 -> mvp:b4 -> outcome:b2 -> bigger:b2 -> app:e

    chain_ids = [
        ["idea:a", "hyp:a1", "exp:a1", "verdict:a1", "mvp:a1", "outcome:a1", "bigger:a1", "app:a"],
        ["idea:b", "hyp:b1", "exp:b1", "exp:b2", "verdict:b1", "mvp:b1", "outcome:b1", "bigger:b1", "app:b"],
        ["hyp:a2", "exp:a2", "verdict:a2", "mvp:a2", "outcome:a2", "bigger:a2", "app:c"],
        ["idea:d", "hyp:d1", "exp:d1", "exp:d2", "exp:d3", "verdict:d1", "mvp:d1", "mvp:d2", "outcome:d1", "bigger:d1", "app:d"],
        ["hyp:b2", "exp:b3", "verdict:b2", "mvp:b3", "mvp:b4", "outcome:b2", "bigger:b2", "app:e"],
    ]
    node_types = [
        ["idea", "hypothesis", "experiment", "verdict", "mvp", "outcome", "bigger_outcome", "app_purpose"],
        ["idea", "hypothesis", "experiment", "experiment", "verdict", "mvp", "outcome", "bigger_outcome", "app_purpose"],
        ["hypothesis", "experiment", "verdict", "mvp", "outcome", "bigger_outcome", "app_purpose"],
        ["idea", "hypothesis", "experiment", "experiment", "experiment", "verdict", "mvp", "mvp", "outcome", "bigger_outcome", "app_purpose"],
        ["hypothesis", "experiment", "verdict", "mvp", "mvp", "outcome", "bigger_outcome", "app_purpose"],
    ]
    last_edit_times = [
        now - 100 * 3600,  # chain 0: very old
        now - 100 * 3600,  # chain 1: very old
        now - 1 * 3600,    # chain 2: recent (recency advantage)
        now - 0.1 * 3600,  # chain 3: very recent (recency advantage)
        now - 100 * 3600,  # chain 4: very old
    ]

    # Build independent chains (0, 1, 3)
    for ids, types, le in zip(
        [chain_ids[0], chain_ids[1], chain_ids[3]],
        [node_types[0], node_types[1], node_types[3]],
        [last_edit_times[0], last_edit_times[1], last_edit_times[3]],
    ):
        _add_chain(graph, ids, types, le)

    # Build shared-prefix fork structure:
    # chain 2 = hyp:a2 (fork from hyp:a1 -> exp:a1), depth=2 because hyp:a2 -> idea:a path has length 2
    # chain 4 = hyp:b2 (fork from hyp:b1 -> exp:b1), depth=2 because hyp:b2 -> idea:b path has length 2
    # First add the shared prefix (idea:a -> hyp:a1) and (idea:b -> hyp:b1)
    for nid, ntype, le in zip(chain_ids[2], node_types[2], [last_edit_times[2]] * len(chain_ids[2])):
        graph.add_node(_make_node(nid, ntype, le))
    for src, tgt in zip(chain_ids[2], chain_ids[2][1:]):
        graph.add_edge(Edge(source_id=src, target_id=tgt, relation="next"))

    for nid, ntype, le in zip(chain_ids[4], node_types[4], [last_edit_times[4]] * len(chain_ids[4])):
        graph.add_node(_make_node(nid, ntype, le))
    for src, tgt in zip(chain_ids[4], chain_ids[4][1:]):
        graph.add_edge(Edge(source_id=src, target_id=tgt, relation="next"))

    # Fork edges: hyp:a1 -> hyp:a2 and hyp:b1 -> hyp:b2
    graph.add_edge(Edge(source_id="hyp:a1", target_id="hyp:a2", relation="next"))
    graph.add_edge(Edge(source_id="hyp:b1", target_id="hyp:b2", relation="next"))

    return graph, chain_ids


class TestDiffRateAboveThreshold:
    """R10.1: Different weight configs produce different top-1 chains ≥60% of the time."""

    def test_diff_rate_above_threshold(self):
        """Run all pairs of weight configs with Δ≥0.3 in at least one component.

        Count how many pairs produce different top-1 chains. Rate must exceed 0.60.
        """
        now = time.time()
        graph, chains = _build_five_chain_fixture(now)

        # 10 distinct weight configurations
        configs = [
            AttractivenessWeights(length=1.0, depth=0.0, recency=0.0, mvp_count=0.0),
            AttractivenessWeights(length=0.0, depth=1.0, recency=0.0, mvp_count=0.0),
            AttractivenessWeights(length=0.0, depth=0.0, recency=1.0, mvp_count=0.0),
            AttractivenessWeights(length=0.0, depth=0.0, recency=0.0, mvp_count=1.0),
            AttractivenessWeights(length=0.5, depth=0.5, recency=0.0, mvp_count=0.0),
            AttractivenessWeights(length=1.0, depth=0.0, recency=1.0, mvp_count=0.0),
            AttractivenessWeights(length=0.5, depth=0.0, recency=0.0, mvp_count=1.0),
            AttractivenessWeights(length=1.0, depth=1.0, recency=1.0, mvp_count=1.0),
            AttractivenessWeights(length=0.25, depth=0.25, recency=0.25, mvp_count=0.25),
            AttractivenessWeights(length=2.0, depth=0.5, recency=0.5, mvp_count=0.5),
        ]

        pairs_differing = 0
        pairs_tested = 0

        for w1, w2 in itertools.combinations(configs, 2):
            if w1.weight_delta(w2) < 0.3:
                continue  # skip pairs that don't differ enough

            pairs_tested += 1

            ranked1 = rank_chains(chains, w1, graph, now)
            ranked2 = rank_chains(chains, w2, graph, now)

            top1_w1 = ranked1[0][0][0] if ranked1 else None
            top1_w2 = ranked2[0][0][0] if ranked2 else None

            if top1_w1 != top1_w2:
                pairs_differing += 1

        assert pairs_tested > 0, "No weight pairs with Δ≥0.3 — test configuration error"
        diff_rate = pairs_differing / pairs_tested
        assert diff_rate >= 0.60, f"diff_rate={diff_rate:.2f} below 0.60 threshold"


class TestScoreVarianceNonzero:
    """R10.2: Score variance across weight configs is > 0.0 for non-trivial graphs."""

    def test_score_variance_nonzero(self):
        """For each config, compute score stddev across chains. All configs must produce non-zero variance."""
        now = time.time()
        graph, chains = _build_five_chain_fixture(now)

        weight_configs = [
            AttractivenessWeights(length=1.0, depth=0.0, recency=0.0, mvp_count=0.0),
            AttractivenessWeights(length=0.0, depth=1.0, recency=0.0, mvp_count=0.0),
            AttractivenessWeights(length=0.0, depth=0.0, recency=1.0, mvp_count=0.0),
            AttractivenessWeights(length=0.0, depth=0.0, recency=0.0, mvp_count=1.0),
            AttractivenessWeights(length=0.5, depth=0.5, recency=0.5, mvp_count=0.5),
        ]

        for weights in weight_configs:
            scored = score_all_chains(chains, weights, now, graph)
            scores = [s for _, s in scored]
            mean = sum(scores) / len(scores)
            variance = sum((s - mean) ** 2 for s in scores) / len(scores)
            stddev = math.sqrt(variance)
            assert stddev > 0.0, f"Zero variance for weights {weights} — function is degenerate"

    def test_weight_sensitivity_length(self):
        """Length-dominant config ranks longer chains higher."""
        now = time.time()
        graph, chains = _build_five_chain_fixture(now)

        weights = AttractivenessWeights(length=1.0, depth=0.0, recency=0.0, mvp_count=0.0)
        ranked = rank_chains(chains, weights, graph, now)

        # Chain 3 is longest (11 nodes); chain 0 is shortest (8 nodes)
        chain_lengths = {c[0]: len(c) for c in chains}
        ranked_by_length = sorted(chain_lengths.items(), key=lambda x: -x[1])
        longest_chain_id = ranked_by_length[0][0]

        top1 = ranked[0][0][0]
        assert top1 == longest_chain_id, f"Expected longest chain {longest_chain_id} as top-1, got {top1}"


class TestAllZeroReturnsConstant:
    """R10.3 / R6.3: All-zero weights return 0.0 for every chain."""

    def test_all_zero_returns_zero(self):
        """All-zero weight vector returns 0.0 for all chains (the documented constant)."""
        now = time.time()
        graph, chains = _build_five_chain_fixture(now)

        zero_weights = AttractivenessWeights()
        scored = score_all_chains(chains, zero_weights, now, graph)

        assert all(score == 0.0 for _, score in scored), "All-zero weights must return 0.0 for all chains"
        assert len(scored) == len(chains), "All chains must be scored"


class TestEqualWeightsIdempotent:
    """R10.4: Equal weight vectors produce identical rankings (idempotence)."""

    def test_equal_weights_idempotent(self):
        """Two calls with identical weights produce identical rankings."""
        now = time.time()
        graph, chains = _build_five_chain_fixture(now)

        weights = AttractivenessWeights(length=0.7, depth=0.3, recency=1.0, mvp_count=0.5)

        ranked1 = rank_chains(chains, weights, graph, now)
        ranked2 = rank_chains(chains, weights, graph, now)

        assert ranked1 == ranked2, "Identical weight inputs must produce identical rankings"

    def test_longest_n_idempotent(self):
        """longest_n is idempotent across repeated calls."""
        now = time.time()
        graph, chains = _build_five_chain_fixture(now)

        weights = AttractivenessWeights(length=0.5, depth=0.5, recency=0.5, mvp_count=0.5)

        result1 = longest_n(chains, 3, weights, graph, now)
        result2 = longest_n(chains, 3, weights, graph, now)

        assert result1 == result2, "longest_n must be idempotent"


class TestR6Criteria:
    """Validate R6 acceptance criteria directly."""

    def test_r6_1_exactly_four_inputs(self):
        """R6.1: attractiveness() is computed from exactly four documented inputs."""
        from chain_engine.attractiveness import ChainMetrics

        # Verify ChainMetrics has exactly four fields
        fields = [f.name for f in ChainMetrics.__dataclass_fields__.values()]
        assert set(fields) == {"length", "depth", "recency", "mvp_count"}, (
            f"ChainMetrics must have exactly 4 fields; got {fields}"
        )

    def test_r6_3_all_zero_does_not_raise(self):
        """R6.3: all-zero weights → returns 0.0, never raises."""
        now = time.time()
        graph, chains = _build_five_chain_fixture(now)

        zero = AttractivenessWeights()
        for chain in chains:
            # Must not raise
            score = attractiveness(chain, zero, now, graph)
            assert score == 0.0

    def test_r6_4_identical_inputs_identical_outputs(self):
        """R6.4: identical inputs always produce identical scores (pure function)."""
        now = time.time()
        graph, chains = _build_five_chain_fixture(now)

        weights = AttractivenessWeights(length=0.3, depth=0.6, recency=0.9, mvp_count=1.2)
        chain = chains[0]

        score1 = attractiveness(chain, weights, now, graph)
        score2 = attractiveness(chain, weights, now, graph)
        assert score1 == score2, "Pure function: identical inputs → identical outputs"

        # Also across multiple chains
        all_scores = [attractiveness(c, weights, now, graph) for c in chains]
        all_scores_again = [attractiveness(c, weights, now, graph) for c in chains]
        assert all_scores == all_scores_again
