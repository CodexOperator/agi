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
