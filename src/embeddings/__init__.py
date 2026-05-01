"""embeddings: vector embeddings of the graph (R1+)."""

from .node2vec import embed_graph, EmbeddingConfig, default_config

__all__ = ["embed_graph", "EmbeddingConfig", "default_config"]
