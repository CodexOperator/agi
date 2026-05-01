"""T-076 tests: skill installation in forked skill repository.

Acceptance criteria:
  R1.1  New skill placed at documented path inside existing skill repo
  R1.2  No file under autoresearch-create or autoresearch-finalize modified/removed
  R1.3  Adding the skill is one new directory of files (not a patch)
  R1.4  After installation, both new and original skills appear in enumeration
"""

from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import pytest


def _dir_sha(dir_path: Path) -> dict[str, str]:
    """Return {rel_path: sha256_hex} for all files under dir_path."""
    result = {}
    for root, _dirs, files in os.walk(dir_path):
        for name in files:
            full = Path(root) / name
            rel = full.relative_to(dir_path)
            result[str(rel)] = hashlib.sha256(full.read_bytes()).hexdigest()
    return result


def _install_skill(source_skill_dir: Path, target_skill_repo: Path) -> subprocess.CompletedProcess:
    """Run install-skill.sh and return the result."""
    script = source_skill_dir / "install-skill.sh"
    result = subprocess.run(
        [str(script), str(target_skill_repo)],
        capture_output=True,
        text=True,
    )
    return result


class TestSkillInstallation:
    """Tests for install-skill.sh."""

    @pytest.fixture
    def source_skill_dir(self) -> Path:
        """Path to the skill source directory (this repo's skill/autoresearch-tree/)."""
        return Path(__file__).parent.parent.parent / "skill" / "autoresearch-tree"

    @pytest.fixture
    def temp_skill_repo(self, tmp_path: Path) -> Path:
        """Create a tempdir that mirrors a minimal skill repo with create + finalize."""
        repo = tmp_path / "pi-autoresearch"
        skills = repo / "skills"

        # Create two pre-existing (stub) skills
        for stub in ("autoresearch-create", "autoresearch-finalize"):
            stub_dir = skills / stub
            stub_dir.mkdir(parents=True)
            (stub_dir / "SKILL.md").write_text(f"# {stub}\n")
            (stub_dir / "stub.txt").write_text(f"stub content for {stub}\n")

        return repo

    def test_r11_new_skill_at_documented_path(
        self, source_skill_dir: Path, temp_skill_repo: Path
    ) -> None:
        """R1.1: New skill placed at skills/autoresearch-tree/ inside target repo."""
        result = _install_skill(source_skill_dir, temp_skill_repo)
        assert result.returncode == 0, f"install failed: {result.stderr}"

        dest = temp_skill_repo / "skills" / "autoresearch-tree"
        assert dest.exists(), "skill directory not created"
        assert (dest / "SKILL.md").exists(), "SKILL.md missing in installed skill"

    def test_r12_existing_skills_untouched(
        self, source_skill_dir: Path, temp_skill_repo: Path
    ) -> None:
        """R1.2: Files under autoresearch-create and autoresearch-finalize unchanged."""
        # Snapshot hashes of existing skills BEFORE install
        before = _dir_sha(temp_skill_repo / "skills")

        result = _install_skill(source_skill_dir, temp_skill_repo)
        assert result.returncode == 0, f"install failed: {result.stderr}"

        # After install: only the new skill files should appear; originals must be byte-equal
        after = _dir_sha(temp_skill_repo / "skills")
        common_keys = set(before.keys()) & set(after.keys())
        assert before == {k: after[k] for k in common_keys}, "existing skill files were modified"
        # Confirm new files were added (sanity)
        new_keys = set(after.keys()) - set(before.keys())
        assert len(new_keys) > 0, "new skill files not added"

    def test_r13_one_new_directory(
        self, source_skill_dir: Path, temp_skill_repo: Path
    ) -> None:
        """R1.3: Adding the skill creates exactly one new directory."""
        skills_before = set(p.name for p in (temp_skill_repo / "skills").iterdir())

        result = _install_skill(source_skill_dir, temp_skill_repo)
        assert result.returncode == 0, f"install failed: {result.stderr}"

        skills_after = set(p.name for p in (temp_skill_repo / "skills").iterdir())
        new_skills = skills_after - skills_before

        assert new_skills == {"autoresearch-tree"}, f"unexpected new skills: {new_skills - {'autoresearch-tree'}}"

    def test_r14_skill_enumeration(
        self, source_skill_dir: Path, temp_skill_repo: Path
    ) -> None:
        """R1.4: Both new skill and original skills appear in SKILL.md enumeration."""
        _install_skill(source_skill_dir, temp_skill_repo)

        skill_md_files = [
            p.relative_to(temp_skill_repo / "skills")
            for p in (temp_skill_repo / "skills").rglob("SKILL.md")
        ]
        skill_names = sorted(p.parent.name for p in skill_md_files)

        assert "autoresearch-create" in skill_names, "autoresearch-create not in enumeration"
        assert "autoresearch-finalize" in skill_names, "autoresearch-finalize not in enumeration"
        assert "autoresearch-tree" in skill_names, "autoresearch-tree not in enumeration"
        assert len(skill_names) == 3, f"expected 3 skills, got {skill_names}"

    def test_install_existing_is_noop(
        self, source_skill_dir: Path, temp_skill_repo: Path
    ) -> None:
        """Installing twice should not error and should skip gracefully."""
        _install_skill(source_skill_dir, temp_skill_repo)
        result = _install_skill(source_skill_dir, temp_skill_repo)

        assert result.returncode == 0, f"second install failed: {result.stderr}"
        assert "already exists" in result.stderr or "skipping" in result.stderr.lower()

    def test_install_missing_target_errors(self, source_skill_dir: Path, tmp_path: Path) -> None:
        """Missing target repo exits with code 1."""
        nonexistent = tmp_path / "does-not-exist"
        result = _install_skill(source_skill_dir, nonexistent)
        assert result.returncode == 1, "expected exit 1 for missing target"
