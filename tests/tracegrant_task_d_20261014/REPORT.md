# TraceGrant Task D: implementation and verification report

Date: 2026-10-14 (Asia/Calcutta). Independent research artifact; no claim of numerical reproduction, author-code fidelity, semantic soundness, novelty or priority.

Implemented Pydantic v2 Contract and Ledger models, ordered static analysis for Algorithm 1, evidence admission, Eq. 5 decision checks, typed derivation/selection proofs, one-shot HMAC certificates, protected dispatch transitions, receipt validation and the final gate. The harness interface is `implementation.engine.check_call(request, state) -> (Decision, RuntimeState)`.

The code's final pytest run passed **52/52** tests, with 0 failed, 0 errors and 0 skipped. Eq. 1 has an input-shape test only because the LLM compiler is intentionally absent. Eq. 10 has a finite toy-domain test only; its general semantic-soundness assumption is not verified. See [equation map](EQUATION_MAP.md).

## Primary and secondary sources

Primary: [TraceGrant arXiv:2608.21126v1](https://arxiv.org/pdf/2608.21126v1), saved unchanged as `sources/tracegrant-2608.21126v1.pdf`. SHA-256: `792b43409241ec642203d85b4c11b01040efed86cd40cb3c05a22a795166331b`. Extracted all 18 pages. Read the method, white-box paths, limitations and data-availability text; visually inspected the method equations and Algorithm 1 on rendered pp. 6-8. Rendered pp. 5-8 are saved. This does not assert that all paper pages were visually inspected.

Secondary: unchanged copy of the supplied `TraceGrant_Step_by_Step_Guide.md`. SHA-256: `042f69fdadd35513cf84d2edf869539f130953885a1681ff3e817fff5daf42ff`. The user's task prompt and the guide are treated as context, not measured results.

Upstream implementation repository URL/commit: **NOT DONE**. No author implementation repository was obtained or executed; the paper's p. 17 data-availability paragraph says additional artifacts are available from the corresponding author on request. No author contact was made. Source identity is pinned by arXiv version and PDF hash. No upstream/native source file was modified. All implementation code is in the new artifact directory.

## Runtime and commands

Observed Python: `3.12.7 (tags/v3.12.7:0b05ead, Oct  1 2024, 03:06:41) [MSC v.1941 64 bit (AMD64)]`. Pydantic `2.12.5`, pydantic_core `2.41.5`, pytest `9.0.2`, pypdf `6.14.2`. [requirements.lock](requirements.lock) records direct/transitive dependencies; [pins.json](pins.json) records the full inherited installed-package inventory, runtime path, platform and input hashes. `logs/11_renderer_version.output.txt` records Poppler's version. No packages were downloaded. Pytest plugin autoload was disabled with `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`.

Working directory for the logged commands: `C:\Users\prath\Downloads\RPaper\tracegrant_task_d_20261014`. `run_logged.ps1` stores structured executable/argument arrays, stdout/stderr and exit codes. The PDF-fetch command files record the URL and destination operation; the PowerShell wrapper resolved destination paths inside this directory. Exact extraction renderer invocations are printed in log 03. Raw outputs and JUnit XML remain saved. Initial read-only discovery commands and the unsuccessful bundled-dependency metadata tool request were not captured in full raw filesystem logs; the discovery tool output was truncated. **NOT DONE:** complete raw recording of that early discovery. All implementation/test/case execution commands below were logged.

| Run | Command (JSON executable/argument array or saved fetch invocation) | Exit code | Output |
| --- | --- | --- | --- |
| 01_fetch | `Invoke-WebRequest -Uri https://arxiv.org/pdf/2608.21126v1 -OutFile sources/tracegrant-2608.21126v1.pdf -TimeoutSec 60` | 1 | [raw output](logs/01_fetch.output.txt) |
| 02_fetch_retry | `Invoke-WebRequest -Uri https://arxiv.org/pdf/2608.21126v1 -OutFile sources/tracegrant-2608.21126v1.pdf -TimeoutSec 60` | 0 | [raw output](logs/02_fetch_retry.output.txt) |
| 03_extract | `["python", "implementation/extract_paper.py"]` | 0 | [raw output](logs/03_extract.output.txt) |
| 04_venv | `["python", "-m", "venv", "--system-site-packages", ".venv"]` | 1 | [raw output](logs/04_venv.output.txt) |
| 05_venv_without_pip | `["python", "-m", "venv", "--without-pip", "--system-site-packages", ".venv"]` | 0 | [raw output](logs/05_venv_without_pip.output.txt) |
| 06_pins | `["./.venv/Scripts/python.exe", "-m", "implementation.pin_environment"]` | 0 | [raw output](logs/06_pins.output.txt) |
| 07_examples | `["./.venv/Scripts/python.exe", "-m", "implementation.example_contracts"]` | 0 | [raw output](logs/07_examples.output.txt) |
| 08_pytest | `["./.venv/Scripts/python.exe", "-m", "pytest", "-v", "--junitxml=logs/08_pytest.junit.xml"]` | 0 | [raw output](logs/08_pytest.output.txt) |
| 09_pytest_final | `["./.venv/Scripts/python.exe", "-m", "pytest", "-v", "--junitxml=logs/09_pytest_final.junit.xml"]` | 0 | [raw output](logs/09_pytest_final.output.txt) |
| 10_synthetic_cases | `["./.venv/Scripts/python.exe", "-m", "implementation.run_artifact"]` | 0 | [raw output](logs/10_synthetic_cases.output.txt) |
| 11_renderer_version | `["C:\\Users\\prath\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\native\\poppler\\Library\\bin\\pdftoppm.exe", "-v"]` | 0 | [raw output](logs/11_renderer_version.output.txt) |
| 12_report | `["./.venv/Scripts/python.exe", "-m", "implementation.make_report"]` | 0 | [raw output](logs/12_report.output.txt) |
| 13_audit | `["./.venv/Scripts/python.exe", "-m", "implementation.audit_artifact"]` | 0 | [raw output](logs/13_audit.output.txt) |
| 14_table_render | `["./.venv/Scripts/python.exe", "-c", "from implementation.run_artifact import render_saved_tables; render_saved_tables()"]` | 0 | [raw output](logs/14_table_render.output.txt) |

The initial sandbox fetch failed with `No such host is known`; the approved retry fetched only the pinned arXiv PDF. The first venv bootstrap failed because ensurepip returned a nonzero status. Its deeper cause is **NOT DONE**; bootstrap succeeded using `--without-pip --system-site-packages`. The final pytest process exited 0 and produced passing JUnit results, but stderr included an ignored `pyreadline3` Console destructor OSError at interpreter shutdown. The exact traceback is preserved; investigation of that environment anomaly is **NOT DONE**. It is not classified as a defense result or silently discarded.

## Valid cases (denominator 5)

Five hand-authored valid Contract fixtures: bill payment, unique owner report, fixed file deletion, budgeted payment retry and output/exemption. Receipt/output-backed completion matched the declared expected outcome in **5/5** cases. Native tool results are synthetic runner fixtures; no real payment, email or deletion occurred. The retry case includes an explicitly failed first result and verifies only the subsequent successful attempt.

See [valid_cases.json](results/valid_cases.json) and its separate table in [TABLES.md](results/TABLES.md).

## Invalid Contracts (denominator 4)

Four distinct invalid fixtures were rejected by the expected predicate: unknown tool (WellFormed), dependency cycle (ControlSafe), missing recipient binding (FlowSafe), and unobservable completion condition (VerifySafe). Matched rejection outcomes: **4/4**. Additional tests exercise ScopeSafe, unreachable hard nodes, disjoint dynamic scopes and evidence lacking a prerequisite relation. These tests are not added to the case denominator.

See [invalid_contracts.json](results/invalid_contracts.json). The optional-recipient fixture is kept in the exploratory table rather than also counted here.

## Invalid inputs (denominator 5)

Boolean/string amounts, an unknown argument, a missing argument and a structurally malformed Contract produced their expected DENY or validation-error outcome: **5/5**. Validation errors are distinct from authorized effects and from native crashes.

See [invalid_inputs.json](results/invalid_inputs.json).

## Exploratory probes (denominator 2)

| Probe | Profile | Observed admission/authorization and completion | Interpretation |
| --- | --- | --- | --- |
| Poisoned designated bill | complete | ALLOW; matching synthetic receipt verified; final gate accepted | Negative security result: authentic provenance does not prove field truth. |
| Unbound optional rent recipient | diagnostic_coverage_gap | id/amount proved; recipient unbound; ALLOW; matching synthetic receipt verified; final gate accepted | Negative security result in an intentionally incomplete profile. The complete static profile rejects this same Contract with FlowSafe. |

Both probes reached receipt-backed completion (**2/2 synthetic probes**). This is not benchmark ASR. The default's optional-coverage check addresses a missing proof; a separate unit test shows that binding recipient to a poisoned notice still permits the poisoned value. It cannot repair semantic authenticity by itself.

See [exploratory_probes.json](results/exploratory_probes.json) and [raw traces](results/traces.jsonl). Every probe is distinct from the valid-case and control denominators.

## Controls (denominator 9)

Wrong tool, wrong derived recipient, out-of-order effect, exhausted budget, risky payload, certificate replay, dispatch argument drift, failed native result and unmet postcondition matched their declared DENY/PROOF-GAP/STEP_UP_AUTH/false transition outcomes: **9/9**. None closed the final gate. These are direct synthetic candidates and faults, not end-to-end agent attacks. The two-thread one-shot test remains in the unit-test denominator only.

See [controls.json](results/controls.json).

## Crash controls (separate denominator 1)

One expected protected-runner exception was observed. Its certificate and budget were consumed, the effect remained incomplete, and the final gate stayed closed. Successful defenses credited to this crashed run: **0/1**. This crash is neither a valid completion nor an attack-rejection success.

See [crash_controls.json](results/crash_controls.json).

## Discrepancies against the supplied guide and reported numbers

1. The guide's Step 4 line-by-line table labels its scope/verification row `CheckScope OR CheckVerification`. Algorithm 1 line 14 in the paper rejects when either check fails, so acceptance requires both checks. The guide's own preceding flow diagram uses AND. This implementation requires both.
2. The guide says the consequence of static rejection is unstated in the pasted text. Paper p. 6 explicitly says a rejected candidate creates no executable Contract. `establish` raises on rejection.
3. The guide's Step 14 says it does not discuss a code/artifact URL. There is no URL in the paper's data-availability paragraph, but it does state that additional implementation configurations and trajectories are available on request. No repository/commit or native Contracts can be claimed here.
4. The paper's normative FlowSafe description and Section 6.3 require coverage of every runtime authority argument, whereas Section 5.7 reports a Contract missing optional-recipient coverage. The default follows the complete requirement; diagnostic mode illustrates the reported gap. These profiles are separated in results.
5. The guide explicitly labels its bill Contract as illustrative. This artifact's bill/rent Contracts are also synthetic, simplify the paper's balance and scheduled-transaction observations, and are not copied native Contracts.
6. The paper reports 97 statically accepted compiled Contracts. This task has ten hand-authored examples: five ordinary valid fixtures, four invalid fixtures and one exploratory gap fixture that the complete profile rejects. No Valid Contract Rate comparison is appropriate.
7. The supplied guide reports end-to-end rates for 949 AgentDojo attacks, 400 ASB attacks and 100 white-box attacks (including two successes), plus utility, ablations and stress results. Those benchmark runs are **NOT DONE**. This artifact's small synthetic tables have different denominators and no native oracle. Differences in TSR/UUA/ASR or fidelity to those reported numbers are **NOT DONE / not comparable**; no numerical deltas are calculated between unrelated datasets.

## What could not be done

- LLM compiler: intentionally **NOT DONE**, as requested. Only hand-authored Contract input and an Eq. 1 IR-shape test are supplied.
- General Eq. 10 semantic soundness or a formal proof: **NOT DONE**. Static acceptance and finite candidate tests do not prove user-intent fidelity.
- Author-code/repository/commit recovery, exact native schemas/Contracts, native trajectory replay, AgentDojo/ASB benchmarks and reported-number reproduction: **NOT DONE**. The author artifact was not available as a supplied file or repository.
- Real query/native service adapters, semantic field authentication, an interactive step-up channel, signed receipt transport, persistent/distributed atomicity and restart recovery: **NOT DONE**, outside this explicitly limited interpreter and harness.
- General conditional graph/expression languages, multi-source bill/balance computation, domain-authenticated exemption verification and semantic output judging: **NOT DONE**. The supported subset is specified in the assumptions.
- Complete early-discovery raw logs, isolated wheel bundle and deeper diagnosis of the setup/console anomalies: **NOT DONE**. The artifacts preserve the available actual setup/test logs and inventory.

All operational choices and trust assumptions are in [ASSUMPTIONS.md](ASSUMPTIONS.md). Results/counts were calculated in Python, not inferred from prose. `implementation/audit_artifact.py` independently checks result denominators and arithmetic, actual JUnit counts, source preservation, Contract count and the final file-hash inventory. The audit returned PASS; see [audit.json](audit.json), [raw audit output](logs/13_audit.output.txt), and [SHA256SUMS.json](SHA256SUMS.json). The hash manifest excludes caches/venv and self-referential audit outputs.
