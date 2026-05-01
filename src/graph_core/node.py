"""Node primitive — implements graph-core/R1.

Six-field, no-frills record. Type semantics deferred to schema-registry.
ID minting deferred to T-005 (mint_id / IdRegistry).

Acceptance criteria covered (T-001 / R1):
- R1.1: id, type, payload_ref, parents, children, tags exposed; nothing else mandatory
- R1.2: no-parent root and no-child leaf accepted
- R1.4: tags is a set of strings independent of typed links
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Node:
    """Generic graph node.

    Exactly six fields. No timestamps. No auto-derived fields.
    """

    id: str
    type: str
    payload_ref: Optional[str] = None
    parents: set[str] = field(default_factory=set)
    children: set[str] = field(default_factory=set)
    tags: set[str] = field(default_factory=set)

    @property
    def is_root(self) -> bool:
        """A node with no parents is a root (R1.2)."""
        return not self.parents

    @property
    def is_leaf(self) -> bool:
        """A node with no children is a leaf (R1.2)."""
        return not self.children
