# AGI Tree — Loop State Handoff
## Session: 2026-05-01 | Engine: b5fd816 + post-wire-fix

---

## Loop Start / Restart / Monitor Commands

```bash
# Terminal 1 — watch loop progress
watch -n5 'echo "=== CHAIN COUNTS ===" && find ~/.hermes/agi-tree/nodes -type d | while read d; do count=$(find "$d" -name "*.md" 2>/dev/null | wc -l); [ "$count" -gt 0 ] && echo "$d: $count"; done | sort'

# Terminal 2 — run N iterations
cd ~/.hermes/agi-tree && autoresearch-tree --max-iters N

# Terminal 3 — tail logs
tail -F ~/.hermes/agi-tree/loop.log

# Manual dispatch (override automation)
cd ~/.hermes/agi-tree && python3 /home/ubuntu/autoresearch-tree/extensions/autoresearch-tree/bin/dispatch.py ~/.hermes/agi-tree N

# Post-wire (wire edges after iteration)
cd ~/.hermes/agi-tree && python3 /home/ubuntu/autoresearch-tree/extensions/autoresearch-tree/bin/post_wire.py ~/.hermes/agi-tree N

# Smoke test: confirm chain count > 2
find ~/.hermes/agi-tree/nodes -name "*.md" | wc -l
find_chains() { find ~/.hermes/agi-tree/nodes -mindepth 1 -maxdepth 1 -type d; }
find_chains | wc -l   # should be > 2
```

---

## What's Working Now (2026-05-01)

- 2-agent pipeline active (claude_max_parallel=2 in config)
- Agent nodes persist across iterations (snapshot-build-site.py merge mode)
- post_wire correctly updates nodes with verdict + wired_at + wired_from
- manifest.json status sync via heal.py (status=done propagates to post_wire)
- node_id and parent written to manifest by dispatch.py

---

## Fixes Applied Today

### 1. snapshot-build-site.py — merge mode (not wipe)
**File:** `/home/ubuntu/autoresearch-tree/extensions/autoresearch-tree/bin/snapshot-build-site.py`

- Removed `shutil.rmtree(NODES_DIR)` wipe (old lines 167-171)
- Added `load_existing_nodes()` — scans all `.md` files under `nodes/`, returns dict keyed by node id
- Added `origin` param to `write_frontmatter()` — tags nodes with `origin: build-site`
- After writing build-site nodes, deletes stale build-site nodes (origin=build-site, not in current output)
- Preserves ALL agent-generated nodes (experiment, verdict, mvp, outcome, bigger-outcome, hypothesis:a00-*)
- Build-site-derived nodes: `idea:domain-*`, `hyp:domain-r*`, `task:t-*`

### 2. dispatch.py — scaffold overwrite logic + manifest node_id
**File:** `/home/ubuntu/autoresearch-tree/extensions/autoresearch-tree/bin/dispatch.py`

- `_scaffold_node_for_agent()`: if file exists with just scaffold prompts (empty body), overwrite it. If body has real content, preserve it.
- `_pick_targets()`: renamed `n` loop variable to `_score` to avoid shadowing the `n` (int) parameter
- Added `node_id` and `parent` to agent_record manifest entry so post_wire can find the wired node

### 3. heal.py — manifest status sync
**File:** `/home/ubuntu/autoresearch-tree/extensions/autoresearch-tree/bin/heal.py`

- Added manifest re-write on every poll cycle: syncs agent status from agent.json back to manifest.json
- Also syncs "failed" status when pid disappears
- This was the root cause of post_wire always showing "no node_id" — manifest had stale "running" status

### 4. dispatch.py — g.nodes dict_values fix
- `_type_diversity()`: `len(g.nodes)` → `len(list(g.nodes))` (dict_values has no len())

---

## Config Change

**File:** `~/.hermes/agi-tree/autoresearch-tree.config.json`

```json
"agent_dispatch": {
  "claude_max_parallel": 2,   // was 1 — enables two-agent pipeline
  ...
}
```

---

## Scaffold Pipeline (How Agents Work Now)

### Two-Agent Parallelism
Single parent node spawns **two agents in parallel** on the same hypothesis:
1. **experiment agent** — runs experiments, tests assumptions, gathers evidence
2. **mvp agent** — builds working code/MVP toward app_purpose

Both share `parent_id`, `role` plumbs through scaffold. Results are verdict nodes
that feed into dispatch attractiveness scoring.

