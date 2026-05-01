---
name: filesystem_tree
active: true
title: "Filesystem Tree Schema"
type: schema
fields:
  node_type:
    description: "Sub-type of filesystem node — 'directory' or 'file'"
    type: string
    required: true
    enum:
      - directory
      - file
  absolute_path:
    description: "Absolute path on the host filesystem"
    type: string
    required: true
  relative_path:
    description: "Path relative to the indexed root"
    type: string
    required: true
  size_bytes:
    description: "Byte size of the file (0 for directories)"
    type: integer
    required: false
  is_symlink:
    description: "True if this entry was a symlink and was skipped"
    type: boolean
    required: false
  skipped_reason:
    description: "Why this entry was skipped (symlink, permission denied, etc.)"
    type: string
    required: false
---

This schema is used by the `filesystem_tree` indexer to emit directory and file nodes.
