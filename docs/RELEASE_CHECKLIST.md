# Release checklist

Work top to bottom. Do not publish or submit while any required gate is open.

## Blocking gates

- [ ] **Final public author email** chosen and inserted in the venue metadata
      (not on the draft PDF until decided). The placeholder recorded internally
      must not appear in any release artifact.
- [ ] **Target venue/CFP** chosen; page limit, anonymity rule, reference style,
      and supplementary rules confirmed against the current CFP.
- [ ] **License selected** for code and manuscript; `LICENSE` replaced;
      `CITATION.cff` and `codemeta.json` updated.
- [ ] **Repository URL** assigned (after publishing) and added to the paper's
      availability section and arXiv comments/metadata.
- [ ] **Archival DOI** obtained (Zenodo/OSF or equivalent) and added; the
      `.zenodo.json` note removed once the record is intentional.
- [ ] **Release sanitization** run and reviewed; publish `dist/sanitized/`, not
      the working tree, if machine paths must not be public.
- [ ] **Manifest regenerated** after the final content change; verifier passes.
- [ ] **Paper rebuild** reviewed against the canonical PDF; page count and
      figure placement unchanged unless deliberately revised.

## Frozen-claim gates

- [ ] H4 and H7 remain `UNTESTED` in the manuscript and docs.
- [ ] Progent remains related work only; no reproduced figure or comparison.
- [ ] Forced and contingent identities remain labeled separately.
- [ ] The measured exception remains scoped to its design point and case
      family and attributed to the scoring convention.
- [ ] Both frozen-set-justified SentinelAgent-pair prediction overrides remain
      disclosed.
- [ ] The Test 2 runner-hash deviation remains disclosed.
- [ ] The zero-seam caveat remains in the manuscript.
- [ ] The eight-entry static reference list is unchanged or updated only after
      explicit approval and verification.
- [ ] No merge into the frozen `MANUSCRIPT.md`.

## arXiv build gates

- [x] arXiv-compliant named-author build created with 1-inch margins, 10 pt
      type, no line numbers/watermarks, and 0 missing glyphs / 0 LaTeX errors /
      0 overfull hboxes. See `docs/ARXIV_BUILD_QA.md`.
- [ ] arXiv license selected and recorded; the choice is irrevocable per
      announced version.
- [ ] arXiv endorsement status resolved for `cs.CR`.
- [ ] Public contact email and optional ORCID finalized.
- [ ] Repository URL / archival DOI added only after the public release gate
      closes, or omitted from the arXiv metadata.

## Packaging gates

- [ ] `python scripts/verify_artifacts.py` passes.
- [ ] `python -m pytest -q qa` passes.
- [ ] `python scripts/package_release.py` produces a zip and its `.sha256`
      sidecar; the zip extracts and the paper build still passes.
- [ ] Zip contains no `.git`, virtual environment, cache, or machine path that
      survived sanitization review.
- [ ] Poppler is not bundled.

## Sign-off

- [ ] Owner has reviewed `CHANGELOG.md` and the sanitization report.
- [ ] No submission has occurred without an explicit instruction to submit.
