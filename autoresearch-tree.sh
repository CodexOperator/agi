#!/bin/bash
# Thin wrapper — delegates to plugin driver. Lets you run from project root
# without typing the long plugin path. The plugin walks back up to find this
# project root via autoresearch-tree.config.json.
#
# Override plugin path with AUTORESEARCH_TREE_PLUGIN env var if needed.

set -euo pipefail

DEFAULT_PLUGIN="/home/ubuntu/.pi/agent/git/github.com/davebcn87/pi-autoresearch/extensions/autoresearch-tree"
PLUGIN="${AUTORESEARCH_TREE_PLUGIN:-$DEFAULT_PLUGIN}"

if [[ ! -x "$PLUGIN/driver.sh" ]]; then
  echo "ERR: plugin driver not found at $PLUGIN/driver.sh" >&2
  echo "Install pi-autoresearch + autoresearch-tree extension, or set AUTORESEARCH_TREE_PLUGIN." >&2
  exit 1
fi

exec "$PLUGIN/driver.sh" "$@"
