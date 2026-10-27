# Review corrections - 21 October 2026

## Purpose and authority

This note records the authorized factual and traceability corrections applied
to `paper\MANUSCRIPT_REVISED.md` after the external review. The scope was
limited to correcting false characterizations and unverifiable provenance. No
new claims, experiments, references, or H4/H7 work were added. The abstract
remains 222 words and byte-identical to the frozen version
(`CD2278607B491BD49FE7A03585979B259BFD187B0E9C0F9D7D1D4181573B9654`).

## Superseded characterizations

| # | Superseded wording or implication | Correction now in the manuscript | Local primary source |
|---|---|---|---|
| 1 | Progent was associated with a `4/20` measurement. | No Progent figure is reproduced, re-measured, or compared. Progent is close related work, not a baseline; its reported numbers remain its authors' self-report. | `audits\task_b_verification_20261014\REPORT.md` records `mcp_raw 4/20` as a local Task B fixture, not a Progent result. Progent arXiv:2504.11703v3 contains no such claim. |
| 2 | APC was expanded as "agent policy core" and its composition theorem was cited as Theorem 4.8. | APC is **Agentic Principal Chain**. The cited result is **Theorem 4.7 (Composition Soundness)**. The text now states C1-C6, the complete restriction set, serialized admission, static X, and the intra-session scope. | APC arXiv:2608.15888v1. Section 4.8 is "Policy Invariants," not the composition theorem. |
| 3 | SentinelAgent Theorem 4 was described as requiring the "same mechanism." | Theorem 4 is **Composition Safety with Write-Impact Notification**, stated for two chains that both satisfy P1-P7 within its own framework. The false "same mechanism" condition is removed. | SentinelAgent arXiv:2604.02767v1, Theorem 4. |
| 4 | APC composition was implied to be cross-mechanism composition. | Composition senses are separated in Sections 2 and 6 and in Table 1: APC composition is intra-session action-sequence composition; it is not cross-mechanism composition. | APC arXiv:2608.15888v1; SentinelAgent arXiv:2604.02767v1. |
| 5 | SentinelAgent clean-comparison language omitted its recorded reconciliation mismatch. | Section 4.3 discloses that `manifest.json` records `expected_vs_observed_ok=false` and `metrics.json` records `comparison.overall_ok=false`, names the two failed checks, and cites `sa\reconciliation.json`. No behavior cell changed. | `tests\seam_pilot_sentinelagent\results\sa\manifest.json`; `metrics.json`; `reconciliation.json`. |
| 6 | The seam predicate was described through a narrower arm set. | The predicate now includes arms 5, 6, and 7, and the E1 arm-5 form is identified. | `tests\seam_pilot_v2\results\extension_e1\assertions.json`. |
| 7 | The Pilot-1 zero-seam reading pointed at the wrong section and was not tied to the forced identity. | The pointer is `tests\seam_pilot_v2\RESULTS_FOR_COAUTHOR.md` Section 1; the zero is derived from the arm2 = arm5 identity. All three forced identities are stated: Pilot 1 arm 2 = arm 5 at 24/24 cases and 26/26 events; SentinelAgent arm 2 = arm 5 at 28/28; boundary arm 2v = arm 5 at 32/32 per variant. | `tests\seam_pilot_v2\RESULTS_FOR_COAUTHOR.md`; the SentinelAgent and boundary result artifacts. |
| 8 | Zero seam could be read as a general theorem. | Section 1 now states that zero seam is a recorded property of narrowing-type families, not a theorem, and that the seam test can fire only where composition widens. | The frozen case sets and the manuscript's own bounded statement. |
| 9 | The positioning could be read as a survey of delegation or capability literature. | Section 6 adds a **Scope of positioning** paragraph that declines to survey the broader literature and makes no novelty claim over it. | The static seven-entry reference list and the existing scope statement. |
| 10 | The mapping and implementation provenance were underspecified. | Section 3.2 defines M0, M2, M2-auth, M0-A, T0, V1, and V2. Before Section 3.6 the text records the pinned APC commit (`d31a1ea115a3`, abbreviated), the SentinelAgent prototype SHA-256 (`739d9db1e836`, abbreviated), the independent TraceGrant Task D implementation, and the bridge mappings as this program's constructions. | Local build and artifact records; abbreviated hashes are used in prose and full values remain in the artifact tree. |
| 11 | Table 6 used long arm names and lacked case-ID traceability; Tables 8 and 9 contained mid-token wraps. | Table 6 uses arm numbers and case IDs `action_narrow-0-a` through `action_narrow-3-a` and `-b` through `-3-b`. Table 8 uses abbreviated metric headers. Table 9 uses compact code cells and a control list with in-place abbreviation definitions. These are layout-only edits; no cell value changed. | `paper\MANUSCRIPT_REVISED.md`; rendered PDF pages 9-13. |

