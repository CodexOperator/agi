# HEALER for hung agent a04-48cbb4bc (iter 4)

The original agent timed out. Diagnose what blocked it and patch.

## Original Agent Record
```json
{
  "id": "a04-48cbb4bc",
  "slot": 4,
  "level": "small",
  "target": "idea:domain-autoresearch-tree-skill",
  "pid": 1073239,
  "started_at": 1777616680,
  "status": "running",
  "context_file": "/home/ubuntu/.hermes/agi-tree/sessions/iter-004/a04-48cbb4bc/context.md",
  "log_file": "/home/ubuntu/.hermes/agi-tree/sessions/iter-004/a04-48cbb4bc/output.log",
  "command": "/home/ubuntu/.npm-global/bin/pi --append-system-prompt @/home/ubuntu/.hermes/agi-tree/sessions/iter-004/a04-48cbb4bc/context.md --append-system-prompt 'You are agent a04-48cbb4bc on iteration 4. When complete, run: python3 /home/ubuntu/autoresearch-tree/extensions/autoresearch-tree/bin/cli.py done 4 a04-48cbb4bc --verdict <state> --confidence <0..1> --node-id <id>. Stay within zoom scope; do NOT wander.' --append-system-prompt @/home/ubuntu/autoresearch-tree/extensions/autoresearch-tree/lib/agent-prompt.md 'Begin iteration 4 as agent a04-48cbb4bc. Read your zoom context, do the work, signal done.'"
}
```

## Last 4 KiB of Agent Output
```

```

## Your Task
1. Identify the failure mode: stuck command, missing dep, infinite loop, syntax error, etc.
2. Apply the smallest patch that unblocks it (NEW commit; do not amend).
3. If unfixable in <5 turns, mark this agent's verdict as `pending` with reason.
4. When done:
   ```
   python3 /home/ubuntu/autoresearch-tree/extensions/autoresearch-tree/bin/cli.py done 4 a04-48cbb4bc --verdict pending --confidence 0.0 \
     --notes "healed by heal-12bdfcb4: <one-line diagnosis>"
   ```
   (Use the ORIGINAL `a04-48cbb4bc`, not your healer id, so the manifest closes out.)

Stay surgical. Don't refactor unrelated code.
