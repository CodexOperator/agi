---
name: autoresearch-tree
description: Capillary DAG memory for fast LLM agent onboarding. Idea→Hypothesis→Experiment→MVP→Outcome chains with longest-chain-wins, mid-chain join, and verdict taxonomy. Forks pi-autoresearch (originals untouched).
---

# autoresearch-tree

## Overview
Capillary DAG memory layer that captures research-and-build trajectories as `Idea → Hypothesis(+) → Experiment → Verdict → MVP → Outcome → Bigger Outcome → App Purpose` chains. Optimized for fast LLM agent onboarding: longest-chain-wins surfacing, mid-chain join, free-form branching, structured verdict taxonomy. (full impl: T-076 / R1)

## When to Use
Invoke when an agent must reason over prior research trajectories rather than a flat task list — multi-iteration exploration, hypothesis chains, experiments whose outcomes feed downstream MVPs. Prefer over `autoresearch-create` when chain memory is load-bearing. (full impl: T-077 / R2)

## Inputs
- `idea`: seed concept (string) — big or small
- `parent_chain`: optional ancestor chain id for mid-chain join
- `mode`: `extend | fork | join | fresh` (default: auto-decided by attractiveness scoring)

(full impl: T-078 / R3)

## Outputs
- `chain_id`: stable id for the new node
- `verdict`: one of `proved | disproved | inconclusive_lean_proved:N | inconclusive_lean_disproved:N | pending`
- `confidence`: 0.0–1.0
- `mvp_artifacts`: paths to any built MVP files

(full impl: T-079 / R4)

## Big-Idea-vs-Small-Idea Decision
Each iteration first asks: explore a big idea (fresh chain, broad) or a small idea (extend existing, granular)? Ratio configurable via `big_idea_vs_small_idea_split` in `context/chain-config.json`. Default 0.3 (30 % big, 70 % small). (full impl: T-080 / R5)

## Agent Dispatch (Claude builders; Ollama deferred to v2)
Dispatcher hands subtasks to up-to-N Claude builder agents in parallel. Default cap = 5 (configurable). Each agent receives current chain stats, attractiveness scores, and available chains to extend / fork / hop. Ollama-backed local builders scoped to v2. (full impl: T-081 / R6)

## Verdict Emission
Each experiment terminates with a structured verdict node attached to its experiment node. Verdicts reference `evidence_runs`, `contradicts`, and `supports` lists so confidence propagates upstream. (full impl: T-082 / R7)

## Bench Harness Extension
Extends predecessor `_benchmark.py` with chain-aware metrics: `longest_chain_length`, `avg_chain_depth`, `mvp_count`, `outcome_coverage`, `chain_branching_factor`. Driver script lives at `bin/autoresearch-tree.sh`. (full impl: T-082..T-085 / R5–R7)

## Examples
End-to-end transcripts (seed → chain construction → verdict → downstream MVP) land here. (full impl: T-086 / R8)

## See Also
- Cavekit: `context/kits/cavekit-autoresearch-tree-skill.md` (R1–R8)
- Build site: `context/plans/build-site.md` (T-076..T-088)
- Predecessor (frozen): `~/.hermes/agi/` iter 47 lessons in `autoresearch.md`
