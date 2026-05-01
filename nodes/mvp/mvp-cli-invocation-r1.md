---
id: mvp:cli-invocation-r1
title: "MVP: CLI Shell Detection"
type: mvp
status: implemented
parents:
  - verdict:cli-invocation-r1
next_edges:
  - outcome:cli-invocation-r1
tags:
  - cli
  - shell
  - detection
---
## MVP: CLI Shell Detection

detect_shell() -> (shell_type: str, confidence: float)
Covers bash/zsh/fish/cmd on Unix/Windows.
