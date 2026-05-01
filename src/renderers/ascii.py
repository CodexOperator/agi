"""ASCII renderer (T-061 / renderers R2).

Hierarchical depth-driven layout. Bounded at 200 lines × 200 cols.
On overflow:
- truncate at column 200 with ``... [line cut]`` suffix
- truncate at line 200 with ``... [truncated, N more nodes]`` final line

Determinism: input is a sorted-by-id deterministic Representation, so output is
byte-equal across runs.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Iterable

from .representation import RenderToken, Representation

MAX_LINES = 200
MAX_COLS = 200
LINE_CUT_MARKER = " ... [line cut]"
TRUNC_MARKER_FMT = "... [truncated, {n} more nodes]"


def render_ascii(representation: Representation) -> str:
    """Render a Representation as bounded ASCII text."""
    tokens = list(representation.tokens)
    lines: list[str] = []

    # Header summary (always 2 lines)
    type_counts: dict[str, int] = defaultdict(int)
    for t in tokens:
        type_counts[t.type] += 1
    summary = f"# graph: {len(tokens)} nodes"
    type_line = "# types: " + ", ".join(
        f"{k}={v}" for k, v in sorted(type_counts.items())
    )
    lines.append(_truncate_line(summary))
    lines.append(_truncate_line(type_line))
    lines.append(_truncate_line("#"))

    # Body: one line per token, indented by depth.
    rendered_count = 0
    for t in tokens:
        if len(lines) >= MAX_LINES - 1:
            remaining = len(tokens) - rendered_count
            lines.append(_truncate_line(TRUNC_MARKER_FMT.format(n=remaining)))
            break
        indent = "  " * max(t.depth, 0)
        edge_summary = ""
        if t.edges:
            edge_strs = [f"{rel}->{tgt}" for tgt, rel in t.edges[:3]]
            extra = f" (+{len(t.edges) - 3})" if len(t.edges) > 3 else ""
            edge_summary = " [" + ", ".join(edge_strs) + extra + "]"
        line = f"{indent}{t.label} :: {t.type}{edge_summary}"
        lines.append(_truncate_line(line))
        rendered_count += 1

    return "\n".join(lines) + "\n"


def _truncate_line(line: str) -> str:
    if len(line) <= MAX_COLS:
        return line
    cut_at = MAX_COLS - len(LINE_CUT_MARKER)
    if cut_at < 0:
        cut_at = 0
    return line[:cut_at] + LINE_CUT_MARKER
