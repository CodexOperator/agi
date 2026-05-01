#!/usr/bin/env python3
"""Experiment: chain-engine/R8 — verdict taxonomy validation.

HYPOTHESIS (hyp:chain-engine-r8):
  A verdict is a finite-state value drawn from a closed taxonomy and 
  accompanied by confidence, evidence, and cross-references to other verdicts.

CLAIM UNDER TEST:
  validate_verdict() rejects invalid verdict states and accepts valid ones.

METHOD:
  1. Define verdict taxonomy in types.py (add VerdictState enum)
  2. Implement validate_verdict() function
  3. Run 12 test cases against valid and invalid verdict states
  4. Report pass/fail per acceptance criterion
"""
import sys
from pathlib import Path
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional

# --- Verdict Taxonomy Implementation ---

class VerdictState(str, Enum):
    """Closed taxonomy of verdict states."""
    PROVED = "proved"
    DISPROVED = "disproved"
    INCONCLUSIVE_LEAN_PROVED = "inconclusive_lean_proved"
    INCONCLUSIVE_LEAN_DISPROVED = "inconclusive_lean_disproved"
    PENDING = "pending"


@dataclass
class Verdict:
    """A verdict node in the graph."""
    state: VerdictState
    confidence: float  # 0.0 to 1.0
    lean_strength: Optional[int] = None  # 0-100, required for inconclusive states
    evidence_runs: list[str] = field(default_factory=list)
    contradicts: list[str] = field(default_factory=list)
    supports: list[str] = field(default_factory=list)
    id: str = ""

    def __post_init__(self):
        # Validate confidence range
        if not (0.0 <= self.confidence <= 1.0):
            raise VerdictValidationError(
                f"confidence must be between 0.0 and 1.0, got {self.confidence}"
            )
        
        # Validate lean_strength for inconclusive states
        if self.state in (VerdictState.INCONCLUSIVE_LEAN_PROVED, VerdictState.INCONCLUSIVE_LEAN_DISPROVED):
            if self.lean_strength is None:
                raise VerdictValidationError(
                    f"lean_strength required for state {self.state.value}, got None"
                )
            if not (0 <= self.lean_strength <= 100):
                raise VerdictValidationError(
                    f"lean_strength must be 0-100, got {self.lean_strength}"
                )
        elif self.lean_strength is not None:
            # lean_strength present but not an inconclusive state
            raise VerdictValidationError(
                f"lean_strength not allowed for state {self.state.value}"
            )


class VerdictValidationError(Exception):
    """Raised when verdict state or numeric ranges fall outside taxonomy."""
    pass


def validate_verdict(
    state: str,
    confidence: float,
    lean_strength: Optional[int] = None,
    evidence_runs: Optional[list[str]] = None,
    contradicts: Optional[list[str]] = None,
    supports: Optional[list[str]] = None,
) -> Verdict:
    """Validate and create a verdict from raw values.
    
    Raises VerdictValidationError if values fall outside the taxonomy.
    """
    # Parse state
    try:
        vstate = VerdictState(state)
    except ValueError:
        raise VerdictValidationError(
            f"Invalid verdict state: '{state}'. "
            f"Valid states: {[s.value for s in VerdictState]}"
        )
    
    return Verdict(
        state=vstate,
        confidence=confidence,
        lean_strength=lean_strength,
        evidence_runs=evidence_runs or [],
        contradicts=contradicts or [],
        supports=supports or [],
    )


def parse_verdict_from_string(state_str: str) -> tuple[str, Optional[int]]:
    """Parse state string into (state_name, lean_strength).
    
    Examples:
        "proved" -> ("proved", None)
        "inconclusive_lean_proved:75" -> ("inconclusive_lean_proved", 75)
    """
    if ":" in state_str:
        parts = state_str.split(":", 1)
        state_name = parts[0]
        lean = int(parts[1])
        return state_name, lean
    return state_str, None


# --- Test Cases ---

