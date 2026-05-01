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
detect_shell() -> (shell_type, confidence). Covers bash/zsh/fish/cmd.
Implementation: environment_indexers/cli.py
