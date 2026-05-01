#!/usr/bin/env python3
"""exp-test-coverage-r1.py — Analyze pytest test coverage of the agi-tree system.

Hypothesis: 257 tests provide >80% coverage of node types, edge relations, and graph operations.
"""
import sys
import ast
import re
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parent


def parse_test_files(tests_dir: Path):
    """Parse all test files and extract test function names."""
    test_functions = []
    test_files = list(tests_dir.glob("**/test_*.py"))
    
    for f in test_files:
        try:
            content = f.read_text()
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                    test_functions.append({
                        'name': node.name,
                        'file': str(f.relative_to(tests_dir)),
                        'line': node.lineno
                    })
        except Exception as e:
            print(f"  Warning: Could not parse {f}: {e}")
    
    return test_functions, test_files


def categorize_tests(test_functions):
    """Categorize tests by what they test."""
    categories = Counter()
    node_types_tested = set()
    operations_tested = set()
    
    for tf in test_functions:
        name = tf['name'].lower()
        
        # Node types
        if 'node' in name:
            node_types_tested.add('node')
            if 'idea' in name:
                node_types_tested.add('idea')
            elif 'hypothesis' in name or 'hyp' in name:
                node_types_tested.add('hypothesis')
            elif 'experiment' in name or 'exp' in name:
                node_types_tested.add('experiment')
            elif 'verdict' in name:
                node_types_tested.add('verdict')
            elif 'task' in name:
                node_types_tested.add('task')
            elif 'mvp' in name:
                node_types_tested.add('mvp')
            elif 'outcome' in name:
                node_types_tested.add('outcome')
        
        # Operations
        if 'add' in name or 'insert' in name:
            operations_tested.add('add')
        if 'remove' in name or 'delete' in name:
            operations_tested.add('remove')
        if 'get' in name or 'retrieve' in name or 'fetch' in name:
            operations_tested.add('retrieve')
        if 'edge' in name:
            operations_tested.add('edge')
        if 'cycle' in name:
            operations_tested.add('cycle_detection')
        if 'dag' in name:
            operations_tested.add('dag_invariant')
        if 'chain' in name:
            operations_tested.add('chain')
        if 'walk' in name:
            operations_tested.add('walk')
        if 'lazy' in name:
            operations_tested.add('lazy')
        if 'identity' in name:
            operations_tested.add('identity')
        
        # Broad categories
        if 'graph' in name:
            categories['graph_operations'] += 1
        elif 'core' in name:
            categories['core_tests'] += 1
        elif 'embed' in name:
            categories['embedding_tests'] += 1
        elif 'render' in name:
            categories['render_tests'] += 1
        elif 'schema' in name:
            categories['schema_tests'] += 1
        elif 'chain' in name:
            categories['chain_tests'] += 1
        elif 'env' in name or 'index' in name:
            categories['environment_tests'] += 1
        else:
            categories['other_tests'] += 1
    
    return categories, node_types_tested, operations_tested


