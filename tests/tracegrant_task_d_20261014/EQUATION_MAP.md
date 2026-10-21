# Source-to-code and test map

Primary source is the saved arXiv v1 PDF. Equation numbers below are its numbers; the implementation is an explicitly documented interpretation.

| Source | Code | Test evidence and limit |
| --- | --- | --- |
| Eq. 1, p. 5 | `Contract`, JSON examples | `test_eq_01_hand_authored_poec_boundary_no_compiler` tests the hand-authored POEC input shape. F_sem is intentionally NOT DONE. |
| Eq. 2 / Algorithm 1, p. 6 | `normalize`, `static_analyze` | `test_eq_02_algorithm_1_acceptance_and_normalization`; static rejection, reachability, budget, scope, selector and optional-coverage tests. All five predicates execute in Algorithm 1 order. |
| Eq. 3, p. 6 | `Ledger`, `establish`, `refresh` | `test_eq_03_ledger_initial_state_and_successor_activation`; evidence, effect, output and waiver transitions. |
| Eq. 4, p. 7 | `evidence_qualifies`, `admit_evidence` | Five independently falsified admission conjuncts; returned observation never becomes proof evidence on failure. |
| Eq. 5, p. 7 | `argument_proofs`, `check_call` | `test_eq_05_all_decision_branches_and_H_precedence`, payload screening, scope/type denials, deterministic selector and both poisoning probes. |
| Eq. 6, p. 7 | `EffectCertificate`, `issue_certificate`, `certificate_mac` | HMAC, binding, budget, session, expiry and tampering tests. Nonce/session/registry/mode/time/MAC are this artifact's additions. |
| Eq. 7, p. 7 | `validate_certificate`, `dispatch`, `Gateway.execute` | Exact-argument match, consumption, replay, competing dispatches and runner-crash control. No real native execution. |
| Eq. 8, p. 8 | `NativeResult`, `EffectReceipt`, `check_receipt` | CertMatch, ExecSuccess, PostSatisfied and ProvenanceValid individually falsified; no completion on a bad result. |
| Eq. 9, p. 8 | `final_gate`, `waive`, `verify_output` | Hard-obligation closure, receipt-before-completion, output and legitimate Contract exemption. Completion support checks strengthen the plain state predicate. |
| Eq. 10, p. 8 | No general implementation | `test_eq_10_finite_soundness_control_not_general_proof` checks a stated four-candidate toy domain only. General semantic soundness is NOT DONE. |
| Section 5.7, pp. 14-15 | Two exploratory probes | Semantic poisoning is admitted by the complete profile; optional-recipient coverage gap is enabled only in diagnostic mode. Synthetic mechanism illustrations, not author-trajectory replay. |
| Section 6.3, p. 17 | Complete binding profile and recorded authenticity limit | Default covers optional authority arguments; complete binding of a poisoned optional field still does not authenticate it. |
