# Audit assumptions and deviations

1. The public repository default-branch head at clone time is the intended artifact; it was pinned to b7b1add07b7485e99aa3b91882a3f8f879f2e357. It is not asserted to be the exact private artifact used to produce the paper.
2. Windows 11 and Python 3.12.7 are acceptable execution hosts. No claim is made that timing matches the paper's host.
3. Native scenario `is_attack` labels are ground truth for reproduction. Own paraphrase harmful interpretations are explicitly investigator-assigned.
4. Native HTTP effective token scope is used for reproduction even where the declared scenario scope differs. Both are preserved.
5. Expected outcomes are derived from native attack/benign labels; catching properties are measured independently by successful HTTP responses.
6. Default install satisfies upstream version lower bounds when available; exact resolved/installed versions are separately recorded. Binary wheels only were allowed to avoid executing source build scripts.
7. Model aliases are resolved to explicit Hugging Face commit revisions during setup. Only configuration/tokenizer assets and safetensors weights are used. Network is blocked after setup except loopback; no API key or user credential is passed to child processes.
8. `offline_entry.py` maps localhost to IPv4 because native HTTPServer is IPv4. It also wraps socket connect and name resolution to deny non-loopback use. These runtime interventions are outside upstream source and recorded; this is not an OS-level isolation claim.
9. The original 1,200-second package deadline and 300-second local HTTP deadline are audit controls. Timeouts are failures or NOT DONE, never defenses.
10. The separate `.venv_local` fallback reuses installed system packages; it is not a clean isolated package reproduction. Global package versions are frozen and any newly installed fallback dependencies are recorded separately.
11. In-process schema mutation requires trusted-state write access; no remote exploit is inferred from that probe.
12. The expired-token fixture is deliberately signed using the native prototype key after its expiry is put in the past, isolating expiry enforcement from signature invalidity.
13. Native theorem/fault-tolerance pass labels are reported as program checks, not accepted as formal proof or distributed security guarantees. No TLA+ model checking result is inferred.
14. Forbidden live LangChain and sentinelagent_llm_* entry points are never run. Installed API libraries, if any, do not imply an API call was made.
15. The NLI training/CV dataset is a separate 190-example set and is not relabeled as DelegationBench v4. Missing natural-language fields are left null, never reconstructed from attack names.
16. Optional forced-label tests replace only the NLI label provider on an audit-created object and use fixed vectors. They test native branch logic, not classifier accuracy. Actual model inference, if completed, is a separate table.
