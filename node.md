---
confidence: 0.85
id: "level3:bin-stitch@v2"
origin: build-version
version: 2
supersedes: "level3:bin-stitch"
parents:
  - goal:g6.3
payload_ref: extensions/agi/bin/stitch.py
tags:
  - level3
  - build-version
  - g6.3
title: "Level-3 v2: extensions/agi/bin/stitch.py — a version chain is not a duplicate payload_ref"
type: level3
---

`extensions/agi/bin/stitch.py` v2 — teaches `stitch.py` the version dimension `goal:g6.3` introduces this iteration, so a v1→v2 build-node pair sharing a `payload_ref` reads as a version chain instead of drift.

**The defect.** `verify_tree()`'s category 3 grouped nodes by `payload_ref` and reported every group of size > 1 as `duplicate_payload_ref`, which feeds `has_drift()` — a nonzero `--strict` exit. `materialize()` sorted by `payload_ref` and let first-writer-wins (`seen_refs`) pick whichever node happened to sort first by filename, silently skipping the rest as duplicates. Neither function knew a v2 build-node was a legitimate evolution of v1 rather than an ambiguous claim. The first time this iteration's convention actually got used — two v2 nodes minted in parallel by sibling kids this same run, `level3:lib-find-root.sh@v2` and `level3:skills-agi-SKILL.md@v2` — both would have broken the drift gate and had their materialization outcome depend on filename sort order rather than on which version was intended. That would have blocked G6.3's whole mechanism on its first real use.

**The predicate implemented for "well-formed chain".** Within one `payload_ref` group of size > 1 (`_is_well_formed_chain` in `stitch.py`):
1. Every node has a distinct integer `version` (no two nodes at the same version).
2. Sorted ascending, those versions form a contiguous run: `max(version) - min(version) + 1 == len(group)` — a missing version number leaves an orphan with no defined predecessor, so a gap is not a chain even if every present `supersedes` link looks correct.
3. Every node except the one with the lowest version has `supersedes` equal to the `node_id` of the group member exactly one version below it (its immediate predecessor).

Only a group passing all three is reported under the new `version_chains: {payload_ref: [ids ascending by version]}` key — informational, deliberately excluded from `has_drift()`'s check list, so it cannot make `--strict` fail. `materialize()` writes the chain **head** (highest version) for such a group instead of the old arbitrary first-writer.

**Why everything else stays drift.** A version collision, a `supersedes` naming the wrong predecessor or an id that isn't in the group at all, or a version gap all fail the predicate above and stay in `duplicate_payload_ref`, exactly as before this change. The failure this refuses to introduce is *silently materializing an arbitrary version of a group that only looks ordered* — e.g. two nodes both claiming `version: 2`, or a `supersedes` typo pointing at a node that doesn't exist. `_is_well_formed_chain` does not attempt to salvage a partial order out of an ambiguous group; it returns `False` and the whole group is reported, unresolved, same as the pre-chain behavior. A `--version N` flag was added to `materialize()`/CLI to pick a specific chain member deterministically (reports, never guesses, when no member has that version) — it does not touch genuine-duplicate groups at all, on the same "ambiguity is not this script's to resolve" principle.

**Verification.** `cd extensions/agi && python3 -m pytest tests/test_stitch.py -q`: 31 passed before this change, 40 passed after (9 new tests added: well-formed chain is not drift + materializes v2 head; same-version collision still drift; `supersedes` naming a missing id still drift; a version gap (v1→v3, no v2) still drift; `--version 1` materializes v1 both via the Python API and the CLI; `--version` with no matching chain member is reported under a new `skipped_no_version` key, not guessed; a non-integer `version` in frontmatter is coerced to 1 with a warning, not a crash). Full engine suite (`pytest tests/`): 503 passed, unaffected. Real-corpus `--verify` against `/home/ubuntu/work/agi-tree` (180 level-3 nodes, run mid-iteration while sibling kids were writing their own v2 nodes in parallel): `duplicate_payload_ref: 0`, `version_chains: 2` (`extensions/agi/lib/find-root.sh` and `skills/agi/SKILL.md`, each `v1 -> v2`) — confirming both real chains classify correctly and neither trips drift. Honest caveat: `stale_contracts` reported 2 (`level3:bin-stitch` and `level3:tests-test-stitch` — both are this change's own payload files, stale relative to their stored contracts only because I edited them and did not run `level3.py`, which is out of scope per this task's rules and owned by other kids this iteration) plus `unreadable_contracts: 2` for the two real v2 nodes themselves — they carry no `LEVEL3-CONTRACT` block at all, since `build-version` nodes are hand-authored, not `level3-scan`-generated. That is a pre-existing, separate gap in category 4 (stale/unreadable contracts have no chain-awareness), not something this change touches or claims to fix.

**What this node does not claim.** This makes `stitch.py` version-*aware* — it can tell a provably ordered v1→v2 pair from an ambiguous duplicate, and it can materialize a chosen version deterministically. It does **not** make the git grid the payload source; `payload_ref` still resolves against the live engine tree exactly as before (untouched), and grid-as-payload-source is still blocked on S9 per `goal:g6.3`. It also does not extend chain-awareness to category 4 (`stale_contracts`/`unreadable_contracts`) — a `build-version` node's missing contract block is reported today exactly as it would be for any other contract-less node, with no special-casing for the version convention. That is a real gap, left open rather than guessed at.
