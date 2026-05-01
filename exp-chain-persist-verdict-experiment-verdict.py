#!/usr/bin/env python3
"""
Experiment: Persist verdict→experiment→verdict next_edges

Hypothesis: The 10-hop chains from iter 8 weren't persisted because verdict→experiment
next_edges weren't written to node files. Adding these edges will make chains
survive cold reload.

Method:
1. Add verdict→experiment next_edges to verdict node files
2. Create extension experiment nodes
3. Create extension verdict nodes
4. Verify chains survive cold reload
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from graph_core.loader import load_directory
from chain_engine.chains import find_chains


def main():
    print("=" * 60)
    print("CHAIN PERSIST: verdict→experiment→verdict next_edges")
    print("=" * 60)

    g, loaded = load_directory("nodes", reconstruct_next_edges=True)
    chains = list(find_chains(g))

    longest_length = max((len(c) for c in chains), default=0)
    chain_count = len(chains)
    ten_hop = len([c for c in chains if len(c) == 10])

    print(f"\nResults:")
    print(f"  Chain count:   {chain_count}")
    print(f"  Longest chain: {longest_length} hops")
    print(f"  10-hop chains: {ten_hop}")

    print(f"\nMETRIC longest_chain_length={longest_length}")
    print(f"METRIC chain_count={chain_count}")
    print(f"METRIC ten_hop_chains={ten_hop}")


if __name__ == "__main__":
    main()
