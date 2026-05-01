"""Tests for scatter renderer (embeddings R6).

R6 acceptance criteria:
- R6.1: registered through the same renderer plugin contract (render_scatter takes Representation)
- R6.2: places each node at its (x, y) without re-projecting
- R6.3: respects ASCII bounds (200 lines × 200 cols), degrades visibly
- R6.4: overlap marker when two nodes share the same character cell
"""

from __future__ import annotations

import sys
from pathlib import Path

# Allow tests to import from src
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))

from renderers.representation import Representation, RenderToken
from renderers.scatter import (
    MAX_COLS,
    MAX_LINES,
    OVERLAP_MARKER,
    EMPTY_MARKER,
    render_scatter,
    _short_label,
    _empty_scatter,
)


def _repr(*tokens: RenderToken) -> Representation:
    r = Representation()
    r.tokens = list(tokens)
    return r


def _token(id_: str, label: str, x: float, y: float) -> RenderToken:
    return RenderToken(id=id_, label=label, type="node", depth=0, x=x, y=y, edges=[])


# ---------------------------------------------------------------------------
# R6.1: plugin contract
# ---------------------------------------------------------------------------

def test_render_scatter_accepts_representation():
    """R6.1: render_scatter takes a Representation, no conversion shim needed."""
    r = _repr(_token("n1", "node-one", 0.0, 0.0))
    out = render_scatter(r)
    assert isinstance(out, str)


# ---------------------------------------------------------------------------
# R6.2: nodes placed at their own x,y without re-projecting
# ---------------------------------------------------------------------------

def test_single_node_at_origin():
    """R6.2: single node at (0,0) appears in output."""
    r = _repr(_token("n1", "alpha", 0.0, 0.0))
    out = render_scatter(r)
    lines = out.splitlines()
    # At least one line contains something other than empty marker
    non_empty = [l for l in lines if EMPTY_MARKER not in l or len(set(l)) > 1]
    assert len(non_empty) > 0


def test_two_nodes_at_distinct_positions():
    """R6.2: two distinct x,y positions produce two non-empty grid cells."""
    r = _repr(
        _token("n1", "alpha", 0.0, 0.0),
        _token("n2", "beta", 1.0, 1.0),
    )
    out = render_scatter(r)
    lines = out.splitlines()
    # Count cells that are not EMPTY_MARKER (not counting overflow footer lines)
    non_empty_count = 0
    for line in lines:
        if "... [" in line:
            continue
        for ch in line:
            if ch != EMPTY_MARKER:
                non_empty_count += 1
    # Should have at least 2 non-empty cells
    assert non_empty_count >= 2


def test_nodes_retain_their_x_y():
    """R6.2: coordinates are not re-projected — same tokens produce same output."""
    tokens = [
        _token("a", "alpha", 0.3, 0.7),
        _token("b", "beta", -0.2, 0.5),
        _token("c", "gamma", 0.9, -0.4),
    ]
    r1 = _repr(*tokens)
    r2 = _repr(*tokens)
    out1 = render_scatter(r1)
    out2 = render_scatter(r2)
    assert out1 == out2


# ---------------------------------------------------------------------------
# R6.3: respects bounds 200×200
# ---------------------------------------------------------------------------

def test_max_lines_respected():
    """R6.3: output has at most MAX_LINES lines."""
    r = _repr(*[_token(f"n{i}", f"n{i}", float(i) * 0.01, float(i) * 0.01) for i in range(50)])
    out = render_scatter(r)
    lines = out.splitlines()
    assert len(lines) <= MAX_LINES


def test_max_cols_respected():
    """R6.3: each output line has at most MAX_COLS characters."""
    r = _repr(*[_token(f"n{i}", f"n{i}", float(i) * 0.01, float(i) * 0.01) for i in range(50)])
    out = render_scatter(r)
    for line in out.splitlines():
        assert len(line) <= MAX_COLS


def test_wide_range_nodes_all_bounded():
    """R6.3: very wide x,y ranges are clamped to 200×200 grid."""
    r = _repr(
        _token("a", "alpha", -1000.0, -1000.0),
        _token("b", "beta", 1000.0, 1000.0),
        _token("c", "gamma", 0.0, 0.0),
    )
    out = render_scatter(r)
    lines = out.splitlines()
    assert len(lines) == MAX_LINES
    for line in lines:
        assert len(line) <= MAX_COLS


# ---------------------------------------------------------------------------
# R6.4: overlap marker
# ---------------------------------------------------------------------------

def test_overlap_marker_on_identical_coords():
    """R6.4: two nodes at identical x,y show overlap marker."""
    r = _repr(
        _token("n1", "alpha", 0.0, 0.0),
        _token("n2", "beta", 0.0, 0.0),
    )
    out = render_scatter(r)
    # The overlapping cell should contain OVERLAP_MARKER
    assert OVERLAP_MARKER in out


def test_three_way_overlap_marker():
    """R6.4: three nodes at same x,y show overlap marker."""
    r = _repr(
        _token("n1", "alpha", 0.5, 0.5),
        _token("n2", "beta", 0.5, 0.5),
        _token("n3", "gamma", 0.5, 0.5),
    )
    out = render_scatter(r)
    assert OVERLAP_MARKER in out


def test_no_overlap_marker_for_distinct_coords():
    """R6.4: distinct coords don't produce overlap marker."""
    r = _repr(
        _token("n1", "alpha", 0.0, 0.0),
        _token("n2", "beta", 0.1, 0.1),
        _token("n3", "gamma", -0.1, -0.1),
    )
    out = render_scatter(r)
    assert out.count(OVERLAP_MARKER) == 0


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_empty_representation():
    """Empty graph: returns bounded empty grid."""
    r = _repr()
    out = render_scatter(r)
    lines = out.splitlines()
    assert len(lines) == MAX_LINES
    for line in lines:
        assert len(line) <= MAX_COLS


def test_single_node():
    """Single node produces bounded output."""
    r = _repr(_token("n1", "alpha", 0.0, 0.0))
    out = render_scatter(r)
    lines = out.splitlines()
    assert len(lines) == MAX_LINES
    for line in lines:
        assert len(line) <= MAX_COLS


def test_short_label_truncation():
    """Long labels are truncated to 3 chars for cell width."""
    assert len(_short_label("verylonglabel", max_len=3)) <= 3
    assert _short_label("ab", max_len=3) == "ab"
    assert _short_label("", max_len=3) == EMPTY_MARKER


def test_id_based_label():
    """Labels with colons use last segment."""
    # "idea:domain-foo" → split → "domain-foo" → truncated to max_len=5 → "domai"
    assert _short_label("idea:domain-foo", max_len=5) == "domai"


def test_determinism():
    """R5.4-equivalent: same inputs → same output."""
    tokens = [_token(f"n{i}", f"node{i}", float(i) * 0.1, float(i) * 0.05) for i in range(20)]
    r = _repr(*tokens)
    out1 = render_scatter(r)
    out2 = render_scatter(r)
    assert out1 == out2


def test_many_nodes_bounded():
    """50 nodes all placed within 200×200 bounds."""
    tokens = [_token(f"n{i}", f"n{i}", float(i) * 0.05 - 1.0, float(i) * 0.03 - 0.5) for i in range(50)]
    r = _repr(*tokens)
    out = render_scatter(r)
    lines = out.splitlines()
    assert len(lines) == MAX_LINES
    for line in lines:
        assert len(line) <= MAX_COLS
