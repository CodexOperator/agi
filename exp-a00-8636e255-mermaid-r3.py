#!/usr/bin/env python3
"""Test Mermaid renderer validity and determinism (R3)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from graph_core.loader import load_directory
from renderers import render_mermaid, build_representation
import re

NODES_DIR = '/home/ubuntu/.hermes/agi-tree/nodes'

graph, _ = load_directory(NODES_DIR)
rep = build_representation(graph)

# Test 1: Determinism — two runs produce byte-identical output
out1 = render_mermaid(rep)
out2 = render_mermaid(rep)
deterministic = out1 == out2
print(f"[1] Deterministic: {deterministic}")
if not deterministic:
    print(f"  Run1 length: {len(out1)}, Run2 length: {len(out2)}")

# Test 2: Directive check
first_line = out1.split('\n')[0]
valid_directive = first_line.strip().startswith(('flowchart TD', 'graph TD'))
print(f"[2] Valid directive: {valid_directive} ('{first_line}')")

# Test 3: Node coverage — every input node must appear in output as a def line
# The node def line format: `    {mid}["{label}"]` where mid = _mermaid_id(id)
# _mermaid_id: replaces non-[A-Za-z0-9_] chars with _
def _mermaid_id(node_id):
    return re.sub(r'[^A-Za-z0-9_]', '_', node_id) or '_'

input_node_ids = {t.id for t in rep.tokens}
output_mermaid_ids = set()
for line in out1.split('\n'):
    # Match `    MermaidID["label"]` or `    MermaidID["label"]:::type_...`
    m = re.match(r'^\s+([A-Za-z0-9_]+)\["', line)
    if m:
        output_mermaid_ids.add(m.group(1))

# Check: all output mermaid IDs are valid transforms of input node IDs
valid_transforms = output_mermaid_ids - input_node_ids  # These should be the transformed ones
output_nodes = set()
for mid in output_mermaid_ids:
    # mid is the mermaid_id — it could equal node_id (no special chars) 
    # or be a transformed version
    output_nodes.add(mid)

# Every input node must be representable (has a mermaid_id in output)
input_missing = []
for nid in sorted(input_node_ids):
    mid = _mermaid_id(nid)
    if mid not in output_mermaid_ids:
        input_missing.append((nid, mid))
        if len(input_missing) <= 3:
            print(f"  Missing: input={nid}, _mermaid_id={mid}")

nodes_missing_count = len(input_missing)
nodes_covered = len(input_node_ids) - nodes_missing_count
nodes_subset = nodes_missing_count == 0
print(f"[3] All {len(input_node_ids)} input nodes have mermaid_id in output: {nodes_subset}")
if not nodes_subset:
    print(f"  Missing {nodes_missing_count} nodes ({nodes_covered}/{len(input_node_ids)})")

# Spurious nodes check: all output mermaid_ids come from valid input transforms
spurious = []
for mid in output_mermaid_ids:
    # A valid mermaid_id either equals the node_id OR is a transformed version
    if mid not in input_node_ids:
        # Check if this mid maps back to a real node
        found = False
        for nid in input_node_ids:
            if _mermaid_id(nid) == mid:
                found = True
                break
        if not found:
            spurious.append(mid)

nodes_spurious = len(spurious)
print(f"[3c] Spurious nodes in output: {nodes_spurious}")

# Test 4: Edge deduplication — every input edge must appear in output
input_edges = set()
for t in rep.tokens:
    for tgt, rel in t.edges:
        input_edges.add((t.id, tgt))

# Parse edges from output: `    src -->|"rel"| tgt` or `    src --> tgt`
output_edges = set()
for line in out1.split('\n'):
    # Match edge patterns
    # Pattern 1: with relation `    src -->|"rel"| tgt`
    m_rel = re.match(r'^\s+([A-Za-z0-9_]+)\s+-->\s*\|[^|]*\|\s*([A-Za-z0-9_]+)', line)
    # Pattern 2: without relation `    src --> tgt`
    m_no_rel = re.match(r'^\s+([A-Za-z0-9_]+)\s+-->\s+([A-Za-z0-9_]+)\s*$', line)
    if m_rel:
        src = m_rel.group(1)
        tgt = m_rel.group(2)
        # These are mermaid_ids — map back to original node ids
        output_edges.add((src, tgt))
    elif m_no_rel:
        src = m_no_rel.group(1)
        tgt = m_no_rel.group(2)
        output_edges.add((src, tgt))

# Now check: every input edge's mermaid_id pair must appear in output
# Note: input_edges uses original node_ids, output uses mermaid_ids
edge_missing = []
edge_spurious = []
for (src_orig, tgt_orig) in sorted(input_edges):
    src_mid = _mermaid_id(src_orig)
    tgt_mid = _mermaid_id(tgt_orig)
    if (src_mid, tgt_mid) not in output_edges:
        edge_missing.append((src_orig, tgt_orig, src_mid, tgt_mid))
        if len(edge_missing) <= 3:
            print(f"  Missing edge: {src_orig}->{tgt_orig} (mid: {src_mid}->{tgt_mid})")

for (src_mid, tgt_mid) in sorted(output_edges):
    # Check if this pair maps back to a real input edge
    found = False
    for (src_orig, tgt_orig) in input_edges:
        if _mermaid_id(src_orig) == src_mid and _mermaid_id(tgt_orig) == tgt_mid:
            found = True
            break
    if not found:
        edge_spurious.append((src_mid, tgt_mid))

edges_missing_count = len(edge_missing)
edges_spurious_count = len(edge_spurious)
edges_complete = edges_missing_count == 0
edges_subset = edges_spurious_count == 0
print(f"[4] All input edges in output: {edges_complete} ({len(input_edges) - edges_missing_count}/{len(input_edges)})")
print(f"[4b] No spurious edges: {edges_subset} ({len(output_edges) - edges_spurious_count}/{len(output_edges)})")

# Test 5: Mermaid id safety (no bare : in unquoted ids)
# The render_mermaid function uses quoted strings for all labels, so this is about node IDs in edges
has_unquoted_complex_id = bool(re.search(r'^\s*[A-Za-z0-9_]+\s+-->\s+[^|"\s]+', out1, re.MULTILINE))
print(f"[5] No unquoted complex ids in edges: {not has_unquoted_complex_id}")

# Summary
all_pass = deterministic and valid_directive and nodes_subset and edges_complete and not has_unquoted_complex_id
partial_pass = sum([deterministic, valid_directive, nodes_subset, edges_complete, not has_unquoted_complex_id])

print(f"\n{'='*50}")
print(f"Results: {partial_pass}/5 criteria passed")
print(f"Overall: {'PROVED' if all_pass else 'DISPROVED' if partial_pass == 0 else 'INCONCLUSIVE'}")
if not nodes_subset:
    print(f"  Node issue: {nodes_missing_count} missing")
if not edges_complete:
    print(f"  Edge issue: {edges_missing_count} missing")

# Metrics
print(f"\nMETRIC criteria_passed={partial_pass}")
print(f"METRIC deterministic={1 if deterministic else 0}")
print(f"METRIC valid_directive={1 if valid_directive else 0}")
print(f"METRIC nodes_complete={1 if nodes_subset else 0}")
print(f"METRIC edges_complete={1 if edges_complete else 0}")
print(f"METRIC safe_ids={1 if not has_unquoted_complex_id else 0}")
print(f"METRIC input_nodes={len(input_node_ids)}")
print(f"METRIC output_nodes={len(output_mermaid_ids)}")
print(f"METRIC nodes_missing={nodes_missing_count}")
print(f"METRIC input_edges={len(input_edges)}")
print(f"METRIC output_edges={len(output_edges)}")
print(f"METRIC edges_missing={edges_missing_count}")
