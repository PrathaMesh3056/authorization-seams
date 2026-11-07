# Read-only reviewer prompt - seam manuscript

Status: prepared 7 November 2026 for an author-authorized internal review.
This prompt is for a reviewer working directly in the repository. It is not a
public release document and it does not assert peer-review status.

## Reviewer authorization and scope

You are reviewing an unpublished single-author manuscript and its build
artifacts at the request of the author. The author has authorized this internal
review. Treat the repository as confidential; do not quote unpublished text
outside the review response, and do not transmit repository contents to any
external service.

Your review is **read-only**. You must not:

- edit, delete, rename, format, or create any file in the repository;
- run any experiment, including any H4 or H7 experiment;
- run build scripts that write into `paper/build/` or regenerate any PDF,
  zip, or artifact;
- modify, regenerate, or re-sanitize frozen artifacts, locks, traces,
  `paper/hashes.txt`, `paper/authority/CONSOLIDATED_CLAIMS.md`, or
  `dist/sanitized`;
- merge `paper/MANUSCRIPT_REVISED.md` into any frozen predecessor;
- push, commit, tag, or publish anything.

Read-only inspection commands are allowed: reading files, listing
directories, computing SHA-256 digests, counting words and references, and
extracting text from an existing PDF into memory or a temporary location
outside the repository. If a check would write into the repository, skip it
and record it as "not run (read-only)".

## Review target

Review the 7 November 2026 revised manuscript and the package around it,
using repository-relative paths:

- `paper/MANUSCRIPT_REVISED.md` - the live manuscript source
- `paper/drafts/MANUSCRIPT_DRAFT_2026-11-07.pdf` - canonical 33-page PDF
- `paper/latex_export/main.tex` and `main.pdf` - standalone LaTeX export
- `paper/arxiv_export/main.tex` and `main.pdf` - arXiv candidate
- `dist/arxiv/authorization-seams-arxiv-2026-11-07.zip` - arXiv source package
- `paper/build/preprocess.py`, `header.tex`, `retable.py`,
  `build_arxiv.py` - build pins and layout settings
- `paper/README.md`, `paper/latex_export/README.md`,
  `paper/arxiv_export/README.md`, `paper/arxiv_export/ARXIV_METADATA.md`
- `docs/ARTIFACT_SNAPSHOT.md`, `docs/ARXIV_BUILD_QA.md`,
  `docs/RESEARCH_STATUS.md`, `docs/TOOLCHAIN.md`
- `CITATION.cff`
- `paper/hashes.txt` and `paper/authority/CONSOLIDATED_CLAIMS.md` as frozen
  authority only; do not edit them

The pre-style backup is `paper/backups/MANUSCRIPT_REVISED_pre_style_20261107.md`.
It predates both the style revision and the external-review reconciliation; use
it only to check the style-revision delta, not as a no-change baseline. The
pre-review 7 November Markdown source was overwritten in place; its canonical
PDF and arXiv zip are archived under `paper/backups/` for comparison.

## Hard constraints to verify

1. H4 and H7 remain `UNTESTED`. No H4/H7 experiment is present or implied.
2. The abstract is 222 words and its SHA-256 is
   `B93412AC45C73A9692F33E6B765959C581231BF93DE65F0D6C2BC8CBC460AF38`.
3. The reference list has exactly 21 entries and all body citations use
   bracketed keys that resolve to those entries.
4. The frozen spines are present and unchanged:
   - `2,446 = 560 + 40 + 6 + 16 + 672 + 1,152`
   - `2,446 = 560 + 46 + 0 + 16 + 672 + 1,152`
   - `638 = 488 + 150`
   - `150 = 40 + 42 + 68`
   - `32 = 28 + 4`
5. The forced-vs-contingent labels, effective sample sizes, scoring
   conventions, and frozen-set deviations are stated consistently and are not
   rounded or inferred. This includes the E1 disclosure that arms 2 and 5 decide
   identically on all eight cases and that the arm-native norm was locked at
   `2026-10-19T12:52:51Z`, after the E1 run began at `2026-10-19T07:12:26Z`;
   Pilot 1's 8/40 falsified and 32/40 matched reconciliation; and H1's resource
   clause recorded as "not supported" per the frozen authority.
6. The author is `Prathamesh N Patil` throughout the title pages, PDF metadata,
   build pins, and `CITATION.cff`.
7. Table 5 headers are `SA`/`M0`/`Retained` with an explicit column key; no cell
   value differs from the pre-edit backup.
8. Declarations state no external funding, no competing interests, full
   single-author CRediT roles, author-retained data availability, and an
   acknowledgments note. No public email, venue, DOI, license, repository URL,
   funding, competing interest, or peer-review status is invented.
9. The canonical PDF is 33 pages; the arXiv candidate is 37 pages; both have
   0 missing glyphs, 0 fatal LaTeX errors, 0 overfull hboxes, and 1 stable
   label warning. The canonical build has 6 cosmetic underfull hboxes; the
   arXiv build has 4.
