# Phase A — Issuance semantics check (read-only)

Source (read-only, not modified):
`sentinelagent_audit_20261014/upstream/sentinelagent_das_prototype.py`
sha256: `739d9db1e836d7edaf567cabfa6c4ae074bb81d74ad522e98b7d04a3237b36be`

All quotations below are line-quoted from that file. Line numbers refer to the
file as read on 2026-10-19.

## Q1 — What does issue_root_token require (key, authority, scope source)?

The key is the module-level constant `DAS_SECRET`, defined at line 27:

```
27: DAS_SECRET = b"sentinelagent-das-secret-key-2026"
```

`issue_root_token` (lines 82-95) is a method on `DelegationAuthorityService`. It
takes the authority inputs as explicit parameters — there is no ambient key or
authority argument; the signer key is the module constant used inside
`DelegationToken._sign()` (line 56):

```
82:     def issue_root_token(self, user: str, agent: str, scope: Set[str],
83:                          manifest: Dict, output_schema: Dict,
84:                          policy: Set[str], intent: str) -> DelegationToken:
...
85:         token = DelegationToken(
86:             token_id=str(uuid.uuid4())[:8], src=user, dst=agent,
87:             scope=scope, manifest=manifest, output_schema=output_schema,
88:             policy=policy, parent_hash="ROOT", expiry=time.time() + 3600,
89:             intent_text=intent
90:         )
```

The **scope source is the caller-supplied `scope` parameter** — it is stored
verbatim as `token.scope` (line 87) with no derivation from any delegator. The
token is then registered in `hash_index` and `children` (lines 92-93):

```
92:         self.hash_index[token.token_hash()] = token.token_id
93:         self.children[token.token_id] = []
```

**Answer:** `issue_root_token` requires (a) the module-level `DAS_SECRET` key
(used by `_sign()` at line 56), (b) explicit authority parameters
`(user, agent, scope, manifest, output_schema, policy, intent)`, and (c) the
scope comes straight from the caller-supplied `scope` argument — it is not
derived from or intersected with any existing delegator state (there is no
parent for a root token).

## Q2 — Does delegate intersect the requested child scope with the delegator's own scope/manifest, or accept the caller-provided scope as-is?

It **intersects / requires subset** — it does NOT accept the caller-provided
scope as-is. `delegate` (lines 97-131):

```
97:     def delegate(self, parent_token_id: str, dst_agent: str,
98:                  requested_scope: Set[str], intent: str) -> Tuple[Optional[DelegationToken], str]:
...
100:         parent = self.tokens.get(parent_token_id)
...
107:         # C2: Authority check — P1 enforcement
108:         if not requested_scope.issubset(parent.scope):
109:             return None, f"C2_FAIL: Scope escalation: {requested_scope - parent.scope}"
110:         # C2a: Manifest narrowing
111:         child_manifest = {s: ops for s, ops in parent.manifest.items() if s in requested_scope}
112:         child_output_schema = {s: schema for s, schema in parent.output_schema.items() if s in requested_scope}
```

Line 108 rejects any requested scope element not already in `parent.scope`
(C2: authority check). Line 111 then derives the child manifest from the
**parent's own manifest**, keeping only entries whose scope element is in the
requested scope (C2a: manifest narrowing). The caller's requested scope is a
filter/upper bound, not a source of new operations.

**Answer:** `delegate` intersects the requested child scope with the delegator's
own scope (C2 rejection on escalation) and narrows the manifest from the
delegator's manifest (C2a). It does not accept the caller-provided scope as-is.

## Q3 — What exactly is signed, with what key; is the manifest validated at issuance or only at presentation?

**What is signed:** `DelegationToken._canonical()` (lines 47-53) and `_sign()`
(lines 55-56):

```
47:     def _canonical(self) -> str:
48:         return json.dumps({
49:             "id": self.token_id, "src": self.src, "dst": self.dst,
50:             "scope": sorted(self.scope), "manifest": {k: sorted(v) for k, v in sorted(self.manifest.items())},
51:             "policy": sorted(self.policy), "parent_hash": self.parent_hash,
52:             "expiry": self.expiry, "intent": self.intent_text
53:         }, sort_keys=True)
54:
55:     def _sign(self) -> str:
56:         return hmac.new(DAS_SECRET, self._canonical().encode(), hashlib.sha256).hexdigest()
```

