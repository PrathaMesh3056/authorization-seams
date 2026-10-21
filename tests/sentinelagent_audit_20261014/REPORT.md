# SentinelAgent reproduction audit — Task C

Audit date: 14 October 2026 (Asia/Calcutta). Repository: https://github.com/ksrpatil/sentinelagent . Pinned commit: `b7b1add07b7485e99aa3b91882a3f8f879f2e357`. MIT license was read. Upstream tracked files remain unchanged; SHA-256 inventory is in `runs/upstream_sha256.json`.

## Main findings

The local HTTP reproduction matches the supplied combined result: **150/150 attacks blocked, 0/366 benign cases blocked**. P6 alone is **130/150 = 86.6667%**, matching 86.7% after rounding. **P7 alone is 60/150 = 40.0%, not 13.3%**. P7 adds 20 unique catches after P6, equal to 13.3333%; 40 attacks are caught by both checks. This is a measured difference between a standalone ablation and incremental coverage.

All 516 native scenarios were extracted into `scenarios.json`, including original scenario scope, effective token scope, manifest entries, API call, tags, label-derived expected outcome, and independently observed catching properties. No scenario intent text exists in this builder; it is recorded as null. No P2 result is invented from names or category labels.

## What ran and where the evidence lives

Commands, exact argv, sanitized environments, start/end timestamps and exit codes are in [COMMANDS.md](COMMANDS.md) and `logs/*.command.json`. Raw outputs are in separate `*.stdout.log` and `*.stderr.log` files. Clone failures and the successful clone are saved in the two setup transcripts. Own code is under `audit/`; generated artifacts are outside `upstream/`.

The fresh isolated `.venv` uses Python **3.12.7**. Initial venv creation failed because sandbox temporary directories were not writable; using `tmp/` inside the audit fixed it. The initial requirements attempt failed on sandbox DNS. The network-enabled installation reached the PyTorch wheel but hit a 1,200-second audit deadline. NumPy **2.5.4** was then installed from a complete downloaded wheel, offline. Its exact wheel hash is recorded. The requirements use lower bounds, not exact version pins; resolved and installed versions must be distinguished.

An explicitly separate `.venv_local` uses `--system-site-packages` as a fallback; its existing runtime initially included NumPy **2.3.2**, torch **2.14.0**, sentence-transformers **6.0.1**, transformers **5.17.0** and huggingface_hub **1.5.0**. `fallback_freeze.stdout.log` records the full initial environment. This reuse is an assumption and a departure from a newly installed isolated package environment. Do not attribute its results to the fresh isolated `.venv`.

Native HTTP scripts initially failed because the sandbox denied outbound loopback sockets. Two scripts swallowed those errors and called them blocked attacks. Those runs are **infrastructure failures**, excluded from defense rates regardless of exit code. The first permissive local DAS attempt then timed out because Windows tried IPv6 before the IPv4 server. Subsequent `audit/offline_entry.py` runs permit only loopback sockets and resolve `localhost` to `127.0.0.1`. This changes connection setup, not native checking logic; it invalidates comparisons of HTTP latency to the paper. Native files were not patched. The successful native DAS script log is `sentinelagent_das_prototype_ipv4.stdout.log`.

## Valid benchmark attack cases — denominator 150

| Configuration | Blocked attacks | TPR |
|---|---:|---:|
| P6 | 130/150 | 86.6667% |
| P7 | 60/150 | 40.0000% |
| P6+P7 | 150/150 | 100.0000% |

Benign outcomes have their own table and denominator of 366 below. Source: `runs/benchmark_summary.json`, backed by 1,032 saved HTTP request/response records in `runs/benchmark_http_responses.json` and the successful native log.

| Category | Cases | P6 blocks | P7 blocks | Combined blocks |
|---|---:|---:|---:|---:|
| A | 20 | 20 | 20 | 20 |
| B | 20 | 20 | 0 | 20 |
| C | 20 | 0 | 20 | 20 |
| D | 20 | 20 | 0 | 20 |
| E | 156 | 0 | 0 | 0 |
| F | 30 | 30 | 0 | 30 |
| G | 20 | 20 | 0 | 20 |
| H | 20 | 20 | 20 | 20 |
| I | 30 | 0 | 0 | 0 |
| J | 180 | 0 | 0 | 0 |

