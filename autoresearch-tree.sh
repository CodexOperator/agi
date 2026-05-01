#!/bin/bash
# autoresearch-tree.sh — manual-controls driver for the capillary DAG loop.
#
# Usage:
#   ./autoresearch-tree.sh [--max-iters N] [--delay-mins M] [--smoke]
#
# Each iteration:
#   1. Refresh INJECTION.md by re-running snapshot + render
#   2. Print injection summary
#   3. Emit METRIC lines for primary + secondary
#   4. Sleep `delay-mins` minutes between iterations
#
# `--smoke` runs a single dry pass without sleeping or invoking agents.
# Real agent dispatch (5 Claude builders + Ollama qwen3:4b) lands under T-081.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
CONFIG="$ROOT/autoresearch-tree.config.json"
INJECTION="$ROOT/context/INJECTION.md"
LOG="$ROOT/loop.log"

MAX_ITERS=1
DELAY_MINS=0
SMOKE=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --max-iters) MAX_ITERS="$2"; shift 2 ;;
    --delay-mins) DELAY_MINS="$2"; shift 2 ;;
    --smoke) SMOKE=true; shift ;;
    -h|--help)
      cat <<EOF
autoresearch-tree.sh — manual capillary DAG loop driver

OPTIONS:
  --max-iters N      Run N iterations (default 1)
  --delay-mins M     Sleep M minutes between iters (default 0)
  --smoke            Single dry run, no sleep, no agent dispatch
  -h, --help         Show this help

INJECTION_FILE: $INJECTION
CONFIG:         $CONFIG
EOF
      exit 0
      ;;
    *) echo "unknown arg: $1" >&2; exit 2 ;;
  esac
done

mkdir -p "$ROOT/context" "$ROOT/nodes"

iter_run() {
  local n="$1"
  local ts
  ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  echo "=== iter $n @ $ts ===" | tee -a "$LOG"

  # 1. Snapshot build site → nodes/
  python3 "$ROOT/bin/snapshot-build-site.py" 2>&1 | tee -a "$LOG"

  # 2. Render context → INJECTION.md
  python3 "$ROOT/bin/render-context.py" "$ROOT/nodes" 2>&1 | tee -a "$LOG"

  # 3. Emit METRIC lines (primary + secondary)
  python3 - <<'PYEOF' 2>&1 | tee -a "$LOG"
import re, sys
from pathlib import Path
sys.path.insert(0, str(Path("$ROOT" if False else ".").resolve() / "src"))

# Re-resolve paths from cwd
import os
root = Path(os.environ.get("AUTORESEARCH_TREE_ROOT", "."))
sys.path.insert(0, str(root / "src"))
from graph_core.loader import load_directory
from graph_core.edge import Edge
from collections import defaultdict

nodes_dir = root / "nodes"
g, loaded = load_directory(nodes_dir)
# Wire children from parents so chain-walking reflects the DAG
for ln in loaded:
    for parent_id in ln.node.parents:
        if g.has_node(parent_id):
            try:
                g.add_edge(Edge(source_id=parent_id, target_id=ln.node.id, relation="spawns"))
            except Exception:
                pass
            parent_node = g.get_node(parent_id)
            if parent_node is not None:
                parent_node.children.add(ln.node.id)

# Longest chain length (BFS-style depth)
def longest(g):
    cache = {}
    def d(nid):
        if nid in cache: return cache[nid]
        n = g.get_node(nid)
        if n is None or not n.children:
            cache[nid] = 0; return 0
        best = 0
        for c in n.children:
            if c == nid: continue
            best = max(best, d(c) + 1)
        cache[nid] = best; return best
    if not g.node_ids: return 0
    return max(d(nid) for nid in g.node_ids)

by_type = defaultdict(int)
for n in g.nodes: by_type[n.type] += 1

mvp_count = by_type.get("mvp", 0)
outcome_count = by_type.get("outcome", 0)
bigger_count = by_type.get("bigger_outcome", 0)
outcome_coverage = (mvp_count / max(by_type.get("hypothesis", 1), 1))

# branching factor: avg children per non-leaf
non_leaf = [n for n in g.nodes if n.children]
branching = sum(len(n.children) for n in non_leaf) / max(len(non_leaf), 1)

avg_depth = sum(len(n.parents) for n in g.nodes) / max(len(g), 1)

print(f"METRIC longest_chain_length={longest(g)}")
print(f"METRIC avg_chain_depth={avg_depth:.2f}")
print(f"METRIC mvp_count={mvp_count}")
print(f"METRIC outcome_coverage={outcome_coverage:.3f}")
print(f"METRIC chain_branching_factor={branching:.2f}")
print(f"METRIC node_count={len(g)}")
print(f"METRIC edge_count={g.edge_count}")
PYEOF

  if [[ "$SMOKE" == "true" ]]; then
    echo "[smoke] skipping agent dispatch" | tee -a "$LOG"
    return
  fi

  # 4. (Future T-081) dispatch agents here.
  echo "[note] agent dispatch is a stub — full impl lands under T-081" | tee -a "$LOG"
}

export AUTORESEARCH_TREE_ROOT="$ROOT"

for i in $(seq 1 "$MAX_ITERS"); do
  iter_run "$i"
  if [[ "$i" -lt "$MAX_ITERS" && "$DELAY_MINS" -gt 0 ]]; then
    echo "sleeping ${DELAY_MINS}m before next iter..." | tee -a "$LOG"
    sleep "$((DELAY_MINS * 60))"
  fi
done

echo "INJECTION_FILE=$INJECTION"
exit 0
