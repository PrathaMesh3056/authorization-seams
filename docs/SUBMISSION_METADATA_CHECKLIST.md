# Submission metadata checklist

**Status:** open. No values are invented here. Fields marked `TBD` require the author or an authorized release decision.

## 1. Manuscript identity

| Field | Current value | Status |
|---|---|---|
| Title | *The Handoff Nobody Owns: A Locked-Artifact Study of Cross-Mechanism Authorization Seams* | Present |
| Abstract | 230 words; rewritten in the 9 November 2026 completion pass with no new experiments, numbers, or citations | Present |
| Keywords | cross-mechanism authorization; agent authorization; authorization seams; scope narrowing; evidence carriage; conformance testing; locked-artifact methodology | Present |
| Current draft | `paper\MANUSCRIPT_REVISED.md` | Present; 884 lines, 171,853 bytes; SHA-256 `CD47F151913AAB5422E26059EE4C474FB703B2254831CA274035C58682B695C7` |
| Current PDF | `paper\drafts\MANUSCRIPT_DRAFT_2026-11-09.pdf` | Present; 38 pages; 385,242 bytes; named-author build; SHA-256 `70F73059168C330703F138404C2F298F7BCE5803CFC749CC27269CBDC3D6FA80` |
| Standalone LaTeX | `paper\latex_export\main.tex` | Present; SHA-256 `0E2FCB09DE5ABEA5DF5459B21D961244D67CBBAC9A4D629DC3D6AAF431BFF26D`; independent XeLaTeX compile verified (38 pages, 385,242 bytes) |
| arXiv PDF | `paper\arxiv_export\main.pdf` | Present; 42 pages; 388,934 bytes; 1-inch margins; named-author `Prathamesh N Patil`; SHA-256 `F3C4C9EB5F8E5E385CC2098286F08CE0A57E7E1AAB4CA4F1B202F06CF23AD093` |
| arXiv LaTeX source | `paper\arxiv_export\main.tex` | Present; generated from the current export; SHA-256 `3C2D57A352F632EEADF9FD30E6B974DF6B5BCE8006EFE37CD7A4151F232381A8` |
| arXiv source package | Superseded: `dist\arxiv\authorization-seams-arxiv-2026-11-07.zip` | Predates the 8-9 November correction passes; do not submit. A fresh package must be generated from the 9 November source. |
| References | Static twenty-one-entry list after Section 9 | Present; first seven identities checked 20 October 2026, MasDrift checked 22 October 2026, RFC 8693/Zanzibar/Macaroons checked 5 November 2026, ten additional entries checked 6 November 2026; claims not reproduced |
| Base draft | archived `MANUSCRIPT.md` (project archive, not this repository) | Preserved, not for merge |

## 2. Authors and affiliations

| Field | Value | Status |
|---|---|---|
| Author order and legal names | Prathamesh N Patil (single author) | CFF, canonical PDF, and arXiv candidate use this form |
| Affiliations | Department of Computer Engineering, Sardar Patel Institute of Technology | Provided 20 Oct 2026; printed in both named-author builds; city/country optional and not yet supplied |
| Emails | `<public-email-unresolved>` (placeholder redacted; not printed on any PDF; replace before submission) | Final public address still needed |
| ORCID iDs | Leave blank - none supplied | Optional; not required for arXiv/most workshops |
| Corresponding author | Prathamesh N Patil | Single-author draft; confirm public email before submission |
| Author contributions | Not required for a single-author paper unless the venue asks | Pending venue check |
| Acknowledgments | `TBD` - use "None" only if true | Missing |

Do not submit with placeholder authors. Do not infer affiliations from the filesystem or account name.

**Named-author build:** the 9 November 2026 canonical PDF prints the author name
and affiliation and carries matching PDF metadata. It is not anonymized; a
double-blind venue requires re-anonymization. The 8 November, 7 November,
6 November, and 31 October PDFs remain archived. The placeholder address is not printed and is redacted in
this checklist.

