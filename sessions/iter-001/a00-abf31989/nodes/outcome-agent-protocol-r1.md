# outcome:agent-protocol-r1

**type**: outcome  
**parent**: verdict:agent-protocol-r1  
**spawned_by**: agent:a00-abf31989 (iter 1)  

## MVP
`verdict_emitter.py` — minimal subagent that emits structured verdict tuples

## input_shape
No input args. Self-contained — constructs verdict tuple internally.

## output_shape
- stdout: `"VERDICT STORED: /path/to/run-001.json"`
- exit 0: valid schema, file written
- exit 1: validation failure with stderr message

## behavior
1. Defines VERDICT_SCHEMA with field-level validation rules
2. Constructs default verdict: `{verdict: "pending", confidence: 0.5, evidence_runs: ["run-001"], contradicts: [], supports: []}`
3. Validates all fields against schema (enum, range, type checks)
4. Writes JSON to `verdicts/run-001.json` atomically
5. Exits 0 on success, 1 on validation failure

## edge_cases
- Missing fields → exit 1
- confidence out of [0,1] → exit 1
- verdict not in enum → exit 1
- Non-list contradicts/supports → exit 1
- Output dir doesn't exist → mkdir -p before write

## code_location
`/home/ubuntu/.hermes/agi-tree/sessions/iter-001/a00-abf31989/verdict_emitter.py`

## bigger_outcome (planned)
- outcome:agent-protocol-r1 → bigger_outcome:agent-protocol-atomicity (atomic commit semantics)
- bigger_outcome:agent-protocol-atomicity → bigger_outcome:agent-protocol-fork-detection (conflict resolution)
- → app_purpose:verifiable-multi-agent-coordination
