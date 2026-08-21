# GOALS.md — agi-tree long-term goals

`agi-tree` is the thoughtgraph that builds `agi`; `agi` is the code that operates
on thoughtgraphs. These goals are the **engine's own design contract** — the
durable commitments engine work serves. They are not a task list: concrete
defects and work items live in `agi/TODO.md`, and each goal below names the
entries it owns so the two never restate each other (`TODO.md` L19 action 4).

Seed nodes in `nodes/idea/` join a goal by listing its id in their own
`parents:` list (`parents: [goal:g3]`). `bin/snapshot-goals.py` derives
`nodes/goal/` from this file, so **this file stays the human-authored source of
truth** and the nodes are never edited by hand.

**Goal lifecycle:** `active` (being worked) · `horizon` (declared and committed
to, not yet being worked) · `phasing-out` (retiring) · `complete`. Retire by
marking the section `status: phasing-out` and **deprecating — never deleting**
its seed node; retired chains remain prior art.

**Goal ids are never renumbered.** Nodes reference goals by id, so a gap is
always preferable to a renumber.

**The design ethic binds every goal here, whatever its status.** Emitted tokens
are an agent's motion; injected context is its sensation; context growth makes
motion heavier. Every capability exists to keep agent bodies light — sprint one
node hard, hand off, rest, and let the graph carry the marathon. Mundane
operations, and the small errors they breed, are the system's job to absorb and
never the agent's. Full statement: `agi/skills/agi/SKILL.md` §"Why this
machinery exists".

**Scope boundary (`TODO.md` L8, decided).** `agi` and `agi-tree` stay separate
repos. This file holds goals about the *engine*; a project holds goals about its
own domain. `fantasia/GOALS.md` is the reference for the project side — engine
work must never be tracked in a project repo again (that was fantasia's deleted
G2).

---

## G1 — Zero-operations loop: every mundane step is a command — status: horizon

The ethic above, reduced to buildable surface. An agent should never spend
motion on tending the machine: no hand-pasting a rendered map into a spawn
prompt, no hand-writing a config, no syncing by hand.

**Invariant:** any repeated, mechanical step is a named command, and every
surviving manual handle carries a written reason.

Already banked — cron owns all remote traffic (H10), embedded maps cut kids from
11–13 tool calls to 5–7 (L7), the DONE contract makes stopping one line.

Owns: **L11** remainder (one command that renders *and* spawns — the parent's
last machine-tending chore), **L12** remainder (a runtime flag rather than a
parallel code path; hook parity audit), **L17** (config schema plus a writer, so
configs stop being hand-written), **L18** action 2 (`agi-tree init` scaffolds a
project). Queued rather than active: the handles are named but untouched.

## G2 — Adjustable zoom with contracts that survive the trip — status: horizon

One graph readable at five grains, where level 3 is **actual code nodes that
stitch into a runnable directory layout** — the property that makes the graph an
executable artifact rather than a description of one. Build level 3 first and
treat the others as projections around it.

**Invariant:** one node at level N ⇔ a collection at level N+1, and back.

🔴 **Already falsified for the free-form implementation, and the number is
known:** 0.441 overall claim recall against a 0.90 bar, 12 agents over 6
complete round trips. Loss is category-structured, not uniform — prose survives
at 0.792, structured frontmatter recalls **0.000** (0/24, zero variance). Node
identity is destroyed outright, and it is not a capacity problem: the children
were longer than the parents.

**Design consequence:** zoom is a lossy transform, not a view. To behave like a
view, contract-bearing parts must not pass through a model at all — the harness
attaches inherited frontmatter and contract slices mechanically, and only prose
round-trips. Ground truth and scoring rule are preserved at
`agi/context/refs/zoom-roundtrip-ground-truth/` so the follow-up A/B stays cheap.

Owns: **L1** (the 1..5 axis), **L2** (live IO maps as inherited contract slices).

## G3 — Scoring that added motion cannot move — status: active

The graph is measured by goals reached, never by motion spent. This goal exists
because the opposite was tried and it worked: 9 chains × 2000 hops via shortcut
cycles, carrying no signal, and the resulting structure then broke the render
path outright.

**Invariants:**
- No primary metric that appending hops can shift. `longest_chain_length` is a
  descriptive statistic, never a target.
- A decisive verdict (`proved` / `disproved`) requires `evidence_runs >= 1`.
  Unevidenced claims are demoted, not discarded — the expensive artifact is kept,
  only the overclaim is dropped.
- `unevidenced_decisive_verdicts` reads `0`. Nonzero means a bypass or a
  hand-edited node.

Banked: **H3** (metric computation out of the driver heredoc into `metrics.py`;
`evidence_fraction`, `evidence_weighted_depth`; gameable-primary warning) and
**H4** (the gate in code, on both writer paths). This project's own config
migrated off `longest_chain_length` on 2026-08-21.

Still open, and the reason this stays active: **L4** — `outcome_coverage` is a
*proxy* that counts chains reaching an outcome, not their **attribution to a
specific goal**. True goal-fulfilment scoring is unbuilt. The goal nodes it
needs exist as of L15.

