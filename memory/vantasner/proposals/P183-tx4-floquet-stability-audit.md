---
description: Audit TX4 and separate exact co-rotating algebra from genuine stability
author: vantasner
created: '2026-08-11T09:20:00Z'
updated: '2026-08-11T09:24:00Z'
tags:
- substrate-framework
- campaign-proposal
- migration-TX4
- floquet
- stability
category: proposals
confidence: exploratory
status: active
---
# P183 TX4 Floquet-Stability Audit

## Question and Positive Deliverable

P183 must determine exactly which TX4 results concern a finite co-rotating
linear system, a declared collective rotor, a restricted rational-map shape
space, or a genuine full-field perturbation problem. The positive deliverable
is an importable exact theorem for every surviving distinct finite-system or
rotor statement, plus a verifier-backed restricted Hessian result if its
inputs close, with spectral, Jordan, symmetry, and scope conditions explicit.
Finding that the source lacks a full-field operator does not complete the
campaign without the corrected positive object or an exact accepted-
composition disposition.

## Base Release and Provenance

The accepted base is v0.134.0 at clean framework commit
`2466d440562a37004aae1eba245b4c6bf40fd950`, with 172 accepted claims. Its
manifest SHA-256 is
`910087c9ccfa45867b6bf8a1bb47246481ccbabc2c00fdbfa2a5ae85c55060c6`.
The governed predecessor baseline is
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`. TX4 is pending at
`merged-framework/bridges/phase-40/bridge_TX4_floquet_stability.py`, SHA-256
`c88ff5fe65473756d36a29546fae4da417c56d7539dcfd8e58304bd0ab7b335f`,
size 24,802 bytes, blob `a8dd0757f4712cd15ddc6c4a0454b3e8aaf0779c`, and sole history commit
`7222eed21720c5174dd35ba8f825d8b7e0a48f3f`. The target path is clean at the
governed source commit; unrelated later source-worktree changes have no
authority.

The generated queue and earlier consumer audits already exposed TX4's dynamic-
stability headline, relative-equilibrium framing, co-rotating derivative,
time-independent generator, `exp(T*A)` monodromy synopsis, collective-rotor
stability language, restricted rational-map Hessian reading, eight static
check calls, and one assertion. P183 therefore claims no fresh source-result
blind. Exact definitions, actions, matrices, spectra, predicates, assertion,
numeric values, and conclusion dataflow remain unopened until this freeze.

## Invariants, Conventions, and Allowed Imports

C-GW-009/010 supply prescribed STF moment paths and conditional TT algebra,
not a rotating field solution. C-RMAP-001/002, C-RPROF-001/002, and
C-RMOM-001/002 supply sphere geometry, a reduced radial branch, and conditional
moments, not a full three-dimensional field or perturbation operator.
C-COL-001 classifies only a declared reduced coordinate with a positive finite
metric and complete stationary curvature. C-SYM-001 certifies Hessian zero
directions only from actual invariance, stationarity, independent generator
tangents, and a positive kinetic metric. C-PDE-009 fixes the separate warning
that an averaged or static auxiliary operator is not a Floquet solution.

A rotating-frame transformation and a stability theorem are distinct. For a
finite autonomous co-rotating generator, a matrix exponential can give the
monodromy, but stability still requires eigenvalue real parts, multiplier
moduli, Jordan blocks, and the intended symmetry quotient. For an unbounded
field operator, a written differential expression is insufficient without its
domain, boundary conditions, constraint/gauge treatment, and well-posed
evolution. An energy-momentum argument additionally requires an action,
momentum map, actual relative equilibrium, symplectic slice, constrained
second variation, and coercivity. Restricted-coordinate positivity never
implies full-field positivity.

Mutable quadrature uses `np.trapezoid` or the canonical
`trapezoid_integral`. A hash-pinned immutable legacy `np.trapz` abort, if one
exists, receives an explicit alias-only replay backed by `np.trapezoid`; it is
compatibility provenance and never a rejected scientific candidate.

## Candidate Preregistration

Six candidates separate literal reproduction, finite Floquet algebra, the
collective rotor, a restricted shape Hessian, full-field stability, and
governance closure.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal TX4 replay | Hash-pinned source environment | Source matrices, steps, tolerances, and literals | Evidence only | AST, native/alias execution, equation, check, assertion, and conclusion reachability audit |
| B | Finite co-rotating theorem | Periodic invertible frame and finite constant generator | Period, angular rate, generator matrices | Strong exact candidate if distinct | Derive transformed generator and fundamental matrix; audit spectral mapping, Jordan blocks, and mutations |
| C | Collective-rotor classification | Complete declared reduced action and conserved structure | Inertias, angular rate, perturbation coordinates | Narrow candidate only | Derive Euler-Lagrange system, exact variational equation, conserved quadratic form, symmetry quotient, and secular/Jordan behavior |
| D | Restricted rational-map Hessian | Exact finite coordinate family and stationary objective | Shape coordinates and declared reduced coefficients | At most ansatz-local evidence | Reconstruct objective, gradient, Hessian, kinetic metric, symmetry tangents, eigenpairs, convergence, and coordinate mutations |
| E | Full-field stability | Accepted action, rotating solution, operator/domain, constraints, boundary data, complete spectrum | Field, angular rate, domain and solver controls | Currently unsupported unless TX4 closes every premise independently | Full residual, linearization, semigroup/Floquet or constrained-energy oracle, refinements, conservation, and independent method |
| F | Governance closure | Claim-level review | None | Required | Dependency, consumer, disposition, queue, release, docs, memory, and debt replay |

## Selection Criteria and Blinding

Selection is ordered by accepted action and solution provenance; operator,
domain, constraint, gauge, and boundary completeness; separation of coordinate
reduction from stability; multiplier, Jordan, and symmetry-quotient
correctness; energy-momentum slice and coercivity; reduced-subspace scope;
assumption and parameter economy; strongest exact or refined independent
oracle; nonduplication; and downstream governance. Exposed source prose cannot
select a candidate or set a numerical threshold. No fresh runtime-output blind
is claimed.

## Proposed Claim Delta

P183 provisionally reserves C-FLO-001 for a finite-dimensional co-rotating
linear-system theorem with exact monodromy and explicit spectral/Jordan
conditions. It separately reserves C-ROT-001 only if TX4 contains a distinct
complete collective-rotor perturbation theorem not already covered by
C-ACT-001, C-COL-001, or C-SYM-001. Repository-wide registry, campaign,
migration, source, test, and durable-memory searches found no collision for
either identifier or P183. Neither identifier denotes a Skyrmion, a full-field
operator, nonlinear stability, a dynamically selected `Omega`, gravity,
radiation, observation, or substrate realization.

Direct consumers include TX4, pending TX5, the accepted collective,
symmetry-Hessian, rational-map, moment, and prescribed-rotation ceilings,
package exports and tests if an API survives, migration state, generated docs,
releases, and memory. No accepted claim becomes retroactively dependent on
P183 and no `supersedes` relation is proposed.

## Implementation and Oracle Plan

The source audit will inventory imports, declared and derived actions,
configuration spaces, coordinate maps, background paths, equations of motion,
linear operators, domains, boundary data, constraints, kinetic metrics,
Hessians, spectra, multipliers, Jordan chains, symmetry tangents, conservation
laws, numerical methods, thresholds, checks, assertions, and conclusion
reachability. Lexical calls, runtime executions, assertions, and headline
claims remain separate inventories.

SymPy and direct matrix algebra are the strongest oracles for finite frame
changes, matrix exponentials, characteristic polynomials, Jordan chains,
finite rotor linearization, stationary gradients, Hessians, symmetry tangents,
and exact mutations. An independent derivation will differentiate the frame
map and solve the lab-frame fundamental matrix without importing the proposed
helper. Counterexamples include a time-independent generator with a positive
real eigenvalue, a unit multiplier with a size-two Jordan block, an incomplete
coordinate Hessian, a nonstationary background, a missing kinetic metric, and
a positive restricted block embedded in an unstable larger operator.

Any numerical Hessian or spectrum must name floating precision, exact
objective/operator, coordinates, domain, boundary data, constraints, mesh or
step sequence, eigensolver, tolerances, stopping status, scale-relative error
norm, symmetry-null classification, and independent route. Resolution and
coordinate transformations must preserve the scoped verdict, and load-bearing
mutations must break it. A full-field PDE claim additionally requires the
actual rotating solution residual, spatial and temporal refinement,
conservation or controlled drift, spectral completeness or a justified bound,
and an independent discretization or energy method. A finite exact result may
not borrow that conclusion.

Canonical integration remains `trapezoid_integral`; mutable scripts use
`np.trapezoid`. TX4 receives alias-only replay only if immutable executable
syntax needs it, without changing its pinned hash or scientific route.

## Attempts and Continuation

Attempt 0001 freezes v0.134.0, framework commit `2466d44`, the TX4 hash and
history, exposed synopsis, six candidates, two provisional identifiers,
selection criteria, oracle hierarchy, compatibility policy, and open debt.
Every failed representation, implementation, spectral route, source
predicate, or validation attempt will remain append-only with a materially
different next action.

## Debt Ledger

The P183 ledger tracks source reachability, background dynamics, rotating-
frame algebra, spectral and Jordan structure, rotor and rational-map scope,
full-field obligations, compatibility, dependencies, consumers, and governed
state.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| TX4's exact implementation, values, predicates, assertion, and dataflow are unaudited in P183 | Pin every definition, input, equation, check, assertion, result sentence, and dependency | open |
| The rotating configuration may be prescribed rather than solved | Derive the action/EOM and prove the exact rotating background residual before any perturbation claim | open |
| A co-rotating identity may be mislabeled an exactly solved spectrum | Derive the transformed generator and separately determine spectrum, multiplier modulus, Jordan structure, and evolution bounds | open |
| A secular term may be relabeled a harmless zero mode | Identify eigenvectors versus generalized eigenvectors, the symmetry quotient, conserved norm, and boundedness criterion | open |
| Collective-rotor stability may be incomplete or duplicate accepted algebra | Reconstruct the complete reduced action and compare exact scope with C-ACT-001/C-COL-001/C-SYM-001 | open |
| Rational-map Hessian positivity may be coordinate, finite-difference, or restricted-space evidence | Establish stationarity, complete coordinates, kinetic metric, symmetry kernel, refined eigenpairs, and ansatz-local scope | open |
| Full-field stability may be inferred from restricted sectors | Supply the field operator/domain/constraints/boundaries and complete full-space oracle, or preserve the claim as unaccepted | open |
| Legacy NumPy access may masquerade as science | Repair mutable code or use immutable alias-only replay without candidate rejection | open |
| Dependencies, consumers, and governed records may disagree | Replay graph and synchronize disposition, queue, memory, claims, release, docs, and debt | open |

## Review and Promotion Plan

Every TX4 equation and conclusion receives an individual verdict. The rotating
background, frame transform, monodromy, spectrum, multiplier, Jordan,
collective, Hessian, symmetry, restricted-space, full-field, nonlinear, and
physical predicates retain separate statuses. Any distinct surviving theorem
must be independently rederived, extracted into a pure tested API, replayed
through direct and indirect consumers, and promoted claim by claim. TX4
receives a structured supported disposition with every unaccepted remainder
preserved; TX5 remains independently pending.

The promotion transaction edits only governed mutable records and generates
the queue and canonical docs. Every evidence path is materialized before
registration. Targeted routes run before one integrated `scripts/validate.sh`;
record-only closure is checked narrowly without repeating the full suite.
Validation and commit remain separate invocations.

## Done Gate

P183 closes only when a positive exact finite co-rotating and/or distinct rotor
theorem or exact accepted-composition disposition exists, every source
predicate is adjudicated, every spectral and stability word matches its actual
configuration space and oracle, dependencies and consumers replay, governed
records agree, and the debt ledger is empty. A time-independent matrix, eight
passing checks, a nonnegative restricted Hessian, or a labeled zero mode alone
keeps the campaign active.

## Cross-References

See C-ACT-001, C-COL-001, C-SYM-001, C-PDE-009, C-RMAP-001/002,
C-RPROF-001/002, C-RMOM-001/002, C-GW-009/010, P054, P060, P102, P104,
P177, P180-P182, E1, E2, M2, QB3, TX1-TX5,
`collective_coordinates.py`, `symmetry_breaking.py`, `rational_maps.py`,
`rational_map_radial.py`, `rational_map_moments.py`, and
`rigid_quadrupole_rotation.py`.
