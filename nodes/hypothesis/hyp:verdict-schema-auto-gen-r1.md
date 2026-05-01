# hypothesis:verdict-schema-auto-gen-r1

**spawned_by**: idea:domain-schema-registry (fork at iter 8 continuation)
**created**: 2026-05-01
**type**: hypothesis

## claim
Verdict node schemas can be auto-generated from the finite-state verdict taxonomy, producing consistent, validated schemas for all verdict nodes.

## testable claim
A schema-registry schema generated from the verdict taxonomy (proved/disproved/inconclusive_lean_*/pending) with confidence (0.0-1.0), evidence_runs, contradicts, supports fields will validate all existing verdict nodes and catch schema violations.

## rationale
- Verdict taxonomy is well-defined in autoresearch.md
- Auto-generation ensures consistency across all verdict nodes
- Schema validation prevents malformed verdicts
- Schema registry already handles bracket convention for other node types

## experiment_design
1. Define verdict taxonomy schema programmatically
2. Generate bracketed schema "verdict:brackets" following schema-registry conventions
3. Validate against existing verdict nodes
4. Test that schema catches violations (missing fields, invalid confidence, etc.)

## expected_outcome
Auto-generated schema validates all existing verdict nodes without errors (proved if ≥95% pass)

## risks
- Existing verdict nodes may not conform to schema
- May need backward-compatible migration

## status
pending