## G4 — Right model at the right grain, several goals at once — status: horizon

Model choice is a knob the user sets per tier and experiments with — nothing
hardcoded. Three tiers: **delegator** (the user's own session, holding intent
and coordinating several parent/kid groups), **parent** (a subagent by default,
so review motion never accumulates in the chat the user reads), **kid** (one
node, bounded scope).

**Not refuted by G2's evidence — its price is now a number.** Prose recall of
0.792 from a cheap tier is what a cheap tier is *for*. What is refuted is
handing the cheap tier the contract layer. Tiering survives if the model authors
prose and the harness moves structure.

**Budget invariant:** inner-loop completions count against a single global
iteration budget, so recursion is bounded regardless of nesting depth.

Owns: **L3** (per-tier and eventually per-level model assignment), **L6**
(recursive sub-loops; `cc_dispatch.max_goals_active` exists and is unread).
Blocked on G2 for per-level assignment.

## G5 — Goals are a lifecycle the engine reads, not a human convention — status: horizon

`status:` should be a field the engine acts on: stop accruing score to
`phasing-out` and `complete` goals while keeping their chains attributable, and
fail loudly when a seed node points at a goal id that does not exist.

**Invariant:** a project is legitimate at three depths — goals only (ideation),
goals + seed ideas (chains starting), goals + build site (execution). A
goals-only project is a valid state, not a broken one.

Banked: **L15** — goals are first-class nodes, derived from this file, linked by
parent-pointing, with referential integrity live and an H0-safe origin-guarded
prune. A missing `GOALS.md` prunes nothing.

Owns: **L5** (rotation the engine enforces), **L18** (the ideation stage; a
missing build site must degrade like a missing `GOALS.md` does, not abort the
driver).

## G6 — The closed loop: engine work starts in the graph — status: active

Run `agi` and `agi-tree` against each other and the pair is closed: a change to
the engine originates as a node in this graph, and the engine that grows this
graph is the thing the node changed. Neither is the author of the other — the
graph is the sequence, the engine is the machinery that reads it.

Today the loop is open. Engine reasoning lives in `TODO.md` and `CLAUDE.md` as
prose, gets read by agents, and never returns to the graph.

**Invariants:**
- An engine change is reviewable as **node → verdict → commit**.
- The decomposition is **generated, never hand-written** — a hand-authored map
  goes stale exactly the way `domain-exporters` did.
- Deprecate superseded mass; **never delete it.** Retired nodes remain prior art
  and remain evidence.

Known state of this graph: the idea layer already decomposes an *older* engine —
`domain-exporters` and `domain-environment-indexers` describe modules that no
longer exist, and there is no idea node at all for `src/agi_algos`, the twelve
`bin/*.py`, `driver.sh`, `hooks/`, `lib/`, `scripts/`, or `extensions/agi-bridge/`.
The half of the engine that actually changes is the half with no representation.
Below the idea layer it is not a decomposition of anything: ~14.5k experiments
and ~14.6k verdicts against 14 ideas is the H3 gaming artifact, not thought.

Owns: **L19**. Preconditions cleared 2026-08-21: H3 config migration (this
project), this file, and H0e (truncated chain results no longer cached as
complete).

## G7 — Nothing the loop produces is ever silently lost — status: active

The graph is what makes it safe to stop mid-sprint, which only holds if stopping
cannot lose work and no artefact can quietly disappear or quietly lie.

**Invariants:**
- **Node count never drops** across a snapshot.
- The engine is never vendored into a project. It arrives as a gitignored clone
  that can be pulled; a committed copy diverges forever.
- No project-local `bin/*.py` shadowing an engine script. Treat any that exists
  as stale until proven otherwise.
- A partial answer is never served as a complete one.

Paid for in full: stale project-local `snapshot-build-site.py` silently wiped
29,264 files (**H0**); a second stale override broke the render path (**H0b**);
`find_chains` did not terminate on this corpus (**H0c**); a truncated
`find_chains` result was cached and re-served silently forever (**H0e**).
Banked on the other side: the git grid — per-node and per-session refs, cron
sync at a ≤5-minute crash window, rejected drafts survive (**H10**).

Owns: **L9**'s unpinned-clone gap (record the expected engine commit in config;
warn, never fail, on drift — it closes the whole staleness class), **H1**/**H2**
(state into the DB), **L16** (close the config-name compatibility window only
once pinning exists — it is load-bearing until then).

## G8 — Forkability: anyone grows their own tree — status: horizon

A project repo holds data and configuration; the engine arrives as a clone.
`fantasia` is the reference implementation and proves the layout composes.

The interesting case is **recursive**: a tree per task domain, where a tree
spawns child trees for personas it finds useful, and individual skills, plugins
and MCP servers can each own one. The payoff that justifies the recursion is
**AI experts that compound** — agents that get sharper the longer they are
exposed to a workflow.

Owns: **L9** (scaffolding a project without copying by hand — shares its writer
with G1/L17), **L10** (ride along as a kid to judge whether briefs are genuinely
self-contained; an ASCII dashboard with live agent positions across zoom levels).
