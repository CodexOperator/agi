"""Indexer registry with decorator-based registration."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Protocol

from .errors import UnknownIndexerError


@dataclass
class IndexerInfo:
    """Metadata for a registered indexer."""

    name: str
    description: str
    func: Callable[..., None]
    tags: list[str] = field(default_factory=list)


class IndexerFn(Protocol):
    """Protocol for indexer functions."""

    def __call__(self, path: str) -> None:
        ...


class IndexerRegistry:
    """Registry of available indexers."""

    def __init__(self) -> None:
        self._indexers: dict[str, IndexerInfo] = {}

    def register(
        self,
        name: str,
        description: str,
        *,
        tags: list[str] | None = None,
    ) -> Callable[[IndexerFn], IndexerFn]:
        """Decorator to register an indexer.

        Args:
            name: Unique identifier for the indexer.
            description: One-line description for --list output.
            tags: Optional list of tags for categorization.

        Returns:
            Decorator that registers the function.
        """

        def decorator(fn: IndexerFn) -> IndexerFn:
            if name in self._indexers:
                raise ValueError(f"Indexer already registered: {name}")
            self._indexers[name] = IndexerInfo(
                name=name,
                description=description,
                func=fn,
                tags=tags or [],
            )
            return fn

        return decorator

    def get(self, name: str) -> IndexerInfo:
        """Get indexer info by name.

        Args:
            name: Indexer name.

        Returns:
            IndexerInfo for the named indexer.

        Raises:
            UnknownIndexerError: If the indexer is not registered.
        """
        if name not in self._indexers:
            raise UnknownIndexerError(name)
        return self._indexers[name]

    def list_indexers(self) -> list[IndexerInfo]:
        """List all registered indexers in registration order."""
        return list(self._indexers.values())

    def __contains__(self, name: str) -> bool:
        return name in self._indexers


# Global registry instance
_registry = IndexerRegistry()


def get_registry() -> IndexerRegistry:
    """Get the global indexer registry."""
    return _registry


def register_indexer(
    name: str,
    description: str,
    *,
    tags: list[str] | None = None,
) -> Callable[[IndexerFn], IndexerFn]:
    """Decorator to register an indexer with the global registry.

    Usage:
        @register_indexer("my_indexer", "Indexes my thing")
        def my_indexer(path: str) -> None:
            ...
    """
    return _registry.register(name, description, tags=tags)
