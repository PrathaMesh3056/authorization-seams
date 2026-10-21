#!/usr/bin/env python3
"""Build a review zip from tracked files after verifying the manifest.

The zip is written under dist/ and contains only files covered by
artifacts/sha256sums.txt. It is a **review package**: frozen artifacts still
contain their recorded machine-local paths. For a public release, first run
scripts/sanitize_release.py and publish dist/sanitized/ with fresh Git history.
"""
from __future__ import annotations

import hashlib
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import repo_common  # noqa: E402
import verify_artifacts  # noqa: E402

DIST = repo_common.ROOT / "dist"
PACKAGE_NAME = "seam-conformance-kit"
FIXED_TIMESTAMP = (2026, 10, 21, 0, 0, 0)


def main() -> int:
    if verify_artifacts.main() != 0:
        print("refusing to package: artifact verification failed", file=sys.stderr)
        return 1

    DIST.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    out = DIST / f"{PACKAGE_NAME}-{stamp}-review.zip"

    files = repo_common.tracked_files()
    # The manifest files are excluded from their own hash list but must ship.
    for extra in (repo_common.MANIFEST_TXT, repo_common.MANIFEST_JSON):
        if extra.exists() and extra not in files:
            files.append(extra)
    files = sorted(set(files), key=repo_common.rel_posix)
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            rel = repo_common.rel_posix(path)
            info = zipfile.ZipInfo(f"{PACKAGE_NAME}/{rel}", date_time=FIXED_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes())

    digest = hashlib.sha256(out.read_bytes()).hexdigest().upper()
    out.with_suffix(out.suffix + ".sha256").write_text(
        f"{digest}  {out.name}\n", encoding="ascii", newline="\n"
    )
    print(f"wrote {out.relative_to(repo_common.ROOT)} ({out.stat().st_size} bytes)")
    print(f"sha256 {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
