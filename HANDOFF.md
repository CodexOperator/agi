# HANDOFF — autoresearch-tree (Capillary DAG)

> Self-contained brief for a fresh Claude Code instance. Read this first; everything else is reachable from here.

## What This Project Is

Capillary DAG memory for fast LLM agent onboarding. Replaces saturated predecessor `~/.hermes/agi/` (iter 47, build_time=0.04ms hardware noise floor — frozen).

**Capillary chain shape:**
```
idea → hypothesis(+) → experiment → verdict → mvp → outcome → bigger_outcome → app_purpose
```
Free-form branching. Longest-chain attractor + mid-chain join. Verdict taxonomy is finite-state.

## Project Tree (everything you need is here)

```
~/.hermes/agi-tree/
├── HANDOFF.md                 ← you are here
├── AGENTS.md / CLAUDE.md      ← project brief (mirror; read once)
├── autoresearch-tree.config.json  ← the marker file (driver walks up to find it)
├── context/
│   ├── INJECTION.md           ← auto-built ASCII view + chain stats (cached)
│   ├── kits/cavekit-*.md      ← 7 cavekits (graph-core, schema-registry, env-indexers,
│   │                              chain-engine, renderers, embeddings, autoresearch-tree-skill)
│   ├── plans/build-site.md    ← 88 tasks across 17 tiers; coverage matrix 100%
│   ├── schemas/[*].md         ← 6 starter bracketed schemas (idea, hypothesis,
│   │                              experiment, task, mvp, outcome)
│   └── impl/tracking.md       ← per-iteration log
├── nodes/                     ← auto-generated frontmatter node files (154 currently)
├── sessions/iter-NNN/<agent>/ ← per-agent run state + logs (when loop runs)
├── src/                       ← graph_core, schema_registry, renderers, embeddings
├── tests/                     ← 167 tests, all passing
├── bin/snapshot-build-site.py ← build-site → nodes/
├── bin/render-context.py      ← nodes/ → INJECTION.md
└── skill/autoresearch-tree/SKILL.md  ← portable skill copy
```

**Plugin (separate, not in project):**
```
~/.pi/agent/git/github.com/davebcn87/pi-autoresearch/extensions/autoresearch-tree/
├── driver.sh                  ← actual orchestrator (auto-detects project via walk-up)
├── bin/{dispatch,zoom,cli,heal}.py
├── lib/{find-root.sh, agent-prompt.md}
└── hooks/cc-session-start.sh  ← THIS injects the map into every CC session
```

**Global CLI:** `~/.local/bin/autoresearch-tree` → driver.sh (in PATH)

## Status as of last session

| Metric | Value |
|---|---|
| Tasks done | **34 / 88** (T0–T4 complete) |
| Tiers complete | **4 / 17** (T0, T1, T2, T3, T4) |
| Tests | **167 / 167 PASS** |
| Domains alive | graph-core (R1–R8 mostly), schema-registry (R1–R5 partial), renderers (ASCII+Mermaid+git-diff), embeddings (Node2Vec+UMAP+similarity), skill (scaffolded) |
| Domains pending | environment-indexers (T-032..T-046), chain-engine (T-047..T-059 mostly), autoresearch-tree-skill body (T-076..T-087) |
| Predecessor `agi/` | FROZEN, untouched |
| pi-autoresearch originals | `autoresearch-create` + `autoresearch-finalize` UNTOUCHED |
| Latest commit | `4d1db60` (drop wrapper, global symlink, skill update) |

## How to Run

### Quick smoke (no agent dispatch)
```bash
cd ~/.hermes/agi-tree
autoresearch-tree --smoke --max-iters 1
```
Outputs METRIC lines + writes `context/INJECTION.md`.

### Real loop (spawns parallel pi agents w/ healing)
```bash
cd ~/.hermes/agi-tree
autoresearch-tree --max-iters 5 --delay-mins 2
```
- 5 parallel pi subprocesses per iter (1 BIG zoom + 4 SMALL zoom on top attractors)
- Each agent times out at `agent_timeout_mins` (default 10) — healer subagent dispatched
- Agents signal done via `cli.py done <iter> <agent_id> --verdict ... --node-id ...`

