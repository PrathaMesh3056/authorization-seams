# Findings (this implementation under our mapping)

Framing: these are observed local mock-tool results. They are statements about *this* APC
pilot, *this* independently written TraceGrant implementation, and *our* one-step
Contract mapping. They are not claims that either paper's mechanism is vulnerable.

## F1 - The scope-only handoff admits 24/40 attacks across the unrepresented dynamic fields

Arm `apc_tracegrant_scope_only` produced 24/40 attack cases with an
oracle-unauthorized effect (26 events), with no false
denials on the 40 benign cases. Oracle reason classes: {'principal_binding': 4, 'task_context': 4, 'prohibited_composition': 4, 'cumulative_budget': 10, 'expired': 4, 'revoked': 4}.
The same 24 cases leak under the root-scope mapping (`tracegrant_alone`, 24/40), so the failure is not caused by the post-handoff snapshot:
the one-step Contract simply has no representation for principal/task, prior-action
composition history, cumulative budget, expiry, revocation, or replay.

Attribution: **Contract-vocabulary/representational gap**. Counterfactual: arm
`apc_tracegrant_retained` (M2) closes all of them (0/40) by carrying
the shadow APC's decision and pre-admission budget as admitted `apc_state` evidence,
which shows the leaks are representable; it does not show a production handoff can
transport that evidence safely (the record is trusted harness input here).

## F2 - The receiving mechanism does not trust a widened resource scope: H1's resource clause does not reproduce

All seven arms deny the four `resource_widen` attacks. `Scope.meet` and
`AuthorizationEnvelope.narrow` intersect R (and A and D) with the role scope, so a role
scope containing an extra resource cannot widen the handoff scope, and M0's resource
choices are therefore already attenuated. The condition predicted these unsafe; they are
the four resource false positives in `results/condition_validation.md`.

Attribution: **condition false positive / mapping-side safety**. The action-type half of
the same concern (a tool in root A but not handoff A) is untested because the frozen set
contains no such case - this is the main coverage gap and the first candidate for the
next extension.

## F3 - VERIFY is an admission/completion boundary, not an admission-time leak

The four `unsatisfiable_verify` attacks are admitted by `check_call` (which does not
evaluate VERIFY) and fail at `check_receipt` in every TraceGrant arm; the mock effect has
already executed by then. No oracle-unauthorized effect occurs. The satisfiable benign
counterparts complete with receipts OK in every TraceGrant arm.

Attribution: **mechanism behavior at a defined boundary**, matching the paper's Algorithm 1
line 14 and this implementation's `check_receipt`. Whether executing before receipt is a
safety problem depends on the deployment's tolerance for a rolled-back or compensated
effect; the experiment does not measure that. The condition should score C1c separately
from unauthorized-effect safety.

## F4 - Argument canonicalization plus scope-derived constraints catch recipient confusion

All seven arms deny `recipient_substitution` and `omitted_forbidden_default` (8 cases,
0 leaks). M0 canonicalizes the omitted Python-signature default and derives the recipient
BIND constraint from the allowlist, so the forbidden default is rejected at `establish`
(constant outside scope) or at `check_call` (MAY constraint).

Attribution: **mapping-side catch**, not a TraceGrant property: a mapping that trusts the
raw call without canonicalization or without a BIND constraint would not catch these.

## F5 - The fail-closed mapping is safe but not selective

Arm `apc_tracegrant_fail_closed` produced 0/40 leaks and
20/40 benign false denials. It denies every untranslatable
exercise rather than trying to carry it, including the five benign stateful/freshness
families. It is a conservative control, not a selective preservation algorithm.

## F6 - The same-mechanism reset control replicates the v1 leak

Arm `apc_apc_reset` leaks 8/40 attacks ({'prohibited_composition': 4, 'cumulative_budget': 4}), including
the four composition-history attacks and two of the four pre-consumed-budget attacks,
reproducing the v1 `apc_apc_reset` behavior on the v2 matrix. This is a deliberate control,
not a new finding.

## Threats to validity

- The mock tools are synthetic; the `MockWorld` returns are fixed strings.
- The mapping M0/M1/M2 and the condition are our constructions, not paper specifications.
- M2's evidence is trusted harness input; no authenticated evidence transport is tested.
- The oracle is our own; only two oracle rules have mutation failure controls.
- Four parameter sets, one TraceGrant implementation, one APC commit, no concurrency.
- The action-type clause of C1a is untested (no frozen case for root-A-minus-handoff-A).
- Latency excludes execution, receipts, IPC and initialization.

