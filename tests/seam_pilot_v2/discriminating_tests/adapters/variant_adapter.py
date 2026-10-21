"""Variant harness for the two discriminating tests (Extension E1 continuation).

Everything in `seam_pilot_v2/discriminating_tests/` is new; no frozen file is
modified. This module contains only imports of the frozen apparatus plus the
two variants under test. It is imported (and hashed into
`discriminating_tests/design/discriminating_lock.json`) BEFORE any run.

Test 1 (scoring-only re-analysis of the frozen arm-2 records)
------------------------------------------------------------
`RootNormOracle` — the E1 reference oracle with the downstream action rule
scored against the arm's own world authority instead of the handoff-narrowed
set. Exact field names from `design/extension_e1_cases.json` (per case):
`root_tools` and `handoff_tools`.

- Handoff norm (frozen, canonical `E1Oracle.decide`): a downstream call violates
  iff a base reference rule fails OR `call.tool` is not in `case.handoff_tools`;
  reason string `handoff_action_scope`.
- Root norm (this variant): a downstream call violates iff a base reference
  rule fails OR `call.tool` is not in `case.root_tools`; reason string
  `root_action_scope`. Every other reference rule is unchanged (base
  `seam_pilot.model.Oracle.decide` reused unmodified).
- In this family `case.permitted_tools == case.root_tools` on all 8 cases; the
  runner asserts this so the two formulations coincide here.

Leak status under norm N = frozen gate allowed AND frozen effects executed AND
norm-N oracle denial. Recorded gate decisions are frozen facts and are never
re-evaluated: a scoring-only change yields zero gate-level deltas by design.

Test 2 (mini-run: an M0 synthesis variant that consumes `snapshot.actions`)
--------------------------------------------------------------------------
`ActionScopeGate` ("M0-A") — the canonical `TraceGrantGate` whose admission
rule additionally consumes the snapshot's action set before contract
synthesis. Locked consumption rule:

- R1: if `snapshot.actions` is present and non-empty and `call.tool` is NOT in
  it -> deny before contract synthesis, gate code `ACTION-SCOPE`. No contract
  is built; no effect executes.
- R2 (field absent/empty): if `snapshot.actions` is absent or empty ->
  deny before contract synthesis, gate code `ACTION-SCOPE-ABSENT`
  (fail-closed; the conservative locked option). This branch is not exercised
  by the 16 scheduled executions: every snapshot in the E1 family carries a
  non-empty action set (arm 2: `case_snapshot` -> root action set; arm 5:
  apc-post-handoff -> narrowed handoff action set).
- R3: otherwise the evaluation is byte-identical to canonical M0 — same
  synthesis call (`build_contract` with the canonical mapping label), same
  constraints, same dispatch and receipt path.

Decision-equivalence note (locked): R1 is decision-equivalent to deriving the
Contract's MAY key set from `snapshot.actions`, because the engine's H check
admits a request only if the requested tool is a key of `contract.MAY`, and
the canonical synthesis builds `MAY = {requested tool}`.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

DT_ROOT = Path(__file__).resolve().parents[1]
V2_ROOT = DT_ROOT.parent
PILOT_ROOT = V2_ROOT.parent / "authorization_pilot"
TASK_D_ROOT = V2_ROOT.parent / "tracegrant_task_d_20261014"
for _path in (str(V2_ROOT / "adapters"), str(V2_ROOT / "design"), str(PILOT_ROOT),
              str(TASK_D_ROOT), str(DT_ROOT / "adapters")):
    if _path not in sys.path:
        sys.path.insert(0, _path)

from seam_pilot.model import Call, Oracle  # noqa: E402
from v2_common import ScopeSnapshot, case_snapshot  # noqa: E402
from extension_e1 import E1Oracle  # noqa: E402
from tracegrant_adapter import GateResult, TraceGrantGate  # noqa: E402
from implementation.models import CallRequest  # noqa: E402

ROOT_NORM_REASON = "root_action_scope"
HANDOFF_NORM_REASON = "handoff_action_scope"  # frozen canonical reason string

ACTION_SCOPE_CODE = "ACTION-SCOPE"
ACTION_SCOPE_ABSENT_CODE = "ACTION-SCOPE-ABSENT"


class RootNormOracle(Oracle):
    """Test-1 scoring variant of the frozen `E1Oracle`.

    Formal norm (locked in `discriminating_tests/design/discriminating_lock.json`):
    a downstream call violates iff a base reference rule fails OR the tool is
    outside the case's root action set (`root_tools`, the authority arm 2's own
    world confers). Reason string: `root_action_scope`. Everything else is the
    base `Oracle.decide` unchanged.
    """

    def decide(self, call: Call, args: dict[str, Any], phase: str) -> list[str]:
        reasons = Oracle.decide(self, call, args, phase)
        if phase == "downstream" and call.tool not in self.case.root_tools:
            reasons.append(ROOT_NORM_REASON)
        return reasons


def score_norms(case: Any, call: Call, args: dict[str, Any], phase: str) -> dict[str, Any]:
    """Fresh-oracle decisions under both norms for one frozen (call, args, phase).

    A fresh oracle instance is used for every row, exactly mirroring the frozen
    runner, which decided each call before any effect was observed.
    """
    handoff = E1Oracle(case).decide(call, args, phase)
    root = RootNormOracle(case).decide(call, args, phase)
    return {"handoff_norm": handoff, "root_norm": root}


class ActionScopeGate(TraceGrantGate):
    """Test-2 variant gate ("M0-A").

    Canonical `TraceGrantGate` whose admission rule additionally consumes the
    snapshot's action set (rules R1-R3 in the module docstring, locked in the
    mini-lock). The variant never alters the synthesized Contract: it calls the
    canonical M0 evaluation unchanged after the action-scope admission check.
    """

    def evaluate(
        self,
        case: Any,
        snapshot: ScopeSnapshot,
        call: Call,
        args: dict[str, Any],
        mapping: str,
        verify_kind: str,
        sequence: int,
        call_cost: float,
        evidence_values: dict[str, Any] | None = None,
        now: int | None = None,
        tainted_payloads: list[str] | None = None,
    ) -> GateResult:
        if mapping != "M0":
            raise ValueError("ActionScopeGate is an M0 variant; mapping must be M0")
        request = CallRequest(tool=call.tool, arguments=args, obligation="F1")
        actions = getattr(snapshot, "actions", None)
        if actions is None or len(actions) == 0:
            # R2: field absent or empty -> fail closed (locked, not exercised here).
            return GateResult(
                admitted=False,
                code=ACTION_SCOPE_ABSENT_CODE,
                reasons=["snapshot.actions absent or empty; no action authority to check (fail-closed, locked)"],
                mapping_note="M0-A action-scope admission: snapshot.actions absent/empty (rule R2)",
                request=request,
            )
        if call.tool not in set(actions):
            # R1: the consuming admission rule.
            return GateResult(
                admitted=False,
                code=ACTION_SCOPE_CODE,
                reasons=[f"action {call.tool} not in snapshot.actions {sorted(set(actions))}"],
                mapping_note=("M0-A action-scope admission consumes snapshot.actions (rule R1); "
                              "decision-equivalent to a MAY key set restricted to snapshot.actions"),
                request=request,
            )
        # R3: byte-identical to canonical M0 (synthesis label stays "M0").
        return super().evaluate(case, snapshot, call, args, "M0", verify_kind,
                                sequence, call_cost, evidence_values,
                                now=now, tainted_payloads=tainted_payloads)
