# CODASPY 2027 Venue Compliance

**Artifact:** `paper/venue_codaspy2027/main.pdf`
**Source:** `paper/venue_codaspy2027/main.tex`
**Date:** 3 November 2026
**Target:** CODASPY 2027 research track
**Requirements checked:** CODASPY 2027 call for papers, verified 2 November 2026

## Verdict

**Local compliance pass.** The venue cut is 13 pages: pages 1-12 are the
double-column main body plus references, and page 13 is a one-column appendix.
This meets the 12-page main limit and the 2-page appendix allowance. The build
is anonymized, all 16 references are cited, the frozen claim counts are
present, and H4/H7 remain `UNTESTED`.

This is a local build record, not a submission record. No push, submission, or
public release has occurred.

## Requirements and evidence

| Gate | Requirement | Evidence | Status |
|---|---|---|---|
| Main length | At most 12 pages, double column, including references | References end on page 12; appendix begins page 13 | PASS |
| Appendix | At most 2 pages, separate from the main limit | One page, one column, four tables | PASS |
| Format | ACM `sigconf`, double column | `\documentclass[sigconf,anonymous,nonacm]{acmart}`; US Letter 612x792 pt | PASS |
| Anonymity | No authors, affiliations, emails, or identifying paths | `anonymous` option; `Anonymous Author(s)`; blank PDF author; token scan clean | PASS |
| References | All cited; verified metadata; no inventions | 16 `\bibitem` entries; BibTeX used 16; DOI/RFC/JHU checks recorded below | PASS |
| Layout | No overfull boxes, undefined references, missing glyphs | 0 overfull hbox; 0 overfull vbox; 0 undefined; 0 missing characters; 0 font warnings | PASS |
| Claims | Frozen counts preserved; H4/H7 `UNTESTED` | Claim spot-check below | PASS |
| Frozen evidence | Canonical artifacts and claim set untouched | Canonical hashes unchanged; 319-file manifest verified | PASS |
| Submission | Not submitted | Local worktree only | NOT SUBMITTED |

## Page accounting

`build.py` locates the appendix opening by its title, `A Hypothesis Lineage and
Detailed Tables`, and treats every page before it as main content:

```text
total pages:              13
main body + references:   pages 1-12  (12 pages, limit 12)
appendix:                 page 13     (1 page, limit 2)
```

The references heading is inside pages 1-12. The main limit is met exactly;
there is no spare main-text page. If final ACM metadata or a copyright block is
added later, re-run the gate and confirm the main body still ends by page 12.

## Format and anonymity

- Class: `acmart` `sigconf`, `anonymous`, `nonacm`.
- Author block: `Anonymous Author(s)` only; no affiliation, email, or URL.
- PDF metadata: title present; author blank; creator/producer are standard
  XeLaTeX and `acmart` strings.
- Body scan for `Prathamesh`, `Sardar Patel`, `spit.ac.in`, `OneDrive`,
  `C:\Users`, `github.com/`, and `RPaper`: no hits.
- Email scan: only synthetic experiment addresses under `example.test`
  (`default@example.test` and the hyphenated `forbidden-default@example.test`
  test value). Neither is author contact information.
- No acknowledgments section and no funding statement are present.

## Frozen evidence and claim integrity

The venue cut is a new file tree. It does not modify the canonical manuscript,
the canonical PDF, the standalone export, the arXiv export, `paper/hashes.txt`,
`paper/CONSOLIDATED_CLAIMS.md`, or `dist/sanitized`.

Canonical hashes at this build:

```text
79CB8E608CD516B18077943E10433A8F22C834B05AD5D19156330B53B258A876  paper/MANUSCRIPT_REVISED.md
F2A3AB17565AF888D23687C5D207DC86C7A6BFE4B58E249608AEF43B607EBE9D  paper/drafts/MANUSCRIPT_DRAFT_2026-10-31.pdf
31F45A48ADFD4B0E16EA87727FEB740A22D33A4362C57D6161DF1E46F379E45A  paper/latex_export/main.pdf
33207E1E00DB205F3C123C763EDC8FC978C959C2417EB2B4AC4B68D304933CE1  paper/arxiv_export/main.pdf
```

The 319-file manifest check reports `verified 319 files; all hashes match`.
The manifest intentionally excludes `paper/venue_codaspy2027/` because the venue
cut is a derivative workspace with its own `build.py` gate; this keeps the
canonical file count and frozen artifact inventory unchanged. No experiment was
run for this cut, no result was re-scored, and no claim was upgraded. H4 (shared
audit trail) and H7 (intent layer P2) are `UNTESTED` in the body, the threats
section, the conclusion, and Appendix A1.

## Claim spot-check

