#!/usr/bin/env python3
"""exp-a01-7031af17-449ecb-r11-path-safety.py — graph-core R11 Path Safety

Hypothesis: PathValidator correctly enforces project-root sandboxing.
Verifies: (1) PathValidator class methods work, (2) loader wires in path safety.

Expected result: DISPROVED — loader does NOT call safe_path() before opening files.
"""
import sys
import tempfile
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from graph_core.paths import PathValidator, safe_path, safe_relative_path
from graph_core.errors import PathOutsideProjectError

# ── Test data ───────────────────────────────────────────────────────────────
project_root = ROOT  # the agi-tree root
pv = PathValidator(project_root)

passed = 0
failed = 0
checks = []

def check(cond: bool, name: str, detail: str = ""):
    global passed, failed
    if cond:
        passed += 1
        checks.append(f"  PASS  {name}")
    else:
        failed += 1
        checks.append(f"  FAIL  {name}: {detail}")

# ── Criterion 1: validate() rejects escape ──────────────────────────────────
try:
    pv.validate("../escape")
    check(False, "criterion_1_validate_rejects_escape", "no error raised")
except PathOutsideProjectError:
    check(True, "criterion_1_validate_rejects_escape")
except Exception as e:
    check(False, "criterion_1_validate_rejects_escape", f"wrong error: {type(e).__name__}: {e}")

# ── Criterion 2: validate() accepts internal path ──────────────────────────
try:
    result = pv.validate("./nodes/idea/test.md")
    check(result.is_absolute(), "criterion_2_validate_accepts_internal", f"returned {result}")
except Exception as e:
    check(False, "criterion_2_validate_accepts_internal", f"{type(e).__name__}: {e}")

# ── Criterion 3: validate_relative() rejects absolute ─────────────────────
try:
    pv.validate_relative("/etc/passwd")
    check(False, "criterion_3_validate_relative_rejects_absolute", "no error raised")
except PathOutsideProjectError:
    check(True, "criterion_3_validate_relative_rejects_absolute")
except Exception as e:
    check(False, "criterion_3_validate_relative_rejects_absolute", f"wrong error: {type(e).__name__}: {e}")

# ── Criterion 4: validate_relative() accepts relative path ────────────────
try:
    result = pv.validate_relative("subdir/node.md")
    check(result.is_absolute(), "criterion_4_validate_relative_accepts_relative", f"returned {result}")
except Exception as e:
    check(False, "criterion_4_validate_relative_accepts_relative", f"{type(e).__name__}: {e}")

# ── Criterion 5: safe_path() module function works ──────────────────────────
from graph_core.paths import set_project_root
set_project_root(project_root)
try:
    result = safe_path("../escape2")
    check(False, "criterion_5_safe_path_rejects_escape", "no error raised")
except PathOutsideProjectError:
    check(True, "criterion_5_safe_path_rejects_escape")
except Exception as e:
    check(False, "criterion_5_safe_path_rejects_escape", f"{type(e).__name__}: {e}")

# ── Criterion 6: Loader wires in safe_path() — SOURCE INSPECTION ───────────
loader_source = (SRC / "graph_core" / "loader.py").read_text()
uses_safe_path = "safe_path" in loader_source or "PathValidator" in loader_source
check(uses_safe_path, "criterion_6_loader_wires_safe_path", f"'safe_path' in loader: {uses_safe_path}")

# ── Criterion 7: payload_ref escape raises at load time ───────────────────
# Create a temp node file with payload_ref pointing outside project root
with tempfile.TemporaryDirectory() as tmpdir:
    tmpdir = Path(tmpdir)
    # Create a node with a dangerous payload_ref
    node_content = """---
id: "exp:r11-test"
type: experiment
parents: []
payload_ref: "../../../etc/passwd"
---
test body
"""
    node_file = tmpdir / "exp-r11-test.md"
    node_file.write_text(node_content)
    
    # Reset validator to use tmpdir as root
    from graph_core.paths import set_project_root as sp2
    sp2(str(tmpdir))
    
    from graph_core.loader import load_directory
    try:
        graph, _ = load_directory(tmpdir)
        check(False, "criterion_7_payload_ref_escape_raises", "loader accepted dangerous payload_ref without error")
    except PathOutsideProjectError:
        check(True, "criterion_7_payload_ref_escape_raises")
    except Exception as e:
        check(False, "criterion_7_payload_ref_escape_raises", f"{type(e).__name__}: {e}")

# ── Summary ─────────────────────────────────────────────────────────────────
total = passed + failed
print(f"\n=== R11 Path Safety Results ===")
for line in checks:
    print(line)
print(f"\nTotal: {passed}/{total} passed, {failed} failed")

# Key finding
if failed > 0 and not uses_safe_path:
    print("\nKEY FINDING: PathValidator class is correct but NOT wired into loader.")
    print("Criterion 6 (loader uses safe_path) is FALSE — hypothesis is DISPROVED.")

# Exit 0: experiment ran successfully (we EXPECTED disproved, that's the finding)
sys.exit(0)
