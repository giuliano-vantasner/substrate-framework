---
description: Audit nonlinear sine-Gordon PDE boundary robustness in NC4
author: vantasner
created: '2026-08-02T01:35:00Z'
updated: '2026-08-02T02:30:00Z'
tags:
- substrate-framework
- campaign-proposal
- sine-gordon
- migration-NC4
category: proposals
confidence: exploratory
status: archived
---
# P051 NC4 PDE Robustness Audit

## Question and Positive Deliverable

P051 must produce a reusable, importable 1+1 normalized sine-Gordon evolution
and diagnostic surface and determine the strongest finite-time,
equation-and-data-specific boundary-correlation or topological statement that
survives an honest audit of NC4. The result must distinguish exact parity
covariance, numerical preservation of a declared IBVP, boundary sign
correlation, boundary winding, and actual topological charge. Reproducing a
source tally, documenting a removed API, or finding that NC4 overclaims would
not alone complete the campaign.

## Base Release and Provenance

The accepted base is `v0.45.0` at framework commit `033e9c7`; its scientific
transaction is `da71477`. The accepted authority includes `C-SG-001`,
`C-SG-002`, and `C-SG-011` through `C-SG-013`. NC4 is a pending primary source
unit at `substrate@6d1f4e0`, path
`merged-framework/bridges/phase-15/bridge_NC4_pde_robustness.py`, SHA-256
`9efa788da093213f354cbd9e26b7bd0be81129d6f966128b5c0fd10fe0081570`.
Its G1/G2/G3 and NC1/NC3 links are evidence or pending dependencies, not
additional promotion units or accepted imports. Memory search found only the
P050 handoff and accepted numerical-method precedents, with no accepted NC4
result. The full NC4 executable remains unopened until this contract is
frozen.

## Invariants, Conventions, and Allowed Imports

The normalized PDE is `phi_tt-phi_xx+sin(phi)=0` with dimensionless field and
coordinates. The declared domain, initial data, boundary data, discretization,
and diagnostic window are part of any numerical claim rather than suppressed
implementation detail. `C-SG-011` fixes orientation
`epsilon^(01)=+1`, charge from spatial endpoint values, and the conditions for
charge conservation. `C-SG-013` fixes the coordinate-boundary correlation and
proves that it neither implies nor is implied by boundary winding. Scalar
parity maps the full field, coordinate point, domain, and boundary data;
comparing two simulations is a parity test only if all of those objects are
mapped. Pending G1, G2, G3, W1, and W3 content, weak dynamics, particle labels,
and a phase-to-chirality dictionary are excluded. Sampled integrals must call
`substrate_framework.numerics.trapezoid_integral`; a removed `np.trapz` is
source-reproduction evidence, never a canonical dependency.

## Candidate Preregistration

The alternatives are frozen from queue metadata and accepted invariants before
the full NC4 executable is read.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal NC4 finite-difference experiment, repaired only for version-independent quadrature | Source-declared PDE, domain, data, boundary rule, diagnostic, and finite-time window | Every source mesh, timestep, domain, amplitude, phase, and threshold remains explicit | Compatible only as qualified setup-specific simulation evidence | Reproduction, solver completion, mesh/timestep/domain refinement, energy balance, parity-paired data, mutation sensitivity, and independent method |
| B | Exact nonlinear rest breather and parity image evolved on a declared large finite domain | Accepted exact solution, causally quiet window, consistent sampled derivatives | Frequency, domain, mesh, timestep, observation point, number of periods | Native soluble reference; large amplitude alone should not create winding or full-period correlation | PDE residual, convergence to exact samples, energy and boundary-charge stability, exact zero-correlation limit, parity covariance |
| C | Separate driven half-line or mirrored full-line IBVP with an explicit boundary action or forcing law | New well-posed boundary dynamics and declared energy flux | Drive shape, amplitude, phase, side, duration, absorbing treatment | Compatible extension only if A lacks sufficient boundary data; higher assumption cost | Boundary compatibility, flux accounting, refinement, parity-mapped forcing, and independence of correlation from winding |

## Selection Criteria and Blinding

Selection is ordered by well-posed equation/domain/data, compatibility with
accepted parity and topological conventions, convergent spatial and temporal
errors, controlled energy flux or conservation, stable endpoint charge,
independent-method or exact-solution agreement, parameter economy, and reusable
API scope. There is no empirical comparator. NC4's source numbers, thresholds,
and conclusions remain unopened until this contract and manifest exist; source
agreement cannot select a candidate.

## Proposed Claim Delta

Provisional `C-SG-014` may record a narrowly specified finite-time simulation
result only if the actual NC4 setup and at least one independent or soluble
route pass. It will depend on the smallest applicable subset of `C-SG-001`,
`C-SG-002`, `C-SG-011`, `C-SG-012`, and `C-SG-013`. It will not promote an
exact theorem from numerics, infer topological discrimination from sign
correlation, infer parity-violating dynamics from a parity-odd observable,
import pending weak-sector content, or use a source target value as an input.
Likely consumers are the NC4 disposition and later W1/W3 audits; pending
consumers cannot become dependencies.

## Implementation and Oracle Plan

