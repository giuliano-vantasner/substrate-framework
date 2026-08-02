---
description: Derive radial fluctuation spectra and audit PG3's Roper identification
author: vantasner
created: '2026-08-02T20:15:00Z'
updated: '2026-08-02T21:00:00Z'
tags:
- substrate-framework
- campaign-proposal
- radial-spectrum
- migration-PG3
category: proposals
confidence: established
status: archived
---
# P062 PG3 Radial-Mode and Roper Audit

## Question and Positive Deliverable

P062 must deliver an importable, convention-explicit account of radial
fluctuations about a stationary spherical profile: the kinetic quadratic form,
energy second variation, self-adjoint operator and weight, origin and outer
boundary conditions, Rayleigh quotient, spectral ordering, and scale ledger.
It must then determine whether PG3 actually constructs that object and whether
its classical mode supports a physical Roper N(1440) identification. Exposing
a source defect or unsupported particle label does not finish the campaign;
the positive general theorem and, if its declared model closes, independently
refined conditional spectrum remain required.

## Base Release and Provenance

The accepted base is `v0.55.0` at framework commit `d76ebb6`, whose scientific
transaction is `0c3585e`. The pinned predecessor is `substrate@6d1f4e0`; PG3
is `/home/dan/substrate/merged-framework/bridges/phase-18/bridge_PG3_roper_radial_excitation.py`
with independently verified SHA-256
`4e3b56ab04977d254a291dd56d28e3285d72e86b3d640e0cfc322d5818cf007f`.
PG3 is pending in the generated queue and names B1, E2, E4, and S2, all still
pending, as dependencies. The predecessor checkout is at the pinned commit but
has unrelated later Phase 47/48 and memory changes, which remain excluded.
The fresh physics-skill preflight passes seven checks without warnings, the
framework tree was clean before this contract was instantiated, and git
history separates the accepted release from its effort-memory sync. Memory
supplies only the accepted frontier and the PG3 pointer; every scientific fact
will be re-sourced. The queue synopsis necessarily exposes the claimed
positive eigenvalue and physical headline, but PG3's executable equations,
checks, and detailed outputs remain unopened at this boundary.

## Invariants, Conventions, and Allowed Imports

A classical radial fluctuation spectrum requires a declared action or paired
kinetic and energy quadratic forms, an actually stationary background, a
domain, a positive kinetic weight, and self-adjoint boundary conditions. A
finite-box positive eigenvalue is not automatically a continuum bound state.
For the scale family `f_lambda(r)=f(lambda*r)`, the infinitesimal tangent at
unit scale is `r*f'(r)`; it is neither a translation tangent nor automatically
an exact zero mode. Classical spatial `l=0` gives no spin one-half, isospin,
fermionic quantization, baryon identity, or Roper dictionary.

Allowed accepted inputs are C-SYM-001's exact stationarity requirement,
C-QBL-003's classical-Hessian versus particle-mass ceiling, C-SK-001 only as
a conditional algebraic mass identity with a free hedgehog coefficient, and
C-DIM-003's free mass-coordinate ledger. Standard exact variational calculus,
Sturm-Liouville and Rayleigh-Ritz mathematics, and explicitly refined SciPy
BVP/eigensolver evidence are permitted. Pending B1, E2, E4, and S2, inserted
nucleon or Roper masses, a fitted physical scale, collective quantization, and
an unaccepted hedgehog action or profile are forbidden premises.

## Candidate Preregistration

The candidate set is frozen before opening PG3's executable internals.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal PG3 reproduction | Every headline object is defined and actually checked | Source symbols only | Narrow numerical or algebraic subclaims may survive while stationarity, scale, or particle identity enters by declaration | Hash-pinned execution, data-flow audit, and load-bearing mutations |
| B | General radial Sturm-Liouville theorem | Declared positive kinetic weight, energy Hessian, stationary profile, and self-adjoint domain | Coefficient functions, domain, boundary data | The mode problem and Rayleigh quotient follow exactly; positivity, binding, and node order remain separate predicates | Exact variation and Green identity plus a soluble-limit spectrum |
| C | Derrick collective coordinate | Declared scaled profile family and finite inertia/energy | Scale coordinate and any energy homogeneity components | The tangent is `r*f'`, and its frequency is curvature divided by inertia; zero or softness follows only from the computed curvature | Differentiate the profile family and energy twice; mutate a homogeneity coefficient |
| D | Conditional Option-C reconstruction | A complete source action, BVP, quadratic form, and scale-free boundary problem survive audit | Every declared coupling, cutoff, wall, mesh, and tolerance | A refined stationary branch and self-adjoint spectrum may earn numeric evidence without physical labels | Independent collocation, operator assembly, mesh/domain/tolerance refinement, node count, and soluble-limit mutation |
| E | Scale and interpretation ledger | Only the classical dimensionless spectrum is supplied | Time scale, background energy, quantization rule, and state dictionary remain independent | A classical frequency cannot determine a Roper mass ratio or J=1/2 identity without extra load-bearing premises | Exact rescaling families and alternative dictionaries preserving the classical eigenproblem |

## Selection Criteria and Blinding

Selection is ordered by accepted dependency closure, derivation from an
explicit stationary action, positive kinetic and self-adjoint structure,
dimensions and boundary regularity, assumption and parameter economy, known
scaling and continuum limits, mutation sensitivity, numerical refinement, and
independent assembly. Numerical proximity to `0.097`, a nucleon/Roper mass
ratio, or another physical comparator is excluded from selection. The queue-
exposed numbers cannot set equations, tolerances, branches, or pass windows.
Candidate objects, structural gates, and interpretation ceilings are frozen
here before PG3's executable is opened.

## Proposed Claim Delta