10. The recorded artifact hashes in `docs/ARTIFACT_SNAPSHOT.md` and
    `docs/ARXIV_BUILD_QA.md` match the files in the repository.
11. The arXiv builder verifies the unified author and rejects the older
    `Prathamesh Patil` variant; the arXiv diff is limited to the margin and
    Figure 2 width plus the generated header.
12. `dist/sanitized` and all frozen authority/lock/trace files remain
    untouched.

## What to assess

Review both the manuscript and the package as a reviewer would:

- **Contribution and positioning.** Is the measurement problem clearly stated?
  Is the two-reading seam test understandable? Is the related-work positioning
  accurate and appropriately bounded?
- **Evidence and claims.** Does every headline number trace to a frozen
  artifact? Are forced and contingent results labeled correctly? Are the
  repair claims supported? Are the zeroes presented as recorded properties
  rather than theorems?
- **Method and reproducibility.** Are the lock discipline, scoring
  conventions, arms, cases, and deviations described precisely enough to
  replicate? Are the build pins and artifact hashes coherent?
- **Writing and presentation.** Check structure, paragraph flow, terminology,
  table/figure readability, reference consistency, and typography. Flag any
  remaining first-person voice in the body, stale numbers, duplicated claims,
  or unreadable tables.
- **Threats to validity and ethics.** Are the scope limits, single-author
  limits, external-validity limits, and AI-use disclosure honest and complete?
- **Venue fit.** Assess arXiv preprint, workshop/short/tool track, main
  research track, and a future full paper separately. Do not assume a venue
  has been selected.

Do not praise or penalize the paper for being single-author, for repository
visibility, or for not having a DOI; those are release decisions, not
manuscript defects. Do not require H4/H7 experiments; they are explicitly out
of scope.

## Scoring rubric

Give each target a score from 1 to 10. Use the whole number that best matches
the evidence, and state the basis in one or two sentences.

| Score | Meaning |
|---:|---|
| 9-10 | Publishable at a strong venue in this category with only minor edits |
| 7-8 | Competitive in this category; fixable weaknesses, no fatal flaw |
| 5-6 | Borderline; a venue cut or substantial revision is needed |
| 3-4 | Not competitive in this category without new evidence or reframing |
| 1-2 | Fundamental claim, method, or presentation problem |

Targets:

1. arXiv preprint
2. Workshop / short paper / tool track
3. Main research track
4. Future full paper

Also give one overall recommendation: `Accept as preprint`, `Minor
revision`, `Major revision`, or `Reject for this category`. The recommendation
must follow from the scores and the stated evidence.

## Required output order

Return the review in exactly this order:

1. **Review metadata.** Authorization basis, scope, conflicts, materials
   reviewed, and a one-line read-only attestation.
2. **Summary of the submission.** What the paper does, in the reviewer's own
   words, in at most 150 words.
3. **Strengths.** Three to six specific strengths with file or section
   references.
4. **Major issues.** Ordered by severity. For each: the issue, the evidence,
   why it matters, and a concrete fix.
5. **Minor issues.** Writing, tables, references, typography, and consistency.
6. **Claim-evidence audit.** A table with the twelve hard constraints above:
   `Check | Result (pass/fail/not run) | Evidence`. Include observed hashes and
   counts. If a file could not be checked read-only, say so explicitly.
7. **Build and artifact verification.** Page counts, PDF metadata, missing
   glyphs, overfull/underfull counts, label warnings, source/PDF hashes, zip
   contents, and any mismatch with the recorded docs.
8. **Scores.** The four targets with scores and one-line bases.
9. **Recommendation.** One of the four labels above.
10. **Required revisions before submission.** A short, prioritized list
    limited to changes that are within the manuscript's current scope.

## Evidence rules

- Cite repository-relative paths, section numbers, table numbers, and exact
  counts. Do not cite local absolute paths in the review body.
- Distinguish `verified`, `reported`, and `not independently verified`.
- Do not infer a number that is not written in the repository.
- Do not treat the frozen `CONSOLIDATED_CLAIMS.md` as current wording
  authority; it is a frozen historical artifact with known superseded
  characterizations.
- If the repository and the recorded docs disagree, report both values and
  identify which file is stale.
- If a constraint cannot be verified without writing to the repository, mark
  it `not run` and explain why. Do not silently pass it.

## Read-only attestation

End the review with this attestation, filled in truthfully:

> Read-only attestation: I did not edit, create, delete, or rename any file in
> the repository; I did not run any experiment or build script; I did not
> modify frozen artifacts, locks, traces, `paper/hashes.txt`,
> `paper/authority/CONSOLIDATED_CLAIMS.md`, or `dist/sanitized`. The checks I
> ran were: [list]. Checks not run: [list and reason].
