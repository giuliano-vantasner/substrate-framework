---
description: Audit BD4's collective-coordinate inertia and barrier-top interpretation
author: vantasner
created: '2026-08-03T13:03:42Z'
updated: '2026-08-05T12:00:00Z'
tags:
- substrate-framework
- campaign-proposal
- collective-coordinate
- migration-BD4
category: proposals
confidence: exploratory
status: archived
---
# P102 BD4 Collective Inertia Audit

## Question and Positive Deliverable

P102 must deliver an exact, importable, mutation-sensitive account of a
one-field collective-coordinate pullback and adjudicate BD4 against it. The
positive object is the conditional kinetic metric, its variable-metric reduced
equation, the rest-stationary linearization, the stable/neutral/unstable sign
classification, and the coordinate-reparameterization law. The capillary
specialization must say what `sqrt(2*pi*P/M)` actually is at the barrier top.

The campaign is not complete merely because the proposed inertia has the
right dimension or BD4 reproduces fourteen checks. It must establish the
profile and boundary assumptions under which the integral exists, preserve
the distinction between an inverted-saddle growth exponent and a stable mode,
and close every source predicate and consumer without manufacturing a material
map, quantum onset, stochastic escape, or observed event.

## Base Release and Provenance

The accepted base is `v0.85.0` at parent commit
`fcede2ea89da17030f99888779e618ec5b4f9617`; the latest claim-promoting
scientific transaction remains P100 at
`020ab1f8eef254e13f98aa88e85d96362ba57346`. P101 subsequently qualified BD3
without changing the release. Source evidence is pinned to
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`; unrelated dirty Phase 47/48
work and the separate NumPy compatibility overlay are excluded from scientific
authority.

BD4 is
`/home/dan/substrate/merged-framework/bridges/phase-28/bridge_BD4_mR_inertia_ceiling_resolution.py`,
11,824 bytes, SHA-256
`2f590473719f614f4ca641ad9443d6b4271429aba27337b94d5d064cc70c9929`,
and git blob `69c5b5bf918daf044562c55b386e944ddff44b34`. It is clean relative to the
pinned commit. The queue marks it pending, records fourteen literal SymPy
checks, and lists candidate dependency `M2`. That name is ambiguous: here it
means leg M2 of legacy
`pulson-backreaction-bridge/sympy/rungs/rung098_material_handle.py`, pinned at
SHA-256 `2e5034841668d10684ef23ac4a1fb7e71d6f08e0c66086c951760049cccd7ee1`
and blob `f9b797be1e19659142a1ae94e106737f98cd3fe0`, not the unrelated phase-7
Meissner/Proca bridge unit also labeled M2.

No genuine body or tally blinding remains. P100 executed BD4 as a pending
consumer and exposed `ALL 14 CHECKS PASS`; the generated queue and parent
memory exposed the inertia and curvature formulas and the claimed ceiling
retirement. Legacy rung098 has now been re-sourced and already identifies the
capillary top as an inverted saddle. P102 freezes the competing structural
interpretations and decisive tests before renewed BD4 inspection or execution.
Direct accepted sources read before freeze are release `v0.85.0`, the relevant
registry entries C-MED-003, C-RG-001, C-RG-002, C-VAR-001, C-BRK-001, and
C-DYN-001, plus their canonical dimensional-field, radial-energy,
variational, and generalized-curvature modules and tests. Durable memory was
re-sourced at those authority surfaces and supplies no accepted radius profile,
cross-sector coefficient map, stable barrier-top mode, onset equality, or
escape theorem.

## Invariants, Conventions, and Allowed Imports

Use the C-MED-003 density convention with dimensionless `u`, physical `x,t`,
and positive kinetic coefficient `lambda`. A declared profile family
`u(x,t)=phi(x,q(t))` must be differentiable enough that
`phi_q` is square-integrable over the declared spatial domain. Its pulled-back
metric is `M(q)=lambda*integral(phi_q**2 dx)`. Positivity and finiteness require
an actual nonzero admissible profile derivative; they do not follow from the
dimension vector.

For reduced potential `U(q)`, the exact equation is
`M*qddot + M'*qdot**2/2 + U'=0`. At a rest stationary point `q0` with
`M(q0)>0` and `U'(q0)=0`, linearization gives
`M(q0)*delta_qddot+U''(q0)*delta_q=0`. Positive curvature is a stable
oscillator, zero curvature is linearly neutral, and negative curvature gives
real exponential roots. For C-RG-001, `R*=T/P` is a maximum and
`U''(R*)=-2*pi*P`, so `sqrt(2*pi*P/M(R*))` is the local instability exponent.

