# Phase A2 — Review-response audit applied to the SA pilot

Source reviewed (read-only): `seam_pilot_v2/ADVERSARIAL_REVIEW_RESULTS.md` (full, 138 lines).
Applies the review's four attack patterns (Leg A arm-invariant scoring, Leg B construction-forced
identities, Task 3 inert fixtures/vacuous checks, Correction 4 structural blindness) to the
SA pilot (`seam_pilot_sentinelagent`) before the boundary lock.

All findings are pre-lock and pre-run. This file and `design/sa_review_audit.json` are hashed
into `design/boundary_lock.json`.

---

## Leg A — Arm-invariant scoring rules (handoff/composition norms applied to no-handoff arms)

The SA pilot scores every arm with the same `V2Oracle` (reused from `seam_pilot_v2/adapters/v2_common.py`),
which is family-wide, not arm-specific. Two rules apply handoff- or composition-derived norms to
arms whose own world contains no handoff — principally arm 2 `sentinelagent_alone` (no APC anywhere).

### Rule A1 — Downstream resource scope intersected with the delegate's role scope

Source: `authorization_pilot/seam_pilot/model.py` (Oracle.decide), lines 130-135:

```python
resource = args.get("resource", "mail:external")
permitted = set(self.case.resources)
if phase == "downstream":
    permitted &= set(self.case.role_resources)
if resource not in permitted:
    reasons.append("resource_scope")
```

`role_resources` is the delegate's pre-narrowing role scope — a handoff/composition concept. The
intersection is applied in the downstream phase of **every** arm, including arm 2
`sentinelagent_alone`, whose world has no APC and no handoff.

**Impact if rescoped to arms where a handoff exists (arms 5/6/7 only):**
- For all 28 arm-2 leak cases, none flip to safe. Verification:
  - `keyholder_widen-0-a..3-a`: sole oracle reason is `resource_scope` on `docs:external/secret`.
    `docs:external/secret` is not in `case.resources` (`doc-001, internal, mail:external`) either, so
    removing the `role_resources` intersection leaves `resource_scope` in place. No flip.
  - Every other arm-2 leak case's reason(s) are `principal_binding`, `task_context`,
    `prohibited_composition`, `cumulative_budget`, `expired`, or `revoked` — none depend on the
    intersection. No flip.
- For arm-2 safe cases (e.g. `resource_widen`), the gate (P6) blocks the widened resource before
  the oracle's narrowing matters, so no safe→unsafe flip either.
**Result: no SA cell or classification flips under rescoping Rule A1.** Zero disclosure required
for A1 from the flip perspective.

### Rule A2 — Cross-call prohibited composition (`prohibited_composition`) applied to arm 2

Source: `authorization_pilot/seam_pilot/model.py`, lines 137-142:

```python
if self.case.composition_required:
    if (call.tool == "send_external" and self.confidential_read) or (
        call.tool == "read_confidential" and self.external_send
    ):
        reasons.append("prohibited_composition")
```

This is a composition-history norm (cross-call state `confidential_read` / `external_send`). It is
applied to arm 2 `sentinelagent_alone`, a standalone world with no APC composition history. The
case fabricates a prelude (`composition_history_loss-0-a` preludes `read_confidential doc-001` by
`agent:a`) to create the cross-call state, then the oracle holds it against arm 2's downstream
call.

**Impact if rescoped to arms where a handoff exists (arms 5/6/7 only):**
- `composition_history_loss-0-a..3-a` (arm 2): oracle reason `prohibited_composition` disappears
  (no handoff → no composition norm). The downstream `send_external` then has no oracle reason
  (recipient matches, resource default `mail:external` is permitted, no cumulative-budget breach).
  Gate allows → no `unauthorized_effect` → arm 2 becomes **safe**.
- Arm 5 (`apc_sentinelagent_scope_only`) remains a leak on the same 4 cases (handoff arm, rule
  still applies).
