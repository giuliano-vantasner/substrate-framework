---
description: Derive normalized whole-line overlap ledgers and audit MH1
author: vantasner
created: '2026-08-03T05:25:00Z'
updated: '2026-08-03T06:10:00Z'
tags:
- substrate-framework
- campaign-proposal
- normalized-overlap
- migration-MH1
category: proposals
confidence: exploratory
status: archived
---
# P070 MH1 Normalized Overlap Audit

## Question and Positive Deliverable

P070 must deliver importable exact expectation bounds, hyperbolic-secant
overlap formulas for declared normalized modes, and a dimension-complete free-
parameter ledger for a conditional mass map. Reproducing `9*pi/32` or rejecting
Hessian eigenvalues as masses does not complete the campaign.

## Base Release and Provenance

The accepted base is `v0.63.0` at scientific commit `b2ccced`; parent-effort
synchronization is commit `d808fc8`. The predecessor is pinned at
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`. MH1 is
`/home/dan/substrate/merged-framework/bridges/phase-20/bridge_MH1_yukawa_overlap_mass_formula.py`,
17788 bytes, with inventory and reproduced SHA-256
`6e32edbd129c40ed587408fa70128951f65c04f379a633414fd8202e80ca1854`.
The generated queue marks MH1 pending and names EM6, FG2, MH2, and MH3. EM6
and FG2 are qualified through accepted C-QBL-001 and C-QBL-003; MH2 and MH3
remain pending. The clean framework tree, recent history, seven-check
preflight, registry, current release, accepted quartic profile and fluctuation
modules, generated synopsis, package searches, templates, and durable memory
were inspected before this contract. Memory contains no accepted normalized
profile-expectation theorem. MH1's executable body and detailed output remain
unopened.

## Invariants, Conventions, and Allowed Imports

C-QBL-003 supplies two exact modes of one conditional scalar Hessian and
already denies that their negative and zero eigenvalues are positive masses or
generations. C-QBL-001 supplies a conditional quartic sech profile, not a
physical condensate or Yukawa sector. P070 may use exact beta/gamma integrals
and normalized L2 expectation bounds. The domain, measure, conjugation,
normalization, profile sign, inverse width, amplitude, exponent, dimensions,
and free mass-map scale remain visible. Cartesian `dx` is not a radial measure.
MH2/MH3 supply no hierarchy or mixing premise.

## Candidate Preregistration

The candidate set is frozen before MH1's executable is opened.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal MH1 | Its profiles, normalization, measure, dimensions, and mass map are fully typed | source inputs | Narrow ratios may survive; generation and absolute-mass readings likely require missing premises | Hash-pinned execution and data-flow audit |
| B | General expectation theorem | Normalized L2 mode and bounded real multiplier | mode and profile | The overlap lies in the profile's essential range and is positive only conditionally | Direct integral inequality and sign counterexamples |
| C | Sech-power gamma ratio | Whole-line `dx`, positive width and admissible powers | `A,kappa,p,r` | Width cancels only when mode and multiplier share it; p=2,r=1 gives `9*pi*A/32` | Independent beta substitutions and exponent mutations |
| D | Accepted even/odd modes | C-QBL-003 shapes under the same declared multiplier | `A,kappa` | Squared-density overlaps are positive, but parity controls cross terms | Exact even/odd integrals and reflection probes |
| E | Dimension/free-parameter ledger | A separately declared map `m=y*v` | profile and scale dimensions | `dim(y)=dim(profile)` and both amplitude and `v` remain free | Rescaling null directions and dimensional balance |
| F | Spectral ceiling | C-QBL-003 only | `kappa` | Negative/zero Hessian levels are not positive masses but do not select a replacement | Logical countermodel with another declared positive functional |

## Selection Criteria and Blinding

Selection is ordered by accepted closure; exact measure, normalization,
conjugation and gamma factors; dimension and parameter completeness; correct
amplitude, width, exponent and parity limits; mutation sensitivity; and a
strict physical ceiling. The source's `9*pi/32` and familiar Yukawa language
cannot select a mass mechanism or generation interpretation.

## Proposed Claim Delta

Provisional C-OVL-001 may state general normalized expectation bounds, exact
sech-power and accepted-mode overlap ratios, and the dimensions and free
directions of a declared `m=y*v` map. It may depend on C-QBL-001 and C-QBL-003
only for their conditional profile and modes. It may not establish a Yukawa
interaction, fermion field or chirality, generation assignment, hierarchy,
mixing, physical condensate, absolute mass, Standard-Model mapping, or
substrate realization.

## Implementation and Oracle Plan

A pure `normalized_overlaps.py` module may expose sech-power whole-line
integrals, normalization factors, exact normalized multiplier overlaps,
C-QBL-003 even/odd-mode ratios, expectation bounds, and a dimension/free-scale
ledger. SymPy exact gamma algebra and integration fit the claim. An independent
route will derive the integrals from a beta substitution and reconstruct the
mode normalizations without importing the canonical API. Mutations will omit
normalization, change `dx` to a radial weight, drop conjugation, hard-code the
ground coefficient, mismatch widths, hide amplitude or free scale, and treat
the spectral no-go as uniqueness. No numerical quadrature is appropriate for
these closed-form whole-line integrals. Canonical code therefore needs neither
`np.trapz` nor `np.trapezoid`.

## Attempts and Continuation

Attempt 0001 will preserve MH1's native process and trace every assertion. If
the source copies mode shapes, verifies only selected integer powers, omits
dimensions, or converts a definition into a mechanism, that failure is
recorded and Candidates B-E continue. Candidate F cannot close P070 alone.

## Debt Ledger

The campaign tracks normalization, measure, profile, dimension, dependency,
interpretation, verification, and synchronization debt.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| MH1's executable and output are unaudited | Hash-check, execute, preserve output, and trace all checks | discharged by attempt 0001 and source audit |
| The overlap measure, conjugation, and normalization may be incomplete | Derive the normalized expectation and exact whole-line ratios from declared inputs | discharged by the expectation theorem and exact mode ledgers |
| The profile family and width cancellation may be overgeneralized | State admissible powers, matched-width premise, and mismatch counterexample | discharged by the positive-power domain and matched-width ceiling |
| The conditional mass map may hide dimensions and free scales | Expose the complete dimension and rescaling ledger | discharged by the dimension and reciprocal-rescaling ledger |
| Pending MH2/MH3 or physical generation language may be imported | Audit source data flow and exclude hierarchy, mixing, and particle premises | discharged; MH2/MH3 and physical flavor premises are excluded |
| Verifier sensitivity, review, and synchronization are incomplete | Complete mutations, independent derivation, impact replay, claim review, disposition, release, docs, queue, and memory | discharged at the v0.64.0 promotion boundary |

## Review and Promotion Plan

Any proposed claim receives independent review of the beta/gamma normalization,
expectation bounds, even/odd mode integrals, measure sensitivity, matched-width
scope, dimensions, free directions, and interpretation ceiling. MH1 receives a
terminal disposition only through the authoritative queue with durable
evidence. Accepted logic moves into the package with focused tests and one full
promotion-boundary workflow gate.

## Done Gate

P070 closes only when the positive importable overlap ledger, sensitive exact
oracles, independent derivation, source adjudication, claim-level decision,
downstream replay, canonical synchronization, and empty campaign debt all
pass. A coefficient or source no-go alone is not completion.

## Adjudication Outcome

Candidates B through E are accepted in C-OVL-001. Candidate A survives only
for its narrow matched-width ratios and common-width cancellation; Candidate F
remains C-QBL-003's existing interpretation ceiling and supplies no selection
principle. MH1 is qualified. The primary route passes 51 checks, the
independent route passes 20 checks, focused/governance replay passes 38 tests,
and the full workflow passes all 582 tests. The v0.64.0 registry, release,
queue, generated docs, and accepted memory agree.

## Cross-References

See C-QBL-001, C-QBL-003, MH1's generated source record, release `v0.63.0`, and
the parent migration effort.
