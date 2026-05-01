---
id: idea:domain-cli-invocation
title: "CLI Invocation: Shell Command Detection and Execution"
type: idea
domain: cli-invocation
tags:
  - cli
  - shell
  - command
  - execution
  - environment
next_edges:
  - hyp:cli-invocation-r1
---

# Domain: CLI Invocation

## Concept
Detect and execute shell commands from the agi-tree system. Understand how environment indexers invoke CLI tools and how to detect shell contexts.

## Motivation
- environment-indexers domain needs CLI invocation capabilities
- Shell detection is hard (bash vs zsh vs fish vs cmd)
- Need to detect interactive vs non-interactive shells
- Cross-platform command execution

## Child Hypotheses

1. **hyp:cli-invocation-r1**: Can reliably detect current shell type from environment
2. **R2**: Can execute commands and capture output reliably
3. **R3**: Can detect interactive vs non-interactive shell state
