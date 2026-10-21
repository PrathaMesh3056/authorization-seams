#!/usr/bin/env python3
"""Verify every tracked repository file against artifacts/sha256sums.txt.

Exit codes:
  0  all hashes match and no unexpected files are present
  1  mismatch, missing file, or unexpected file
  2  manifest missing or malformed
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import repo_common  # noqa: E402


def main() -> int:
    expected = repo_common.load_manifest()
    if not expected:
        print("manifest missing or empty: artifacts/sha256sums.txt", file=sys.stderr)
        return 2

    actual: dict[str, str] = {}
    for path in repo_common.tracked_files():
        actual[repo_common.rel_posix(path)] = repo_common.sha256_file(path)

    missing = sorted(set(expected) - set(actual))
    unexpected = sorted(set(actual) - set(expected))
    mismatched = sorted(
        rel for rel in set(expected) & set(actual) if expected[rel] != actual[rel]
    )

    if mismatched:
        print(f"mismatched files ({len(mismatched)}):", file=sys.stderr)
        for rel in mismatched:
            print(f"  {rel}", file=sys.stderr)
            print(f"    expected {expected[rel]}", file=sys.stderr)
            print(f"    actual   {actual[rel]}", file=sys.stderr)
    if missing:
        print(f"missing files ({len(missing)}):", file=sys.stderr)
        for rel in missing:
            print(f"  {rel}", file=sys.stderr)
    if unexpected:
        print(f"unexpected files ({len(unexpected)}):", file=sys.stderr)
        for rel in unexpected:
            print(f"  {rel}", file=sys.stderr)

    if mismatched or missing or unexpected:
        return 1

    print(f"verified {len(expected)} files; all hashes match")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