**Result: a flip occurs.** Under rescoping, arm 2 `composition_history_loss-0-a..3-a` flip from
leak→safe, and the seam test (arms 1+2 safe ∧ composed leak) would fire on those 4 cases with
**zero change in gate behavior** — the same instability the reviewer identified for the v2 pair.
This is disclosed here and in Phase D; it does not change the boundary experiment's V1/V2
predictions (those target `resource_widen` and `omitted_forbidden_default`, arm 5 only, arm 2
always canonical and safe).

### Summary of Leg A

| Rule | Source | Handoff/composition norm? | Applied to no-handoff arm 2? | Cell flips if rescoped? |
|------|--------|---------------------------|------------------------------|-------------------------|
| A1 downstream `permitted &= role_resources` | model.py:130-135 | Yes (delegate role scope) | Yes | No |
| A2 `prohibited_composition` (cross-call state) | model.py:137-142 | Yes (composition history) | Yes | Yes — `composition_history_loss-0-a..3-a` arm 2 leak→safe |

Disclosure: the SA arm-2 baseline is scored against norms its own world cannot violate, exactly as
the reviewer found for the v2 pair. The boundary experiment does not re-score; it reports under the
locked SA scoring and discloses this convention.

---

## Leg B — Construction-forced identities

Diff of consumed inputs per arm per case (T0 consumes only `snapshot.handoff_resources` for resource
ops and `snapshot.recipient` for the SEND endpoint; `sa_harness.t0_ops`, lines 168-171).

### Identity claim B1 — arm 2 == arm 5 leak sets (the pilot's headline: identical 28-case leak sets)

- Arm 2 snapshot: `case_snapshot(case)` → `handoff_resources = case.resources`, `recipient = case.recipient` (`v2_common.case_snapshot`, lines 153-167).
- Arm 5 snapshot: APC `post-handoff` effective scope → `handoff_resources = scope.resources`, `recipient = case.recipient` (`v2_common.APCV2.snapshot`, lines 126-142).
- For all 96 cases the post-handoff effective scope equals the root scope: APC's own `meet` narrows the role scope to `root R ∩ role R`, so for `resource_widen` the widened resource `docs:external/secret` is excluded, and for every other template `role_resources == resources`.
- Therefore T0's manifest is byte-identical between arm 2 and arm 5 on every case → identical P6/P7 decisions → identical leak sets **necessarily**.

**Label: forced-by-construction.** Set equality `arm2 == arm5` carries zero evidential weight about
composition; it could not come out otherwise. The informative contrast for the boundary experiment
is canonical arm 2 (safe) vs composed variant arm 5 (leak), and standalone arm 2v (leak) vs canonical
arm 2 (safe).

### Identity claim B2 — self-review `arm2_arm5_identical_leak_sets`

Directly checks B1. **Label: forced-by-construction** (it verifies a construction-forced identity).

### Identity claim B3 (boundary prediction) — under V1, 2v and 5 both derive from `role_resources` → identical manifests → 2v==5v set equality

**Label: forced-by-construction, not evidence.** Under V1, arm 2v (standalone variant) and arm 5
(scope-only variant) both build manifests from `case.role_resources`, so their manifests are
identical on every case and their leak sets are identical by construction. Under V2, 2v and 5 both
fill the omitted recipient with `forbidden-default@example.test` → identical manifests → identical
leak sets by construction. The informative contrast is canonical arm 2 (safe) vs composed variant
arm 5 (leak).

---

## Task 3 — Inert fixtures and vacuous checks

