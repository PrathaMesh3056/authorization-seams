# APC call → SentinelAgent delegation token mapping (design choice, written before code)

Date: 2026-10-19. Status of everything in this file: **DESIGN CHOICE / HYPOTHESIS (ours)**.
Nothing here is READ from either paper as a translation rule. Neither paper specifies
how to turn an APC-authorized call into a SentinelAgent delegation token; this document
is our own construction, and every result produced with it is a statement about *this
implementation under this mapping*, never about "SentinelAgent's behavior" and never
about "a vulnerability in SentinelAgent or APC".

This is the third mechanism pair in the project (after Progent via Task B, TraceGrant
via `seam_pilot_v2` + Extension E1). It reuses, read-only: the frozen 80-case set and
the APC wrapper from `seam_pilot_v2` (untouched), and the pinned SentinelAgent
prototype from `sentinelagent_audit_20261014/upstream/` (untouched). No file in either
directory is modified; source SHA-256 values are recorded in the run manifest.

## 1. The modeling problem

- APC's unit of authorization is a single tool call evaluated against a session scope
  `S=(R,A,D,X)`, a budget, prior-action state, and an intent `Ψ`.
- SentinelAgent's unit of authorization is a **per-delegation-hop bearer token**
  `τ=(token_id, src, dst, scope, manifest, output_schema, policy, parent_hash, expiry,
  intent_text)`, HMAC-SHA256-signed, checked by two properties: **P6** (does the
  requested API call match the token's permitted scope/manifest) and **P7** (do the
  output's declared tags match the token's permitted output schema).
- There is no paper-specified translation from "APC admitted this call" to "mint a
  SentinelAgent token for it." The smallest bridge we can build is a **one-hop token
  synthesis**: one token per admitted call, one scope element, one manifest entry set,
  signed by the integration bridge.

This bridge necessarily drops most of APC's session state. The experiment measures
which dropped fields matter, and separates failures caused by the bridge shape from
failures caused by the token check itself.

## 2. Re-read records used for this design

### 2.1 Task C audit report (re-read)

Query: "token canonicalization/signing/verification scheme, P6/P7 behaviour, expiry/revocation coverage, signature controls, P2 status"
Date: 2026-10-19
Opened: `sentinelagent_audit_20261014/REPORT.md`, lines 92-113 (code-level token verification, exploratory token probes, signature controls), lines 46-52 (benchmark scope/limitations), lines 3, 9 (pins and reproduction summary).
Blocked: nothing failed to load.
Stopped: yes - task-specific; the unrelated benchmark/fault-tolerance sections were re-read only where they touch the token scheme. (The full report was read earlier during this project.)
Conclusion: within the sections opened - `_canonical()` signs `id, src, dst, sorted scope, sorted manifest, sorted policy, parent_hash, expiry, intent` via `json.dumps(..., sort_keys=True)`; `_sign()`/`verify_signature()` use the single literal prototype key `DAS_SECRET` with `hmac.compare_digest`; `output_schema` and `revoked` are **not** in the signed payload; P6/P7 check revocation and signatures but **do not check expiry**; a legitimately signed expired token passed both P6 and P7 in Task C's own probe; and because the scheme is one symmetric HMAC key with no signer identity, "key possession also permits minting signatures" (Task C's own words). The DAS prototype never invokes an IntentVerifier (P2 unenforced).

Claim: `_canonical()` excludes `output_schema` and `revoked`; P6/P7 check signatures and revocation but not expiry; the scheme has no asymmetric verification key and no signer identity.
Status: READ
Access: read-directly (report lines quoted above; verified again against `upstream/sentinelagent_das_prototype.py:47-72,133-172`)
Source: `sentinelagent_audit_20261014/REPORT.md:94-113`; `sentinelagent_audit_20261014/upstream/sentinelagent_das_prototype.py:47-72` and `:133-172`
Not claimed: This does not claim any remote exploit; Task C's schema probe was an in-process stored-token mutation under a stated access assumption.

### 2.2 Pinned SentinelAgent prototype (re-read for this bridge)

