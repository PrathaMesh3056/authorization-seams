# CODASPY 2027 Cut Plan

**Canonical source:** `paper/MANUSCRIPT_REVISED.md` (32 pages as of the 6 November
2026 revision; this cut was built against the 31 October 29-page snapshot)
**Venue target:** `paper/venue_codaspy2027/main.tex` (13 pages, ACM `sigconf`
double column)
**Date:** 3 November 2026 (positioning hardened 4 November 2026)

## Purpose

Produce a venue-ready CODASPY 2027 research-track cut that meets the 12-page
double-column limit without changing the frozen evidence, the claim set, or the
canonical preprint. The 31 October 29-page build and 32-page arXiv candidate
were the stable inputs when this cut was made; the current 6 November canonical
is 32 pages and the arXiv candidate is 35 pages. This venue cut has not been
rebuilt against the 6 November source.

This is a **separate cut**, not a backport. New positioning references,
compressed prose, and renumbered tables exist only under
`paper/venue_codaspy2027/`.

## Budget and result

| Component | Limit | Result |
|---|---|---|
| Main body + references | 12 pages, double column | 12 pages (pages 1-12) |
| Appendix | 2 pages, one column | 1 page (page 13) |
| Total PDF | 14 pages maximum under this reading | 13 pages |
| Main tables | No fixed limit | 4 |
| Figures | No fixed limit | 2 |
| Appendix tables | No fixed limit | 4 |
| References | No fixed limit | 19, all cited |

The main limit is met exactly. There is no spare page for added front matter or
a copyright block; the gate must be re-run after final metadata is added.

## What is preserved

- Every frozen count in the claim set: the 2,446-execution ledger, Pilot-1
  24/40 with 26 events and 0/40 novelty, SentinelAgent 28/48 with 30 events and
  0/48 novelty, E1 4/4 arm-native vs. 0/4 family-wide, boundary 32 = 28 + 4
  with 34 events, and fail-closed 20 benign false denials / 28 FD events.
- Every load-bearing caveat: construction-forced pair zeroes, the E1
  convention dependence, the single design point, the boundary's thin attack
  structure, arm-6 trusted-key assumption, arm-7 utility cost, M2-auth's lack
  of authenticated transport, and the keyholder finding.
- All hypothesis statuses, including H4 and H7 as `UNTESTED`.
- The no-new-experiments, no-re-scoring, no-claim-upgrade rule.
- The canonical bibliography as it stood when this cut was built, plus the
  positioning anchors described under Reference changes; the 6 November
  canonical revision has not been back-ported.

## Section mapping

| Canonical | Venue cut | Treatment |
|---|---|---|
| Abstract | Abstract | Condensed; claim, method, scope, and non-claims retained |
| 1. Introduction | 1. Introduction | Condensed; contribution, headline counts, and non-claims retained |
| 2. Background | 2. Background and the Uncovered Slot | Condensed; APC, TraceGrant, SentinelAgent, Progent positioning retained |
| 3.1 Pre-registration by lock | 3.1 Pre-registration by lock | Condensed; five-stage protocol retained |
| 3.2 Formal core | 3.2 The formal core | Condensed; definitions, blindness observation, narrowing preservation, taxonomy retained |
| 3.3 Seam test and two readings | 3.3 The seam test and two readings | Retained with equations |
| 3.4 Scoring conventions | 3.4 Scoring conventions and execution ledger | Conventions folded into prose; ledger table retained |
| 3.5 Execution ledger | 3.4 Scoring conventions and execution ledger | Merged with 3.4 |
| 3.6 Review loop | 3.1 and 8 | Folded into method and reproducibility prose |
| 3.7 Ethics, AI use, reflexivity | 3.5 Threat model, ethics, and scope | Condensed into one paragraph |
| 3.8 Threat model | 3.5 Threat model, ethics, and scope | Condensed; adversary and out-of-scope list retained |
| 3.9 Hypothesis key | Appendix A1 | Moved to lineage table; statuses also in body |
| 4.1 Pilot 1 | 4.1 Pilot 1 | Condensed; per-template detail moved out |
| 4.2 Extension E1 | 4.2 Extension E1 | Condensed; resolving tests described in text |
| 4.3 SentinelAgent pair | 4.3 SentinelAgent pair | Condensed; signature family moved to Appendix A2 |
| 4.4 Boundary | 4.4 Boundary | Condensed; absolute-plus-delta matrix moved to Appendix A4 |
| 4.5 Cross-cutting synthesis | 4.5 Cross-cutting synthesis | Condensed; two-reading table retained |
| 5. Discussion | 5. Discussion | Condensed to practical question, E1 locus, repairs, H5, statuses |
| 6. Related work | 6. Related Work | Condensed; 8 verified anchors added here |
| 7. Threats to validity | 7. Threats to Validity | Condensed; construct/internal/external/open hypotheses retained |
| 8. Reproducibility | 8. Reproducibility and Artifacts | Condensed; ledger, controls, release-candidate limits retained |
| 9. Conclusion | 9. Conclusion | Condensed; statuses and non-claims retained |
| Appendix A | Appendix A | One-column; A1 lineage, A2 signatures, A3 field audit, A4 boundary detail |

## Table mapping