Under a smooth locally invertible coordinate change `q=g(Q)`, the metric is
`M_Q=M_q*(dq/dQ)**2`. At a stationary point the Hessian transforms with the
same square factor, making `U_QQ/M_Q` invariant; away from stationarity an
extra `U_q*d2q/dQ2` term remains. Curvature or inertia alone therefore cannot
be treated as a coordinate-free observable. A stable natural frequency, an
unstable growth rate, `hbar` times either scale, thermal crossover, stochastic
escape, and measured onset remain distinct.

## Candidate Preregistration

The candidates are frozen before renewed BD4 source-body inspection or
execution and before further downstream output is inspected.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal reproduction | Pinned source environment | Source symbols and literals | Tally proves only implemented predicates | Hash, AST, process, output, predicate ledger |
| B | Dimensions-only completion | Declared integral dimension | lambda and an abstract integral | Correct mass dimension but no existence, value, or profile theorem | Dimension matrix plus divergent/zero counterprofiles |
| C | Genuine field pullback | Smooth square-integrable profile family | lambda, phi, q | Exact positive semidefinite kinetic metric | Chain rule, direct integration, factor mutation |
| D | Variable-metric reduction | Differentiable positive metric and potential | M(q), U(q) | Exact connection term and stationary linearization | Euler-Lagrange derivation and omitted-half mutation |
| E | Curvature-sign classification | Rest stationary point and positive finite metric | M0, U''0 | Stable, neutral, and unstable branches remain distinct | Characteristic roots and sign mutations |
| F | Coordinate covariance | Smooth local inverse | q=g(Q) | Metric and stationary Hessian co-transform; ratio invariant | Direct chain rule and nonstationary counterexample |
| G | Concrete-profile audit | Declared domain and boundary behavior | profile shape and coordinate convention | Finiteness and normalization are profile-dependent | Finite, zero, divergent, and rescaled-profile examples |
| H | Normalization audit | Common or independent sector scaling | continuum and capillary coefficients | Common action scale cancels; lambda-only scaling changes rate | Exact rescalings and dependency search |
| I | Interpretation and consumer audit | Accepted dependencies only | none | No onset, escape, or event theorem follows | Registry and consumer premise ledger |

## Selection Criteria and Blinding

Selection is ordered by accepted dependency closure and nonduplication; exact
variational derivation, dimensions, sign, factor normalization, regularity,
coordinate covariance, and mutations; separation of a stable spectrum from an
unstable saddle exponent and from onset or escape; assumption and parameter
economy; canonical extraction; and complete consumer classification. A source
tally or narrative term cannot select a candidate.

The main source formula, output, and intended headline were exposed before
P102. The campaign claims no formula or comparator blinding. It freezes the
profile pullback, connection term, curvature sign branches, reparameterization
test, common-versus-independent scaling, missing-state countermodels, and
no-sprawl boundary before renewing source inspection or execution.

## Proposed Claim Delta

P102 reserves `C-COL-001`. Collision searches across the registry, campaigns,
proposals, durable memory, source modules, and tests found no use of that
identifier and no accepted claim containing the full field pullback plus
stationary sign and coordinate-covariance theorem. C-BRK-001 owns a supplied
constant kinetic coefficient and a potential Hessian; C-MED-003 owns the field
density; neither derives the induced metric from a profile family or classifies
the capillary maximum.

The proposed claim depends on C-MED-003 for the kinetic density and C-RG-001
for the capillary specialization. C-VAR-001 and C-BRK-001 are consistency
anchors, not hidden sources of a profile. No claim is challenged or
superseded. Promotion is conditional on exact independent evidence and may be
abandoned while the source is still terminally adjudicated if collision or
dependency review defeats novelty.

## Implementation and Oracle Plan

