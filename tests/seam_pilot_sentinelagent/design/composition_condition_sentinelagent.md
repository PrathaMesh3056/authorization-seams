# A testable composition condition for an APC → SentinelAgent handoff

Date: 2026-10-19. Status: **HYPOTHESIS**, stated before any case was run.
This is not a theorem. It is tested on 96 synthetic cases (the frozen 80-case set from
`seam_pilot_v2`, read-only, plus 16 new signature-family cases) under one mapping
choice (T0 in `call_to_token_mapping.md`) and does not generalize beyond
APC → this SentinelAgent prototype until checked further.

## 1. The condition

A handoff from APC to a synthesized SentinelAgent delegation token is **safe for a
given call** only if all three hold:

### C1 — Completeness of the translated authority

For every authority-bearing aspect that the call exercises, the token (or the token
plus a signature-verified attestation carried through the token primitive) must carry
a non-null, non-default representation derived from APC's post-admission state, not
from the mapping's fallback, and that representation must be **checked**:

- **C1a Static authority**: the tool/action is checked against APC's `A`; every
  resource is checked against the **root authorization's `R`** (for the arm 5
  scope-only mapping, the manifest's resource choices are additionally intersected
  with the root `R`, because the post-handoff role scope can itself be wider than the
  root authorization and must not be trusted as the source of authority); the
  recipient is checked against APC's allowlist; the canonical argument value
  (including a Python-signature default) is the value that is checked.
- **C1b Dynamic authority**: if the case depends on APC's prior-action composition
  history `X`, cumulative budget consumed, envelope expiry, revocation status, or
  cross-call replay state, that fact must be a checked field of the token or of a
  signature-verified carrier. A field that the check never consults (e.g. `expiry` in
  this prototype) does not count as representation.
- **C1c Attestation integrity**: any carried decision record must be verified with the
  receiving mechanism's own signature primitive before it can affect the outcome.

### C2 — Serialized handoff

The token must be synthesized from a snapshot taken after the relevant APC
admission/state update, and no APC state mutation may occur between the snapshot and
the receiving check. Concurrent admission of the same call by both mechanisms is
outside the condition.

### C3 — Static token

The token must be constructed once per call and must not be mutated or re-signed
during the downstream check. If APC state changes after the snapshot, the token must
either be re-minted from a new snapshot or the change must be carried in the
attestation; silently using a stale snapshot violates C3.

## 2. Translation of APC's Theorem 4.8 preconditions into token terms

APC's Theorem 4.8 is a same-mechanism result. Its three preconditions do not
automatically mean anything for a token receiver. Our translation is a design choice:

| APC precondition | APC meaning (paper `main.tex:297-305`) | Token-target meaning in this experiment |
|---|---|---|
| Complete X | The restriction set covers at least one required pair for every prohibited outcome. | **C1a/C1b**: every authority/action/resource/recipient fact and every dynamic fact the call depends on is represented in a **checked** token/attestation field. "Complete" is relative to the case's exercised aspects. |
| Serialized admission | No concurrent composition-check/record race. | **C2**: APC admission commits before the token snapshot; the receiver sees the post-commit snapshot; the harness runs strictly sequentially. |
| Static X | The restriction set does not change within the session. | **C3**: the token is constructed once per call, never re-signed mid-check; dynamic APC state may change only if carried in the attestation or a new snapshot. |

**Which preconditions this handoff satisfies or violates:**

- **C1 (completeness): violated by T0** for the fields in C1b, and deliberately for
  the action-type check (T0 uses the attempted tool as the scope element, unchecked).
  T2-attest attempts to restore C1b through a signed carrier; T1 fails closed when C1
  cannot be met.
- **C2 (serialization): satisfied by construction** in every arm: one process, one
  call at a time, shadow APC admission before token synthesis. This is a harness
  property, not a claim about a distributed deployment.
- **C3 (static): satisfied by construction**: one token per call, signed once by the
  prototype's own `_sign()`; the harness never re-signs during a check. The *APC
  snapshot* can be stale relative to later APC state, which is a C1b/C2 failure, not a
  C3 failure.

So the condition predicts that T0 is **serialized and static but incomplete**. The
experiment asks whether incompleteness actually produces unsafe effects, and whether
the missing fields are the ones APC's own theorem says matter.

