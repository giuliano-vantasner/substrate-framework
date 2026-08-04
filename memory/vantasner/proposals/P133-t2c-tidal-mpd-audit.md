---
description: Audit T2C's optical-curvature finite-width and MPD force claim
author: vantasner
created: '2026-08-09T00:30:00Z'
updated: '2026-08-09T00:30:00Z'
tags: [substrate-framework, campaign-proposal, optical-geometry, finite-size, migration-T2C]
category: proposals
confidence: exploratory
status: active
---
# P133 T2C Tidal MPD Audit

## Question and Positive Deliverable

P133 must reproduce and adjudicate T2C's assertion that a finite breather width
couples to the static optical curvature as a leading post-geodesic
Mathisson-Papapetrou-Dixon acceleration. The positive deliverable is either a
distinct reusable and dimensionally closed extended-body force theorem, or a
terminal source mapping that preserves exact geometry and Fourier-moment facts
while rejecting an unsupported mechanism identification.

## Base Release and Provenance

The accepted base is v0.100.0 at parent checkpoint `10950aa`; the latest
scientific adjudication is P132 at `477c809`. T2C is pinned to
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`, path
`merged-framework/bridges/phase-2/bridge_T2C_tidal_MP.py`, SHA-256
`651fd75287dd25b5c34208ea5789df89be50f5050ec139ae2d99f4962440c369`.

The generated queue exposes thirteen literal checks, one assertion, a symbolic
oracle, the preferred curvature-times-moment formula, and dependencies FS1,
FS2, FS4, P3D3, and T1B. FS1, FS2, P3D3, and T1B are qualified; FS4 is duplicate
evidence. Their accepted mappings and explicit physical ceilings are authority,
not their source chronology or T2C's synopsis. T2C's body has not been opened or
executed during this freeze.

## Invariants, Conventions, and Allowed Imports

C-OG-001 fixes `g=diag(-1/n,n/c0^2)`, coordinates `(t,x)`, signature `(-,+)`,
and exact scalar curvature. The frozen Riemann convention is
`R^rho_(sigma mu nu)=d_mu Gamma^rho_(nu sigma)-d_nu Gamma^rho_(mu sigma)
+Gamma^rho_(mu lambda)Gamma^lambda_(nu sigma)-Gamma^rho_(nu lambda)
Gamma^lambda_(mu sigma)`. All component comparisons must retain slot order and
index position.

C-CC-001 owns the declared point-collective action and its exact coordinate-time
acceleration, including slow limit `c0^2*n_x/(2*n^3)`. C-SG-009 owns the exact
centered unnormalized scalar energy moment and explicitly no physical finite-size
coupling. For `w_tilde(k)=integral exp(-i*k*y)w(y)dy`, sufficient moment bounds
give `-w_tilde''(0)=integral y^2*w(y)dy`; raw YAML doubles the apostrophes only
to escape a single quote. Normalized and unnormalized moments must not be mixed.

In physical coordinate units, scalar curvature has units `T^-2` and a normalized
spatial second moment has units `L^2`; their product is not acceleration. An
MPD quadrupole force, geodesic deviation, Taylor-averaged point acceleration,
and a declared response ansatz are different mechanisms and must be derived
separately. Primary MPD literature may be read after freeze for exact equation
and convention provenance, not as authority for applying it to the substrate.

## Candidate Preregistration

The candidate set separates replay, exact tensor construction, Fourier-moment
calculus, direct profile averaging, genuine MPD closure, accepted-claim
composition, countermodels, and governance.

| Candidate | Construction | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal T2C replay | Source conventions | Source values | Predicates repeat | Thirteen-predicate and provenance audit |
| B | Exact optical tensor derivation | C-OG-001 metric | `n,c0` | Curvature components close | Independent Christoffel/Riemann/scalar agreement |
| C | Fourier moment theorem | Declared integrable profile | Profile normalization | Second derivative gives second moment | Sign, order, centering, translation guards |
| D | Taylor-averaged point acceleration | C-CC-001 slow law plus centered profile | Width moments | Leading correction uses the actual second derivative of point acceleration | Exact expansion and profile countermodels |
| E | Typed MPD/Dixon route | Explicit multipole law and worldline data | No hidden coupling | Survives only with rank, mass, velocity, derivative, and units closed | Equation-level dependency and dimension audit |
| F | Accepted composition | C-OG-001/C-CC-001/C-SG-009 | None new | Useful facts are duplicate | Claim and API nonduplication audit |
| G | Countermodels | Frozen conventions | Simple index profiles | Named mechanisms separate | Flat, linear, zero-width, sign, and unit probes |
| H | Governance closure | Accepted authority order | None | Narrow terminal disposition | Dependency, consumer, impact, and generated-state replay |

## Selection Criteria and Blinding

Selection is ordered by accepted dependency closure, fixed tensor conventions,
dimensional consistency, correct Fourier normalization and point limit,
independent tensor agreement, mechanism-specific derivation, mutation
sensitivity, known limits, parameter economy, reusable API fit, physical-scope
honesty, and nonduplication. The queue already exposes the favored formula and
verdict. There is no empirical comparator, and exposed source output cannot
establish its mechanism.

## Proposed Claim Delta

P133 provisionally reserves C-OG-004 only for a genuinely distinct typed
finite-width or MPD force theorem with closed equations, units, normalization,
and accepted dependencies. Exact Riemann components already implied by
C-OG-001, the generic Fourier moment identity, or an unsupported coupling name
do not warrant a claim, package API, or release.

## Implementation and Oracle Plan

After the freeze commit, the primary route will hash, parse, and execute T2C,
map all thirteen predicates, and rebuild its Christoffels, Riemann tensor,
Ricci contraction, scalar curvature, moment identity, claimed force, units, and
limits. SymPy exact identities are the primary oracle. A direct two-dimensional
curvature identity and a fresh component construction will be independent
checks rather than a second call to the same helper.

The finite-width alternative will Taylor-expand the accepted slow point
acceleration over a normalized centered profile. The MPD alternative must state
the precise multipole equation, rank and symmetries, worldline tangent, momentum
or mass normalization, curvature derivative, time parameter, and supplementary
conditions needed by its claimed specialization. Sign, slot-order, omitted
derivative, wrong normalization, translated profile, constant/linear index, and
zero-width mutations must break the relevant verdict.

No numerical quadrature is needed when exact differentiation closes. If source
reproduction or an independent integral needs sampling, mutable code uses
`np.trapezoid` or the canonical `trapezoid_integral`, never `np.trapz`, and
records domain and resolution refinement. An immutable legacy compatibility
call receives an alias-only replay and is classified separately from science.

## Attempts and Continuation

Attempt 0001 freezes this contract before source-body inspection or execution.
Every later implementation, representation, convention, concept, dependency,
or consumer failure is preserved append-only and followed by a materially
different repair or candidate.

## Debt Ledger

The ledger tracks source, tensor, moment, mechanism, physical-scope, dependency,
consumer, and novelty debt until each item has evidence-level closure.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| T2C executable surface unaudited | Hash, execute, AST audit, and map all thirteen predicates | open |
| Optical tensor conventions | Exact Christoffels, Riemann slots, contraction, sign mutations, and C-OG-001 agreement | open |
| Fourier moment object untyped | Fix transform sign, derivative order, normalization, centering, units, and point limit | open |
| Claimed force mechanism unclosed | Derive a typed MPD law or reject the identification | open |
| Finite-width alternative unaudited | Derive Taylor-averaged point acceleration and compare functional dependence | open |
| Physical language ungoverned | Separate effective coordinate model, extended body, gravity, material, and observation | open |
| Dependencies, consumers, and novelty | Audit FS1/FS2/FS4/P3D3/T1B, reverse consumers, accepted APIs, and generated state | open |

## Review and Promotion Plan

Primary and independent routes precede source disposition and any claim review.
Impact, dependency, consumer, nonduplication, candidate, predicate, provenance,
and compatibility records must agree. A new accepted claim requires package
code, tests, registry entry, release, generated docs and memory, and the single
integrated promotion gate. A terminal mapping with unchanged science uses
targeted checks at freeze and one integrated adjudication boundary, then only
record-sensitive checks after final attempt bookkeeping.

## Done Gate

P133 closes only when a positive distinct force theorem exists or the exact
surviving surface is completely mapped to accepted claims, every predicate and
mechanism overread is adjudicated, exact and independent oracles are
mutation-sensitive, dimensions and point limits close, consumers replay,
generated state agrees, and campaign debt is empty.

## Cross-References

See P004, P007, P010, P040, P041, P043, P046, P133, T2C, FS1, FS2, FS4,
P3D3, T1B, C-OG-001 through C-OG-003, C-CC-001, C-SG-009, provisional
C-OG-004, v0.100.0, and the parent framework-migration effort.
