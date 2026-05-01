"""Frontmatter reader/writer (T-006 / graph-core R4).

Two file shapes accepted (R4.3):
- ``.md``: ``---\nYAML\n---\nbody...``
- ``.json``: ``{"frontmatter": {...}, "body": "..."}``

Round-trips are byte-equivalent modulo whitespace (R4.2):
- normalized line endings (LF only)
- top-level frontmatter keys serialized in sorted order
- trailing newline preserved
- JSON dumped with ``indent=2`` and ``sort_keys=True``
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


class FrontmatterError(Exception):
    """Raised when a node file cannot be parsed."""


@dataclass
class NodeFile:
    frontmatter: dict[str, Any]
    body: str
    suffix: str  # ".md" or ".json"


def _detect_suffix(path: Path) -> str:
    s = path.suffix.lower()
    if s not in {".md", ".json"}:
        raise FrontmatterError(f"unsupported file extension: {path.suffix}")
    return s


def load_node_file(path: str | Path, body: bool = True) -> NodeFile:
    """Load a node file. Pass ``body=False`` to skip body parsing (lazy read).

    For ``.json`` files, the body field is still read (it's already in memory),
    but for ``.md`` files we genuinely skip reading past the closing ``---``.
    """
    p = Path(path)
    suffix = _detect_suffix(p)
    text = p.read_text(encoding="utf-8")
    if suffix == ".md":
        return _parse_md(text, suffix=suffix, want_body=body)
    return _parse_json(text, suffix=suffix, want_body=body)


def _parse_md(text: str, suffix: str, want_body: bool) -> NodeFile:
    lines = text.splitlines(keepends=False)
    if not lines or lines[0].strip() != "---":
        raise FrontmatterError("md file missing opening '---'")
    # Find closing ---
    close_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            close_idx = i
            break
    if close_idx is None:
        raise FrontmatterError("md file missing closing '---'")
    yaml_text = "\n".join(lines[1:close_idx])
    fm = yaml.safe_load(yaml_text) or {}
    if not isinstance(fm, dict):
        raise FrontmatterError(f"frontmatter must be a mapping, got {type(fm).__name__}")
    if want_body:
        body_lines = lines[close_idx + 1 :]
        # Strip leading single blank line if present (a common convention)
        if body_lines and body_lines[0] == "":
            body_lines = body_lines[1:]
        body = "\n".join(body_lines)
    else:
        body = ""
    return NodeFile(frontmatter=fm, body=body, suffix=suffix)


def _parse_json(text: str, suffix: str, want_body: bool) -> NodeFile:
    obj = json.loads(text)
    if not isinstance(obj, dict):
        raise FrontmatterError("json node must be a top-level object")
    fm = obj.get("frontmatter", {})
    if not isinstance(fm, dict):
        raise FrontmatterError("'frontmatter' field must be a mapping")
    body = obj.get("body", "") if want_body else ""
    if not isinstance(body, str):
        raise FrontmatterError("'body' field must be a string")
    return NodeFile(frontmatter=fm, body=body, suffix=suffix)


def save_node_file(path: str | Path, nf: NodeFile) -> None:
    """Save a node file in normalized form (R4.2)."""
    p = Path(path)
    suffix = _detect_suffix(p)
    if suffix != nf.suffix:
        raise FrontmatterError(
            f"suffix mismatch: file is {suffix} but NodeFile claims {nf.suffix}"
        )
    if suffix == ".md":
        text = _emit_md(nf)
    else:
        text = _emit_json(nf)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\n")


def _emit_md(nf: NodeFile) -> str:
    yaml_block = yaml.safe_dump(
        nf.frontmatter,
        sort_keys=True,
        default_flow_style=False,
        allow_unicode=True,
    ).rstrip("\n")
    body = nf.body.rstrip("\n")
    if body:
        return f"---\n{yaml_block}\n---\n\n{body}\n"
    return f"---\n{yaml_block}\n---\n"


def _emit_json(nf: NodeFile) -> str:
    obj = {"frontmatter": nf.frontmatter, "body": nf.body}
    return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
