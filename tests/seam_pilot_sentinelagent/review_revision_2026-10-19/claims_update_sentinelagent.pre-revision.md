# Claims update (H1–H6) after the SentinelAgent pair (96×7)

Statuses are observations about this implementation under this mapping (the pinned prototype, the harness bridge key model, the frozen case set), not claims about SentinelAgent as deployed. Each block: operationalization in this pair, locked expectation, observed result, revised status. Artifacts: `results/sa/`; the claim/search/check records live in the design documents.

## H1 — Trusted-request laundering / scope trust

Operationalization: the bridge mints the token from the post-handoff snapshot; the receiving check treats the signed manifest as the authority record.

Observed: strict on what the vocabulary can express — resource widening (4), recipient substitution (4) and the forbidden default (4) are all denied by P6 (`BLOCKED: ... not in manifest`, 12 case-denials, 0 leaks) — and silent on what it cannot: 28 attack cases leak in arms 2/5, of which 24 are dynamic-state/identity classes with clean benign counterparts (0 FD).

Status: **SUPPORTED within this mapping, same shape as the TraceGrant pair.** The token is a faithful scope record; the laundering happens because a faithful scope record cannot carry an authorization decision.

Not claimed: that this is a flaw of the token design as such; it is what a scope-only handoff does when the receiving vocabulary lacks the fields.

## H2 — Dynamic state, identity and freshness do not cross and leak

Operationalization: principal/task rebinding, composition history, cumulative budget and replay, expiry, revocation; paired benign controls.

Observed: **supported again**. 24 of the 28 leaks are exactly this class (principal 4, composition 4 with marker-bearing external effects, repeated-calls 4 cases/6 events, budget 4, expiry 4, revocation 4). Arm 5 = arm 2, identical sets. Arm 6 carries the APC decision as signed evidence and closes all 28 with 0 leaks / 0 FD; arm 7 closes by refusing the untranslatable cases (20 benign FD).

Status: **SUPPORTED (second receiving mechanism).** The fix, again, is carrying the upstream decision across the seam under a trust boundary — not a check inside the receiving vocabulary.

## H3 — Vocabulary mismatch

Operationalization: `allowed` = HTTP method + endpoint pairs here, action type + resource in APC; intent = `intent_text` here, Ψ in APC.

Observed: mismatches manifest as **silence, not misparse**: expiry and revocation have no representable field at all, so expired/revoked tokens are admitted (4/4 each); the token's `src` is set from the attempted call's actor and never re-checked by P6/P7 (4/4 principal-rebind leaks); the completion/postcondition vocabulary of the other pair has no counterpart (the unsatisfiable-VERIFY class is inert — admitted, no effect, recorded, not scored as a pass).

Status: **SUPPORTED (structural).** Three pairs in, no shared vocabulary element for state or identity has appeared in any mapping we built.

## H4 — No shared audit trail

Observed: **not tested in this run.** The tokens are one-hop (`parent_hash = ROOT`) and no chain reconstruction or cross-mechanism trail interchange was exercised; the harness event log is not a mechanism trail.

Status: **UNCHANGED / UNTESTED.** The next natural instrument is a case family that reconstructs authority from the token hash chain and compares it with the APC envelope's history.

## H5 — Verification gap (first end-to-end test)

Operationalization: the bridge signs with the DAS key under the trust model; the receiver runs the native `verify_signature` path; foreign-key probes sign with the prototype's published constant.

Observed: a different key is always rejected (`SIGNATURE_INVALID`, 4 case-events per token arm; controls S2-foreign / S1-failure / S2-mutated; correctly rejected tokens are not false denials). A different minter with the same key is never distinguished (S2-two-minters returns identical codes; delegate-minted `keyholder_plain` admitted in all arms; `keyholder_widen` admitted 4/4 in arms 2/5 like any validly signed token).

Status: **CONFIRMED for "cannot verify without the key"; REFINED for what verification attests.** The HMAC check verifies integrity and key possession, not the source of authority: any keyholder is, to the receiver, equivalent to the DAS within the token vocabulary. Consequently the seam's critical interface is key distribution/trust, and a bridge holding the key is a fully trusted minter. The "or a call to the DAS" alternative was not exercised end-to-end (prototype has no live DAS service; checks ran in-process).

Not claimed: a universal statement about HMAC deployments; one prototype, one key model, one case family.

## H6 — Similar-pair vs dissimilar-pair failure

Operationalization: APC→SentinelAgent (chain narrowing) against the recorded APC→TraceGrant results.

Observed: the leak *shape* is nearly identical across the two pairs (dynamic state, identity, freshness dominate; arms 2/5 identical to each other; 0 FD in the standalone and scope-only arms). The pair differences show up in (a) the remediation mechanics (signed attestation vs evidence digest/receipt), and (b) one new standalone class, `keyholder_widen`, which is a property of the token ecosystem, not of the composition.

Status: **SUPPORTED with refinement.** For both pairs, the seam added no new failure mode; the receiving mechanism's vocabulary decided the failure face. The similar/dissimilar distinction affects how the seam can be repaired, not whether it fails.

## Cross-cutting: the pattern claim

Three pilots (TraceGrant pair 80×7, E1 40, SentinelAgent pair 96×7) produced zero composition-specific failures: every leak in a composed arm was already present with the receiving mechanism alone. This is now the paper's load-bearing finding; the per-pair sections above are its mechanism-specific instances.

