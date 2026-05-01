# AGI Tree — Loop State Handoff
## Session: 2025-05-01 | Engine: b5fd816

---

## Loop Start / Restart / Monitor Commands

```bash
# Terminal 1 — watch loop progress
watch -n5 'echo "=== CHAIN COUNTS ===" && find ~/.hermes/agi-tree/nodes -type d | while read d; do count=$(find "$d" -name "*.md" 2>/dev/null | wc -l); [ "$count" -gt 0 ] && echo "$d: $count"; done | sort'

# Terminal 2 — run one iteration
cd ~/.hermes/agi-tree && bash bin/autoresearch-tree.sh run --iter N

# Terminal 3 — tail logs
tail -F ~/.hermes/agi-tree/logs/loop.log

# Manual dispatch (override automation)
cd ~/.hermes/agi-tree && python3 bin/dispatch.py --iter N --dry

# Post-wire (wire edges after iteration)
cd ~/.hermes/agi-tree && python3 bin/post_wire.py --iter N

# Smoke test: confirm chain count > 2
find ~/.hermes/agi-tree/nodes -name "*.md" | wc -l
find_chains() { find ~/.hermes/agi-tree/nodes -mindepth 1 -maxdepth 1 -type d; }
find_chains | wc -l   # should be > 2
```

---

## Scaffold Pipeline (How Agents Work Now)

### Two-Agent Parallelism (b5fd816 new)
Single parent node spawns **two agents in parallel** on the same hypothesis:
1. **experiment agent** — runs experiments, tests assumptions, gathers evidence
2. **mvp agent** — builds working code/MVP toward app_purpose

Both share `parent_id`, `role` plumbs through scaffold. Results are
verdict nodes that feed into dispatch attractiveness scoring.

### Dispatch Target Selection
`_pick_targets()` in `dispatch.py`:
- Loads `closed_chains.txt` → excludes those chain IDs from all candidates
- Scores each chain by: edges_wired, chain_length, missing_mvp, missing_verdict
- Picks highest-attractiveness chain; spawns research+mvp agents on it

### Edge Wiring
`post_wire.py` wires new nodes into the graph:
- `_wire_verdicts()` — rel=next from parent verdict to new verdict
- `_wire_mvps()` — rel=next from parent mvp to new mvp
- `_wire_experiment_to_verdict()` — rel=supports from experiment to verdict
- Writes plain node IDs to `next_edges:` in frontmatter (no YAML list)

### Next Edge Flag (b5fd816 new)
`cli.py --next-edge TARGET` writes a node ID as a plain string to the
`next_edges:` frontmatter field of the current node (not a YAML list).
Used by `post_wire.py` to wire programmatic next-edge overrides.

---

## What to Watch For (Working Signals)

| Signal | Location | Meaning |
|--------|----------|---------|
| Chain count grows | `find_chains \| wc -l` | New chains spawning |
| verdict/ dir grows | `ls verdict/` | Experiment → verdict pipeline running |
| mvp/ dir grows | `ls mvp/` | MVP agents shipping code |
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

## This Session's Engine Changes (b5fd816)

### 1. `--next-edge TARGET` flag (cli.py)
- Adds `cli.py --next-edge TARGET` option
- Writes TARGET as plain string (not YAML list) to `next_edges:` in frontmatter
- Enables programmatic next-edge override for post_wire.py

### 2. Two-Agent Pipeline (dispatch.py)
- New `_research_pipeline_targets()` — picks best attractiveness chain as single parent
- Spawns **research agent** (role=experiment) + **implementation agent** (role=mvp)
- Both on same parent; both get `role` plumbed through scaffold
- `find_chains` should grow by 2 (experiment + mvp) per iteration

### 3. closed_chains.txt (dispatch.py)
- Loaded at top of `_pick_targets()` before candidate filtering
- Excludes closed chain IDs from attractiveness scoring
- File location: `~/.hermes/agi-tree/closed_chains.txt`
- Format: one `chain_id` per line, `#` comments

### 4. Ollama Benchmark Feedback Loop (idea node)
- Not yet wired into loop
- Idea: benchmark verdict → closed_chains.txt → dispatch picks differently
- Remaining work: `--auto` mode in benchmark.py, driver.sh integration

---

## File Inventory

```
~/.hermes/agi-tree/
├── HANDOFF.md              ← this file
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
    ├── autoresearch-tree.sh    ← loop entry point
    ├── cli.py                   ← --next-edge flag added (b5fd816)
    ├── dispatch.py              ← two-agent pipeline + closed_chains (b5fd816)
    ├── post_wire.py             ← edge wiring (plain strings, rel="next")
    ├── benchmark.py             ← Ollama judgment (continue/close/branch)
    ├── heal.py                  ← timeout monitoring
    └── zoom.py                  ← context scoping
```

---

## Next Steps for Testing

1. Run `bash bin/autoresearch-tree.sh run --iter N`
2. After completion: `find_chains | wc -l` should be > 2
3. Check `hypothesis/`, `mvp/`, `verdict/` for new nodes
4. If chains < 3, check `closed_chains.txt` and dispatch.py attractiveness scoring
