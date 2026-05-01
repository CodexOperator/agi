"""Scatter renderer (embeddings R6): ASCII scatter from UMAP coordinates.

Takes a Representation whose RenderToken.x, y are already populated with
UMAP-projected coordinates (via embeddings.apply_umap_coords). Produces a
bounded ASCII scatter plot.

Acceptance criteria (embeddings/R6):
- R6.1: registered through the same renderer plugin contract as other renderers
- R6.2: places each node at its (x, y) without re-projecting
- R6.3: respects ASCII bounds (200 lines × 200 cols), degrades visibly
- R6.4: overlap marker when two nodes share the same character cell

Plugin contract: render_scatter(representation: Representation) -> str
Returns a string with at most MAX_LINES lines and MAX_COLS columns per line.
"""

from __future__ import annotations

from collections import defaultdict

from .representation import Representation

MAX_LINES = 200
MAX_COLS = 200
OVERLAP_MARKER = "+"
EMPTY_MARKER = "·"


def render_scatter(repr_: Representation) -> str:
    """Render a UMAP-scattered graph as bounded ASCII art.

    - Each RenderToken is placed at its (x, y) coordinate
    - Coordinates are normalized to fit within MAX_LINES × MAX_COLS
    - Nodes at the same cell are shown with OVERLAP_MARKER
    - Empty cells show EMPTY_MARKER
    - Output is bounded to MAX_LINES lines, each ≤ MAX_COLS chars
    """
    tokens = list(repr_)
    if not tokens:
        return _empty_scatter()

    # Normalize x, y to integer grid coords in [0, MAX_LINES-1] × [0, MAX_COLS-1]
    xs = [t.x for t in tokens]
    ys = [t.y for t in tokens]

    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)

    # If all nodes share the same x or y, use a tiny range to avoid division by zero
    x_range = max(x_max - x_min, 1e-9)
    y_range = max(y_max - y_min, 1e-9)

    # Grid cells: (row, col) where row 0 = top (max y), row MAX_LINES-1 = bottom (min y)
    def to_grid(x: float, y: float) -> tuple[int, int]:
        col = int((x - x_min) / x_range * (MAX_COLS - 1) + 0.5)
        row = int((y_max - y) / y_range * (MAX_LINES - 1) + 0.5)
        # Clamp to bounds
        col = max(0, min(MAX_COLS - 1, col))
        row = max(0, min(MAX_LINES - 1, row))
        return row, col

    # Map grid cell -> list of (token_id, label) for overlap detection
    cell_tokens: dict[tuple[int, int], list[tuple[str, str]]] = defaultdict(list)
    for token in tokens:
        row, col = to_grid(token.x, token.y)
        cell_tokens[(row, col)].append((token.id, token.label))

    # Track overflow: nodes outside bounds (shouldn't happen with clamping, but be safe)
    overflow_count = 0

    # Build the grid
    grid: list[list[str]] = [[EMPTY_MARKER] * MAX_COLS for _ in range(MAX_LINES)]
    for (row, col), tlist in cell_tokens.items():
        if len(tlist) == 1:
            token_id, label = tlist[0]
            # Show short label; truncate to 3 chars for cell width
            marker = _short_label(label, max_len=3)
            grid[row][col] = marker
        else:
            # Overlap: show + marker
            grid[row][col] = OVERLAP_MARKER

    # Count cells that were actually occupied (not empty)
    occupied = sum(1 for row_ in grid for cell in row_ if cell != EMPTY_MARKER)
    overflow_count = len(tokens) - occupied

    # If overflow detected, add a warning footer
    lines: list[str] = []
    for row_ in range(MAX_LINES):
        line = "".join(grid[row_])
        # Truncate to MAX_COLS
        lines.append(line[:MAX_COLS])

    # Add overflow annotation if any
    if overflow_count > 0:
        footer = f"... [{overflow_count} nodes overflowed cell capacity]"
        if len(lines[-1]) + len(footer) <= MAX_COLS:
            lines[-1] = lines[-1] + footer
        else:
            lines.append(footer[:MAX_COLS])

    return "\n".join(lines)


def _short_label(label: str, max_len: int = 3) -> str:
    """Shorten a label to at most max_len chars for a grid cell."""
    if not label:
        return EMPTY_MARKER
    # For node ids, just use last meaningful segment
    if ":" in label:
        parts = label.split(":")
        label = parts[-1]
    if len(label) <= max_len:
        return label
    return label[:max_len]


def _empty_scatter() -> str:
    """Return an empty scatter plot."""
    lines = []
    for _ in range(MAX_LINES):
        lines.append(EMPTY_MARKER * MAX_COLS)
    return "\n".join(lines)
