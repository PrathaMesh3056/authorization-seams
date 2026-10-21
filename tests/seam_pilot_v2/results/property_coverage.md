# Property coverage of the seven-arm matrix

All cells are measured on the frozen 80-case set (40 attack / 40 benign). Numbers are
from `results/raw_metrics.json` and `results/traces.jsonl`.

| Property | What the matrix measures | Result by arm |
|---|---|---|
| Principal chain | Principal/task rebinding attack (`principal_rebind` x4) | arm2/arm5 leak 4 each (part of their 24/40 attack totals); arm1/3/4/6/7 deny all |
| Attenuation | Resource widening via a role scope with an extra resource (`resource_widen` x4); action-type widening untested | all seven arms deny the widened resource (`narrow` intersects R); 0 leaks |
| Stale/widened/context-free authority | Expired (`expired_delegation` x4), revoked (`revoked_envelope` x4), principal/task (`principal_rebind` x4) | arm2/arm5 leak 12; arm4 leaks 0 of these; arm1/3/6/7 deny all |
| Confused deputy | Recipient substitution (`recipient_substitution` x4) and omitted forbidden default (`omitted_forbidden_default` x4) | all seven arms deny all 8; M0 catches both via canonicalization + scope-derived BIND constraints |
| Aggregation/inference | Prohibited composition after a confidential read (`composition_history_loss` x4), marker exfiltration counted | arm2/arm5 leak 4 each, with 4 marker-bearing external effects each; arm4 leaks 4 (reset control); arm1/3/6/7 zero |
| Budget/replay | Repeated calls over the cumulative ceiling (`repeated_calls` x4) and pre-handoff budget (`budget_reset` x4) | arm2/arm5 leak 8 each (4 repeated + 4 budget); arm4 leaks 8 in total (4 composition + 2 repeated + 2 budget_reset); arm1/3/6/7 zero |
| False denial | Paired benign cases on the same axes | arm7 20/40; all other arms 0/40 |
| Audit completeness | Gate evidence and receipts recorded per event | arm6 records admitted `apc_state` evidence for every downstream admission; receipt failures: arm2 4, arm5 4, arm6 4, all other arms 0 |
| Completion integrity | Unsatisfiable VERIFY (`unsatisfiable_verify` x4): admission vs receipt | arms 2/5/6 admit and fail the receipt (4 each); arm1/3/4 admit with no receipt model (not comparable); arm7 denies at translation (fail-closed) |
| Latency | Warm admission path, 1000 samples/arm | see `results/latency.md`; measurement includes shadow APC + contract establishment for concatenated arms |
| Determinism | 10-pair replay, canonical projection excluding wall-clock | 10 pairs semantically identical |

Coverage gaps: (1) the action-type half of C1a is untested because no frozen case uses a
tool present in root A but absent from the handoff A; (2) the oracle is our own and only
two of its rules have mutation failure controls; (3) M2's evidence is trusted harness
input, so arm6 is an upper bound on what evidence can close, not a deployment result.

