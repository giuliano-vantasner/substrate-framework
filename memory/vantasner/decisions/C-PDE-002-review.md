---
description: Independent review of C-PDE-002
author: vantasner-review
created: '2026-08-01T20:21:47Z'
updated: '2026-08-01T20:21:47Z'
tags:
- substrate-framework
- claim-review
- radial-moment
- simulation-evidence
category: decisions
confidence: working
status: archived
---
# Review of C-PDE-002

## Claim Under Review

The claim records a resolution-bounded near-two frequency relation between the
energy-radius moment of the localized `C-PDE-001` core and its contemporaneous
field oscillation. It fixes the initial-data branch, time interval, core
cutoffs, estimators, and refinement scope and does not assert an exact global
frequency theorem.

## Sourced Inputs

The review read `v0.39.0`, `C-PDE-001`, P045's frozen contract, extended radial
module and tests, all three attempts, the independent DOP853 review, and
hash-pinned P3D2. The source FFT result is comparison evidence only, and its
assembled zero tensor and physical radiation prose are excluded.

## Independence

The primary route uses centered leapfrog data, the canonical `r^4*T00`
quadrature, a detrended Hann FFT with sub-bin interpolation, and prominent
maximum periods. The independent route uses DOP853 method-of-lines, a local
frequency implementation, and a coarser `dr=0.2` trajectory through `t=300`.
It agrees with leapfrog without importing the campaign verifier.

## Verification Status

The strongest earned status is `simulation_evidence`. The moment formula is
exactly defined and unit-tested, but its evolution, dominant frequency, and
cutoff behavior are finite-grid observations. Clean completion, finite values,
mesh/timestep/domain studies, two settled windows, two estimators, cutoff
sensitivity, an independent integrator, and counterexamples support the
qualified numeric statement.

## Sensitivity and Counterexamples

Meshes `0.1/0.05/0.025`, timestep halving, and domains `160/200/240` retain
near-two ratios. Cutoffs 20, 25, and 30 agree, whereas cutoff 40 fails the
dominant-frequency verdict because `r^4` amplifies a radiative shell and slow
drift. The weak dispersive seed resolves no combined persistent-core moment.
The source's bins 17 and 34 explain its artificial exact ratio. Two preserved
attempt failures repair symbolic normalization and sub-sample peak timing
without changing the physics thresholds.

## Framework Compatibility

The claim is a qualified numerical consumer of `C-PDE-001`. It adds no new
field parameter or scale. `S_R` is a cutoff diagnostic, not a conserved charge;
the accepted cutoffs are part of the claim. The approximately doubled
frequency is compatible with an energy density even in the field but is not
promoted as an exact symmetry theorem for the nonlinear chirping trajectory.

## Dependency and Consumer Replay

The sole accepted dependency is `C-PDE-001`. Direct consumers are the extended
radial evolution record, frequency helpers, P045, and tests. The P044 verifier
is replayed because its canonical solver gained diagnostics. P3D3/P3D4 remain
pending and cannot turn the scalar moment into a nonzero STF source or physical
radiation channel.

## Competing Candidate Audit

Candidate A is selected with an explicit cutoff qualification because all
predeclared numerical gates close on 20 through 30 and the radius-40
counterexample defines the boundary. Candidate B would be selected for an
unrestricted or global moment claim, which the evidence rejects. Candidate C
is structurally incompatible with the absence of gravitational dynamics.

## Four-Axis Decision

The axes preserve the numerical and cutoff ceiling.

- Verification: simulation_evidence
- Review: accepted
- Compatibility: native
- Epistemic: qualified
- Relationship: finite-time diagnostic consumer of C-PDE-001

## Promotion Transaction

Promotion adds moment diagnostics and peak-frequency APIs/tests, immutable
passing and failed evidence, qualified P3D2 disposition, separate numeric
registry entry, release, generated records, and parent synchronization.

## Continuation if Not Accepted

If cutoff 20 through 30 or independent-method closure failed, Candidate B
would retain only `C-MOM-003`; the exact tensor theorem would not be used to
mask the numerical failure.

## Done Gate

Definition, cutoff, solver status, variation, dual frequency routes,
refinements, independent method, counterexamples, source scope, consumers, and
debt are closed.

## Cross-References

See P045, P3D2, `C-PDE-001`, `C-MOM-003`, the radial module, and the parent
migration effort.
