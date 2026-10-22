# Recheck reconciliation — 21 October 2026

Reconciliation of the independent external recheck of the corrected manuscript against the raw experiment artifacts, with the author-side corrections applied on this date.

- **Recheck report:** `paper\MANUSCRIPT_CROSSCHECK_SONNET5_2026-10-21.md` — filed under the prompt's naming convention; free-model fallback run (runner designated GLM-5.3-Flash Free). SHA-256 `D22C24E99E5A124C3AE8701577261181F911F40E574EDD5AB5D92EFD31BF0668`.
- **Reviewed manuscript at review time:** `paper\MANUSCRIPT_REVISED.md`, SHA-256 `D1A7AA9E3119AE3850FBA1C012B12ED528F6BF2B0CA0A794BC2A63310E06AF1D`.
- **Scope of this record:** author-side reconciliation only; frozen artifacts, locks, traces, backups, and prior review records are untouched.

## Recheck outcome

- Verdict: **PASS WITH NOTES** — 183 itemized rows: 174 MATCH, 0 UNBACKED, 0 claim MISMATCH.
- All eleven correction-regression items present and correct; execution ledger recomputed exactly (2,446 = 560 + 40 + 6 + 16 + 672 + 1,152); Table 15 hashes verified against `paper\hashes.txt` with all six artifacts re-hashed; figures confirmed vector-only (zero raster objects).
- Abstract byte-identical: SHA-256 `CD2278607B491BD49FE7A03585979B259BFD187B0E9C0F9D7D1D4181573B9654` (222 words); re-verified after the corrections below — unchanged.

## Findings and dispositions

