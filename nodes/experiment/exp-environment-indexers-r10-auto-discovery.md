# experiment:environment-indexers-r10

**type**: experiment
**parent**: hyp:environment-indexers-r10
**spawned_by**: agent:a02-b000ca8a (iter 5)

## hypothesis
hyp:environment-indexers-r10 (Indexer Auto-Discovery)

## testable_claim
Given a target path, the system auto-detects which indexer(s) apply without the caller needing to know the indexer names.

## experiment_design

### Test Cases

**TC1: Python project detection**
- Input: path containing `pyproject.toml`
- Expected: indexer auto-detected as `python-dependency`

**TC2: API spec detection (OpenAPI)**
- Input: path containing `openapi.yaml`
- Expected: indexer auto-detected as `api-dependency`

**TC3: Code symbol detection**
- Input: path with `.py` files but no manifest files
- Expected: indexer auto-detected as `code-symbol`

**TC4: Unknown type fallback**
- Input: path with only `.txt` files
- Expected: suggestion to use `filesystem-tree` or specify manually

**TC5: Explicit override bypasses auto-discovery**
- Input: path with `pyproject.toml` + explicit `--indexer filesystem-tree`
- Expected: `filesystem-tree` runs, python-dependency is NOT invoked

### Implementation
Prototype `discover_indexer(target_path)` function implementing the heuristic mapping above.