Attack categories are A/B/C/D/F/G/H. Benign categories are E/I/J. Counts sum to 150 + 366 = 516 in executed arithmetic. Categories E/I/J contain zero attacks: their attack TPR is **not applicable**, rather than 0/0 = 0%. Each JSON scenario ID is unique, but only **163** distinct (declared scope, API call, output tags) tuples exist, and only **152** distinct effective (API call, tags) tuples. These are defined operational duplicate counts, not claims that all semantic scenarios are identical.

### Benchmark scope and limitations

- The native evaluator uses one child token with both `read_records` and `query_eligibility` for every case; it does not use each scenario's `scope`. All 30 category-F rows have a different declared scope, preserved in the extraction alongside effective scope.
- Category G does not replay or expire a token. It supplies unauthorized API strings as a replay stand-in. A genuine signed-expired-token probe is reported separately below.
- Category B has no natural-language paraphrase field. Categories E and J reuse fixed calls and tags across domain names; J's rows do not implement 30 separate mutable multi-agent workflows.
- P6 checks a method/endpoint string, not an executed government API or its parameters. P7 checks supplied tag strings, not actual response content or independent semantic tagging. The two checks are called even if P6 blocked; raw standalone P7 results are therefore available.
- The DAS prototype never invokes an IntentVerifier. Its delegation method does not enforce P2. Neither the fine-tuning script nor the simulation supplies a 516-case P2 evaluation, and the simulation always loads the off-the-shelf model ID.

## Other valid attack suites — separate denominators

| Suite | Blocked attacks | Attack denominator | Notes |
|---|---:|---:|---|
| Native black-box red team | 30 | 30 | 20 API + 10 output-tag attacks |
| Independent red team, strict audit recount | 45 | 45 | 42 direct attacks + 3 malicious second chain steps |
| Robustness, expected-block cases | 16 | 16 | Scope, API/tag, lifecycle and isolation cases; not all are natural-language attacks |

The independent native script prints `Blocked: 42/45 (93.3%)` and `Evaded: 0/45`, then says all 45 blocked. Its per-category counts total 45 blocks. It incorrectly subtracts three from `total_blocked`, even though the three benign chain steps were already excluded by being allowed. `audit/independent_redteam_counts.py` replayed the same generators with strict HTTP status/response checks and observed **45/45** blocks. Raw rows and separate controls are in `runs/independent_redteam_*`.

## Benign and positive controls — separate denominators

| Control set | Correctly allowed | False positives | Own denominator |
|---|---:|---:|---:|
| DelegationBench E/I/J, P6 | 366 | 0 | 366 |
| DelegationBench E/I/J, P7 | 366 | 0 | 366 |
| DelegationBench E/I/J, P6+P7 | 366 | 0 | 366 |
| Native black-box controls | 10 | 0 | 10 |
| Independent named controls | 14 | 0 | 14 |
| Independent benign first chain steps | 3 | 0 | 3 |
| Robustness expected-allow cases | 13 | 0 | 13 |
| Valid HTTP request after malformed inputs | 1 | 0 | 1 |

Native robustness prints 29/29 passing checks: 16 expected-block and 13 expected-allow. This is a conformance pass rate, not 29 attack detections. Despite its header, the native suite does not exercise missing-field or wrong-type JSON. Own invalid-input cases are kept separate.

## Invalid inputs — own denominator 6

| Input | HTTP handler outcome | Counted as defense success? |
|---|---|---|
| Missing API method | KeyError; connection closed | No |
| Null API method | AttributeError; connection closed | No |
| Integer endpoint | AttributeError; connection closed | No |
| Null tags | TypeError; connection closed | No |
| Unhashable tag object | TypeError; connection closed | No |
| Integer scope | TypeError; connection closed | No |

**6/6 requests caused a handler exception and RemoteDisconnected; 0/6 returned a structured rejection.** The server remained available and accepted the separate valid control (1/1). These are handler failures, not full server process crashes and not successful defenses. Requests and client errors: `runs/invalid_inputs.json`. Server traceback evidence: `logs/token_invalid_probes.stderr.log`.

## Token verification at code level