## 3. Per-case prediction rule (locked before the run)

For each case we record:

- `exercised_aspects`: the authority/dynamic facts the case construction uses.
- `mapping_represents`: for each exercised aspect, whether T0 (the primary scope-only
  handoff used in arm 5) carries it **as a checked representation**. This is a property
  of the design in `call_to_token_mapping.md` §4, fixed before data.
- `predicted_safe`:
  - `true` if every exercised aspect is represented by T0;
  - `true` if the case is a benign control whose exercised aspect's value is inside the
    represented constraint (so dropping the extra field cannot change the outcome);
  - `true` if the exercised aspect is a mapping-created obligation with no authority
    content under the token model (the unsatisfiable-VERIFY family: the VERIFY
    postcondition was created by the other pair's mapping vocabulary; T0 fabricates no
    obligation, so there is nothing to fail);
  - `false` otherwise.
- `condition_reason`: one sentence naming the first violated C1/C2/C3 component and
  the aspect. No sentence may refer to an observed outcome.

The prediction is for the **scope-only cross-mechanism arm 5**. Arms 6 and 7 are
interventions that add a signed carrier / fail closed; they are expected to change
the outcome and are not used to fit the condition. Arm 2 (the standalone token arm)
repeats T0 on the frozen root scope; the condition also predicts its outcome, and the
seam test asks whether any case is safe in arms 1 and 2 but unsafe in 5/6/7.

## 4. Pre-data template predictions

