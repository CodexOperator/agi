---
acceptance_criteria:
  - R1.1 (new skill at documented path inside existing autoresearch skill repository)
  - R1.2 (no file under autoresearch-create or autoresearch-finalize modified or removed)
  - R1.3 (adding the skill is one new directory of files
  - not a patch)
  - R1.4 (after installation
    both new and original skills appear in enumeration)
blocked_by: []
cavekit_req: autoresearch-tree-skill/R1
effort: M
id: "task:t-076"
parents:
  - hyp:autoresearch-tree-skill-r1
status: done
tags:
  - M
  - tier--1
tier: -1
title: "T-076: Skill installation in forked skill repository"
type: task
---

**Description:** Place the new skill at `agi-tree/skills/autoresearch-tree/` with its own SKILL.md, scripts/, and references/. Document the installation path and confirm the layout doesn't touch existing skills. Provide an `install-skill.sh` that copies the directory into a target skill repo without modifying anything else.

**Files:** `agi-tree/skills/autoresearch-tree/SKILL.md`, `agi-tree/skills/autoresearch-tree/scripts/`, `agi-tree/skills/autoresearch-tree/references/`, `agi-tree/skills/autoresearch-tree/install-skill.sh`, `agi-tree/tests/skill/test_skill_installation.py`

**Test Strategy:** Test installs into a tempdir mirroring an existing skill repo with create/finalize subdirs; asserts those are byte-equal before and after install and the new skill appears in `find skills/ -name SKILL.md` enumeration.

**Validation:** All 6 tests in `tests/skill/test_skill_installation.py` pass:
- test_r11_new_skill_at_documented_path PASSED
- test_r12_existing_skills_untouched PASSED
- test_r13_one_new_directory PASSED
- test_r14_skill_enumeration PASSED
- test_install_existing_is_noop PASSED
- test_install_missing_target_errors PASSED

Experiment: `experiment:autoresearch-tree-skill-r1-e1`
Verdict: `verdict:autoresearch-tree-skill-r1-e1-v1` (proved, confidence 0.95)
