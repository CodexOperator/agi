---
confidence: 0.99
contrasts: []
evidence_runs:
  - "exp-loader-csafe.py"
id: "verdict:a00-324837df-2546ce-csafe-loader"
next_edges: []
parents:
  - "exp:a00-324837df-2546ce-csafe-loader"
status: "proved"
subgraph: false
supports:
  - "verdict:graph-core-r1"
title: "iter30b: CSafeLoader PROVED - 4x speedup (1884ms → 468ms)"
type: "verdict"
---

**Verdict:** PROVED (confidence 0.99)

**Evidence:**
- `yaml.safe_load` → `yaml.load(Loader=yaml.CSafeLoader)` in frontmatter.py
- Baseline: 1884ms (SafeLoader, Python-based)
- Optimized: 468ms (CSafeLoader, C-based)
- **Speedup: 4.02x, time saved: 1416ms (75.1%)**
- 274 tests pass

**Root Cause:**
- Python's `yaml.safe_load` uses the Python-based `SafeLoader` parser
- YAML parsing is CPU-bound; SafeLoader is pure Python (slow)
- `yaml.CSafeLoader` is a C-based libyaml binding (3-5x faster)
- Most of load_directory time is spent in YAML parsing

**Impact:**
- Cold load: 1884ms → 468ms (4x faster)
- Each experiment iteration now starts 1.4s sooner
- The experiment loop (multiple iterations) benefits most
