---
description: Select and validate one complete local Lorentz-covariant M5 4x4 action
author: codex
created: '2026-08-20T11:06:43+02:00'
updated: '2026-08-20T18:40:00+02:00'
tags:
- substrate-framework
- campaign-proposal
- m5
- lorentz-covariant-action
category: proposals
confidence: exploratory
status: active
---

## Question and Positive Deliverable

P239 asks which smallest explicit local Lorentz-covariant M5 4x4 action can
simultaneously retain the established spatial 3x3 and Coulomb reductions,
select a finite nonzero fixed-angular-momentum electron-hedgehog frequency,
and produce an attractive inverse-square interaction between fully relaxed
mass defects. The deliverable is the selected action, independent coefficient
relations, exact field equations and sector reductions, refined one- and
two-defect solutions, reusable implementation, individual reviews of
C-M5-001 through C-M5-004, accepted registry entries, and a pinned release.
A failed contraction or no-go is attempt evidence and does not complete #147.

## Base Release and Provenance

The accepted base is `v0.163.0` at
`substrate-framework@6e5a4ba001bfdb41ea6e5157a43b0a854d118e1a`.
Accepted inputs are C-LOR-002 for the mostly-plus Lorentz-generator convention,
C-KRN-001 for a conditional three-dimensional massless Green kernel,
C-VAR-003 for separately relaxed interaction energies, and C-IGR-004 plus
C-GRV-002 for the conditional total gravitational coupling and sign map.
P236 is noncanonical evidence/machinery: issue #96 is reopened because its
landed headline minimized one ambient rapidity with imposed Gaussian cores.
The corrective branch at `1f8b728` will be audited before any implementation
is transferred. OpenWave is pinned at public current main
`c001aa26afc344806781153fd8f71816e347e70e` and at P236's verified source
object `614a223fff01b768550b0917d0f96621d6bbe155`.

## Source Inventory and Access Gate

Every load-bearing source is accessible, but its scientific authority is
typed before use.

| Source | Access status | Extracted claims (with page/eq) |
| --- | --- | --- |
| OpenWave current M5 source at `c001aa26...` | Public Git, HEAD verified | Current canonical action and M5.21.14-16 source surfaces; exact equation/file-hash inventory is the first post-schema artifact |
| OpenWave P236 source at `614a223fff...` | In-hand detached checkout | M5.8 fixed-clock, M5.17 two-center, M5.21.14 guarded dressing, M5.21.15 fixed-J, M5.21.16 contraction comparison |
| P236 campaign and correction branch | Repository and remote ref accessible | Stationary solver, quadrature, common-action subtraction, force fitting; no accepted M5 claim |
| Issue #146 Jarek Duda direction | Public GitHub comment | Retain spatial Coulomb, reverse boost/Newton sign, finite nonzero hedgehog omega; test traced curvature-squared terms first |
| Accepted release `v0.163.0` | In hand | Exact conditional imports named above |

## Invariants, Conventions, and Allowed Imports

Spacetime uses `eta=diag(-1,1,1,1)`. Each retained term must be a typed local
Lorentz scalar under one source-verified index convention. Spatial restriction
must recover the audited 3x3 functional without reinterpreting coefficients.
Charge and mass sectors share one action, admissible field space, boundary
data, and stationary definition. Pair interactions use separately relaxed
energies and never imposed Gaussian overlap. Finite frequency means a strict
interior minimum at fixed nonzero angular momentum with positive inertia.
Allowed imports are exactly the accepted claims and pinned public sources in
the manifest. OpenWave/P236 evidence is proposal input, not accepted canon.

## Candidate Preregistration