**Author note:** Prathamesh N Patil is an M.Tech. Computer Engineering student at Sardar Patel Institute of Technology. Student status is context for the affiliation; it is not normally printed as a separate title-page field. The affiliation confirms the academic base and does **not** imply that the institution funded, supervised, or endorsed the work. The canonical 9 Nov PDF, the arXiv candidate, and `CITATION.cff` use `Prathamesh N Patil`; the 6 Nov, 5 Nov, 31 Oct, and 23 Oct PDFs remain archived.

### Affiliation and ORCID guidance

- **No university or employer affiliation:** use `Independent Researcher`. This is acceptable for arXiv and many workshop/tool tracks. Do not name an institution you are not actually affiliated with.
- **Student:** listing the college is truthful but optional for independent work. Use `Department of <subject>, <College>` if you used institutional resources or want your academic base listed; use `Independent Researcher` if the work was entirely self-directed and used no college resources. Listing the college does not imply that it funded, endorsed, or helped with the paper.
- **College name-use rules:** check whether the institution requires approval to use its name. This is separate from whether you may list it as an affiliation.
- **Employed:** use the employer name only if you are willing to have it published and your employer permits it.
- **ORCID is optional.** It is a free persistent researcher identifier, not a submission requirement for arXiv or most workshops. Do not invent one. If you want one, register at <https://orcid.org/register>; it can be added after the draft is built.
- **Email:** A placeholder address is recorded internally and redacted here. It
  is not printed. Replace it with an address you control and are willing to
  display publicly before submission.
- **Single-author paper:** author-contribution and corresponding-author statements are usually trivial or unnecessary; confirm against the target CFP.

## 3. Declarations

| Declaration | Current state | Action |
|---|---|---|
| Ethics / AI use | Manuscript `Declarations` section and Section 3.7 describe AI use in the experiment/artifact pipeline, QA, and manuscript editing; no human-subjects data; synthetic/offline work | Confirm wording and placement for target venue |
| Funding | `Declarations` states no funding source is declared; final funding statement pending author confirmation | Confirm before submission |
| Competing interests | `Declarations` states no competing interests are declared; final confirmation pending | Confirm before submission |
| Author contributions (CRediT) | `Declarations` identifies the sole author and states CRediT roles are pending confirmation | Confirm role list before submission |
| Data availability | `Declarations` describes the artifact tree and pending public archive; no URL/DOI/license asserted | Add release pointer only after the release gate |
| Code availability | Conformance kit exists; repository URL/license/DOI unassigned | Add only after release gate |
| Limitations | `Declarations` cross-references Section 7 and restates the scope limits | Keep synchronized with Section 7 |
| Inclusive language / accessibility | Figures have `<title>`/`<desc>`; not a formal accessibility statement | Check venue requirements |

## 4. arXiv metadata (if arXiv-first)

| Field | Proposed value | Status |
|---|---|---|
| Primary category | `cs.CR` (security) | Proposed; needs final choice |
| Cross-list | `cs.AI` | Proposed; needs final choice |
| License | `TBD` | Author choice; do not assume CC BY; irrevocable per announced version |
| Comments | 42 pages, 2 figures, 19 numbered tables plus Appendix Tables A1 and A2; artifact release pending | Computed from the arXiv build; add a URL only after a public release |
| Journal reference | None | Leave empty unless a venue accepts |
| DOI | arXiv-issued DOI | Generated by arXiv; do not fabricate |
| Endorsement | Check current arXiv policy and whether endorsement is needed | Open; 21 Jan 2026 policy requires institutional email plus prior arXiv authorship for automatic endorsement, otherwise personal endorsement. `cs.CR` maps to the `cs` endorsement domain, not a separate `cs.CR` domain; Prof. Sudhir Dhage has four countable `cs.*` papers and is the first ask. |
| Format | 1-inch margins, 10 pt, letter paper, no line numbers/watermark | Verified 26 Oct 2026; build refreshed 9 Nov 2026 after the second external-review completion pass |

## 5. Venue track

