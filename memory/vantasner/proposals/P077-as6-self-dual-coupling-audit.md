---
description: Derive a normalization-explicit reciprocal-coupling ledger and audit AS6's self-dual pin
author: vantasner
created: '2026-08-03T12:00:00Z'
updated: '2026-08-03T13:30:00Z'
tags:
- substrate-framework
- campaign-proposal
- coupling-duality
- migration-AS6
category: proposals
confidence: exploratory
status: archived
---
# P077 AS6 Self-Dual Coupling Audit

## Question and Positive Deliverable

P077 must derive an exact, importable ledger for positive reciprocal coupling
involutions, their fixed points, normalization covariance, arbitrary-target
families, and off-fixed dual orbits. It must then determine whether AS6 proves
an accepted framework duality that selects `beta^2=4*pi`, or only solves the
fixed point of a separately imposed map.

## Base Release and Provenance

The accepted base is `v0.69.0` at scientific commit `0940dd9`; parent-effort
synchronization is commit `1ac6e75`. The predecessor is pinned at
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`. AS6 is
`/home/dan/substrate/merged-framework/bridges/phase-22/bridge_AS6_beta_self_dual_pin.py`,
19399 bytes, with SHA-256
`2f6c76d8aedde25b343f85cb54b2618cd03c816a29553fa70a523909265dd7f0`.
The queue marks AS6 pending and names AS1, AS3, AS5, AS7, B1, G1, G2, QCD3,
T1Z2, W3, and WZ3. AS1, AS3, and AS5 are qualified with explicit ceilings;
the later or unrelated units cannot supply an accepted duality or coupling
value. Release v0.69.0, relevant claim entries, canonical modules, history,
the clean framework worktree, dirty-but-pinned predecessor state, source
inventory, and repository-scoped memory search were checked. Only AS6's
generated synopsis is open; its source body and later numerical data remain
closed.

## Invariants, Conventions, and Allowed Imports

The accepted sine-Gordon root is the classical normalized `beta=1` equation;
it contains no accepted Coulomb-gas, bosonization, Coleman, fermion, or
electric-magnetic map. C-RGE-001 retains the coupling and beta coefficient as
inputs. C-DIM-008 rejects AS5's dimensionless-only absolute-scale headline and
requires correct inverse-energy orientation. For positive `x` and separately
declared positive `A`, `D_A(x)=A/x` is an involution with positive fixed point
`sqrt(A)`. Under `x'=rho*x`, the equivalent coordinate formula has
`A'=rho^2*A`. Exact algebra may analyze this map; physical duality language
requires an accepted action or observable equivalence with audited
normalization. Primary literature may be audited after freeze only because
AS6 explicitly invokes it; it does not become a framework premise.

## Candidate Preregistration

The candidates are frozen before the AS6 source body, numeric output, or later
comparators are read.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal AS6 promotion | Every named duality and corpus convention is accepted | Source inputs | `beta^2=4*pi` may be selected physically | Hash-pinned execution and data-flow audit |
| B | Conditional stated involution | `D(x)=16*pi^2/x` is supplied on `x>0` | Fixed coefficient | Unique positive fixed coordinate is `4*pi` | Exact solve and double-application test |
| C | General reciprocal family | `D_A(x)=A/x`, `A>0` | Free `A` | Fixed point is `sqrt(A)` and any target can be encoded | Exact family and coefficient mutations |
| D | Coordinate-covariant family | `x'=rho*x` is a convention change | `rho>0` | Coefficient and numeric fixed point rescale; orbit structure does not | Symbolic conjugation of the map |
| E | Accepted-action audit | A physical duality needs a proven action/observable map | Any fields and normalizations must be explicit | No coupling can be selected if the accepted action map is absent | Dependency and source audit |
| F | Fixed-subfamily ceiling | A theory may be restricted by the extra equation `x=D(x)` | The restriction itself | Generic positive x forms an off-fixed dual pair; duality does not force self-duality | Constructive counterfamily |

## Selection Criteria and Blinding

Selection is ordered by accepted action-level closure, exact algebra and
domain, normalization covariance, distinction between map and selection,
parameter economy, mutation sensitivity, and compatibility with the
normalized accepted root. The queue exposes `4*pi` and one approximate
hierarchy only as source claims. Neither may set a coefficient, physical
dictionary, threshold, tolerance, or verdict, and later AS7 data remain
closed.

