"""Schema file loader (T-019 / schema-registry R1).

Naming convention:
- ``context/schemas/name.md``   — schema file, inactive
- ``context/schemas/[name].md`` — schema file, active for this dir tree (R2 — covered later)
- Both ``.md`` (with YAML frontmatter) and ``.json`` accepted (R1.4).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from graph_core.persistence import load_node_file, FrontmatterError


_BRACKET_RE = re.compile(r"^\[(.+)\]$")


def is_bracketed(stem: str) -> bool:
    """Return True if a file stem is bracketed (e.g. ``[hypothesis]``)."""
    return bool(_BRACKET_RE.match(stem))


def canonical_name(stem: str) -> str:
    """Strip brackets to get the canonical schema name."""
    m = _BRACKET_RE.match(stem)
    if m:
        return m.group(1)
    return stem


@dataclass
class Schema:
    """A single schema definition loaded from disk."""

    name: str  # canonical name (no brackets)
    active: bool  # True if file was bracketed
    fields: dict[str, Any]  # declared fields (from frontmatter `fields` block, or empty)
    source_path: Path
    frontmatter: dict[str, Any] = field(default_factory=dict)


@dataclass
class SchemaRegistry:
    """Registry of loaded schemas, keyed by canonical name."""

    schemas: dict[str, Schema] = field(default_factory=dict)
    errors: list[tuple[Path, str]] = field(default_factory=list)

    def get(self, name: str) -> Schema | None:
        return self.schemas.get(name)

    def has(self, name: str) -> bool:
        return name in self.schemas

    def names(self) -> set[str]:
        return set(self.schemas.keys())

    def active(self) -> dict[str, Schema]:
        return {n: s for n, s in self.schemas.items() if s.active}


def load_schemas_from_dir(directory: str | Path) -> SchemaRegistry:
    """Load all schema files from ``directory``. R1.1 + R1.4."""
    d = Path(directory)
    reg = SchemaRegistry()
    if not d.is_dir():
        return reg
    # Iterate the directory ourselves so we have file paths.
    for p in sorted(d.iterdir()):
        if not p.is_file():
            continue
        if p.suffix.lower() not in {".md", ".json"}:
            continue
        try:
            nf = load_node_file(p)
        except FrontmatterError as e:
            reg.errors.append((p, str(e)))
            continue
        except Exception as e:  # noqa: BLE001
            reg.errors.append((p, f"{type(e).__name__}: {e}"))
            continue
        stem = p.stem
        active = is_bracketed(stem)
        # Schema name: prefer explicit frontmatter `name`, else canonical (de-bracketed) stem.
        fm_name = nf.frontmatter.get("name")
        if isinstance(fm_name, str) and fm_name:
            name = fm_name
        else:
            name = canonical_name(stem)
        # Schema fields can live under `fields:` in the frontmatter.
        declared_fields = nf.frontmatter.get("fields", {}) or {}
        if not isinstance(declared_fields, dict):
            reg.errors.append((p, "schema 'fields' must be a mapping"))
            continue
        # If both `[name].md` and `name.md` exist, the bracketed (active) one wins.
        existing = reg.schemas.get(name)
        if existing is not None and existing.active and not active:
            continue
        reg.schemas[name] = Schema(
            name=name,
            active=active,
            fields=declared_fields,
            source_path=p,
            frontmatter=nf.frontmatter,
        )
    return reg
