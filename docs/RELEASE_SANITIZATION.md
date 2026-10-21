# Release sanitization

## Why

Frozen artifacts and logs record the machine paths used when the experiments
ran. They are kept byte-identical in the source tree so the recorded hashes
verify. A public release should not necessarily expose those paths, and must
never expose the internal placeholder email.

## Procedure

1. Verify the source tree first:

   ```powershell
   python scripts/verify_artifacts.py
   ```

2. Produce the sanitized tree:

   ```powershell
   python scripts/sanitize_release.py
   ```

3. Review `dist/sanitized/SANITIZATION_REPORT.json`. Every changed file records
   its original SHA-256 and the number of replacements.

4. Re-verify the sanitized tree by running the verifier with `dist/sanitized`
   as the working tree, or simply inspect that no replacement tokens remain:

   ```powershell
   Get-ChildItem dist\sanitized -Recurse -File |
     Select-String -Pattern 'C:\\Users|/home/|/Users/|agentscan@gmail\.com'
   ```

5. Publish `dist/sanitized/` as a fresh repository/archive. Do **not** push the
   working tree and then delete the paths: the original bytes would remain in
   Git history.

## What the script rewrites

Text files only. Binary files (PDFs, figures, zips) are copied unchanged.

| Pattern | Replacement |
|---|---|
| Windows user paths, escaped or plain | `<LOCAL_PATH>` |
| POSIX/macOS home paths | `<LOCAL_PATH>` |
| Internal placeholder email | `<EMAIL_REDACTED>` |

## Known files with machine-local references

This list is illustrative, not exhaustive; the script report is the authority.

- `tests/seam_pilot_sentinelagent/results/sa/manifest.json`
- `tests/seam_pilot_sa_boundary/results/boundary/manifest.json`
- `tests/seam_pilot_sentinelagent/results/adversarial_review.json`
- `tests/seam_pilot_sentinelagent/results/ADVERSARIAL_REVIEW.md`
- `tests/seam_pilot_sa_boundary/design/build_boundary_lock.py`
- `tests/seam_pilot_v2/design/phase0_state.md`
- `tests/seam_pilot_v2/design/call_to_contract_mapping.md`
- `tests/seam_pilot_v2/discriminating_tests/design/discriminating_lock.json`
- `tests/tracegrant_task_d_20261014/pins.json`
- `tests/tracegrant_task_d_20261014/REPORT.md`
- `tests/tracegrant_task_d_20261014/logs/*`
- `tests/sentinelagent_audit_20261014/BOOTSTRAP_COMMANDS.md`
- `paper/figures/FIGURE_PDF_HASHES.txt`

## What sanitization must not change

- The canonical manuscript, figures, or canonical PDF.
- Frozen result values, counts, hashes, or labels. Only machine-path strings and
  the internal placeholder email may change.
- Third-party license notices.

## Secrets check

The script does not exhaustively detect credentials, and the repository should
never contain any. Before release, also scan for token-shaped strings and
confirm that no API key, cookie, or private key was committed. The harnesses are
designed to run offline and to take no credentials.