def main() -> int:
    print("=== Test Coverage Analysis R1 ===\n")
    
    # Count total tests via pytest
    import subprocess
    result = subprocess.run(
        ['python3', '-m', 'pytest', str(ROOT / 'tests'), '--collect-only', '-q'],
        capture_output=True, text=True, timeout=30
    )
    collected = result.stdout + result.stderr
    match = re.search(r'(\d+) test', collected)
    total_tests = int(match.group(1)) if match else len(parse_test_files(ROOT / 'tests')[0])
    print(f"Total tests collected: {total_tests}")
    
    # Parse test files
    print("\nParsing test files...")
    tests_dir = ROOT / 'tests'
    test_functions, test_files = parse_test_files(tests_dir)
    print(f"Test files: {len(test_files)}")
    print(f"Test functions found: {len(test_functions)}")
    
    # Categorize
    categories, node_types_tested, operations_tested = categorize_tests(test_functions)
    
    print(f"\n=== CATEGORIES ===")
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count} tests")
    
    print(f"\n=== NODE TYPES TESTED ===")
    all_node_types = {'node', 'idea', 'hypothesis', 'experiment', 'verdict', 'task', 'mvp', 'outcome', 'bigger_outcome', 'app_purpose'}
    for nt in sorted(all_node_types):
        status = "✓" if nt in node_types_tested else "✗"
        print(f"  {status} {nt}")
    
    node_coverage = len(node_types_tested) / len(all_node_types) * 100
    
    print(f"\n=== OPERATIONS TESTED ===")
    all_ops = {'add', 'remove', 'retrieve', 'edge', 'cycle_detection', 'dag_invariant', 'chain', 'walk', 'lazy', 'identity'}
    for op in sorted(all_ops):
        status = "✓" if op in operations_tested else "✗"
        print(f"  {status} {op}")
    
    ops_coverage = len(operations_tested) / len(all_ops) * 100
    
    # Check hypothesis coverage
    print(f"\n=== HYPOTHESIS COVERAGE ===")
    hyp_dir = ROOT / 'nodes' / 'hypothesis'
    hyp_files = list(hyp_dir.glob("*.md"))
    verdict_dir = ROOT / 'nodes' / 'verdict'
    verdict_files = list(verdict_dir.glob("*.md"))
    
    print(f"Hypotheses: {len(hyp_files)}")
    print(f"Verdicts: {len(verdict_files)}")
    
    # Compute hypothesis coverage: use graph loader to check for verdict edges
    sys.path.insert(0, str(ROOT / 'src'))
    from graph_core.loader import load_directory
    g, _ = load_directory(ROOT / 'nodes')
    
    hyp_with_verdict = 0
    for f in hyp_files:
        content = f.read_text()
        match = re.search(r'^id:\s*"?([^"]+)"?', content, re.MULTILINE)
        if not match:
            continue
        hyp_id = match.group(1)
        # Check if hypothesis node has edges to verdict nodes
        hyp_node = g.get_node(hyp_id)
        if hyp_node:
            # Check outgoing edges to verdicts
            has_verdict = False
            for edge in g.edges:
                if edge.source_id == hyp_id and 'verdict' in edge.target_id:
                    has_verdict = True
                    break
            if has_verdict:
                hyp_with_verdict += 1
    
    hyp_coverage = hyp_with_verdict / len(hyp_files) * 100 if hyp_files else 0
    
    print(f"Hypotheses with verdict edges: {hyp_with_verdict}/{len(hyp_files)} ({hyp_coverage:.0f}%)")
    
    # Compute overall coverage score
    overall_coverage = (node_coverage + ops_coverage + hyp_coverage) / 3
    
    print(f"\n=== COVERAGE SUMMARY ===")
    print(f"METRIC overall_coverage={overall_coverage:.1f}%")
    print(f"METRIC node_coverage={node_coverage:.1f}%")
    print(f"METRIC ops_coverage={ops_coverage:.1f}%")
    print(f"METRIC hyp_coverage={hyp_coverage:.1f}%")
    print(f"METRIC test_count={len(test_functions)}")
    
    # Interpretation
    threshold = 80.0
    if overall_coverage >= threshold:
        verdict = "proved"
        interpretation = f"Coverage ({overall_coverage:.0f}%) meets threshold ({threshold}%)"
    elif overall_coverage >= 60:
        verdict = "inconclusive_lean_proved:60"
        interpretation = f"Coverage ({overall_coverage:.0f}%) is moderate, below threshold ({threshold}%)"
    else:
        verdict = "disproved"
        interpretation = f"Coverage ({overall_coverage:.0f}%) below threshold ({threshold}%)"
    
    print(f"\nVerdict: {verdict.upper()}")
    print(f"Interpretation: {interpretation}")
    
    # Write verdict node
    verdict_id = "verdict:test-coverage-r1"
    verdict_path = ROOT / "nodes" / "verdict" / f"{verdict_id.replace(':', '-')}.md"
    verdict_content = f"""---
id: "{verdict_id}"
title: "R1: Test coverage analysis of node types, edge relations, and graph operations"
type: verdict
parent_hypothesis: hyp:test-coverage-r1
domain: test-coverage
status: {verdict.split(':')[0]}
confidence: {overall_coverage / 100:.2f}
evidence_runs:
  - exp:test-coverage-r1
tags:
  - tests
  - coverage
  - R1
---

**Verdict:** {verdict.upper()}

**Coverage Metrics:**
- Overall: {overall_coverage:.1f}%
- Node types: {node_coverage:.1f}% ({len(node_types_tested)}/{len(all_node_types)})
- Operations: {ops_coverage:.1f}% ({len(operations_tested)}/{len(all_ops)})
- Hypotheses with verdicts: {hyp_coverage:.1f}% ({hyp_with_verdict}/{len(hyp_files)})

**Evidence:**
- {len(test_functions)} test functions across {len(test_files)} files
- Threshold: {threshold}%

**Interpretation:**
{interpretation}

**Categories by test count:**
{chr(10).join(f"- {cat}: {count}" for cat, count in sorted(categories.items(), key=lambda x: -x[1]))}
"""
    
    with open(verdict_path, 'w') as f:
        f.write(verdict_content)
    print(f"\nVerdict written to {verdict_path}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