Query: "DelegationToken fields and constructor, check_api_call/check_output exact behaviour, DelegationAuthorityService surface"
Date: 2026-10-19
Opened: `sentinelagent_audit_20261014/upstream/sentinelagent_das_prototype.py`, lines 27-205 (key constant, `DelegationToken`, `DelegationAuthorityService.issue_root_token/delegate/check_api_call/check_output/reconstruct_chain/revoke_chain`).
Blocked: nothing failed to load.
Stopped: yes - the HTTP handler and benchmark builder below line 205 were not re-read here (already covered by Task C).
Conclusion: P6 normalizes the call as `f"{method.strip().upper()} {endpoint.rstrip('/')}"` and allows it if the string appears in any manifest operation list; P7 takes the union of `permitted` tags across the token's output schemas and blocks if any presented tag is outside it; both first return `TOKEN_NOT_FOUND` / `TOKEN_REVOKED` / `SIGNATURE_INVALID` as applicable. `expiry` participates only in delegation (`C5_FAIL`), never in P6/P7.

Claim: P6 is a manifest string membership check and P7 is a permitted-tag whitelist check, both gated only by token presence, revocation and signature; neither consults `expiry`.
Status: READ
Access: read-directly
Source: `sentinelagent_audit_20261014/upstream/sentinelagent_das_prototype.py:133-172`
Not claimed: This says nothing about the paper's full protocol; it is the pinned prototype's behaviour.

## 3. Token vocabulary used by the bridge

Reused verbatim from the pinned prototype (no reimplementation): `DelegationToken`
(constructor and `_canonical`/`_sign`/`verify_signature`/`token_hash`/`to_dict`) and
`DelegationAuthorityService.check_api_call` / `check_output` / `revoke_chain`. The
bridge constructs tokens with the same class the prototype uses; the receiving check
is the prototype's own methods, called on a token registered in a fresh
`DelegationAuthorityService` per check (the same store-lookup shape the prototype's
HTTP endpoints use; the HTTP transport itself is not part of this experiment).

## 4. T0 — primary one-step scope-only token synthesis (arms 2 and 5)

Given a call with canonical arguments (the same `MockWorld.canonical` result the
existing pilot uses, so Python-signature defaults are already applied) and a scope
snapshot (arm 5: APC's post-handoff snapshot; arm 2: the frozen case's root scope via
`case_snapshot`), the bridge mints exactly one token τ with:

