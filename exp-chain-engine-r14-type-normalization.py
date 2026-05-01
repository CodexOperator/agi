#!/usr/bin/env python3
"""
Experiment: chain-engine-r14-type-normalization

Hypothesis: Node type strings with hyphens (bigger-outcome, app-purpose)
cause is_valid_transition to fail, resulting in 0 chains being found
despite 36 'next' edges being correctly persisted.

Root cause: _node_from_frontmatter reads 'type' directly from frontmatter
without normalizing hyphens to underscores. The VALID_TRANSITIONS set uses
underscores (bigger_outcome, app_purpose), but some node files use hyphens.

Fix: normalize type_str = str(fm.get("type", "node")).replace("-", "_")
in _node_from_frontmatter.

Expected outcome: chains jump from 0 to 5 × 8-hop after fix.
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
    print("CHAIN-ENGINE-R14: TYPE NORMALIZATION FIX")
    print("=" * 60)

    g, loaded = load_directory("nodes", reconstruct_next_edges=True)
    chains = list(find_chains(g))

    longest_length = max((len(c) for c in chains), default=0)
    chain_count = len(chains)

    weights = AttractivenessWeights()
    top_chains = longest_n(chains, 5, weights, g)

    print(f"\nResults:")
    print(f"  Chain count:  {chain_count}")
    print(f"  Longest chain: {longest_length} hops")

    for chain, score, length in top_chains:
        print(f"  [{length}-hop, score={score:.3f}] {chain[0]}")

    print(f"\nMETRIC longest_chain_length={longest_length}")
    print(f"METRIC chain_count={chain_count}")

    # Verdict
    if longest_length >= 8 and chain_count >= 5:
        verdict = "proved"
        confidence = 1.0
        print(f"\nVERDICT: PROVED (confidence={confidence})")
    elif longest_length > 0:
        verdict = "inconclusive_lean_proved:70"
        confidence = 0.7
        print(f"\nVERDICT: INCONCLUSIVE_LEAN_PROVED:70")
    else:
        verdict = "disproved"
        confidence = 0.5
        print(f"\nVERDICT: DISPROVED")

    return 0


if __name__ == "__main__":
    sys.exit(main())