| Family | Template pair | Exercised aspect(s) | T0 represents? | Predicted attack | Predicted benign |
|---|---|---|---|---|---|
| Authority | resource_widen / narrowed_scope | resource | yes - manifest from the post-handoff effective R (root R ∩ role R by APC's meet) | safe | safe |
| Authority | principal_rebind / preserved_binding | principal + task | no - `src` is carried but never compared | **unsafe** | safe (values match handoff) |
| Stateful | composition_history_loss / history_sufficient | composition_history (X) | no - no checked field | **unsafe** | safe (benign history) |
| Stateful | repeated_calls / single_call | replay_state + budget | no | **unsafe** | safe (no replay) |
| Stateful | budget_reset / budget_preserved | budget_consumed | no | **unsafe** | safe (sufficient budget) |
| Freshness | expired_delegation / current_delegation | expiry | no - `expiry` is a field but P6/P7 never consult it | **unsafe** | safe (current) |
| Freshness | revoked_envelope / renewed_grant | revocation | no - `revoked` stays False; not signed; never set from APC state | **unsafe** | safe (not revoked) |
| Action | recipient_substitution / correct_translation | recipient | yes - manifest SEND allowlist from the snapshot | safe | safe |
| Action | omitted_forbidden_default / permitted_default | argument_default + recipient | yes (canonicalized) | safe | safe |
| Action | unsatisfiable_verify / verified_evidence | verify_satisfiability | not applicable - the token check has no completion/postcondition stage; the frozen call is an ordinary oracle-authorized call under this pair | safe | safe |
| Signature (new) | foreign_key_signed / trusted_key_signed | signer_key | yes - the signature check binds to key material; a different key fails before P6/P7 | safe | safe |
| Signature (new) | keyholder_widen / keyholder_plain | mint_provenance | no - a symmetric HMAC has no signer identity; any holder of the trusted key is equivalent to the issuer (H5) | **unsafe** | safe |

Expected pre-data 2x2 against **actual unauthorized effects in arm 5**: 28 true
positives (7 leaking attack templates × 4 parameter sets), 0 false positives, 0 false
negatives, 68 true negatives (48 benign + 20 caught attacks). This expectation is
recorded here to make the prediction falsifiable; it is not a result. If the observed
table differs, the difference is the finding.

Two attack templates are re-predicted relative to the frozen TraceGrant-pair lock for
the same frozen cases — `resource_widen` (frozen: unsafe; SA: safe, because T0's
manifest is APC's post-handoff effective scope, which the mechanism's own meet narrows
to root R ∩ role R) and `unsatisfiable_verify` (frozen: unsafe; SA: safe, because no
VERIFY obligation is fabricated under this pair). `design/sa_lock.json` records each
overridden case with both predictions and the mechanism reason.

## 5. The freshness prediction (stronger than the TraceGrant pair's)

Task C established (READ) that P6/P7 check revocation and signatures but do **not**
check expiry, and that a legitimately signed expired token passed both checks in an
exploratory probe. This run tests it inside the seam:

- Locked statement: a synthesized token whose `expiry` lies in the past **still passes
  P6 and P7**, because neither check consults the field and the signature covers it
  while remaining valid.
- Which arm adds its own expiry check: **none at the token layer**. Every arm presents
  the same T0 token with the carried `expiry` value and never inspects it. The arms
  that nevertheless deny the expired cases do so at other layers, locked here:
  - arms 1/3/4: APC itself denies the expired envelope (same-mechanism layers);
  - arm 6: the signed attestation requires `freshness ∈ {current, renewed}` (a
    carried-field requirement, not a token-expiry check);
  - arm 7: refuses cases that exercise expiry as untranslatable dynamic state.
  - arms 2 and 5 are the arms under test: predicted to admit the expired attack.
- A dedicated control (S1, §7) presents an expired, validly signed token directly to
  the native P6/P7 with a signature-broken failure control and a revoked-token probe.

## 6. The signature-family prediction (first end-to-end H5 test)

H5 (`Paper_Claims_and_Takeaways.md:42`): "SentinelAgent tokens are HMAC-signed, so
another mechanism cannot verify them without the key or a call to the DAS." This run
operationalizes both directions:

1. **Key material is bound**: a token signed with a key the receiver does not hold
   (the prototype's published key, or any other) fails `verify_signature()` inside
   P6/P7 with `SIGNATURE_INVALID`, in every arm that runs the check. The receiver
   "notices" a different **key**.
2. **Signer identity does not exist**: a token minted by any other key holder - the
   delegate itself - under the receiver's configured key is indistinguishable from a
   bridge-minted token; the check answers "valid under my key?", not "who signed?".
   Predicted consequence: an escalated manifest written by the delegate is admitted in
   the scope-only arms (2 and 5) exactly as if the bridge had written it.

Locked predictions: `foreign_key_signed` attack is safe everywhere (rejected at the
signature check, arms 2/5/6/7); `keyholder_widen` attack leaks in arms 2 and 5 (the
scope-only mappings accept the caller-written manifest), and is denied in 6 (the
attestation carries the shadow APC denial) and 7 (shadow denial / untranslatable
resource).

## 7. Reference oracle and scoring rules for this run (locked)

The authority-level reference oracle is `V2Oracle` unchanged (actor, session, policy
version, resource scope, recipient, prohibited composition, cumulative budget,
downstream action list). Three additions are locked before the run:

- `unauthorized_effect` (per event) = (oracle reasons non-empty AND an effect ran) OR
  (the call was admitted AND a token was presented AND that token's signature did not
  verify under the trusted key). The second clause encodes the receiving mechanism's
  own advertised contract: an effect admitted under an unverifiable token is
  unauthorized.
- `false_denial` (per event) = oracle reasons empty AND the call was denied AND NOT
  (a token was presented and its signature did not verify). Correctly rejecting an
  unverifiable token is required behavior, not a false denial. Denials with no token
  presented (T1 refusals, shadow denials) count as false denials when the oracle was
  clean, as in the TraceGrant run.
- `attack_success` (per case) = any unauthorized_effect event; `benign_false_denial`
  (per case) = any false_denial event.

Locked control expectations (own denominators; each a Check with a failure control):

| Control | Setup | Expected |
|---|---|---|
| S1-valid | expired, validly signed T0 token for an allowed call | P6 `ALLOWED by scope:...`, P7 `OUTPUT_ALLOWED` |
| S1-failure | same token content, manifest mutated after signing | P6/P7 `SIGNATURE_INVALID` |
| S1-probe | same token, revoked via `revoke_chain` | P6/P7 `TOKEN_REVOKED` |
| S2-foreign | T0 content signed with `REAL_DAS_KEY` | P6/P7 `SIGNATURE_INVALID` |
| S2-trusted (failure control) | identical content signed with `BRIDGE_KEY` | P6 `ALLOWED`, P7 `OUTPUT_ALLOWED` |
| S2-two-minters | identical content, "bridge-minted" vs "delegate-minted" under the trusted key | both P6 `ALLOWED` with identical code strings; P7 identical |
| S2-mutated (failure control) | delegate-minted token, manifest widened after signing | `SIGNATURE_INVALID` (content binding holds) |
| S3-valid | signed attestation for a benign call | admitted; probe: signature field tampered -> `ATTESTATION-SIGNATURE-INVALID` |
| S3-mutated | `apc_allowed` flipped after signing | `ATTESTATION-SIGNATURE-INVALID`; probe: unmutated and denied by shadow -> `APC-DENY` |
| S3-replay | valid attestation bound to a different call | `ATTESTATION-BINDING-MISMATCH`; probe: original call -> admitted |

## 8. Expected per-arm table (locked before the run)

| Arm | Leak cases (expected) | Leak events (expected) | Benign FD cases (expected) | Notes |
|---|---:|---:|---:|---|
| 1 apc_alone | 0 | 0 | 0 | all oracle-unauthorized attacks are APC-denied; benign all admitted |
| 2 sentinelagent_alone | 28 | 30 | 0 | the 7 leaking templates x 4; events include the two-call replay cases |
| 3 apc_apc_preserved | 0 | 0 | 0 | preserved budget/composition deny all attacks |
| 4 apc_apc_reset | 8 | 8 | 0 | reset control: composition 4, repeated 2, budget 2 (identical to the frozen run's arm 4 on the shared 80; new cases contribute 0) |
| 5 apc_sentinelagent_scope_only | 28 | 30 | 0 | same set as arm 2 by construction |
| 6 apc_sentinelagent_retained | 0 | 0 | 0 | attestation denies every shadow denial: APC-DENY x40; SIGNATURE_INVALID x4 (foreign key); allows 48 benign + 4 oracle-clean unsatisfiable cases |
| 7 apc_sentinelagent_fail_closed | 0 | 0 | 20 (FD events 26) | SHADOW-DENY x40, T1-REFUSE x24 (20 benign dynamic + 4 unsatisfiable), SIGNATURE_INVALID x4; FD events = 20 benign + 4 unsatisfiable + 2 oracle-clean first calls of the replay attack |

Seam test expectation: **0 cases** where arms 1 and 2 are both safe and any of arms
5/6/7 leaks. If the run measures a nonzero seam test, that is the project's first
composition-specific effect and the report must lead with it (highlighted section, new
finding, condition refined); if it measures 0 while arms 2/5 leak the same 28 cases,
the third pair **holds** the standalone-gap pattern and the report must name that as
the paper's actual finding. The two outcomes must not share boilerplate language.

## 9. What would falsify the condition

- A case predicted safe that leaks in arm 5: the condition is too weak on a field T0
  is supposed to represent (resource/recipient/canonicalization).
- A case predicted unsafe that does not leak **and** the receiving check's admission
  was the reason (not just a redundant earlier denial): the condition is too
  conservative on that field class.
- A nonzero seam test in either direction: the condition's separation between
  "incomplete but standalone" and "composition-specific" fails for this pair.
- A failed control (e.g., S1-valid rejected, or S2-foreign accepted): the harness or
  the prototype reading is wrong, and no claim from this run is kept until fixed.

## 10. Claim records

Claim: A handoff is safe only if the token carries a **checked** representation of
every authority and dynamic fact the call exercises, is synthesized serially after
APC's admission, and is not re-signed mid-check.
Status: HYPOTHESIS (stated before the run; tested on 96 synthetic cases under T0)
Access: reasoning (our construction; APC's Theorem 4.8 is READ but does not state this
cross-mechanism condition)
Source: APC `main.tex:297-305` for the same-mechanism precondition wording; no
SentinelAgent source states a cross-mechanism condition
Not claimed: This is not a theorem, does not generalize beyond APC → this SentinelAgent
prototype under T0, and does not show that any implementation of either paper must
behave this way.

Claim: The T0 handoff is serialized and static by harness construction but incomplete
on action-set membership, principal/task, composition history, cumulative budget,
expiry enforcement, revocation propagation, cross-call replay, and signer identity.
Status: DESIGN CHOICE / HYPOTHESIS
Access: reasoning (`call_to_token_mapping.md` §4-§7; the token fields and the P6/P7
code paths)
Source: `sentinelagent_audit_20261014/upstream/sentinelagent_das_prototype.py:47-72,133-172`
Not claimed: This does not show that a richer token or a chained delegation cannot
represent those facts; the attestation arm is exactly such an attempt.
