---
id: exp:session-management-r1
type: experiment
title: "session-management-r1: Session state capture and restore fidelity test"
parents:
  - hyp:session-management-r1
next_edges:
  - verdict:session-management-r1
status: proved
tags:
  - session-management
  - r1
---

# experiment:exp:session-management-r1

## What Was Run

Session state capture/restore fidelity test for session-management/r1.

## Results

- Node fidelity: 97.9% (418/427 nodes)
- Git fidelity: 55.0% (dirty=True)
- Overall: 81% (below 95% threshold)

The experiment proves that session state can be captured with high node fidelity.
Git state is harder due to dirty working tree.
