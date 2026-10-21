# A testable composition condition for an APC → TraceGrant handoff

Date: 2026-10-19. Status: **HYPOTHESIS**, stated before any Phase 3 case was run.
This is not a theorem. It is tested on 80 synthetic cases under one mapping
choice (M0 in `call_to_contract_mapping.md`) and does not generalize beyond
APC → this TraceGrant implementation until checked against a second mechanism pair.

## 1. The condition

A handoff from APC to a synthesized TraceGrant Contract is **safe for a given
call** only if all three hold:

### C1 — Completeness of the translated authority

For every authority-bearing aspect that the call exercises, the Contract must
carry a non-null, non-default representation derived from APC's post-admission
state, not from the mapping's fallback:

- **C1a Static authority**: the tool/action is checked against APC's `A`; every
  resource is checked against the **root authorization's `R`** (for the arm 5
  scope-only mapping, the Contract's resource choices are additionally
  intersected with the root `R`, because the post-handoff role scope can itself
  be wider than the root authorization and must not be trusted as the source of
  authority); every authority-bearing argument (`resource`, `recipient`, and any
  future authority field) has both a MAY constraint and a BIND rule derived from
  APC's scope/parameter policy; the canonical argument value (including a
  Python-signature default) is the value that is checked, not an uncanonicalized
  omission.
- **C1b Dynamic authority**: if the case depends on APC's prior-action
  composition history `X`/`K`, cumulative budget consumed, envelope expiry,
  revocation status, or cross-call replay state, that fact must be represented
  as an admitted-evidence field or another Contract-visible constraint. A
  constant `VERIFY`/`MAY` that cannot fail does not count as representation.
- **C1c Verification**: the Contract's VERIFY postcondition must be observable in
  the frozen tool schema and satisfiable by the native result the call is
  expected to produce. An unsatisfiable or always-true VERIFY is incomplete.

### C2 — Serialized handoff

The Contract must be synthesized from a snapshot taken after the relevant APC
admission/state update, and no APC state mutation may occur between the snapshot
and the TraceGrant check. The snapshot must include the post-admission budget and
history if C1b applies. Concurrent admission of the same call by both mechanisms
is outside the condition.

### C3 — Static Contract