| Canonical table | Venue table | Treatment |
|---|---|---|
| Table 3, execution ledger | Table 1 | Kept, restated as the explicit sum |
| Table 4, Pilot-1 arm outcomes | Table 2 | Kept, condensed |
| Table 5, Pilot-1 leak classes | - | Folded into Section 4.1 prose; headline counts retained |
| Table 6, E1 outcome matrix | Table 3 | Kept; arm-6 verification moved to caption/text |
| Table 7, E1 resolving tests | - | Folded into Section 4.2 prose |
| Table 8, SentinelAgent per-template | - | Folded into Section 4.3 prose; counts retained |
| Table 9, SentinelAgent signatures | Table A2 | Moved to appendix |
| Table 10, boundary absolute-plus-delta | Table A4 | Moved to appendix |
| Table 11, boundary seam counts | - | Folded into Section 4.4 prose |
| Table 12, two readings | Table 4 | Kept |
| Table 13, field audit | Table A3 | Moved to appendix |
| Table 14, claim locus synthesis | - | Statuses folded into Sections 4.5, 5, and 9 |
| Table 15, repair patterns | - | Folded into Section 5 repair prose |
| Table 16, threat ledger | - | Folded into Section 7 prose |
| Table 17, artifact hashes | - | Full values remain in the canonical ledger and `hashes.txt`; prose retains the citation-aid pointer |
| Table A1, hypothesis lineage | Table A1 | Kept |
| Tables 1-2, formal spines and scoring conventions | - | Folded into Sections 2 and 3.4 prose |

Net: 10 canonical tables were removed or folded into prose; 8 tables remain
(4 main, 4 appendix). No canonical table row that carries a frozen claim count
was dropped without its count appearing in the venue text.

## Figure mapping

| Canonical figure | Venue figure | Treatment |
|---|---|---|
| Figure 1, handoff anatomy | Figure 1 | Kept; width set to `0.95\columnwidth` |
| Figure 2, repair loci | Figure 2 | Kept; width set to `0.9\columnwidth` |

Both figures are schematic and carry no data, so they consume space without
adding evidentiary weight. They were retained because they carry the paper's
central vocabulary: the carried record vs. the receiver's read set, and the two
repair loci.

## Reference changes

The venue cut carries 19 entries: six core mechanism or standards entries (APC,
TraceGrant, SentinelAgent, Progent, MasDrift, and the IETF individual
Internet-Draft) plus thirteen positioning anchors. The first eight anchors were
added with the original cut:

1. Macaroons (NDSS 2014), DOI `10.14722/ndss.2014.23212`
2. Fong, relationship-based access control (CODASPY 2011), DOI
   `10.1145/1943513.1943539`
3. Blaze, Feigenbaum, and Lacy, decentralized trust management (IEEE S&P 1996),
   DOI `10.1109/SECPRI.1996.502679`
4. Appel and Felten, proof-carrying authentication (CCS 1999), DOI
   `10.1145/319709.319718`
5. RFC 8693, DOI `10.17487/RFC8693`
6. RFC 9396, DOI `10.17487/RFC9396`
7. RFC 2693, DOI `10.17487/RFC2693`
8. Miller, robust composition (JHU PhD thesis, 2006; no DOI)

The 4 November hardening added five 2026 anchors:

9. Parisel, A Theory of Least Autonomy in AI (arXiv:2607.09744)
10. ChainCaps (arXiv:2605.26542)
11. Overlaying Governance (arXiv:2606.03518)
12. PEDIGREE (IETF draft-rampalli-pedigree-00; expired)
13. Local Allow, Global Deny (arXiv:2610.27620)

These anchors answer the "positioning is thin" review concern without turning
the paper into a survey. They are cited in Section 6 and are not baselines; no
numbers are compared. Verification is recorded in `COMPLIANCE.md`.

The venue cut has not been rebuilt against the 5 November or 6 November
canonical revisions. The 6 November canonical has 21 entries and contains all
19 venue entries except PEDIGREE, plus Noma, Tallam, and Zanzibar. A rebuild
would change frozen hashes and page counts and is a separate approval decision.

## Compression decisions

1. **Keep every count that carries a claim.** Per-template tables were collapsed
   only after the headline counts and their denominators were retained in prose
   or a main table.
2. **Keep every caveat that limits a claim.** The cut removes repetition, not
   qualifications. Forced identities, convention dependence, single-design-point
   warnings, and repair costs remain.
3. **Move detail, not evidence, to the appendix.** The appendix holds lineage,
   signature cells, the field audit, and the boundary matrix. It is one column
   and one page.
4. **Drop administrative inventories.** The threat ledger, artifact hash table,
   and claim-locus table are navigation aids; their content survives in prose,
   the canonical manuscript, and `hashes.txt`.
5. **Do not add results.** No new experiment, no re-scoring, no new claim, and
   no status upgrade. H4 and H7 stay `UNTESTED`.
6. **Compress references carefully.** Redundant URLs and `howpublished` fields
   were removed where a DOI identifies the work; DOI metadata was retained.
   Missing page/address fields are left missing rather than invented.

## Verification

From `paper/venue_codaspy2027/`:

```powershell
python build.py
```

The gate checks:

- main body + references at most 12 pages;
- appendix at most 2 pages;
- no overfull hboxes or vboxes;
- no undefined references or citations;
- no missing glyphs, font warnings, or acmart accessibility warnings;
- 19 bibliography entries;
- anonymous body and blank PDF author metadata;
- every frozen claim string;
- H4 and H7 `UNTESTED`;
- no `TODO`/`XXX`/`PLACEHOLDER`/`TBD`.

Expected final line:

```text
PASS: all venue checks satisfied (13 pages; 12 main + 1 appendix)
```

## Open decisions

1. Backport the 8 anchors to the canonical/arXiv builds? Not approved; would
   change frozen hashes and page counts.
2. Accept the current cosmetic residuals (139 underfull hboxes, 15 underfull
   vboxes, 2 BibTeX completeness warnings)? They do not fail any gate.
3. Final venue metadata, license, public contact, repository URL, and DOI.
4. Submission approval. Nothing is submitted or pushed.
