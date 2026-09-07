---
id: experiment:a00-76bbb729-a84e2a
mint_id: 714307b632624d878a721918e16bb491
type: experiment
parents:
  - hypothesis:l3w4-branch-shared-state
next_edges: []
confidence: 0.6
edited_by: a00-76bbb729
evidence_runs:
  - experiment:a00-76bbb729-a84e2a
loop: hypothesis:l3w4-branch-shared-state@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 39562bffb51fffee
season: 2
title: Worktree shares .env and names the graph fork, built red first
verdict: inconclusive_lean_proved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-76bbb729-a84e2a

## Experiment

What did you do? What happened? Include command/inputs and actual outputs.

## Evidence

Raw output, screenshots, logs.

## Agent Notes
<Built it, red-first. hypothesis:l3w4-branch-shared-state split out the two isolation leaks at L3.33; I made a real source diff that closes the .env leak and names the graph fork in zoom (the brief's explicit "at minimum name it"). Own code change = 64 insertions / 10 deletions across locations.py, envfile.py, zoom.py + a new test file test_shared_state_worktree.py. DO NOT run git was obeyed; edits are in the main checkout working tree for the director to commit.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
<Design decision, recorded (the brief demands it not be unrecorded). Clause 1 is unambiguous: .env is gitignored, exists only in the main checkout, so the credential lookup must resolve the MAIN graph from any worktree. Fix = locations.shared_project_root(start): find_project_root -> git_common_root -> re-derive the graph root there; identity in the main checkout, so non-worktree calls are byte-unchanged (pinned by test). envfile.resolve() now anchors to shared_project_root, so both the secrets geometry node AND the <source_root>/.env resolve to the one shared body. Clause 2 (the graph fork): the brief lists two defensible resolutions and forbids weakening child_working_graph() (the L3.31 isolation gate). I chose merge-up-carries-forked-nodes: the working graph a kid EDITS stays its own worktree fork, carried home by merge-up; I did NOT reroute write.py to the main graph. What I closed on the read side is the dispatch-killer zoom refusal: a --branch worktree cut at the tip cannot see a node minted after it, and the old error sent the reader hunting a typo in a correct id. zoom now says the target EXISTS in the main checkout fork, nameable. A parallel seat (a00-22069a30) independently built the same shared_project_root+envfile change; my zoom naming is the complementary piece. NOTE a00 keeps the brief twice-owned but not conflicting: the two working trees are separate.
<!-- THOUGHT:END -->

<EVIDENCE. Red-first: before the fix, all 4 new tests failed (shared_project_root did not exist; zoom refusal read "Fix the graph_core import / target id" instead of naming the fork). After: "4 passed in 0.28s". Full suite: "3 failed, 2018 passed, 1 skipped" -- the 3 failures are in test_sensei.py, the owner's UNTRACKED master-sensei WIP (seats.md fixture lacks dir-g1), independent of this change, same files failing before. My-touched areas (envfile, zoom, locations, dispatch, shared_state): "204 passed". LIVE run quoted verbatim (main checkout = identity, unchanged): $ python3 extensions/agi/bin/envfile.py --what env-file -> /home/ubuntu/work/agi/.env ; $ locations.py --json -> root: .agi. (worktree .env + zoom naming are proven through real git-worktree fixtures in test_shared_state_worktree.py -- those are the live worktree runs).