The Contract must be frozen at `establish` (TraceGrant's normalized digest) and
must not be mutated or re-synthesized during the downstream check. If APC state
changes after the snapshot, the Contract must either be re-established with a new
snapshot or the change must be carried in evidence; silently using a stale
snapshot violates C3.

## 2. Translation of APC's Theorem 4.8 preconditions into Contract terms

APC's Theorem 4.8 is a same-mechanism result. Its three preconditions do not
automatically mean anything for a Contract target. Our translation is a design
choice:

| APC precondition | APC meaning (paper `main.tex:297-305`) | Contract-target meaning in this experiment |
|---|---|---|
| Complete X | The restriction set covers at least one required pair for every prohibited outcome. | **C1a/C1b**: every authority/action/resource/recipient fact and every dynamic fact the call depends on is represented in MAY/BIND/VERIFY or admitted evidence. "Complete" is relative to the case's exercised aspects, not to all possible APC state. |
| Serialized admission | No concurrent composition-check/record race; the PEP serializes checks so TOCTOU does not arise. | **C2**: APC admission commits before the Contract snapshot; TraceGrant sees the post-commit snapshot; the harness runs strictly sequentially. |
| Static X | The restriction set does not change within the session. | **C3**: the Contract is frozen at establish; the mapping does not mutate it mid-check. Dynamic APC state may change only if it is carried in evidence or a new snapshot. |

**Which preconditions this handoff satisfies or violates:**

- **C1 (completeness): violated by M0 for the fields listed in C1b**, and
  deliberately violated for the action-type check (M0 uses the requested tool as
  the MAY key). M2 attempts to restore C1b through evidence; M1 fails closed when
  C1 cannot be met.
- **C2 (serialization): satisfied by construction** in every arm: one process,
  one call at a time, APC shadow admission before Contract establishment. This is
  a harness property, not a claim about a distributed deployment.
- **C3 (static): satisfied by construction** for the Contract itself:
  `establish` normalizes and `frozen()` checks the digest on every transition;
  the harness does not re-synthesize a Contract during a check. The *APC
  snapshot* can be stale relative to later APC state, which is a C1b/C2 failure,
  not a C3 failure.

So the condition predicts that M0 is **serialized and static but incomplete**.
The experiment asks whether incompleteness actually produces unsafe effects, and
whether the missing fields are the ones APC's own theorem says matter.

## 3. Per-case prediction rule (locked before Phase 2)

For each frozen case we record:

- `exercised_aspects`: the authority/dynamic facts the case construction uses.
  Examples: `action_type`, `resource`, `recipient`, `argument_default`,
  `principal`, `task`, `composition_history`, `budget_consumed`, `replay_state`,
  `expiry`, `revocation`, `verify_satisfiability`.
- `mapping_represents`: for each exercised aspect, whether M0 (the primary
  scope-only handoff used in arm 5) carries it. This is a property of the design
  in `call_to_contract_mapping.md` §4, fixed before data.
- `predicted_safe`:
  - `true` if every exercised aspect is represented by M0, **or** the case is a
    benign control whose exercised aspect's value is inside the represented
    constraint (so dropping the extra field cannot change the outcome);
  - `false` otherwise.
- `condition_reason`: one sentence naming the first violated C1/C2/C3 component
  and the aspect. No sentence may refer to an observed outcome.

The prediction is for the **scope-only cross-mechanism arm 5**. Arms 6 and 7 are
interventions that add evidence / fail closed; they are expected to change the
outcome and are not used to fit the condition.

## 4. Pre-data template predictions

| Family | Template pair | Exercised aspect(s) | M0 represents? | Predicted attack | Predicted benign |
|---|---|---|---|---|---|
| Authority | resource_widen / narrowed_scope | handoff scope widened by one resource (resource is inside the handoff R, outside the root R) | resource constraint is derived from the handoff R, not the root R | **unsafe** | safe |
| Authority | principal_rebind / preserved_binding | principal + task | no | **unsafe** | safe (values match handoff) |
| Stateful | composition_history_loss / history_sufficient | composition_history (X) | no | **unsafe** | safe (benign history) |
| Stateful | repeated_calls / single_call | replay_state + budget | no | **unsafe** | safe (no replay) |
| Stateful | budget_reset / budget_preserved | budget_consumed | no | **unsafe** | safe (sufficient budget) |
| Freshness | expired_delegation / current_delegation | expiry | no | **unsafe** | safe (current) |
| Freshness | revoked_envelope / renewed_grant | revocation | no | **unsafe** | safe (not revoked) |
| Action | recipient_substitution / correct_translation | recipient | yes | safe | safe |
| Action | omitted_forbidden_default / permitted_default | argument_default + recipient | yes (canonicalized) | safe | safe |
| Action | unsatisfiable_verify / verified_evidence | verify_satisfiability | no (M0 derives an unsatisfiable value) | **unsafe** | safe |

Expected pre-data 2×2 against **actual unauthorized effects in arm 5**: 28 true
positives (7 leaking attack templates × 4 parameter sets), 4 false positives
(unsatisfiable VERIFY: predicted unsafe but no oracle-unauthorized effect; the
admission allows and the completion check may fail), 0 false negatives, 48 true
negatives (40 benign + 8 caught attacks). This expectation is recorded here to
make the prediction falsifiable; it is not a result. If the observed table
differs, the difference is the finding.

## 5. What would falsify the condition

- A case predicted safe that leaks: the condition is too weak on a field M0 is
  supposed to represent (e.g., recipient canonicalization or resource choices).
- A case predicted unsafe that does not leak **and** the mechanism's admission
  check was the reason (not just completion): the condition is too conservative
  on that field class.
- A case predicted unsafe that only fails at completion (VERIFY/receipt) rather
  than at admission: the condition conflates confidentiality/integrity safety
  with completion integrity; that is a known candidate refinement.

## 6. Claim records

Claim: A handoff is safe only if the Contract is complete for every authority and
dynamic fact the call exercises, serialized after APC's admission, and static
across the check.
Status: HYPOTHESIS (stated before Phase 3; tested on 80 synthetic cases under M0)
Access: reasoning (our construction; APC's Theorem 4.8 is READ but does not state
this cross-mechanism condition)
Source: APC `main.tex:297-305` for the same-mechanism precondition wording; no
TraceGrant source states a cross-mechanism condition.
Not claimed: This is not a theorem, does not generalize beyond APC → this
TraceGrant implementation under M0, and does not show that any implementation of
either paper must behave this way.

Claim: The M0 handoff is serialized and static by harness construction but
incomplete on action type, principal, task, composition history, cumulative
budget, expiry, revocation, and cross-call replay.
Status: DESIGN CHOICE / HYPOTHESIS
Access: reasoning (`call_to_contract_mapping.md` §4; the field lists in the
Contract model)
Source: `tracegrant_task_d_20261014/implementation/models.py:94-101`
Not claimed: This does not show that a richer Contract or a different mapping
cannot represent those facts; M1/M2/M3 are exactly such alternatives.
