# External Reference Verification

**Date:** 20 October 2026. **Scope:** bibliographic identity only — authors, title, date/version, locator, and status. No full-text reproduction, no re-measurement, no experiments, and no manuscript edits. This file is an addendum to `CITATION_LOCAL_SCOUT.md`; the local-only scout is left unchanged as a record of what was known before external checking.

**Result:** all seven citation targets now have a stable public locator and a verified identity. Four upstream works are arXiv preprints; no peer-reviewed venue was verified for any of them. Two §6 entries are non-peer-reviewed pointers (an industry blog and an Internet-Draft). One §6 entry is a related arXiv preprint. `references.bib` contains the corresponding entries.

## 1. Verification sources

- **arXiv API:** `https://export.arxiv.org/api/query?id_list=...` for the five arXiv IDs.
- **DataCite DOI registry:** `https://api.datacite.org/dois/10.48550/arXiv.<id>` for each arXiv DOI.
- **Noma canonical page:** `https://noma.security/blog/your-agents-are-trusting-each-other-should-they`.
- **IETF Datatracker:** `https://datatracker.ietf.org/doc/draft-diaconu-agents-authz-info-sharing/01/`.

## 2. Verified entries

| Manuscript key / pointer | BibTeX key | Verified identity | Locator | Status |
|---|---|---|---|---|
| `[APC]` | `muruaga2026bounded` | Xabier Muruaga, “Bounded Agents: Delegation Security for Multi-Agent AI Systems,” arXiv:2608.15888v1, 16 Aug 2026, cs.AI | DOI `10.48550/arXiv.2608.15888`; `https://arxiv.org/abs/2608.15888` | Verified arXiv preprint; no peer-reviewed venue verified |
| `[TraceGrant]` | `liao2026tracegrant` | Bohao Liao, Jingchao Wang, Qipeng Song, Jin Cao, Jieling Wang, Boyu Deng, “TraceGrant: A Contract-Governed Security Framework for the Task-Effect Lifecycle of Networked LLM Agents,” arXiv:2608.21126v1, 21 Aug 2026, cs.CR | DOI `10.48550/arXiv.2608.21126`; `https://arxiv.org/abs/2608.21126` | Verified arXiv preprint; no peer-reviewed venue verified |
| `[SentinelAgent]` | `patil2026sentinelagent` | KrishnaSaiReddy Patil, “SentinelAgent: Intent-Verified Delegation Chains for Securing Federal Multi-Agent AI Systems,” arXiv:2604.02767v1, 3 Apr 2026, cs.CR | DOI `10.48550/arXiv.2604.02767`; `https://arxiv.org/abs/2604.02767` | Verified arXiv preprint; **no IEEE TDSC venue or DOI verified** |
| `[Progent]` | `shi2025progent` | Tianneng Shi, Jingxuan He, Zhun Wang, Hongwei Li, Linyu Wu, Wenbo Guo, Dawn Song, “Progent: Securing AI Agents with Privilege Control,” arXiv:2504.11703v3, revised 14 May 2026, cs.CR | DOI `10.48550/arXiv.2504.11703`; `https://arxiv.org/abs/2504.11703` | Verified arXiv preprint; original 2025, v3 note retained; no peer-reviewed venue verified |
| Noma (Apr 2026) | `noma2026agents` | Noma Security, “Your Agents Are Trusting Each Other - Should They?”, 23 Apr 2026; canonical page byline: Diana Kelley | `https://noma.security/blog/your-agents-are-trusting-each-other-should-they` | Verified industry blog; not peer reviewed |
| IETF draft (revised Aug 2026) | `diaconu2026authz` | Jean Diaconu, Marcelo Yannuzzi, Hervé Muyal, Frank Brockners, Nik Kale, Ankit Agarwal, Jeffrey Hickman, Amritha Lal, “Cross-Domain AuthZ Information sharing for Agents,” `draft-diaconu-agents-authz-info-sharing-01`, 4 Aug 2026 | `https://datatracker.ietf.org/doc/draft-diaconu-agents-authz-info-sharing/01/` | Verified active individual Internet-Draft; expires 5 Feb 2027; not endorsed by the IETF |
| arXiv 2605.05440 | `tallam2026authorization` | Krti Tallam, “Authorization Propagation in Multi-Agent AI Systems: Identity Governance as Infrastructure,” arXiv:2605.05440v1, 6 May 2026, cs.AI | DOI `10.48550/arXiv.2605.05440`; `https://arxiv.org/abs/2605.05440` | Verified related arXiv preprint; not reproduced |

## 3. Discrepancy decisions

