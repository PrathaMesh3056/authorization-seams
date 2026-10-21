#!/usr/bin/env python3
"""Fetch the two pinned upstream checkouts used by the APC pilot.

The upstream code is not redistributed in this repository. This script clones
the exact commits recorded in tests/authorization_pilot/pins.json into the
paths the harness expects, then verifies that each checkout is clean and on the
pinned commit.

Setup needs network access. Experiment execution is offline.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PINS = ROOT / "tests" / "authorization_pilot" / "pins.json"


def run(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        args,
        cwd=str(cwd) if cwd else None,
        text=True,
        capture_output=True,
        check=False,
    )


def head(path: Path) -> str:
    result = run(["git", "-C", str(path), "rev-parse", "HEAD"])
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git rev-parse failed")
    return result.stdout.strip()


def main() -> int:
    pins = json.loads(PINS.read_text(encoding="utf-8"))
    for name, pin in pins["repositories"].items():
        target = ROOT / pin["path"]
        commit = pin["commit"]
        if target.exists():
            current = head(target)
            if current != commit:
                print(
                    f"ERROR {name}: existing checkout is at {current}, expected {commit}\n"
                    f"      remove {target} and rerun if you want a fresh clone",
                    file=sys.stderr,
                )
                return 1
            print(f"ok {name}: {pin['path']} at {commit[:12]}")
            continue

        target.parent.mkdir(parents=True, exist_ok=True)
        print(f"cloning {name}: {pin['url']}")
        clone = run(
            [
                "git",
                "-c",
                "core.hooksPath=",
                "clone",
                "--quiet",
                pin["url"],
                str(target),
            ]
        )
        if clone.returncode != 0:
            print(f"ERROR {name}: clone failed\n{clone.stderr.strip()}", file=sys.stderr)
            return 1
        checkout = run(["git", "-C", str(target), "checkout", "--quiet", commit])
        if checkout.returncode != 0:
            print(
                f"ERROR {name}: checkout {commit} failed\n{checkout.stderr.strip()}",
                file=sys.stderr,
            )
            return 1
        current = head(target)
        status = run(["git", "-C", str(target), "status", "--porcelain"])
        if current != commit or status.stdout.strip():
            print(
                f"ERROR {name}: verification failed "
                f"(HEAD={current}, dirty={bool(status.stdout.strip())})",
                file=sys.stderr,
            )
            return 1
        print(f"ok {name}: {pin['path']} at {commit[:12]}")

    print("all pinned inputs ready")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
