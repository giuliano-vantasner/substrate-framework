---
description: Derive a normalized scalar-lattice continuum ledger and audit ME3
author: vantasner
created: '2026-08-03T04:35:00Z'
updated: '2026-08-03T05:10:00Z'
tags:
- substrate-framework
- campaign-proposal
- lattice-continuum
- migration-ME3
category: proposals
confidence: exploratory
status: archived
---
# P069 ME3 Lattice-to-Continuum Audit

## Question and Positive Deliverable

P069 must deliver an importable exact nearest-neighbour scalar-lattice
operator, its full Brillouin-zone symbol and controlled long-wave expansion,
and a measure-normalized discrete sine-Gordon action with a precisely typed
continuum limit. Reproducing the coefficient `1/12` or documenting an omitted
spacing factor does not complete the campaign.

## Base Release and Provenance

The accepted base is `v0.62.0` at scientific commit `3b4e9f2`; parent-effort
synchronization is commit `47a9f05`. The predecessor is pinned at
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`. ME3 is
`/home/dan/substrate/merged-framework/bridges/phase-20/bridge_ME3_lattice_continuum.py`,
19045 bytes, with inventory and reproduced SHA-256
`8b5f888708b2edc202cb1acba37780aa62e7d71d002dc5042fd92e8afefbb0d0`.
The generated queue marks ME3 pending and lists ME1 and ME2 as candidate
dependencies, but neither supplies a premise needed by the scalar lattice
problem. The clean framework tree, recent history, seven-check preflight,
registry, current release, accepted normalized sine-Gordon and numerical
modules, generated synopsis, package searches, templates, and durable memory
were inspected before this contract. Memory contains no accepted spatial
lattice continuum theorem. ME3's executable body and detailed output remain
unopened.

## Invariants, Conventions, and Allowed Imports

C-SG-001 supplies the normalized continuum equation only. P069 may use exact
finite differences, Taylor expansion with explicit regularity and remainder,
finite Fourier modes, periodic Riemann sums, and C-VAR-001's fixed-global-factor
theorem. The interval, periodic boundary condition, site count, spacing,
sampling map, field dimensions, smoothness, time interval, action measure, and
wave-number domain must remain visible. A local truncation formula is not an
operator, action, or solution convergence theorem. The exact symbol is retained
on the first Brillouin zone, and the spacing remains an input rather than a
substrate or Angstrom-scale prediction. Exact obligations use no quadrature;
any sampled regression must call the shared current-first `np.trapezoid`
compatibility helper rather than a version-specific alias.

## Candidate Preregistration

The candidate set is frozen before ME3's executable is opened.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal ME3 | Its sums, signs, smoothness, and limits are already typed | source inputs | Some algebra may survive, while action and physical readings may require repair | Hash-pinned execution and data-flow audit |
| B | Exact Fourier symbol | Periodic uniform nearest-neighbour lattice | `a,N,k` | The symbol is `-4*sin(ka/2)^2/a^2` on the first Brillouin zone | Direct eigenvector substitution, edge and alias probes |
| C | Physical-space Taylor ledger | A sufficiently smooth field near one site | `a` and derivative jet | The centered difference has the even-derivative series with a controlled remainder | Independent plus/minus Taylor expansions and polynomial counterexamples |
| D | Normalized discrete action | Fixed periodic interval and Riemann weight `a` | `a,N,T` | Variation gives the discrete sine-Gordon equation and the action has a finite continuum limit | Exact variation, constant/one-mode limits, missing-weight mutation |
| E | Modewise convergence | Resolved smooth trigonometric polynomial | `a,k` | Operator and action errors are second order for fixed physical modes | Exact series plus grid refinement as regression evidence |
| F | Unweighted action equivalence | Fixed nonzero `a` only | `a` | Dropping the overall weight preserves the fixed-grid EOM but not the action-value limit | C-VAR-001 application and divergent constant-field sequence |

## Selection Criteria and Blinding

Selection is ordered by accepted closure; exact normalization and sign;
boundary, measure, and dimension typing; full-zone behavior and correct smooth
limits; separation of convergence notions; mutation sensitivity; and parameter
economy. The source's displayed `1/12`, `1/360`, and matching dispersion cannot
select the action convention or physical interpretation.

## Proposed Claim Delta

Provisional C-LAT-001 may state the exact periodic lattice Laplacian symbol,
its controlled long-wave expansion, a Riemann-normalized discrete sine-Gordon
action and Euler-Lagrange equation, and a bounded modewise continuum statement.
It may depend on C-SG-001 for the target continuum convention and C-VAR-001 for
global fixed-spacing action equivalence. It may not establish solution
convergence for arbitrary data, nonlinear stability, a three-dimensional
lattice, a hydrogen medium, spacing selection, an EFT cutoff identity, or any
material or substrate realization.

## Implementation and Oracle Plan

A pure `lattice_scalar.py` module may expose the centered operator, exact
symbol, Taylor coefficients/remainder ledger, normalized periodic action, its
discrete Euler-Lagrange residual, and long-wave dispersion. SymPy exact algebra
fits the finite-difference, variation, Fourier, and series obligations. An
independent route will derive the symbol from shift eigenvalues and the action
from a fresh index variation without importing the canonical API. Mutations
will reverse the spatial sign, replace the centered stencil, omit the Riemann
weight or gradient denominator, copy the target coefficient, admit unresolved
aliases, and treat `a=0` as a finite lattice. Constant fields, affine/quartic
polynomials, one Fourier mode, `k=0`, and the Brillouin edge provide limiting
and counterexample probes. A short grid refinement may guard the package
implementation but is not independent evidence when the exact symbol already
fixes its result. If a sampled integral is useful, it uses
`substrate_framework.numerics.trapezoid_integral`, which resolves
`np.trapezoid` first and retains the legacy name only for supported NumPy 1.26.

## Attempts and Continuation

Attempt 0001 will preserve ME3's native process and trace every assertion. If
the source confuses a site sum with an integral, omits boundary or smoothness
hypotheses, or turns a long-wave series into a global equality, that failure is
recorded and Candidates B-E continue. Candidate F can repair fixed-grid
equations but cannot close the continuum action objective alone.

## Debt Ledger

The campaign tracks measure, stencil, smoothness, convergence, aliasing,
dependency, verification, and synchronization debt.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| ME3's executable and output are unaudited | Hash-check, execute, preserve output, and trace all checks | discharged by attempt 0001 and source audit |
| The discrete action normalization and field dimensions may be incomplete | Derive a typed Riemann-normalized action and audit every spacing power | discharged by the periodic action and variation |
| A local Taylor series may be promoted to a global continuum theorem | State smoothness, remainder, domain, norm, and the exact convergence scope | discharged by the local remainder and action-error bound |
| The small-wave-number dispersion may hide aliases or edge behavior | Retain the full symbol and test zero, edge, and aliased modes | discharged by the exact Brillouin-zone ledger |
| ME1/ME2 or a material spacing may be imported as authority | Audit source data flow and exclude every unaccepted physical premise | discharged; ME1/ME2 and physical spacing are excluded |
| Verifier sensitivity, review, and synchronization are incomplete | Complete mutations, independent derivation, impact replay, claim review, disposition, release, docs, queue, and memory | discharged at the v0.63.0 promotion boundary |

## Review and Promotion Plan

Any proposed claim receives independent review of stencil normalization,
Taylor remainder, index variation, action measure, exact symbol, long-wave
sign, Brillouin scope, convergence semantics, and interpretation ceiling. ME3
receives a terminal disposition only through the authoritative queue with
durable evidence. Accepted logic moves into the package with focused tests and
one full promotion-boundary workflow gate.

## Done Gate

P069 closes only when the positive importable lattice/action ledger, sensitive
exact oracles, independent derivation, source adjudication, claim-level
decision, downstream replay, canonical synchronization, and empty campaign
debt all pass. A Taylor coefficient or source pass tally alone is not
completion.

## Adjudication Outcome

Candidates B through E are accepted in C-LAT-001. Candidate A survives only
for narrow formal stencil and normalized linearized long-wave fragments;
Candidate F survives only as fixed-grid global-multiplier equivalence. ME3 is
qualified. The exact primary route passes 55 checks, the independent route
passes 23 checks, focused/governance replay passes 37 tests, and the full
workflow passes all 561 tests. The v0.63.0 registry, release, queue, generated
docs, and accepted memory agree.

## Cross-References

See C-SG-001, C-VAR-001, ME3's generated source record, release `v0.62.0`, and
the parent migration effort.
