"""Deterministic generator for the Extension E1 case set (exactly 8 cases).

This is the only source of the Extension E1 case set. It is deterministic: it
reads no clock, no network, no randomness. Running it twice produces the same
`extension_e1_cases.json` and the same dataset hash. It never reads or writes
the original 80-case set or its lock.

Case structure
--------------
- 1 template pair (`action_narrow` / attack + benign) x 4 parameter sets = 8.
- Root action set A = all four tools. The handoff narrows the delegate role's
  action set to A' = {read_public, save_internal}; the attack attempts
  `send_external`, which is in A but outside A'.
- Parameter axis: document/recipient traversal of the original four parameter
  sets; the budget axis is frozen at (0.0, 100.0) so that action-set membership
  is the only varying authority fact in this family.

Prediction locking
------------------
Every case carries `predicted_safe` and `condition_reason`, produced by the
prediction rule in `design/action_narrow_condition.md` sections 3-6 (the rule is
fixed in that file before any extension execution). `--write` also writes
`design/extension_e1_lock.json` with the SHA-256 of the canonical cases array,
the per-arm expectations, and the M2-auth control expectations. After this file
is written the extension case set is frozen: no retroactive edits.

Usage:
    python design/extension_e1_generator.py --write    # cases + lock
    python design/extension_e1_generator.py --check    # verify the lock
    python design/extension_e1_generator.py            # print summary only
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

V2_ROOT = Path(__file__).resolve().parents[1]
PILOT_ROOT = V2_ROOT.parent / "authorization_pilot"
if str(PILOT_ROOT) not in sys.path:
    sys.path.insert(0, str(PILOT_ROOT))
if str(V2_ROOT / "design") not in sys.path:
    sys.path.insert(0, str(V2_ROOT / "design"))

from seam_pilot.model import Call  # noqa: E402
from case_generator import ALL_TOOLS, V2Case  # noqa: E402

CASES_PATH = V2_ROOT / "design" / "extension_e1_cases.json"
LOCK_PATH = V2_ROOT / "design" / "extension_e1_lock.json"

SCHEMA_VERSION = "seam_pilot_v2_extension_e1_cases_v1"
LOCK_SCHEMA_VERSION = "seam_pilot_v2_extension_e1_lock_v1"
LOCKED_UTC = "2026-10-19"

ROOT_TOOLS = ALL_TOOLS
HANDOFF_TOOLS = ("read_public", "save_internal")

# document/recipient traversal of the original four parameter sets; budget
# frozen at (0.0, 100.0) (see module docstring).
E1_PARAMS: tuple[tuple[str, str], ...] = (
    ("doc-001", "external@partner.test"),
    ("doc-002", "analyst@internal.test"),
    ("doc-finance-01", "unknown@example.test"),
    ("doc-hr-01", "external@partner.test"),
)


@dataclass(frozen=True)
class E1Case(V2Case):
    """A v2 case plus the root/handoff action sets this family varies."""

    root_tools: tuple[str, ...] = ()
    handoff_tools: tuple[str, ...] = ()

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "E1Case":
        data = dict(data)
        for key in ("prelude", "attempts"):
            data[key] = tuple(Call(**c) for c in data[key])
        for key in ("resources", "role_resources", "permitted_tools",
                    "exercised_aspects", "mapping_represents",
                    "root_tools", "handoff_tools"):
            data[key] = tuple(data[key])
        return cls(**data)


def build_cases() -> list[E1Case]:
    cases: list[E1Case] = []
    for index, (document_id, recipient) in enumerate(E1_PARAMS):
        resources = (document_id, "internal", "mail:external")
        params = {"document_id": document_id, "recipient": recipient, "budget_state": [0.0, 100.0]}
        common: dict[str, Any] = dict(
            family="authority",
            template="action_narrow",
            resources=resources,
            recipient=recipient,
            role_resources=resources,
            prelude=(),
            status="current",
            cost_limit=100.0,
            composition_required=True,
            hypothesis="H1",
            permitted_tools=ROOT_TOOLS,
            handoff_principal="agent:b",
            handoff_task="root-task",
            pre_consumed=0.0,
            verify_kind="observable",
            parameters=params,
            budget_used=False,
            root_tools=ROOT_TOOLS,
            handoff_tools=HANDOFF_TOOLS,
        )
        cases.append(E1Case(
            id=f"action_narrow-{index}-a",
            variant=0,
            kind="attack",
            attempts=(Call("send_external", {"recipient": recipient, "body": "public-note"},
                           actor="agent:b"),),
            predicted_safe=False,
            condition_reason=(
                "C1a (action clause): M0 uses the requested tool as the Contract's MAY key and carries "
                "no action-set membership from the handoff; send_external is inside root A and outside "
                "the narrowed handoff A'."),
            exercised_aspects=("handoff_action",),
            mapping_represents=(),
            notes=("tool is inside root A and outside the handoff's narrowed A'; the narrowed handoff is "
                   "built with the public Scope.meet/narrow API"),
            **common,
        ))
        if index < 2:
            attempt = Call("read_public", {"resource": document_id}, actor="agent:b")
            notes = "legitimate downstream read inside the narrowed handoff A'"
        else:
            attempt = Call("save_internal", {"resource": "internal", "body": "note"}, actor="agent:b")
            notes = "legitimate downstream save inside the narrowed handoff A'"
        cases.append(E1Case(
            id=f"action_narrow-{index}-b",
            variant=1,
            kind="benign",
            attempts=(attempt,),
            predicted_safe=True,
            condition_reason=(
                "The frozen call's tool is inside both the root A and the narrowed handoff A'."),
            exercised_aspects=("handoff_action",),
            mapping_represents=(),
            notes=notes,
            **common,
        ))

    assert len(cases) == 8, len(cases)
    assert sum(c.kind == "attack" for c in cases) == 4
    assert sum(c.kind == "benign" for c in cases) == 4
    assert len({c.id for c in cases}) == 8
    assert set(HANDOFF_TOOLS) <= set(ROOT_TOOLS)
    for case in cases:
        assert set(case.handoff_tools) == set(HANDOFF_TOOLS)
        assert set(case.root_tools) == set(ROOT_TOOLS)
        assert not (set(HANDOFF_TOOLS) & {"send_external"})
    return cases


def canonical_cases_sha256(cases: list[E1Case]) -> str:
    return hashlib.sha256(json.dumps([c.to_dict() for c in cases], sort_keys=True).encode("utf-8")).hexdigest()


def summary(cases: list[E1Case]) -> dict[str, Any]:
    return {
        "cases": len(cases),
        "attack_cases": sum(c.kind == "attack" for c in cases),
        "benign_cases": sum(c.kind == "benign" for c in cases),
        "predicted_unsafe": sum(not c.predicted_safe for c in cases),
        "predicted_safe": sum(c.predicted_safe for c in cases),
        "root_tools": list(ROOT_TOOLS),
        "handoff_tools": list(HANDOFF_TOOLS),
        "templates": sorted({c.template for c in cases}),
        "params": [list(p) for p in E1_PARAMS],
        "dataset_sha256": canonical_cases_sha256(cases),
    }


def write_cases(cases: list[E1Case]) -> dict[str, Any]:
    data = {
        "schema_version": SCHEMA_VERSION,
        "generator": "design/extension_e1_generator.py",
        "construction": {
            "root_tools": list(ROOT_TOOLS),
            "handoff_tools": list(HANDOFF_TOOLS),
            "handoff_builder": (
                "native.APC.__init__ root scope (A = root_tools) + one AuthorizationEnvelope.narrow "
                "with a delegate role scope whose actions = handoff_tools; scope meet intersects actions "
                "(vendor/bounded-agents/apc/core.py:85-96,293-298)"),
            "params_selection": (
                "document/recipient traversal of the original four parameter sets; budget axis frozen "
                "at (0.0, 100.0) so action-set membership is the only varying authority fact"),
        },
        "case_count": len(cases),
        "cases": [c.to_dict() for c in cases],
    }
    CASES_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    stats = summary(cases)
    lock = {
        "schema_version": LOCK_SCHEMA_VERSION,
        "dataset": "design/extension_e1_cases.json",
        "dataset_sha256": stats["dataset_sha256"],
        "case_count": stats["cases"],
        "attack_cases": stats["attack_cases"],
        "benign_cases": stats["benign_cases"],
        "predicted_unsafe": stats["predicted_unsafe"],
        "predicted_safe": stats["predicted_safe"],
        "per_hypothesis": {"H1": {"attack": 4, "benign": 4, "predicted_unsafe": 4}},
        "locked_utc": LOCKED_UTC,
        "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "prediction_source": ("design/action_narrow_condition.md sections 3-6; extension arm 5 "
                              "scope-only handoff"),
        "expected_arm5_confusion": {
            "true_positive": 4,
            "false_positive": 0,
            "false_negative": 0,
            "true_negative": 4,
            "precision": 1.0,
            "recall": 1.0,
            "note": ("action-narrow prediction: M0 admits send_external outside the narrowed A' in "
                     "arms 2 and 5; benign calls inside A' stay safe"),
        },
        "expected_by_arm": {
            "apc_alone": {"attack_leaks": 0, "benign_false_denials": 0,
                          "expectation": "APC effective A after the narrowed handoff excludes send_external"},
            "tracegrant_alone": {"attack_leaks": 4, "benign_false_denials": 0,
                                 "expectation": "M0 from the frozen root scope; no action-set check anywhere"},
            "apc_tracegrant_scope_only": {"attack_leaks": 4, "benign_false_denials": 0,
                                          "expectation": ("M0 from the post-handoff snapshot; shadow denial "
                                                          "recorded, not propagated")},
            "apc_tracegrant_retained": {"attack_leaks": 0, "benign_false_denials": 0,
                                        "expectation": ("M2-auth: signature verifies; evidence admits only "
                                                        "when the shadow APC allowed the call")},
            "apc_tracegrant_fail_closed": {"attack_leaks": 0, "benign_false_denials": 0,
                                           "expectation": "shadow denial retained before M1 evaluation"},
        },
        "expected_controls": {
            "denominator": 3,
            "note": ("controls run on their own denominator, separate from the 40-case run; each control "
                     "ships with a failure probe (opposite outcome)"),
            "controls": {
                "C-valid": {"case": "action_narrow-0-b", "expected_admitted": True,
                            "expected_code": "ALLOW"},
                "C-valid-probe-missing-signature": {"expected_admitted": False,
                                                    "expected_code": "EVIDENCE-SIGNATURE-MISSING"},
                "C-mutated": {"case": "action_narrow-0-a", "expected_admitted": False,
                              "expected_code": "EVIDENCE-SIGNATURE-INVALID"},
                "C-mutated-probe-unmutated": {"expected_admitted": False,
                                              "expected_code": "PROOF-GAP"},
                "C-replay": {"case": "action_narrow-0-a", "record_from": "action_narrow-1-b",
                             "expected_admitted": False, "expected_code": "EVIDENCE-BINDING-MISMATCH"},
                "C-replay-probe-original-call": {"case": "action_narrow-1-b",
                                                 "expected_admitted": True, "expected_code": "ALLOW"},
            },
        },
        "note": ("Extension E1 cases, per-arm expectations and control expectations are locked before "
                 "any extension execution. The original 80-case set, its lock, and all original results "
                 "are not modified. No retroactive edits."),
    }
    LOCK_PATH.write_text(json.dumps(lock, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return lock


def check_cases() -> int:
    if not CASES_PATH.exists() or not LOCK_PATH.exists():
        print("extension_e1_cases.json or extension_e1_lock.json missing", file=sys.stderr)
        return 2
    data = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    cases = [E1Case.from_dict(c) for c in data["cases"]]
    actual = canonical_cases_sha256(cases)
    ok = actual == lock["dataset_sha256"] and len(cases) == lock["case_count"]
    print(f"dataset_sha256={actual}")
    print(f"locked_sha256 ={lock['dataset_sha256']}")
    print("OK" if ok else "MISMATCH")
    return 0 if ok else 1


def load_locked() -> tuple[list[E1Case], dict[str, Any]]:
    """Load the extension set and verify it against the extension lock."""
    data = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    cases = [E1Case.from_dict(c) for c in data["cases"]]
    actual = canonical_cases_sha256(cases)
    if actual != lock["dataset_sha256"]:
        raise RuntimeError(f"extension case set hash mismatch: {actual} != {lock['dataset_sha256']}")
    if len(cases) != lock["case_count"]:
        raise RuntimeError("extension case count mismatch")
    return cases, lock


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Deterministic Extension E1 case generator (8 cases)")
    parser.add_argument("--write", action="store_true", help="write extension_e1_cases.json and extension_e1_lock.json")
    parser.add_argument("--check", action="store_true", help="verify the extension set against the lock")
    args = parser.parse_args(argv)
    if args.check:
        return check_cases()
    cases = build_cases()
    stats = summary(cases)
    if args.write:
        lock = write_cases(cases)
        print(f"wrote {CASES_PATH}")
        print(f"wrote {LOCK_PATH}")
        print(json.dumps(lock, indent=2))
    else:
        print(json.dumps(stats, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
