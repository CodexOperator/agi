"""schema-registry: pluggable, file-driven node schemas (R1+)."""

from .loader import (
    Schema,
    SchemaRegistry,
    load_schemas_from_dir,
    is_bracketed,
    canonical_name,
)

__all__ = [
    "Schema",
    "SchemaRegistry",
    "load_schemas_from_dir",
    "is_bracketed",
    "canonical_name",
]
