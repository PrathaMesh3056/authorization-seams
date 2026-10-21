# Disagreements between the root-task oracle and the mechanism gates

An *unauthorized effect* is an event where the mechanism allowed a call the oracle
denied and the mock tool executed. A *false denial* is an event where the mechanism
denied a call the oracle allowed. Receipt failures without an unauthorized effect are
listed separately as completion-integrity events, not leaks.

## Per-arm summary

| Arm | Unauthorized effect events | Cases with a leak / 40 attacks | False denial events | Cases with a false denial / 40 benign | Receipt failures |
|---|---:|---:|---:|---:|---:|
| apc_alone | 0 | 0 | 0 | 0 | 0 |
| tracegrant_alone | 26 | 24 | 0 | 0 | 4 |
| apc_apc_preserved | 0 | 0 | 0 | 0 | 0 |
| apc_apc_reset | 8 | 8 | 0 | 0 | 0 |
| apc_tracegrant_scope_only | 26 | 24 | 0 | 0 | 4 |
| apc_tracegrant_retained | 0 | 0 | 0 | 0 | 4 |
| apc_tracegrant_fail_closed | 0 | 0 | 28 | 20 | 0 |

## Attribution of every disagreement

| Arm | Attribution | Events | Cases |
|---|---|---:|---|
| apc_apc_reset | deliberate_state_reset_control | 8 | 8: budget_reset-1-a, budget_reset-2-a, composition_history_loss-0-a, composition_history_loss-1-a, composition_history_loss-2-a, composition_history_loss-3-a ... |
| apc_tracegrant_fail_closed | conservative_fail_closed_control | 28 | 26: budget_preserved-0-b, budget_preserved-1-b, budget_preserved-2-b, budget_preserved-3-b, current_delegation-0-b, current_delegation-1-b ... |
| apc_tracegrant_scope_only | cross_mechanism_gap: cumulative budget/replay not carried by M0 | 10 | 8: budget_reset-0-a, budget_reset-1-a, budget_reset-2-a, budget_reset-3-a, repeated_calls-0-a, repeated_calls-1-a ... |
| apc_tracegrant_scope_only | cross_mechanism_gap: freshness/revocation not carried by M0 | 8 | 8: expired_delegation-0-a, expired_delegation-1-a, expired_delegation-2-a, expired_delegation-3-a, revoked_envelope-0-a, revoked_envelope-1-a ... |
| apc_tracegrant_scope_only | cross_mechanism_gap: principal/task not carried by M0 | 4 | 4: principal_rebind-0-a, principal_rebind-1-a, principal_rebind-2-a, principal_rebind-3-a |
| apc_tracegrant_scope_only | cross_mechanism_gap: prior-action composition history not carried by M0 | 4 | 4: composition_history_loss-0-a, composition_history_loss-1-a, composition_history_loss-2-a, composition_history_loss-3-a |
| tracegrant_alone | cross_mechanism_gap: cumulative budget/replay not carried by M0 | 10 | 8: budget_reset-0-a, budget_reset-1-a, budget_reset-2-a, budget_reset-3-a, repeated_calls-0-a, repeated_calls-1-a ... |
| tracegrant_alone | cross_mechanism_gap: freshness/revocation not carried by M0 | 8 | 8: expired_delegation-0-a, expired_delegation-1-a, expired_delegation-2-a, expired_delegation-3-a, revoked_envelope-0-a, revoked_envelope-1-a ... |
| tracegrant_alone | cross_mechanism_gap: principal/task not carried by M0 | 4 | 4: principal_rebind-0-a, principal_rebind-1-a, principal_rebind-2-a, principal_rebind-3-a |
| tracegrant_alone | cross_mechanism_gap: prior-action composition history not carried by M0 | 4 | 4: composition_history_loss-0-a, composition_history_loss-1-a, composition_history_loss-2-a, composition_history_loss-3-a |

Classification rule: a failure is a **mapping artifact** if a reasonable alternative
mapping using TraceGrant's Contract vocabulary removes it, and a **Contract-vocabulary**
gap if it persists because the Contract model has no field for the exercised fact.
Receipt failures are not classified as leaks; they are the admission/completion boundary.

## Phase 5.5 adversarial self-review of the top three distinct findings

### Review 1 - cross-mechanism leaks in the scope-only arm (M0)

Evidence: the same 24 cases leak under both M0 mappings (`apc_tracegrant_scope_only` 26 events, `tracegrant_alone` 26 events; the
`repeated_calls` family contributes two denied events in the consumed=0 parameters).
Oracle reasons are in the unrepresented dynamic/identity set (principal/task,
composition history, cumulative budget, expiry, revocation). Counterfactual tests:

- **M2 evidence (arm `apc_tracegrant_retained`)**: zero unauthorized effects on the same
  80 cases. The leaks are therefore *representable* in TraceGrant as admitted evidence;
  they are not a hard impossibility result. M2's evidence is trusted harness input
  (`results/diagnostics.json` and `design/call_to_contract_mapping.md` section 6).
- **Root-scope mapping (arm `tracegrant_alone`)**: the same 24 attack cases leak. The
  failure is not caused by using the post-handoff scope; it is the absence of the dynamic
  fields in the Contract.
- **Payload provenance (Phase 5.5 diagnostic)**: supplying `tainted_payloads=["body"]`
  does not close the composition leak, because TraceGrant's H check is a content
  heuristic (script/eval/secret regex), and `CONFIDENTIAL-MARKER:` does not match it.

Verdict: survives as a **Contract-vocabulary/representational gap**, closed only by
carrying upstream state as evidence (M2) or by a richer Contract; it is not shown to be
a TraceGrant algorithmic defect.

### Review 2 - unsatisfiable VERIFY is a completion failure, not a leak

The four unsatisfiable-VERIFY attack cases are admitted by `check_call` and fail at
`check_receipt` (locked expectation already flagged this as the expected false-positive
class). Counterfactual: the satisfiable benign counterparts complete with receipts OK in
every TraceGrant arm. Verdict: the condition conflates completion integrity with
unauthorized effect; refine C1c to score completion separately. It remains a real
admission/completion boundary, not a confidentiality or integrity leak in this matrix.

### Review 3 - resource-widen predicted unsafe but did not leak

`Scope.meet`/`AuthorizationEnvelope.narrow` intersects R with the role scope, so a role
scope containing an extra resource cannot widen the handoff R. Both the root-scope and
handoff-scope mappings therefore deny it. Verdict: the C1a resource clause was too
conservative for this implementation; no mechanism failure. The action-type half of C1a
is untested by the frozen set (no case exercises a tool in root A but outside handoff A).