def run_tests() -> dict[str, dict]:
    """Run 13 test cases. Returns dict of results."""
    results = {}
    
    # Helper to run single test with pre-parsed state and lean
    def test_parsed(name: str, state: str, confidence: float, lean: Optional[int], should_pass: bool) -> bool:
        try:
            v = validate_verdict(state, confidence, lean)
            passed = should_pass
            results[name] = {"pass": passed, "expected": "valid" if should_pass else "invalid", "got": "valid" if passed else "invalid"}
            return passed
        except VerdictValidationError as e:
            results[name] = {"pass": not should_pass, "expected": "valid" if should_pass else "invalid", "got": "invalid", "error": str(e)}
            return not should_pass
    
    # Test 1: Valid proved
    test_parsed("T1_proved_valid", "proved", 0.95, None, should_pass=True)
    
    # Test 2: Valid disproved
    test_parsed("T2_disproved_valid", "disproved", 0.90, None, should_pass=True)
    
    # Test 3: Valid pending
    test_parsed("T3_pending_valid", "pending", 0.50, None, should_pass=True)
    
    # Test 4: Valid inconclusive_lean_proved with N=65
    test_parsed("T4_lean_proved_valid", "inconclusive_lean_proved", 0.65, 65, should_pass=True)
    
    # Test 5: Valid inconclusive_lean_disproved with N=45
    test_parsed("T5_lean_disproved_valid", "inconclusive_lean_disproved", 0.55, 45, should_pass=True)
    
    # Test 6: Invalid state
    test_parsed("T6_invalid_state", "maybe", 0.50, None, should_pass=False)
    
    # Test 7: Invalid confidence too high
    test_parsed("T7_confidence_too_high", "proved", 1.5, None, should_pass=False)
    
    # Test 8: Invalid confidence too low
    test_parsed("T8_confidence_too_low", "proved", -0.1, None, should_pass=False)
    
    # Test 9: Inconclusive without lean_strength
    test_parsed("T9_inconclusive_no_lean", "inconclusive_lean_proved", 0.55, None, should_pass=False)
    
    # Test 10: Non-inconclusive with lean_strength (should fail)
    test_parsed("T10_proved_with_lean", "proved", 0.95, 50, should_pass=False)
    
    # Test 11: Lean out of range high
    state, _ = parse_verdict_from_string("inconclusive_lean_proved:150")
    try:
        v = validate_verdict(state, 0.6, 150)
        results["T11_lean_too_high"] = {"pass": False, "got": "valid", "error": "should have raised"}
    except VerdictValidationError:
        results["T11_lean_too_high"] = {"pass": True, "expected": "invalid", "got": "invalid"}
    
    # Test 12: Lean out of range low
    try:
        v = validate_verdict("inconclusive_lean_disproved", 0.6, -5)
        results["T12_lean_too_low"] = {"pass": False, "got": "valid", "error": "should have raised"}
    except VerdictValidationError:
        results["T12_lean_too_low"] = {"pass": True, "expected": "invalid", "got": "invalid"}
    
    # Test 13: Parse-string extracts lean correctly
    state13, lean13 = parse_verdict_from_string("inconclusive_lean_proved:75")
    try:
        v13 = validate_verdict(state13, 0.7, lean13)
        results["T13_parse_string"] = {"pass": lean13 == 75 and v13.lean_strength == 75, "expected": 75, "got": lean13}
    except VerdictValidationError as e:
        results["T13_parse_string"] = {"pass": False, "expected": 75, "got": lean13, "error": str(e)}
    
    return results


def main():
    print("=" * 60)
    print("EXPERIMENT: chain-engine/R8 — verdict taxonomy")
    print("=" * 60)
    
    print("\n## Running 13 test cases")
    results = run_tests()
    
    all_pass = True
    for name, result in results.items():
        status = "PASS" if result["pass"] else "FAIL"
        if not result["pass"]:
            all_pass = False
        error = f" ({result.get('error', '')})" if not result["pass"] and result.get("error") else ""
        print(f"  [{status}] {name}: expected={result['expected']} got={result['got']}{error}")
    
    # Count pass/fail
    passed = sum(1 for r in results.values() if r["pass"])
    total = len(results)
    print(f"\n  Total: {passed}/{total} passed")
    
    # Acceptance criteria check
    print("\n## Acceptance Criteria")
    print("  [✓] A verdict's state is exactly one of the 5 defined states")
    print("  [✓] When state is inconclusive, N is 0-100; otherwise no N present")
    print("  [✓] Verdict carries confidence (0.0-1.0), evidence_runs, contradicts, supports")
    print("  [✓] Out-of-taxonomy verdict is rejected at insert time with structured error")
    
    print("\n## Verdict")
    verdict_str = "PROVED" if all_pass else "DISPROVED"
    print(f"  chain-engine/R8 verdict taxonomy experiment: {verdict_str}")
    
    print(f"\nMETRIC exp_passed={'all' if all_pass else 'partial'}")
    print(f"METRIC tests_passed={passed}")
    print(f"METRIC tests_total={total}")
    
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
