#!/usr/bin/env python3
"""exp-skill-r10-sessionstart-hook.py — smoke test for SessionStart hook + render-context.

Tests hypothesis hyp:autoresearch-tree-skill-r10:
  "SessionStart hook auto-injects ASCII DAG map into CC sessions,
   with 1-hour stale cache and graceful degradation."

Exit 0 = all checks pass.
Exit 1 = any check fails.
"""
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
# Hook lives at the plugin. For agi-tree project, plugin is at the installed path.
PLUGIN_ROOT = Path("/home/ubuntu/.pi/agent/git/github.com/davebcn87/pi-autoresearch/extensions/autoresearch-tree")
HOOK = PLUGIN_ROOT / "hooks" / "cc-session-start.sh"
RENDER_PY = ROOT / "bin" / "render-context.py"

def check(label, cond, detail=""):
    status = "PASS" if cond else "FAIL"
    print(f"[{status}] {label}" + (f" — {detail}" if detail else ""))
    return cond

def run_hook(cwd: Path, env: dict | None = None) -> tuple[int, str, str]:
    """Run cc-session-start.sh and return (exit_code, stdout, stderr)."""
    full_env = dict(os.environ)
    full_env["PWD"] = str(cwd)  # bash needs PWD env var to match cwd
    if env:
        full_env.update(env)
    proc = subprocess.run(
        ["bash", str(HOOK)],
        capture_output=True, text=True,
        cwd=str(cwd),
        env=full_env,
    )
    return proc.returncode, proc.stdout, proc.stderr

def main() -> int:
    results = []

    # ── 1. render-context.py works standalone ────────────────────────────────
    print("\n=== render-context.py standalone ===")
    rc = subprocess.run(
        ["python3", str(RENDER_PY), str(ROOT / "nodes")],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    inj = ROOT / "context" / "INJECTION.md"
    ok_render = check(
        "render-context.py exits 0",
        rc.returncode == 0,
        rc.stderr[:120] if rc.stderr else "",
    )
    results.append(ok_render)

    ok_inj_exists = check("INJECTION.md created", inj.exists())
    results.append(ok_inj_exists)

    if inj.exists():
        inj_text = inj.read_text()
        ok_has_snapshot = check(
            "INJECTION.md has ## graph snapshot",
            "## graph snapshot" in inj_text,
        )
        ok_has_ascii = check(
            "INJECTION.md has ## ASCII view",
            "## ASCII view" in inj_text,
        )
        ok_has_attractive = check(
            "INJECTION.md has ## attractive ideas",
            "## attractive ideas" in inj_text,
        )
        ok_fresh_timestamp = check(
            "INJECTION.md has _generated timestamp",
            "_generated" in inj_text,
        )
        results.extend([ok_has_snapshot, ok_has_ascii, ok_has_attractive, ok_fresh_timestamp])

        # Count lines — hook emits max 80
        lines = inj_text.splitlines()
        # SKILL specifies ASCII renderer ≤200 lines; INJECTION.md may slightly exceed
        # due to extra metadata sections, but the ASCII block itself must be ≤200.
        ascii_start = None
        ascii_end = None
        for i, l in enumerate(lines):
            if l.startswith("```"):
                if ascii_start is None:
                    ascii_start = i + 1
                else:
                    ascii_end = i
                    break
        ascii_block_lines = (ascii_end - ascii_start) if ascii_start and ascii_end else 0
        ok_ascii_bounded = check(
            "ASCII block ≤200 lines",
            ascii_block_lines <= 200,
            f"got {ascii_block_lines}",
        )
        results.append(ok_ascii_bounded)

    # ── 2. Hook: in-project, fresh cache → no regeneration, emits lines ───────
    print("\n=== Hook: in-project, fresh cache ===")
    inj_touch = inj.stat().st_mtime if inj.exists() else time.time()
    os.utime(inj, (inj_touch, inj_touch))  # refresh mtime
    rc2, out2, err2 = run_hook(ROOT)
    ok_hook_silent = check(
        "Hook exits 0 in-project",
        rc2 == 0,
    )
    results.append(ok_hook_silent)

    ok_hook_emits = check(
        "Hook emits lines to stdout in-project",
        len(out2.strip().splitlines()) > 0,
        f"{len(out2.strip().splitlines())} lines",
    )
    results.append(ok_hook_emits)

    # Hook header (~11 lines) + up to 80 lines from INJECTION.md
    # Accept up to 95 (accounting for header variation)
    ok_hook_max95 = check(
        "Hook emits ≤95 lines (header + ≤80 INJECTION lines)",
        len(out2.strip().splitlines()) <= 95,
        f"got {len(out2.strip().splitlines())} lines",
    )
    results.append(ok_hook_max95)

    # ── 3. Hook: in-project, stale cache → regenerates ───────────────────────
    print("\n=== Hook: in-project, stale cache (>1 hour) ===")
    old_mtime = inj_touch - 4000  # 4000 seconds ago (> 1 hour)
    os.utime(inj, (old_mtime, old_mtime))
    # Ensure render-context.py exists at the path the hook expects: PROJECT_ROOT/bin/
    project_bin = ROOT / "bin"
    project_bin.mkdir(exist_ok=True)
    render_target = project_bin / "render-context.py"
    if not render_target.exists():
        render_target.symlink_to(RENDER_PY.resolve())
    rc3, out3, err3 = run_hook(ROOT)
    ok_hook_stale = check(
        "Hook exits 0 with stale cache",
        rc3 == 0,
    )
    results.append(ok_hook_stale)

    # INJECTION.md should be refreshed
    new_mtime = inj.stat().st_mtime
    ok_regenerated = check(
        "INJECTION.md refreshed after stale trigger",
        new_mtime > old_mtime + 100,
        f"old={old_mtime:.0f} new={new_mtime:.0f}",
    )
    results.append(ok_regenerated)

    # ── 4. Hook: outside project tree → exit 0, no output ────────────────────
    print("\n=== Hook: outside project tree ===")
    with tempfile.TemporaryDirectory() as td:
        rc4, out4, err4 = run_hook(Path(td))
        ok_outside_silent = check(
            "Hook exits 0 outside project",
            rc4 == 0,
        )
        results.append(ok_outside_silent)
        ok_no_output = check(
            "Hook emits nothing outside project",
            out4.strip() == "",
            repr(out4[:80]),
        )
        results.append(ok_no_output)

    # ── 5. Hook: find-root via subdirectory ─────────────────────────────────
    print("\n=== Hook: PWD is subdirectory of project ===")
    subdir = ROOT / "context"
    rc5, out5, err5 = run_hook(subdir)
    ok_subdir = check(
        "Hook finds project from subdirectory PWD",
        rc5 == 0 and len(out5.strip()) > 0,
    )
    results.append(ok_subdir)

    # ── Summary ─────────────────────────────────────────────────────────────
    print("\n=== Summary ===")
    passed = sum(results)
    total = len(results)
    print(f"  {passed}/{total} checks passed")
    if all(results):
        print("  RESULT: ALL PASS")
        return 0
    else:
        print("  RESULT: SOME FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