If candidate C survives, an importable pure module will expose the exact
profile-metric integral, variable-metric Euler-Lagrange expression,
stationary spectral ratio, coordinate transformation, and capillary-top
specialization. It will accept the profile, domain, coordinate, and coefficients
explicitly and will not execute integration, simulation, or printing on import
beyond requested symbolic construction. Campaign verifiers will call that API;
an independent route will rederive the chain rule and Euler-Lagrange equation
without importing it.

SymPy is the strongest oracle because every proposed statement is exact
calculus, algebra, sign classification, or dimension analysis. Tests will use
a finite translation profile, a coordinate-rescaled profile, a zero derivative,
and a non-square-integrable counterprofile; mutate the kinetic half factor, the
metric derivative coefficient, the capillary curvature sign, and the
coordinate Jacobian; and require the load-bearing verdicts to fail. No numeric
quadrature, ODE, PDE, NumPy, or SciPy solver is needed.

The compatibility preflight confirms BD4 imports no NumPy. If a hash-pinned
consumer later aborts only on `np.trapz`, P102 records an alias-only replay
before scientific adjudication; a version-only abort is not candidate evidence.
Focused replay covers the new module, dimensional sine-Gordon, radial energy,
variational, and generalized-curvature tests and affected campaigns. One full
workflow gate runs at the meaningful promotion/adjudication boundary, with no
duplicate standalone pytest run afterward.

## Attempts and Continuation

Every source, dependency, profile, representation, factor, sign, covariance,
interpretation, or verifier failure is append-only with a diagnosis and next
candidate. A dimensions-only candidate can be preserved as a bounded result
while the effort continues through the genuine pullback and terminal source
adjudication. A failed onset interpretation does not finish the campaign.

## Debt Ledger

P102 tracks source and predecessor hashes, prior exposure, imports, every
literal check, profile definition and domain, boundary and regularity
assumptions, integral finiteness and positivity, kinetic factors, dimensions,
potential convention, stationary sign, characteristic roots, coordinate
normalization, cross-sector coefficient scaling, hbar and onset semantics,
consumers, source disposition, generated state, and parent continuation. Every
item must be derived, declared, rejected, or excluded before closure.

## Review and Promotion Plan

The proposed claim receives a primary exact verifier, an independent
rederivation, claim-level prose review, source predicate adjudication, impact
analysis, and affected-consumer replay. Acceptance requires canonical package
extraction, sensitive tests, governance and release updates, generated docs,
accepted-memory synchronization, a terminal BD4 disposition, and one full
workflow validation. A final record-only update will rerun only record-sensitive
repository, generation, memory, and diff checks.

## Done Gate

P102 closes only when the conditional collective-coordinate object exists,
both derivations and mutations validate it, profile and coordinate premises are
explicit, the capillary maximum is correctly classified, every BD4 predicate
and consumer is adjudicated, claim and release surfaces agree, campaign debt is
empty, and the parent migration advances. A correct dimension or fourteen-check
tally is not completion.

## Cross-References

This campaign cross-references legacy rung098 leg M2, BD4, BD5, BD-L, C-MED-003,
C-RG-001, C-RG-002, C-VAR-001, C-BRK-001, C-DYN-001, P095, P099, P100, and the
canonical dimensional-field and radial-energy modules.

## Terminal Adjudication

P102 promotes C-COL-001 as an exact conditional theorem and qualifies BD4. A
declared admissible field-profile family induces
`M(q)=lambda*integral((partial_q phi)^2 dx)` and the variable-metric reduced
equation. At rest stationary points the curvature sign separates stable,
neutral, and unstable branches, while smooth coordinate changes preserve the
stationary curvature-to-inertia ratio. The accepted capillary point is a strict
maximum, so `sqrt(2*pi*P/M)` is its exponential instability rate.

BD4's dimension predicates survive, but it never supplies the profile or cross-
sector action, and its ceiling-retirement, stable-frequency, and onset readings
do not. Its Lean consumer proves only weaker dimension and unrelated algebraic
conjuncts. BD5 and the engineering adapter execute but use BD4 only in prose.
The claim imports no material, quantum, stochastic, or event map. Claim-level
debt is empty after promotion replay; the corpus migration continues to BD5.
