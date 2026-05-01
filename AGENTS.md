# Autoresearch-Tree — Capillary DAG Memory for Agent Onboarding

## What This Is

Fresh chain of autoresearch (iter 0) replacing saturated `~/.hermes/agi/` (iter 47, build_time at 0.04ms hardware noise floor).

**Pivot**: stop optimizing graph build time. Build a *capillary DAG* of research ideas → hypotheses → experiments(verdicts) → MVP scripts → outcomes (i/o-doc fusion) → broader outcomes → entire-stack purpose. Agents browse the DAG to onboard fast and pick where to contribute next.

## Mental Model: Capillary System

```
Big idea (artery)
  └── Hypothesis (vein)
        └── Experiment → verdict ±confidence
              └── (more hypotheses)
                    └── MVP script (capillary)
                          └── Outcome [i/o-doc + README fusion]
                                └── Broader outcome
                                      └── App purpose (back to artery)
```

Branchy, free-form. Same idea spawns N hypotheses. Same hypothesis spawns N experiments. Verdicts spawn new ideas/hypotheses. Eventually fine-grained nodes converge to MVPs.

## Chain Mechanics (blockchain/DAG-style)

- Each path from idea → outcome = a "chain"
- **Longest-chain attracts** but not exclusive: short chains may be unique/strategic
- Agents pick: extend longest, fork mid-chain, start fresh, or hop between chains
- Multiple long chains converging on similar outcome = MVP feature signal

### Tunable Params (config)

```json
{
  "chain_min_join_length": 3,
  "mid_chain_join_prob": 0.3,
  "fresh_start_prob": 0.15,
  "big_idea_vs_small_idea_split": 0.3,
  "attractiveness_weights": {
    "length": 0.4,
    "depth": 0.2,
    "recency": 0.2,
    "mvp_count": 0.2
  }
}
```

## Verdict Schema

```
verdict: proved | disproved | inconclusive_lean_proved:N | inconclusive_lean_disproved:N | pending
N: 0-100 (lean strength)
confidence: 0.0-1.0
evidence_runs: [run_ids]
contradicts: [verdict_ids]      # list of prior verdicts this contradicts
supports: [verdict_ids]         # list of prior verdicts this reinforces
```

## Node Types

| Type | Role | Children |
|---|---|---|
| `idea` | big or small idea node | hypothesis(+) |
| `hypothesis` | testable claim | experiment(+) |
| `experiment` | run + outputs | verdict, child hypothesis(+), MVP(+) |
| `verdict` | proved/disproved/lean | new idea(+), new hypothesis(+) |
| `mvp` | minimum-viable code snippet | outcome(+) |
| `outcome` | i/o doc + README fusion (input shape, output shape, behavior, edge cases) | bigger_outcome(+) |
| `bigger_outcome` | aggregates outcomes into module purpose | app_purpose |
| `app_purpose` | top-level mission statement | (root, terminal) |

Plus: `chain` (virtual: ordered list of node ids), `tag`, `agent_session`.

## Renderers (multi-format, same underlying graph)

- **ASCII** — primary, compact, line-bounded (≤200 lines / ≤200 cols)
- **Mermaid** — clean DAG export (`graph TD` / `flowchart`)
- **Git-tree** — `git log --graph` shape rendering of chain history
- **Vector embedding** — Node2Vec + UMAP → 2D coords; project to ASCII scatter or use for similarity
- **Git-diff** — exp run → exp run mutation diff for chain inspection

**Critical**: ASCII renderer must use SAME underlying representation as vector embedding so the CoT-steering surface and visualization are isomorphic.

## Big Ideas Seeded (chain 0 starters)

- **A**: Capillary DAG memory for agent onboarding (this doc)
- **B**: Multi-format CoT-steering surface (ASCII/Mermaid/git-diff/git-tree as steering inputs)
- **C**: Graph↔vector duality via Node2Vec+UMAP — shared representation between B's surface and the embedding layer

## Off-limits

- Don't touch `~/.hermes/agi/` (frozen historical record at iter 47)
- Don't modify pi internal core
- DO modify pi-autoresearch plugin skill repo (add new `autoresearch-tree` skill, keep `autoresearch-create`/`finalize` untouched)

## Run Model

- 5 Claude subagents + 5 Ollama-qwen subagents = 10 concurrent
- Each agent picks: extend chain | fork | hop mid-chain | start fresh
- Skill `autoresearch-tree` decides big-idea-vs-small-idea per iteration

## Saved For Later

- sqlite3/duckdb in-mem backend (will be needed for swarm read-write at scale)
- Multi-repo cross-ref
- Incremental cache invalidation

## Inherited Lessons (from agi/ iter 1-47)

- `lru_cache` on builder object = O(1) warm load regardless of node count → reuse pattern
- pickle/json/msgpack serialization all hit noise floor → don't re-explore
- Tag-based `relates_to` edges bridge isolated clusters → port idea, may not fit DAG
- Precomputed BFS paths kill query_time_ms → port pattern
- Hub reachability matrix (32 hubs, O(1) reach) → port pattern
