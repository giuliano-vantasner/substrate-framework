---
description: Independent review of the conditional massive triplet dipole interaction theorem C-SKY-001
author: vantasner-review
created: '2026-08-09T07:00:00Z'
updated: '2026-08-09T07:00:00Z'
tags: [substrate-framework, claim-review, skyrmion, dipole, yukawa]
category: decisions
confidence: established
status: archived
---
# Review of C-SKY-001

## Claim Under Review

C-SKY-001 derives the isolated-self-energy-subtracted cross term of two equal
triplet point dipoles in a declared three-component static massive linear
field. It proves the complete classical relative-orientation extrema, the
fixed-orientation attractive force, finite-range behavior, and massless limit.
It is not a nonlinear Skyrme or nucleon theorem.

## Sourced Inputs

The review reads v0.104.0, the frozen P137 contract, hash-pinned S1 and dossier,
the accepted C-CC-001/C-MED-001/C-VIR-001/C-RPROF-001 ceilings, all P137
attempts and evidence, the canonical implementation, focused tests, both
derivations, and the source graph. The linear field, coupling sign, point
sources, self-energy subtraction, K, P, m, R, and SO(3) orientation are visible
declared inputs. No pending source edge grants a premise.

## Independence

The primary route consumes `massive_dipoles.py`, differentiates the radial
Yukawa Green function, and proves global bounds with Rodrigues certificates.
The independent reviewer does not import that module. It differentiates the
Cartesian Green function, reconstructs the Fourier source-pairing sign,
derives both orientation gaps afresh, and tests 4,096 deterministic random
proper rotations.

## Verification Status

The maximum verdict is `symbolic_verified`. The primary verifier passes 26
exact/source checks, the independent route passes 13 checks, and 28 focused
package/shared tests pass. Random SO(3) sampling is auxiliary sensitivity
evidence; exact certificates establish the extrema.

## Sensitivity and Counterexamples

Zero P removes the interaction. Doubling K halves it; multiplying P by three
multiplies it by nine. Reversing the source-coupling sign reverses attraction
and orientation ordering. The identity, perpendicular-axis pi rotation, and
radial-axis pi rotation have distinct exact energies. An improper `-I` probe is
outside SO(3) and the API rejects improper matrices. Positive mass gives
exponential range; zero mass gives the inverse-cube limit. S1's numeric RHS is
wrong by the variable factor R despite passing its sign check.

## Framework Compatibility

The theorem adds a pure module without modifying C-CC-001 or conditional
single-profile Skyrme claims. It requires no accepted dependency because its
field action and sources are explicit premises. The thematic identifier does
not map the declared triplet to a physical Skyrmion. Its ceilings preserve
C-RPROF-001's absence of a full 3D action or particle map.

## Dependency and Consumer Replay

T2B and S5 contribute only their accepted narrow claims. B1, G1, and G2 remain
pending. PG4 and PN6 retain independent accepted closures; WN6, WM7, and WM8
remain pending. Eleven hash-pinned scripts replay 157 runtime predicates. G1
and B1 receive isolated legacy aliases backed by `np.trapezoid`; no mutable
claim or campaign file has executable legacy integration access.

## Competing Candidate Audit

Candidate A is reproduction evidence only. Candidate B is exact existing
C-CC-001 composition and not novel. Candidate C is selected for the first
complete action/source/subtraction/orientation object. Candidate D would need
an unaccepted nonlinear action, state and scale and is not needed for this
long-range theorem. Candidate E maps source remnants; Candidate F closes
governance.

## Four-Axis Decision

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: new conditional long-range triplet-dipole theorem with no accepted scientific dependency

## Promotion Transaction

Promotion adds the pure module and exports, focused tests, C-SKY-001, release
v0.105.0, generated records, and qualified S1 disposition. Generated docs and
memory are rebuilt from governance rather than edited by hand.

## Continuation if Not Accepted

This clause is inactive for the conditional theorem. It remains active for the
excluded physical objective: a future proposal must derive the nonlinear
Skyrme action, B=1 states, two-center dynamics, quantization, core, units and
observation map independently.

## Done Gate

Action, source sign, subtraction, Green normalization, Hessian, SO(3) domain,
global extrema, force, range, limits, mutations, independence, implementation,
dependencies, consumers, compatibility and novelty are closed for C-SKY-001.

## Cross-References

See P137, S1, T2B, S5, PG4, PN6, C-CC-001, C-MED-001, C-VIR-001,
C-RPROF-001, `massive_dipoles.py`, and `test_massive_dipoles.py`.
