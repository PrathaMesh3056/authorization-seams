# Claims update (H1-H4, H6) after the 80x7 matrix

Each block states the hypothesis as operationalized in this experiment, the locked
prediction, the observed result, and the revised status. Statuses are SELF-REPORTED
observations about this implementation under this mapping.

## H1 - The receiving mechanism re-derives scope or trusts the already-authorized caller

Operationalization: the scope-only handoff uses the attempted tool as the MAY key and
derives resource choices from the handoff scope; attacks widen the action or resource.

Observed: **not supported for resources** - all seven arms deny the four `resource_widen`
cases (`narrow` meets R). **Untested for action type** - no frozen case uses a tool in
root A but outside handoff A. The 'trusts the caller' concern is supported only in the
weaker sense of F1: fields the Contract cannot represent are not re-derived at all.

Status: **WEAKENED / PARTIALLY UNTESTED.** Next experiment: add a handoff whose role A is
a strict subset of root A and attempt the missing tool.

## H2 - Dynamic state, identity and freshness are not carried across the seam and leak

Operationalization: principal/task rebinding, composition history, cumulative budget,
expiry, revocation, replay; each with a paired benign case.

Observed: **supported**. Arm 5 leaks 24/40 attacks with
0 false denials; the leaking classes are principal/task (4),
composition history (4, with marker-bearing external effects), cumulative budget/replay
(8), expiry (4), revocation (4). Arm 6 (M2 evidence) leaks 0/40, showing they are representable as evidence.

Status: **SUPPORTED within this mapping**; the fix is evidence carriage (with a trust
boundary), not a TraceGrant check.

## H3 - VERIFY postconditions are an admission/completion boundary

Observed: **supported**. The four unsatisfiable-VERIFY cases admit and fail the receipt
in every TraceGrant arm; zero unauthorized effects. Benign counterparts complete.

Status: **SUPPORTED**, with the clarification that this is a completion-integrity
boundary, not an unauthorized-effect leak. The condition should score C1c separately.

## H4 - Mapping choices decide whether a failure is a mechanism property or an artifact

Observed: **supported**. Recipient/default attacks are caught by mapping-side
canonicalization and BIND constraints (0 leaks); the resource-widen prediction is
falsified by APC's scope meet; the state/identity/freshness leaks persist under both the
root-scope and handoff-scope mappings and are therefore Contract-vocabulary gaps; the
unsatisfiable-VERIFY class is a boundary artifact of the condition, not a leak.

Status: **SUPPORTED with refinements**; see `results/condition_validation.md`.

## H6 - Comparison with the Progent reference numbers

Reference: the Task B verification pilot recorded 4/20 unauthorized effects for the raw
MCP default-argument path across 8 functions (and 4/8 prompt frames as default leaks),
with different tools, cases, denominators and a static JSON-schema profile.

Observed here: M0 leaks 24/40 attack cases; M2 0/40;
fail-closed 0/40 with 20/40 benign denials.
The denominators and mechanisms differ, so the numbers are not directly comparable. The
directional result is that a scope-only cross-mechanism handoff leaks on unrepresented
dynamic/identity fields, and that carrying the upstream decision as evidence closes the
measured gap under trusted transport.

Status: **DIRECTIONAL ONLY; no comparable claim.**

