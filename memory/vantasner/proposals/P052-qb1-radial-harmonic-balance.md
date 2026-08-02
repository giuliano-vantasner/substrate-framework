---
description: Construct and audit a radial sine-Gordon harmonic-balance quasibreather
author: vantasner
created: '2026-08-02T02:45:00Z'
updated: '2026-08-02T06:00:00Z'
tags:
- substrate-framework
- campaign-proposal
- radial-sine-gordon
- migration-QB1
category: proposals
confidence: exploratory
status: archived
---
# P052 QB1 Radial Harmonic-Balance Audit

## Question and Positive Deliverable

P052 must construct a reusable, importable odd-harmonic formulation of the
dimensionless radial sine-Gordon equation and determine the strongest honest
finite-domain or radiation-aware quasibreather object supported by QB1. The
deliverable includes explicit projected equations, origin and outer data, a
nontrivial normalization or continuation coordinate, residuals outside the
solve grid and retained harmonic subspace, and a numerical solution only if it
passes refinement and independent reconstruction. A failed root, an artificial
box mode, or a no-go observation does not complete the positive solver and
adjudication object.

## Base Release and Provenance

The accepted base is `v0.45.0` at framework commit `6039190`; its last
scientific transaction is `8eaf104`. The authority relevant here is
`C-SG-001` and `C-PDE-001`, supported by the canonical radial solver and P044.
QB1 is a pending primary unit at `substrate@6d1f4e0`, path
`merged-framework/bridges/phase-16/bridge_QB1_radial_eigenvalue_quasibreather.py`,
SHA-256 `1f387c140ca80be0e457efd17146267bdecab1cbdbcdd10dd34287bc5de2dc7a`.
Its P3D1 link is source evidence; only accepted `C-PDE-001` may enter the
dependency closure. Memory search found the migration handoff and P044's
preregistered but unused Fourier/BVP alternative, not an accepted QB1 result.
The full QB1 source and its reported numerical root remain unopened until this
contract is frozen.

## Invariants, Conventions, and Allowed Imports

The declared equation is
`u_tt-u_rr-(2/r)u_r+sin(u)=0` in dimensionless 3+1 radial coordinates, with
even regularity at the origin. A cosine expansion uses a declared phase origin;
half-period antisymmetry, if imposed, permits odd temporal harmonics but does
not prove a solution exists. Every finite outer boundary is a model or
numerical condition, not spatial localization by definition. `C-PDE-001`
supplies resolution-bounded evolution of one Gaussian IVP and a frequency
interval only; it supplies no exact periodicity, eigenfrequency, uniqueness,
or infinite lifetime. Standard Fourier orthogonality, radial calculus, and
audited SciPy BVP, least-squares, quadrature, and continuation methods are
permitted. No source-reported frequency, field profile, lifetime, gravity,
particle label, or substrate interpretation is an input.

## Candidate Preregistration

The candidate set is frozen from queue metadata and accepted radial
invariants before the QB1 executable or its root is opened.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal QB1 odd-cosine harmonic-balance equations and root | Every source truncation, domain, normalization, projection, solver, and boundary choice remains explicit | Source harmonic count, mesh, domain, seed, tolerance, and any frequency parameter | Useful reproduction evidence if correctly posed; no authority from its tally | Hash-pinned run, equation reconstruction, nontriviality guard, residual audit, and load-bearing mutations |
| B | Canonical finite-radius odd-harmonic Galerkin BVP | Regular origin, declared outer data, central-amplitude or other explicit family coordinate | Harmonic set, central amplitude, radius, mesh, quadrature, tolerance | Compatible numerical object with a finite-box ceiling | Radial/time/harmonic/domain/tolerance refinement, continuation, off-grid and omitted-mode residuals, and an independent projection |
| C | Radiation-aware quasibreather with harmonic-dependent asymptotic channels | Explicit standing-wave or outgoing-tail condition rather than universal decay | Fundamental frequency, tail phase or amplitude, matching radius, truncation | Natural if nonlinear harmonics cross the linear radiation threshold | Derive each far-field channel, mutate the asymptotic sign, refine matching/domain, and distinguish finite-energy localization from a tail-bearing quasibreather |

## Selection Criteria and Blinding

Selection is ordered by exact PDE and Fourier normalization, regular origin and
honest outer asymptotics, assumption and parameter economy, convergence in
radial mesh, temporal projection, harmonic truncation, domain, and nonlinear
tolerance, residual control between nodes and in omitted modes, continuation
stability, sensitivity to normalization and boundary mutations, compatibility
with `C-PDE-001`, and independent reconstruction. Numerical proximity to the
P3D1 interval or QB1's reported root cannot select a candidate. The comparator
gate opens only after this contract, the manifest, structural tail tests, and
residual metrics are frozen.

## Proposed Claim Delta

