# Boundary condition — APC -> SentinelAgent bridge boundary test

Date: 2026-10-19. Status: **PRE-REGISTERED / LOCKED**. Predictions are locked and hashed
BEFORE any run; the lock is never edited after the first run; any locked-vs-observed
mismatch goes into results/boundary/reconciliation.json, never into edits.

This is one bounded, deterministic experiment in the APC -> SentinelAgent seam program.
It reuses, read-only: seam_pilot_sentinelagent (adapters/sa_harness.py, design/sa_cases.json,
design/sa_lock.json), seam_pilot_v2 (adapters/v2_common.py, adapters/arms.py), and the pinned
SentinelAgent prototype (sentinelagent_audit_20261014/upstream/sentinelagent_das_prototype.py).
No file outside seam_pilot_sa_boundary is modified. No git. No network. No paid LLM calls.

## 1. Question

Does a plausible NON-narrowing-preserving bridge design create cases where arms 1 and 2
(mechanism-alone) are safe but a composed arm (5/6/7) leaks — i.e., a seam-specific failure
— under pre-registered predictions? Two bridge variants are tested; only the token-manifest
derivation changes. Scope tags, expiry, key handling, attestation, and scoring stay identical
to canonical T0.

## 2. Variants (manifest derivation only)

V1 role-scope derivation: resource ops in the minted manifest derive from case.role_resources
(the delegate's pre-narrowing role scope) instead of the post-handoff effective scope. The SEND
endpoint is unchanged.

V2 resolved-call default filling: for calls that omit a recipient, the manifest SEND endpoint
derives from the resolved argument (MockWorld default filled in) instead of the snapshot
recipient. Resource ops unchanged.

Arms: 1 apc_alone, 2 sentinelagent_alone (canonical bridge reference), 2v
sentinelagent_alone_variant (standalone, variant bridge), 5 apc_sentinelagent_scope_only,
6 apc_sentinelagent_retained, 7 apc_sentinelagent_fail_closed. Matrix:
arms {1,2,2v,5,6,7} x variants {v1,v2} x 96 cases = 1152 runs, strictly sequential.

## 3. Predictions (locked, pre-run; pure function of frozen inputs)

### Diff tables (pre-computed at lock time; pure function of sa_cases.json)

V1 diverges from canonical on 8 attack cases (resource_widen-0-a..3-a, keyholder_widen-0-a..3-a),
each adding `READ docs:external/secret` (the widened resource outside root R). No benign case
diverges. Note: keyholder_widen cases are delegate-minted (provenance=delegate), so the V1
derivation is not applied to them — no behavioral effect. Behavioral V1 divergence =
resource_widen-0-a..3-a only.

V2 diverges from canonical on 4 attack cases (omitted_forbidden_default-0-a..3-a), each
replacing the snapshot recipient with `SEND forbidden-default@example.test`. No benign case
diverges. Behavioral V2 divergence = omitted_forbidden_default-0-a..3-a only.

### Per-arm per-variant predictions

V1:
- arm 1 apc_alone: 0 leaks (APC-only, unchanged).
- arm 2 sentinelagent_alone (canonical): 0 leaks, safe on all cases.
- arm 2v sentinelagent_alone_variant (V1): leaks resource_widen-0-a..3-a (4 leaks). Standalone.
- arm 5 apc_sentinelagent_scope_only (V1): leaks resource_widen-0-a..3-a (4 leaks).
- arm 6 apc_sentinelagent_retained (V1): 0 leaks; APC-DENY on the 4 resource_widen attacks.
- arm 7 apc_sentinelagent_fail_closed (V1): 0 leaks; SHADOW-DENY / T1-REFUSE on the 4.
- benign families: unchanged (no benign divergence in the diff table).

V2:
- arm 1 apc_alone: 0 leaks.
- arm 2 sentinelagent_alone (canonical): 0 leaks, safe on all cases.
- arm 2v sentinelagent_alone_variant (V2): leaks omitted_forbidden_default-0-a..3-a (4 leaks). Standalone.
- arm 5 apc_sentinelagent_scope_only (V2): leaks omitted_forbidden_default-0-a..3-a (4 leaks).
- arm 6 apc_sentinelagent_retained (V2): 0 leaks; APC-DENY on the 4 omitted_forbidden_default attacks.
- arm 7 apc_sentinelagent_fail_closed (V2): 0 leaks; SHADOW-DENY / T1-REFUSE on the 4.
- benign families: unchanged (no benign divergence in the diff table).

### Seam test (arms 1 and 2 safe AND a composed arm leaks)

V1: numeric seam fires on resource_widen-0-a..3-a (arm 2 safe, arm 5 leaks).
V2: numeric seam fires on omitted_forbidden_default-0-a..3-a (arm 2 safe, arm 5 leaks).

Classification: because arm 2v (standalone variant bridge) leaks the EXACT same set as arm 5
in each variant, the failure is a **bridge-design artifact that exists standalone**; composition
neither creates nor removes it. It is NOT composition-specific. The informative contrast is
canonical arm 2 (safe) vs composed variant arm 5 (leak), and standalone arm 2v (leak) vs
canonical arm 2 (safe).

## 4. Named conventions (declared in the lock)

- "the arm-2 authority input is the frozen case root scope, via canonical T0" (analog of the
  v2 reviewer's Task 3.1). Arm 2 is always canonical regardless of the variant loop variable.
- Scoring conventions carried from the SA pilot (V2Oracle, unauthorized_effect, false_denial,
  attack_success per sa_lock.json / composition_condition_sentinelagent.md section 7).
- Construction-forced identities predicted (from the diff tables): under V1, 2v and 5 both
  derive from role_snapshot/resources → identical manifests → 2v==5v set equality is
  construction-forced, NOT evidence; under V2, 2v and 5 both fill the default recipient →
  identical manifests → construction-forced, NOT evidence. The informative contrast is
  canonical arm 2 (safe) vs composed variant arm 5 (leak).

## 5. Falsification criteria

- Any predicted cell differing from observation is recorded verbatim in
  results/boundary/reconciliation.json; the lock is never edited after the first run.
- A failed control (CV1-CV5) aborts the matrix; no claim is kept until fixed.
- The boundary theory "seam adds composed authority iff the bridge is not narrowing-preserving"
  is supported if arm 5 leaks exactly the predicted 4 cases per variant while arms 1/2 are safe
  and arms 6/7 suppress, AND arm 2v leaks the identical set standalone (bridge-design artifact,
  not composition-specific). It is falsified if arm 5 does not leak the predicted cases, or if
  a benign case leaks, or if arms 6/7 leak.

## 6. Section 10 classification reminder (call_to_token_mapping.md)

Every disagreement gets one of two verdicts before a finding is kept:
- **Mapping artifact**: the failure depends on a T0 choice that could reasonably be made
  differently while still using SentinelAgent's token vocabulary (e.g., deriving the manifest
  from role_resources instead of the post-handoff effective scope; filling the default recipient
  instead of the snapshot recipient).
- **Mechanism / token-vocabulary behavior**: the failure persists under a reasonable alternative
  mapping because the token model itself has no checked field for the exercised fact, or P6/P7
  have no place to consult it, or a symmetric HMAC has no signer identity.
V1/V2 leak cases are mapping artifacts (the manifest derivation choice), not defects in
SentinelAgent or APC; canonical zero-seam is a property of a narrowing-preserving mapping, now
bounded rather than assumed.
