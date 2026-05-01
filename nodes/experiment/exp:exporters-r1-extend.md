---
id: exp:exporters-r1-extend
title: "Experiment: Exporters R1 Extended"
type: experiment
status: proved
verdict: proved
confidence: 1.0
parents:
  - hyp:exporters-r1
  - verdict:exporters-r1
tags:
  - exporters
  - chain-extension
  - r1-extend
next_edges:
  - verdict:exporters-r1-extend
---

# Experiment: Exporters R1 Extended

Extends the exporters chain from 8 to 10 hops via verdict→experiment→verdict pattern.

## Chain Extension

- verdict:exporters-r1 → exp:exporters-r1-extend → verdict:exporters-r1-extend → mvp:exporters-r1

This adds 2 more hops to the chain, demonstrating the verdict→experiment→verdict pattern is stackable.
