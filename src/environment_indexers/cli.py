"""CLI for environment indexers.

Implements:
- `agi-tree index --list` - List all registered indexers
- `agi-tree index <name> <path>` - Run a specific indexer

Acceptance Criteria (R1):
- [x] The command accepts a target path and an indexer name and runs only that indexer
- [x] Listing available indexers without invoking one produces a summary with each indexer's name and one-line description
- [x] An unknown indexer name returns a structured error and does not run anything
- [x] The command exits with a non-zero status when the indexer reports any failure that prevented node emission
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .errors import IndexerExecutionError, UnknownIndexerError
from .registry import get_registry


def list_indexers(args: argparse.Namespace) -> int:
    """List all registered indexers.

    Args:
        args: Parsed arguments with optional --json flag.

    Returns:
        Exit code (0 for success).
    """
    registry = get_registry()
    indexers = registry.list_indexers()

    if args.json:
        import json

        output = [
            {
                "name": idx.name,
                "description": idx.description,
                "tags": idx.tags,
            }
            for idx in indexers
        ]
        print(json.dumps(output, indent=2))
    else:
        if not indexers:
            print("No indexers registered.")
        else:
            print("Available indexers:")
            for idx in indexers:
                tags_str = f" [{', '.join(idx.tags)}]" if idx.tags else ""
                print(f"  {idx.name}{tags_str} — {idx.description}")

    return 0


def run_indexer(args: argparse.Namespace) -> int:
    """Run a specific indexer on a target path.

    Args:
        args: Parsed arguments with name and path.

    Returns:
        Exit code (0 for success, non-zero for failure).
    """
    registry = get_registry()
    target_path = Path(args.path).resolve()

    try:
        idx = registry.get(args.name)
    except UnknownIndexerError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        print("Run 'agi-tree index --list' to see available indexers.", file=sys.stderr)
        return 1

    try:
        idx.func(str(target_path))
        return 0
    except IndexerExecutionError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"ERROR: {args.name} failed unexpectedly: {e}", file=sys.stderr)
        return 1


def main(argv: list[str] | None = None) -> int:
    """Main entry point for the index command.

    Args:
        argv: Command-line arguments (uses sys.argv if None).

    Returns:
        Exit code.
    """
    parser = argparse.ArgumentParser(
        prog="agi-tree index",
        description="Index external sources into the graph.",
    )

    # --list is a mutually exclusive way to invoke
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all registered indexers and exit",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output list as JSON (use with --list)",
    )

    # Positional: indexer name and path (for running)
    parser.add_argument(
        "name",
        nargs="?",
        help="Indexer name",
    )
    parser.add_argument(
        "path",
        nargs="?",
        help="Target path to index",
    )

    args = parser.parse_args(argv)

    if args.list:
        # Override json default when --list is given
        if not hasattr(args, "json"):
            args.json = False
        return list_indexers(args)

    if args.name is None or args.path is None:
        parser.error("Either --list or both <name> and <path> are required")
        return 1  # unreachable but helps type checker

    return run_indexer(args)


if __name__ == "__main__":
    sys.exit(main())