The scientific mechanism is open, so five materially different local routes
are registered before any new P239 comparator is evaluated.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Complete independent curvature-squared contraction basis | Source tensor symmetries and local second-derivative order | Independent dimensionless quadratic ratios after overall normalization | Best parameter economy and exact Lorentz covariance | Simultaneous nonempty coefficient region for 3x3 recovery, Coulomb sign, bounded fixed-J inertia, and Newton sign |
| B | A plus the minimum quartic curvature/current stabilizer | One higher local invariant | One additional coefficient unless identities reduce it | May bound the boost sector without changing infrared quadratic kernels | Exact reduction plus positive high-gradient coercivity and refined stationary branches |
| C | A plus sextic current/curvature term and Lorentz-scalar spectrum potential | Local higher order and declared preferred spectrum | Minimum independent sextic and potential coefficients | Stronger scale selection at greater assumption cost | Strict fixed-J interior minimum and unchanged long-range kernels with regular cores |
| D | Local auxiliary mediator with exact algebraic elimination | Auxiliary field is local, covariant, and non-propagating or has a derived kernel | Minimum kinetic/coupling coefficients | Makes exchange sign explicit but risks adding field content | Exact local elimination into an eligible 4x4 invariant and no hidden fitted Green kernel |
| E | Field-dependent spectral-Cartan internal metric | A simple real timelike eigenline of `eta^-1 M`, continuously connected to the vacuum `g` branch | No new coefficient or field | Covariantizes the healthy internal Frobenius contraction while preserving the full 3x3 action | Exact covariance, projector applicability, positive Hamiltonian, relaxed hedgehog, and relaxed-pair gates |
| F | E plus the timelike-projector sigma current | Same simple timelike branch; one positive stiffness `kappa` | One dimensionful coefficient, no new field | Adds the boost Goldstone's Laplace kernel and Derrick `R` term while remaining zero on every uniform-time-row 3x3 field | Exact scaling/linearization followed by stationary hedgehog and relaxed-pair refinement |

Attempt 0001 rejected A: the complete 3x3-preserving quadratic nullspace
vanishes on an explicit negative clock direction constructed from symmetric
M5 field derivatives. Attempt 0002 selected E at the action-structure level.
Its exact local density uses
`h^ab=eta^ab-2 P_t^a_c eta^cb`, where `P_t` is the local spectral idempotent
of the simple timelike branch. It passed exact covariance, positive-energy,
static-reduction, source-clock, and fixed-Frobenius mutation gates. The
stationary-solution and force gates remain open. Exact post-attempt power
counting then exposed that E alone is quartic around the vacuum orbit and
scales only as `1/R`; F was registered before numerical output as its minimum
two-derivative completion.

## Selection Criteria and Blinding

The ordered criteria are Lorentz/index validity, boundedness and regular
stationarity, exact 3x3/charge recovery, common force/frequency mechanism,
assumption and parameter economy, dimensions/topology/limits, accepted-sector
composition, then numerical robustness. Empirical closeness is last. Issue
#147 publicly exposed earlier P236/OpenWave values before P239 existed; that is
recorded as unavoidable prior exposure. New P239 force/frequency outputs remain
blinded until the complete invariant basis, reductions, coefficient domains,
solver, boundary data, norms, thresholds, and mutations are frozen.

## Proposed Claim Delta

The provisional identifiers were collision-searched across registry,
campaigns, proposals, and durable memory before reservation.

| Claim | Proposed positive statement | Dependencies | Evidence and consumers |
| --- | --- | --- | --- |
| C-M5-001 | One explicit selected local Lorentz-covariant 4x4 action has the complete declared invariant basis, exact Euler-Lagrange equations, bounded energy-Casimir domain, and exact 3x3/charge/boost/hedgehog reductions | approved pinned M5 source; C-LOR-002 convention | SymPy tensor/reduction proof plus independent component contraction; canonical action API and all later P239 claims |
| C-M5-002 | The selected action has a regular relaxed electron-hedgehog branch with `0<omega*=J/(2I)<infinity` and a strict fixed-J energy minimum | C-M5-001 | exact fixed-J derivative/Hessian identities plus refined SciPy branch and independent solver |
| C-M5-003 | Separately relaxed charge defects have `U_C=K_C q1 q2/r+o(1/r)`, `K_C>0` | C-M5-001, C-KRN-001, C-VAR-003 | exact infrared kernel reduction plus relaxed two-defect convergence and sign/source mutations |
| C-M5-004 | Separately relaxed mass defects have `U_N=-K_N m1 m2/r+o(1/r)`, `K_N>0`, with the conditional C-IGR-004/C-GRV-002 coefficient bridge | C-M5-001, C-KRN-001, C-VAR-003, C-IGR-004, C-GRV-002 | exact boost-kernel/sign reduction plus relaxed two-defect convergence, independent representation, and coupling typing |

No existing accepted claim is challenged or changed by the initial proposal.
Any independent canonical inconsistency will open a separate challenge.

## Implementation and Oracle Plan

