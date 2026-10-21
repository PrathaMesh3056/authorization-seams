# Frozen experiment trees

This directory holds the frozen experiments and the pinned inputs their scripts
read. **Keep these folders together at this level and do not rename them** -
every frozen record names them, and the scripts compute their paths from their
own location. The sibling layout is part of the setup.

| Folder | What it is | Status |
|---|---|---|
| `authorization_pilot/` | Shared `seam_pilot` package, pin file, and protocol notes (virtual environments not included) | inputs only |
| `seam_pilot_v2/` | Pilot 1 (APC → TraceGrant) + E1 action extension + resolving tests | frozen, QA-passed |
| `seam_pilot_sentinelagent/` | Pilot 3 (APC → SentinelAgent) + pinned prototype excerpt | frozen |
| `seam_pilot_sa_boundary/` | Boundary experiment (V1/V2 bad-bridge variants) | frozen, QA-passed |
| `sentinelagent_audit_20261014/` | Pinned SentinelAgent prototype excerpt and audit assumptions/report | upstream pinned |
| `tracegrant_task_d_20261014/` | Independent TraceGrant Task D implementation, examples, tests, results | frozen |

## Rerunning

The writers overwrite files under `results/`. Rerun only in a scratch copy; see
`docs/REPRODUCIBILITY.md`. Non-destructive `--check` modes exist for the E1,
SentinelAgent, and boundary runners.

## Upstream inputs

APC and Progent are not redistributed. Fetch their pinned commits with:

```powershell
python scripts/bootstrap_vendor.py
```

The SentinelAgent prototype is included as a small MIT-licensed excerpt at
`sentinelagent_audit_20261014/upstream/` with its license.
