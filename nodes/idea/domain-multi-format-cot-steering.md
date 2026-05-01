---
id: idea:domain-multi-format-cot-steering
title: "domain: Multi-Format CoT Steering Surface"
type: idea
tags:
  - big-idea
  - co-steering
  - renderers
  - big-idea-b
spawns:
  - hyp:cot-steering-r1
  - hyp:cot-steering-r2
  - hyp:cot-steering-r3
descendants: 2
---

# Big Idea B: Multi-Format CoT Steering Surface

## Core Thesis

The same underlying capillary DAG can be rendered as multiple formats (ASCII, Mermaid, git-tree, git-diff), each serving as a different "steering surface" for LLM agents. Agents can read the graph in one format and write changes in another, creating a bidirectional CoT (Chain of Thought) pipeline.

## Motivation

Currently, the ASCII renderer is the primary surface for agents. But:
- ASCII is compact but lossy (no type colors, edge shapes)
- Mermaid is exportable to diagrams.net, GitHub, Notion
- git-tree shows historical evolution
- git-diff shows mutation between experiment runs

## Key Hypotheses

1. **R1 (Ascii-isomorphic)**: ASCII and Mermaid renderers produce representations that are isomorphic — same nodes, same edges, same hierarchy. Converting between them is lossless. **[PROVED]**

2. **R2 (Steerable-via-Mermaid)**: An agent can read the Mermaid output, understand the graph structure, and emit edits that when applied produce correct graph mutations.

3. **R3 (Git-diff as mutation log)**: The git-diff between two snapshot renders captures the exact graph mutation that occurred, suitable as a "mutation log" for replay.

## Relationship to Other Domains

- **renderers**: This domain EXTENDS the renderers domain by adding a new capability (steering) on top of existing formats
- **graph-core**: The graph-core provides the underlying data model that all renderers consume
- **embeddings**: Embeddings provide similarity-based navigation; steering provides deliberate navigation

## Implementation Notes

- Start with ASCII → Mermaid isomorphism (R1) ✓ DONE
- Then add steering capability (R2)
- Then add git-diff capture (R3)

## Status

1 hypothesis proved (R1: ASCII-Mermaid isomorphism confirmed), 2 hypotheses pending (R2, R3)
