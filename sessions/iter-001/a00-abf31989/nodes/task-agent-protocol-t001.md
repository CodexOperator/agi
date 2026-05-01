# task:agent-protocol-t001

**type**: task  
**parent**: hypothesis:agent-protocol-r1  
**spawned_by**: agent:a00-abf31989 (iter 1)  

## goal
Implement a minimal subagent script that:
1. Constructs a valid verdict tuple: `{verdict: "pending", confidence: 0.5, evidence_runs: ["run-001"], contradicts: [], supports: []}`
2. Writes it to a `verdicts/` directory as JSON
3. Validates schema on write (exit 0 if valid, exit 1 if malformed)

## acceptance criteria
- `python3 verdict_emitter.py` exits 0
- Output file `verdicts/run-001.json` exists with valid schema
- Schema fields: verdict ∈ {proved,disproved,inconclusive_lean_proved:inconclusive_lean_disproved,pending}, confidence ∈ [0,1], evidence_runs: list, contradicts: list, supports: list

## run log
<run>
  command: mkdir -p /home/ubuntu/.hermes/agi-tree/sessions/iter-001/a00-abf31989/verdicts && cat > /home/ubuntu/.hermes/agi-tree/sessions/iter-001/a00-abf31989/verdict_emitter.py << 'EOF'
import json, sys
from pathlib import Path

VERDICT_SCHEMA = {
    "verdict": {"type": "string", "enum": ["proved", "disproved", "inconclusive_lean_proved", "inconclusive_lean_disproved", "pending"]},
    "confidence": {"type": "float", "min": 0.0, "max": 1.0},
    "evidence_runs": {"type": "list"},
    "contradicts": {"type": "list"},
    "supports": {"type": "list"},
}

def validate(t):
    for k, rule in VERDICT_SCHEMA.items():
        if k not in t: return False, f"missing {k}"
        v = t[k]
        if rule["type"] == "string" and v not in rule["enum"]: return False, f"{k} not in enum"
        if rule["type"] == "float" and not (0.0 <= v <= 1.0): return False, f"{k} out of range"
        if rule["type"] == "list" and not isinstance(v, list): return False, f"{k} not a list"
    return True, "ok"

verdict = {
    "verdict": "pending",
    "confidence": 0.5,
    "evidence_runs": ["run-001"],
    "contradicts": [],
    "supports": [],
}

valid, msg = validate(verdict)
if not valid:
    print(f"VALIDATION FAILED: {msg}", file=sys.stderr)
    sys.exit(1)

out = Path(__file__).parent / "verdicts" / "run-001.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(verdict, indent=2))
print(f"VERDICT STORED: {out}")
sys.exit(0)
EOF
python3 /home/ubuntu/.hermes/agi-tree/sessions/iter-001/a00-abf31989/verdict_emitter.py
</run>
**result**: VERDICT STORED: /home/ubuntu/.hermes/agi-tree/sessions/iter-001/a00-abf31989/verdicts/run-001.json
**exit**: 0

## verdict_for_hypothesis
**hypothesis**: hypothesis:agent-protocol-r1  
**verdict**: proved  
**confidence**: 0.85  
**evidence_runs**: ["run-001"]  
**contradicts**: []  
**supports**: []  
**notes**: Subagent can emit structurally valid verdict tuples. Schema validation passes. Atomic graph commit is the next step.
