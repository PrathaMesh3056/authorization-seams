# Warm admission latency

Each arm measured on the benign `narrowed_scope-0-b` call, strictly sequential, in one
process. TraceGrant arms synthesize a fresh Contract per call (the mapping's design), so
their numbers include `establish`/static analysis. Tool execution, receipts, IPC and
initialization are excluded.

| Arm | p50 (us) | p95 (us) | p99 (us) | mean (us) | Admitted fraction |
|---|---:|---:|---:|---:|---:|
| apc_alone | 54.00 | 80.20 | 147.20 | 59.12 | 1.00 |
| tracegrant_alone | 1258.55 | 1717.90 | 2273.60 | 1335.62 | 1.00 |
| apc_apc_preserved | 53.70 | 84.50 | 165.50 | 59.27 | 1.00 |
| apc_apc_reset | 54.40 | 78.70 | 167.90 | 59.37 | 1.00 |
| apc_tracegrant_scope_only | 1740.70 | 4017.60 | 5009.20 | 2211.19 | 1.00 |
| apc_tracegrant_retained | 4895.55 | 7274.20 | 8085.40 | 4961.67 | 1.00 |
| apc_tracegrant_fail_closed | 2695.10 | 4177.40 | 4676.20 | 2735.10 | 1.00 |

Warmup 100, samples 1000 per arm.
The fail-closed arm admits this benign case (its translation checks pass), so its latency
is an admission measurement, not a rejection measurement.

