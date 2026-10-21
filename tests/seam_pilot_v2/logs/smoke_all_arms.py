"""Smoke test: one case across all seven arms. Not a result; a wiring check."""
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
    by_template = {}
    for case in cases:
        by_template.setdefault(case.template, case)
    for template, case in by_template.items():
        print(f"--- {template} ({case.id})")
        for arm in ARMS_V2:
            run = run_case(case, arm)
            trail = []
            for event in run["events"]:
                receipt = event.get("receipt_ok")
                trail.append(f"{event['phase'][:2]}:{event['tool']} allow={int(event['allowed'])} "
                             f"oracle={int(event['oracle_allowed'])} "
                             f"unauth={int(event['unauthorized_effect'])} "
                             f"receipt={('-' if receipt is None else int(receipt))}")
            print(f"  {arm:32s} " + " | ".join(trail))


if __name__ == "__main__":
    main()
