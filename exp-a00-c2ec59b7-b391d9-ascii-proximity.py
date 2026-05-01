#!/usr/bin/env python3
"""Test ASCII render proximity vs graph descendant overlap isomorphism."""
import sys, os
sys.path.insert(0, '/home/ubuntu/.hermes/agi-tree/src')
os.chdir('/home/ubuntu/.hermes/agi-tree')

from graph_core.loader import GraphLoader
from renderers.ascii import render_ascii
from renderers.representation import build_representation

NODES_DIR = '/home/ubuntu/.hermes/agi-tree/nodes'

loader = GraphLoader(NODES_DIR)
graph = loader.load()

# Build descendant sets (BFS from each node)
descendants = {}
for node_id in graph.nodes:
    desc = set()
    queue = list(graph.children.get(node_id, []))
    seen = set(queue)
    while queue:
        cur = queue.pop(0)
        desc.add(cur)
        for child in graph.children.get(cur, []):
            if child not in seen:
                seen.add(child)
                queue.append(child)
    descendants[node_id] = desc

# Filter to nodes with at least 1 descendant
nodes_with_desc = [n for n in graph.nodes if descendants.get(n)]
print(f"Total nodes: {len(graph.nodes)}, nodes with descendants: {len(nodes_with_desc)}")

# Sample 30 node pairs (A, B) where A != B
import random
random.seed(42)
pairs = []
attempts = 0
while len(pairs) < 30 and attempts < 1000:
    a = random.choice(nodes_with_desc)
    b = random.choice(nodes_with_desc)
    if a != b and (a, b) not in pairs and (b, a) not in pairs:
        pairs.append((a, b))
    attempts += 1

# Compute Jaccard overlap for each pair
overlaps = []
for a, b in pairs:
    da = descendants.get(a, set())
    db = descendants.get(b, set())
    if da or db:
        union = da | db
        inter = da & db
        jaccard = len(inter) / len(union) if union else 0.0
        overlaps.append((a, b, jaccard))
    else:
        overlaps.append((a, b, 0.0))

print(f"Computed Jaccard overlaps for {len(overlaps)} pairs")

# Render ASCII
rep = build_representation(graph)
ascii_output = render_ascii(rep)
lines = ascii_output.split('\n')
print(f"ASCII render: {len(lines)} lines")

# Extract line numbers for each node ID
# The ASCII render format: "{indent}{label} :: {type}[ edge_summary]"
# We need to map node IDs to their render line numbers
# Strategy: look for the short ID or label in each line

node_line = {}  # node_id -> line number (0-indexed)

# Get all nodes as sorted list for predictable ordering
sorted_nodes = sorted(graph.nodes)

for row, line in enumerate(lines):
    # Check if this line contains a node reference
    for node_id in sorted_nodes:
        # Match short form of ID
        short = node_id.split(':')[-1] if ':' in node_id else node_id[:16]
        # Also try full ID or last 20 chars
        if short in line:
            if node_id not in node_line:
                node_line[node_id] = row

print(f"Extracted positions for {len(node_line)} nodes")

# Compute line distances for our pairs
distances = []
for a, b, jaccard in overlaps:
    if a in node_line and b in node_line:
        line_diff = abs(node_line[a] - node_line[b])
        distances.append((a, b, jaccard, line_diff))
    else:
        distances.append((a, b, jaccard, None))

# Spearman correlation between Jaccard overlap and proximity (1 / (1 + line_diff))
valid = [(a, b, j, d) for a, b, j, d in distances if d is not None]
print(f"Pairs with position data: {len(valid)}/{len(distances)}")

if len(valid) >= 10:
    # Spearman: rank by jaccard, rank by proximity (inverse of line_diff)
    sorted_by_j = sorted(valid, key=lambda x: x[2])
    sorted_by_d = sorted(valid, key=lambda x: x[3])  # lower dist = higher rank
    
    n = len(valid)
    d_sq = 0
    for i, (a, b, j, d) in enumerate(sorted_by_j):
        # Find rank in distance-sorted (1 = closest = highest rank)
        rank_d = next((j for j, (aa, bb, jj, dd) in enumerate(sorted_by_d)), 0)
        rank_j = i
        d_sq += (rank_j - rank_d) ** 2
    
    spearman = 1.0 - (6.0 * d_sq) / (n * (n**2 - 1)) if n > 1 else 0.0
    print(f"\nSpearman correlation (overlap vs proximity): {spearman:.3f}")
    
    # Top-5 by overlap
    top5 = sorted(overlaps, key=lambda x: x[2], reverse=True)[:5]
    print(f"\nTop-5 overlapping pairs (render line distance):")
    total_line_diff = 0
    for a, b, j in top5:
        if a in node_line and b in node_line:
            ld = abs(node_line[a] - node_line[b])
            total_line_diff += ld
            print(f"  {a[-30:]} <-> {b[-30:]}: Jaccard={j:.3f}, line_diff={ld}")
        else:
            print(f"  {a[-30:]} <-> {b[-30:]}: Jaccard={j:.3f}, pos=UNKNOWN")
    avg_line_diff = total_line_diff / 5 if top5 else None
    print(f"Top-5 avg line diff: {avg_line_diff:.1f}")
    
    # Threshold check
    if spearman >= 0.5 and avg_line_diff and avg_line_diff < 5:
        print(f"\nVERDICT: PROVED (spearman={spearman:.3f} >= 0.5, avg_line_diff={avg_line_diff:.1f} < 5)")
    elif spearman <= 0.2:
        print(f"\nVERDICT: DISPROVED (spearman={spearman:.3f} <= 0.2)")
    else:
        print(f"\nVERDICT: INCONCLUSIVE (spearman={spearman:.3f} between 0.2 and 0.5)")
    
    print(f"\nMETRIC spearman={spearman:.3f}")
    print(f"METRIC top5_avg_line_diff={avg_line_diff:.1f}" if avg_line_diff else "METRIC top5_avg_line_diff=N/A")
else:
    print("Insufficient pairs with position data")
    print("METRIC spearman=N/A")
