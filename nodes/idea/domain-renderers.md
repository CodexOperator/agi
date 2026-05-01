---
confidence: 1.0
id: "idea:domain-renderers"
scale: big
status: open
tags:
  - domain
  - seed
title: "Domain: renderers"
type: idea
next_edges:
  - hyp:renderers-r1
---

Multi-format renderers that turn a graph into human-readable views. All renderers consume a single shared internal representation, so a new renderer is one class implementing a single method. The same representation is also consumed by the embeddings kit, which is what keeps visualization and embedding isomorphic. Renderers are pure functions: same input, same output, no side effects.
