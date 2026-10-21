# Phase 0 — Located components, verified APIs, and paper re-read

Date: 2026-10-19 (Asia/Calcutta). This file records what existed before any new
harness code was written. `seam_pilot_v2/` did not exist at the start of this phase.

## 1. Existing APC pilot harness

Path: `C:\Users\prath\Downloads\RPaper\authorization_pilot\`

| Item | State |
|---|---|
| `seam_pilot/model.py` | 5,756 bytes, SHA-256 `83B2BBD3D2FFA050106E36B74013004B15C696CA46612E494F680FEE31B816A2` |
| `seam_pilot/native.py` | 8,566 bytes, SHA-256 `AF3114AEF550B01F9F87D98434059FFE181337F5BC1ADBBAFE208823E35936B0` |
| `seam_pilot/adapters.py` | 2,714 bytes, SHA-256 `9FE5482D84F95DAA0B212C7ECFD0F41C2B4A31799921D0FD7C76F1151C0BBDEE` |
| `seam_pilot/cases.py` | 3,053 bytes, SHA-256 `B80D8A7A76CCB1A13DA400C697FE142D1583294DA37E522958C96EF065ED7D33` |
| `seam_pilot/run.py` | 27,244 bytes, SHA-256 `7BAC2EB992569D8B211F0459A34A71534F85ED0BA0B9AE03504CF9FBE6788056` |
| Copied Task B pilot | `C:\Users\prath\Downloads\RPaper\task_b_verification_20261014\authorization_pilot\seam_pilot\` — all ten `.py` files are byte-identical to the originals (verified by SHA-256). |
| APC vendored repo | `authorization_pilot\vendor\bounded-agents`, git HEAD `d31a1ea115a3e97ab972ac8d03f23ef36cf9b653`, matching `pins.json`. |
| APC tests | `python -m pytest tests -q` from the vendored repo with system Python 3.12.7: **215 passed in 0.37s**. |
| Pilot `.venv` | `authorization_pilot\.venv\Scripts\python.exe` is Python 3.12.7 with `z3`, `pydantic` 2.12.5, `jsonschema`, and `docstring-parser`, but no pytest. The system Python 3.12.7 has pytest but no `z3`. Resolution: v2 harness runs use the pilot `.venv` interpreter (needed for `apc.pdp`/`secagent.tool` and the TraceGrant Pydantic models); generator/static checks may use either. Both can import `seam_pilot.model` alone. This is a runtime fact, not a code failure. |

The existing types this project reuses (not copies):

- `Call` (`model.py:14-22`): `tool`, `args`, `actor="agent:b"`, `session="root-task"`, `policy_version="pilot-v1"`, `cost=1.0`.
- `Case` (`model.py:24-51`): `id`, `family`, `template`, `variant`, `kind`, `resources`, `recipient`, `role_resources`, `prelude`, `attempts`, `status`, `cost_limit`, `composition_required`, `intervention`.
- `Decision` (`model.py:54-60`): `allowed`, `reasons`, `evidence`, `native_chain`, `checked_by`.
- `MockWorld` (`model.py:63-104`): four mock tools (`read_confidential`, `read_public`, `save_internal`, `send_external`), an `effects` list, `canonical()` which applies Python-signature defaults, and `execute()` which records effects.
- `Oracle` (`model.py:106-152`): independent root-task oracle; checks actor, session, policy version, resource scope, recipient, prohibited composition, cumulative budget; `observe()` records realized effects.
- `APC` wrapper (`native.py:62-135`): calls the real `apc.pdp.PolicyDecisionPoint.evaluate`; `handoff()` narrows to `agent:b`, can expire or revoke the envelope, can reset budget/composition, and can rebuild the PDP.
- `Progent` wrapper (`native.py:138-166`): not used by this experiment.

Existing pilot result relevant as a control reference: from
`authorization_pilot\results\verified\metrics.json`, `apc_alone` had 0 attack
successes / 0 benign false denials and `apc_apc_reset` had 10 attack successes /
0 benign false denials out of 40 attack and 40 benign cases (100 events per arm
because some cases have prelude+attempt events). This is the known reset leak
the new arm 4 must reproduce, not a new finding.

## 2. Independent TraceGrant implementation (Task D)

Path: `C:\Users\prath\Downloads\RPaper\tracegrant_task_d_20261014\implementation\`

| File | SHA-256 |
|---|---|
| `engine.py` | `25E8EB6EF0AB16FC7089373AB539ACF6FADF184507E67AC8EEEFA60386ACE72B` |
| `models.py` | `15423218D08A856FB2EB2D5888BA0AF949A14A18A3319CFB98A689A3EA34DA67` |
| `example_contracts.py` | `9BF21E722048F668C93AA18ED144E0AE8738037E4AB3A5B2882234483EFD6EE5` |
| `__init__.py` | `4603D8A5EB6B3468D07CC1D3D59B0781F70E472B677470FCB5C598209CEDFADB` |

The directory is not a git repository; the implementation identity is the SHA-256
hash above plus the Task D artifact path. This is **our own reimplementation from
the paper**, not the authors' code. No author repository/commit exists in the
artifact (Task D REPORT.md:15: upstream repository URL/commit NOT DONE).

Tests: `.\.venv\Scripts\python.exe -m pytest -q` with
`PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` from the Task D directory: **52 passed in
0.46s** on 2026-10-19. Python 3.12.7, Pydantic 2.12.5.

Public interface confirmed by reading the code, not assumed from the prompt:

```python
# implementation/engine.py:471
def check_call(request: CallRequest, state: RuntimeState) -> tuple[Decision, RuntimeState]:
```

- `CallRequest` (`implementation/models.py:117-123`): `tool: str`, `arguments: dict[str, JsonValue]`, `obligation: str | None`, `tainted_payloads: list[str]`.
- `Decision` (`implementation/models.py:201-207`): `code` in `ALLOW | DENY | PROOF-GAP | STEP_UP_AUTH`, `checks: dict[str, bool]` with `H/M/O/P/B`, `missing`, `obligation`, `proofs`.
- `establish(contract, registry, session, binding_mode='complete')` (`engine.py:336-348`) runs Algorithm 1 and raises `ValueError` on rejection; no executable state is created.
- `admit_evidence(record, state)` (`engine.py:380-397`) returns `(accepted, new_state)`.
- `check_call` does **not** check VERIFY postconditions; those are checked by `check_receipt` (`engine.py:559-589`) after dispatch. This matters for the mapping and property-coverage table.
- `check_call` returns a new state but does not consume budget, issue a certificate, or execute anything (`engine.py:471-494`).

## 3. Paper re-read — Search records

### 3.1 APC paper

Query: "Authorization Scope Definition 4.1, meet composition rule, Theorem 4.8 composition soundness preconditions"   Date: 2026-10-19
Opened: `C:\Users\prath\Downloads\RPaper\authorization_pilot\vendor\bounded-agents\paper\main.tex`, lines 219-309: Section 4.1 `Authorization Scope`, Definition 4.1 (`S=(R,A,D,X)`), the meet equation `S1 ⊓ S2 = (R1∩R2, A1∩A2, D1∩D2, X1∪X2)`, Definitions 4.2-4.4 (principal chain, budget, scoped principal), Section 4.4 `Prior-Action State`, Section 4.5 `Composition Constraints`, Theorem 4.8 and its proof plus the `Scope and limitations` paragraph. Also opened lines 63-90 (abstract/contributions) for context.
Blocked: nothing failed to load. I did not visually open the PDF `bounded-agents.pdf`; the `.tex` file is the source used to produce that PDF, and the text above is the actual source text.
Stopped: no for the requested sections. I did not read the full evaluation section, appendices, or the related-work section.
Conclusion: within the sections opened, APC defines `S=(R,A,D,X)`, the meet intersects R/A/D and unions X, and Theorem 4.8 is conditional on (1) completeness of X, (2) serialized admission, and (3) static X within a session; the theorem is about same-mechanism composition, not a cross-mechanism handoff.

Claim: APC's Theorem 4.8 states three preconditions for composition soundness: complete X, serialized admission, and static X.
Status: READ
Access: read-directly (`paper/main.tex:297-305`)
Source: `authorization_pilot/vendor/bounded-agents/paper/main.tex:297-305`
Not claimed: This does not show that APC's implementation enforces all three preconditions, nor that the theorem applies to a TraceGrant Contract; the theorem is stated for APC action sequences.

### 3.2 TraceGrant paper

Query: "Contract MAY/MUST/BIND/VERIFY structure, Equation 2 static analysis, Algorithm 1 line 14 CheckScope/CheckVerification"   Date: 2026-10-19
Opened: `C:\Users\prath\Downloads\RPaper\tracegrant_task_d_20261014\sources\paper.txt` (extracted from the saved PDF `tracegrant-2608.21126v1.pdf`), lines 230-318: Sections 4.2.1 `Semantic Contract Compilation`, Equation 1, the POEC Contract description, Section 4.2.2 `Static Contract Analysis`, Equation 2 `StaticAccept = WellFormed ∧ ControlSafe ∧ FlowSafe ∧ ScopeSafe ∧ VerifySafe`, and Algorithm 1 lines 1-18. Also opened lines 392-440 (Section 4.4, Equations 8-10), lines 755-823 (Section 5.7 white-box analysis and the optional-recipient gap), and lines 914-940 (Section 6.3 Limitations).
Blocked: the extracted text has layout artifacts (two-column interleaving and some replacement characters); Algorithm 1 line 14 is legible as `if ¬CheckScope(C′,RΣ,Σ) ∨ ¬CheckVerification(E,C′,OΣ,Σ) then return Reject ▷ ScopeSafe or VerifySafe`. I did not visually inspect the saved page images `page-05.png`...`page-08.png`, and I did not open the PDF page by page.
Stopped: no for the requested sections. I did not read the full evaluation, appendices, or related work.
Conclusion: within the sections opened, acceptance requires both CheckScope and CheckVerification to pass (the algorithm rejects if either fails); the Contract has MAY/MUST/BIND/VERIFY with the meanings described; and the paper's Limitations section says binding must cover every authority-bearing argument, including optional ones. I found no cross-mechanism composition theorem and no same-mechanism composition theorem for Contracts in the extracted text; the word "composition" appears only as "task composition" and "task decomposition" in the lines I searched.

Claim: Algorithm 1 line 14 rejects when either CheckScope or CheckVerification fails, so acceptance requires both.
Status: READ
Access: read-directly (`sources/paper.txt:280-282`; Task D code `static_analyze` at `engine.py:292-302` rejects on either predicate failure)
Source: `tracegrant_task_d_20261014/sources/paper.txt:280-282`; `implementation/engine.py:292-302`
Not claimed: This does not show that every implementation of the paper uses the same conjunction; it is the paper's Algorithm 1 and this reimplementation's behavior.

Claim: The TraceGrant Contract has no native field for principal identity, task revocation, expiry, or APC-style prior-action composition history.
Status: READ (absence observed in the Contract model and the sections opened)
Access: read-directly (`implementation/models.py:94-101`; paper `sources/paper.txt:234-260`, 296-318)
Source: `tracegrant_task_d_20261014/implementation/models.py:94-101`; paper `sources/paper.txt:234-318`
Not claimed: This does not show that TraceGrant cannot encode such facts as evidence or constraints in a richer Contract; it shows the current Contract model and the sections opened do not define native fields for them.

## 4. Directory state before new code

`C:\Users\prath\Downloads\RPaper\seam_pilot_v2\` did not exist. No new code was
written before this file. No file in `authorization_pilot\`, the Task B copy, or
`tracegrant_task_d_20261014\` was modified. No network calls and no paid LLM
calls were made in Phase 0.

## 5. Phase 0.5 — environment resolution and prediction freeze (2026-10-19)

- Combined interpreter check (pilot `.venv` Python, `sys.path` = `authorization_pilot`
  and `tracegrant_task_d_20261014`): `load_native()` succeeds and
  `from implementation.engine import check_call, establish, admit_evidence` succeeds.
  This is the interpreter used for the v2 matrix.
- Design documents written before harness code: `design/call_to_contract_mapping.md`
  (M0/M1/M2/M3, arm-by-arm mapping, artifact-vs-mechanism rule) and
  `design/composition_condition.md` (C1/C2/C3, prediction rule, pre-data template
  table, expected 2x2).
- Frozen case set: `design/case_generator.py` (deterministic; no clock, network, or
  randomness) produced `design/frozen_cases.json` and `design/prediction_lock.json`.
- Lock facts: 80 cases, 40 attack / 40 benign, 10 template pairs x 4 stratified
  parameter sets x 2 variants; 32 predicted unsafe, 48 predicted safe;
  `dataset_sha256 = 0fe1eafb0552549370415711a3aa08993715160d4ce391f10cfd59c988605ad2`.
- Expected arm 5 confusion (locked before data): TP=28, FP=4, FN=0, TN=48,
  precision=0.875, recall=1.0. The four expected false positives are the
  unsatisfiable-VERIFY attack family (admission allows, completion fails, no
  oracle-unauthorized effect).
- No prediction or case field may be edited after this lock. Results will be
  compared against this lock in `results/condition_validation.md`.
