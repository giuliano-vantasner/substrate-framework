---
description: Derive and promote the exact normalized sine-Gordon breather and its Hamiltonian energy
author: vantasner
created: '2026-08-01T10:35:44Z'
updated: '2026-08-01T10:49:03Z'
tags:
- substrate-framework
- campaign-proposal
- sine-gordon
category: proposals
confidence: exploratory
status: archived
---
# P001 Exact Sine-Gordon Root

## Question and Positive Deliverable
This campaign constructs an exact localized time-periodic solution of the normalized sine-Gordon equation for every `0 < omega < 1` and derives its conserved Hamiltonian energy as an importable framework result.

The positive deliverable is two individually reviewable claims: `C-SG-001`, the exact on-shell breather field, and `C-SG-002`, its exact conserved energy and physical endpoint limits. A failed ansatz or a consistency-only cross-check does not complete the campaign.

## Base Release and Provenance
The accepted base release is null at framework commit `6220237`. The immutable predecessor evidence baseline is `substrate@6d1f4e0`; dirty predecessor Phase 47/48 files are excluded.

Source evidence read directly includes `pulson-backreaction-bridge/sympy/rungs/rung147_c024_breather_energy_amplitude.py`, `merged-framework/bridges/phase-1/bridge_T1E_E0_triple_oracle.py`, `sg-breather-ionization/formalization/Energy.lean`, and the root statements in `merged-framework/north-star.md`. These artifacts are evidence candidates only. In particular, `Energy.lean` defines the energy formula and proves consequences of that definition; it does not derive the coefficient from the Hamiltonian.

## Invariants, Conventions, and Allowed Imports
The model is the real normalized `1+1` dimensional sine-Gordon equation
`phi_tt - phi_xx + sin(phi) = 0` with Hamiltonian density
`phi_t^2/2 + phi_x^2/2 + 1 - cos(phi)`. Coordinates and the field are dimensionless under `c = m = beta = 1`. The parameter domain is `0 < omega < 1`, with positive inverse width `eta = sqrt(1 - omega^2)`.

Permitted imports are exact real algebra/calculus identities, SymPy as the exact oracle, SciPy quadrature as an independent non-authoritative cross-check, and the pinned source files as provenance. No empirical number or fitted threshold is permitted.

## Candidate Preregistration
The candidates are alternative constructions of the same requested positive object.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Direct `4 atan` breather ansatz, exact PDE substitution, and Hamiltonian integration | Normalized sine-Gordon model and real calculus | `omega` only | Native, exact, branch-transparent, and directly importable | Full symbolic PDE residual and energy integral vanish exactly; normalization mutations fail |
| B | Baecklund or complex kink-pair construction | Same model plus transform conventions and complex branch control | `omega` plus eliminable transform auxiliaries | Exact but more representation-heavy | Recovered real field agrees with the PDE and has no residual branch debt |
| C | Time-periodic numerical BVP | Same model plus finite domain, mesh, phase condition, and solver tolerances | `omega` plus numerical controls | Compatible but earns only numerical evidence | Domain/mesh/tolerance refinement converges to a localized periodic orbit and its energy |

## Selection Criteria and Blinding
The frozen order is exact equation fit, assumption/parameter economy, branch clarity, strongest verdict, correct localization and endpoint limits, independent reproducibility, then API simplicity. There is no empirical comparator in this claim, so the comparator gate is explicitly not applicable.

Candidate A is selected structurally before implementation because it exposes the governing equation and Hamiltonian directly, has one physical parameter, and admits exact verification. Candidate B remains the alternate exact construction if A develops branch or simplification debt. Candidate C remains a numerical fallback and independent soluble-limit pattern, not a route for upgrading a numerical result to exact status.

## Proposed Claim Delta
The proposal adds two root claims and no supersession relationship.

| Claim | Exact statement | Dependencies | Evidence plan | Anticipated consumers |
| --- | --- | --- | --- | --- |
| C-SG-001 | For `0 < omega < 1`, the direct arctangent field with `eta = sqrt(1-omega^2)` is an exact localized, time-periodic solution of the normalized sine-Gordon equation | Declared normalized sine-Gordon model; exact calculus | Exact SymPy residual, localization/period checks, coefficient/width/sign mutations | C-SG-002 and every later breather-sector claim |
| C-SG-002 | The `C-SG-001` solution has conserved Hamiltonian energy `16 sqrt(1-omega^2)`, tending to `16` as `omega -> 0+` and `0` as `omega -> 1-` | C-SG-001; Hamiltonian definition | Exact clean-slice derivation, independent full-density numerical quadrature at nonzero phases, normalization mutations, endpoint limits | action variable, mass/inertia, bridge, radiation, and scale claims |

## Implementation and Oracle Plan
Canonical expressions and pure transformations will live in `src/substrate_framework/sine_gordon.py`; imports will execute no algebra, simulation, or printing. Unit tests will cover domains, formulas, and numerical evaluation. The campaign verifier will import those APIs and use `CheckLedger`.

SymPy is the strongest practical oracle for the PDE residual, exact energy reduction, and limits. SciPy quadrature at multiple frequencies and phases supplies an independently evaluated cross-check of the full Hamiltonian density. Load-bearing mutations change the field coefficient, width relation, equation sign, and energy normalization; a relevant verdict must fail for each.

## Attempts and Continuation
The frozen attempt history is under `campaigns/P001-sine-gordon-root/attempts/`.

Attempt `0001` implemented Candidate A and exited cleanly with `P001 ALL 25 CHECKS PASS`. Exact residual, localization, periodicity, independent energy derivation, mutations, endpoint limits, nonzero-phase quadrature, and domain refinement all passed. Candidate B was not activated because Candidate A accumulated no scientific or representation debt.

## Debt Ledger
The campaign starts with three concrete debts.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| Exact PDE residual may depend on hidden branch assumptions | Residual is identically zero on the declared real domain, with branch assumptions explicit | discharged |
| Energy derivation could share copied literals with the expected formula | Derive density from the field and integrate before comparing to the canonical expression; cross-check full density numerically at nonzero phases | discharged |
| Legacy consumers are numerous and inconsistently documented | Record direct source consumers and successor API consumers; replay all successor consumers before promotion | discharged for P001; 40 nonaccepted source consumers remain in the parent migration backlog |

## Review and Promotion Plan
Each claim received its own raw-artifact review record based on exact statements rather than campaign prose. Both were accepted as `symbolic_verified`, `native`, and `active`; the independent route used the quarter-period gradient-plus-potential slice rather than the proposal verifier's zero-field kinetic slice.

The claims were promoted in dependency order to `v0.1.0`. The package API/tests, frozen campaign, registry, pinned/current release manifests, generated documentation, and generated accepted memory now materialize the same two-claim set.

## Done Gate
P001 is closed: both positive claims passed exact verification, sensitivity audit, claim-level review, successor replay, canonical extraction, release materialization, and memory synchronization with an empty campaign debt ledger. This does not close the parent corpus migration.
