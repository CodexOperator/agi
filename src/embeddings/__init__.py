"""embeddings: vector embeddings of the graph (R1+)."""

from .node2vec import embed_graph, EmbeddingConfig, default_config
from .projection import project, ProjectionConfig, apply_umap_coords
from .similarity import similar_to, cosine

__all__ = [
    "embed_graph",
    "EmbeddingConfig",
    "default_config",
    "project",
    "ProjectionConfig",
    "apply_umap_coords",
    "similar_to",
    "cosine",
]
