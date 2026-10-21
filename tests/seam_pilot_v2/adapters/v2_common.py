"""Shared v2 harness types: case loading, oracle, APC wrapper, scope snapshots.

No upstream file is modified. The APC wrapper composes the existing
`seam_pilot.native.APC` unchanged; the only additions are a restricted-action
proxy (so the root scope's action set is the case's `permitted_tools`), an
explicit pre-consumed budget, and snapshot/visibility helpers.
"""
from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

V2_ROOT = Path(__file__).resolve().parents[1]
PILOT_ROOT = V2_ROOT.parent / "authorization_pilot"
DESIGN_DIR = V2_ROOT / "design"
TASK_D_ROOT = V2_ROOT.parent / "tracegrant_task_d_20261014"
for _path in (str(PILOT_ROOT), str(DESIGN_DIR), str(TASK_D_ROOT)):
    if _path not in sys.path:
        sys.path.insert(0, _path)

from seam_pilot.model import Call, Decision, MockWorld, Oracle  # noqa: E402
from seam_pilot.native import APC as NativeAPC, block_network, load_native  # noqa: E402
from case_generator import V2Case  # noqa: E402

CASES_PATH = DESIGN_DIR / "frozen_cases.json"
LOCK_PATH = DESIGN_DIR / "prediction_lock.json"

ARMS_V2 = (
    "apc_alone",
    "tracegrant_alone",
    "apc_apc_preserved",
    "apc_apc_reset",
    "apc_tracegrant_scope_only",
    "apc_tracegrant_retained",
    "apc_tracegrant_fail_closed",
)

ARM_MECHANISM = {
    "apc_alone": "APC",
    "tracegrant_alone": "TraceGrant",
    "apc_apc_preserved": "APC",
    "apc_apc_reset": "APC",
    "apc_tracegrant_scope_only": "TraceGrant",
    "apc_tracegrant_retained": "TraceGrant",
    "apc_tracegrant_fail_closed": "TraceGrant",
}

ARM_MAPPING = {
    "tracegrant_alone": "M0",
    "apc_tracegrant_scope_only": "M0",
    "apc_tracegrant_retained": "M2",
    "apc_tracegrant_fail_closed": "M1",
}


@dataclass(frozen=True)
class ScopeSnapshot:
    """What the handoff carries across the seam, in one flat record."""

    source: str
    root_resources: tuple[str, ...]
    handoff_resources: tuple[str, ...]
    actions: tuple[str, ...]
    recipient: str
    principal: str
    task: str
    budget_consumed: float
    budget_ceiling: float
    status: str
    revoked: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ScopeProxy:
    """Restrict the APC root scope's action set without touching MockWorld."""

    def __init__(self, functions: tuple[str, ...]):
        self.functions = tuple(functions)


class V2Oracle(Oracle):
    """Root-task oracle plus the v2 action-scope check.

    The base oracle checks actor, session, policy version, resource scope,
    recipient, prohibited composition and cumulative budget. v2 adds the
    downstream action allowlist (`permitted_tools`) because the v2 cases
    separate "resource in root R" from "tool in downstream A".
    """

    def __init__(self, case: V2Case):
        super().__init__(case)
        self.total_cost = float(case.pre_consumed)

    def decide(self, call: Call, args: dict[str, Any], phase: str) -> list[str]:
        reasons = super().decide(call, args, phase)
        if phase == "downstream" and call.tool not in self.case.permitted_tools:
            reasons.append("action_scope")
        return reasons


class APCV2:
    """The existing APC wrapper plus v2 observations. Upstream code untouched."""

    def __init__(self, case: V2Case):
        load_native()
        self.case = case
        self.scope_world = ScopeProxy(tuple(case.permitted_tools))
        self.native = NativeAPC(case, self.scope_world)
        if case.pre_consumed:
            from apc.budget import ActionCost
            self.native.budget.consume(ActionCost(compute_cost=case.pre_consumed))
        self.downstream = False

    def handoff(self, reset: bool = False, fresh_pdp: bool = False) -> None:
        self.native.handoff(reset=reset, fresh_pdp=fresh_pdp)
        self.downstream = True

    def authorize(self, call: Call, args: dict[str, Any]) -> Decision:
        return self.native.authorize(call, args)

    def snapshot(self) -> ScopeSnapshot:
        envelope = self.native.envelope
        scope = envelope.effective_scope
        chain = list(envelope.chain)
        return ScopeSnapshot(
            source="apc-post-handoff" if self.downstream else "apc-root",
            root_resources=tuple(sorted(str(r) for r in self.native.root_scope.resources)),
            handoff_resources=tuple(sorted(str(r) for r in scope.resources)),
            actions=tuple(sorted(str(a) for a in scope.actions)),
            recipient=self.case.recipient,
            principal=chain[-1].principal_id if chain else "",
            task=envelope.task_session_id,
            budget_consumed=float(self.native.budget.cumulative_cost),
            budget_ceiling=float(envelope.budget_spec.max_cost),
            status=self.case.status,
            revoked=bool(self.native.revocations.is_revoked(envelope.envelope_id)),
        )

    def state(self) -> dict[str, Any]:
        return {
            "budget": self.native.budget.snapshot(),
            "history": list(self.native.composition.action_history),
            "envelope_id": self.native.envelope.envelope_id,
            "downstream": self.downstream,
        }


def case_snapshot(case: V2Case) -> ScopeSnapshot:
    """Arm 2's root-scope snapshot: the frozen case itself, no APC anywhere."""
    return ScopeSnapshot(
        source="case-root",
        root_resources=tuple(sorted(case.resources)),
        handoff_resources=tuple(sorted(case.resources)),
        actions=tuple(sorted(case.permitted_tools)),
        recipient=case.recipient,
        principal=case.handoff_principal,
        task=case.handoff_task,
        budget_consumed=float(case.pre_consumed),
        budget_ceiling=float(case.cost_limit),
        status=case.status,
        revoked=case.status == "revoked",
    )


def mock_result(call: Call, args: dict[str, Any]) -> dict[str, Any]:
    """The frozen MockWorld's known return for a canonical call.

    Kept in the harness, not in MockWorld, so the mock world is not modified.
    """
    if call.tool == "read_confidential":
        return {"content": f"CONFIDENTIAL-MARKER:{args['resource']}"}
    if call.tool == "read_public":
        return {"content": f"PUBLIC-MARKER:{args['resource']}"}
    if call.tool == "save_internal":
        return {"status": "saved"}
    if call.tool == "send_external":
        return {"status": "sent"}
    raise ValueError(f"unknown mock tool {call.tool}")


def load_frozen_cases() -> tuple[list[V2Case], dict[str, Any]]:
    """Load the frozen set and verify it against the locked dataset hash."""
    import hashlib

    data = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    cases = [V2Case.from_dict(c) for c in data["cases"]]
    actual = hashlib.sha256(json.dumps([c.to_dict() for c in cases], sort_keys=True).encode("utf-8")).hexdigest()
    if actual != lock["dataset_sha256"]:
        raise RuntimeError(f"frozen case set hash mismatch: {actual} != {lock['dataset_sha256']}")
    if len(cases) != lock["case_count"]:
        raise RuntimeError("frozen case count mismatch")
    return cases, lock


def evidence_digest(payload: dict[str, Any]) -> str:
    import hashlib

    return hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def prepare() -> None:
    block_network()
    load_native()