| Claim | Required value | Venue location |
|---|---|---|
| Execution ledger | 2,446 = 560 + 40 + 6 + 16 + 672 + 1,152 | Section 3.4, Table 1; Section 8; Section 9 |
| Pilot-1 leaks | 24/40 attack cases, 26 unauthorized-effect events | Section 4.1, Table 2 |
| Pilot-1 novelty | 0/40 receiver-relative novelty | Sections 4.1 and 4.5, Table 4 |
| SentinelAgent leaks | 28/48 attack cases, 30 unauthorized-effect events | Section 4.3, Table 4 |
| SentinelAgent novelty | 0/48 receiver-relative novelty | Sections 4.3 and 4.5, Table 4 |
| E1 composition-specific result | 4/4 arm-native vs. 0/4 family-wide | Section 4.2, Tables 3-4 |
| E1 repair | 4/4 attacks denied, 4/4 benign allowed | Section 4.2, Table 3 and text |
| Boundary counts | 32 = 28 + 4, 34 unauthorized-effect events | Section 4.4, Table A4 |
| Fail-closed cost | 20 benign false denials, 28 FD events | Sections 4.3 and 5 |
| Non-vacuity | 638 = 488 + 150 | Section 4.3 |
| Evaluated events | 756 = 488 + 150 + 118 | Section 4.3 |
| H4 | `UNTESTED` | Sections 5 and 7.5; Conclusion; Appendix A1 |
| H7 | `UNTESTED` | Sections 5 and 7.5; Conclusion; Appendix A1 |

## Reference verification

The canonical preprint keeps its original 8 references. The venue cut adds 8
positioning anchors, all cited in Section 6. Metadata was checked through
Crossref, the RFC Editor/DOI resolver, or the JHU scholarship record; no field
was invented.

| Key | Reference | Identifier | Verified metadata |
|---|---|---|---|
| `macaroons` | Macaroons: Cookies with Contextual Caveats (NDSS 2014) | doi:10.14722/ndss.2014.23212 | Internet Society, Reston, VA; no page range in Crossref |
| `fong` | Relationship-Based Access Control (CODASPY 2011) | doi:10.1145/1943513.1943539 | ACM, New York, NY, USA; pp. 191-202 |
| `blaze` | Decentralized Trust Management (IEEE S&P 1996) | doi:10.1109/SECPRI.1996.502679 | IEEE Comput. Soc. Press; pp. 164-173; no publisher-location in Crossref |
| `appel` | Proof-Carrying Authentication (CCS 1999) | doi:10.1145/319709.319718 | ACM, New York, NY, USA; pp. 52-62 |
| `rfc8693` | OAuth 2.0 Token Exchange | doi:10.17487/RFC8693 | RFC Editor |
| `rfc9396` | OAuth 2.0 Rich Authorization Requests | doi:10.17487/RFC9396 | RFC Editor |
| `rfc2693` | SPKI Certificate Theory | doi:10.17487/RFC2693 | RFC Editor |
| `miller` | Robust Composition (JHU PhD thesis, 2006) | JHU JScholarship item `b8376e55-208e-4fcc-81a2-ad5a7de0acbb` | Johns Hopkins University, Baltimore, MD; no DOI |

The existing 8 entries are the frozen canonical references: APC, TraceGrant,
SentinelAgent, Progent, MasDrift, Noma, the IETF draft, and Tallam. Their
bibliographic identities were already checked for the canonical build and were
not changed here.

BibTeX uses all 16 entries. Two completeness warnings remain and are disclosed
rather than papered over:

- `macaroons`: no page numbers in the Crossref record, so none are asserted.
- `blaze`: no publisher-location in the Crossref record, so no address is
  asserted.

The four inproceedings entries now carry verified publisher/address/page
metadata where the record supplies it; the arXiv, blog, and RFC entries carry
their DOI or URL only. The complete list is
`paper/venue_codaspy2027/references.bib`.

## Layout QA

Recorded on the 3 November 2026 build:

```text
Overfull \hbox:      0
Overfull \vbox:      0
Underfull \hbox:   139   (cosmetic; justified lines)
Underfull \vbox:    15   (cosmetic; page fill)
LaTeX Warning:       0
Font Warning:        0
Missing character:   0
Undefined refs/cites: 0
BibTeX warnings:     2   (metadata completeness, listed above)
```

Underfull boxes are loose lines and page-fill slack, not content outside the
text block. They do not affect the page limit or readability gate. If the
venue's review copy is regenerated with a different TeX distribution, re-run
`build.py`; page breaks and these cosmetic counts can shift.

## Build and reproduce

```powershell
cd paper\venue_codaspy2027
python build.py
```

The script runs `xelatex`, `bibtex`, and two more `xelatex` passes, then checks
the page budget, layout counters, anonymity, bibliography size, frozen claim
strings, H4/H7 status, and placeholders. It exits non-zero on any failed gate.

To check the existing PDF without rebuilding:

```powershell
python build.py --skip-build
```

Expected final line:

```text
PASS: all venue checks satisfied (13 pages; 12 main + 1 appendix)
```

## Residual risks and open items

1. **Main-page slack is zero.** The main body ends on page 12 exactly. Any added
   front matter, copyright block, or expanded reference list can push references
   to page 13 and fail the limit. Re-run the gate after final metadata.
2. **Appendix interpretation.** The cut treats the 2-page appendix allowance as
   outside the 12 main pages, per the call for papers. If the chair counts it
   inside, the cut would be over length.
3. **Template drift.** `acmart` v2.20 (2026/08/16) is installed locally. A
   different version may change spacing and page breaks.
4. **Cosmetic warnings.** The 139 underfull hboxes, 15 underfull vboxes, and two
   BibTeX completeness warnings are documented; none is a correctness or
   anonymity failure.
5. **Backport not approved.** The 8 new references are venue-only. Moving them
   into the canonical or arXiv build would change frozen hashes and page counts
   and requires a separate decision.
6. **Release not approved.** Public contact, license, repository URL, DOI,
   arXiv endorsement, and release sanitization remain open.
