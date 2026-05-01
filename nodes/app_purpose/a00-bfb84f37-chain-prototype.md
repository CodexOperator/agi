---
id: app_purpose:a00-bfb84f37-chain-prototype
parents:
  - bigger_outcome:a00-bfb84f37-chain-prototype
status: complete
tags:
  - a00-bfb84f37
  - chain-prototype
  - app_purpose
title: "App Purpose: Prove capillary DAG chain mechanics"
type: app_purpose
---

# app_purpose:a00-bfb84f37-chain-prototype

## Mission

Prove that adding `next_edges` to connect a complete chain (idea → hypothesis → experiment → verdict → mvp → outcome → bigger_outcome → app_purpose) makes `find_chains()` return ≥1 chain, setting `longest_chain_length > 0`.

## This Closes the Loop

- idea:domain-graph-core (root)
  → hypothesis:a00-bfb84f37-38c7fb (chain prototype hypothesis)
    → experiment:a00-bfb84f37-chain-prototype
      → verdict:a00-bfb84f37-chain-prototype
        → mvp:a00-bfb84f37-chain-prototype
          → outcome:a00-bfb84f37-chain-prototype
            → bigger_outcome:a00-bfb84f37-chain-prototype
              → app_purpose:a00-bfb84f37-chain-prototype

## Result

longest_chain_length = 8 hops (proved)
