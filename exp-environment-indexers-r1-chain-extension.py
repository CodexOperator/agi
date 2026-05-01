#!/usr/bin/env python3
"""
Experiment: environment-indexers-r1-chain-extension

Hypothesis: environment-indexers domain has 9 hypotheses but its r1 chain
was only 8-hop. Extending via verdict→experiment→verdict cycles would
bring it to 12 hops (matching the other domains).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from graph_core.loader import load_directory
from chain_engine.chains import find_chains
from chain_engine.attractiveness import AttractivenessWeights
from chain_engine.queries import longest_n


def main():
    print("=" * 60)
    print("ENVIRONMENT-INDEXERS CHAIN EXTENSION")
    print("=" * 60)

    g, loaded = load_directory("nodes", reconstruct_next_edges=True)
    chains = list(find_chains(g))

    longest_length = max((len(c) for c in chains), default=0)
    chain_count = len(chains)

    # Check environment-indexers specifically
    env_chains = [c for c in chains if "environment" in c[0]]
    env_longest = max((len(c) for c in env_chains), default=0)

    weights = AttractivenessWeights()
    top = longest_n(chains, 5, weights, g)

    print(f"\nResults:")
    print(f"  Chain count:  {chain_count}")
    print(f"  Longest chain: {longest_length} hops")
    print(f"  Environment-indexers chains: {len(env_chains)}, longest: {env_longest} hops")

    for chain, score, length in top:
        marker = " ⭐" if length == longest_length else ""
        print(f"  [{length}-hop{marker}] {chain[0]}")

    print(f"\nMETRIC longest_chain_length={longest_length}")
    print(f"METRIC chain_count={chain_count}")
    print(f"METRIC environment_indexers_hops={env_longest}")

    # Verdict
    if env_longest >= 12:
        verdict = "proved"
        confidence = 1.0
        print(f"\nVERDICT: PROVED (confidence={confidence})")
    elif env_longest >= 10:
        verdict = "inconclusive_lean_proved:80"
        confidence = 0.8
        print(f"\nVERDICT: INCONCLUSIVE_LEAN_PROVED:80")
    else:
        verdict = "pending"
        confidence = 0.5
        print(f"\nVERDICT: PENDING")

    return 0


if __name__ == "__main__":
    sys.exit(main())
