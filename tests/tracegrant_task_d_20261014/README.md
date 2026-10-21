# TraceGrant Task D research artifact

Independent Python 3.12 / Pydantic v2 implementation of the deterministic Contract, Ledger and task-effect checks described by TraceGrant arXiv:2608.21126v1. Hand-authored Contracts only; no LLM compiler or real service invocation.

Start with `REPORT.md`, `ASSUMPTIONS.md`, and `results/TABLES.md`. `pins.json` records the paper/guide hashes and actual runtime. The code is in `implementation/`, separate from the untouched copied sources. Ten Contracts are in `examples/`; the registry is synthetic.

## Harness interface

```python
from implementation.engine import establish, admit_evidence, check_call
from implementation.models import Contract, Registry, CallRequest, EvidenceRecord

# Contract and Registry can be loaded with model_validate_json(...).
state = establish(contract, frozen_registry, session="harness-session")
accepted, state = admit_evidence(protected_query_result, state)
decision, new_state = check_call(
    CallRequest(tool="send_money", arguments={"recipient": "...", "amount": 250}),
    state,
)
print(decision.code, decision.checks, decision.missing)
state = new_state
```

`check_call(request, state) -> (Decision, RuntimeState)` takes Pydantic models. `Decision.code` is ALLOW, DENY, PROOF-GAP or STEP_UP_AUTH. It includes M/O/P/B/H checks and missing-proof reasons. It returns a copy and does not issue a certificate, invoke a tool, consume a budget, or verify completion. A rejected static Contract cannot establish state. Any change to the frozen Contract or registry raises ValueError.

For effects, use `issue_certificate(request, state, key, now)`, `validate_certificate(cert, request, state, key, now)`, `dispatch(cert, request, state, key, now)`, and `check_receipt(native, cert, state, key)`. Each transition returns new state. `final_gate(state)` checks task closure. `Gateway` wraps certificate issuance and execution in authoritative in-process state, serializes dispatch, and takes a trusted runner callback; inspect `snapshot()` after a fault. Tainted-payload metadata, evidence records, native results, keys, waiver decisions and the state itself are trusted harness inputs, not planner-controlled assertions.

Default complete binding requires every permitted authority argument, including optional ones. Explicit `diagnostic_coverage_gap` mode exists only for the optional-recipient probe. It deliberately models the incomplete coverage in the reported white-box path. Binding a poisoned field still cannot authenticate it.

## Re-run in this workspace (PowerShell)

The saved venv uses the installed Python 3.12.7 packages; no download is required. This run pinned Pydantic 2.12.5 and pytest 9.0.2. See `requirements.lock` for dependencies and `pins.json` for the full inherited package inventory.

```powershell
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'
./run_logged.ps1 -Name replay_pytest -Executable ./.venv/Scripts/python.exe -Arguments @('-m','pytest','-v','--junitxml=logs/replay_pytest.junit.xml')
./run_logged.ps1 -Name replay_cases -Executable ./.venv/Scripts/python.exe -Arguments @('-m','implementation.run_artifact')
```

The case runner reads the saved `logs/09_pytest_final.junit.xml` for the original unit-test summary. To regenerate that summary from a new unit-test run, use the name `09_pytest_final` and the same XML destination. Each command records its actual invocation, merged stdout/stderr and exit code under `logs/`. Re-running the case runner replaces result tables and random certificates; archive the original results first if you need immutable history.

For a new installation on another machine, use Python 3.12 and install `requirements.lock` into a fresh environment after reviewing the dependencies. This artifact did not download or package wheels. Exact environment and Windows-only console anomalies are recorded in the report.
