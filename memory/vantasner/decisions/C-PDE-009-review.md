---
description: Independent review of C-PDE-009 real-l2 m-degeneracy and averaging ceiling
author: vantasner-review
created: '2026-08-02T11:20:00Z'
updated: '2026-08-02T11:20:00Z'
tags:
- substrate-framework
- claim-review
- l2-perturbation
category: decisions
confidence: established
status: active
---
# C-PDE-009 Claim Review

## Claim Under Review

The proposed claim states that every declared real ℓ=2 angular quadratic
has eigenvalue -6, so a radial background gives one common regular radial
linearized equation independent of `m`; it also states the exact pointwise
defect introduced by replacing `cos(P)` with its phase average. It supplies no
mode-existence, frequency, stability, nonlinear, or infinite-domain theorem.

## Sourced Inputs

The review reads release v0.47.0, C-PDE-003, C-PDE-004, C-PDE-006, P054's
frozen proposal, attempts 0001 through 0005, the hash-pinned QB3 source, the
canonical `triaxial_l2` module and tests, and the source/impact audits. QB3's
averaged eigenvalue, boundary data, and reported residual are evidence under
review rather than derivation inputs.

## Independence

The primary route differentiates all five real spherical quadratics and
integrates their moments. The independent route instead represents each as
`n^T*A*n`, uses the isotropic Cartesian fourth moment, and derives the omitted
Fourier coefficient from the J0 integral derivative and Bessel recurrence.
It compares the canonical API only after those formulas are fixed.

## Verification Status

The claim earns `symbolic_verified`. Primary attempt 0002 passes 19 exact
checks and repaired independent attempt 0005 passes 22. Attempt 0004 is
preserved as a failed oracle: SymPy left a Fourier integral unevaluated, so it
did not count as proof. The repaired identity evaluates exactly and a 192-node
Gauss-Legendre calculation is cross-check evidence only.

## Sensitivity and Counterexamples

Changing ℓ(ℓ+1), the triple-STF factor, the twice-phase sign or factor,
the origin order, or a static background causes a load-bearing check to fail.
For `P=a*cos(tau)`, the defect begins at
`-a^2*cos(2*tau)*psi/4`; it vanishes in the tested static limit but not at
nonzero amplitudes. QB3's start gives exact mismatch `1e-6`.

The separate averaged spectral precursor passes residual, approximately
second-order mesh, and exact vacuum-box gates. It fails the predeclared bound-
state and full-equation-equivalence gates, so it is retained as rejection
evidence and does not raise the exact claim's verification status.

## Framework Compatibility

The result is native to C-PDE-003's dimensionless equation and regularity.
It adds no fitted parameter or comparator. The m label changes only angular
basis within a fixed ℓ eigenspace. Time averaging is explicitly a different
operator unless its displayed pointwise defect vanishes.

## Dependency and Consumer Replay

The only scientific dependency is C-PDE-003. C-PDE-004 is a downstream
application through C-GW-007; C-PDE-006 is used only in the rejected averaged
precursor. Focused l-mode, tensor, TT, and governance paths plus QB3 and QB4
consumer meanings are replayed. No accepted equation changes.

## Competing Candidate Audit

Candidates A through D and structural criteria were frozen before the source
was opened. Literal A fails regularity and full-equation gates. The averaged
precursor to C converges but is a wall state. Exact B is selected for no new
dynamical parameter and full framework fit; D's positive finite-time object
is discharged by exact transfer of the already accepted C-PDE-004 solution.

## Four-Axis Decision

The decision accepts the claim as exact native structure.

- Verification: `symbolic_verified`
- Review: `accepted`
- Compatibility: `native`
- Epistemic: `active`
- Relationship: no challenge or supersession

## Promotion Transaction

Promotion adds C-PDE-009 to the registry and v0.48.0, preserves P054 as an
immutable campaign, renders docs and accepted memory, qualifies QB3 through
the editable disposition map, regenerates the queue, and runs the primary,
independent, targeted, and repository gates.

## Continuation if Not Accepted

No claim-level repair remains. A genuine Floquet spectrum about C-PDE-006
would require a separate proposal and cannot be inferred from the rejected
averaged state.

## Done Gate

The exact positive theorem, source rejection mechanisms, independent route,
consumer map, and transaction gates are specified with no reduced scope.

## Cross-References

See P054, C-PDE-003, C-PDE-004, C-PDE-006, C-GW-007, QB3, and pending QB4.
