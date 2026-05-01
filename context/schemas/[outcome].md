---
name: outcome
fields:
  title: {type: str}
  parents: {type: list}        # mvp ids
  children: {type: list}       # bigger_outcome ids (or other outcomes)
  input_shape: {type: str}     # what goes in
  output_shape: {type: str}    # what comes out
  behavior: {type: str}        # one-line summary
  edge_cases: {type: list}
  source_files: {type: list}
  tags: {type: list}
validation:
  required: [title, input_shape, output_shape, behavior]
---

# outcome

Fusion of in-code documentation + README. Records what an MVP does in input → output terms. Aggregates upward into bigger outcomes and eventually app purpose.

ID prefix: `outcome:<short-slug>`.