| Field | Value (T0) | Note |
|---|---|---|
| `token_id` | `tau-{case_id}-{sequence:02d}` | deterministic; the prototype's `issue_root_token` uses `uuid4`, the harness does not read randomness |
| `src` | the calling agent (`call.actor`) | P6/P7 never read `src`; this is carried, not checked |
| `dst` | `mock-tool-executor` | synthetic tool-execution principal |
| `scope` | `{call.tool}` | one scope element: **the attempted tool** (the M0-analogue "trust the already-authorized caller" choice; never compared with APC's action set A) |
| `manifest` | `{call.tool: [op, ...]}` | see the operation table below; derived from the snapshot's authority values, not from the attempted argument |
| `output_schema` | `{call.tool: {"permitted": [standard_tag(call.tool)], "prohibited": []}}` | standard tag per frozen tool: `read_confidential→confidential_record`, `read_public→public_record`, `save_internal→internal_write`, `send_external→external_send` |
| `policy` | `set()` | no APC policy vocabulary is mapped |
| `parent_hash` | `"ROOT"` | one-hop token; the bridge acts as issuer |
| `expiry` | `4102444800.0` (2100-01-01Z) when `status != "expired"`, else `978307200.0` (2001-01-01Z) | deterministic constants; no wall clock. P6/P7 do not check expiry (READ, §2); the value is carried, not enforced |
| `intent_text` | `one-step bridge call: {tool}` | template string naming the tool; no natural-language check (P2 out of scope, §7) |
| `signature` | native `_sign()` | computed by the prototype's own method under the bridge key (§6) |
| `revoked` | `False` | prototype default; not in the signed payload; the bridge does not know about APC-side revocation |

**Call derivation (the string P6 checks, and the manifest it checks against):**

| Tool | verb | authority value | manifest operation list (T0) | standard output tag |
|---|---|---|---|---|
| `read_confidential` | `READ` | canonical `resource` | `[READ r for r in snapshot.handoff_resources]` | `confidential_record` |
| `read_public` | `READ` | canonical `resource` | `[READ r for r in snapshot.handoff_resources]` | `public_record` |
| `save_internal` | `WRITE` | canonical `resource` | `[WRITE r for r in snapshot.handoff_resources]` | `internal_write` |
| `send_external` | `SEND` | canonical `recipient` | `[SEND snapshot.recipient]` | `external_send` |

P6 is therefore a membership test of the attempted authority value against the
snapshot-derived list; the tool axis always passes by construction (the scope element
is the attempted tool). P7 is checked with the standard tag derived from the attempted
tool; it therefore always passes for the frozen tool set and checks schema membership
only, never a value the mapping would have to trust.

**Execution.** Register τ in a fresh `DelegationAuthorityService`; call the native
`check_api_call(token_id, verb, endpoint)` and `check_output(token_id, {standard_tag})`;
admission requires both to return allowed. Both raw messages are recorded on the
event.

**What T0 translates:** the requested tool as the scope element (not checked against
APC's action set A), resource choices from the snapshot's R, the recipient allowlist
from the snapshot, canonical argument defaults, the signature-keyed token identity,
and a schema-level output tag.

**What T0 does not translate:** action-set membership (the tool is copied), principal
and task (carried as `src`, never compared), composition history X / prior-action
state, cumulative budget consumed, cross-call replay state, envelope expiry
enforcement, revocation propagation, signer identity (§6), value-level/semantic
output tags, payload semantics, and the P2 intent check (§7).

## 5. Case-declared token provenance (signature family)

For the new signature-family cases the presented token is not bridge-synthesized; the
case declares its provenance and the receiving check treats the presented token as
untrusted input (the caller substitutes its own token):

- `signer="foreign"`: the token content is the same T0 content, but the signature is
  computed manually with the prototype's published key (`REAL_DAS_KEY`) instead of the
  trusted bridge key. The expected result of the check is `SIGNATURE_INVALID`.
- `mint="delegate"`: the token is minted by the calling delegate itself under the
  trusted bridge key, with a manifest the delegate wrote (for the attack variant, a
  manifest that includes an escalated resource outside the root R). The expected
  result of the check, for a key holder, is "no difference from a bridge-minted
  token": verification is key-possession equality, not provenance.

This is the first end-to-end operationalization of H5 ("SentinelAgent tokens are
HMAC-signed, so another mechanism cannot verify them without the key or a call to the
DAS" - `Paper_Claims_and_Takeaways.md:42`): the check can distinguish *key material*
(a different key fails), but a symmetric HMAC has no signer identity, so any holder of
the trusted key is equivalent to the issuer.

## 6. Key material model and the trust relationship

- `BRIDGE_KEY = b"seam-pilot-sentinelagent-bridge-test-key-2026"` - the harness's own
  test key. The bridge signs with it. Deliberately public; this experiment does not
  test key management or key secrecy.
- The receiving check runs the prototype's own `check_api_call` / `check_output`,
  which verify with the module constant `DAS_SECRET`. The harness **sets that module
  constant to `BRIDGE_KEY` at runtime** (in-process attribute assignment on the
  imported module). This is the modeled **trust relationship**: a real deployment
  would need the issuing mechanism's actual key or a mutual trust relationship between
  issuer and receiver; here the receiver is configured with the bridge's key.
  Upstream files are not edited; the file's byte SHA-256 is recorded in the run
  manifest. Documented difference from a real deployment: the "real DAS" is not in
  this loop, and the key is a public test credential.
- `REAL_DAS_KEY = b"sentinelagent-das-secret-key-2026"` - the literal prototype key
  (READ from `sentinelagent_das_prototype.py:27`). It appears in this experiment only
  as the "different key" for the foreign-signer probe. `verify_signature()` is
  symmetric: a token signed with this key does **not** verify under the receiver's
  configured key, and (equivalently) the receiver could not verify a token from the
  prototype's own DAS without being given that key.

## 7. P2 / intent: explicitly out of scope

No natural-language intent exists in an APC call to compare against, and the pinned
prototype never invokes an IntentVerifier in its delegation path (READ, §2.1). This
experiment therefore does not synthesize an intent for P2 to check; `intent_text` is
a template string. No case family targets P2, no LLM/NLI call is made anywhere in
this run, and no prediction depends on P2. This is stated as a scope limitation, not
silently omitted.

## 8. T1 — conservative-reject variant (arm 7)

T1 refuses before token construction if any of the following cannot be translated
(each refusal names its field; the call is denied):

1. the attempted tool is not in the snapshot's action set A;
2. an authority argument has no snapshot-derived operation, where the resource must be
   derivable from the **intersection of the root R and the handoff R** (a resource
   present only in the handoff scope is untranslatable), and the recipient must equal
   the snapshot's allowlisted recipient;
3. the declared output tags are not derivable from the frozen tool schema (vacuous
   for the frozen tool set);
4. the case exercises envelope expiry, revocation, prior-action composition history,
   cumulative cost, or cross-call replay (T0 cannot represent any of these natively);
5. `verify_kind == "unsatisfiable"`: the token vocabulary has no completion stage, so
   an unsatisfiable completion claim is untranslatable rather than silently dropped;
6. the call's actor or session differs from the handoff context;
7. the token chain is unsatisfiable: `parent_hash != "ROOT"` and unresolvable in the
   service's hash index (vacuous under T0/T1 construction, implemented for
   completeness).

T1 is expected to deny many benign cases; that is the point of a fail-closed control.
It must not leak.

## 9. T2-attest — retained variant (arm 6)

T2-attest builds the same T0 token τ and adds one **attestation token** τ_att: a real
`DelegationToken` constructed by the bridge, signed by the bridge's own `_sign()`
(§6), whose `intent_text` is the canonical JSON of the shadow APC decision record
(the 12 fields of `shadow_evidence_values`, reused from the v2 harness:
`apc_allowed, apc_reasons, budget_remaining, composition_clear, freshness, revoked,
principal, task, tool, resource, recipient, evidence_digest`). The attestation's
`scope` is `{"apc-attestation"}`; its manifest carries the tool and a one-line digest
of the decision.

The receiving gate verifies, in order, and denies at the first failure (all condition
booleans are recorded):

1. attestation present → `ATTESTATION-MISSING`
2. `τ_att.verify_signature()` (the prototype's own method, real code path) →
   `ATTESTATION-SIGNATURE-INVALID`
3. `intent_text` parses to a JSON object with all required fields →
   `ATTESTATION-PAYLOAD-INVALID`
4. binding: the signed record's tool/resource/recipient/task/principal equal the call
   and snapshot being checked → `ATTESTATION-BINDING-MISMATCH` (this is the replay
   check: a validly signed record for another call)
5. `apc_allowed is True` → otherwise `APC-DENY` (reasons carried from the record)
6. `budget_remaining >= call.cost` → `BUDGET-INSUFFICIENT`
7. `freshness ∈ {current, renewed}` → `FRESHNESS-INVALID`
8. `revoked is False` → `REVOKED-INVALID`
9. `composition_clear is True` → `COMPOSITION-INVALID`
10. then P6/P7 on τ as in T0.

The attestation is a signed harness artifact, not a production key-distribution
design; it shows what *can* be carried through the token primitive's own signature
path.

## 10. Arm-by-arm mapping use

| Arm | Receiving check | Mapping / state carried |
|---|---|---|
| 1 `apc_alone` | APC | none; APC sees all calls with full state (arm code reused from `seam_pilot_v2` verbatim) |
| 2 `sentinelagent_alone` | SentinelAgent P6/P7 | T0 from the frozen case root scope; no APC anywhere; prelude calls gated by T0 as well |
| 3 `apc_apc_preserved` | APC | same-mechanism control; envelope narrowed to `agent:b`, budget/composition preserved (reused verbatim) |
| 4 `apc_apc_reset` | APC | same-mechanism control; budget/composition reset at handoff (reused verbatim) |
| 5 `apc_sentinelagent_scope_only` | SentinelAgent P6/P7 | T0 from APC's **post-handoff** effective scope snapshot; shadow APC runs first and commits state but its denial is not propagated |
| 6 `apc_sentinelagent_retained` | SentinelAgent P6/P7 + attestation | T2-attest; the shadow APC decision and pre-admission budget state are carried in the signed attestation; the trust boundary is the attestation |
| 7 `apc_sentinelagent_fail_closed` | SentinelAgent P6/P7 | T1; shadow denial retained; deny on any untranslatable exercised field |

**Interpretation of "run APC's admission first" (execution order):** every call is
executed strictly sequentially; no arm runs concurrently with another. In arms 2/5/6/7
the handoff is serialized: the prelude is processed first (APC for 5/6/7, T0 for 2);
at the downstream phase the handoff is performed, then for each call a pre-snapshot is
taken, the shadow APC admission (if present) completes and commits its budget and
composition state, and only then is the token synthesized from the **pre-admission
snapshot** and checked. In arm 5 the shadow denial is recorded but not propagated;
in arm 6 the shadow decision is what crosses; in arm 7 the shadow denial is retained.

## 11. Anticipated failure modes (HYPOTHESIS, before data)

- T0 is expected to leak on: principal/task rebinding, composition-history loss,
  cumulative-budget reset, cross-call replay, expiry, revocation, and delegate-minted
  tokens (no signer identity).
- T0 is expected to catch resource widening (the post-handoff effective scope is
  `root R ∩ role R` by APC's own meet, so the widened resource is not in the manifest),
  recipient substitution, omitted-argument forbidden defaults, and foreign-key-signed
  tokens (signature check).
- The unsatisfiable-VERIFY family has no retention-target analogue: the SentinelAgent
  check has no completion/postcondition stage, so those cases are ordinary
  oracle-authorized calls under this pair (recorded as `verify_satisfiability` being
  not-applicable in the condition).
- T1 is expected to deny every attack and the benign cases whose construction touches
  dynamic state.
- T2-attest is expected to close the T0 leaks by carrying the shadow decision in the
  token's own signed payload, at the cost of depending on the bridge's key being the
  receiver's configured key.

## 12. Mapping artifact vs mechanism behavior — the classification rule

Adapted from `seam_pilot_v2/design/call_to_contract_mapping.md` section 10, with
"Contract" replaced by "token":

- **Mapping artifact**: the failure depends on a T0 choice that could reasonably be
  made differently while still using SentinelAgent's token vocabulary (e.g., using the
  requested tool as the scope element instead of checking A; deriving the manifest per
  call instead of a delegated chain; copying the attempted call's standard output tag).
- **Mechanism / token-vocabulary behavior**: the failure persists under a reasonable
  alternative mapping because the token model itself has no *checked* field for the
  exercised fact (composition history, cumulative cost, replay state) or the P6/P7
  checks have no place to consult it (expiry and revocation are token fields but are
  not consulted by P6/P7 - READ, §2), and a symmetric HMAC has no signer identity at
  all.
- Every disagreement in the SA results gets one of these verdicts before a finding is
  kept.

## 13. Claim records

Claim: A one-hop token per APC call is a possible bridge, but it drops APC's principal
comparison, prior-action history, cumulative budget, expiry enforcement, revocation
propagation, and has no signer identity.
Status: DESIGN CHOICE (HYPOTHESIS)
Access: reasoning (no source states this; it follows from the token field/check lists
in `sentinelagent_das_prototype.py:29-72,133-172` and Task C's report)
Source: `sentinelagent_audit_20261014/upstream/sentinelagent_das_prototype.py:29-72`;
`sentinelagent_audit_20261014/REPORT.md:94-113`
Not claimed: This does not show that a richer token or a chained delegation cannot
carry those facts; the attestation arm is exactly such an attempt.

Claim: Under T0 the unsupported fields can leak, so the composition condition predicts
those cases unsafe before any run.
Status: HYPOTHESIS (untested at the time of writing)
Access: reasoning (mapping design, not measured)
Source: none (our construction)
Not claimed: This does not show that SentinelAgent's intended deployment shape would
leak the same way; a real deployment's receiver may hold the real key and use chains.
