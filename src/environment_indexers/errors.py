"""Custom errors for environment_indexers."""

from __future__ import annotations


class EnvironmentIndexerError(Exception):
    """Base error for environment indexers."""

    pass


class UnknownIndexerError(EnvironmentIndexerError):
    """Raised when the requested indexer name is not registered."""

    def __init__(self, name: str) -> None:
        self.name = name
        super().__init__(f"Unknown indexer: {name}")


class IndexerExecutionError(EnvironmentIndexerError):
    """Raised when an indexer fails to emit nodes."""

    def __init__(self, indexer_name: str, reason: str) -> None:
        self.indexer_name = indexer_name
        self.reason = reason
        super().__init__(f"{indexer_name} failed: {reason}")
