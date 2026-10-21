#!/usr/bin/env python3
"""Regenerate artifacts/sha256sums.txt and artifacts/manifest.json.

Run only when an authorized revision changes tracked content. The frozen
experiment artifacts themselves must never be edited in place.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import repo_common  # noqa: E402


def main() -> int:
    metadata = repo_common.write_manifest()
    print(f"wrote {repo_common.MANIFEST_TXT.relative_to(repo_common.ROOT)}")
    print(f"files: {metadata['file_count']}")
    print(f"bytes: {metadata['total_bytes']}")
    print(f"wrote {repo_common.MANIFEST_JSON.relative_to(repo_common.ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