1. **SentinelAgent venue.** The local upstream README carries an “IEEE TDSC” badge whose link is `https://doi.org/TBD`. No IEEE TDSC record was found, and the arXiv API and DataCite record show no journal reference or venue DOI. The bibliography therefore cites arXiv only. Do not restore the IEEE TDSC label without a live venue/DOI record.
2. **TraceGrant venue.** The arXiv record has no `journal_ref` and no DOI beyond the arXiv DOI. The manuscript’s §2 claims are about the arXiv text; the bibliography cites arXiv only.
3. **APC venue.** The arXiv record has no `journal_ref`; it is cited as an arXiv preprint, primary class cs.AI.
4. **Progent date.** The original submission is 16 Apr 2025; v3 was revised 14 May 2026. The entry uses year 2025 and records the v3 revision in `note`, matching the original/v3 distinction already noted in `CITATION_LOCAL_SCOUT.md`.
5. **Noma byline.** The canonical page displays Diana Kelley as the byline and 23 Apr 2026 as the date. An external search snippet also surfaced Gal Moyal, but the canonical page does not show a co-byline. The entry uses corporate author `Noma Security` to avoid asserting an unverified individual co-authorship, with Diana Kelley recorded in `note`.
6. **IETF status.** The document is an active individual Internet-Draft, not an RFC or an IETF-endorsed standard. It declares “Intended status: Standards Track” but has no formal standards standing. Cite it as work in progress, not as an adopted protocol.
7. **arXiv 2605.05440 title.** The full title includes the subtitle “Identity Governance as Infrastructure”; the manuscript pointer uses only the main title. The bibliography preserves the full verified title.

## 4. Manuscript guard language - historical (pre-integration)

**Superseded by Section 6 below.** This section records the pre-integration
state and is not the current manuscript wording.

The manuscript still carries the pre-verification language because changing it would alter a claim surface, not just a reference list. In particular:

- §2 says “citations are unverified.”
- §6 says the industry/standards pointers are “unverified; nothing is fetched.”

Verification of bibliographic identity does **not** mean the works were reproduced, their claims confirmed, or their full texts assessed. Proposed replacement language, for approval only:

- §2: “bibliographic identities were checked against public records on 20 October 2026; the works themselves were not reproduced.”
- §6: “these are pointers to external sources; their bibliographic identities were checked on 20 October 2026, but their claims were not reproduced and none is treated as a verified input to this manuscript.”

No manuscript file was changed in this pass. The guard language remains accurate until those edits are approved.

## 5. Remaining reference tasks

- Choose the reference style required by the target venue or arXiv template.
- The three Section 6 pointers remain descriptive (no bracketed keys); this was confirmed during the 21 October 2026 integration.
- Add author/venue metadata and release information once those are supplied.
- Do not add a peer-reviewed venue claim for APC, TraceGrant, SentinelAgent, or Progent without a live record.
- Re-check all locators immediately before submission; metadata can change.

**Counts:** 7 verified targets = 4 arXiv upstream works + 1 related arXiv preprint + 1 industry blog + 1 Internet-Draft. `references.bib` contains 7 entries.

## 6. Integration update - 21 October 2026

The approved Progent replacement and the static seven-entry reference list are
now in `paper\MANUSCRIPT_REVISED.md` (SHA-256
`27B253EB22C52D81B70585EC1B801760DA001B47F79C4AA8D0CA60837F0ACC8C`).

- Section 2 now describes Progent as a close reference point on monotonic
  confinement inside one privilege-control layer, not as an unread pointer.
- Section 2 guard language now says "citations are pointers, not verified
  inputs"; it no longer says "citations are unverified."
- Section 6 now says the industry/standards pointers' bibliographic identities
  were checked while their claims remain unverified, and removes the stale
  "Progent remains unread" wording.
- The static list is embedded after Section 9. It is style-neutral and not a
  venue-formatted bibliography.
- This remains an identity-verification record: no full text was reproduced,
  no upstream claim was verified, and no Progent experiment was run.

## 7. Addendum - 22 October 2026: MasDrift (eighth entry)

MasDrift was authorized as an eighth reference on 22 October 2026 and judged
important for related-work positioning as the closest prior work in kind.
Bibliographic identity was verified against the live arXiv record and its
version history:

| Manuscript key | BibTeX key | Verified identity | Locator | Status |
|---|---|---|---|---|
| `[MasDrift]` | `xu2026masdrift` | Zhuoning Xu, Xiucheng Zhang, Hanjun Luo, Yingbin Jin, Yinpeng Dong, Hanan Salam, “MasDrift: Benchmarking Authorization Preservation Across Multi-Agent Architectures,” arXiv:2608.07556v3 (v1 2 Aug 2026; v2 11 Aug 2026; v3 15 Oct 2026), cs.MA | DOI `10.48550/arXiv.2608.07556`; `https://arxiv.org/abs/2608.07556` | Verified arXiv preprint; no peer-reviewed venue verified |

The manuscript cites **v3**, the latest version at verification.

- The addition is a scale/design distinction in Section 6 only: MasDrift studies
  authorization preservation across multi-agent coordination architectures
  using benign productivity tasks; this paper is a small deterministic
  conformance study of two specific public authorization artifacts and their
  argument-binding paths. No MasDrift number is reproduced, re-measured, or
  compared.
- No claim, experiment, or H4/H7 status changed; the abstract remains
  byte-identical
  (`CD2278607B491BD49FE7A03585979B259BFD187B0E9C0F9D7D1D4181573B9654`,
  222 words).
- Counts are now **8 verified targets = 4 arXiv upstream works + 2 related
  arXiv preprints + 1 industry blog + 1 Internet-Draft**; `references.bib`
  contains 8 entries.

**Manuscript identity after the addition:** `paper\MANUSCRIPT_REVISED.md`,
553 lines, 110,031 bytes, SHA-256
`18480AE19967FCA9DF6BBAFBFF88580981D5DC3169A53A11044758B9AB55B780`.

