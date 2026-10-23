# Contributing

This is a research artifact repository tied to a specific manuscript revision.
The most important contribution rule is simple: **do not edit frozen
artifacts.**

## Ground rules

1. **Frozen means frozen.** Files under `paper/` (manuscript source, hashes)
   and `tests/**` (cases, locks, results) are the evidence for the manuscript.
   Corrections are made by adding a new dated artifact or a new revision, never
   by editing an existing one in place.
2. **No new claims without evidence.** The manuscript reports only what the
   locked artifacts support. Do not add results, comparisons, or performance
   claims to the manuscript without a new frozen experiment and review.
3. **H4 and H7 stay `UNTESTED`.** Do not present analysis, commentary, or
   partial runs as tests of either hypothesis.
4. **Third-party material is referenced, not absorbed.** Do not vendor
   upstream projects beyond the small MIT-licensed SentinelAgent excerpt that
   is already present. Use `scripts/bootstrap_vendor.*` for pinned clones.
5. **No secrets, tokens, or personal credentials.** The harnesses run locally
   with network access disabled during runs.

## Making a change

```powershell
python scripts/verify_artifacts.py
python -m pytest -q qa
```

If you change a file covered by `artifacts/sha256sums.txt`, the integrity check
will fail. That is intended. Regenerate the manifest only when the change is an
authorized revision, and record what changed and why in `CHANGELOG.md`.

## Review checklist

- [ ] The change does not modify a frozen artifact in place.
- [ ] `scripts/verify_artifacts.py` passes.
- [ ] `python -m pytest -q qa` passes.
- [ ] If the manuscript changed, the hash in `paper/build/preprocess.py` and
      the canonical PDF were regenerated deliberately.
- [ ] No placeholder contact, token, or machine-local path was added.
- [ ] Claims remain scoped to the locked case families.