Reusable pure APIs will live in `m5_covariant_action.py` and
`m5_stationary_fields.py`; campaign scripts will import them. SymPy will
enumerate contractions, remove tensor-identity duplicates, vary the action,
and derive exact sector coefficients. An independent explicit-component route
will reconstruct every load-bearing contraction. SciPy will solve the reduced
radial BVP and the relaxed spatial stationary systems with solver-success,
finite-data, residual, boundary, refinement, and method-cross-check gates.
Canonical quadrature will use `trapezoid_integral`; sparse operators and
source-centred coordinates will be used where appropriate. New numerical
thresholds will be scale-relative and frozen before production. Mutations flip
Lorentz signature, remove a traced term, corrupt one source, delete the
stabilizer, and break fixed-J sign/normalization; each must fail its relevant
gate. Direct/imported/dynamic `np.trapz` syntax is preflighted.

## Attempts and Continuation

Attempts are append-only under `proposals/P239-m5-4x4-action/attempts/`.
Wave 0 freezes source conventions and the invariant basis. Wave 1 derives the
exact coefficient map. Wave 2 follows one-body fixed-J branches. Wave 3 runs
relaxed charge/mass pairs. A failed route is diagnosed as implementation,
numerical method, representation, candidate, target, or foundation and queues
the next materially different candidate.

Executed attempts now include the 41-check complete quadratic basis and
source-admissible no-go (`0001`) and the 23-check exact spectral-Cartan action
verification plus six canonical unit tests (`0002`). The next attempt must
derive and solve the fixed-J stationary branch while checking that the simple
timelike eigenline remains isolated throughout the solution.

## Debt Ledger

The initial in-boundary debt ledger is empty. The unresolved action,
coefficients, solutions, and promotion are active campaign frontier, not
promises made by a merged unit. Any later hidden assumption, fitted parameter,
unsupported source bridge, or broken affected consumer must be discharged
before promotion.

## Review and Promotion Plan

C-M5-001 through C-M5-004 each receive one independent claim review at one
frozen transaction, followed by at most one correction check. Successful
reusable logic is extracted before promotion. Promotion updates the accepted
registry, creates the next release manifest, moves the adjudicated P239 record
to `campaigns/`, renders docs with `scripts/render_docs.py`, synchronizes
accepted memory, performs impact-bounded replay, and records one final
content-addressed validation receipt. The authoring agent will leave any PR
ready for a distinct merger unless the repository owner explicitly authorizes
self-merge.

## Done Gate

P239 and issue #147 close only when the explicit action, exact reductions,
finite-frequency branch, relaxed Coulomb and Newton tails, reusable APIs,
individual reviews, accepted registry, release, generated docs, memory, and
empty debt ledger all exist and validate. Any missing item keeps the objective
open and selects the next attempt.

## 2026-08-20 continuation checkpoint

M5.17 uses the uniaxial pure-director exterior `(1,0,0)` and its quartic
Landau-de Gennes potential; M5.18's `(1,delta,0)` trace-power potential is a
later replacement. Attempt 0004 proved the moving biaxial frame has a
logarithmic pole obstruction. Attempt 0005 constructed the exact Lorentz lift
`Y=(I-P_t)(eta^-1 M)(I-P_t)` of the complete M5.17 potential (14/14).

Candidate H adds the massless timelike eigenvalue
`tau=Tr(P_t eta^-1 M)`, its positive scalar current, and
`A(tau)=exp(2 alpha(tau-g))`. Attempt 0007 proved the exact weak-field result
`U_N=-alpha^2*m1*m2/(pi*kappa_tau*r)` (14/14), with exact M5.17 recovery at
`tau=g`. This is an action/kernel theorem only; no nonlinear relaxed Newton
claim is promoted.

Attempts 0008-0012 exposed a principal-eigenvalue closure, an isotropic melt
surface, and a permuted-uniaxial ordinary-rotation runaway. Candidate J made
the clock-axis lift explicit (12/12 exact checks). Candidate K added
`V_lock=zeta*(Tr(Y^2)-Tr(P_N Y)^2)` (8/8), exactly zero on every aligned
pure-director M5.17 amplitude. Its cscale-normalized coarse solve remains
nonstationary (`1.95e-3` relative gradient versus the frozen `5e-4` gate).
Attempt 0014 is active; no frequency, pair, registry, or release claim is
accepted.
