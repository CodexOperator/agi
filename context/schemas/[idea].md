---
name: idea
fields:
  title: {type: str}
  scale: {type: str}      # "big" | "small"
  parents: {type: list}
  children: {type: list}
  tags: {type: list}
  confidence: {type: float}
  status: {type: str}     # "open" | "extended" | "abandoned"
validation:
  required: [title, scale]
  types:
    title: str
    scale: str
  regex:
    scale: '^(big|small)$'
---

# idea

Big or small concept seed. Spawns one or more hypotheses. May fork mid-chain.

- **big** = top-level new chain, broad
- **small** = granular extension of existing chain

ID prefix: `idea:<short-slug>` (e.g. `idea:capillary-dag-memory`).
