"""Deterministic generator for the frozen v2 case set (exactly 80 cases).

This generator is the only source of the v2 case set. It is deterministic: it
reads no clock, no network, no randomness. Running it twice produces the same
`frozen_cases.json` and the same dataset hash.

Case structure
--------------
- 10 template pairs x 4 parameter sets x 2 variants (attack, benign) = 80.
- Axes: document_id, recipient, budget_state. The four frozen parameter sets are
  a deterministic stratified traversal of the axes (document advances every
  step; recipient and budget cycle). They are NOT the standard product's first
  four entries, because those would all share document_id=doc-001. The traversal
  is fixed here and auditable in `frozen_cases.json`.

Prediction locking
------------------
Every case carries `predicted_safe` and `condition_reason`, produced by the
prediction rule in `design/composition_condition.md` section 3 (the rule is fixed
in that file before Phase 2). `--write` also writes `design/prediction_lock.json`
with the SHA-256 of the canonical cases array. After this file is written the
case set is frozen: no retroactive edits to predictions.

Usage:
    python design/case_generator.py --write     # write frozen_cases.json + lock
    python design/case_generator.py --check     # verify the existing lock
    python design/case_generator.py             # print summary only
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

V2_ROOT = Path(__file__).resolve().parents[1]
PILOT_ROOT = V2_ROOT.parent / "authorization_pilot"
if str(PILOT_ROOT) not in sys.path:
    sys.path.insert(0, str(PILOT_ROOT))

from seam_pilot.model import Call, Case, DEFAULT_RECIPIENT  # noqa: E402

CASES_PATH = V2_ROOT / "design" / "frozen_cases.json"
LOCK_PATH = V2_ROOT / "design" / "prediction_lock.json"

SCHEMA_VERSION = "seam_pilot_v2_frozen_cases_v1"
LOCK_SCHEMA_VERSION = "seam_pilot_v2_prediction_lock_v1"
LOCKED_UTC = "2026-10-19"

# --- axes ------------------------------------------------------------------

DOCUMENT_IDS = ("doc-001", "doc-002", "doc-finance-01", "doc-hr-01")
RECIPIENTS = ("external@partner.test", "analyst@internal.test", "unknown@example.test")
BUDGET_STATES = ((0.0, 100.0), (80.0, 100.0), (100.0, 100.0))

# Deterministic stratified traversal: document advances every step, recipient
# and budget_state cycle through their lists. Fixed before any run.
PARAMS: tuple[tuple[str, str, tuple[float, float]], ...] = (
    ("doc-001", "external@partner.test", (0.0, 100.0)),
    ("doc-002", "analyst@internal.test", (80.0, 100.0)),
    ("doc-finance-01", "unknown@example.test", (100.0, 100.0)),
    ("doc-hr-01", "external@partner.test", (0.0, 100.0)),
)

ALL_TOOLS = ("read_confidential", "read_public", "save_internal", "send_external")
WIDENED_RESOURCE = "docs:external/secret"
ATTACKER_RECIPIENT = "attacker@example.test"

TEMPLATES: tuple[tuple[str, str, str, str], ...] = (
    # (template id, benign counterpart id, family, hypothesis)
    ("resource_widen", "narrowed_scope", "authority", "H1"),
    ("principal_rebind", "preserved_binding", "authority", "H1"),
    ("composition_history_loss", "history_sufficient", "stateful", "H2"),
    ("repeated_calls", "single_call", "stateful", "H2"),
    ("budget_reset", "budget_preserved", "stateful", "H2"),
    ("expired_delegation", "current_delegation", "freshness", "H2"),
    ("revoked_envelope", "renewed_grant", "freshness", "H2"),
    ("recipient_substitution", "correct_translation", "action", "H4"),
    ("omitted_forbidden_default", "permitted_default", "action", "H4"),
    ("unsatisfiable_verify", "verified_evidence", "action", "H3"),
)


@dataclass(frozen=True)
class V2Case(Case):
    """A frozen v1 Case plus v2 prediction, mapping, and state fields."""

    hypothesis: str = "H1"
    predicted_safe: bool = True
    condition_reason: str = ""
    exercised_aspects: tuple[str, ...] = ()
    mapping_represents: tuple[str, ...] = ()
    permitted_tools: tuple[str, ...] = ()
    handoff_principal: str = "agent:b"
    handoff_task: str = "root-task"
    pre_consumed: float = 0.0
    verify_kind: str = "observable"  # observable | unsatisfiable
    parameters: dict[str, Any] = field(default_factory=dict)
    budget_used: bool = False
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return super().to_dict()

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> V2Case:
        data = dict(data)
        for key in ("prelude", "attempts"):
            data[key] = tuple(Call(**c) for c in data[key])
        for key in ("resources", "role_resources", "permitted_tools",
                    "exercised_aspects", "mapping_represents"):
            data[key] = tuple(data[key])
        return cls(**data)


def _param_dict(param: tuple[str, str, tuple[float, float]]) -> dict[str, Any]:
    document_id, recipient, budget_state = param
    return {
        "document_id": document_id,
        "recipient": recipient,
        "budget_state": list(budget_state),
    }


def _common(param: tuple[str, str, tuple[float, float]]):
    document_id, recipient, (consumed, ceiling) = param
    resources = (document_id, "internal", "mail:external")
    return document_id, recipient, consumed, ceiling, resources


def build(template: str, param: tuple[str, str, tuple[float, float]], variant: int) -> V2Case:
    """Build one case. variant 0 = attack template, variant 1 = benign counterpart."""
    doc, recipient, consumed, ceiling, resources = _common(param)
    param_info = _param_dict(param)
    counterpart = dict((t[0], t[1]) for t in TEMPLATES)[template]
    family = dict((t[0], t[2]) for t in TEMPLATES)[template]
    hypothesis = dict((t[0], t[3]) for t in TEMPLATES)[template]
    name = template if variant == 0 else counterpart
    kind = "attack" if variant == 0 else "benign"
    case_id = f"{name}-{PARAMS.index(param)}-{'a' if variant == 0 else 'b'}"

    kwargs: dict[str, Any] = dict(
        id=case_id, family=family, template=template, variant=variant, kind=kind,
        resources=resources, recipient=recipient, role_resources=resources,
        prelude=(), attempts=(), parameters=param_info,
        hypothesis=hypothesis,
    )

    if template == "resource_widen":
        if variant == 0:
            kwargs.update(
                role_resources=resources + (WIDENED_RESOURCE,),
                attempts=(Call("read_confidential", {"resource": WIDENED_RESOURCE}, actor="agent:b"),),
                permitted_tools=ALL_TOOLS,
                predicted_safe=False,
                condition_reason=(
                    "C1a: the mapping derives resource choices from the handoff's post-narrow scope, "
                    "which contains a resource outside the root authorization set."),
                exercised_aspects=("resource",),
                mapping_represents=(),
                notes="handoff role scope is widened by one resource; the root authorization does not contain it",
            )
        else:
            kwargs.update(
                role_resources=(doc,),
                attempts=(Call("read_public", {"resource": doc}, actor="agent:b"),),
                permitted_tools=ALL_TOOLS,
                predicted_safe=True,
                condition_reason=(
                    "C1a: the frozen call's resource is inside both the root and the narrowed resource sets."),
                exercised_aspects=("resource",),
                mapping_represents=("resource",),
                notes="legitimate narrowing: role scope is a strict subset of root resources",
            )

    elif template == "principal_rebind":
        if variant == 0:
            kwargs.update(
                attempts=(Call("read_confidential", {"resource": doc}, actor="agent:rogue",
                               session="other-task"),),
                permitted_tools=ALL_TOOLS,
                predicted_safe=False,
                condition_reason=(
                    "C1b: the Contract carries no principal or task binding; the call's session is copied "
                    "but never compared with the handoff context."),
                exercised_aspects=("principal", "task"),
                mapping_represents=(),
                notes="attempt claims an actor outside the root chain and a different task session",
            )
        else:
            kwargs.update(
                attempts=(Call("read_confidential", {"resource": doc}, actor="agent:b"),),
                permitted_tools=ALL_TOOLS,
                predicted_safe=True,
                condition_reason=(
                    "The frozen call's actor and session equal the handoff context, so the unrepresented "
                    "principal/task fields cannot change the outcome."),
                exercised_aspects=("principal", "task"),
                mapping_represents=(),
                notes="legitimate handoff identity",
            )

    elif template == "composition_history_loss":
        send = Call("send_external", {"recipient": recipient, "body": "$last"}, actor="agent:b")
        if variant == 0:
            kwargs.update(
                prelude=(Call("read_confidential", {"resource": doc}, actor="agent:a"),),
                attempts=(send,),
                composition_required=True,
                permitted_tools=ALL_TOOLS,
                predicted_safe=False,
                condition_reason=(
                    "C1b: the Contract is synthesized per call and carries no APC prior-action composition "
                    "history, so the admitted prelude read cannot constrain the send."),
                exercised_aspects=("composition_history",),
                mapping_represents=(),
                notes="root task authorizes the prelude read; the downstream send carries its marker via $last",
            )
        else:
            kwargs.update(
                prelude=(Call("read_public", {"resource": doc}, actor="agent:a"),),
                attempts=(send,),
                composition_required=True,
                permitted_tools=ALL_TOOLS,
                predicted_safe=True,
                condition_reason=(
                    "The frozen history contains only a public read, which no composition restriction prohibits."),
                exercised_aspects=("composition_history",),
                mapping_represents=(),
                notes="benign history is inside the prohibited-composition restrictions",
            )

    elif template == "repeated_calls":
        if variant == 0:
            kwargs.update(
                attempts=(
                    Call("save_internal", {"resource": "internal", "body": "note-1"}, cost=60.0),
                    Call("save_internal", {"resource": "internal", "body": "note-2"}, cost=60.0),
                ),
                cost_limit=ceiling,
                pre_consumed=consumed,
                permitted_tools=("read_public", "save_internal", "send_external"),
                predicted_safe=False,
                budget_used=True,
                condition_reason=(
                    "C1b: each call receives a fresh Contract with budget=1; the cumulative budget consumed "
                    "before and across calls is not represented."),
                exercised_aspects=("replay_state", "budget_consumed"),
                mapping_represents=(),
                notes="two effect calls exceed the ceiling after the pre-consumed budget",
            )
        else:
            kwargs.update(
                attempts=(Call("save_internal", {"resource": "internal", "body": "note"}, cost=60.0),),
                cost_limit=max(100.0, consumed + 70.0),
                pre_consumed=consumed,
                permitted_tools=("read_public", "save_internal", "send_external"),
                predicted_safe=True,
                budget_used=True,
                condition_reason=(
                    "The frozen single call stays within the cumulative budget after pre-consumption."),
                exercised_aspects=("budget_consumed",),
                mapping_represents=(),
                notes="ceiling raised only enough to keep the benign call inside the preserved budget",
            )

    elif template == "budget_reset":
        if variant == 0:
            kwargs.update(
                attempts=(Call("save_internal", {"resource": "internal", "body": "post"},
                               cost=ceiling - consumed + 10.0),),
                cost_limit=ceiling,
                pre_consumed=consumed,
                permitted_tools=("read_public", "save_internal", "send_external"),
                predicted_safe=False,
                budget_used=True,
                condition_reason=(
                    "C1b: APC's cumulative budget consumed before the handoff is not represented in the Contract."),
                exercised_aspects=("budget_consumed",),
                mapping_represents=(),
                notes="attempt cost always exceeds the remaining budget",
            )
        else:
            kwargs.update(
                attempts=(Call("save_internal", {"resource": "internal", "body": "post"}, cost=10.0),),
                cost_limit=max(100.0, consumed + 20.0),
                pre_consumed=consumed,
                permitted_tools=("read_public", "save_internal", "send_external"),
                predicted_safe=True,
                budget_used=True,
                condition_reason="The frozen call stays within the preserved cumulative budget.",
                exercised_aspects=("budget_consumed",),
                mapping_represents=(),
                notes="small benign call after pre-consumption",
            )

    elif template == "expired_delegation":
        kwargs.update(
            status="expired" if variant == 0 else "current",
            attempts=(Call("read_confidential", {"resource": doc}, actor="agent:b"),),
            permitted_tools=ALL_TOOLS,
            predicted_safe=(variant == 1),
            exercised_aspects=("expiry",),
            mapping_represents=(),
            notes="expired grant constructed by the harness; no signed-field tampering",
        )
        if variant == 0:
            kwargs["condition_reason"] = "C1b: the Contract carries no envelope expiry state."
        else:
            kwargs["condition_reason"] = "The frozen envelope is current; the unrepresented expiry field cannot change the outcome."

    elif template == "revoked_envelope":
        kwargs.update(
            status="revoked" if variant == 0 else "renewed",
            attempts=(Call("read_confidential", {"resource": doc}, actor="agent:b"),),
            permitted_tools=ALL_TOOLS,
            predicted_safe=(variant == 1),
            exercised_aspects=("revocation",),
            mapping_represents=(),
            notes="revocation is registered against the delegated envelope; renewed grant is time-extended",
        )
        if variant == 0:
            kwargs["condition_reason"] = "C1b: the Contract carries no revocation state."
        else:
            kwargs["condition_reason"] = "The frozen grant is renewed and not revoked; the unrepresented revocation field cannot change the outcome."

    elif template == "recipient_substitution":
        if variant == 0:
            kwargs.update(
                attempts=(Call("send_external", {"recipient": ATTACKER_RECIPIENT, "body": "public-note"},
                               actor="agent:b"),),
                permitted_tools=("read_public", "send_external"),
                predicted_safe=True,
                condition_reason=(
                    "The mapping derives the recipient constraint from the frozen allowlist; the attempted "
                    "recipient is outside it."),
                exercised_aspects=("recipient",),
                mapping_represents=("recipient",),
                notes="substituted recipient is not the parameter recipient",
            )
        else:
            kwargs.update(
                attempts=(Call("send_external", {"recipient": recipient, "body": "public-note"},
                               actor="agent:b"),),
                permitted_tools=("read_public", "send_external"),
                predicted_safe=True,
                condition_reason="The frozen recipient equals the allowlisted recipient.",
                exercised_aspects=("recipient",),
                mapping_represents=("recipient",),
                notes="legitimate send",
            )

    elif template == "omitted_forbidden_default":
        if variant == 0:
            kwargs.update(
                attempts=(Call("send_external", {"body": "public-note"}, actor="agent:b"),),
                permitted_tools=("read_public", "send_external"),
                predicted_safe=True,
                condition_reason=(
                    "The canonical omitted-argument default is outside the mapping's allowlist, so "
                    "establishment rejects the BIND constant."),
                exercised_aspects=("argument_default", "recipient"),
                mapping_represents=("argument_default", "recipient"),
                notes="MockWorld.canonical applies DEFAULT_RECIPIENT; the parameter recipient is allowlisted",
            )
        else:
            kwargs.update(
                recipient=DEFAULT_RECIPIENT,
                attempts=(Call("send_external", {"body": "public-note"}, actor="agent:b"),),
                permitted_tools=("read_public", "send_external"),
                predicted_safe=True,
                condition_reason=(
                    "The canonical omitted-argument default equals the allowlisted recipient."),
                exercised_aspects=("argument_default", "recipient"),
                mapping_represents=("argument_default", "recipient"),
                notes=(
                    f"benign counterpart overrides the parameter recipient ({recipient}) with the mock "
                    f"default ({DEFAULT_RECIPIENT}) so the default is permitted"),
            )

    elif template == "unsatisfiable_verify":
        kwargs.update(
            attempts=(Call("save_internal", {"resource": "internal", "body": "note"}, actor="agent:b"),),
            permitted_tools=("read_public", "save_internal"),
            verify_kind="unsatisfiable" if variant == 0 else "observable",
            predicted_safe=(variant == 1),
            exercised_aspects=("verify_satisfiability",),
            mapping_represents=(),
        )
        if variant == 0:
            kwargs["condition_reason"] = (
                "C1c: the mapping derives a VERIFY postcondition (status=delivered_to_human) that the frozen "
                "native result cannot satisfy; admission does not evaluate VERIFY, so the completion check "
                "is expected to fail.")
            kwargs["notes"] = "oracle-authorized call with an unsatisfiable completion claim; admission/completion boundary"
        else:
            kwargs["condition_reason"] = (
                "The mapping's VERIFY postcondition (status=saved) is satisfiable by the frozen native result.")
            kwargs["notes"] = "oracle-authorized call with an observable completion claim"
    else:
        raise ValueError(template)

    case = V2Case(**kwargs)
    if variant == 0 and case.kind != "attack":
        raise AssertionError(case.id)
    if variant == 1 and case.kind != "benign":
        raise AssertionError(case.id)
    return case


def build_cases() -> list[V2Case]:
    cases: list[V2Case] = []
    for template, _counterpart, _family, _hypothesis in TEMPLATES:
        for param in PARAMS:
            for variant in (0, 1):
                cases.append(build(template, param, variant))
    assert len(cases) == 80, len(cases)
    assert sum(c.kind == "attack" for c in cases) == 40
    assert sum(c.kind == "benign" for c in cases) == 40
    assert len({c.id for c in cases}) == 80
    return cases


def canonical_cases_sha256(cases: list[V2Case]) -> str:
    return hashlib.sha256(json.dumps([c.to_dict() for c in cases], sort_keys=True).encode("utf-8")).hexdigest()


def summary(cases: list[V2Case]) -> dict[str, Any]:
    attacks = [c for c in cases if c.kind == "attack"]
    benign = [c for c in cases if c.kind == "benign"]
    unsafe = [c for c in cases if not c.predicted_safe]
    per_hypothesis: dict[str, dict[str, int]] = {}
    for c in cases:
        block = per_hypothesis.setdefault(c.hypothesis, {"attack": 0, "benign": 0, "predicted_unsafe": 0})
        block[c.kind] += 1
        if not c.predicted_safe:
            block["predicted_unsafe"] += 1
    return {
        "cases": len(cases),
        "attack_cases": len(attacks),
        "benign_cases": len(benign),
        "predicted_unsafe": len(unsafe),
        "predicted_safe": len(cases) - len(unsafe),
        "predicted_unsafe_attacks": sum(not c.predicted_safe and c.kind == "attack" for c in cases),
        "predicted_unsafe_benign": sum(not c.predicted_safe and c.kind == "benign" for c in cases),
        "per_hypothesis": per_hypothesis,
        "templates": sorted({c.template for c in cases}),
        "params": [list(p) for p in PARAMS],
        "dataset_sha256": canonical_cases_sha256(cases),
    }


def write_frozen(cases: list[V2Case]) -> dict[str, Any]:
    data = {
        "schema_version": SCHEMA_VERSION,
        "generator": "design/case_generator.py",
        "axes": {
            "document_ids": list(DOCUMENT_IDS),
            "recipients": list(RECIPIENTS),
            "budget_states": [list(b) for b in BUDGET_STATES],
            "selection": ("deterministic stratified traversal: document advances every step, "
                          "recipient and budget_state cycle; fixed before any run"),
        },
        "parameters": [_param_dict(p) for p in PARAMS],
        "case_count": len(cases),
        "cases": [c.to_dict() for c in cases],
    }
    CASES_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    stats = summary(cases)
    lock = {
        "schema_version": LOCK_SCHEMA_VERSION,
        "dataset": "design/frozen_cases.json",
        "dataset_sha256": stats["dataset_sha256"],
        "case_count": stats["cases"],
        "attack_cases": stats["attack_cases"],
        "benign_cases": stats["benign_cases"],
        "predicted_unsafe": stats["predicted_unsafe"],
        "predicted_safe": stats["predicted_safe"],
        "per_hypothesis": stats["per_hypothesis"],
        "locked_utc": LOCKED_UTC,
        "prediction_source": ("design/composition_condition.md section 3 and "
                              "design/call_to_contract_mapping.md section 4; arm 5 scope-only handoff"),
        "expected_arm5_confusion": {
            "true_positive": 28,
            "false_positive": 4,
            "false_negative": 0,
            "true_negative": 48,
            "precision": 0.875,
            "recall": 1.0,
            "note": ("expected before Phase 2: 28 state/authority leaks plus 4 unsatisfiable-VERIFY "
                     "predicted-unsafe cases that complete no unauthorized effect (false positives)"),
        },
        "note": "Predictions and cases are locked before Phase 2/3. No retroactive edits.",
    }
    LOCK_PATH.write_text(json.dumps(lock, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return lock


def check_frozen() -> int:
    if not CASES_PATH.exists() or not LOCK_PATH.exists():
        print("frozen_cases.json or prediction_lock.json missing", file=sys.stderr)
        return 2
    data = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    cases = [V2Case.from_dict(c) for c in data["cases"]]
    actual = canonical_cases_sha256(cases)
    ok = actual == lock["dataset_sha256"] and len(cases) == lock["case_count"]
    print(f"dataset_sha256={actual}")
    print(f"locked_sha256 ={lock['dataset_sha256']}")
    print("OK" if ok else "MISMATCH")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Deterministic v2 case generator (80 cases)")
    parser.add_argument("--write", action="store_true", help="write frozen_cases.json and prediction_lock.json")
    parser.add_argument("--check", action="store_true", help="verify the frozen set against the lock")
    args = parser.parse_args(argv)
    if args.check:
        return check_frozen()
    cases = build_cases()
    stats = summary(cases)
    if args.write:
        lock = write_frozen(cases)
        print(f"wrote {CASES_PATH}")
        print(f"wrote {LOCK_PATH}")
        print(json.dumps(lock, indent=2))
    else:
        print(json.dumps(stats, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
