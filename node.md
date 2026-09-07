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
the scaffolded node — including this node's own frontmatter — so the resolved
identity is not unknown at write time. It is known, used, and dropped.

The engine made a real distinction between kinds of consciousness and kept no
record of having made it. That is the failure this idea names.

**B — the same brief, two enforcements. OPEN, under adversarial test.**

`pi_adapter.py:120` states the contract: "the brief is assembled once, by
tier, outside every harness. This adapter decides only how to SPELL a segment
on pi's command line." One brief for both harnesses — the instruction *is*
unified. The enforcement is not. `claude_code_adapter.py:100-108` refuses
`git commit|add|push|stash|checkout|reset|rm`, `*HANDOFF.md*`, `*CLAUDE.md*`
and `*dispatch.py*` (`goal:s34` item 10). `pi_adapter.py` contains no tool,
allow-list or deny-list surface at all — 226 lines, zero occurrences of
"tool". A pi kid is restrained by prose; a claude-code kid is restrained by
the harness.

That asymmetry is not a declared difference between *roles*; it is an
undeclared difference between *harnesses*, and it lands on the tier where it
matters most — the wave-3 ladder below the director runs GLM parents and
DeepSeek kids on pi (`ladder:ladder` rows, tier 1 parent and tier 0). It is
also the exact shape of the incident this project already paid for: the
2026-08-31 `git commit -A` that swept a second kid's half-written node and a
human's uncommitted edits into one commit. The refusal built afterwards was
built on one harness only.

Stated as open, not asserted: whether some other layer already closes this for
pi agents was under adversarial check when this node was written, and B should
be settled before it is acted on. A is not conditional on B.

## What this proposes next

One hypothesis per instance, not one big fix:

1. `dispatch.py` records the **effective** `role` and `ladder_tier` it
   resolved, and a test asserts that the identity used to grant tools is the
   identity written to `agent_record` — the two can never again be different
   variables. Smallest real slice; belongs to `goal:g16`, fixable under
   `goal:g15`.
2. Whatever tool surface the pi harness can or cannot enforce is **declared**
   in `ladder:ladder` next to `harness`/`model`/`effort`/`settings`, so a
   harness that cannot refuse says so in the graph instead of by silence.
   If the enforcement gap is real, declaring it is the first step and closing
   it is the second.

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

Instance A is proven and cited to line; instance B is deliberately left open
rather than asserted, because the advisor found it by reading two adapters and
had not yet finished trying to refute it. Recording a finding at the
confidence it was actually earned is the point — an idea node that overstates
B would put a false claim under a vision, which is worse than a slower fix.

The two instances are kept in ONE idea because they are one principle, and
split into TWO proposed hypotheses because they are two fixes. The idea is the
link; the hypotheses are the work.
<!-- THOUGHT:END -->
