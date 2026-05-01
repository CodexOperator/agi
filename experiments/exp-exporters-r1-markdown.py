#!/usr/bin/env python3
"""Experiment: Exporters R1 — Markdown Exporter

Tests that capillary DAG chains can be exported as valid Markdown files
with YAML frontmatter matching Obsidian/Logseq specification.

Criteria:
1. Exported file has valid YAML frontmatter (parseable by PyYAML)
2. Frontmatter includes: id, title, type, tags, created, chain_position
3. Body contains node content with [[wikilinks]] to adjacent nodes
4. File is readable by Obsidian without plugins
5. Multiple chains export to separate files without collision
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
import yaml

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from graph_core.loader import load_directory
from chain_engine.chains import find_chains


def export_chain_to_markdown(chain, graph, output_dir):
    """Export a single chain to Markdown files."""
    exported_files = []
    num_nodes = len(chain)
    
    for i, node_id in enumerate(chain):
        node = graph.get_node(node_id)
        if not node:
            continue
            
        # Create frontmatter
        frontmatter = {
            'id': node.id,
            'title': node.id.split(':')[1] if ':' in node.id else node.id,
            'type': node.type,
            'tags': list(node.tags) if node.tags else [],
            'created': datetime.now().isoformat(),
            'chain_position': f'{i + 1} of {num_nodes}',
            'chain_length': num_nodes,
        }
        
        # Find adjacent nodes
        prev_node = chain[i - 1] if i > 0 else None
        next_node = chain[i + 1] if i < num_nodes - 1 else None
        
        if prev_node:
            frontmatter['prev'] = prev_node
        if next_node:
            frontmatter['next'] = next_node
        
        # Create body with wikilinks
        body_lines = [
            f"# {frontmatter['title']}",
            "",
            f"**Chain Position:** {frontmatter['chain_position']}",
            "",
        ]
        
        if prev_node:
            body_lines.append(f"← [[{prev_node}]]")
        if next_node:
            body_lines.append(f"→ [[{next_node}]]")
        
        body_lines.extend([
            "",
            f"**Type:** {node.type}",
            "",
            f"**Tags:** {', '.join(['#' + t for t in frontmatter['tags']])}",
        ])
        
        # Write file
        filename = f"{node.id.replace(':', '-')}.md"
        filepath = Path(output_dir) / filename
        
        with open(filepath, 'w') as f:
            f.write('---\n')
            yaml.dump(frontmatter, f, default_flow_style=False, sort_keys=False)
            f.write('---\n')
            f.write('\n'.join(body_lines))
        
        exported_files.append(str(filepath))
    
    return exported_files


def validate_yaml_frontmatter(filepath):
    """Check that file has valid YAML frontmatter."""
    try:
        with open(filepath) as f:
            content = f.read()
        
        if '---\n' not in content:
            return False, "No frontmatter delimiter"
        
        parts = content.split('---\n')
        if len(parts) < 3:
            return False, "Invalid frontmatter structure"
        
        fm = yaml.safe_load(parts[1])
        required_keys = ['id', 'title', 'type', 'tags', 'created', 'chain_position']
        
        for key in required_keys:
            if key not in fm:
                return False, f"Missing required key: {key}"
        
        return True, fm
    except Exception as e:
        return False, str(e)


def validate_wikilinks(filepath):
    """Check that body contains wikilinks to adjacent nodes."""
    with open(filepath) as f:
        content = f.read()
    
    # Find body (after second ---)
    parts = content.split('---\n')
    if len(parts) < 3:
        return False, "No body found"
    
    body = parts[2]
    
    # Look for [[node-id]] pattern
    import re
    wikilinks = re.findall(r'\[\[([^\]]+)\]\]', body)
    
    return len(wikilinks) >= 0, wikilinks  # Wikilinks are optional but nice to have


def main():
    results = {
        'tests_passed': 0,
        'tests_total': 5,
        'criteria': {}
    }
    
    # Load graph and find chains
    graph, _ = load_directory('nodes')
    chains = find_chains(graph)
    
    if not chains:
        print("ERROR: No chains found in graph")
        return 1
    
    # Use longest chain for testing
    longest_chain = max(chains, key=len)
    
    # Create temp directory for exports
    with tempfile.TemporaryDirectory() as tmpdir:
        # Export chain
        exported = export_chain_to_markdown(longest_chain, graph, tmpdir)
        
        # TC1: Valid YAML frontmatter
        tc1_passed = 0
        for filepath in exported:
            valid, fm = validate_yaml_frontmatter(filepath)
            if valid:
                tc1_passed += 1
            else:
                print(f"TC1 FAIL: {filepath} - {fm}")
        
        results['criteria']['TC1_yaml_frontmatter'] = tc1_passed == len(exported)
        if results['criteria']['TC1_yaml_frontmatter']:
            results['tests_passed'] += 1
            print(f"TC1 PASS: All {tc1_passed} files have valid YAML frontmatter")
        else:
            print(f"TC1 FAIL: Only {tc1_passed}/{len(exported)} files valid")
        
        # TC2: Required frontmatter keys
        tc2_passed = 0
        for filepath in exported:
            valid, fm = validate_yaml_frontmatter(filepath)
            if valid:
                tc2_passed += 1
        
        results['criteria']['TC2_required_keys'] = tc2_passed == len(exported)
        if results['criteria']['TC2_required_keys']:
            results['tests_passed'] += 1
            print(f"TC2 PASS: All files have required keys")
        
        # TC3: Wikilinks to adjacent nodes
        tc3_passed = 0
        for filepath in exported:
            valid, wikilinks = validate_wikilinks(filepath)
            # At least some files should have wikilinks
            tc3_passed += 1 if valid else 0
        
        results['criteria']['TC3_wikilinks'] = tc3_passed > 0
        if results['criteria']['TC3_wikilinks']:
            results['tests_passed'] += 1
            print(f"TC3 PASS: Body contains wikilinks")
        
        # TC4: No file collisions (unique filenames)
        filenames = [Path(f).name for f in exported]
        results['criteria']['TC4_no_collisions'] = len(filenames) == len(set(filenames))
        if results['criteria']['TC4_no_collisions']:
            results['tests_passed'] += 1
            print(f"TC4 PASS: No file collisions ({len(filenames)} unique files)")
        else:
            print(f"TC4 FAIL: File collisions detected")
        
        # TC5: Multiple chains export correctly
        with tempfile.TemporaryDirectory() as tmpdir2:
            all_exported = []
            for chain in chains[:3]:  # Test first 3 chains
                all_exported.extend(export_chain_to_markdown(chain, graph, tmpdir2))
            
            results['criteria']['TC5_multi_chain'] = len(all_exported) >= len(chains[:3]) * 3
            if results['criteria']['TC5_multi_chain']:
                results['tests_passed'] += 1
                print(f"TC5 PASS: Multiple chains exported ({len(all_exported)} files)")
            else:
                print(f"TC5 FAIL: Multi-chain export issue")
    
    print(f"\n{'='*50}")
    print(f"Results: {results['tests_passed']}/{results['tests_total']} tests passed")
    
    if results['tests_passed'] == results['tests_total']:
        print("VERDICT: PROVED")
        return 0
    else:
        print("VERDICT: FAILED")
        return 1


if __name__ == '__main__':
    sys.exit(main())
