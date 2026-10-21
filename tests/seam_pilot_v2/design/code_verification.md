# Code verification of two claims from the seam_pilot_v2 report

Date: 2026-10-19. Purpose: verify, by reading the actual source, the two explanations
that `RESULTS_FOR_COAUTHOR.md` §3 gave for the two falsified predictions of the
original 80-case run. Both claims are recorded below as Claim records with the
quoted source attached. No code was modified for this verification; nothing was
re-executed; the quotes are from the pinned upstream files.

Verdict summary (details in the records):

- **Claim 1 (resource widening is dropped by the scope meet): CONFIRMED**, with one
  precision of wording that does not change the substance: the left operand of the
  meet is the *parent envelope's effective scope* (`self.effective_scope`), which in
  this pilot is itself a previously narrowed envelope — not the original root scope
  object. For the frozen `resource_widen` construction the resulting resource set is
  `root R ∩ (root R ∩ role_a R) ∩ role_b R`, which drops the widened resource exactly
  as claimed.
- **Claim 2 (`check_call` never evaluates VERIFY; only `check_receipt` does):
  CONFIRMED.** `check_call` computes exactly H, M, O, P, B and derives its decision
  code from them; the `VERIFY` field is read only in `check_receipt`.
- **Neither claim is wrong. No correction to the claims file (including the H1
  block) is required on these two points.** The precision in Claim 1 is noted so the
  wording can be made exact if the claims file is ever restated; it is not a factual
  error.

---

## Claim record 1 — the handoff's effective scope is a meet, and a role-only resource is dropped

**Claim.** "The handoff's effective scope is computed as `root.meet(role)`, so a
resource present only in the role scope but absent from the root R is dropped before
any Contract is synthesized."

**Status:** READ
**Access:** read-directly (quotes attached below)
**Source:** `authorization_pilot/vendor/bounded-agents/apc/core.py:85-96` (`Scope.meet`),
`apc/core.py:293-298` (`AuthorizationEnvelope.narrow`); context:
`authorization_pilot/seam_pilot/native.py:107-108` (the handoff that constructs the
delegate role scope), `seam_pilot_v2/adapters/v2_common.py:126-134` (the snapshot the
Contract is synthesized from).

**Quote 1a — `Scope.meet`, `apc/core.py:85-96` (verbatim):**

```python
    def meet(self, other: Scope) -> Scope:
        """Narrowing operation S₁ ⊓ S₂.

        Resources, actions, data_classifications: intersection.
        Composition restrictions: union (asymmetric — restrictions only grow).
        """
        return Scope(
            resources=self.resources & other.resources,
            actions=self.actions & other.actions,
            data_classifications=self.data_classifications & other.data_classifications,
            composition_restrictions=self.composition_restrictions | other.composition_restrictions,
        )
```

**Quote 1b — `AuthorizationEnvelope.narrow`, `apc/core.py:293-298` (verbatim):**

```python
    def narrow(self, delegate: Principal, key: bytes) -> AuthorizationEnvelope:
        """Create a narrowed envelope for a downstream principal.

        S(pᵢ) = S(pᵢ₋₁) ⊓ S_role(pᵢ)
        """
        narrowed_scope = self.effective_scope.meet(delegate.role_scope)
```

**Quote 1c — the pilot handoff that feeds `narrow` (context), `seam_pilot/native.py:107-108` (verbatim):**

```python
        role = Scope(frozenset(c.role_resources), self.root_scope.actions, self.root_scope.data_classifications)
        self.envelope = self.envelope.narrow(Principal("agent:b", ExecutionRole.ON_BEHALF_OF, role), self.key)
```

**Quote 1d — the snapshot the Contract is synthesized from (context), `seam_pilot_v2/adapters/v2_common.py:126-134` (verbatim):**

```python
    def snapshot(self) -> ScopeSnapshot:
        envelope = self.native.envelope
        scope = envelope.effective_scope
        chain = list(envelope.chain)
        return ScopeSnapshot(
            source="apc-post-handoff" if self.downstream else "apc-root",
            root_resources=tuple(sorted(str(r) for r in self.native.root_scope.resources)),
            handoff_resources=tuple(sorted(str(r) for r in scope.resources)),
```

**Assessment: CONFIRMED, with a wording precision.**

