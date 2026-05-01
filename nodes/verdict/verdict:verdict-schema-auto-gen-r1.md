# verdict:verdict-schema-auto-gen-r1

**spawned_by**: hyp:verdict-schema-auto-gen-r1
**created**: 2026-05-01
**experiment**: exp-verdict-schema-auto-gen-r1.py

## verdict
**proved**

## confidence
0.88

## evidence_runs
- iter-8-a00-7ef61010: schema_enforcement=87.5%, validation_rate=0% (existing nodes need migration)

## description
Verdict node schemas CAN be auto-generated from the finite-state verdict taxonomy. Schema enforcement works at 87.5% (catches invalid verdict values and out-of-range confidence).

However, existing verdict nodes don't conform to the schema (missing `verdict` field in frontmatter). They contain verdict content in the body instead. Migration needed.

Schema fields defined:
- verdict: enum [proved, disproved, inconclusive_lean_proved, inconclusive_lean_disproved, pending]
- confidence: 0.0-1.0
- evidence_runs: array
- contradicts: array
- supports: array

## supports
- idea:domain-schema-registry chain extension
- Verdict taxonomy in autoresearch.md is machine-readable

## contradicts
- None

## next_steps
- Migrate existing verdict nodes to add verdict/confidence/evidence_runs fields
- Register [verdict] schema with schema-registry
- Add validation to verdict emission process
