---
description: Independent review of C-KRN-001 leading-power and Riesz-kernel theorem
author: vantasner-review
created: '2026-08-02T23:25:00Z'
updated: '2026-08-02T23:25:00Z'
tags:
- substrate-framework
- claim-review
- riesz-kernel
category: decisions
confidence: established
status: archived
---
# C-KRN-001 Claim Review

## Claim Under Review

C-KRN-001 states that the smallest positive exponent with a provably nonzero
combined coefficient controls a supplied inverse kernel's infrared power.
Exact cancellations remove an exponent, and a lower fractional bare term
survives analytic corrections. Under the separately fixed inverse Fourier
convention, nonzero inverse-kernel coefficient, radius `r>0`, and
`0<s<d/2`, it derives the general Riesz Green kernel and its conditional
`d=3,s=1` specialization. It does not select an exponent, dimension, force
law, charge normalization, or physical sector.

## Sourced Inputs

The review reads release `v0.57.0`, C-GAU-001 and C-DIM ceilings, the frozen
P064 candidate set, hash-pinned D3S and its pending EM3/EM5/EM7/QCD5
dependencies, attempts 0001 through 0004, source audit and adjudication,
primary-provenance record, canonical implementation and tests, both exact
verifiers, and the impact analysis. D3S's unconditional `s=1`, `d=3`,
Coulomb, Maxwell, and substrate conclusions remain outside the claim.

## Independence

The independent route imports no canonical kernel API. It takes infrared
ratios directly, constructs an exact cancellation, derives the Riesz
normalization from the Schwinger representation and Gaussian Fourier
transform, and independently evaluates the three-dimensional endpoint with
an exponential regulator and spherical angular integration. Dimension and
fractional-power mutations are recomputed from the general formula.

## Verification Status

The maximum verdict is `symbolic_verified`. Every promoted leading exponent,
gamma normalization, radial power, derivative, and specialization is an
evaluated exact SymPy expression. The convergence inequality remains an
explicit assumption rather than an unresolved proof output. The source's
numeric fit of an exact `r**(-1)` array is classified as regression theater
and supplies no independent evidence.

## Sensitivity and Counterexamples

The canonical classifier refuses a symbolic coefficient whose zero status is
undecidable. A declared nonzero coefficient gives leading exponent one, while
D3S's allowed tuning `e2=6*pi*m2` cancels it and exposes exponent two with
coefficient `1/(5*m2)`. Adding exponent one-half or two-thirds makes that
fractional term lead. Changing `d=3` to four changes the Green kernel to
`1/(4*pi**2*r**2)`; changing `s=1` to one-half gives
`1/(2*pi**2*r**2)`; doubling the inverse-kernel coefficient halves the Green
kernel. The logarithmic boundary `s=d/2` is refused without a prescription.

## Framework Compatibility

The theorem is additive and dependency-free. It preserves C-GAU-001's
explicit absence of a gauge kinetic coefficient and the accepted dimensional
claims' free-coordinate semantics. Exponents, coefficients, Fourier
normalization, dimension, radius, convergence regime, contact-term exclusion,
and physical dictionary remain separate premises. No pending Riesz or QCD
campaign supplies authority.

## Dependency and Consumer Replay

The accepted dependency closure is empty. Consumers are the new pure module,
focused tests, P064 verifiers, governance, generated docs and memory, and
future inverse-kernel audits. The pre-change graph found no canonical
fractional-Laplacian flow and no callers of the nearest finite-matrix expansion.
Post-change detection reports zero affected pre-existing processes, and the
full 484-test repository replay passes.

## Competing Candidate Audit

Candidate D is selected because it tests absence, cancellation, and lower
fractional terms instead of solving a preassigned exponent equation. Candidate
E is selected because it derives the general normalized kernel before any
named endpoint. Candidate A fails the nonzero-coefficient, bare-kernel, and
dimension provenance criteria. The `1/(4*pi*r)` endpoint did not select the
general theorem.

## Four-Axis Decision

The axes support a new exact conditional theorem with no challenge or
supersession relationship.

- Verification: `symbolic_verified`
- Review: `accepted`
- Compatibility: `compatible_extension`
- Epistemic: `active`
- Relationship: new dependency-free inverse-kernel and Fourier theorem

## Promotion Transaction

Promotion adds C-KRN-001 to release `v0.58.0`, archives P064 and this review,
qualifies D3S with structured evidence, and synchronizes implementation,
tests, registry, release, queue, docs, and memory. Both exact routes, focused
consumers, graph detection, one full workflow, and diff checks must pass.

## Continuation if Not Accepted

This clause is inactive because the conditional theorem is accepted. A
future physical Coulomb claim must separately derive a nonzero two-derivative
inverse coefficient, the absence of lower powers, spatial dimension, source
coupling, boundary conditions, force dictionary, and substrate realization.

## Done Gate

The claim-level and transactional debt is empty after synchronization and
replay. The parent migration effort remains active because later queue units
are pending.

## Cross-References

See P064, D3S, C-LOC-001, `momentum_kernels.py`,
`test_momentum_kernels.py`, release `v0.58.0`, and the parent migration
effort.