### Continue building remaining tiers (the cavekit way)
Pick the next tier from `context/plans/build-site.md`, dispatch task-builder agents.
Pattern from prior tiers: 5 parallel `general-purpose` agents (NOT `ck:task-builder` — those mocked tool calls), each with explicit file content in the prompt. Use `git add -A && commit` after each task.

Tier-5 (next): T-012, T-014, T-023, T-027, T-031, T-067, T-072 — 7 tasks.

## Key Conventions

- **Node IDs**: `<type-prefix>:<short-slug>` (e.g. `hyp:lru-saturates-warm-load`). Kebab-case 2–5 words. Collisions append `:n`. Target ≤40 chars.
- **Schema files**: `[name].md` (brackets) = active for that dir tree. Plain `name.md` = inactive.
- **Verdict taxonomy** (finite-state):
  ```
  proved | disproved | inconclusive_lean_proved:N | inconclusive_lean_disproved:N | pending
  ```
  Plus `confidence: 0..1`, `evidence_runs`, `contradicts`, `supports`.
- **Recursive nodes**: frontmatter `subgraph: true` → body parsed as nested graph.
- **Renderer↔embeddings isomorphism**: UMAP `(x, y)` ARE the `RenderToken.x, y`. Single source of truth.

## What NOT to Do

- ❌ Don't touch `~/.hermes/agi/` (frozen historical record, iter 47 saturated).
- ❌ Don't modify `~/.pi/.../skills/autoresearch-create/` or `autoresearch-finalize/` (originals).
- ❌ Don't edit kits or build-site without explicit user direction (architecture is locked).
- ❌ Don't skip tests (run `python3 -m pytest tests/ -q` after every change).

## Auto-Injection (CC SessionStart hook)

When a CC session starts inside this project tree, `~/.claude/settings.json`'s SessionStart hook chain runs `cc-session-start.sh`. It:
1. Walks up to find `autoresearch-tree.config.json`
2. Re-renders `INJECTION.md` if cache >1hr stale (silent on failure)
3. Outputs the first 80 lines of INJECTION.md to stdout → CC injects as additional_context
4. Outside any project: silent no-op

So a fresh CC instance lands with the ASCII map already in context. No manual file reading needed.

## First-Move Suggestions for a Fresh CC Instance

1. **Sanity check**: `cd ~/.hermes/agi-tree && python3 -m pytest tests/ -q` (expect 167 passing).
2. **Check git state**: `git log --oneline | head -5` (latest = `4d1db60`).
3. **See what's pending**: `cat context/plans/build-site.md | grep -A 2 "T-012\|T-014\|T-023" | head -20` (tier-5 starters).
4. **Read one cavekit fully** (e.g. chain-engine): `cat context/kits/cavekit-chain-engine.md`.
5. **Run smoke** to refresh map: `autoresearch-tree --smoke --max-iters 1`.

## Glossary

- **Cavekit**: implementation-agnostic spec, R-numbered requirements with testable acceptance criteria.
- **Tier**: dependency layer in build-site (T0 = no deps, T16 = depends on everything).
- **Zoom level**: BIG = whole graph context for an agent; SMALL = subtree-bounded (2-hop) around a target node.
- **Capillary DAG**: the free-branching idea→hypothesis→experiment→verdict→mvp→outcome graph.
- **Attractor**: an idea/chain ranked by descendant count; small-zoom agents target top attractors.

## Files Worth Bookmarking

| File | Purpose |
|---|---|
| `context/kits/cavekit-overview.md` | Domain index + cross-ref map |
| `context/plans/build-site.md` | 88-task graph with coverage matrix |
| `context/impl/tracking.md` | What's been built, when, by which task |
| `context/INJECTION.md` | Auto-rendered ASCII view (auto-injected on CC start) |
| `~/.pi/.../extensions/autoresearch-tree/lib/agent-prompt.md` | Shared rules for builder agents |
| `~/.hermes/agi-tree/AGENTS.md` | Original project brief |

---

**Last session ended:** 167 tests passing, tier-4 complete, plugin extension in place, global CLI installed, SessionStart hook registered. Ready for tier-5+ build OR full autoresearch-tree run with real agent dispatch.