| Field | Current state | Action |
|---|---|---|
| Strategy | arXiv first, then workshop/short or tool track; not main-track | Accepted strategy |
| CODASPY 2027 lead | Verified 26 Oct 2026: research 12 pages, dataset/tool 6 pages, BlueSky 10 (invitation), SoK 15 (invitation); abstract 16 Nov 2026, paper 23 Nov 2026 | Official CFP checked; current 38-page single-column paper is not CODASPY-ready |
| Target track | `TBD` | arXiv-first; choose a workshop/short or tool track after release decisions |
| Page limit | arXiv has no page limit; CODASPY research is 12 pages double-column | Confirm the exact track before formatting |
| Template | Standard `article` / arXiv-style single-column draft | Canonical format selected; use a venue template only after a specific CFP is chosen |
| Anonymity | Named-author build (not anonymized) | arXiv can use the named PDF; a double-blind venue requires a separate anonymized build |
| Reference style | `TBD` | Static list is style-neutral; adapt only after venue selection |
| Artifact/tool-track requirement | Kit release likely required for tool track | Release gate must close first |

## 6. Release package

| Item | Current state | Action |
|---|---|---|
| Repository URL | Not assigned | Create or designate |
| License | Not assigned | Choose compatible license |
| Tagged release / commit | Not assigned | Freeze after sanitization |
| Archival DOI | Not assigned | Use Zenodo/OSF or venue archive if available |
| Sanitization | Pending | Remove secrets, local paths, caches, vendored code with incompatible licenses, and private data |
| Release manifest | `artifacts\sha256sums.txt` covers tracked files; `paper\hashes.txt` remains the six Table 15 hashes | Regenerate after any authorized content change; do not alter `hashes.txt` |
| README / reproduction instructions | Partial | Write for external runner |
| Kit scope statement | Present in Section 8 | Reuse; do not inflate |

## 7. Pre-submission gates

- [x] Figures converted to vector PDF; text selectable; fonts embedded; no rasterization.
- [x] Figure 1 v2 canonical; v1 archived and not embedded.
- [x] Figure 2 included; captions unchanged.
- [x] Body and figure font fallback removed; no Segoe UI Symbol or Lucida Sans Unicode.
- [x] Bibliography identities verified (`references.bib`, `REFERENCE_VERIFICATION.md`); static twenty-one-entry reference list appended, with RFC 8693, Zanzibar, and Macaroons verified 5 Nov 2026 and ten additional entries verified 6 Nov 2026.
- [x] Pointer-only claims retained as clearly marked pointers; their claims are not verified inputs.
- [ ] Venue-specific reference style selected and applied.
- [ ] Author/affiliation/contact/ORCID metadata complete. Named author and affiliation are printed in the current canonical and arXiv builds; the public email remains open.
- [ ] Funding, competing-interest, acknowledgment, and contribution statements complete.
- [ ] AI-use disclosure checked against venue policy.
- [ ] Release tree sanitized; license and repository URL assigned.
- [x] Target CFP checked directly; CODASPY 2027 page limits, anonymity, and deadlines verified 26 Oct 2026; arXiv format verified 26 Oct 2026.
- [x] Factual/traceability correction pass applied; no new claims, experiments, or H4/H7 work. The 23 Oct F1-F13 finalization pass, the F4/F5 wording corrections, the 638 non-vacuity wording correction, the 26 Oct audit correction pass, the 28 Oct path-format correction, the 31 Oct review-correction pass, the 5 Nov declarations/positioning revision, the 6 Nov positioning/related-work revision, and the 8-9 Nov second external-review completion pass are applied. See `docs\REVIEW_CORRECTIONS_2026-10-21.md`, `docs\FINAL_BUILD_QA.md`, `docs\ARTIFACT_SNAPSHOT.md`, and `docs\RESEARCH_STATUS.md`.
- [x] Manuscript compiled; 0 overfull hboxes; 38 pages; 5 cosmetic underfull hboxes; standalone LaTeX export verified.
- [x] arXiv-compliant build created: 42 pages, 1-inch margins, 10 pt, named author; 0 missing glyphs, 0 fatal LaTeX errors, 0 overfull hboxes, 3 cosmetic underfull hboxes. The 7 November source zip is superseded and must be rebuilt from the 9 November source before submission.
- [ ] arXiv endorsement and license selected; public email and optional ORCID finalized.
- [ ] Final QA pass completed after final email and venue metadata; no frozen file changed; no merge into `MANUSCRIPT.md` without approval.

**No submission or merge until every gate is closed.**
