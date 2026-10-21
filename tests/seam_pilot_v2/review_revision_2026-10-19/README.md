# Review revision — 2026-10-19

Pre-revision copies kept for audit (this program tree has no git). The live files were corrected per the
independent adversarial review in `..\ADVERSARIAL_REVIEW_RESULTS.md`, **language only — no number, outcome, or case changed**.

## Files here (pre-revision snapshots)
- `claims_update_extension.md.pre_review`
- `EXTENSION_E1_RESULTS.md.pre_review`
- `extension_e1_reports.py.pre_review`

## Changes applied (via editing the generator `extension_e1_reports.py`, then regenerating; verbatim-embed checks passed)
1. Attribution sentence replaced: transport clean / receiver blind decomposition; the family-wide (arm-invariant)
   oracle convention disclosed; composition-attribution question marked **open** with the two discriminating tests named.
2. Arm-6 "Fixes" claim: mapping-doc §8 inherited-trust caveat (fix only relative to a correctly deciding upstream).
3. Not claimed: M2-auth evidence path scoped (tamper-evidence + call-binding under an honest signer with a public key;
   trusted-evidence transport gap narrowed, not closed).
4. Not claimed: seam-test reach caveat (can fire only on widening-type families).
5. Revision note added at the end of the claims record (visible in results §5 embed as well).

Diff verification: in `EXTENSION_E1_RESULTS.md` only the line-count header (433→438), Q1 point 2, and the §5 embed
changed; in `claims_update_extension.md` only the three edits + revision note. No numbers anywhere else.

## Hash notes
- The manifest's recorded `reports.py` sha256 (`935764e6…`) refers to the original `reports.py`, which is unchanged
  and untouched. `extension_e1_reports.py` is not part of any recorded hash, so regenerating invalidates nothing.
- New hashes (post-revision):
  - `results/claims_update_extension.md`: `de555b0fbefc0ccc95432e47aea8c1dd9e9dc333c5982d4531f524968fdf518d`
  - `results/EXTENSION_E1_RESULTS.md`: `96861c2f66550abe89bfed76ea10dc1ac8f4b5ce5ca1e3d26cf8b112c4d866dd`