In `sentinelagent_das_prototype.py`, `_canonical()` JSON-serializes `id`, `src`, `dst`, sorted `scope`, sorted manifest keys and operation lists, sorted `policy`, `parent_hash`, `expiry`, and `intent`, using `json.dumps(..., sort_keys=True)` with its default JSON formatting. `_sign()` applies HMAC-SHA256 using the literal prototype key `DAS_SECRET`; the hexadecimal digest is compared with `hmac.compare_digest` in `verify_signature()`. `token_hash()` is SHA-256 of UTF-8 `(canonical string + signature)`. `to_dict()` uses different external names for some fields: an independent verifier must rebuild the signed representation, not hash `to_dict()` directly.

A different implementation needs the **same symmetric HMAC key**, exact canonical fields/serialization, UTF-8 encoding and HMAC/SHA-256/digest conventions to verify this signature locally. Key possession also permits minting signatures. A hash alone is insufficient. Alternatively, it can ask the trusted DAS to validate stored state, but these HTTP endpoints accept a token ID and look up the stored token; they do not verify a presented serialized bearer token. Full authorization also requires consistent token store, revocation state, parent lookup, and expiry policy. There is no asymmetric public verification key here.

The simulation uses a **different** hard-coded HMAC key and pipe-delimited `to_bytes()` serializer, so it is not signature-compatible with the HTTP prototype. It defines a verification helper, but `request_delegation()` and `authorize_tool_call()` do not call it. The AiTM test runner calls it directly; passing those tests does not prove runtime signature enforcement in all paths.

The fault-tolerance variant uses three different symmetric HMAC keys and counts at least two valid replica MACs. This is a local simulation of independently keyed MACs, not an implemented distributed threshold cryptographic protocol. A verifier needs replica keys, matching canonical JSON and the threshold configuration, or trusted online replica verification.

### Exploratory token probes — own denominator 2

| Probe | Observation | Access/fixture assumption |
|---|---|---|
| Mutate `output_schema.permitted` after signing | Previously rejected output tag becomes allowed; signature and token hash stay unchanged | In-process stored-token mutation; no HTTP schema-update endpoint exists |
| Legitimately signed expired token | New delegation rejected by C5; permitted P6 API and P7 output both allowed | Expiry moved into the past and token re-signed with the native prototype key |

`output_schema` and `revoked` are not in the prototype's signed canonical payload. P6/P7 check revocation and signatures but do not check expiry. The schema probe establishes a signature-coverage gap under the stated access assumption; it does not claim an unauthenticated remote schema exploit. `runs/token_exploratory.json` preserves before/after observations.

### Signature controls — own denominator 2

The unchanged token had a valid signature and permitted API/tag checks passed. Mutating signed scope invalidated the signature and P6 rejected it. These controls are in `runs/token_controls.json` and are not added to benchmark denominators.

## Fault tolerance — nine scenario checks

Native output reports all **9/9** scenario checks passed. Case-level rows must not be confused with token attempts. Actual observed subchecks: healthy 50/50 issued and verified; one crash 50/50; two crashes 0/20 issued; one Byzantine 50/50 verified; one partition 50/50; Byzantine+crash 20/20 issued but **0/20** verified; key rotation three boolean checks; scope-under-fault one permitted and one rejected scope check; timing 100 issuance calls each in healthy/degraded states.

The native summary prints Byzantine+crash `verified=0/0`; that zero denominator is an expected-success field, not the number of attempts. The script counts received signatures before issuing and checks their validity later, so the mixed faulty case still issues 20 unusable tokens. Its last timing row reports verification without actually invoking verification in those loops. It claims P4/P6 preservation, but ThresholdDAS contains no parent hash chain or manifest checks. Therefore 9 passing checks support these modeled local conditions only; they do not establish production availability, general Byzantine safety, distributed agreement or P4/P6 preservation.

## Theorem script — five returned checks

The unchanged Python theorem script ran and returned **5/5** passing functions. The native summary calls them verified theorems; this audit records passing executable checks only. T1 marks seven examples exploitable while largely hard-coding other-properties-hold. T2 counts eight manually labeled ambiguous texts. T3 compares seven hand-written damage sets to a 12-action set. T4 enumerates **126/126** proper nonempty subsets using a stipulated one-property/one-action prevention mapping. T5 hard-codes property booleans and counts a fixed 50-case schedule: 20 disjoint + 20 read-shared + 5 notified writes = **45/50** designated safe, with 5 unnotified writes designated at risk.

