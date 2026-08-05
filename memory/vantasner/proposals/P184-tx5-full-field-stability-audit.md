---
description: Audit TX5 and derive a complete constrained full-field or narrow lattice stability object
author: vantasner
created: '2026-08-11T10:40:00Z'
updated: '2026-08-11T10:40:00Z'
tags:
- substrate-framework
- campaign-proposal
- migration-TX5
- full-field
- stability
category: proposals
confidence: exploratory
status: active
---
# P184 TX5 Full-Field Stability Audit

## Question and Positive Deliverable

P184 must decide whether TX5 establishes a strict local minimum of a specified
degree-two SU(2) field in the full three-dimensional static Skyrme energy, and
must produce the strongest positive importable object that closes naturally.
The deliverable is a complete constrained full-field or finite-discrete
stationarity and Hessian result if the source and repaired methods support it;
otherwise a distinct exact or converged lattice-functional, kinetic-tangent,
topology, or second-variation theorem must be extracted while the unsupported
minimum remains unaccepted. A list of missing full-field obligations alone is
not completion.

## Base Release and Provenance

The accepted base is v0.135.0 at clean framework commit
`60c557621114ffca258357b6a2f540153dd69f62`, with 175 accepted claims. Its
manifest SHA-256 is
`001e589256cf33518612e5f24e8714bed14b1ff59cf78343448e90f29c949ecf`.
The governed predecessor baseline is
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`. TX5 is pending at
`merged-framework/bridges/phase-40/bridge_TX5_full_field_stability.py`,
SHA-256
`ea12c1fee0dab254c4d8cdc984ee694622199e7cb5380674d689cf1fe6f0e31a`,
size 30,201 bytes, blob `4a2355274a314cbd97c51e7ec658d591b14f3b01`, and sole
history commit `7222eed`. The target path is clean at the governed source
commit; later source-worktree prose has no authority.

The generated queue already exposes TX5's full-3D strict-minimum headline,
one-dimensional energy and baryon validation, exact positive mass-operator
language, Derrick scale checks, random smooth perturbation curvatures, a
targeted `m=2` direction, eight static check calls, two assertions, and a
positive result synopsis. P184 therefore claims no fresh result blinding. The
implementation body, equations, numerical values, perturbation construction,
predicates, assertion reachability, and conclusion dataflow remain unopened
until this contract passes validation.

## Invariants, Conventions, and Allowed Imports

C-RMAP-001/002, C-RPROF-001/002, C-RMOM-001/002, and C-RMAP-003 govern only
declared rational-map geometry, reduced radial branches, conditional moments,
and one fixed-degree angular Hessian. They supply no stationary 3D field or
full-field Hessian. C-GW-009/010 are prescribed moment kinematics. C-FLO-001 is
a finite-matrix theorem and C-ROT-001 is an abstract free top; neither is a
rotating Skyrme solution or collective inertia. C-PDE-009 explicitly rejects
promoting an auxiliary static operator without its missing evolution.

A finite lattice and continuum field are distinct. P184 may import exact SU(2),
Pauli, tangent, Derrick, constrained-Hessian, and finite-dimensional spectral
identities, plus NumPy/SciPy methods with every equation, precision, boundary,
mesh, step, tolerance, status, and norm explicit. It may inspect hash-pinned
TX5 and its source graph only as noncanonical evidence. Candidate dependency
E4 maps to accepted BPS-Skyrme identities and supplies no authority for the
classical full-field minimum. No empirical value, physical-state label,
selected angular speed, gravity, radiation, or observation is permitted.

Mutable numerical integration uses `np.trapezoid` or the canonical
`trapezoid_integral`. Direct, imported, dynamic, and eager-default legacy
`np.trapz` access is preflighted. A version-only immutable abort receives an
alias-only replay backed by `np.trapezoid` and never rejects a candidate.

## Candidate Preregistration

Six candidates separate literal evidence, a narrow lattice/kinetic theorem, a
complete finite-discrete Hessian, a continuum coercive route, bounded positive
composition, and governance closure.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Exact TX5 reproduction and predicate audit | Hash-pinned source environment | Source box, grids, steps, seeds, literals | Evidence only | AST, native/alias execution, dataflow, equation, predicate, assertion, and headline reachability audit |
| B | Narrow finite-lattice SU2 functional and positive tangent metric | Declared constrained lattice field and boundary | Box, mesh, derivative stencil | Strong if exact definitions and refinements close | Derive functional and kinetic quadratic form, validate constraints, limits, topology, dimensions, and mutations |
| C | Complete discrete local-minimum theorem | Stationary constrained finite-box field | Mesh, box, Hessian step, eigensolver tolerance | Strong numeric candidate if all tangent directions are classified | Stationary residual plus lowest complete constrained Hessian spectrum after symmetry quotient and refinements |
| D | Continuum coercive local-minimum theorem | Exact stationary field and function-space control | None beyond declared model | Strongest but most demanding | Exact second variation and a coercive bound on the topology-preserving quotient space |
| E | Narrow Derrick, baryon, targeted-direction, or accepted composition | Only the exact object actually computed | Declared reduced or lattice inputs | Compatible fallback but cannot carry full-field prose | Independent derivation and sensitive scoped verifier with every broader reading rejected |
| F | Governed closure | Claim-level evidence | None | Required | Dependency, consumer, queue, release, docs, memory, and empty-debt replay |

## Selection Criteria and Blinding

Selection is ordered by exact field/action/topology conventions, actual
stationarity, complete constrained tangent coverage, symmetry and boundary
handling, mesh/domain/step/tolerance refinement, independent method and
mutation sensitivity, separation of kinetic/static/dynamic claims, assumption
economy, novelty beyond accepted reduced claims, and global closure. Random
positive samples and comparator agreement cannot select a concept. Queue
synopses already reveal headline results, so the meaningful gate is frozen
criteria before the source body and numerical outputs are opened.

## Proposed Claim Delta

P184 provisionally reserves C-SKY-002 for a distinct exact or converged SU(2)
static-functional/kinetic-tangent result and C-PDE-014 for a complete
resolution-bounded constrained finite-box stationarity and Hessian result if
earned. Repository-wide registry, campaign, source, test, and durable-memory
searches find neither identifier. Rejected identifiers remain reserved. Both
are new proposals with no `supersedes` edge. Their likely consumers are TX5,
canonical field/numerics modules, tests, the registry and release, generated
docs and memory, migration dispositions and queue, and any later physical or
dynamical consumer, which inherits only the exact accepted scope.

## Implementation and Oracle Plan

The source audit first pins native or alias execution, AST check inventory,
every field and functional definition, boundary and topology convention,
stationarity residual, perturbation generator, energy curvature, refinement,
random seed, assertion, and conclusion edge. Reusable code will live under
`src/substrate_framework/`; imports will not simulate or print.

Exact algebra is required for SU(2) constraints, tangent parameterization,
kinetic positivity, continuum identities, and Derrick relations. Genuine
three-dimensional numerical claims use float64 or explicitly declared higher
precision, the exact static functional, box and boundary data, spatial stencil
or spectral method, constraint projection, stationary residual norm, sparse or
matrix-free Hessian solver status, mesh/domain/Hessian-step/tolerance axes,
symmetry-mode identification, and lowest-eigenvalue error model. A second
Hessian-vector construction or analytically soluble limit is independent
evidence. Random and targeted directions are regression or counterexample
search only, never completeness. Negative-curvature, wrong normalization,
constraint-breaking, boundary, topology, nonstationarity, and symmetry
mutations must break relevant verdicts.

Primary, independent, source-graph, affected-test, generated-consumer, and one
integrated workflow gates remain separate. `scripts/validate.sh` supplies the
single full-suite boundary; record-only closure receives narrow checks.

## Attempts and Continuation

Attempt 0001 freezes v0.135.0, framework commit `60c5576`, the TX5 hash and
history, exposed synopsis, two provisional identifiers, six candidates,
selection criteria, oracle hierarchy, compatibility policy, and debt before
opening the source body. The memory recall invocation also preserves one
non-scientific CLI mistake: `memory grep` has no `--limit` option; the earlier
successful `memory search` remains the recall evidence. Every later failed
implementation, representation, numerical, candidate, or verifier route is
append-only and names a materially different continuation.

## Debt Ledger

The P184 ledger tracks source reachability, field and action definitions,
topology, stationary residual, tangent completeness, Hessian and symmetry
classification, numerical refinement, compatibility, dependencies, consumers,
and governed state.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| TX5's exact implementation, values, predicates, assertions, and dataflow are unopened | Pin and audit every definition, input, equation, result, and headline dependency | open |
| The lattice field may not be stationary for its own discrete energy | Compute a constraint-aware full residual before interpreting second differences | open |
| Random directions may be mistaken for a complete Hessian test | Classify the complete finite constrained spectrum or prove a coercive bound | open |
| Continuum, finite-box, and lattice claims may be conflated | State the exact object and pass mesh, box, stencil, and boundary refinements | open |
| Symmetry, constraint, boundary, and topology directions may be mixed | Derive the tangent space and quotient, then test independent span and mutations | open |
| Positive kinetic metric may be overread as energy or dynamic stability | Separate kinetic, static Hessian, Floquet, and nonlinear predicates claim by claim | open |
| Reduced energies and baryon values may be circular comparators | Re-derive conventions and keep post-freeze values out of selection and thresholds | open |
| Legacy NumPy access may masquerade as science | Repair mutable code or use immutable alias-only replay without candidate rejection | open |
| Dependencies, consumers, and governed records may disagree | Replay the graph and synchronize disposition, queue, claims, release, docs, memory, and debt | open |

## Review and Promotion Plan

C-SKY-002 and C-PDE-014 receive separate claim reviews with raw primary,
independent, mutation, refinement, and consumer artifacts. Verification,
review, compatibility, and epistemic axes remain independent. Any accepted
logic is extracted into pure modules and tests; rejected random-sampling or
full-field prose remains attempt evidence. TX5 receives a structured qualified,
refuted, duplicate, or out-of-scope disposition with exact remaining subclaims
preserved. Every registered evidence path is materialized before governance,
the queue and canonical views are generated, and validation and commit remain
separate invocations.

## Done Gate

P184 closes only when a positive importable object exists, the full-field
minimum language matches a complete oracle or is explicitly unaccepted, every
source predicate has an individual verdict, dependencies and downstream
consumers replay, governance and generated state agree, and debt is empty. A
native pass tally, baryon closeness, positive mass matrix, Derrick direction,
random positive curvatures, or one targeted direction alone keeps P184 active.

## Cross-References

See C-PDE-009, C-RMAP-001/002/003, C-RPROF-001/002, C-RMOM-001/002,
C-GW-009/010, C-FLO-001, C-ROT-001, P180-P183, E1, E2, E4, TX1, TX2,
TX4, TX5, `rational_maps.py`, `rational_map_radial.py`,
`rational_map_moments.py`, `rational_map_stability.py`,
`rotating_stability.py`, and `numerics.py`.