## Additional corrected details

- The `4/20` number is a local Task B fixture (`mcp_raw 4/20`), not a Progent
  measurement.
- Table 3 is a **matrix execution ledger**, with footnote records
  for the Pilot-1 controls (21), replay (10 pairs), and latency harness
  (7 arms x 100 warmup + 1,000 measured), plus the existing control and replay
  records.
- The SentinelAgent reconciliation note records the two locked derivations
  that disagreed with observation (false-denial events 26 -> 28; arm-5
  confusion TN denominator 68 -> 20) with `affects_behavior_cells` false.
- Tables 6 and 8 were checked visually after the layout changes, not only by
  text extraction. `pdftotext` garbles math glyphs; extracted `?` characters
  are not missing-glyph evidence.

## Files changed

- `paper\MANUSCRIPT_REVISED.md` - corrections and layout-only table edits.
- `paper\build\preprocess.py` - expected source hash updated to the new
  manuscript hash.
- `paper\build\retable.py` - table-block width map updated after the Table 9
  controls table became a list.
- `paper\latex_export\main.tex`, `main.pdf`, `README.md` - standalone export
  regenerated from the corrected build.
- `paper\drafts\MANUSCRIPT_DRAFT_2026-10-21.pdf` - canonical draft replaced
  with the 24-page build.
- `paper\drafts\seam_manuscript_latex_2026-10-21.zip` - export package
  regenerated and independently compiled.
- `paper\ARTIFACT_SNAPSHOT.md`, `paper\RESEARCH_STATUS.md`,
  `paper\SUBMISSION_METADATA_CHECKLIST.md`, `paper\TOOLCHAIN.md`,
  `docs\FINAL_BUILD_QA.md`,
  `docs\FONT_QA_REPORT.md` - current build state and hashes
  refreshed.
- `future_paper\FUTURE_PAPER_BUILD.md` - separate proposed full-paper build;
  not part of the current paper.

## Frozen files kept untouched

`paper\MANUSCRIPT.md`, `paper\CONSOLIDATED_CLAIMS.md`, `paper\hashes.txt`,
locks, traces, pre-revision files, and figure artifacts were not edited.

`paper\CONSOLIDATED_CLAIMS.md` remains frozen but now contains superseded
Progent/APC/SentinelAgent characterizations. It is not the current wording
authority until separately reconciled; this note is the correction record and
does not modify it.

## Build state after corrections

- Manuscript SHA-256:
  `D1A7AA9E3119AE3850FBA1C012B12ED528F6BF2B0CA0A794BC2A63310E06AF1D`
- Draft PDF SHA-256:
  `5635F9DDA3A9D75B56C791939F80DC3ACBF5254619661131A6E80AB47F2FB494`
- Pages: 24; page size 612 x 792 pt; PDF 1.7.
- 0 missing glyphs, 0 LaTeX errors, 0 overfull hboxes.
- 3 cosmetic underfull hboxes; 1 stable `Label(s) may have changed` warning
  with no unresolved-reference warning.
- Standalone `main.tex` SHA-256:
  `73CDBEF4E38721D50FB4CCA6973D7E4A0FB8818D86D3C74F06D67384BF049A24`
- Standalone `main.pdf` SHA-256:
  `163CBD7D5D771C6B751DBB6B6A8C63B85E2CE039AA043C9B66951524F8B58BFA`
- Export zip SHA-256:
  `D64FD1D46ED0C2A70BF10B2CD1D753DBD130BB4E9B52D247EBAB03B60AD670A2`
  (independently extracted and compiled: 24 pages, 0 errors, 0 missing
  characters, 0 overfull hboxes).

## Deferred, not authorized by this pass

- Classic delegation/capability literature expansion. The reference list
  remains the static seven-entry list; additions need explicit approval and
  new verification.
- The 40-50 percent length cut.
- Any new data figure or new experiment.
- H4 and H7 remain `UNTESTED`; no H4/H7 experiments were run or authorized.
- No merge into `paper\MANUSCRIPT.md`, no submission, and no change to the
  paper's workshop/short-paper, tool-track, or arXiv-preprint target.