These checks neither execute the full DAS under the asserted conditions nor prove a general impossibility or composition theorem. T4 prints stale `35/20` triple and `35/15` quadruple denominators; correct combinations for seven properties are 7,21,35,35,21,7, summing to 126. Arithmetic is saved in `runs/static_inventory.json` and `runs/arithmetic_checks.json`. No novelty or priority inference is drawn from native claims.

## Supplied numbers and source comparison

| Supplied target | Audit disposition |
|---|---|
| 516 = 150 attacks + 366 benign; given category counts | Reproduced exactly from native builder |
| P6+P7 100% TPR; 0% FPR | Reproduced: 150/150; 0/366 |
| P6 only 86.7% | Reproduced after rounding: 130/150 |
| P7 only 13.3% | Discrepancy: standalone 60/150 = 40%; incremental-only 20/150 = 13.3% |
| P2 off-the-shelf 13.3% on 516 | **NOT DONE**: builder has no natural-language intents and HTTP harness never runs P2 |
| P2 fine-tuned 88.3% on 516 | **NOT DONE**: no 516-case P2 harness or intents; training/CV script uses a different 190-example dataset |

The paper's [Table VI](https://arxiv.org/html/2604.02767v1#S7.T6) lists the supplied ablations; its fine-tuning discussion separately uses 190 examples. The repository's literal training data contains 65 entailment, 65 neutral, and 60 malicious labels. Its comment saying 200 examples is stale. 88.3% corresponds to 53/60 rounded; it is not a possible one-decimal single aggregate proportion out of 150. A macro-average or repeated-run rate could have another interpretation, but no such 516-case measurement is present in the inspected harness. Training-set sanity checks must not be reported as held-out performance.

## Optional own P2 paraphrases — exploratory

Ten own texts include verify/calculate/generate and contain no substring from the native malicious-keyword set. Their harmful interpretation is specified separately in `runs/p2_branch_exploratory.json`; labels are investigator assumptions, not model outputs. The native function was called without loading models, using controlled vectors and each forced NLI label. **10/10 texts passed for all three labels (30/30 branch paths)**; a contradiction was changed to neutral by the benign-indicator override. Two separate branch controls blocked (2/2): a contradiction with no benign indicator, and a text containing an explicit malicious keyword despite a benign verb.

These are deterministic branch probes, **not real NLI inference results**. The paper calls this Layer 3; the inspected code places it inside the contradiction branch and comments it as Layer 2b. The code tests `any` benign substring plus no malicious substring; it does not require the entire subtask to contain only benign terms. Its stored cosine threshold is never used to reject a subtask. This explains why changing the NLI weights alone cannot reject these ten inputs through this function. Real-model exploratory results, if obtained, are documented in the status appendix, with their own denominator.

## Arithmetic and preservation checks

All counts, percentages, combinations and operational duplicate counts above were computed by audit code. Raw numerical objects are retained. Wilson intervals for the combined result are in `runs/arithmetic_checks.json`; they describe these fixed constructed cases, not external-world generalization. `git status --porcelain` and tracked-byte SHA-256 comparisons verify source preservation. Final pins, installed-package snapshots, downloads and missing work are in the status appendix below. Assumptions are explicitly listed in [ASSUMPTIONS.md](ASSUMPTIONS.md).

## Final execution status and missing work

