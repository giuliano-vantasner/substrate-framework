---
description: Accepted review of conditional massive-scalar SU2 vacuum polarization claim C-NVP-001
author: vantasner-review
created: '2026-08-10T14:18:00Z'
updated: '2026-08-10T14:25:00Z'
tags: [substrate-framework, claim-review, C-NVP-001, nonabelian-vacuum-polarization]
category: decisions
confidence: established
status: archived
---
# C-NVP-001 Claim Review

## Claim Under Review

C-NVP-001 states a conditional exact one-loop theorem for massive complex
scalar multiplets in an explicitly validated finite SU2 representation on
Euclidean two-space. It covers the representation-indexed transverse kernel,
bubble--seagull Ward cancellation, exact limits, typed component and trace
coefficients, and the background-field completion of the leading local term.

## Dependency Closure

The claim depends directly on C-NAG-001 for the connection, curvature, and
trace convention and on C-VAC-001 for the complete Abelian complex-scalar
determinant and kernel. It independently validates the supplied generators and
derives their trace index. C-REP-002 is an example boundary, not a hidden
physical carrier import. No pending source, fitted constant, bare coefficient,
counterterm, physical matter dictionary, or observable is imported.

## Exact Derivation and Independent Oracle

The canonical route composes the accepted Abelian ledger with the exact
representation trace and independently reconstructs the proper-time
curvature coefficient. A fresh reviewer imports neither the new module nor the
Abelian helper: it derives the real-parameter antiderivative, closed form,
low-momentum series coefficient, bubble--seagull contraction, proper-time
mass integral, fundamental and adjoint trace metrics, and a noncommuting
constant-background curvature control.

## Sensitivity and Counterexamples

Deleting or sign-flipping the seagull breaks the Ward contraction. Replacing
the scalar numerator by YM1's numerator changes the kernel and massless limit.
Omitting T(R) changes the fundamental kernel; rescaling generators breaks the
fixed SU2 commutators. Halving the determinant breaks the complex-scalar
proper-time match. A curl-only projector misses noncommuting constant
curvature. Bare, counterterm, and field-coordinate families reject a unique
induced coupling.

## Framework Compatibility

The implementation is additive pure exact SymPy algebra and changes no
accepted symbol or convention. GitNexus reports LOW risk, no pre-existing
function callers, no affected process, and only the package export as a direct
class import. Exact search finds actual consumers only in the P158 verifier
and focused tests. Mutable code contains no executable legacy NumPy
integration access.

## Dependency and Consumer Replay

The eleven-node graph replays 132 source predicates and eleven assertions.
EM5 and W7 supply corrected accepted boundaries; W2 supplies only a generator
example. W2/W7 retroactive closure prose is rejected. M1/M2 retain their
separately declared kinetic premises. Pending YM2/GK1 receive no authority.
YM2's immutable `np.trapz` spelling runs only through an isolated alias backed
by `np.trapezoid`, so compatibility does not become scientific failure.

## Competing Candidate Audit

The declared scalar-loop candidate is selected because it uniquely closes the
quantum action, representation, Ward, kernel, local, and background-field
obligations. Algebra-only retention cannot provide a loop. Accepted
composition alone lacks the non-Abelian completion. Classical action and
physical-substrate candidates either duplicate an accepted boundary or lack
their required premises.

## Four-Axis Decision

The four axes support additive promotion.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: additive conditional non-Abelian scalar-loop theorem

## Promotion Transaction

The transaction adds the pure module, focused tests, public exports,
C-NVP-001, release v0.123.0, qualified YM1 disposition, generated state, and
accepted memory. The terminal integrated attempt is the promotion-boundary
oracle; no source tally can substitute for it.

## Continuation if Not Accepted

Nonacceptance would retain the module and campaign as proposal evidence and
return to a direct diagrammatic or background-field derivation. A physical
weak or substrate gauge mechanism requires a separate proposal with quantum
matter content, regulator, counterterms, matching, state, dimension, and
observable evidence.

## Done Gate

The registry, release, disposition, queue, generated documentation, memory,
compatibility policy, and debt ledger must agree. C-NVP-001 remains
conditional and does not promote YM1's physical headline.

## Cross-References

See P158, YM1, C-NAG-001, C-VAC-001,
`nonabelian_vacuum_polarization.py`, its focused tests, and P158's evidence and
reviews.
