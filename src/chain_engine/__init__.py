"""Chain engine — virtual chain queries on top of graph-core.

Chains are computed from the graph, not stored separately.
"""
from .types import Chain
from .chains import find_chains

__all__ = ["Chain", "find_chains"]
