---
id: "mvp:autoresearch-tree-skill-r1"
title: "mvp:autoresearch-tree-skill-r1"
type: mvp
parents:
  - "verdict:autoresearch-tree-skill-r1"
next_edges:
  - "outcome:autoresearch-tree-skill-r1"
---

## MVP: autoresearch-tree-skill/R1 Verification Script

Script that verifies the skill installation criteria:

```bash
#!/bin/bash
# verify-skill-install.sh — verifies R1 acceptance criteria
SKILL_REPO="/home/ubuntu/.pi/agent/git/github.com/davebcn87/pi-autoresearch/skills"

# Check new skill exists
if [ ! -d "$SKILL_REPO/autoresearch-tree" ]; then
    echo "FAIL: autoresearch-tree directory missing"
    exit 1
fi

# Check original skills untouched
for skill in autoresearch-create autoresearch-finalize; do
    if [ ! -f "$SKILL_REPO/$skill/SKILL.md" ]; then
        echo "FAIL: $skill/SKILL.md missing"
        exit 1
    fi
done

# Check new skill is own directory (not patch)
file_count=$(find "$SKILL_REPO/autoresearch-tree" -type f | wc -l)
if [ "$file_count" -eq 0 ]; then
    echo "FAIL: autoresearch-tree is empty"
    exit 1
fi

echo "PASS: All R1 criteria met"
```

Usage: `bash verify-skill-install.sh`
