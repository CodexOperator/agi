# HANDOFF — autoresearch-tree (Capillary DAG Memory)

> Fresh session brief. Read top-to-bottom once. Everything else is reachable from here.

## What This Project Is

Capillary DAG memory layer: LLM agents build a graph of `idea → hypothesis → experiment → verdict → mvp → outcome → bigger_outcome → app_purpose` chains. The graph is the knowledge base; agents onboard fast by reading it.

**Predecessor** (`~/.hermes/agi/`) is frozen at iter 47 — 40-hop chains, 257 tests, proved formula `hops = 2×N + 8`. This project is a fresh run with a new scaffold pipeline.

## Project Root

`~/.hermes/agi-tree/` — all state lives here.

## How to Run the Loop

```bash
# Start (55 iters, 1 agent/iter, fresh session)
cd ~/.hermes/agi-tree
tmux new-session -d -s autoresearch-tree \
  "autoresearch-tree --max-iters 55 2>&1 | tee ~/.hermes/agi-tree/loop.log"

# Monitor
tail -f ~/.hermes/agi-tree/loop.log

# Attach to see live output
tmux attach -t autoresearch-tree

# Stop
tmux kill-session -t autoresearch-tree
```

## Key Files

| File | Purpose |
|------|---------|
| `loop.log` | Driver output — METRICS, spawns, healers, iter summaries |
| `sessions/iter-NNN/manifest.json` | Per-iter agent IDs, pids, statuses |
| `context/INJECTION.md` | Auto-rendered ASCII graph snapshot (≤200 lines) |
| `autoresearch.jsonl` | Frozen predecessor's experiment log (~89 entries) |
| `nodes/` | All node files — hypothesis/, idea/, task/ (verdict/exp/mvp/outcome dirs will grow) |
| `autoresearch-tree.config.json` | Config (1 agent/iter, 55 max, 10min timeout) |

## Plugin (Engine Code — where changes land)

`~/.pi/agent/git/github.com/davebcn87/pi-autoresearch/extensions/autoresearch-tree/`

Key files modified in this session:
- `bin/dispatch.py` — scaffolds node file before each agent starts
- `bin/cli.py` — agent signals done here; writes verdict into node frontmatter
- `lib/agent-prompt.md` — agent rules + Chain Workflow section

## The Scaffold Pipeline (How It Works Now)

1. **Driver spawns agent** → `dispatch.py` calls `_scaffold_node_for_agent()` 
2. **Node file pre-created** → `nodes/<type>/<slug>.md` with frontmatter already filled (`type`, `parents`, `next_edges: []`)
3. **Agent fills body** → only the markdown body, frontmatter untouched
4. **Agent signals done** → `cli.py done` finds the node by ID, adds `verdict:` + `confidence:` to frontmatter, appends notes

Node type per iteration:
- Big zoom → `hypothesis` (new chain branch)
- Small zoom → next step: hypothesis→experiment→verdict→mvp→outcome→bigger-outcome

## Current Loop Status

- **Loop**: Running (tmux `autoresearch-tree`, started ~15:01)
- **Iter**: ~1–5 range (fresh restart after plugin update)
- **Metrics**: `longest_chain_length=2` (only idea→hypothesis, no exp/verdict nodes yet)
- **Problem known**: Prior 20 iters produced `verdict=proved` but no node files on disk — fixed by scaffold pipeline
- **Git commit**: `b5fd816` — "engine: scaffold+verdict pipeline"

## Frozen Predecessor Key Discoveries (from `autoresearch.jsonl`)

**PROVED:**
- Chain formula: `hops = 2×N + 8` where N = verdict→experiment→verdict cycles. Basic chain = 8 hops.
- Node2Vec 2D projection NOT isomorphic to graph (Spearman -0.18 — DISPROVED)
- Test coverage 41% — disproved >80% hypothesis
- `next_edges` in YAML frontmatter required for chain reconstruction on cold reload
- Git `checkout HEAD -- nodes/` WIPES verdict/mvp/outcome — must commit immediately
- Type normalization bug: hyphens vs underscores silently broke chain edges

**Critical bugs fixed by predecessor:**
- `_reconstruct_next_edges` break-at-first-level prevented subdirectory traversal
- 3 verdict files missing `type:verdict` frontmatter
- schema-registry missing `bigger-outcome:schema-registry-r2` node

## What's Different This Fresh Run

- 157 seed nodes loaded (7 ideas, 60 hypotheses, 90 tasks) — inherited from predecessor graph
- `longest_chain_length=2` because no experiment/verdict/mvp/outcome nodes exist yet
- Agents previously called `done --verdict proved` without creating node files → FIXED (scaffold pipeline)
- 55 iters budgeted, 1 agent/iter

## Monitoring One-Liners

```bash
# Current position
grep "^=== iter" ~/.hermes/agi-tree/loop.log | tail -5

# Last iter result
grep -E "^iter [0-9]+:" ~/.hermes/agi-tree/loop.log | tail -3

# Healers fired
grep "healer:" ~/.hermes/agi-tree/loop.log | wc -l

# Primary metric over time
grep "METRIC longest_chain_length" ~/.hermes/agi-tree/loop.log

# Node count growth
grep "METRIC node_count" ~/.hermes/agi-tree/loop.log

# Are verdict/exp/mvp dirs growing?
ls ~/.hermes/agi-tree/nodes/
```

## What to Look For in 5–10 More Iters

- `METRIC longest_chain_length` climbing past 2 (needs experiment→verdict pair)
- `METRIC mvp_count` going from 0 to >0
- New directories appearing in `nodes/` (verdict/, experiment/, mvp/)
- Agents completing without healers (iter summary shows `status=done` with no `healer:` line above it)

## If Loop Dies or Gets Stuck

```bash
# Check if driver still alive
pgrep -f "autoresearch-tree --max-iters" | head -3

# Force restart
tmux kill-session -t autoresearch-tree 2>/dev/null
cd ~/.hermes/agi-tree
tmux new-session -d -s autoresearch-tree \
  "autoresearch-tree --max-iters 55 2>&1 | tee ~/.hermes/agi-tree/loop.log"
```

## Architecture Decision Record (This Session)

- **Scaffold-first**: driver pre-creates node skeleton → agent fills body → `cli.py done` adds verdict. Eliminates silent success (agent reports done but writes nothing).
- **No auto-experiment-run**: the scaffold tells agent what kind of node, agent decides the content. Kept simple to avoid over-automation.
- **Fresh loop vs continue**: killed old session and restarted so new pipeline (commit `b5fd816`) takes effect from iter 1.

---

**Last updated:** 2026-05-01T15:01 UTC | **Loop:** running | **Commit:** `b5fd816`
