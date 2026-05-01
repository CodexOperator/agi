"""R1 tests: skill installation via experiment-runner path.

Canonical tests live at tests/skill/test_skill_installation.py.
This file re-exports them so the experiment-runner's test_r<n>.py convention finds them.
"""
import sys
from pathlib import Path

# Import from canonical location
canonical_test = Path(__file__).resolve().parents[2] / "skill" / "test_skill_installation.py"
sys.path.insert(0, str(canonical_test.parent))
import test_skill_installation

# Re-export all public names
TestSkillInstallation = test_skill_installation.TestSkillInstallation
_dir_sha = test_skill_installation._dir_sha
_install_skill = test_skill_installation._install_skill
