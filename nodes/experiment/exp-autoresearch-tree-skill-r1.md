---
id: "exp:autoresearch-tree-skill-r1"
title: "exp:autoresearch-tree-skill-r1"
type: experiment
parents:
  - "hyp:autoresearch-tree-skill-r1"
next_edges:
  - "verdict:autoresearch-tree-skill-r1"
---

## Experiment: autoresearch-tree-skill/R1

Tests that the skill is installed in a forked repository alongside existing skills.

### Verification Steps

1. Check skill directory exists: `/home/ubuntu/.pi/agent/git/github.com/davebcn87/pi-autoresearch/skills/autoresearch-tree/`
2. Check original skills untouched: `ls /home/ubuntu/.pi/agent/git/github.com/davebcn87/pi-autoresearch/skills/autoresearch-create/` and `autoresearch-finalize/`
3. Check new skill is own directory (not patch to existing files)
4. Verify both new and original skills listed in enumeration

### Results

- ✅ `/home/ubuntu/.pi/agent/git/github.com/davebcn87/pi-autoresearch/skills/autoresearch-tree/` exists with SKILL.md
- ✅ `autoresearch-create/` and `autoresearch-finalize/` both present and unchanged (each has only SKILL.md)
- ✅ New skill is one directory of files, not a patch
- ✅ Both new and original skills listed via standard enumeration

**Conclusion: PROVED**