Signed payload: `id, src, dst, scope, manifest, policy, parent_hash, expiry,
intent`. **Not signed:** `output_schema` and `revoked` (absent from
`_canonical`, present only in `to_dict` lines 64-72). This is independently
noted in `call_to_token_mapping.md` section 2.1.

**With what key:** `DAS_SECRET` (line 27), a single symmetric HMAC-SHA256 key.
`self.signature = self._sign()` is computed in `DelegationToken.__init__` at
line 44 — i.e., **at issuance/token-construction time**.

**Manifest validation:** At issuance, `delegate` *derives* the child manifest
from the parent manifest (line 111) but does not validate it against an
independent authority record. At presentation, `check_api_call` (P6, lines
133-149) enforces membership of the requested call string against the
presented token's own manifest:

```
133:     def check_api_call(self, token_id: str, method: str, endpoint: str) -> Tuple[bool, str]:
...
143:         call = f"{method.strip().upper()} {endpoint.rstrip('/')}"
144:         for scope_elem, permitted_ops in token.manifest.items():
145:             if call in permitted_ops:
146:                 self._log("P6_ALLOW", token, extra={"call": call})
147:                 return True, f"ALLOWED by scope:{scope_elem}"
148:
149:         return False, f"BLOCKED: {call} not in manifest"
```

So the manifest is **bound by signature at issuance** (it is part of the
signed canonical payload) and **enforced at presentation time** (P6/P7 consult
`token.manifest`). `output_schema` and `revoked` are presentation-time reads
of unsigned fields.

**Answer:** The signature covers `id, src, dst, scope, manifest, policy,
parent_hash, expiry, intent` under `DAS_SECRET`, computed at token
construction (issuance). `output_schema` and `revoked` are NOT signed. The
manifest is enforced at presentation (P6 membership check against the
presented token's manifest), while issuance only derives/narrows it from the
parent (no independent validation).

## Q4 — Consequence: can a party holding the signing key mint scope beyond any delegator's manifest, with only presentation-time manifest checks in the way?

**Yes.** Because the scheme is a single symmetric HMAC key with no signer
identity (no `signer` or `issuer` field in `_canonical`), verification answers
"is this valid under my key?", not "who minted it?". A holder of `DAS_SECRET`
can construct a `DelegationToken` whose `manifest` contains any operation on
any scope element, sign it with `_sign()`, and the receiver's `verify_signature()`
(line 58-59) will accept it:

```
58:     def verify_signature(self) -> bool:
59:         return hmac.compare_digest(self.signature, self._sign())
```

P6 then admits exactly what that minter wrote into the manifest (line 144-147).
The harness operationalizes this trust model in `install_bridge_key()` (the
receiver is configured with the bridge key) and the signature family
(`keyholder_widen`: a delegate holding the trusted key mints a manifest
containing `docs:external/secret`, outside the root `R`, and it is admitted in
arms 2/5). The only gate is presentation-time P6/P7, which check against the
*presented* manifest — the minter's own manifest — so they add no constraint
beyond key possession.

**Answer:** Yes. A party holding the signing key can mint a token whose manifest
carries scope beyond any delegator's manifest; because verification is key-
possession equality with no signer identity, and P6/P7 enforce only against the
presented token's own manifest, the presentation-time checks admit whatever the
key holder wrote. The delegate's manifest does not constrain a fellow key
holder.

## One-line answer

`issue_root_token` requires the module `DAS_SECRET` key plus explicit `(user,
agent, scope, manifest, output_schema, policy, intent)` parameters and takes
scope verbatim from the caller; `delegate` intersects `requested_scope`
against `parent.scope` (rejecting escalation) and narrows the manifest from
`parent.manifest` (it never accepts caller scope as-is); the signature covers
`id, src, dst, scope, manifest, policy, parent_hash, expiry, intent` under
`DAS_SECRET` at issuance (`output_schema` and `revoked` are unsigned), and the
manifest is enforced only at presentation via P6/P7 membership against the
presented token's manifest — so any holder of the signing key can mint scope
beyond any delegator's manifest, with presentation-time checks offering no
further constraint.
