# Claims update (H1-H6) after the SentinelAgent boundary experiment (1152 runs)

Statuses are observations about this implementation under the V1/V2 bridge mappings (the pinned prototype,
the harness bridge key model, the frozen 96-case set), not claims about SentinelAgent as deployed.

## H1 — Trusted-request laundering / scope trust
Operationalization: the bridge mints the token from a variant-derived manifest; the receiving check treats the
signed manifest as the authority record.
Observed: V1 admits the widened resource `docs:external/secret` in arm 5 (and standalone arm 2v) because the
manifest is derived from the delegate's pre-narrowing role scope; V2 admits the default-filled send to
`forbidden-default@example.test` in arm 5 (and standalone arm 2v) because the manifest SEND endpoint is the
resolved default. Both are faithful to the manifest the bridge wrote — the laundering is in the manifest
derivation, not in a check failure.
Status: REFUNDED for V1/V2 bridges — a non-narrowing-preserving manifest derivation launders widened scope.
Canonical T0 (narrowing-preserving) remains strict on resource widening.

## H2 — Dynamic state, identity and freshness do not cross and leak
Operationalization: principal/task rebinding, composition history, cumulative budget and replay, expiry,
revocation; paired benign controls, under V1 and V2.
Observed: unchanged from the SA pilot — these classes leak in arms 2/2v/5 under both variants and are
suppressed by arms 6/7. V1/V2 add no new dynamic-state leak class; their new leaks are scope/manifest
derivation classes (resource_widen under V1, omitted_forbidden_default under V2).
Status: SUPPORTED under V1/V2 (no new dynamic-state leak from the variants).

## H3 — Vocabulary mismatch
Operationalization: P6 manifest membership vs the authority the call actually needs.
Observed: V1's mismatch is resource-scope (role scope exceeds root R); V2's mismatch is the SEND endpoint
(default-filled recipient not the allowlisted snapshot recipient). Both manifest the receiver's vocabulary
gap: the token admits what the bridge wrote into the manifest.
Status: SUPPORTED under V1/V2 — two new concrete manifestations of the vocabulary mismatch.

## H4 — No shared audit trail
Observed: not tested in this run (same as the SA pilot).
Status: UNCHANGED / UNTESTED.

## H5 — Verification gap (keyholder minting power)
Operationalization: Phase A issuance review — any holder of the signing key can mint a manifest carrying scope
beyond any delegator's manifest; P6/P7 enforce only against the presented token's manifest (key-possession
equality, no signer identity).
Observed: confirmed as the root enabler of V1/V2. Because verification answers 'valid under my key?' not
'who signed?', a bridge holding the key can write a widened manifest (V1 role scope) or a default-filled SEND
endpoint (V2) and the receiver admits it. This is the same keyholder-minting property demonstrated by the SA
`keyholder_widen` family, now generalized to the bridge's own manifest derivation.
Status: UPDATED — H5 now explicitly covers keyholder minting power at the bridge/manifest-derivation layer,
not only at delegate-minted tokens.

## H6 — Similar-pair vs dissimilar-pair failure (UPGRADED)
Operationalization: the seam adds composed authority iff the bridge is not narrowing-preserving.
Observed: V1 and V2 are non-narrowing-preserving, and arm 5 leaks exactly the predicted 4 cases per variant
while arm 2 (canonical, narrowing-preserving T0) is safe on them and arms 6/7 suppress (0 leaks). So the
seam DOES add composed authority under a non-narrowing-preserving bridge. **However**, standalone arm 2v leaks
the identical set per variant, so the failure is a bridge-design artifact that exists without composition —
it is NOT composition-specific. The 'arm-5-only' phrasing is therefore imprecise: arm 2v (standalone) leaks
identically, so composition neither creates nor removes the failure.
Status: UPGRADED to: 'seam adds composed authority iff the bridge is not narrowing-preserving (witnesses V1/V2;
arm 5 leaks while canonical arm 2 is safe; suppressed by arms 6/7). Canonical T0/T1/T2 preserve zero seam.
Composition-specificity: NOT demonstrated by V1/V2 (arm 2v standalone leaks identically).

## Cross-cutting

The boundary experiment bounds the SA pilot's zero-seam finding: canonical zero-seam is a property of a
narrowing-preserving mapping, now bounded rather than assumed. V1/V2 produce the program's first seam-visible
leaks under non-narrowing-preserving bridges, but they are bridge-design artifacts (standalone in arm 2v),
not composition-specific failures. So the program's 'seam subtracts, it does not add' pattern holds for
composition, while the mapping-layer boundary is now characterized.

