# Provenance of included inputs

## Pinned third-party checkouts

| Name | Source | Commit | Handling |
|---|---|---|---|
| APC (Bounded Agents) | `https://github.com/xmuruaga/bounded-agents.git` | `d31a1ea115a3e97ab972ac8d03f23ef36cf9b653` | Fetched by `scripts/bootstrap_vendor.py`; not redistributed |
| Progent | `https://github.com/sunblaze-ucb/progent.git` | `5be7b63fa96f70bc19b72fbcee81f1c0bcc1a565` | Fetched by `scripts/bootstrap_vendor.py`; not redistributed |
| SentinelAgent | `https://github.com/ksrpatil/sentinelagent` | `b7b1add07b7485e99aa3b91882a3f8f879f2e357` | MIT excerpt included under `sentinelagent_audit_20261014/upstream/` |
| TraceGrant paper | arXiv:2608.21126v1 | n/a | Referenced; PDF and extracted text not redistributed |

## What was copied and what was not

Copied byte-for-byte from the working archive:

- `seam_pilot_v2/`, `seam_pilot_sentinelagent/`, `seam_pilot_sa_boundary/`
  (including design files, locks, results, and traces);
- `authorization_pilot/seam_pilot/` and its pin/protocol files;
- `tracegrant_task_d_20261014/` implementation, examples, tests, results, and
  logs, excluding its virtual environment and downloaded paper sources;
- the SentinelAgent audit's assumptions, bootstrap commands, report, and the
  prototype/license files needed by the second pilot.

Excluded: virtual environments, caches, the full APC/Progent checkouts, the
SentinelAgent full repository and audit runs, third-party paper PDFs, and the
frozen predecessor manuscript/claim file.

## Hash authority

`artifacts/sha256sums.txt` covers the repository copies. The manuscript and
canonical PDF hashes are additionally recorded in
`paper/latex_export/README.md` and checked by `qa/`.
