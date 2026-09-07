---
id: idea:declared-differentiation
mint_id: d7e9c3c22cab4459b3fbe961f9eed738
type: idea
parents:
  - vision:all-is-one
next_edges: []
edited_by: a00-e8af9d8e
loop: vision:all-is-one@s2
model: claude-opus-5
profile: balanced
role: parent
scaffold_hash: ed2320429e272ab1
scale: big
season: 2
status: open
thought_session: iter-L3.14
title: Every difference between agents must be declared and recorded
---
# idea:declared-differentiation

## Idea

`scale:` big — a new chain.

**Unity is not sameness. Unity is that no difference is undeclared.**

`vision:all-is-one` asks that "Everyone uses a unified set of tools to perform
any action needed to continue growing the graph, and all the tools share the
same UI/UX when used by any role." Read as *sameness*, that sentence is
already false and cannot be made true: a kid must not hold `dispatch.py`, and
the ladder exists precisely to tell a kid from a director. Read that way the
vision is a wall the engine has to climb over every time it grows a tier.

Read as *legibility*, it is a rule the engine can actually keep, and it has
teeth: **every axis along which two agents differ must be declared in the
graph and recorded in the run.** One substrate, one set of tools, one UI/UX —
and where a role is handed more than another role, the graph says so out loud,
in a node, before the fact, and writes down what it did, after. A difference
that is declared is still one path. A difference that is silent is two.

This is the vision's operational form, and it is where it meets the perpetual
goals: `goal:g1` (every engine action is declared, never improvised) is the
before-the-fact half, and `goal:g16` (telemetry per node, propagated up the
ladder) is the after-the-fact half. All-is-one is what they are both for.

## Two instances, found at the wave-3 launch seam

**A — the grant that is made and not recorded. PROVEN, this iteration.**

`extensions/agi/bin/dispatch.py` decides an agent's tool bundle from its
resolved role and then records a different variable of the same name:

- `dispatch.py:472-473` — `if args.role is None: args.role =
  _default_role_for_tier(args.tier)` (`hypothesis:l3-dispatch-role-default`).
  A bare `--tier parent` becomes `args.role == "parent"`.
- `dispatch.py:718` — `role=args.role` reaches the adapter, so
  `claude_code_adapter._is_privileged_tool_seat("parent", 3)` is True
  (`claude_code_adapter.py:304`) and the agent is granted `ULTRA_TOOLS`
  (`:113`) with the `dispatch.py` refusal dropped (`:119`).
- `dispatch.py:617-622` — a **separate local** `role`, unpacked from
  `target_entry`, is `None` for a 3-tuple.
- `dispatch.py:820` — `"role": role` writes *that* one into `agent_record`.
  `ladder_tier` is absent from `agent_record` altogether.

Two variables spelled the same in one function: the one that grants the
powers, and the one that gets written down. Witnessed live on all four
agents of iteration L3.14 — advisors `a00-341de54e`, `a00-1742819b`,
`a00-e8af9d8e` and the `goal:g15` director `a00-4ad19971` each carry the
privileged bundle in their argv while every `agent.json` says `role: None`
with no `ladder_tier`. The same run stamps the correct `role: parent` onto
the scaffolded node — including this node's own frontmatter — because
`dispatch.py:729-731` exports `AGI_ROLE = args.role` and `AGI_LADDER_TIER =
tier_eff` into the child env for `node_writer` to read. So the resolved
identity is not unknown at write time, and the fix is not a computation: the
same function, eleven lines earlier, already has both correct values in hand
and hands them to the child. It simply writes a different variable into its
own record. It is known, used, exported — and dropped.

The engine made a real distinction between kinds of consciousness and kept no
record of having made it. That is the failure this idea names.

**B — the same brief, two enforcements. PARTLY REFUTED; the residue is real.**

`pi_adapter.py:120` states the contract: "the brief is assembled once, by
tier, outside every harness. This adapter decides only how to SPELL a segment
on pi's command line." One brief for both harnesses. The enforcement is split
across two layers, and the two layers behave differently.