| Field / check | Consumed by | Single-valued / inert? | Cannot fail by construction outside one template? |
|---------------|-------------|------------------------|---------------------------------------------------|
| `output_schema` | P7 `check_output` | Not signed (absent from `_canonical`, prototype.py:47-53); `permitted = [STANDARD_TAG[tool]]` | Yes — P7 always ALLOWED for the frozen tool set (the presented tag is always in `permitted`). Vacuous. |
| `revoked` | P6/P7 revocation gate | Not signed; bridge tokens always `revoked=False`; never set from APC state | Yes for bridge tokens — revocation is APC-side only, never injected into the token. Inert at the token layer. |
| `expiry` | carried in token, never consulted | `EXPIRY_CURRENT` (2100) or `EXPIRY_PAST` (2001) per `status`; P6/P7 do not check expiry (prototype.py:133-149) | Yes — expiry cannot cause a P6/P7 deny/allow. Inert field; the expired/attack arm-2/arm-5 leaks happen because P6 ignores expiry, not because it enforces it. |
| `chain_refusal` (parent_hash != "ROOT") | arm 7 T1 chain check | All T0/T1 tokens have `parent_hash="ROOT"` | Vacuous under this construction; implemented for completeness only (harness.py:343-348). |
| T1 `tags_untranslated` | arm 7 T1 refusal | `derivable_tags` from the 4 frozen tools always contains `STANDARD_TAG[tool]` | Vacuous for the frozen tool set (harness.py:331-333). |
| T1 `recipient_untranslated` for non-send tools | arm 7 T1 refusal | Only checked for `send_external` | Inert for all `read_confidential`/`read_public`/`save_internal` calls. |
| `intent_text` | carried, never classified | Template string `one-step bridge call: {tool}` | P2 (intent NLI) is out of scope (mapping.md §7); never consulted. Inert. |

**Vacuous checks outside one template:** P7 cannot fail for any frozen-tool case (not just one template — all of them). `revoked` cannot fail for any bridge token. `expiry` cannot fail at the token layer in any arm. These are global vacuities, not template-scoped.

---

## Correction 4 — Structural blindness of the canonical seam test under a narrowing-preserving bridge

**Can the canonical seam test (arms 1 and 2 safe ∧ any of arms 5/6/7 leaks) fire under T0 (narrowing-preserving) in SA?**

No. Under T0, arm 2 == arm 5 by construction (B1: identical manifests because APC's meet narrows
the post-handoff scope to `root R ∩ role R`, never wider than root). So any case arm 5 leaks,
arm 2 also leaks → the conjunction "arm 2 safe AND arm 5 leaks" is false on every row → seam count
is structurally 0. This is exactly why the pilot's `expected_seam_test_cases = 0` and the self-review
`arm2_arm5_identical_leak_sets` passes.

**Which family types could make it fire?** Only a WIDENING family where the post-handoff scope
includes a call the root scope excludes — but T0's `meet` prevents that by construction. So under
narrowing-preserving T0, no family type can make the seam test fire. The seam test is structurally
blind to narrowing-type composition effects; it can only ever fire on a bridge that is NOT
narrowing-preserving (i.e., one whose manifest derivation widens relative to the root scope).

**That is the stated motivation for V1/V2:** V1 derives resource ops from `case.role_resources`
(the delegate's pre-narrowing role scope, which can exceed root R) and V2 fills the omitted
recipient default — both are non-narrowing-preserving derivations that let arm 5 admit calls arm 2
blocks. The boundary experiment exists precisely because the canonical seam test cannot fire under
T0; V1/V2 are the discriminating tests the v2 review's correction 4 called for ("an M0 variant
whose [manifest] is derived from the handoff scope" was not run in the SA pilot).

---

## Conventions to disclose (in the direct answer and reports)

1. **Arm-2 authority-input convention:** "the arm-2 authority input is the frozen case root scope,
   via canonical T0" — arm 2 is always canonical regardless of the variant loop variable (analog of
   the v2 reviewer's Task 3.1).
2. **Scoring convention:** `V2Oracle` is family-wide and arm-invariant; `permitted &= role_resources`
   (A1) and `prohibited_composition` (A2) are applied to arm 2 although arm 2's world has no handoff.
   Rescoping A2 flips `composition_history_loss-0-a..3-a` arm 2 leak→safe (disclosed; does not
   affect V1/V2 boundary predictions).
3. **Construction-forced identities:** arm 2==arm 5 (SA pilot, forced); 2v==5v under each boundary
   variant (forced). Neither is evidence about composition; the informative contrast is canonical
   arm 2 (safe) vs composed variant arm 5 (leak).
4. **Seam-test conditionality:** under narrowing-preserving T0 the seam test is structurally blind
   (count forced to 0); any nonzero seam under V1/V2 is a bridge-design artifact that exists
   standalone (arm 2v leaks identically), not a composition-specific effect.
