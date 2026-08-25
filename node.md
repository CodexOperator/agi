---
confidence: 1.0
goal_id: G6.9
goal_kind: subgoal
id: "goal:g6.9"
mint_id: f9e21a010143472d8f198d7ea5b10fe0
origin: goals-doc
parents:
  - goal:g6
seeds: []
status: active
tags:
  - goal
  - subgoal
title: "G6.9: `GOALS.md` is rendered from the nodes, not the other way round"
type: goal
---

**The last hand-authored source in this repo becomes derived, like everything
else.** `nodes/goal/` is currently generated *from* `GOALS.md`, which makes the
document the source of truth and the nodes a projection — the exact arrow
**G6.1** just reversed for engine code, still pointing the wrong way for the
goals themselves. Every property that made the inversion right there is true
here: a goal is a thought, thoughts live in nodes, and a node can be versioned,
zoomed, addressed and linked in ways a heading in a 2,600-line markdown file
cannot.

**What the document becomes: a rendered convenience, not a store.** A flat
human-readable digest of the goal nodes — useful for reading top to bottom, for
`git log`, for a person who wants the whole contract in one scroll. Not
authoritative, and marked as such in its own header so nobody edits it and
expects the edit to survive. The same relationship `context/INJECTION.md`
already has to the graph.

**And it is explicitly the weaker interface.** The real one is the dynamic
hypergraph renderer (**G9.4**, **G10.3**): a viewport a human pans and an agent
queries at the resolution it needs, which is strictly better for both readers
than a linear document is for either. Markdown is what we render *until* that
exists, not the target.

**The hard part is not the renderer, it is `snapshot-goals.py`'s prune.** That
script deletes every `origin: goals-doc` node it does not re-derive on a run —
H0i's shape exactly, and the reason CLAUDE.md carries a standing warning about
emptying a generator input. Inverting the direction means that prune must go
*before* the nodes become the source, not after: for the window where both
exist, a `GOALS.md` that fails to mention a goal must never be able to delete
that goal's node.

**Sequencing, and it is the whole risk:**
1. **Render first, prune never.** Add the node → document renderer and run it
   alongside the existing parser. Diff the rendered document against the
   hand-written one until they agree; that diff is the migration's own test.
2. **Cut the prune.** `snapshot-goals.py` stops deleting, then stops parsing.
3. **Nodes become authoritative.** `GOALS.md` gains a "generated — edit the
   nodes" header, and editing a goal means editing `nodes/goal/<id>.md`.

**Ids are the thing that must survive intact.** Goal ids are never renumbered
(this document's oldest rule), so the renderer's ordering and heading shape
have to be derived from the node's own `goal_id`, never from file order or
from position in the rendered output.

Falsifier: delete a goal's heading from `GOALS.md`, run the loop, and confirm
the goal node is still there and the next render puts the heading back. Until
that holds, the document is still the source and this is not done.
