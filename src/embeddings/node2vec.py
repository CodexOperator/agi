"""Node2Vec-style embedding (T-069 / embeddings R1).

Uses gensim Word2Vec skip-gram for true neural embedding (R2 verdict: gensim
skip-gram achieves Spearman=0.37 vs hash-based -0.18).

Upgrade path: if gensim is unavailable, falls back to hash-based projection
so the module still works (with degraded quality). The gensim path is
preferred and tested in experiments R2, R3, R4, R5.

Acceptance criteria (R1):
- Every node has exactly one vector after embed (R1.1)
- Vector dimensionality is configurable; default 64 (R1.2)
- Seeded; identical inputs + seed → identical vectors (R1.3)
- Empty graph → empty result (R1.4)
"""

from __future__ import annotations

import hashlib
import math
import random
from dataclasses import dataclass

try:
    from gensim.models import Word2Vec

    HAS_GENSIM = True
except ImportError:
    HAS_GENSIM = False

from graph_core.graph import Graph


@dataclass(frozen=True)
class EmbeddingConfig:
    dim: int = 64
    walk_length: int = 40  # gensim default; hash fallback uses 16
    walks_per_node: int = 5
    seed: int = 42
    p: float = 1.0  # return parameter (API parity)
    q: float = 1.0  # in-out parameter (API parity)
    # R7: when True, embed_and_store persists vectors to node frontmatter files
    store_in_graph: bool = False


def default_config() -> EmbeddingConfig:
    return EmbeddingConfig()


def embed_graph(
    graph: Graph,
    config: EmbeddingConfig | None = None,
) -> dict[str, list[float]]:
    """Return {node_id -> dim-length float vector}.

    Uses gensim skip-gram when available (R2 verdict: Spearman=0.37),
    falls back to hash-based projection otherwise.
    """
    cfg = config or default_config()
    if len(graph) == 0:
        return {}

    adjacency = _build_adjacency(graph)
    walks = _generate_walks(adjacency, cfg)

    if HAS_GENSIM:
        return _embed_gensim(walks, cfg, graph.node_ids)
    return _embed_hash(walks, adjacency, cfg)


def _build_adjacency(graph: Graph) -> dict[str, list[str]]:
    """Build deterministic {node_id: [target_ids]} adjacency list."""
    adj: dict[str, list[str]] = {}
    for nid in sorted(graph.node_ids):
        targets = []
        for e in sorted(graph.edges, key=lambda x: x.triple):
            if e.source_id == nid:
                targets.append(e.target_id)
        adj[nid] = targets
    return adj


def _generate_walks(
    adjacency: dict[str, list[str]],
    cfg: EmbeddingConfig,
) -> list[list[str]]:
    """Generate deterministic random walks using per-node seeded RNG."""
    all_walks: list[list[str]] = []
    for nid in sorted(adjacency):
        node_seed_hash = int.from_bytes(
            hashlib.sha256(f"{cfg.seed}|{nid}".encode("utf-8")).digest()[:8],
            "big",
        )
        node_rng = random.Random(node_seed_hash)
        for _ in range(cfg.walks_per_node):
            walk = [nid]
            for _ in range(cfg.walk_length - 1):
                neighbours = adjacency.get(walk[-1], [])
                if not neighbours:
                    break
                walk.append(node_rng.choice(neighbours))
            all_walks.append(walk)
    return all_walks


def _embed_gensim(
    walks: list[list[str]],
    cfg: EmbeddingConfig,
    node_ids: frozenset,
) -> dict[str, list[float]]:
    """Train gensim skip-gram and extract vectors.

    Uses skip-gram (sg=1) per R5 verdict (sg slightly better than CBOW,
    Spearman=0.865 vs 0.757).
    """
    model = Word2Vec(
        sentences=walks,
        vector_size=cfg.dim,
        window=5,
        sg=1,  # skip-gram (R5 verdict: preferred over CBOW)
        epochs=10,
        seed=cfg.seed,
        workers=1,
        min_count=1,
    )
    vectors: dict[str, list[float]] = {}
    for nid in node_ids:
        nid_str = str(nid)
        if nid_str in model.wv:
            vectors[nid] = list(model.wv[nid_str])
        elif nid in model.wv:
            vectors[nid] = list(model.wv[nid])
        else:
            # Node in graph but not in vocabulary (isolated?); zero vector
            vectors[nid] = [0.0] * cfg.dim
    return vectors


def _embed_hash(
    walks: list[list[str]],
    adjacency: dict[str, list[str]],
    cfg: EmbeddingConfig,
) -> dict[str, list[float]]:
    """Hash-based fallback (degraded quality: Spearman=-0.18 per R2).

    Used only when gensim is unavailable.
    """
    # Build per-node walk lists for hashing
    node_walks: dict[str, list[list[str]]] = {nid: [] for nid in adjacency}
    for walk in walks:
        if walk:
            node_walks[walk[0]].append(walk)
    return {
        nid: _walks_to_vector(node_walks.get(nid, []), dim=cfg.dim, seed=cfg.seed)
        for nid in adjacency
    }


def _walks_to_vector(walks: list[list[str]], dim: int, seed: int) -> list[float]:
    """Hash each (seed, node, position) into a dim-bucket and accumulate."""
    vec = [0.0] * dim
    if not walks:
        return vec
    for walk in walks:
        for pos, node_id in enumerate(walk):
            h = hashlib.sha256(f"{seed}|{node_id}|{pos}".encode("utf-8")).digest()
            b1 = int.from_bytes(h[:4], "big") % dim
            b2 = int.from_bytes(h[4:8], "big") % dim
            sign = 1.0 if (h[8] & 1) == 0 else -1.0
            vec[b1] += sign * 1.0 / (pos + 1)
            vec[b2] += sign * 0.5 / (pos + 1)
    norm = math.sqrt(sum(v * v for v in vec))
    if norm > 0:
        vec = [v / norm for v in vec]
    return vec
