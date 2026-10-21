# Future Paper Build — SeamBench (Proposed, Not Committed)

**Status:** proposal only. This folder is outside `paper\` and is not part of the
current manuscript, the frozen evidence set, or any submission package. Nothing
here is a claim about the current paper, and no experiment named here is
authorized by this file.

**Working title:** *SeamBench: A Locked-Artifact Benchmark for Cross-Mechanism
Authorization Seams*

**Relationship to the current paper:** the current manuscript is a
workshop/short-paper or arXiv measurement report. This build is the proposed
full-paper program that would turn the same seam question into a benchmark
contribution. It must not be merged into `paper\MANUSCRIPT.md` or substituted
for the current draft without a separate decision.

## 1. Why a separate build

The current paper is deliberately bounded: three mechanism pairs, one
action-narrowing extension, one boundary study, frozen case sets, and two
untested hypotheses (H4 and H7). A full benchmark paper would need a broader
mechanism matrix, independently authored cases, cross-implementation
replication, and a release process. Those are different claims and different
evidence obligations, so they belong in a separate build with separate locks.

## 2. Proposed scope

### 2.1 Research question

At a cross-mechanism handoff, does the composed system enforce the sender's
narrowing, or does the seam admit calls the narrowing never conferred? The
benchmark would measure the seam case-wise across mechanism pairs, bridge
mappings, and scoring conventions, and would report where composition adds an
authorization failure that neither mechanism exhibits standalone.

### 2.2 Mechanism matrix

Proposed measured mechanisms, subject to pinned versions and independent
verification:

- APC (Agentic Principal Chain), upstream pinned commit.
- TraceGrant, independent Task D implementation.
- SentinelAgent, pinned prototype.
- At least one additional receiver with a different authorization vocabulary.
- At least one non-token delegation mechanism, selected only after a verified
  source review.

Progent remains a close related-work reference, not a baseline. Its reported
numbers stay its authors' self-report. No benchmark number would be attributed
to Progent unless the benchmark actually executes a pinned Progent build.

### 2.3 Bridge families

Carry forward the current taxonomy as the starting point, not as a complete
benchmark:

| Label | Bridge construction | Intended role |
|---|---|---|
| M0 | One-step, transport-faithful, scope-only | Transport control |
| M2 | Digest-only evidence carriage | Evidence control |
| M2-auth | HMAC-signed evidence carriage | Authenticated-evidence control |
| M0-A | M0 with a consuming action-scope gate | Repair variant |
| T0 | Canonical narrowing-preserving mapping | Primary mapping |
| V1 | Manifest derived from pre-narrowing role scope | Deliberate widening |
| V2 | Omitted-recipient default filled into SEND | Deliberate widening |

New bridge families require their own pre-registration, implementation
provenance, and a negative control showing that the bridge can fail.

### 2.4 Case families

- The existing Pilot-1, E1, SentinelAgent, and boundary families, retained as
  frozen regression inputs only.
- Independently authored state/identity cases.
- Action-scope cases with more than one design point and a live parameter axis.
- Bridge-derivation cases that separate transport, manifest derivation, and
  receiver consumption.
- Cross-implementation cases where the same contract is realized twice.
- H4 instrument: a case family that reconstructs authority from a token hash
  chain and compares it with the APC envelope's history.
- H7 instrument: a benign-word override probe for the SentinelAgent intent
  layer, with pre-registered classifications.

H4 and H7 remain `UNTESTED` until their instruments, locks, and analyses are
separately approved.

### 2.5 Arms

Keep the seven-arm structure where it applies: sender-alone, receiver-alone,
scope-only composition, composition with evidence carriage, composition with
fail-closed behavior, and the two mechanism-specific controls. Every arm must
state its own-world authority and its scoring convention. Forced identities
must be labeled forced and must not be counted as evidence about composition.

### 2.6 Scoring conventions

The benchmark would preserve the current four-convention disclosure:

- frozen family-wide;
- arm-native;
- boundary canonical / variant-manifest;
- SentinelAgent arm-invariant.

A benchmark score must name its convention. Convention-invariance is not
assumed. Any new convention requires a pre-registration and a sensitivity
analysis.

## 3. Baselines and comparisons

Proposed baselines, all executed locally and pinned:

1. Sender mechanism alone.
2. Receiver mechanism alone.
3. Scope-only composition.
4. Evidence-carrying composition.
5. Fail-closed composition.
6. A no-op bridge that passes the sender record through unchanged.
7. A deliberately widening bridge as a positive control.

Comparisons must be paired by case, not by aggregate only. No external
self-reported number is used as a baseline. A related-work section may compare
designs conceptually, but not numerically, unless the comparison is executed.

## 4. Metrics

- Case-wise seam predicate: arms 1 and 2 safe while at least one of arms 5, 6,
  or 7 is unsafe.
- Leaked cases and unauthorized-effect events.
- Benign false-denial cases and false-denial events.
- Effective sample size by design point, not by row count.
- Evidence verification and receipt coverage.
- Fail-closed utility cost.
- Convention sensitivity: the same cells under each named convention.
- Reproducibility: lock hash, case-set hash, run-manifest hash, and
  re-execution determinism.
- Reconciliation: every prediction-observation mismatch recorded verbatim,
  with `affects_behavior_cells` stated explicitly.

No aggregate is reported without its component sum. No percentage is reported
without its denominator.

## 5. Replication and artifact release

- Two independent implementations of each bridge where feasible.
- A clean-room re-execution of at least one mechanism pair by a person who did
  not author the original harness.
- Frozen locks before execution; no post-run case edits.
- A release kit containing cases, locks, manifests, traces, scoring code, and
  a reproducibility script.
- A public artifact manifest with hashes; no Poppler or other local QA tool is
  bundled into the release.
- A data-availability statement that distinguishes artifacts from
  third-party mechanisms.

## 6. H4/H7 gates

H4 and H7 are not authorized by the current paper or by this proposal. Before
either becomes a measured claim:

1. Write the instrument design and the null/positive controls.
2. Freeze the case set and predictions.
3. Run the instrument sequentially and offline.
4. Record predictions versus observations verbatim.
5. Reconcile any mismatch without editing the lock.
6. Obtain a separate approval to report the result.

Until then, both stay `UNTESTED` in every public artifact.

## 7. Risks

- **Construct risk:** constructed witnesses are not a benchmark population.
- **Convention risk:** seam counts can move under a different scoring rule.
- **Bridge risk:** a non-narrowing-preserving bridge can create a seam without
  composition; attribution must stay at the bridge layer.
- **Implementation risk:** upstream prototypes are not production systems and
  may change; pins and provenance must be recorded.
- **Comparison risk:** related systems may not expose comparable interfaces;
  conceptual comparison must not become a numeric claim.
- **Release risk:** third-party code and keys may not be redistributable; the
  release must separate original artifacts from dependencies.
- **Scope risk:** a full benchmark can overstate generality; the paper must
  state the mechanism matrix and case-family limits.

## 8. Venue plan

- Primary: a workshop or short-paper track with an artifact-evaluation option.
- Secondary: an arXiv preprint of the full build after the artifact release is
  reproducible.
- Tool track: only if the release kit and reproduction script are the main
  contribution.
- Main-track submission is not assumed and requires a separate readiness
  review.

Venue, page limit, anonymity, reference style, license, repository URL, and
archival DOI remain open decisions.

## 9. Merge and submission gates

This build may not be merged into the current paper until:

- the new mechanism matrix and case families are locked;
- H4/H7 have separate authorization or remain explicitly `UNTESTED`;
- every reported number is generated from a stored artifact;
- the release kit compiles from a clean extraction;
- the public email and license are resolved;
- the current paper's frozen artifacts and hashes remain untouched.

**Proposed owner:** the same program, with a new lock and a new evidence
directory. **Do not reuse** the current `paper\hashes.txt` or
`paper\CONSOLIDATED_CLAIMS.md` as the authority for this future build.