The claim delta is split by oracle in recorded proposal revision 0001.
Provisional `C-PDE-005` may state the exact odd-harmonic projection, origin
regularity, and evanescent/threshold/radiative far-field classification.
Provisional `C-PDE-006` may separately record a premise-explicit,
resolution-bounded finite-box branch if a nontrivial object passes all numeric
gates. Their dependencies are limited to the smallest applicable subset of
`C-SG-001` and `C-PDE-001`; the finite-time trajectory may be a comparator but
not a boundary condition or fitted target. No finite box, finite harmonic
truncation, or small residual will be promoted as an exact infinite-domain
periodic breather, unique nonlinear eigenvalue, lifetime law, gravitational
source, particle, or substrate claim. Expected consumers are the QB1
disposition and pending QB2 through QB4 units.

## Implementation and Oracle Plan

A pure package module will own odd-harmonic indexing, time reconstruction,
nonlinear sine projection, the radial projected residual, origin regularity,
outer-channel classification, branch normalization, and structured BVP or
least-squares evidence. Shared numerical evidence helpers will be reused or
minimally generalized after impact analysis. Imports will not solve or print.

Exact algebra will derive the projected linear operator, origin limit, Fourier
normalization, half-period selection rule, and far-field channel thresholds.
SciPy is appropriate for the coupled nonlinear BVP or least-squares root; the
record will include float64, equations, radius interval, origin and outer data,
mesh, harmonic count, temporal quadrature or collocation, algorithm, tolerance,
node limit, status, residual norms, and continuation coordinate. Radial mesh,
temporal samples, retained harmonics, domain or matching radius, and tolerance
will be varied independently. Residuals will be evaluated on a denser radial
and temporal grid and projected into at least the first omitted odd harmonic.
Mutations will change the radial coefficient, sine sign or coefficient,
Fourier normalization, origin rule, branch normalization, harmonic selection,
and outer asymptotics. A separately implemented projection/BVP route or a
time-domain evolution initialized from the reconstructed profile will supply
the independent check without treating agreement to a source value as proof.

## Attempts and Continuation

The append-only campaign preserves eleven attempt stages. Literal QB1 exits
with six checks and reproducible frequency values. A cold unconstrained BVP
then lands on invalid or unintended branches; sub-gap parameterization and
continuation repair that representation. Core-remainder refinement succeeds
through N=9, while an independent review is repaired after a static function-
name typo, an unjustified raw finite-difference tolerance, and a least-squares
stopping failure. Attempt 0010 finally passes DOP853 shooting, Gauss-projected
collocation, and three-grid second-order finite differences; attempt 0011
passes all 41 primary exact, mutation, refinement, calibration, and
interpretation checks.

## Debt Ledger

This ledger tracks source reproduction, equation and projection normalization,
nontrivial branch selection, origin and outer data, harmonic tails, numerical
convergence, independent evidence, interpretation, consumers, and canonical
state.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| QB1's literal equations, solver, and current-environment behavior are unaudited | Hash-check, run, and preserve its complete result or failure | discharged by attempt 0001 and the source-reproduction record |
| No canonical radial harmonic-balance surface exists | Implement pure projected-equation, reconstruction, residual, and boundary APIs with tests | discharged by `radial_harmonic_balance.py` and six focused tests |
| A nonlinear homogeneous BVP admits the trivial field | Declare and test a load-bearing branch coordinate or normalization without inserting the target root | discharged by the explicit central fundamental and amplitude mutations |
| The source's outer condition may conflate a finite box with localization | Derive all harmonic far-field channels and test domain or matching-radius sensitivity | discharged by C-PDE-005 and the R=30/40/50/60 tail scan |
| Truncation and collocation residuals are unknown | Refine mesh, time projection, harmonics, domain, and tolerance and measure omitted modes off grid | discharged by attempts 0004, 0005, 0010, and 0011 |
| Relation to the accepted finite-time IVP is unknown | Compare only after structural selection, without fitting the BVP to the IVP frequency | discharged; P3D1 is a comparator only and QB1's own fit is classified as calibration |
| Consumers and generated state are unreplayed | Complete impact analysis, targeted consumers, one final repository gate, and queue regeneration | discharged; 38 focused tests, P044, the generated queue, and the 372-test gate pass |

## Review and Promotion Plan

The review and promotion transaction is complete. `C-PDE-005` receives the
exact native theorem status `symbolic_verified/accepted/native/active`;
`C-PDE-006` receives the finite-box status
`numeric_evidence/accepted/compatible_extension/qualified`. Reusable logic
lives under `src/substrate_framework/`, QB1 has a structured qualified
disposition, v0.46.0 pins both claims, and generated docs and accepted memory
match the registry. The source's unsupported subclaims remain named in its
source adjudication rather than inheriting acceptance from the campaign.

## Done Gate

P052 is closed. The positive harmonic-balance API, exact channel theorem,
finite-box N=9 branch, source adjudication, load-bearing mutations, convergence
and wall scans, three independent numerical routes, claim-level reviews,
consumer replay, qualified QB1 disposition, and v0.46.0 transaction all pass.
The final unchanged-boundary gate validated 64 accepted claims, 218 migration
units with 168 pending and 43 qualified, 232 memory records, the repo-local
skill, and 372 tests; `git diff --check` passes. The campaign debt ledger is
empty and the parent migration continues at QB2.
