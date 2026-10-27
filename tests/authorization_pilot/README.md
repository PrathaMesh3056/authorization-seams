# APC / Progent authorization handoff pilot

The completed empirical manuscript is `paper/MANUSCRIPT_REVISED.md`, with the
canonical named-author PDF at
`paper/drafts/MANUSCRIPT_DRAFT_2026-10-26.pdf` and the standalone LaTeX export
at `paper/latex_export/`. Read `docs/RESEARCH_STATUS.md` for the evidence
boundary and final validation. The canonical PDF is a native XeLaTeX build;
the earlier ReportLab review rendering is not part of this package.

This runnable local conformance study uses the authors' implementations at the
commits in `pins.json`. No LLM, API key, or paid inference is required. Native code
is imported directly from unmodified pinned checkouts; it is not reimplemented.

From this directory in PowerShell:

```powershell
./bootstrap.ps1
./.venv/Scripts/python.exe -m seam_pilot native
./.venv/Scripts/python.exe -m seam_pilot run
```

`bootstrap.ps1` downloads source and checker dependencies, then runs the harness
tests. Evaluation workers block socket connections. Setup requires network access;
evaluation does not. The environment uses Python 3.12 and the minimal checker
dependencies in `requirements.lock`, rather than optional model clients/frameworks.

Each run creates a new output directory and refuses to overwrite one. Outputs:

- `REPORT.md`: observed results, attribution, limitations, and research gate.
- `manifest.json`: commits, native source hashes, dataset/outcome hashes, environment
  versions, parameters, timestamps, and completion status.
- `harness_sources/`: frozen runner source, policy protocol and dependency/source
  pins used for that run, so later harness edits do not obscure reproducibility.
- `cases.json` and `traces.jsonl`: frozen 80-case dataset and 560 complete traces.
- `native_checks.json`: native behavior and wrapper/default diagnostics.
- `metrics.json`: paired security/utility and family-level results.
- `counterexamples.jsonl`: reduced replay of every oracle/adapter disagreement.
- `adaptive_probes.jsonl` / `adaptive_summary.json`: bounded feedback probes.
- `latency.json`: 1,000 warmup and 10,000 measured decisions per arm.

Read `PROTOCOL.md` before interpreting results. The lossy configurations are
explicit controls. Passing or failing them does not establish a new vulnerability,
literature novelty, production attack prevalence, or model-level attack robustness.

The completed verified run is in `results/verified/REPORT.md`; the earlier run is
preserved in `results/initial/`. Their matrix outcome hashes are compared in
`results/verification.json`. Setup/verification commands are in `verification.json`.

Harness verification can be rerun offline:

```powershell
./.venv/Scripts/python.exe -m unittest discover -s tests -v
```

The public author repositories and their original licenses remain in `vendor/`.
Progent is a sparse checkout of `secagent` plus root files to avoid downloading its
large benchmark artifacts. Native optional SDK integrations are outside v1.

## Completed callable-policy and MCP follow-up

`PROTOCOL_INTEGRATION.md` specifies the stronger bridge and real in-memory MCP
experiment. It uses a separate environment with FastMCP 2.13.0, matching the
authors' declared range; the frozen minimal v1 environment stays intact.

```powershell
./bootstrap-integration.ps1
./.venv-integration/Scripts/python.exe -m seam_pilot.integration --output results/new-integration-run
./.venv-integration/Scripts/python.exe -m seam_pilot.audit_integration results/new-integration-run
```

The completed runs are `results/integration/` and `results/integration-replay/`.
Independent oracle/effect replay and matching outcome hashes are recorded in
`results/integration-verification.json`. The fixed matrix has 80 cases on four
paths, with 20 additional exploratory diagnostics and nine Progent-only controls.

Wrapped and canonicalized callable policies preserve the tested obligations.
Raw checker/MCP paths admit omitted forbidden defaults on our mock backend; the
same gap occurs without APC. This supports a bounded integration finding, not a
new handoff-specific vulnerability or an affected real deployment. Read the
follow-up report before interpreting these results. MCP latency includes the
round trip and mock effect; direct checker timing uses prebound arguments and
does not measure full wrapper execution. Source hashes and dependency versions
are frozen in each run.
