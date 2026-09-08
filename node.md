---
id: hypothesis:l3-engine-files-outside-the-grid
mint_id: eb52f664dcd7448ab482abbb2b555a43
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam-S1-L3-XII
scaffold_hash: e077642e6d37617e
season: 2
testable_claim: After the change, every tracked engine file that the project intends to grid-version has a build node whose payload_ref resolves to it, proven by a checker that enumerates tracked engine files, subtracts every declared payload_ref, and exits nonzero on any remainder outside a declared exclusion list -- with the remainder at zero and level3.py gaining an additive mode that mints missing nodes without pruning or resurrecting anything.
thought_session: belam-S1-L3-XII
title: "Seventy-two tracked engine files have no build node, so their bytes are outside the grid entirely: rotate.py, season.py, send.py and write_guard.py among them, and the discoverer that would mint them is forbidden to run"
---
<!-- BODY:BEGIN -->
# hypothesis:l3-engine-files-outside-the-grid

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