- `narrow` computes `self.effective_scope.meet(delegate.role_scope)`; `meet`
  intersects resources (Quote 1a, line `resources=self.resources & other.resources`)
  and actions (`actions=self.actions & other.actions`). A resource present only in
  the delegate role scope and absent from the parent effective scope is removed by
  that intersection. **Substance confirmed.**
- Precision: the left operand is the parent envelope's `effective_scope`, not the
  original root scope object. In this pilot the envelope passed to the handoff was
  already narrowed once (`native.py:86`, `self.envelope = envelope.narrow(agent, self.key)`),
  and each `narrow` re-meets with the delegate role scope. For the frozen
  `resource_widen` case the chain is `root R ∩ agent:a role R ∩ agent:b role R`,
  and since the role sets are supersets of root R except for the one widened
  resource, the effective resource set equals root R and the widened resource
  `docs:external/secret` is dropped. The claim's wording "root.meet(role)" is a
  simplification of "parent-effective.meet(role)"; the outcome is identical for the
  frozen construction.
- "Before any Contract is synthesized": confirmed for arm 5 — `arms.py` calls
  `apc.handoff(...)` and then takes `pre_snapshot = apc.snapshot()` (whose
  `handoff_resources` come from `envelope.effective_scope`, Quote 1d) before
  `gate.evaluate(...)` synthesizes the Contract; the widened resource is therefore
  already absent from the snapshot the mapping reads.
- **Action-set consequence (relevant to Extension E1, not part of this claim):**
  the same `meet` also intersects `actions` (Quote 1a). The original handoff cannot
  narrow the action set below the root A because the role scope is constructed with
  `self.root_scope.actions` (Quote 1c); E1 exercises the intersection by calling
  the public `narrow` API with a role scope whose action set is the narrowed A'.

**Not claimed:** This record does not claim that any other APC operation or any
deployment configuration behaves this way; it verifies the code path used by this
pilot. It does not re-run the original 80 cases or re-score any result.

---

## Claim record 2 — `check_call` never evaluates VERIFY; `check_receipt` is where VERIFY is checked

**Claim.** "`check_call` evaluates exactly H, M, O, P, B and never evaluates VERIFY;
VERIFY is only checked later by `check_receipt`."

**Status:** READ
**Access:** read-directly (quotes attached below)
**Source:** `tracegrant_task_d_20261014/implementation/engine.py:471-494` (`check_call`),
`engine.py:466-468` (`RISK`, the H input), `engine.py:559-589` (`check_receipt`).

**Quote 2a — `check_call`, `engine.py:471-494` (verbatim):**

```python
def check_call(request: CallRequest, state: RuntimeState) -> tuple[Decision, RuntimeState]:
    """Harness interface; Eq. 5. Authorization alone never spends effect budget."""
    frozen(state)
    new = state.model_copy(deep=True)
    schema = new.registry.tools.get(request.tool)
    permission = new.contract.MAY.get(request.tool)
    H = False
    if schema and permission:
        H = any(arg in request.arguments and arg in schema.args and schema.args[arg].role == 'payload'
                and (arg not in permission.trusted_payloads or not same(request.arguments[arg], permission.trusted_payloads[arg]))
                and RISK.search(canon(request.arguments[arg])) is not None for arg in request.tainted_payloads)
    M = bool(schema and schema.kind == 'effect' and permission and may_arguments(request.arguments, permission, schema))
    matching = [o for o in new.contract.MUST if o.kind == 'effect' and o.tool == request.tool
                and new.ledger.S[o.id] == OS.ACTIVE and (request.obligation is None or request.obligation == o.id)]
    O = len(matching) == 1
    B = new.ledger.B.get(request.tool, 0) > 0
    proofs, missing = ({}, [])
    if M and O:
        proofs, missing = argument_proofs(request, matching[0].id, new)
    P = M and O and not missing
    code = (DecisionCode.STEP_UP_AUTH if H else DecisionCode.ALLOW if M and O and P and B
            else DecisionCode.PROOF_GAP if M and O and B and not P else DecisionCode.DENY)
    return Decision(code=code, checks=dict(H=H, M=M, O=O, P=P, B=B), missing=missing,
                    obligation=matching[0].id if O else None, proofs=proofs), new
```