## Proposed Claim Delta

Provisional C-SYM-002 may state the exact reciprocal-involution family,
positive fixed point, arbitrary-target coefficient, coordinate covariance,
and distinction between dual pairing and self-dual restriction if that
composition is reusable and nonduplicate. It may not establish a physical
sine-Gordon/Coulomb-gas or massive-Thirring duality, Coleman normalization,
free fermions, a beta function, a selected coupling, QCD, confinement,
absolute scale, or phenomenology.

## Implementation and Oracle Plan

SymPy exact algebra is the strongest oracle for the involution, fixed points,
coordinate conjugation, and counterfamilies. A pure `coupling_duality` module
is allowed only for a nonduplicate surviving composition and will reuse the
shared verification ledger in campaigns. The independent route will rebuild
the equations without importing that module. Mutations will change the
reciprocal coefficient, omit positivity, apply the map twice, rescale the
coordinate without rescaling the coefficient, choose off-fixed dual pairs,
and compose AS5's rejected hierarchy sign. Source predicates will be checked
against mutated formulas rather than trusted by tally. No numerical
integration is required; neither `np.trapz` nor another NumPy quadrature alias
will appear. Any Coleman or Coulomb-gas attribution receives a separate
primary-literature audit after the source is opened.

## Attempts and Continuation

Attempt 0001 preserves the manifest-key validation failure and its schema-only
repair. Attempt 0002 reproduces all nine hash-pinned AS6 checks and rejects
their physical-selection headline while retaining the conditional algebra.
Attempt 0003 preserves the promotion-order failure caused by registering a
not-yet-materialized final evidence path. Attempt 0004 completes Candidates
B-F, the source disposition, independent review, and the v0.70.0 gate.

## Debt Ledger

The campaign tracks map-premise, normalization, action-equivalence,
fixed-point-selection, hierarchy, literature, dependency, verification, and
synchronization debt.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| The coefficient `16*pi^2` may be treated as derived | Generalize to `A`, mutate it, and audit its source | discharged by the D_A family, coefficient mutation, and conditional N=2 literature map |
| A numeric coupling coordinate may be called convention independent | Conjugate the map under `x'=rho*x` | discharged by A'=rho^2*A and fixed-coordinate covariance |
| A duality map may be called a mechanism selecting its fixed point | Exhibit off-fixed dual pairs and identify the extra self-dual restriction | discharged by the exact 2<->9/2 counterfamily |
| Literature labels may substitute for an accepted action map | Audit primary sources and the exact accepted framework dependencies | discharged by the Coleman and two-field SDSG primary audit |
| AS5's rejected absolute-scale and hierarchy orientation may be reused | Compose only C-DIM-008's accepted reference-explicit orientation | discharged by the exp(+X) inverse-energy replay |
| Existing algebra may make the proposed claim duplicate | Compare its complete object and consumers against accepted claims | discharged; C-SYM-002 adds the general orbit, inverse-target, and coordinate-conjugation composition |
| Sensitive verification, review, and synchronization are incomplete | Complete mutations, independent route, source disposition, review, replay, and generated synchronization | discharged at the v0.70.0 promotion boundary |

## Review and Promotion Plan

Any surviving claim receives independent involution, normalization,
counterfamily, action-dependency, and literature review. AS6 receives a
terminal structured disposition through `migration/dispositions.yaml` and
queue regeneration. Reusable accepted logic moves into package code with
focused tests. Promotion requires claim review, release and registry closure,
generated docs and accepted memory, affected-consumer replay, one integrated
workflow boundary, and a separate whitespace check.

## Outcome

P077 accepts the exact conditional reciprocal-coupling ledger as C-SYM-002
and qualifies AS6. The primary route passes 30 checks, the independent route
passes 23 checks, 105 affected tests and 17 focused governance tests pass, and
the integrated workflow passes all 720 tests. The N=2 primary self-dual
extension conditionally explains AS6's coefficient only with a dual field,
second cosine, and equal amplitudes absent from the accepted root. The map
therefore does not select an accepted framework coupling, and AS6's hierarchy
and phenomenology remain outside dependency closure.

## Done Gate

P077 is complete: the positive ledger, source mapping, primary audit,
mutations, independent derivation, qualified disposition, C-SYM-002 review,
v0.70.0 release, generated consumers, replay, and empty campaign debt agree.
The parent migration remains active with 143 pending units.