A pure module will own the 1D spatial operator, explicit initial and boundary
data, energy and endpoint-charge diagnostics, boundary-trace sampling, and a
finite-time evolution result. Shared `solve_method_of_lines`,
`SolverTolerances`, `trapezoid_integral`, and verification primitives will be
reused where appropriate. Candidate A's literal scheme will be reproduced
append-only before repair. Candidate B supplies an exact large-amplitude
nonlinear solution and parity map; Candidate C is opened only if boundary
dynamics are genuinely missing rather than to rescue a desired sign.

For a PDE claim the record will state IEEE float64, equation, finite domain,
initial and boundary data, spatial stencil, time algorithm, timestep or
adaptive tolerances, stopping status, sampling, diagnostic window, and error
norm. Spatial, temporal, domain, and adaptive-tolerance effects will be varied
independently. Closed or causally quiet cases will test energy conservation;
driven or absorbing cases must account for boundary or damping flux rather
than call nonconservation a solver error. Exact breather samples or a linear
mode will supply a soluble reference, and a materially different DOP853
method-of-lines or conservative explicit scheme will supply the method
cross-check. Mutations will change the nonlinear term, spatial sign, parity
map, boundary side or normal, phase convention, quadrature normalization,
endpoint charge orientation, and load-bearing drive or initial data. Numeric
results can earn only `simulation_evidence`; exact covariance and residual
parts are reviewed separately with symbolic algebra.

## Attempts and Continuation

Attempt 0001 hash-pinned the source and preserved its literal NumPy 2 failure
at the removed `np.trapz` call before any scientific tally. Attempt 0002 used
an in-memory compatibility alias only and reproduced `ALL 30 CHECKS PASS`,
which established source reproducibility but not the headline. Attempt 0003
exposed an over-tight convergence oracle for discontinuous sampled sign data;
the verifier was repaired by checking its actual first-order refinement.
Attempt 0004 then passed all 36 primary checks. Attempt 0005 found that the
independent spectral breather domain was too short for its threshold; the
domain was enlarged without changing the oracle, and attempt 0006 passed all
nine independently implemented checks.

The source sweep changes frequency, phase, force amplitude, width, and duration.
A common phase changes corrected `dQ` from about `-1.033` at `w=0.6` to about
`+1.947` at `w=0.8`, while adding pi exactly swaps the epsilon-labelled drives.
The tuned `w=0.6` response is reproducible, but the amplitude-robust physical
headline is not. Candidate B validates the solver; Candidate C was not opened
because a new boundary action would broaden rather than repair NC4.

## Debt Ledger

This ledger tracks the source setup, PDE well-posedness, quadrature version,
boundary semantics, conservation or flux balance, topological accounting,
convergence, independent validation, interpretation, and consumers.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| NC4's literal setup and current-environment behavior are unaudited | Hash-check, run, and preserve the full source result or failure | discharged by attempts 0001 and 0002 |
| No canonical 1D finite-time sine-Gordon simulation surface is established | Implement the minimal pure solver and diagnostic API with focused tests | discharged by `sine_gordon_1d.py` and eight tests |
| Source quadrature uses a version-specific NumPy name | Reproduce the failure and use only the shared compatibility helper canonically | discharged; literal failure preserved and canonical integration uses `trapezoid_integral` |
| Boundary correlation may be conflated with winding or charge discrimination | Compute both independently and include implication counterexamples | discharged by endpoint, correlation, vacuum, and common-phase checks |
| Parity may map only a sign while leaving data or domain unmapped | Transform field, coordinate, domain, boundary data, and normal explicitly | discharged by exact phase-label mutation and C-SG-013 semantics |
| Numerical robustness is not established | Pass mesh, timestep, domain, tolerance, invariant/flux, mutation, and independent-route gates | discharged by 36 primary and nine independent checks |
| Consumers and generated state are not replayed | Complete impact analysis, targeted consumers, one full promotion gate, and canonical regeneration | discharged; focused replay passed and repository gate passed 365 tests |

## Review and Promotion Plan

Each exact and numerical claim receives a separate four-axis review from raw
attempt, refinement, mutation, and independent-route artifacts. Accepted
reusable logic moves under `src/substrate_framework/` with tests. NC4 receives
a structured terminal disposition in `migration/dispositions.yaml`; mixed
content is `qualified`, with every unaccepted physical inference named and
durable evidence linked. Promotion requires a pinned release, registry closure,
generated docs and accepted memory, affected-consumer replay, one final
`scripts/validate.sh`, and separate `git diff --check`.

## Done Gate

P051 is closed. The reusable solver/diagnostic surface, corrected tuned-subcase
result, exact mutations, convergence series, energy-flux checks, independent
Fourier/direct-`solve_ivp` route, claim-level rejection, targeted consumers,
and qualified NC4 disposition all pass. The regenerated queue contains 218
units with 169 pending and 42 qualified. `scripts/validate.sh` passed the
workflow, all 226 memory files, skill validation, and 365 tests; `git diff
--check` passes. No registry or release change was warranted, so `v0.45.0`
remains current. The campaign debt ledger is empty and migration continues at
QB1.
