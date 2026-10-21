# Security policy

## Scope

This repository contains offline research harnesses and frozen result files.
It should not contain credentials, API keys, personal data, or live network
code. The experiment runners deliberately disable network access (`block_network`
in `tests/authorization_pilot/seam_pilot/native.py` and the audit entry points).

## Reporting

Do **not** open a public issue for a suspected credential leak or a security
problem in a third-party project. Once a repository remote exists, use the
host's private vulnerability-reporting feature. Until then, report privately to
the repository owner.

Include:

- the affected path or artifact;
- whether the issue is in this repository or in a pinned third-party project;
- a minimal reproduction if one is safe to share.

## Out of scope

- The paper's research findings, scoped-claim disputes, and review comments are
  not security reports. Use the normal issue/contribution process for those.
- Vulnerabilities in upstream APC, Progent, TraceGrant, or SentinelAgent must
  be reported to those projects, not here.

## Release gate

`scripts/verify_artifacts.py` and `docs/RELEASE_SANITIZATION.md` are part of the
release process. A public release must pass both.
