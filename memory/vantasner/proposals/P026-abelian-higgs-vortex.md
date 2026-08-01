---
description: Audit CF1's conditional Abelian-Higgs vortex and BVP evidence
author: vantasner
created: '2026-08-01T15:28:12Z'
updated: '2026-08-01T15:41:27Z'
tags:
- substrate-framework
- campaign-proposal
- abelian-higgs-vortex
- migration-CF1
category: proposals
confidence: exploratory
status: archived
---
# P026 Abelian-Higgs Vortex

## Question and Positive Deliverable
P026 must determine whether CF1 supplies a mathematically closed conditional
radial Abelian-Higgs vortex and trustworthy numerical BVP evidence. The positive
deliverable is importable exact equations, energy and flux machinery, plus a
separately scoped numerical claim if convergence survives. A vortex in a
declared Abelian-Higgs model is not by itself a substrate, chromoelectric, QCD,
dual-superconductor, or confinement construction.

## Base Release and Provenance
The accepted base is `v0.22.0` at commit `cf65ac8`. `C-DIM-007` fixes only the
power of a tension when its existence and sole-scale premises are declared;
it does not build a flux tube. `C-TOP-001` is only an integer winding character.
The hash-pinned candidate is CF1 at
`merged-framework/bridges/phase-10/bridge_CF1_dual_superconductor_flux_tube.py`,
SHA-256 `a4ec97923804f1b7c624b7619bc6b6a1cbb62f42d659897799545b257ca33f5d`.
Memory search found no accepted vortex construction, so source equations and
numerical values will be independently audited.

## Invariants, Conventions, and Allowed Imports
The radial functional, gauge ansatz, coupling normalization, winding sign,
coordinate measure, and boundary conditions must form one convention set.
Integer winding is an explicit model input. Exact variational calculus and
cylindrical geometry are allowed. SciPy BVP machinery must be called through
the shared numerical evidence module and must expose solver success and
residuals. No physical gauge-sector identification or confinement premise is
allowed.

## Candidate Preregistration
The candidates are frozen from migration metadata before reading CF1's full
implementation or reported tension.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Promote exact conditional vortex equations/flux and a separate numerical BVP/tension claim | Declared Abelian-Higgs functional and ansatz | Explicit winding, couplings, vacuum scale, truncated radial domain | Compatible conditional model | Exact EL rederivation plus solver-status, residual, domain, mesh/tolerance, and independent-route checks |
| B | Promote only exact equations and finite-energy boundary consequences | Same functional, no numerical existence conclusion | Symbolic parameters | Preferred if source convergence measures only repeated collocation output | Recompute the BVP with multiple domains, tolerances, guesses, and an independent method or soluble limit |
| C | Promote a physical substrate chromoelectric tube and confinement mechanism | Unaccepted dual-superconductor and gauge-sector map | Physical QCD parameters | Conflicts with accepted interpretation boundaries | Dependency closure for the physical map and a nonperturbative confinement oracle |

## Selection Criteria and Blinding
Selection is ordered by functional/equation convention closure, regularity and
finite-energy boundaries, solver-status and residual evidence, domain and
tolerance convergence, independent numerical or analytic agreement, parameter
economy, and interpretation scope. The tension value visible in migration
metadata is excluded from candidate selection and treated only as a source
regression after the equations and thresholds freeze.

## Proposed Claim Delta
Provisional `C-VTX-001` would state the exact radial Euler-Lagrange equations,
finite-energy asymptotic gauge condition, and flux for one declared convention.
Provisional `C-VTX-002` would record only resolution-bounded existence and
tension evidence for an explicit parameter/domain family. The claims are
reviewed independently; failure of the numeric claim does not lower the exact
claim's standard or terminate the migration effort.

## Implementation and Oracle Plan
A pure `abelian_higgs_vortex.py` module will own the functional density,
Euler-Lagrange residuals, flux, BVP equations/boundaries, solver, and tension
quadrature. SymPy is the oracle for variation, dimensions, regularity, and
normalization mutations. Numeric evidence will state the equations, parameter
values, radial interval, boundary data, initial mesh/guess, collocation
tolerance, maximum nodes, residual norm, quadrature, and convergence metric.
It will vary initial mesh, outer domain, inner cutoff, tolerance, and initial
guess; verify boundary residuals and finite energy; and compare either a
shooting construction or an analytically controlled limit. Mutating winding,
coupling normalization, a boundary value, or an equation sign must break a
load-bearing verdict.

## Attempts and Continuation
Attempt `0001` will reproduce CF1 and inventory the actual solver and energy
checks. Solver, quadrature, and representation failures are preserved
append-only and repaired. If numeric independence cannot be earned, Candidate B
remains a positive exact result and further numeric attempts continue only when
they add a stronger oracle rather than another repeated solve.

## Debt Ledger
This ledger tracks convention, numerical, and physical-interpretation debt.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| Functional and displayed ODEs may use inconsistent gauge normalization | Derive both equations and flux from one frozen ansatz | discharged |
| Repeated adaptive meshes may mimic convergence | Add residual, domain, cutoff, tolerance, guess, and independent-route checks | discharged |
| Reported tension may depend on truncation or omitted terms | Audit the full radial integrand and tail behavior | discharged |
| Conditional vortex may be renamed physical confinement | Exclude the map or supply separately accepted nonperturbative closure | discharged |

## Review and Promotion Plan
Exact and numerical claims receive separate reviews and four-axis decisions.
Promotion requires importable APIs/tests, immutable attempts, source
reproduction and check-level adjudication, migration disposition, release and
generated synchronization, targeted consumer replay, and one full unchanged
gate. Mixed exact/numeric support with rejected physical interpretation gives
CF1 a qualified disposition.

## Results and Promotion
The predecessor passes two exact checks and then fails at removed `np.trapz`, so
its advertised terminal tally is not reused. Three preserved repair attempts
precede attempt `0004`, which passes 31 exact and refinement checks. The
independent sparse finite-difference route passes six checks and converges from
101 through 401 points toward the collocation tension; 14 focused tests pass.
`C-VTX-001` promotes exact conditional model structure and `C-VTX-002` promotes
only bounded numerical evidence. CF1 is qualified, with every dual, QCD,
substrate, confinement, absolute-scale, and v=0-uniqueness reading excluded.

## Done Gate
P026 is complete. CF1 has a terminal qualified disposition, the convention is
closed, the numerical verdict has independent convergence and sensitivity,
physical overreach is excluded, consumers are recorded, and the debt ledger is
empty.
