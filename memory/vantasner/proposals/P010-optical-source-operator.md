---
description: Derive the exact conditional optical source-operator identity and adjudicate T1B
author: vantasner
created: '2026-08-01T12:20:35Z'
updated: '2026-08-01T12:25:15Z'
tags:
- substrate-framework
- campaign-proposal
- optical-geometry
- migration-T1B
category: proposals
confidence: exploratory
status: archived
---
# P010 Conditional Optical Source Operator

## Question and Positive Deliverable
P010 derives a positive exact object: the source-side scalar obtained by applying
the full curved 1+1 optical operator to the dilaton after the conditional TF map.
The proposed `C-OG-003` states the exact cancellation
`-Box_g(log(n(Phi))) = 2*Phi_xx`, not merely its weak-field limit. It also states
the resulting equivalence between a separately declared equation
`-Box_g(phi)=kappa*rho` and `Phi_xx=(kappa/2)*rho` without asserting that either
matter equation or a value of `kappa` follows from the accepted geometry.

## Base Release and Provenance
The accepted base is `v0.9.0` at framework commit `e52dec9`. `C-OG-001` supplies
the exact 1+1 metric, dilaton, wave operator, and curvature identity. `C-OG-002`
supplies the imported TF relation `n=1/(1+2*Phi/c0^2)` and its exact drift map.

The hash-pinned predecessor unit is T1B at
`merged-framework/bridges/phase-1/bridge_T1B_phi_ln_n_potential.py`, SHA-256
`d23749be7385706cad0e7b3441298c30d085d4ce3992fa558cd0283d847d7947`.
It is partially migrated through `C-OG-001/002`; its remaining scope is the
matter-sourced equation, Poisson normalization, and 3+1 ceiling.

## Invariants, Conventions, and Allowed Imports
The metric is the accepted static 1+1 `diag(-1/n,n/c0^2)` metric, with positive
`n` and `c0`. The TF map remains conditional. The sign convention is the
accepted `Box_g f = c0^2*d_x[(d_x f)/n]`. No matter action, stress-energy trace,
Newton constant, or 3+1 field equation may enter unless separately derived.

## Candidate Preregistration

The following alternatives and decisive tests were frozen before implementation.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Simplify the full curved operator after the exact TF substitution | C-OG-001/002 | none | Native exact consequence | Symbolic cancellation and wrong-map mutations |
| B | Treat T1B's prose source law and `kappa=8*pi*G_eff` as derived | unstated dilaton EOM and coupling premise | `kappa`, `G_eff` | Fails dependency closure | Locate an action variation and normalization derivation in the unit |
| C | Retain only a flat weak-field Taylor reduction | C-OG-002 plus flat limit | bookkeeping scale | Compatible but strictly weaker | Compare with the unexpanded curved operator |

## Selection Criteria and Blinding
The frozen order is accepted dependency closure, exactness before approximation,
separation of kinematics from dynamics, assumption economy, then independent
tensor reconstruction. Candidate A is preferred if its exact cancellation
holds. Candidate B is admissible only if the source derives the matter EOM and
coupling; prose assertion and symbolic renaming do not qualify. No empirical
comparator exists.

## Proposed Claim Delta

The campaign proposes one conditional geometry claim with explicit consumers.

| Claim | Exact statement | Dependencies | Oracle | Consumers |
| --- | --- | --- | --- | --- |
| C-OG-003 | Under the conditional TF map, the source-side optical dilaton operator is exactly `2*Phi_xx`; a separately assumed source equation is therefore equivalent to a 1D Poisson-form equation | C-OG-001, C-OG-002 | exact SymPy substitution, independent determinant-form derivation, mutations | optical source models and T1B adjudication |

## Implementation and Oracle Plan
The canonical optical module will expose a pure source-operator function rather
than a matter field equation. The main exact verifier will derive the identity
through package APIs, verify dimensions/sign/c0 cancellation, distinguish the
exact statement from the weak-field expansion, and reject coefficient, sign,
exponent, and metric-volume mutations. An independent review will reconstruct
the scalar operator from `sqrt(|g|) d_mu(sqrt(|g|) g^munu d_nu phi)` without
importing the proposed API. Tests will cover a symbolic profile and domain guards.

The source review will audit each T1B check. It will classify the accepted
geometry and drift against `C-OG-001/002`, the exact operator pullback against
`C-OG-003`, the matter equation and `kappa=8*pi*G_eff` as undeclared premises,
and the 3+1 residual as a negative scope guard.

## Attempts and Continuation
Attempt `0001` implements Candidate A and the independent determinant-form
review. If the exact cancellation fails, the next route is Candidate C with an
explicit order-controlled limit. Candidate B cannot repair an algebraic failure
without a separately sourced action and normalization.

## Debt Ledger

Each interpretive debt must be discharged without weakening the positive claim.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| T1B calls a matter equation derived without varying or declaring one | Source audit isolates it from the exact operator identity | discharged |
| T1B introduces `kappa=8*pi*G_eff` by assignment | Registry excludes an unproved physical normalization | discharged |
| A nonzero 3+1 residual could be mistaken for a gravity construction | Final disposition records it only as a scope guard | discharged |

## Review and Promotion Plan
One claim review and one source adjudication will audit `C-OG-003` and every T1B
check family. Promotion will freeze P010, add the API/test and claim, pin a new
release, change T1B from partial to evidence-backed qualified, regenerate all
canonical consumers, replay optical dependents, and run full validation once at
the unchanged boundary.

## Results and Promotion
Attempt `0001` passed 11 exact checks. A determinant-form reconstruction that
does not import the proposed API passed five independent checks. Candidate A
establishes `-Box_g(log(n(Phi)))=2*Phi_xx` exactly; Candidate C is its weaker
limit, and Candidate B is rejected because T1B contains neither a matter-action
variation nor a coupling derivation. `C-OG-003` is accepted in `v0.10.0`, and
T1B is terminally qualified with a check-family source audit.

## Done Gate
P010 is complete. The exact positive operator identity has independent and
mutation-sensitive evidence, T1B has a terminal evidence-backed disposition,
affected consumers replay, generated state agrees, and debt is empty.
