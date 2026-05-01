---
name: mvp
fields:
  title: {type: str}
  parents: {type: list}        # experiment ids
  children: {type: list}       # outcome ids
  source_files: {type: list}   # paths to actual code
  tests_pass: {type: bool}
  commit_hash: {type: str}
  tags: {type: list}
validation:
  required: [title, source_files]
  types:
    tests_pass: bool
---

# mvp

Minimum viable production code snippet. Points to actual source files and the commit that landed them. Children are outcome nodes (i/o-doc fusion).

ID prefix: `mvp:<short-slug>`.
