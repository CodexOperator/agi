---
id: hypothesis:l3-parent-never-told-to-iterate
mint_id: eb9c2af3f472407d9bd590c2a0602b31
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam-S1-L3-XI
scaffold_hash: 1e192743e0840662
season: 2
testable_claim: "After the change, a parent dispatched at one target keeps working that target across successive kids until it judges the work done: it reviews each kid, judges continue or adjust or done, spawns the next kid with what the previous one learned, and stops on an explicit bounded condition - proven by ONE live pi parent landing two or more kid nodes from a single dispatch, with the second kid's brief demonstrably carrying the first's result."
thought_session: belam-S1-L3-XI
title: brief.py calls the parent a loop and never tells it to run one, so every parent spawns exactly one kid and exits — the continue/adjust vocabulary exists only in the director block one tier up
---
<!-- BODY:BEGIN -->
# hypothesis:l3-parent-never-told-to-iterate

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
BUILD, NOT A PROBE. YOUR ARTEFACT IS A DIFF. An empty `git diff --stat` at the end means you are NOT done.

THE OWNER SPOTTED THIS, 2026-09-08, verbatim: "Also do pi parents know they can keep spawning kids repeatedly? It seems they never do our super-loop where they can just say continue or adjust".

THEY DO NOT KNOW, AND THE MEASUREMENT IS UNAMBIGUOUS. Across the two rounds run immediately before this brief was minted — L3.41 with two parents and L3.42 with six — **every single parent spawned exactly one kid and exited.** Eight for eight. Not one of them considered a second kid, and none of them were wrong to: nothing told them they could.

WHERE THE GAP IS, EXACTLY. `brief.py`'s `_parent` duties block opens with the docstring "A loop, not a node" and then enumerates the four things it says a parent needs: (1) how to spawn, via `dispatch.py --tier kid`; (2) the review gate and that a bypass is not a shortcut; (3) the serialization rule, now enforced by leases rather than requested; (4) what its artefact is — a parent authors no node, signals with `--owns`, and puts its review in its kids' THOUGHT blocks. **Read that list as a parent reads it: spawn a kid, review it, signal done. That is a single-shot script, and single-shot is exactly what eight of eight parents executed.** The name says loop; the instructions describe a straight line.

AND THE VOCABULARY ALREADY EXISTS — ONE TIER UP. The same file's DIRECTOR block hands down `continue | adjust | done` explicitly, wired to `season.py judge <outcome-id> --against goal:<id>`, with continue meaning keep going, adjust meaning reword the plan node, done meaning stop. So this project already has the exact judgement the owner is describing; it was given to tier 1 and never to tier 0.

WHAT IT COSTS, because this is not a tidiness bug. If a parent is single-shot then N briefs require N parent dispatches by the prime, every one of them hand-aimed. That is the whole shape of the prime's day, and it is the concrete root of the owner's earlier complaint that the loop "feels like doing everything by hand". A parent that iterates turns one dispatch into a worked area instead of one node.

WHAT TO BUILD.
1. An explicit ITERATION CONTRACT in the parent duties block. After reviewing a kid's node, the parent judges: **continue** — the target has more in it, spawn another kid, and the next brief must carry what the last kid actually produced so the second is not a blind rerun of the first; **adjust** — the brief was wrong or the kid misread it, re-brief and respawn against the correction; **done** — signal and exit. Use the existing continue/adjust/done words. Do not coin new ones when the director block already speaks this language.
2. A STOP CONDITION THAT IS EXPLICIT, BOUNDED AND CHEAP TO EVALUATE. This is the half that matters most and the half a careless build will get wrong. An unbounded parent loop on a paid provider is a money leak with a review gate attached, and the account it would spend has roughly $18 in it. Give it a hard ceiling on kids per dispatch, make the ceiling visible in the brief so the parent plans around it rather than discovering it as an unexplained refusal — the reasoning the serialization rule already documents for `spawn.max_live` — and make "done" the default judgement when the parent is unsure. A parent that cannot tell whether there is more to do should stop, not continue.
3. HONOUR EVERYTHING ALREADY THERE. The per-kid review gate runs on EVERY kid, not once at the end. The lease bound still applies and a refused slot is still an answer. The parent still authors no node and still records each review in that kid's THOUGHT block.

PROVE IT LIVE, AND ONLY LIVE. The gate is ONE pi parent, from a single `dispatch.py` invocation, landing TWO OR MORE kid nodes, where the second kid's brief demonstrably contains something the first kid produced. Paste the parent's own log showing both spawns and the judgement between them. A dry run does not prove this, a claude-code parent does not prove this for pi, and a unit test asserting the template contains the word "continue" proves only that a string is present — that last one is the trap, so do not stop there.

DO NOT touch `workflow.py`, `rotate.py`, `write.py` or `zoom.py` — other parents hold them this round. `brief.py` is yours. `dispatch.py` only if the ceiling genuinely must live there; say why in your node if you go there. Do not write `.agi/nodes/.geometry/seats.md`. Do not kill any `belam-*` tmux window.

YOU HOLD A BRANCH (Belam XI, L3.43). You are in your own worktree on your own `loop/...@s2` branch. COMMIT YOUR KID'S WORK TO IT BEFORE YOU EXIT:

    git add -A
    git commit -m "L3.43 <your agent id>: <what landed>"

Measured twice, including the round before this one: every `--branch` parent so far exited at ZERO commits ahead, `merge-up` merged an empty branch and reported green, and a human harvested the work by hand. Do NOT push, do NOT merge, do NOT touch `season/s2`. Run on pi. Your kid: `dispatch.py . L3.43 --target <this node> --level small --tier kid --harness pi`. Do NOT run `workflow.py run` this round.
