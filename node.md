---
id: experiment:a00-4e293497-87fd0c
mint_id: f06d786fec084a4ca043f5f6363f0aae
type: experiment
parents:
  - hypothesis:l2w2-telemetry-stamps
next_edges: []
confidence: 0.8
scaffold_hash: 77e3712110c7718e
title: Investigate telemetry stamp sources for cli.py done
verdict: inconclusive_lean_proved:80
---
# experiment:a00-4e293497-87fd0c

## Experiment

Investigated three candidate telemetry sources for stamping `tokens_in`, `tokens_out`, `cost_usd` on a kid's node at `cli.py done` time, as specified in goal:g16 / section 5 of the season-ladder brief.

### Source A: pi session logs (CONFIRMED)

Pi writes per-session JSONL files to `~/.pi/agent/sessions/--<project-slug>--/<uuid>.jsonl`. Each `type:message` record contains:
- `message.usage.input` (prompt tokens)
- `message.usage.output` (completion tokens)
- `message.usage.cost.total` (cost in USD, float)
- `message.model` (the model used)
- `message.responseId` (generation id, usable for OpenRouter lookup)

**Verification** — read two session files from the current project:
- `2026-09-06T09-50-51-291Z...jsonl`: 16 msgs, 98464 tokens_in, 9191 tokens_out, $0.025210
- `2026-09-06T09-50-52-491Z...jsonl`: 14 msgs, 91003 tokens_in, 11355 tokens_out, $0.018784

The model field also identifies which model was used (deepseek/deepseek-v4-flash).

**Challenge**: need to correlate a pi session UUID to an agent id. The pi process is spawned in the session dir, writing to `output.log`. If pi prints its session UUID at startup (or to stderr which goes to output.log), that UUID maps to the JSONL file. Otherwise, match by process pid + start time.

### Source B: OpenRouter provisioning API (PARTIAL)

`provisioning.py status` calls `GET /keys` and returns cumulative `usage` per key (total USD spent, not per-generation).
- Shows total spend per key: e.g. this agent's key `agi-iterL2.06-kid-a00-4e293497 used=0.002345501`
- Does NOT show token counts
- Does NOT show per-generation breakdown
- Accessible with the provisioning key only, not the kid's runtime key

**Limitation**: cumulative spend only; cannot extract per-session tokens_in/out without additional API calls.

### Source C: OpenRouter per-generation endpoint (NOT VERIFIED)

`GET https://openrouter.ai/api/v1/generation?id=<generation_id>`
- Would need the `responseId` from pi's message log
- The responseId format is `gen-<timestamp>-<random>`
- Requires the per-spawn minted key to authenticate
- Would give per-generation tokens_in, tokens_out, cost

**Not verified against live API** — requires a completed generation and an API call.

### Source D: accepted_diff_bytes (DEFERRED)

This is a parent-time concept: the parent accepts a kid's work and records the byte size of the node file plus its payload. Not stampable at `cli.py done` — that's the kid's signal. Belongs at parent acceptance (`--owns` path).

## Evidence

### pi session log showing usage data (real record):
```json
{
  "type": "message",
  "message": {
    "role": "assistant",
    "model": "deepseek/deepseek-v4-flash",
    "usage": {
      "input": 2403,
      "output": 1690,
      "cost": {
        "input": 0.001021275,
        "output": 0.0043095,
        "total": 0.010262135
      }
    },
    "responseId": "gen-1788682389-KtdvpYNMAgFQRSFXW2wy"
  }
}
```

### provisioning.py status output:
```
provisioning: available  keys_visible=7  engine_minted=6
  outstanding: agi-iterL2.06-kid-a00-4e293497 used=0.002345501 expires=2026-09-06T10:50:49.639Z
```

### pi session aggregated totals (this project):
- 30 messages across 2 sessions: 189467 tokens_in, 20546 tokens_out, $0.043994 total cost
- All via deepseek/deepseek-v4-flash

## Conclusion

Three sources are viable (pi logs = confirmed, provisioning API = partial/aggregate, OpenRouter per-generation = callable with responseId). The pi session log is the most practical source for per-message token/cost data at done time. The correlation from pi session UUID to agent id needs a mechanism (capture UUID from pi's output, or match by pid+time). The `accepted_diff_bytes` part of the hypothesis is a parent-time operation, not stampable at the kid's `done`.

## Agent Notes
Confirmed pi session logs contain tokens_in/tokens_out/cost_usd per message. Read real records from ~/.pi/agent/sessions/. provisioning.py shows cumulative spend. OpenRouter per-generation needs responseId from pi log. Correlation pi session->agent needs mechanism (capture UUID from pi output or match by pid). accepted_diff_bytes is parent-time, not kid-done-time.
