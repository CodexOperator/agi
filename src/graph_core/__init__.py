"""graph-core: generic node/edge primitives for autoresearch-tree.

Implements cavekit-graph-core.md (R1+).
"""

from .node import Node
from .paths import (
    PathOutsideProjectError,
    PathValidator,
    get_validator,
    safe_cache_path,
    safe_path,
    safe_relative_path,
    set_project_root,
)

__all__ = [
    "Node",
    "PathOutsideProjectError",
    "PathValidator",
    "get_validator",
    "safe_cache_path",
    "safe_path",
    "safe_relative_path",
    "set_project_root",
]
