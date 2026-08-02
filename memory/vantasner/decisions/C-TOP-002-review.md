---
description: Independent review of C-TOP-002 SU3 winding current and hedgehog charge
author: vantasner-review
created: '2026-08-02T17:00:00Z'
updated: '2026-08-02T17:00:00Z'
tags:
- substrate-framework
- claim-review
- su3-winding-current
category: decisions
confidence: established
status: archived
---
# C-TOP-002 Claim Review

## Claim Under Review

C-TOP-002 states an exact mathematical theorem in C-LIE-001's fundamental
trace convention. The SU(3) trace-three cochain represents the one-dimensional
third cohomology; an explicit upper-SU(2) quaternion block independently fixes
its generator period; the normalized four-dimensional coordinate current is
identically conserved; and a regular embedded hedgehog has the displayed local,
radial, and boundary charge formulas. Its sign, epsilon orientation, endpoint
hypotheses, and relationship to the positive quaternion generator are explicit.
The claim excludes Noether, gauged-WZW response, physical baryon, anomaly,
`N_c`, representation, scale, and substrate meanings.

## Sourced Inputs

The review reads pinned release `v0.51.0`, C-LIE-001, the deliberately limited
C-WZW-001 and C-WZW-002 statements, P058's frozen proposal, four attempt
records, the SHA-256-pinned WZ3 source and reproduction, source audit,
topology/anomaly provenance, primary verifier, independent review script,
canonical `wzw.py`, focused tests, impact analysis, and the regenerated WZ3
migration record. Pending NC1, S2, and S3 supply no premises. WZ3's source file
is verified at
`30da2ac41a0d46c48bd4e1b9733c3712d0b6c1c9b4838f1a1df3c4db22cc3569`.

## Independence

The independent review imports no canonical WZW or winding-current helper. It
rebuilds the quaternion map and its differential, computes the degree-one
first-column Jacobian, alternates the Pauli traces, expands the three graded
Leibniz/cyclic terms, derives the hedgehog angular trace, checks the boundary
antiderivative, and performs a separate `np.trapezoid` regression on an
analytic profile. Its first exact comparison failed because one side remained
in complex exponentials; that run is preserved, and the repaired oracle expands
the exact residual into a common real representation rather than adding a
tolerance. It also independently derives the anomaly-consistent general-`N_c`
charge cancellation.

## Verification Status

The maximum verdict is `symbolic_verified`. Exact CE matrices give
`rank(d2)=20`, `rank(d3)=35`, a 21-dimensional cocycle kernel and
one-dimensional H3. The actual trace-three cochain is closed, has nine nonzero
components and squared norm 9, and raises the d2 image rank from 20 to 21. The
explicit generator has raw tangent density 12, sphere volume `2*pi^2`, and raw
period `24*pi^2`, deriving the coefficient `-1/(24*pi^2)`. The primary verifier
passes 26 checks; the independently implemented exact/regression review passes
10. Numerical quadrature is classified only as regression because the charge
is already exact.

## Sensitivity and Counterexamples

Orientation reversal flips the current and charge while preserving closure.
Changing the generator normalization sign changes its normalized period from
minus one to plus one. Constant, half-endpoint, doubled, and reversed hedgehog
data give charges zero, one-half, two, and minus one rather than silently
passing the unit-charge predicate. Removing full antisymmetry produces a
generic nonzero symmetrized four-trace. The analytic-profile quadrature uses
501 through 8001 logarithmic points and its error decreases from
`1.2725e-4` to `4.9705e-7`; three scale deformations retain the same exact
boundary charge. WZ3's plus-sign headline gives minus one for its decreasing
profile, while its later numerical sign flip gives plus one. The native source
also fails at removed `np.trapz`, whereas canonical evidence uses
`np.trapezoid`.

For the color claim, fixed charges give `N_c/3` and recover three only after
the target one is inserted. Anomaly-consistent
`Q_u=(1+1/N_c)/2`, `Q_d=(1/N_c-1)/2` instead give
`N_c*(Q_u^2-Q_d^2)=1` identically, agreeing with the audited Baer-Wiese
counteranalysis. Thus WZ3.6 cannot promote.

## Framework Compatibility

The selected B/C construction preserves C-LIE-001 exactly, introduces no fitted
constant, and needs no pending physics unit. Its minus normalization is derived
from the positive generator period and the declared decreasing-hedgehog charge
convention. It is a compatible mathematical extension. Candidate A conflicts
with its own sign and uses structural stand-ins; Candidate D yields a response
only after declaring a free external-source coupling and cannot be mislabeled a
derivation from accepted ungauged WZW authority.

## Dependency and Consumer Replay

The only accepted dependency is C-LIE-001. GitNexus rates the `wzw.py` addition
LOW risk; the existing trace-five cohomology process is unchanged. Focused WZW
tests pass 17 checks. WZ4, QCD7, MK2.2, MK5, and other later narrative consumers
remain pending and receive no accepted baryon, anomaly, color, or descent
premise. Registry, release, generated documentation, migration inventory, and
memory are replayed in the promotion transaction.

## Competing Candidate Audit

Candidates A through D and their criteria were frozen before the source
implementation was opened. B and C are selected because generator degree,
period, closure, and hedgehog charge are independently exact and require only
accepted SU(3) algebra plus audited topology. A is rejected as a positive route
despite its shimmed tally. D is retained only as conditional source-coupling
algebra with free coefficient. No printed unit charge or anomaly comparator
selected the construction.

## Four-Axis Decision

The axes are assigned independently and without a supersession relationship.

- Verification: `symbolic_verified`
- Review: `accepted`
- Compatibility: `compatible_extension`
- Epistemic: `active`
- Relationship: new claim depending only on C-LIE-001

## Promotion Transaction

Promotion adds pure APIs and tests in `wzw.py`, C-TOP-002 in the registry,
release `v0.52.0`, the immutable P058 campaign, a qualified WZ3 disposition,
regenerated source claims, rendered canonical docs and accepted memory, and
the separate effort sync. Targeted verifiers, focused consumers, the full
workflow gate, the explicitly required pytest replay, memory validation, and
`git diff --check` must all pass before commit.

## Continuation if Not Accepted

This clause is inactive because the mathematical claim is accepted. WZ3's
gauged-WZW, baryon, anomaly, and color conclusions remain historical attempt
evidence and cannot be treated as accepted dependencies. A future positive
physical claim requires a separately governed action, source transformations,
descent equation, microscopic representations, and anomaly inventory.

## Done Gate

The claim-level mathematical debt is empty after exact and independent review.
The parent corpus migration remains active because the queue still contains
pending units.

## Cross-References

See P058, C-LIE-001, C-WZW-001, C-WZW-002, WZ3, `wzw.py`, `test_wzw.py`, and
release v0.52.0.