| Requested item | Status | Exact disposition | Evidence |
|---|---|---|---|
| DAS prototype | **DONE** | 150/150 attacks blocked; 0/366 benign blocked | [log](logs/sentinelagent_das_prototype_ipv4.stdout.log) |
| Simulation v1 | **NOT DONE** | Initial missing dependencies; fallback eventually raised SafetensorError for truncated NLI file. No 100-case results produced. | [log](logs/fallback_simulation_complete_models.stdout.log) |
| Theorem Python script | **DONE** | 5/5 returned checks; limitations and stale denominators described above. | [log](logs/sentinelagent_theorems_initial.stdout.log) |
| Native red team | **DONE** | 30/30 attacks blocked; controls 0/10 false positives. | [log](logs/sentinelagent_redteam_loopback.stdout.log) |
| Independent red team | **DONE** | 45/45 corrected strict count; 0/14 named control false positives; 0/3 chain control false positives. | [log](logs/independent_redteam_counts.stdout.log) |
| Native robustness | **DONE** | 29/29 conformance checks; controls and expected-block cases separated above. | [log](logs/sentinelagent_robustness_loopback.stdout.log) |
| Fault tolerance | **DONE** | 9/9 modeled scenario checks; no production distributed proof inferred. | [log](logs/sentinelagent_fault_tolerance.stdout.log) |
| NLI baseline / fine-tuning / cross-validation on 190 | **NOT DONE** | Initial missing sentence-transformers; fallback training dependencies timed out; final attempt refused invalid weights. No baseline, trained, CV or training-set metric obtained. | [log](logs/fallback_nli_finetune.stdout.log) |
| P2 on DelegationBench v4 | **NOT DONE** | No scenario intents or implemented P2 evaluation in 516-case harness. No mapping from the separate 190-example training set is assumed. | [log](logs/static_inventory.stdout.log) |
| Optional own real-model paraphrase inference | **NOT DONE** | First attempt lacked cached NLI; later attempt stopped after weight integrity failure. No empirical classifier rate. | [log](logs/fallback_p2_complete_models.stdout.log) |
| Optional own deterministic P2 branch probes | **DONE** | 10 own attack texts pass all 30 forced-label paths; 2 separate controls block. | [log](logs/p2_branch_exploratory.stdout.log) |
| Complete isolated requirements installation | **NOT DONE** | DNS failure; 1,200-second timeout; resumed PyTorch download canceled after invalid model was established. Isolated venv contains pip and NumPy only. | [log](logs/install_requirements_resume.stdout.log) |
| Complete fallback requirements installation | **NOT DONE** | No-index install found existing core ML libraries but could not find datasets; attempted training-only dependencies then timed out. | [log](logs/fallback_install_requirements.stdout.log) |
| TLA+ / 2.7-million-state verification | **NOT DONE** | Java and tla2tools.jar absent; shell verification was not run. It writes cfg, so any future run must use a separate copied working directory. | [log](logs/final_inventory.stdout.log) |
| Live LangChain and sentinelagent_llm_* | **NOT DONE** | Intentionally excluded exactly as instructed; no OpenAI API call or key. | [log](logs/final_inventory.stdout.log) |

### Model pins and integrity

| Model | Revision | Received weight bytes | Expected framing bytes | Status |
|---|---|---:|---:|---|
| sentence-transformers/all-MiniLM-L6-v2 | `1110a243fdf4706b3f48f1d95db1a4f5529b4d41` | 90868376 | 90868376 | complete |
| cross-encoder/nli-MiniLM2-L6-H768 | `b95119ce93d3e065de6214e38cd4a97b0f2f2c6d` | 105337812 | 328499560 | FAILED_INCOMPLETE_WEIGHTS |

The embedding weights validate in size. The NLI transfer ended early: **105,337,812 / 328,499,560 bytes**. The download process originally printed completed because its streaming loop reached EOF without checking the required tensor data length. Independent safetensors framing validation caught the incomplete body and corrected `runs/model_downloads.json`; original raw output is preserved. `runs/model_validation.json` is the authoritative integrity result. SHA-256 values record the received bytes, not an assertion that the truncated file is a valid model. The fallback native simulation independently raised `SafetensorError: incomplete metadata, file not fully covered`. The downloader now checks both Content-Length and safetensors framing for any future rerun. Its original version is saved under `audit/source_versions/download_models_original.py`.

The full requirement installation was not completed. The isolated NumPy wheel hash and downloaded sentence-transformers wheel hash are in `runs/recovered_wheels.json`; downloading the latter did not install it. Final isolated and fallback version inventories are in `runs/*_final_environment.json`; full exact freeze outputs are in `requirements.isolated.lock.txt` and `requirements.fallback.snapshot.txt`. These files pin observed environments, not an assertion that the upstream complete requirements were satisfied. Failed resolution attempts and cancellation provenance remain in raw logs and `runs/setup_cancellation.json`.

No API-key-dependent program was run. TLA+ was not run, and no model-checking state count or invariant result is credited. Source preservation and required JSON fields were checked in code (`runs/final_validation.json`). The DAS's v3 result banner and 216-case docstring are stale despite the 516-row builder; they are preserved in raw logs and are not used as denominators.
