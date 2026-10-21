"""Smoke test 2: benign counterparts across all seven arms."""
import sys
from pathlib import Path

V2_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(V2_ROOT / "adapters"))
sys.path.insert(0, str(V2_ROOT / "design"))

from v2_common import ARMS_V2, load_frozen_cases, prepare  # noqa: E402
from arms import run_case  # noqa: E402


def main() -> None:
    prepare()
    cases, _lock = load_frozen_cases()
    benign = [c for c in cases if c.kind == "benign" and c.variant == 1]
    for case in benign:
        print(f"--- {case.template} -> {case.id}")
        for arm in ARMS_V2:
            run = run_case(case, arm)
            trail = []
            for event in run["events"]:
                receipt = event.get("receipt_ok")
                trail.append(f"{event['phase'][:2]}:{event['tool']} allow={int(event['allowed'])} "
                             f"oracle={int(event['oracle_allowed'])} fd={int(event['false_denial'])} "
                             f"receipt={('-' if receipt is None else int(receipt))}")
            print(f"  {arm:32s} " + " | ".join(trail))


if __name__ == "__main__":
    main()