**Quote 2b — the H input regex, `engine.py:466-468` (context):**

```python
RISK = re.compile(r'<script\b|javascript:|\b(?:eval|exec)\s*\(|\b(?:bash|powershell|cmd)\s+-|'
                  r'ignore\s+(?:all\s+)?(?:previous|prior)\s+instructions|'
                  r'-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY-----|\b(?:password|api[_ -]?key)\s*[:=]', re.I)
```

**Quote 2c — `check_receipt`, `engine.py:559-589` (verbatim, the relevant part; full function shown through its return):**

```python
def check_receipt(native: NativeResult, cert: EffectCertificate, state: RuntimeState,
                  key: bytes) -> tuple[bool, RuntimeState]:
    """Eq. 8. Protected runner alone supplies NativeResult; no planner claims."""
    frozen(state)
    new = state.model_copy(deep=True)
    if not authentic_registered(cert, new, key):
        return False, new
    entry = new.ledger.K[cert.nonce]
    if entry.lifecycle != 'CONSUMED' or entry.receipt_processed:
        return False, new
    # One native outcome per dispatch, even when unsuccessful.
    entry.receipt_processed = True
    if (native.certificate_nonce != cert.nonce or native.tool != cert.tool or
            canon(native.arguments) != cert.canonical_arguments or not native.success or
            new.ledger.S[cert.obligation] != OS.ACTIVE):
        return False, new
    conditions = new.contract.VERIFY[cert.obligation].postconditions
    schema = new.registry.tools[cert.tool]
    if not all(k in native.result and type_matches(native.result[k], schema.result_fields[k]) and
               same(native.result[k], v) for k, v in conditions.items()):
        return False, new
    request = CallRequest(tool=cert.tool, arguments=native.arguments, obligation=cert.obligation)
    proofs, missing = argument_proofs(request, cert.obligation, new)
    if missing or not same(proofs, cert.proofs):
        return False, new
    new.ledger.receipts[cert.nonce] = EffectReceipt(certificate_nonce=cert.nonce,
                                                obligation=cert.obligation,
                                                native_result_digest=digest(native))
    new.ledger.S[cert.obligation] = OS.VERIFIED
    refresh(new)
    return True, new
```

**Assessment: CONFIRMED.**

- `check_call` computes exactly five booleans — `H`, `M`, `O`, `B`, `P` — and the
  decision code is a pure function of them (`STEP_UP_AUTH if H … PROOF_GAP … DENY`,
  Quote 2a). No `VERIFY`, no `postconditions`, and no `native.result` expression
  appears anywhere in the function. "Never evaluates VERIFY" is exact.
- The `VERIFY` field is read in `check_receipt` (Quote 2c:
  `conditions = new.contract.VERIFY[cert.obligation].postconditions`) and compared
  against the protected runner's `NativeResult`. "Only checked later by
  `check_receipt`" is exact *for VERIFY evaluation*; the precision is that
  `check_receipt` does more than that (certificate authenticity, nonce lifecycle,
  argument canonicalization, proof equality, obligation state) — it is not a
  "VERIFY-only" function. That does not change the claim.
- H is dormant unless the caller marks arguments as tainted (Quote 2a:
  `for arg in request.tainted_payloads`); the extension's Phase 5.5 finding that
  supplying provenance alone does not close the composition leak follows directly
  from Quote 2b (the marker string does not match `RISK`). This is consistent with
  `RESULTS_FOR_COAUTHOR.md` §5.

**Not claimed:** This record does not claim the implementation is free of other
VERIFY-adjacent checks, and does not claim that the paper's Algorithm 1 has the same
admission/completion split; it verifies only the two quoted functions as they exist
in the pinned Task D implementation.

---

## Outcome for the claims file

Neither claim is wrong. The "UNTESTED for action type" line in the H1 block of
`results/claims_update.md` concerns H1's action-type coverage, not either claim here,
and is superseded separately by `results/claims_update_extension.md` (Extension E1).
No correction to `results/claims_update.md` or to `RESULTS_FOR_COAUTHOR.md` §3 is
required by this verification; the only optional wording tightening is the Claim 1
precision noted above ("parent-effective.meet(role)" rather than "root.meet(role)").
