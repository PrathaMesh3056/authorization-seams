#!/usr/bin/env python3
"""Produce a sanitized release tree under dist/sanitized/.

The source tree keeps frozen artifacts byte-identical. This script copies the
tracked files and rewrites machine-local paths and the known placeholder email
in text files only. A JSON report records every file whose bytes changed and the
original SHA-256, so the sanitized copy can be traced back to the frozen file.

After sanitizing, the script regenerates the release manifest inside the
sanitized tree and preserves the frozen manifest as
`artifacts/sha256sums.frozen.txt`. The sanitized tree verifies against its own
`artifacts/sha256sums.txt`.

This script is a release helper, not a substitute for reviewing the diff.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import repo_common  # noqa: E402

DIST = repo_common.ROOT / "dist" / "sanitized"
TEXT_SUFFIXES = {
    ".md", ".txt", ".json", ".jsonl", ".py", ".ps1", ".sh", ".cff", ".toml",
    ".yml", ".yaml", ".tex", ".cfg", ".ini", ".csv", ".svg", ".gitignore",
    ".gitattributes", ".editorconfig",
}
TEXT_NAMES = {"Makefile", "LICENSE", "README", "CHANGELOG", "CONTRIBUTING"}
SKIP_REWRITE = {
    "scripts/sanitize_release.py",
    "docs/RELEASE_SANITIZATION.md",
}

REPLACEMENTS = [
    (re.compile(r"agentscan@gmail\.com"), "<EMAIL_REDACTED>"),
    # JSON-escaped Windows paths: C:\\Users\\name\\...
    (re.compile(r"[A-Za-z]:\\\\Users\\\\[^\"\\\s]+"), "<LOCAL_PATH>"),
    # Plain Windows paths: C:\Users\name\...
    (re.compile(r"[A-Za-z]:\\Users\\[^\\\s\"]+"), "<LOCAL_PATH>"),
    # Forward-slash Windows paths: C:/Users/name/...
    (re.compile(r"[A-Za-z]:/Users/[^/\s\"]+"), "<LOCAL_PATH>"),
    # POSIX/macOS home paths.
    (re.compile(r"/home/[^/\s\"]+"), "<LOCAL_PATH>"),
    (re.compile(r"/Users/[^/\s\"]+"), "<LOCAL_PATH>"),
]

RELEASE_NOTES = """\
# Sanitized release tree

This tree was produced by `scripts/sanitize_release.py` from the frozen
repository. Machine-local paths and the internal placeholder email were
rewritten in text files only; binary artifacts are byte-identical copies.

- `artifacts/sha256sums.txt` is the **release manifest** for this tree.
- `artifacts/sha256sums.frozen.txt` is the original frozen manifest.
- `SANITIZATION_REPORT.json` lists every changed file with its original
  SHA-256 and replacement count.

Verify this tree from its root:

    python scripts/verify_artifacts.py

Publish this tree with fresh Git history. Do not publish the working tree and
then delete paths: the original bytes would remain in history.
"""


def is_text(path: Path) -> bool:
    return path.suffix.lower() in TEXT_SUFFIXES or path.name in TEXT_NAMES


def sanitize(text: str) -> tuple[str, int]:
    count = 0
    for pattern, replacement in REPLACEMENTS:
        text, n = pattern.subn(replacement, text)
        count += n
    return text, count


def main() -> int:
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)

    report: list[dict] = []
    skipped: list[str] = []
    copied = 0
    changed = 0
    for path in repo_common.tracked_files():
        rel = repo_common.rel_posix(path)
        target = DIST / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if is_text(path) and rel not in SKIP_REWRITE:
            with path.open("r", encoding="utf-8", newline="") as handle:
                text = handle.read()
            new_text, count = sanitize(text)
            with target.open("w", encoding="utf-8", newline="") as handle:
                handle.write(new_text)
            if count:
                changed += 1
                report.append(
                    {
                        "path": rel,
                        "replacements": count,
                        "original_sha256": repo_common.sha256_file(path),
                    }
                )
        else:
            shutil.copyfile(path, target)
            if rel in SKIP_REWRITE:
                skipped.append(rel)
        copied += 1

    # Preserve the frozen manifest next to the release manifest.
    frozen_manifest = repo_common.MANIFEST_TXT
    if frozen_manifest.exists():
        (DIST / "artifacts").mkdir(parents=True, exist_ok=True)
        shutil.copyfile(frozen_manifest, DIST / "artifacts" / "sha256sums.frozen.txt")

    (DIST / "SANITIZATION_REPORT.json").write_text(
        json.dumps(
            {
                "source": "repository tracked files",
                "files_copied": copied,
                "files_changed": changed,
                "files_skipped": sorted(skipped),
                "changed": report,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    (DIST / "README_RELEASE.md").write_text(RELEASE_NOTES, encoding="utf-8", newline="\n")

    # Regenerate the release manifest inside the sanitized tree.
    manifest_result = subprocess.run(
        [sys.executable, "scripts/write_manifest.py"],
        cwd=str(DIST),
        text=True,
        capture_output=True,
        check=False,
    )
    if manifest_result.returncode != 0:
        print(
            "WARNING: could not regenerate the release manifest:\n"
            + manifest_result.stdout
            + manifest_result.stderr,
            file=sys.stderr,
        )

    # Remove caches created by running the manifest tool inside the release tree.
    for cache_name in ("__pycache__", ".pytest_cache"):
        for cache_dir in DIST.rglob(cache_name):
            if cache_dir.is_dir():
                shutil.rmtree(cache_dir, ignore_errors=True)

    print(f"sanitized tree: {DIST}")
    print(f"files copied: {copied}; files changed: {changed}; files skipped: {len(skipped)}")
    for item in report:
        print(f"  {item['replacements']:>3}  {item['path']}")
    print("review dist/sanitized/ and SANITIZATION_REPORT.json before publishing")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