Provisional C-MOD-001 may state the exact radial second-variation and
generalized Sturm-Liouville theorem, including Green boundary form, Rayleigh
quotient, positivity conditions, and the distinction among a zero tangent, a
positive box eigenvalue, and a continuum bound state. Provisional C-MOD-002
may state only a fully declared, independently refined Option-C stationary
profile and spectrum if the source supplies enough action-level closure.
Provisional C-SCL-001 may state the exact rescaling and free-premise ledger
between a classical dimensionless frequency and any excitation energy or mass
ratio. No claim may identify a mode as a physical Roper, assign J=1/2, import a
pending dependency, or use a comparator to define the result. Claims will be
reviewed individually and may be narrowed or rejected without blanket
promotion.

## Implementation and Oracle Plan

A pure additive module under `src/substrate_framework/` will expose exact
radial quadratic-form and scaling identities plus, only if admissible, a
side-effect-free conditional BVP/spectrum API using shared numerical evidence
patterns. The module will not execute a solve at import time. Exact SymPy
variation and boundary-form algebra are the strongest oracles for the general
theorem and Derrick tangent. A soluble radial operator will independently test
the spectrum and node ordering. If Option-C survives audit, SciPy collocation
and a symmetric sparse or tridiagonal generalized eigensolver will record
float64 precision, equations, cutoffs, boundary data, mesh, tolerances, status,
residual norms, domain and mesh refinement, continuum threshold, and node
counts. An independently assembled shooting or finite-volume/finite-difference
route must reproduce the structural verdict. Mutations will alter the kinetic
weight, potential coefficient, background stationarity, origin condition,
outer wall, domain, mesh, and scale dictionary. Canonical quadrature, if
needed, will use `numpy.trapezoid`, never the version-specific deprecated
alias. Focused tests and scientific verifiers precede one full workflow gate
at promotion; unchanged full tests will not be duplicated.

## Attempts and Continuation

The append-only ledger contains five attempts. Attempt 0001 reproduces PG3's
eight-check tally and preserves the conditional profile while rejecting the
bound-mode, Roper, quantum-label, and gap-ratio headlines. Attempt 0002 derives
the complete Hessian and shows that its lowest positive box level collapses
like the inverse wall radius squared. Attempt 0003 passes 30 primary checks
covering exact variation, profile refinement, continuum classification,
mutations, and scale accounting. Attempt 0004 preserves an independent
`solve_bvp` callback-signature failure. The repaired, otherwise unchanged
attempt 0005 passes 16 checks through fresh symbolic expansion, collocation,
Simpson quadrature, and a mass-lumped finite-volume spectrum. Candidates B,
C, and E are selected; D is selected only for its qualified profile and box-
continuum content; A remains rejected as the advertised physical route.

## Debt Ledger

This ledger tracks action and profile provenance, stationarity, kinetic
weight, Hessian normalization, self-adjoint boundaries, scale and translation
tangents, spectral binding and ordering, numerical refinement, physical label
imports, independent evidence, consumers, and canonical synchronization.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| PG3's literal equations, checks, imports, and output are unaudited | Hash-check, execute, trace every subclaim to its defining object, and preserve output or failure | discharged by source reproduction, source audit, and attempt 0001 |
| The positive radial second-variation object is not implemented | Derive the quadratic forms, operator, boundary form, weight, Rayleigh quotient, scale tangent, and limiting guards in tested importable APIs | discharged by `radial_modes.py`, focused tests, and attempts 0002/0003/0005 |
| The Option-C background and spectrum may depend on pending units or copied values | Reconstruct only from a complete declared action/BVP or reject that numerical candidate and preserve the exact missing closure | discharged conditionally by independent shooting/collocation; no pending unit or comparator is imported |
| A box eigenvalue may be mislabeled a bound physical excitation | Audit continuum threshold, node ordering, domain refinement, dimensional scale, and quantization/state dictionary separately | discharged by the exact zero threshold and inverse-wall-squared collapse under two spectral assemblies |
| A declared Derrick or translation mode may be miscomputed | Differentiate the actual profile family and coordinate transformations and test the operator residual or Rayleigh quotient | discharged by exact logarithmic scaling; PG3's radial shift is rejected as a rigid translation test |
| Numerical checks may be insensitive | Mutate every load-bearing coefficient and boundary, refine independently, and require relevant verdicts to break | discharged by mixed-term, weight, potential, mesh, domain, residual, and soluble-limit tests |
| Downstream impact and independent review are unknown | Complete graph impact analysis, independent rederivation, targeted replay, and claim-level review | discharged by additive graph analysis, independent attempt 0005, and three separate claim reviews |
| Registry, release, docs, queue, and memory are unsynchronized | Promote only reviewed claims, regenerate canonical consumers, and empty this campaign ledger | discharged by the v0.56.0 promotion transaction and canonical generators |

## Review and Promotion Plan

C-MOD-001, C-MOD-002, and C-SCL-001 received separate reviews over exact
quadratic forms, boundaries, solver diagnostics, refinements, mutations,
scales, and interpretation ceilings. All accepted APIs move into the package
and release `v0.56.0` with generated docs and accepted memory. PG3 is qualified
because its conditional stationary profile survives while its incomplete
Hessian, bound-mode, Roper, J=1/2, and gap-ratio readings do not. The editable
migration disposition is the only hand-authored queue input; the queue is
regenerated mechanically.

## Done Gate

P062 closes with C-MOD-001, C-MOD-002, and C-SCL-001 accepted in `v0.56.0`
and PG3 qualified after the positive radial-mode APIs, 30 primary and 16
independent checks, focused and full replay, claim-level reviews, regenerated
consumers, and empty campaign debt ledger pass. The parent corpus migration
remains active because later queue units remain pending.
