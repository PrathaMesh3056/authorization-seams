# Submission metadata checklist

**Status:** open. No values are invented here. Fields marked `TBD` require the author or an authorized release decision.

## 1. Manuscript identity

| Field | Current value | Status |
|---|---|---|
| Title | *The Handoff Nobody Owns: Measuring What Cross-Mechanism Authorization Seams Cannot Carry* | Present |
| Abstract | 222 words; no new numbers, claims, statuses, or citations | Present, frozen guardrail |
| Keywords | cross-mechanism authorization; agent authorization; authorization seams; scope narrowing; evidence carriage; conformance testing; locked-artifact methodology | Present |
| Current draft | `paper\MANUSCRIPT_REVISED.md` | Present; SHA-256 `1F82A0ED02CF02405FD8076EDAD74B9ADD2130F154D38F87CE493F80D00E6510` |
| Current PDF | `paper\drafts\MANUSCRIPT_DRAFT_2026-10-23.pdf` | Present; 24 pages; named-author build; SHA-256 `086F0F6D451060644DA1C9A8F22DDA985A0F2B16D90A4B9D4BDDF22638BD67AC` |
| Standalone LaTeX | `paper\latex_export\main.tex` | Present; SHA-256 `28EA541F13643026DA05BCC906CCC2649C08ED1BDA630DCBCF8FF6495B00A8DB`; independent XeLaTeX compile verified (24 pages) |
| References | Static eight-entry list after Section 9 | Present; first seven identities checked 20 October 2026, MasDrift checked 22 October 2026; claims not reproduced |
| Base draft | `paper\MANUSCRIPT.md` | Preserved, not for merge |

## 2. Authors and affiliations

| Field | Value | Status |
|---|---|---|
| Author order and legal names | Prathamesh Patil (single author) | Provided 20 Oct 2026; printed in the 23 Oct named-author build |
| Affiliations | Department of Computer Engineering, Sardar Patel Institute of Technology | Provided 20 Oct 2026; printed in the 23 Oct named-author build; city/country optional and not yet supplied |
| Emails | `<public-email-unresolved>` (placeholder redacted; not printed on the draft PDF; replace before submission) | Final public address still needed |
| ORCID iDs | Leave blank - none supplied | Optional; not required for arXiv/most workshops |
| Corresponding author | Prathamesh Patil | Single-author draft; confirm public email before submission |
| Author contributions | Not required for a single-author paper unless the venue asks | Pending venue check |
| Acknowledgments | `TBD` - use "None" only if true | Missing |

Do not submit with placeholder authors. Do not infer affiliations from the filesystem or account name.

**Named-author build:** the 23 October 2026 PDF prints the author name and
affiliation and carries matching PDF metadata. It is not anonymized; a
double-blind venue requires re-anonymization. The placeholder address is not
printed and is redacted in this checklist.

**Author note:** Prathamesh Patil is an M.Tech. Computer Engineering student at Sardar Patel Institute of Technology. Student status is context for the affiliation; it is not normally printed as a separate title-page field. The affiliation confirms the academic base and does **not** imply that the institution funded, supervised, or endorsed the work.

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
| Ethics / AI use | Section 3.7 describes AI-assisted drafting, review, and QA; no human-subjects data; synthetic/offline work | Confirm wording and placement for target venue |
| Funding | `TBD` | Add or state "none" only if true |
| Competing interests | `TBD` | Add or state "none" only if true |
| Data availability | Artifact tree exists; release not sanitized | Add only after release gate |
| Code availability | Conformance kit exists; repository URL/license/DOI unassigned | Add only after release gate |
| Inclusive language / accessibility | Figures have `<title>`/`<desc>`; not a formal accessibility statement | Check venue requirements |

## 4. arXiv metadata (if arXiv-first)

| Field | Proposed value | Status |
|---|---|---|
| Primary category | `cs.CR` (security) | Proposed; needs final choice |
| Cross-list | `cs.AI` | Proposed; needs final choice |
| License | `TBD` | Author choice; do not assume CC BY |
| Comments | Page count, figure/table count, artifact URL | Compute after PDF and release |
| Journal reference | None | Leave empty unless a venue accepts |
| DOI | arXiv-issued DOI | Generated by arXiv; do not fabricate |
| Endorsement | Check current arXiv policy and whether endorsement is needed | Open |

## 5. Venue track

| Field | Current state | Action |
|---|---|---|
| Strategy | arXiv first, then workshop/short or tool track; not main-track | Accepted strategy |
| CODASPY 2027 lead | Research 12 pages, dataset/tool 6 pages, BlueSky 10, SoK 15; no short-paper category | Unverified lead; check official CFP |
| Target track | `TBD` | Choose after CFP check |
| Page limit | `TBD` | Confirm in CFP |
| Template | Standard `article` / arXiv-style single-column draft | Canonical format selected; use a venue template only after a specific CFP is chosen |
| Anonymity | Named-author build (not anonymized) | A double-blind venue requires re-anonymization; single-blind/arXiv can use the named PDF |
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
| Release manifest | `paper\hashes.txt` covers the six Table 15 hashes only | Build a full artifact manifest; do not alter `hashes.txt` |
| README / reproduction instructions | Partial | Write for external runner |
| Kit scope statement | Present in Section 8 | Reuse; do not inflate |

## 7. Pre-submission gates

- [x] Figures converted to vector PDF; text selectable; fonts embedded; no rasterization.
- [x] Figure 1 v2 canonical; v1 archived and not embedded.
- [x] Figure 2 included; captions unchanged.
- [x] Body and figure font fallback removed; no Segoe UI Symbol or Lucida Sans Unicode.
- [x] Bibliography identities verified (`references.bib`, `REFERENCE_VERIFICATION.md`); static eight-entry reference list appended.
- [x] Pointer-only claims retained as clearly marked pointers; their claims are not verified inputs.
- [ ] Venue-specific reference style selected and applied.
- [ ] Author/affiliation/contact/ORCID metadata complete. Named author and affiliation are printed in the 23 Oct build; the public email remains open.
- [ ] Funding, competing-interest, acknowledgment, and contribution statements complete.
- [ ] AI-use disclosure checked against venue policy.
- [ ] Release tree sanitized; license and repository URL assigned.
- [ ] Target CFP checked directly; page limit, template, anonymity, and reference style confirmed.
- [x] Factual/traceability correction pass applied; no new claims, experiments, references, or H4/H7 work. The 23 Oct F1-F13 finalization pass and the F4/F5 wording corrections are also applied. See `paper\agent_reports\REVIEW_CORRECTIONS_2026-10-21.md`, `paper\agent_reports\FINAL_BUILD_QA.md`, and `paper\RESEARCH_STATUS.md`.
- [x] Manuscript compiled; 0 overfull hboxes; 24 pages; standalone LaTeX export verified. The 23 Oct named-author build places the Table 15 caption and body together on page 23.
- [ ] Final QA pass completed after final email and venue metadata; no frozen file changed; no merge into `MANUSCRIPT.md` without approval.

**No submission or merge until every gate is closed.**
