---
id: hyp:cli-invocation-r1
title: "R1: Can reliably detect current shell type from environment"
type: hypothesis
parent_idea: idea:domain-cli-invocation
domain: cli-invocation
tags:
  - cli
  - shell
  - detection
  - R1
spawns:
  - task:t-096
status: pending
verdict: pending
---

## Hypothesis

**Claim**: Current shell type (bash/zsh/fish/cmd) can be reliably detected with >90% accuracy using environment variables and parent process inspection.

**Test**:
1. Check $SHELL environment variable
2. Check $0 or ps output
3. Check parent process name
4. Compare detection results across known shell types
5. Measure accuracy against ground truth

**Expected**: >90% detection accuracy.

## Rationale
- $SHELL is usually set correctly on Unix
- ps/ppid can reveal parent shell
- Multiple detection methods provide redundancy

## Failure Mode
- Container environments may not set $SHELL
- Windows has different shell semantics (cmd.exe, PowerShell)
- Detached processes may lose shell context
