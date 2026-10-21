# Condition validation: locked predictions vs observed arm-5 effects

The prediction rule is in `design/composition_condition.md` section 3 and was locked in
`design/prediction_lock.json` (`dataset_sha256 = 0fe1eafb0552549370415711a3aa08993715160d4ce391f10cfd59c988605ad2`) before Phase 2/3.
`predicted_safe` describes the arm-5 scope-only handoff (`apc_tracegrant_scope_only`).

## 2x2 against observed unauthorized effects (arm 5)

| | Observed leak | Observed no leak |
|---|---:|---:|
| Predicted unsafe | 24 (TP) | 8 (FP) |
| Predicted safe | 0 (FN) | 48 (TN) |

- Precision: 0.750 (lock expected 0.875)
- Recall: 1.000 (lock expected 1.0)
- Locked expectation: TP=28, FP=4, FN=0, TN=48

## Per-hypothesis

| Hypothesis | Cases | TP | FP | FN | TN |
|---|---:|---:|---:|---:|---:|
| H1 | 16 | 4 | 4 | 0 | 8 |
| H2 | 40 | 20 | 0 | 0 | 20 |
| H3 | 8 | 0 | 4 | 0 | 4 |
| H4 | 16 | 0 | 0 | 0 | 16 |

## False positives (predicted unsafe, no unauthorized effect)

- `resource_widen-0-a` (resource_widen): predicted unsafe by H1; observed gate denied the call.
- `resource_widen-1-a` (resource_widen): predicted unsafe by H1; observed gate denied the call.
- `resource_widen-2-a` (resource_widen): predicted unsafe by H1; observed gate denied the call.
- `resource_widen-3-a` (resource_widen): predicted unsafe by H1; observed gate denied the call.
- `unsatisfiable_verify-0-a` (unsatisfiable_verify): predicted unsafe by H3; observed receipt failed (completion boundary).
- `unsatisfiable_verify-1-a` (unsatisfiable_verify): predicted unsafe by H3; observed receipt failed (completion boundary).
- `unsatisfiable_verify-2-a` (unsatisfiable_verify): predicted unsafe by H3; observed receipt failed (completion boundary).
- `unsatisfiable_verify-3-a` (unsatisfiable_verify): predicted unsafe by H3; observed receipt failed (completion boundary).

## Interpretation of the two falsified clauses

1. **C1a resource clause too conservative.** The four `resource_widen` cases were predicted
   unsafe because the mapping was assumed to inherit a role scope wider than the root R.
   `AuthorizationEnvelope.narrow` performs the scope meet, so the handoff R cannot widen;
   both M0 and the root-scope mapping deny the widened resource. The condition's resource
   clause should read: *the handoff scope is safe against widening if `narrow` meets R;
   the mapping must still not use a non-attenuated scope if one is supplied.*
2. **C1c conflates completion with effect safety.** The four `unsatisfiable_verify` cases
   admit at `check_call` by algorithm design and fail at `check_receipt`; no oracle-
   unauthorized effect occurs. C1c should be scored as a separate completion-integrity
   predicate, not folded into the safety label.

The untested C1a action-type clause remains a coverage gap: no frozen case exercises a
tool in root A but outside handoff A.

