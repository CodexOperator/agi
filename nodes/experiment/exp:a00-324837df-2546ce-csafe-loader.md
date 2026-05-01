---
id: "exp:a00-324837df-2546ce-csafe-loader"
type: experiment
title: "iter30b: CSafeLoader reduces load_directory from 1884ms to 468ms (4x speedup)"
parents:
  - "hypothesis:a00-324837df-2546ce"
next_edges:
  - "verdict:a00-324837df-2546ce-csafe-loader"
---

**Experiment:** Replace `yaml.safe_load` with `yaml.CSafeLoader` in frontmatter.py

**Results:**
- Baseline (SafeLoader): 1884ms
- Optimized (CSafeLoader): 468ms
- **Speedup: 4.02x, improvement: 75.1%**
- 274 tests pass

**Files changed:** `src/graph_core/persistence/frontmatter.py`
