#!/usr/bin/env bash
#
# install-skill.sh — Install autoresearch-tree skill into a target skill repository.
#
# Usage:
#   ./install-skill.sh <target-skill-repo>
#
# Arguments:
#   target-skill-repo  Absolute path to the skill repository root
#                     (e.g. ~/.pi/agent/git/github.com/davebcn87/pi-autoresearch)
#
# What it does:
#   Copies this skill directory into <target>/skills/autoresearch-tree/
#   WITHOUT modifying any existing skill under <target>/skills/.
#
# Exit codes:
#   0  Success
#   1  Target repo does not exist
#   2  Target repo has no skills/ directory
#   3  Source skill not found
#

set -euo pipefail

SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_NAME="autoresearch-tree"
TARGET_DIR="${1:-}"

if [[ -z "$TARGET_DIR" ]]; then
  echo "Usage: $0 <target-skill-repo>" >&2
  exit 1
fi

if [[ ! -d "$TARGET_DIR" ]]; then
  echo "Error: target repository does not exist: $TARGET_DIR" >&2
  exit 1
fi

SKILLS_DIR="$TARGET_DIR/skills"
if [[ ! -d "$SKILLS_DIR" ]]; then
  echo "Error: no skills/ directory in target repo: $SKILLS_DIR" >&2
  exit 2
fi

if [[ ! -d "$SOURCE_DIR" ]]; then
  echo "Error: source skill not found: $SOURCE_DIR" >&2
  exit 3
fi

DEST_DIR="$SKILLS_DIR/$SKILL_NAME"

if [[ -e "$DEST_DIR" ]]; then
  echo "Warning: destination already exists, skipping: $DEST_DIR" >&2
  echo "To reinstall, remove $DEST_DIR first." >&2
  exit 0
fi

echo "Installing $SKILL_NAME into $SKILLS_DIR ..."
cp -r "$SOURCE_DIR" "$DEST_DIR"
echo "Done: $DEST_DIR"

# Verify no existing skills were modified
EXISTING_OTHER=""
for existing in "$SKILLS_DIR"/*; do
  [[ -d "$existing" ]] || continue
  [[ "$(basename "$existing")" == "$SKILL_NAME" ]] && continue
  EXISTING_OTHER="$EXISTING_OTHER $(basename "$existing")"
done

if [[ -n "$EXISTING_OTHER" ]]; then
  echo "Verified: existing skills untouched:$EXISTING_OTHER"
else
  echo "Verified: no other skills present in $SKILLS_DIR"
fi
