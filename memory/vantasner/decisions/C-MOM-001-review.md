---
description: Independent review of C-MOM-001
author: vantasner-review
created: '2026-08-01T17:44:29Z'
updated: '2026-08-01T17:44:29Z'
tags:
- substrate-framework
- claim-review
- conserved-stress
- multipole-moments
category: decisions
confidence: working
status: archived
---
# Review of C-MOM-001

## Claim Under Review

The claim states the exact integrated monopole, momentum, dipole, second-moment,
and STF identities of a smooth localized symmetric conserved tensor in flat
`3+1` spacetime, with surface and convention assumptions explicit and every
gravitational radiation interpretation excluded.

## Sourced Inputs

The review read `v0.31.0`, P036, both exact routes, package APIs/tests,
hash-pinned GW1 and its successful reproduction, and the subclaim source
adjudication. G1, G2, GW2, and GW3 were inventoried as unaccepted radiation
relationships rather than dependencies.

## Independence

The main route uses a locally conserved translating three-dimensional Gaussian
and directly audits GW1's functions. The independent route uses three inertial
point masses, origin translation, a finite-domain flux example, a separate
nonsymmetric tensor, and a static anisotropic STF tensor. It imports neither
the moment module nor GW1 constants.

## Verification Status

Exact local residuals, Gaussian moments, direct differentiation, integration-
by-parts counterexamples, and STF algebra support `symbolic_verified`. No
numeric simulation or source pass tally earns a gravitational radiation
verdict.

## Sensitivity and Counterexamples

Nonzero monopole rate, wrong dipole sign, accelerated isolated dipole, and a
missing factor two all fail the main predicate. A finite boundary flux changes
the monopole while preserving local continuity. A nonsymmetric conserved
tensor separates energy flux from momentum density. A static nonzero
quadrupole has zero derivatives. GW1's arbitrary `g(t)` current contradicts its
compact-stress momentum equation unless `g'=0`.

## Framework Compatibility

The claim is native conditional tensor mathematics. It fixes contravariant
conservation, inertial coordinates, tensor symmetry, localization, all
coordinate-weighted surface terms, and both STF normalizations. It introduces
no gravitational action, coupling, field, gauge, Green function, wave zone, or
radiation criterion.

## Dependency and Consumer Replay

There are no accepted claim dependencies. Direct consumers are
`conserved_moments.py`, its exports/tests, P036, GW1's disposition, and future
source-moment audits. The gravitational consumers remain outside the accepted
graph. Focused replay passes with no debt.

## Competing Candidate Audit

Candidate A was selected because the fully conserved source and independent
route close the second-moment and STF factors, making Candidate B too weak.
Candidate C fails dependency closure and confuses a nonzero source derivative
with a solved radiative field.

## Four-Axis Decision

The axes apply only to the localized conserved-stress moment theorem.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: native
- Epistemic: active
- Relationship: standalone conditional moment theorem

## Promotion Transaction

Promotion adds pure moment/STF APIs, guarded tests, immutable P036, qualified
GW1 disposition, `v0.32.0`, generated records, and parent-effort
synchronization. No gravitational claim or consumer is promoted.

## Continuation if Not Accepted

If symmetry or the factor-two identity had failed, Candidate B would retain
only total conserved charges. Radiation requires a separately governed field
equation, retarded solution, gauge/TT projection, wave-zone observable,
normalization, and source consistency.

## Done Gate

Boundary terms, tensor symmetry, derivative hierarchy, STF normalizations,
frame limits, mutations, radiation boundary, consumers, disposition, and debt
closure are complete.

## Cross-References

See P036, GW1, `conserved_moments.py`, and the parent migration effort.