### Dispatch Target Selection
`_pick_targets()` in `dispatch.py`:
- Loads `closed_chains.txt` → excludes those chain IDs from all candidates
- Scores each chain by: descendant count + recency boost + type diversity
- Picks highest-attractiveness chain; spawns research+mvp agents on it

### Edge Wiring
`post_wire.py` wires new nodes into the graph:
- `_wire_verdicts()` — rel=next from parent verdict to new verdict
- `_wire_mvps()` — rel=next from parent mvp to new mvp
- `_wire_experiment_to_verdict()` — rel=supports from experiment to verdict
- Writes plain node IDs to `next_edges:` in frontmatter (no YAML list)

### Next Edge Flag (b5fd816)
`cli.py --next-edge TARGET` writes a node ID as a plain string to the
`next_edges:` frontmatter field of the current node (not a YAML list).
Used by `post_wire.py` to wire programmatic next-edge overrides.

---

## What to Watch For (Working Signals)

| Signal | Location | Meaning |
|--------|----------|---------|
| `nodes updated: N` in post_wire | loop.log | N nodes got verdict wired |
| `edges added: N` in post_wire | loop.log | N edges wired |
| Chain count grows | find_chains \| wc -l | New chains spawning |
| verdict/ dir grows | ls verdict/ | Experiment → verdict pipeline running |
| mvp/ dir grows | ls mvp/ | MVP agents shipping code |
| hypothesis/ dir | hypothesis chain growing | Interpretability work |
| closed_chains.txt | root | benchmark.py actively culling dead chains |
| find_chains > 2 | smoke test | At least 3 chains alive |

---

## Frozen Predecessor Discoveries

- **Ollama model**: qwen3:4b (judge), llama3:8b (fallback)
- **benchmark.py**: sends node content to Ollama, returns continue/close/branch
- **closed_chains.txt**: Filter loaded at top of `_pick_targets()` — works but
  integration not end-to-end; chains can still be picked if not yet in file
- **heuristic edge wiring** in `post_wire.py` is fragile — inspect `find_chains`
  output after each run to verify correct parents

---

## File Inventory

```
~/.hermes/agi-tree/
├── HANDOFF.md              ← long-form context
├── closed_chains.txt       ← benchmark.py writes closed chain IDs here
└── nodes/
    ├── hypothesis/         ← hypothesis chain
    ├── experiment/         ← experiment results (research agent output)
    ├── mvp/                ← shipped code (implementation agent output)
    ├── verdict/            ← Ollama verdicts (continue/close/branch)
    ├── app_purpose/        ← app purpose chain
    ├── bigger_outcome/     ← bigger outcome chain
    ├── idea/               ← ideas for future work
    └── ...
bin/
    ├── autoresearch-tree.sh    ← loop entry point (stub)
    ├── render-context.py       ← renders INJECTION.md from nodes/
    └── snapshot-build-site.py  ← builds nodes/ from build-site.md (merge mode)

Plugin: /home/ubuntu/autoresearch-tree/extensions/autoresearch-tree/
bin/
    ├── cli.py                   ← --next-edge flag
    ├── dispatch.py              ← two-agent pipeline + closed_chains
    ├── post_wire.py             ← edge wiring
    ├── benchmark.py             ← Ollama judgment
    ├── heal.py                  ← timeout monitoring + manifest sync
    └── zoom.py                  ← context scoping
```

---

## Known Remaining Issues

1. **Ollama ERR persists** — driver checks `import ollama` not `pip show`. Smoke mode still triggers it. Non-blocking for dispatch.
2. **Two-agent pipeline not fully wired** — research + implementation agents both spawn but only hypothesis nodes scaffolded (not experiment + mvp). The `_research_pipeline_targets()` path is defined but the scaffold logic maps role→node_type correctly.
3. **post_wire edge wiring limited** — only 1 edge added per iteration (the branch_fork parent edge). Next edges between verdict/mvp nodes not yet wired.
4. **longest_chain_length=2 metric** — graph has 15,846 nodes but longest chain reports 2 hops. `next_edges` not properly populated in most nodes.

---

## Next Steps for Testing

1. Run: `cd ~/.hermes/agi-tree && autoresearch-tree --max-iters 3`
2. After completion: `find_chains | wc -l` should be > 2
3. Check `hypothesis/`, `mvp/`, `verdict/` for new nodes
4. Check `loop.log` for `nodes updated: N` and `edges added: N` from post_wire
5. If chains < 3, check `closed_chains.txt` and dispatch.py attractiveness scoring
6. Verify node files have `verdict:` and `wired_at:` frontmatter fields
