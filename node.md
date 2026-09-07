---
id: experiment:a00-25b153f9-453c86
mint_id: e2aabe33963241a2a2d31486148dfaa5
type: experiment
parents:
  - hypothesis:l3w4-workflows-config-maxxed
next_edges: []
confidence: 0.8
evidence_runs:
  - experiment:a00-25b153f9-453c86
loop: hypothesis:l3w4-workflows-config-maxxed@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: ae90d3e7afb0c1af
season: 2
title: "L3.31 — live pi-harness draft: the stub is dead"
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-25b153f9-453c86

## Experiment

Sliced `l3w4-workflows-config-maxxed` forward on its one unproven, load-bearing
piece: **the pi-harness live path of `workflow.py run`**. The L3.27 run had
built the config-maxxed runner, stage manifests, config rows and 5 build
nodes and stopped at `inconclusive_lean_proved:80` because a live dispatch was
unexercised. L3.28 (Belam VII) then measured the pi path was a *stub*: it called
`dispatch.py` with a bogus `key:label` `--target` and a `workflow_stage`
`--template` that exists nowhere, printed the resolved model/effort and never
passed them (or the stage prompt) to the child — `--dry-run` looked green
because it returns before any of that. This kid made the path real.

Root cause found beyond the three reported defects: the `.json` stage
manifests carried **no prompt text at all**, so the pi runner physically could
not execute a stage even with the dispatch call fixed. So the work was:

1. **Added a `prompt` template to every stage** in `drafting.json` and
   `review.json` (draft, critic, global-checks, review), derived from the
   `.js` script prompts and parameterized over the run args (`{scratch}`,
   `{slug}`, `{parent}`, `{scope}`). One form, read by both harnesses — the
   config-maxxed contract applied to the prompt, not just the knobs.
2. **Rewrote the pi branch of `run_workflow`** (`workflow.py`) to execute each
   stage for real: `_run_stage_pi` spawns the pi binary headlessly
   (`pi -p --provider openrouter --model <resolved> --thinking <effort-mapped>
   "<rendered prompt>"`), captures stdout, parses the last JSON object
   (`_parse_last_json`, tolerant) and validates it against the stage schema
   (`validate_return`). Resolved model/effort now actually reach the child;
   effort maps to a pi thinking level (`max/high→high, low→low, else medium`,
   or a `--args thinking` override).
3. **Render-safety fix**: the prompt's inline JSON schema braces (`{"a":1}`)
   are not str.format placeholders; a regex over `{word}` keys expands only
   real placeholders and passes schema braces through literally (the first
   live attempt died on `str.format_map`).
4. **Credential hygiene**: the pi child env is scrubbed of all
   Claude-Code-injected Anthropic credentials (`_pi_env`), the same policy
   `dispatch.py` applies, so a pi run bills the configured provider (openrouter
   = pay-per-token, zero subscription tokens) — exactly the owner item 32 ask.
5. **`_expand_stages` now carries the repeat item** (`_repeat_item`) so each
   concrete stage's prompt is rendered per item.

Tests: +7 in `test_workflow.py` (prompt render incl. repeat-item fields and
schema-brace survival, last-JSON parse tolerance, effort→thinking map,
`_run_stage_pi` passes resolved model + rendered prompt + scrubbed env, and
rejects schema-violating returns). Full repo suite untouched-green.

**Then the live proof** — the gate Belam VII named:

```
workflow.py run drafting --harness pi --args '{"model":"~z-ai/glm-flash-latest",
  "scratch":"/tmp/wf-live","briefs":[{"slug":"wf-liveproof",...}]}'
```

Exit **0**. Both stages (`draft:wf-liveproof`, `critic`) returned schema-valid
JSON (`[ok]` lines), and the draft stage wrote a real 5.7 KB markdown brief to
`/tmp/wf-live/wf-liveproof.md`. The critic then fixed it in place and returned
`ok:true`. OpenRouter, cheap model, zero subscription tokens.

## Evidence

Live run (abridged; full transcript in body):

```
$ python3 extensions/agi/bin/workflow.py run drafting --harness pi \
    --args '{"model":"~z-ai/glm-flash-latest","scratch":"/tmp/wf-live",...}'
# [dispatch] draft:wf-liveproof :: role=drafter model=~z-ai/glm-flash-latest effort=max
$ /home/ubuntu/.npm-global/bin/pi -p --provider openrouter --model ~z-ai/glm-flash-latest --thinking high "…draft prompt…"
[ok] draft:wf-liveproof -> {"body_path": "/tmp/wf-live/wf-liveproof.md", "slug": "wf-liveproof", …}
# [dispatch] critic :: role=critic model=~z-ai/glm-flash-latest effort=max
[ok] critic -> {"fixed": […], "ok": true, …}
[summary] workflow=drafting harness=pi stages=2 all schema-valid
```

`ls /tmp/wf-live/` → `-rw-rw-r-- wf-liveproof.md  5791 bytes`. The draft is a
real house-style brief (CLAIM / WHY / FILES / DESIGN / TESTS / GATE / NOT IN
SCOPE / SOURCE) that correctly labels its own non-owner decisions
"(director proposal)".

Meter: the run spent only on OpenRouter — `OPENROUTER_API_KEY` was set,
`ANTHROPIC_API_KEY` was not, and `_pi_env` strips any anthropic credential
anyway, so no subscription token was touched.

Full repo suite: `python3 -m pytest extensions/agi/tests/ -q` →
**1992 passed, 1 skipped, 0 failed**. `test_workflow.py` 15 passed.

## Agent Notes
This run closes Belam VII's live gate and with it the biggest open item on
`l3w4-workflows-config-maxxed`: a real, schema-valid, zero-subscription draft
written to disk by `workflow.py run … --harness pi`, exit 0. `cli.py done` will
stamp the verdict. Remaining before `proved`: Claude Code name-registry
resolution of `Workflow({name})` through the symlinks (runtime behavior not
exercised here), and the .js harness run — both static/CC-side, unaffected by
this change.

## Agent Notes
Fixed workflow.py pi-harness stub (bogus dispatch target/nonexistent template/unpassed knobs + prompts missing from manifests): stage prompts added to drafting.json/review.json, _run_stage_pi executes each stage headlessly with resolved model/thinking/scrubbed env, validates JSON return; live run drafting --harness pi wrote real draft file /tmp/wf-live/wf-liveproof.md, exit 0, both returns schema-valid, openrouter (zero subscription tokens). Full suite 1992 passed. Remaining: CC name-registry resolution.
