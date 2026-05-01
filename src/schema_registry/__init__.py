"""schema-registry: pluggable, file-driven node schemas (R1+)."""

from .active_set import ActiveSet, DuplicateActiveSchemaError, build_active_set
from .loader import (
    Schema,
    SchemaRegistry,
    canonical_name,
    is_bracketed,
    load_schemas_from_dir,
)

__all__ = [
    "Schema",
    "SchemaRegistry",
    "load_schemas_from_dir",
    "is_bracketed",
    "canonical_name",
    "ActiveSet",
    "DuplicateActiveSchemaError",
    "build_active_set",
]
