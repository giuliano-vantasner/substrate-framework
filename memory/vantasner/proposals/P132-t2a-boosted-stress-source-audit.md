---
description: Audit T2A's boosted breather stress tensor and physical source boundary
author: vantasner
created: '2026-08-08T23:45:00Z'
updated: '2026-08-08T23:45:00Z'
tags: [substrate-framework, campaign-proposal, sine-gordon, stress-tensor, migration-T2A]
category: proposals
confidence: exploratory
status: active
---
# P132 T2A Boosted Stress Source Audit

## Question and Positive Deliverable

P132 must reproduce and adjudicate T2A's assertion that a uniformly boosted
sine-Gordon breather is a new conserved moving source. The positive deliverable
is either a distinct, reusable, dependency-closed stress-to-dilaton source
theorem beyond C-SG-008 and C-SG-012, or a terminal source mapping that preserves
the exact boosted field and charges while rejecting unsupported gravity,
radiation, material, and observational lifts.

## Base Release and Provenance

The accepted base is v0.100.0 at parent checkpoint `4be5953`; the latest
scientific adjudication is P131 at `3ee5942`. T2A is pinned to
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`, path
`merged-framework/bridges/phase-2/bridge_T2A_moving_source.py`, SHA-256
`669803de1403c8ca66e399aa4b7c0e762447e40df7c241fe530a6b4e06dde70a`.

The generated queue exposes twelve literal checks, one assertion, symbolic and
numeric language, and dependencies GW1 and GW4. Both predecessors are qualified;
GW1 supplies only C-MOM-001's conditional conserved-moment theorem, and GW4's
corrected conditional waveform maps to C-MOM-001 and C-GW-001 through C-GW-003.
Reverse candidate consumers G1 and G4 remain pending. This metadata and the
queue excerpts are navigation evidence, not authority, and T2A's source body
has not been opened or executed during this freeze.

## Invariants, Conventions, and Allowed Imports

C-SG-008 already supplies the exact boosted-breather phase and energy-momentum
vectors. C-SG-012 supplies the canonical symmetric tensor, distinguishes
covariant `T_01=phi_t*phi_x` from contravariant `T^01=-phi_t*phi_x`, and proves
the exact off-shell divergence. The boost convention is
`x'=gamma*(x-v*t)`, `t'=gamma*(t-v*x)`, with a scalar field pullback and
signature `(+,-)`. Full-line integrated conservation additionally requires the
localized boundary flux to vanish.

The accepted breather field, energy, boost, stress, divergence, and conditional
moment APIs may be imported. Exact Lorentz and SymPy algebra, analytic integrals,
and an independent rapidity derivation are permitted. High-precision mpmath
quadrature may only regress an exact result and must declare domain, precision,
tail and sample refinement. A nonzero mixed tensor component is not a dilaton or
Einstein source map without an explicit varied equation, coupling, units, and
closed dependency chain. Uniform inertial motion is not acceleration or
radiation. T2A becomes evidence only after this contract freezes.

## Candidate Preregistration

The candidate set distinguishes exact replay, Lorentz-tensor derivation,
accepted-claim composition, independent charge derivation, numerical regression,
physical source typing, countermodels, and governance closure.

| Candidate | Construction | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal T2A replay | Source conventions | Source values | Predicates repeat | Predicate and provenance audit |
| B | Exact Lorentz tensor route | C-SG-001/012 | `omega,v` | Field, tensor, and divergence transform | Symbolic covariance and sign checks |
| C | Accepted-claim composition | C-SG-008/012 | None new | Useful exact surface is duplicate | Claim/API nonduplication audit |
| D | Rapidity or analytic charge route | Localization and boundary decay | `omega,rapidity` | Charges form the accepted vector | Independent full-line derivation |
| E | High-precision regression | Declared quadrature protocol | Precision and domain only | Converges to exact charge | Precision/tail/velocity refinement |
| F | Dilaton source theorem | Varied field equation and typed coupling | Explicitly derived only | New claim only if map closes | Dependency, unit, and variation audit |
| G | Motion/radiation countermodels | Exact inertial kinematics | Acceleration mutation | Translation is nonradiative by itself | Zero-acceleration and map counterexamples |
| H | Governance closure | Accepted authority order | None | Narrow terminal disposition | Dependency, consumer, and impact replay |

## Selection Criteria and Blinding

Selection is ordered by dependency closure, fixed Lorentz and index conventions,
exact local and integrated conservation, independent analytic agreement,
mutation sensitivity, correct limits, physical-scope honesty, parameter economy,
reusable API fit, and nonduplication. The synopsis already exposes the preferred
charge formulas and source verdict. There is no empirical comparator, and those
values cannot establish novelty or a physical source map.

## Proposed Claim Delta

P132 provisionally reserves C-SG-020 only for a genuinely new, typed, reusable
stress-to-source theorem with a varied target-field equation and closed imports.
If T2A only composes C-SG-008 and C-SG-012, no claim, package API, or release is
added; T2A will instead be terminally qualified or marked duplicate evidence at
the exact subclaim level.

## Implementation and Oracle Plan

The primary route will hash and parse T2A, classify all twelve predicates, and
rederive its scalar pullback, field residual, tensor components, divergence,
boundary decay, and charges from accepted definitions. SymPy is appropriate for
the exact differential and tensor identities. Direct analytic integration or a
rapidity transformation will establish the charge vector without copied source
constants.

The independent route will avoid T2A helper functions and derive the transformed
tensor from a rest-frame stress distribution and Lorentz matrix, checking the
Jacobian and both index placements. Velocity reversal, wrong boost sign, wrong
mixed-index sign, omitted Jacobian, finite-boundary flux, a nonrelativistic
momentum guess, and acceleration/source-map countermodels must break overstrong
verdicts. The rest limit and finite rapidities are exact; the singular light-speed
limit is analytic rather than a sampled endpoint.

Any numerical quadrature is regression coverage only. It will use mpmath or the
canonical `trapezoid_integral`, never `np.trapz`, and will report precision,
domain/tail refinement, error scale, and solver status. Compatibility preflight
requires mutable scripts to use `np.trapezoid`; an immutable legacy `np.trapz`
call receives an alias-only recorded replay and is not a scientific failure.

## Attempts and Continuation

Attempt 0001 freezes this contract before source-body inspection or execution.
Every later implementation, representation, numerical, concept, source-map, or
consumer failure is preserved append-only and followed by a materially different
repair or candidate.

## Debt Ledger

The campaign tracks source, convention, conservation, quadrature, source-map,
physical-scope, dependency, consumer, and nonduplication debt.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| T2A executable surface unaudited | Hash, execute, AST audit, and predicate mapping | open |
| Boost and tensor conventions | Exact scalar pullback, both index placements, and sign mutations | open |
| Integrated charges and boundaries | Independent exact derivation plus decay and Jacobian audit | open |
| Numerical evidence ceiling | Declared refinement or explicit finding that no numeric oracle is needed | open |
| Dilaton-source claim untyped | Supply varied field equation/coupling or reject the lift | open |
| Radiation and material language | Separate uniform motion from acceleration and require governed maps | open |
| Dependencies, consumers, and novelty | Audit GW1/GW4, G1/G4, accepted claims/APIs, and generated state | open |

## Review and Promotion Plan

Primary and independent routes precede source disposition and claim-level review.
Impact, dependency, consumer, nonduplication, candidate, predicate, provenance,
and compatibility records must agree. A new accepted claim requires package code,
tests, registry entry, release, generated docs and memory, and the integrated
promotion gate. A terminal mapping with unchanged science uses targeted record
checks at freeze and one integrated adjudication boundary, then only
record-sensitive checks after final attempt bookkeeping.

## Done Gate

P132 closes only when a positive distinct source theorem exists or the exact
surviving surface is completely mapped to accepted claims, every predicate and
physical overread is adjudicated, exact and independent oracles are mutation
sensitive, consumers replay, generated state agrees, and campaign debt is empty.

## Cross-References

See P012, P036, P039, P049, P132, T2A, GW1, GW4, G1, G4, C-SG-008,
C-SG-012, C-MOM-001, C-GW-001 through C-GW-003, provisional C-SG-020,
v0.100.0, and the parent framework-migration effort.
