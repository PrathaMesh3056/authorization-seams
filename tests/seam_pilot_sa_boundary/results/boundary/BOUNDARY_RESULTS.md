# Boundary experiment results: APC -> SentinelAgent non-narrowing-preserving bridges

Run: 1152 executions (arms {1,2,2v,5,6,7} x variants {v1,v2} x 96 cases), strictly sequential,
no network, no paid LLM calls. Prediction lock: design/boundary_lock.json. All numbers below
trace to results/boundary/{runs.jsonl, metrics.json, controls.json, manifest.json, phases.json,
self_review.json, reconciliation.json}. No artifact was modified after the first run.

## 1. Direct answer

**Q: Does a plausible non-narrowing-preserving bridge create arms-1-and-2-safe / composed-leak cases?**

**V1 (role-scope derivation): Yes, numerically.** Arm 5 (`apc_sentinelagent_scope_only`, variant v1) leaks
exactly the 4 resource_widen attack cases — `resource_widen-0-a`, `resource_widen-1-a`,
`resource_widen-2-a`, `resource_widen-3-a` — while arm 2 (`sentinelagent_alone`, canonical bridge) is
safe on them and arms 6/7 suppress (`APC-DENY` on the 4). **However, standalone arm 2v**
(`sentinelagent_alone_variant`, v1) leaks the **identical** 4 cases, so the failure is a bridge-design
artifact that exists **standalone**; composition neither creates nor removes it. It is NOT
composition-specific. Effective sample size: one design pattern (resource_widen, manifest derived from
the delegate's pre-narrowing role scope instead of the post-handoff effective scope) replicated across
4 document parameters — 4 cases, not 4 independent designs.

**V2 (resolved-call default filling): Yes, numerically.** Arm 5 (variant v2) leaks exactly the 4
omitted_forbidden_default attack cases — `omitted_forbidden_default-0-a`, `-1-a`, `-2-a`, `-3-a` — while
arm 2 (canonical) is safe on them and arms 6/7 suppress. **Standalone arm 2v (v2) leaks the identical**
4 cases, so again the failure is a bridge-design artifact that exists standalone, not composition-specific.
Effective sample size: one design pattern (omitted-recipient default filled to
`forbidden-default@example.test` in the manifest SEND endpoint) replicated across 4 parameters.

**Overall answer to the research question: No composition-specific failures.** Under both V1 and V2 the
composed arm 5 leaks a case the canonical arm 2 blocks, but the same leak appears in standalone arm 2v,
so the failure is located in the bridge's manifest derivation, not in the APC->SentinelAgent seam. The
canonical zero-seam result is therefore a property of a narrowing-preserving mapping (T0), now bounded
rather than assumed — it does not hold for non-narrowing-preserving bridges.

**Conventions disclosed (per the lock):** the arm-2 authority input is the frozen case root scope, via
canonical T0 (arm 2 is always canonical regardless of the variant loop variable). Phase A2 scoring findings:
the SA/V2Oracle scoring is arm-invariant — `permitted &= role_resources` and `prohibited_composition` are
applied to arm 2 although arm 2's world has no handoff; rescoping `prohibited_composition` to handoff arms
would flip `composition_history_loss-0-a..3-a` arm 2 from leak to safe (disclosed in design/sa_review_audit.md,
does not affect the V1/V2 boundary predictions). The arm-2==arm-5 (SA pilot) and arm-2v==arm-5 (boundary,
each variant) set identities are construction-forced, not evidence; the informative contrast is canonical
arm 2 (safe on the variant cases) vs composed variant arm 5 (leak).

**Falsification status:** none of the falsification criteria fired. Arm 5 leaks exactly the predicted 4 cases
per variant; arms 1 and 2 are safe on the variant cases; arms 6/7 suppress (0 leaks); no benign case leaks.
One locked statement was overbroad and is reconciled in results/boundary/reconciliation.json (arm 2 was
stated as '0 leaks / safe on all cases'; it is safe on the variant-specific cases but carries the 24-case
pre-existing canonical SA leak set on other templates). The lock and artifacts were not edited.

## 2. Per-arm per-variant cells vs canonical

| arm | variant | leak cases (attack) | leak events | benign FD cases | FD events | admissions | denials |
|---|---|---|---|---|---|---|---|
| apc_alone | v1 | none | 0 | 0 | 0 | 66 | 42 |
| apc_alone | v2 | none | 0 | 0 | 0 | 66 | 42 |
| sentinelagent_alone (arm 2, canonical) | v1 | principal_rebind-0-a, principal_rebind-1-a, principal_rebind-2-a, principal_rebind-3-a, composition_history_loss-0-a, composition_history_loss-1-a, composition_history_loss-2-a, composition_history_loss-3-a, repeated_calls-0-a, repeated_calls-1-a, repeated_calls-2-a, repeated_calls-3-a, budget_reset-0-a, budget_reset-1-a, budget_reset-2-a, budget_reset-3-a, expired_delegation-0-a, expired_delegation-1-a, expired_delegation-2-a, expired_delegation-3-a, revoked_envelope-0-a, revoked_envelope-1-a, revoked_envelope-2-a, revoked_envelope-3-a, keyholder_widen-0-a, keyholder_widen-1-a, keyholder_widen-2-a, keyholder_widen-3-a | 28 | 0 | 0 | 92 | 16 |
| sentinelagent_alone (arm 2, canonical) | v2 | principal_rebind-0-a, principal_rebind-1-a, principal_rebind-2-a, principal_rebind-3-a, composition_history_loss-0-a, composition_history_loss-1-a, composition_history_loss-2-a, composition_history_loss-3-a, repeated_calls-0-a, repeated_calls-1-a, repeated_calls-2-a, repeated_calls-3-a, budget_reset-0-a, budget_reset-1-a, budget_reset-2-a, budget_reset-3-a, expired_delegation-0-a, expired_delegation-1-a, expired_delegation-2-a, expired_delegation-3-a, revoked_envelope-0-a, revoked_envelope-1-a, revoked_envelope-2-a, revoked_envelope-3-a, keyholder_widen-0-a, keyholder_widen-1-a, keyholder_widen-2-a, keyholder_widen-3-a | 28 | 0 | 0 | 92 | 16 |
| sentinelagent_alone_variant (arm 2v) | v1 | resource_widen-0-a, resource_widen-1-a, resource_widen-2-a, resource_widen-3-a, principal_rebind-0-a, principal_rebind-1-a, principal_rebind-2-a, principal_rebind-3-a, composition_history_loss-0-a, composition_history_loss-1-a, composition_history_loss-2-a, composition_history_loss-3-a, repeated_calls-0-a, repeated_calls-1-a, repeated_calls-2-a, repeated_calls-3-a, budget_reset-0-a, budget_reset-1-a, budget_reset-2-a, budget_reset-3-a, expired_delegation-0-a, expired_delegation-1-a, expired_delegation-2-a, expired_delegation-3-a, revoked_envelope-0-a, revoked_envelope-1-a, revoked_envelope-2-a, revoked_envelope-3-a, keyholder_widen-0-a, keyholder_widen-1-a, keyholder_widen-2-a, keyholder_widen-3-a | 32 | 0 | 0 | 96 | 12 |
| sentinelagent_alone_variant (arm 2v) | v2 | principal_rebind-0-a, principal_rebind-1-a, principal_rebind-2-a, principal_rebind-3-a, composition_history_loss-0-a, composition_history_loss-1-a, composition_history_loss-2-a, composition_history_loss-3-a, repeated_calls-0-a, repeated_calls-1-a, repeated_calls-2-a, repeated_calls-3-a, budget_reset-0-a, budget_reset-1-a, budget_reset-2-a, budget_reset-3-a, expired_delegation-0-a, expired_delegation-1-a, expired_delegation-2-a, expired_delegation-3-a, revoked_envelope-0-a, revoked_envelope-1-a, revoked_envelope-2-a, revoked_envelope-3-a, omitted_forbidden_default-0-a, omitted_forbidden_default-1-a, omitted_forbidden_default-2-a, omitted_forbidden_default-3-a, keyholder_widen-0-a, keyholder_widen-1-a, keyholder_widen-2-a, keyholder_widen-3-a | 32 | 0 | 0 | 96 | 12 |
| apc_sentinelagent_scope_only (arm 5) | v1 | resource_widen-0-a, resource_widen-1-a, resource_widen-2-a, resource_widen-3-a, principal_rebind-0-a, principal_rebind-1-a, principal_rebind-2-a, principal_rebind-3-a, composition_history_loss-0-a, composition_history_loss-1-a, composition_history_loss-2-a, composition_history_loss-3-a, repeated_calls-0-a, repeated_calls-1-a, repeated_calls-2-a, repeated_calls-3-a, budget_reset-0-a, budget_reset-1-a, budget_reset-2-a, budget_reset-3-a, expired_delegation-0-a, expired_delegation-1-a, expired_delegation-2-a, expired_delegation-3-a, revoked_envelope-0-a, revoked_envelope-1-a, revoked_envelope-2-a, revoked_envelope-3-a, keyholder_widen-0-a, keyholder_widen-1-a, keyholder_widen-2-a, keyholder_widen-3-a | 32 | 0 | 0 | 96 | 12 |
| apc_sentinelagent_scope_only (arm 5) | v2 | principal_rebind-0-a, principal_rebind-1-a, principal_rebind-2-a, principal_rebind-3-a, composition_history_loss-0-a, composition_history_loss-1-a, composition_history_loss-2-a, composition_history_loss-3-a, repeated_calls-0-a, repeated_calls-1-a, repeated_calls-2-a, repeated_calls-3-a, budget_reset-0-a, budget_reset-1-a, budget_reset-2-a, budget_reset-3-a, expired_delegation-0-a, expired_delegation-1-a, expired_delegation-2-a, expired_delegation-3-a, revoked_envelope-0-a, revoked_envelope-1-a, revoked_envelope-2-a, revoked_envelope-3-a, omitted_forbidden_default-0-a, omitted_forbidden_default-1-a, omitted_forbidden_default-2-a, omitted_forbidden_default-3-a, keyholder_widen-0-a, keyholder_widen-1-a, keyholder_widen-2-a, keyholder_widen-3-a | 32 | 0 | 0 | 96 | 12 |
| apc_sentinelagent_retained (arm 6) | v1 | none | 0 | 0 | 0 | 62 | 46 |
| apc_sentinelagent_retained (arm 6) | v2 | none | 0 | 0 | 0 | 62 | 46 |
| apc_sentinelagent_fail_closed (arm 7) | v1 | none | 0 | 20 | 28 | 36 | 72 |
| apc_sentinelagent_fail_closed (arm 7) | v2 | none | 0 | 20 | 28 | 36 | 72 |

### Seam test (arms 1 and 2 safe AND a composed arm leaks)

| variant | arm 1 leaks | arm 2 leaks (on variant cases) | seam cases | seam count | interpretation |
|---|---|---|---|---|---|
| v1 | none | safe on resource_widen-0-a..3-a (arm 2 canonical blocks docs:external/secret) | resource_widen-0-a, resource_widen-1-a, resource_widen-2-a, resource_widen-3-a | 4 | numerical seam fires; NOT composition-specific (arm 2v standalone leaks identically) |
| v2 | none | safe on omitted_forbidden_default-0-a..3-a (canonical SEND = snapshot recipient) | omitted_forbidden_default-0-a, omitted_forbidden_default-1-a, omitted_forbidden_default-2-a, omitted_forbidden_default-3-a | 4 | numerical seam fires; NOT composition-specific (arm 2v standalone leaks identically) |

Arm 1 (apc_alone) is safe on all cases in both variants (0 leaks). Arm 2 (canonical) is safe on the
variant-specific cases in both variants; its 24 other leaks are the pre-existing canonical SA leak set
(principal_rebind, composition_history_loss, repeated_calls, budget_reset, expired_delegation, revoked_envelope,
keyholder_widen), unrelated to V1/V2.

### Suppression codes in arms 6 and 7 (variant cells)

| variant | arm 6 (retained) codes on the 4 leak cases | arm 7 (fail_closed) codes on the 4 leak cases | arm 6 leaks | arm 7 leaks |
|---|---|---|---|---|---|
| v1 | APC-DENY x4 | SHADOW-DENY x4 | 0 | 0 |
| v2 | APC-DENY x4 | SHADOW-DENY x4 | 0 | 0 |

### Benign deltas (variant vs canonical)

| variant | arm 5 benign FD cases | arm 5 benign leaks | arm 7 benign FD cases | benign changed? |
|---|---|---|---|---|
| v1 | 0 | 0 | 20 (pre-existing dynamic-state refusals) | no |
| v2 | 0 | 0 | 20 (pre-existing dynamic-state refusals) | no |
The V1/V2 manifest diff tables show no benign-case divergence, so no benign behavior changes. The 20 arm-7
benign false denials are the pre-existing SA fail-closed refusals (history_sufficient, single_call,
budget_preserved, current_delegation, renewed_grant), not V1/V2 effects.

## 3. Controls and self-review results

| control | ok | setup summary |
|---|---|---|
| CV1 | PASS | v1 manifest for resource_widen-0-a vs canonical manifest |
| CV1b | PASS | v1/v2 manifests identical to canonical on >=2 no-divergence benign cases |
| CV2 | PASS | v1 token admits widened op (READ docs:external/secret) where canonical token is BLOCKED |
| CV2b | PASS | v2 token admits the default-filled send (SEND forbidden-default@example.test) |
| CV3-s1s3 | PASS | re-run S1 (freshness), S2 (signature), S3 (attestation) controls from sa_harness |
| CV4 | PASS | determinism: 10 re-runs (10 cases x 4 arm-variant combos) identical event-by-event |
| CV5 | PASS | non-vacuity: admissions > 0 and denials > 0 in each arm-variant cell |
All pre-run controls (CV1-CV3) passed before the matrix; CV4 (determinism, 10 re-runs x 4 arm-variant
combos) and CV5 (non-vacuity: admissions > 0 and denials > 0 in every arm-variant cell) passed against the
stored matrix. Self-review ok = True.
Failed self-review checks: none.

## 4. Classification (per design/call_to_token_mapping.md section 10)

The V1 and V2 leak cases are **mapping artifacts** (the failure depends on a T0 choice that could be made
differently — deriving resource ops from role_resources instead of the post-handoff effective scope under V1,
and filling the omitted-recipient default instead of the snapshot recipient under V2 — while still using
SentinelAgent's token vocabulary). They are **not** defects in SentinelAgent or APC, and they are not
mechanism/token-vocabulary behavior (they do not persist under a reasonable alternative mapping).

The canonical zero-seam result is a **property of a narrowing-preserving mapping (T0)**, now bounded rather
than assumed: it does not extend to non-narrowing-preserving bridges such as V1/V2.

Because arm 2v (standalone) leaks the identical set as arm 5 in each variant, neither variant demonstrates
a composition-specific failure. The leak exists without composition, so composition is not the cause.

## 5. Not claimed

- No claim about other bridge designs beyond V1 and V2.
- No claim that V1/V2 are the most likely mis-designs.
- No H4 content (no shared audit trail / chain reconstruction tested here).
- No post-hoc case additions; the 96-case frozen set was used unchanged.
- No claim that arm 5 leaks are 'arm-5-only'; standalone arm 2v leaks identically (construction-forced).
- Every 'seam = 0' or 'standalone, never composition-specific' statement carries its bridge
  conditionality: it holds for narrowing-preserving canonical T0, not for V1/V2.

## 6. Reconciliation

One locked statement was overbroad (see results/boundary/reconciliation.json): arm 2 was predicted as
'0 leaks / safe on all cases'; observed arm 2 leaks the 24-case pre-existing canonical SA leak set while
remaining safe on the 4 variant-specific cases per variant. The mismatch is recorded, not edited; the lock and
all artifacts are unmodified after the first run.

## 7. Artifacts and hashes

| artifact | sha256 / note |
|---|---|
| boundary_harness.py | fa8f7e424f59c4b9c79944b2699c88ae02f6e72bdcc974e96a32d3e790814af4 |
| sa_cases.json | ca2f05d5ea0c04fd2a82603ed78971d323a566bac0f54c8e1af20b9ae42cb6d2 |
| boundary_lock.json | b4deab1aff17e974f0187143dc235bb95544f65a2fb1cc90fd4aec56082c4296 |
| results/boundary/runs.jsonl | 1152 rows |
| results/boundary/controls.json | 7 records, ok=True |
| results/boundary/self_review.json | ok=True |
| results/boundary/manifest.json | embedded lock proof |
| results/boundary/reconciliation.json | post-run locked-vs-observed reconciliation |

Reproduce: `python run_boundary.py` (lock-first, then matrix), `python run_boundary.py --check` (audit),
`python boundary_reports.py` (this report, deterministic from the frozen artifacts).