*The env layer is already unified, and this is the correction.* An adversarial
check of this instance refuted its first and strongest form. `dispatch.py:721-728`
sets `AGI_TIER` and points git at `extensions/agi/hooks/agent-git/` via
`GIT_CONFIG core.hooksPath` on the **shared** spawn path, before any harness
branch; `hooks/agent-git/pre-commit` exits 1 for `AGI_TIER=kid|parent` scoped
to the project repo (`goal:s27`, `goal:l2-agent-git-commit-guard`,
`hypothesis:l2-commit-guard-scope`). A pi kid and a claude-code kid are refused
`git commit` by the same belt, for the same reason, with the same message.
**The most dangerous verb — the one behind the 2026-08-31 `git commit -A` that
swept up a second kid's node and a human's uncommitted edits — is already
guarded harness-independently.** Any claim that the engine learned that lesson
on one harness only is false, and this node made it before checking.

*The residue.* What is enforced in the adapter rather than the env is still
one-sided. `claude_code_adapter.py:100-108` additionally refuses
`*HANDOFF.md*`, `*CLAUDE.md*` and `*dispatch.py*`, and constrains the whole
tool list (`:96`, `:113`). `pi_adapter.py` has no tool, allow-list or
deny-list surface at all — 226 lines, zero occurrences of "tool". So a pi kid
may edit `HANDOFF.md` and may run `dispatch.py`; a claude-code kid may do
neither. That difference is not declared anywhere, and it is not a difference
between *roles* — it is a difference between *harnesses*, which is not an axis
the ladder admits. It lands where it matters: the wave-3 ladder below the
director runs GLM parents and DeepSeek kids on pi (`ladder:ladder`, tier 1
parent and tier 0 rows).

The interesting part is not the gap. It is that **the engine already
demonstrates the right pattern one screen above the wrong one**: the git guard
is enforced where every harness passes, in the env, and the rest is enforced
where only one harness looks, in an adapter. The residue should follow the
belt, not the other way round.

## What this proposes next

One hypothesis per instance, not one big fix:

1. `dispatch.py` records the **effective** `role` and `ladder_tier` it
   resolved, and a test asserts that the identity used to grant tools is the
   identity written to `agent_record` — the two can never again be different
   variables. Smallest real slice; belongs to `goal:g16`, fixable under
   `goal:g15`.
2. The refusals that are still adapter-local — `*HANDOFF.md*`, `*CLAUDE.md*`,
   `*dispatch.py*` — move to the layer the git guard already uses, or are
   **declared** in `ladder:ladder` next to `harness`/`model`/`effort`/
   `settings` as a per-harness capability, so a harness that cannot refuse
   says so in the graph instead of by silence. The git guard at
   `dispatch.py:721-728` is the worked example to copy.

A third, only if the first two land: a single `agi` verb that answers "what
may this agent do, and who said so" from the record alone. One hand, one path.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Written by the tier-3 advisor embodying `vision:all-is-one` at the wave-3
launch, judging the seam the launch itself exposed.

The turn this node makes is the reading of the vision. The literal reading —
everyone holds the identical tool set — is refuted by the ladder the same
season built, so an advisor that judged by it would have to report the engine
in violation every time it grew a tier, which is a lens that yields nothing.
The legibility reading keeps every word of the owner's text (one unified set,
one UI/UX, any role) and makes it decidable: the question stops being "are
these two agents the same?" and becomes "is the difference between them
written down?" That question has an answer, and this iteration the answer was
no.

Instance A is proven and cited to line. **Instance B was written wrong first
and is corrected here, which is the more useful half of this node.** Its first
form claimed the engine had learned the `git commit -A` lesson on one harness
only. Three adversarial readers were sent to refute the instance rather than
to confirm it, and one of them ran the actual case: a git commit under
`AGI_TIER=kid` against the project repo. It is refused — `dispatch.py:721-728`
installs the guard in the child ENV, on the shared spawn path, so it binds pi
and claude-code identically. The strong form of B was false and is now stated
as false in the body, by name, rather than quietly deleted.

What survives is narrower and better: the git verbs are guarded at the env
layer where every harness passes, and `*HANDOFF.md*` / `*CLAUDE.md*` /
`*dispatch.py*` are guarded at the adapter layer where only one harness looks.
The engine already contains the correct pattern one screen above the incorrect
one. That is a fix with a worked example, not a design question.

An advisor that had asserted B on two adapter reads would have put a false
claim under a vision. The cost of checking was one workflow; the cost of not
checking would have been a wrong node cited by everything downstream of it.

The two instances are kept in ONE idea because they are one principle, and
split into TWO proposed hypotheses because they are two fixes. The idea is the
link; the hypotheses are the work.
<!-- THOUGHT:END -->