| # | Finding (from the recheck report) | Verification | Disposition |
|---|---|---|---|
| 1 | FROZEN-SOURCE DISCREPANCY / E22 AMBIGUOUS — H5 signature family stated as "2 pairs × 4 parameters = 8 cases (4 attack, 4 benign)" | Confirmed. Artifact truth: **16 cases = 2 pairs × 4 document parameters × 2 variants (8 attack + 8 benign)**. Evidence: direct count of `tests\seam_pilot_sentinelagent\results\sa\runs.jsonl` (16 unique signature cases, 8 per kind); `results\SA_RESULTS.md` Section 7 ("the 16 new cases are the signature family (2 pairs x 4 document parameters x 2 variants)"); `results\ADVERSARIAL_REVIEW.md` item C1 ("16 new sig cases = 2 pairs x 4 params x 2 variants"); SA scale 96 = 80 reused + 16 new. The frozen map (`CONSOLIDATED_CLAIMS.md`, H5 sample-size line) dropped the "× 2 variants" factor; the manuscript had inherited it verbatim. No behavior cell, leak count, or status token is affected (Table 9's "x4" cells × 4 templates = 16). | Manuscript corrected (see below). `CONSOLIDATED_CLAIMS.md` remains frozen and untouched; superseded on this line by the artifact. |
| 2 | AUXILIARY MISMATCH — figure hash records no longer match the on-disk bytes | Confirmed. `figures\FIGURE_PDF_HASHES.txt` and the post-edit block of `figures\FIGURE_CHANGELOG.md` recorded PDFs `5343A821…`/`96D0A841…` and SVGs `799B1B91…`/`F8E5FBDA…` from the 20 Oct 18:16 pass; current bytes are PDFs `0AA8A365…`/`5ABCDD26…` and SVGs `035902B0…`/`F80E70F4…`. `figure_1_handoff_anatomy_v2.svg` remains at the promoted hash `799B1B91…`, so the "byte-identical" status note is historical. `FIGURE_INTEGRATION_CHANGELOG.md` final section already carries the current PDF hashes. The manuscript makes no figure-hash claim. | `FIGURE_PDF_HASHES.txt` regenerated against current PDF bytes; dated addendum appended to `figures\FIGURE_CHANGELOG.md`. |
| 3 | FORMAT — `\raggedright` at the start of References in the markdown | Confirmed at `MANUSCRIPT_REVISED.md` line 533; passed through to the LaTeX build; not present in the built PDF text (verified with `pdftotext`). It left-aligns the reference list (LaTeX-only layout directive). | Retained; recorded as presentation-only. It renders literally if the markdown itself is rendered. |
| 4 | GRANULARITY — Task D path citation omits the `tests\` prefix | Confirmed; the manuscript's own convention prefixes `tests\` (e.g., line 134). | Corrected (see below). |
| 5 | GRANULARITY — "the arm-5 confusion matrix on the four attacks" scopes the 2×2 to the attack half | Confirmed; the 2×2 spans the eight-case E1 family (TP = the 4 attacks, TN = the 4 benign). Numbers unchanged. | Corrected (see below). |
| 6 | J4 ABSENT — no author/affiliation block | Expected for the anonymized draft; required at camera-ready. | Open gate (with repo name/visibility, license, and public-email decisions). |
| 7 | E38/J8 NOT VERIFIED — external bibliographic identities and venue compliance | Disclosed in the manuscript itself; outside a local read-only check. | No action. |

## Corrections applied to `paper\MANUSCRIPT_REVISED.md` (21 October 2026)

Three in-line replacements; no other line changed (diff against the pre-edit copy in `RPaper-repo`: exactly 6 diff entries = 3 replaced lines; line count unchanged at 549).

1. Section 4.3 (line 267): `2 pairs × 4 parameters = 8 cases (4 attack, 4 benign)` → `2 pairs × 4 document parameters × 2 variants = 16 cases (8 attack, 8 benign)`.
2. Section 4.2 (line 136): Task D path `tracegrant_task_d_20261014/implementation/` → `tests\tracegrant_task_d_20261014\implementation\`.
3. Section 4.1 (line 213): `the arm-5 confusion matrix on the four attacks` → `the arm-5 confusion matrix on the eight-case family`.

**Manuscript identity after corrections:** 549 lines, 109,122 bytes, SHA-256 `E3E5CE2C18D7F9EC0178095EA4275C1FE303DFF72E92869D1EB6CE78C402B724`.

## File updates

| File | Change | SHA-256 after update |
|---|---|---|
| `paper\MANUSCRIPT_REVISED.md` | the three corrections above | `E3E5CE2C18D7F9EC0178095EA4275C1FE303DFF72E92869D1EB6CE78C402B724` |
| `paper\figures\FIGURE_PDF_HASHES.txt` | regenerated against current PDF bytes | `736517D5EA9FA77393C1FBB217D3BC9D22BDC05EACEF0B1BCCB6C9A71069895F` |
| `paper\figures\FIGURE_CHANGELOG.md` | addendum with current hashes | `804A66915980CB34651A2B16F454B04B5CD995401E3B6CF7FFE1891444B8BEB3` |

## Unchanged by this reconciliation

- Abstract: `CD2278607B491BD49FE7A03585979B259BFD187B0E9C0F9D7D1D4181573B9654` (recomputed from the paragraph text, UTF-8, no EOL; 222 words).
- All table cells, counts, hash ledgers, and status tokens (H1 `REFINED`; H2 `SUPPORTED`; H3 `SUPPORTED`; H5 `REFINED`; H6 `SUPPORTED`; ★ `SUPPORTED`; H4 `UNTESTED`; H7 `UNTESTED`).
- Frozen files, verified by hash after the corrections: `paper\MANUSCRIPT.md` `44FB84EEB2586A99172B2EB09F41C1FFC40A90E572FE1BF4A728E97211FBA2AF`; `paper\CONSOLIDATED_CLAIMS.md` `AB088CDFBAF64B14C57C63423B908DEAF7404465C15852FD355D6C3F7870BE51`; `paper\hashes.txt` `9A87ED363F7C481837985BD6C8DE15B4FAA168FE7365B67D12263C408AB0E557`; locks, traces, evidence files, and backups untouched.
- No new claims, experiments, references, or H4/H7 work were introduced.

## Pending refresh (deferred, tracked)

The canonical PDF (`paper\drafts\MANUSCRIPT_DRAFT_2026-10-21.pdf`, SHA-256 `5635F9DDA3A9D75B56C791939F80DC3ACBF5254619661131A6E80AB47F2FB494`, 24 pages) and the staged repository (`RPaper-repo`, HEAD `012a1ea`) remain pinned to the reviewed revision and now trail these corrections. At the finalization pass (author block plus any approved final edits):

1. Update the build guard `EXPECTED_SHA` in `paper\build\preprocess.py` to the new manuscript SHA; rebuild the canonical PDF; verify page count, glyph, and layout metrics; refresh `paper\latex_export\`.
2. Copy the corrected manuscript, the updated figure records, and this reconciliation record into `RPaper-repo`; regenerate the artifact manifest and `artifacts\sha256sums.txt`; update the QA/integrity pins that expect `D1A7AA9E…` and `5635F9DD…`; refresh the state docs that cite the old hashes as current (`ARTIFACT_SNAPSHOT.md`, `RESEARCH_STATUS.md`, `SUBMISSION_METADATA_CHECKLIST.md`, `agent_reports\FINAL_BUILD_QA.md`, `agent_reports\FONT_QA_REPORT.md`, `agent_reports\REVIEW_CORRECTIONS_2026-10-21.md`, `latex_export\README.md`, and their repo copies); regenerate `dist\sanitized\`.
3. Add the author/affiliation block and re-run the release checklist.

*Applied by the local assistant session on 21 October 2026 on the author's instruction; the recheck report reconciled here is preserved at `paper\MANUSCRIPT_CROSSCHECK_SONNET5_2026-10-21.md`.*
