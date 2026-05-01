"""environment_indexers — pluggable source indexers.

Each indexer consumes an external source (directory, repo, API spec, etc.)
and emits nodes into the graph via graph-core and schema-registry.

Usage:
    from environment_indexers import register_indexer

    @register_indexer("my_indexer", "Indexes my thing")
    def my_indexer(path: str) -> None:
        # Emit nodes using graph-core API
        pass
"""

from __future__ import annotations

from .errors import (
    EnvironmentIndexerError,
    IndexerExecutionError,
    UnknownIndexerError,
)
from .registry import (
    IndexerInfo,
    IndexerRegistry,
    get_registry,
    register_indexer,
)

__all__ = [
    "EnvironmentIndexerError",
    "IndexerExecutionError",
    "IndexerInfo",
    "IndexerRegistry",
    "UnknownIndexerError",
    "get_registry",
    "register_indexer",
]
