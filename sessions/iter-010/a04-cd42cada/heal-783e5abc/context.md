# HEALER for hung agent a04-cd42cada (iter 10)

The original agent timed out. Diagnose what blocked it and patch.

## Original Agent Record
```json
{
  "id": "a04-cd42cada",
  "slot": 4,
  "level": "small",
  "target": "idea:domain-chain-engine",
  "pid": 1100712,
  "started_at": 1777621027,
  "status": "running",
  "context_file": "/home/ubuntu/.hermes/agi-tree/sessions/iter-010/a04-cd42cada/context.md",
  "log_file": "/home/ubuntu/.hermes/agi-tree/sessions/iter-010/a04-cd42cada/output.log",
  "command": "/home/ubuntu/.npm-global/bin/pi --append-system-prompt @/home/ubuntu/.hermes/agi-tree/sessions/iter-010/a04-cd42cada/context.md --append-system-prompt 'You are agent a04-cd42cada on iteration 10. When complete, run: python3 /home/ubuntu/autoresearch-tree/extensions/autoresearch-tree/bin/cli.py done 10 a04-cd42cada --verdict <state> --confidence <0..1> --node-id <id>. Stay within zoom scope; do NOT wander.' --append-system-prompt @/home/ubuntu/autoresearch-tree/extensions/autoresearch-tree/lib/agent-prompt.md 'Begin iteration 10 as agent a04-cd42cada. Read your zoom context, do the work, signal done.'"
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
   python3 /home/ubuntu/autoresearch-tree/extensions/autoresearch-tree/bin/cli.py done 10 a04-cd42cada --verdict pending --confidence 0.0 \
     --notes "healed by heal-783e5abc: <one-line diagnosis>"
   ```
   (Use the ORIGINAL `a04-cd42cada`, not your healer id, so the manifest closes out.)

Stay surgical. Don't refactor unrelated code.
