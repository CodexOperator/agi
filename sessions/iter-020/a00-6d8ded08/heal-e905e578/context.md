# HEALER for hung agent a00-6d8ded08 (iter 20)

The original agent timed out. Diagnose what blocked it and patch.

## Original Agent Record
```json
{
  "id": "a00-6d8ded08",
  "slot": 0,
  "level": "big",
  "target": null,
  "pid": 1185410,
  "started_at": 1777646255,
  "status": "running",
  "context_file": "/home/ubuntu/.hermes/agi-tree/sessions/iter-020/a00-6d8ded08/context.md",
  "log_file": "/home/ubuntu/.hermes/agi-tree/sessions/iter-020/a00-6d8ded08/output.log",
  "command": "/home/ubuntu/.npm-global/bin/pi --append-system-prompt @/home/ubuntu/.hermes/agi-tree/sessions/iter-020/a00-6d8ded08/context.md --append-system-prompt 'You are agent a00-6d8ded08 on iteration 20. When complete, run: python3 /home/ubuntu/autoresearch-tree/extensions/autoresearch-tree/bin/cli.py done 20 a00-6d8ded08 --verdict <state> --confidence <0..1> --node-id <id>. Stay within zoom scope; do NOT wander.' --append-system-prompt @/home/ubuntu/autoresearch-tree/extensions/autoresearch-tree/lib/agent-prompt.md 'Begin iteration 20 as agent a00-6d8ded08. Read your zoom context, do the work, signal done.'"
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
   python3 /home/ubuntu/autoresearch-tree/extensions/autoresearch-tree/bin/cli.py done 20 a00-6d8ded08 --verdict pending --confidence 0.0 \
     --notes "healed by heal-e905e578: <one-line diagnosis>"
   ```
   (Use the ORIGINAL `a00-6d8ded08`, not your healer id, so the manifest closes out.)

Stay surgical. Don't refactor unrelated code.
