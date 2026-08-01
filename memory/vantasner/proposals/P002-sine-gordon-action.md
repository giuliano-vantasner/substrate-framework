---
description: Derive and promote the exact action variable of the accepted sine-Gordon breather
author: vantasner
created: '2026-08-01T10:56:05Z'
updated: '2026-08-01T11:04:10Z'
tags:
- substrate-framework
- campaign-proposal
- sine-gordon
- action-angle
category: proposals
confidence: exploratory
status: archived
---
# P002 Sine-Gordon Action Variable

## Question and Positive Deliverable
This campaign derives the canonical action variable of the accepted normalized sine-Gordon breather and the exact inverse energy-action parameterization.

The positive object is `C-SG-003`: for `0 < omega < 1`, the action normalized by `J=(1/(2*pi))*closed_integral(p dq)` is `J(omega)=16 arccos(omega)`, satisfies `dE/dJ=omega`, maps the family onto `0 < J < 8*pi`, and gives `omega=cos(J/16)` and `E=16 sin(J/16)`. No quantization rule, measured Planck constant, DHN spectrum, or coupling identification is in scope.

## Base Release and Provenance
The accepted base is `v0.1.0` at framework commit `1bb6c4a`, providing `C-SG-001` and `C-SG-002`. The predecessor evidence boundary remains `substrate@6d1f4e0`; dirty later work is excluded.

Source evidence read directly includes `merged-framework/bridges/phase-45/bridge_HE4_dhn_action_variable.py` and `pulson-backreaction-bridge/sympy/imported/soliton-shadow/i_breather_closed_form.py`. The HE4 literature comparison is not imported into the proposed claim.

## Invariants, Conventions, and Allowed Imports
The accepted breather period is `T=2*pi/omega`, its energy is `E=16 sqrt(1-omega^2)`, and `0<omega<1`. The action convention is `J=(1/(2*pi))*closed_integral(p dq)`, so the standard one-degree-of-freedom/periodic-field action-angle identity is `dJ/dE=T/(2*pi)=1/omega`.

Permitted inputs are accepted claims `C-SG-001/002`, that explicitly named Hamiltonian theorem, exact calculus, SymPy, and high-precision field quadrature as corroboration. The integration constant is fixed structurally by `J -> 0` at the vanishing-amplitude endpoint `omega -> 1-`; it is not fitted.

## Candidate Preregistration
Three derivation routes are registered before implementation.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Integrate `dJ/dE=T/(2*pi)` using accepted `E(omega),T(omega)` and `J(1)=0` | Accepted claims plus standard action-angle identity | none beyond `omega` | Exact, dependency-minimal, and branch-controlled | Differential identity, endpoint, inverse map, and normalization mutations |
| B | Directly evaluate `(1/(2*pi))*int_0^T dt int dx phi_t^2` | Accepted field plus phase-space definition and quadrature controls | numerical precision/domain controls | Most direct physical construction but numerical unless the remaining time integral closes exactly | Precision/refinement agreement with an independently frozen exact expression |
| C | Derive an on-shell Legendre functional independently and use `J=-dI/domega` | Accepted field plus a separately verified functional identity | none beyond `omega` | Exact if the functional is independently established, but reverses the desired dependency order | Functional derivation must not assume J or copy its formula |

## Selection Criteria and Blinding
The frozen order is accepted dependency closure, exact satisfaction of the defining identity, absence of fitted scales, minimal auxiliary assumptions/branches, correct endpoints and inversion, independent field-level support, then API simplicity. There is no empirical comparator.

Candidate A is selected because it is exact and depends only on accepted claims plus the named action-angle theorem. Candidate B is retained as the independent field-level review route. Candidate C is deferred because its prerequisite functional is not yet accepted and using it now would reverse the dependency graph.

## Proposed Claim Delta
The proposal adds one claim and no challenge or supersession relationship.

| Claim | Exact statement | Dependencies | Oracle | Consumers |
| --- | --- | --- | --- | --- |
| C-SG-003 | `J(omega)=16 arccos(omega)` is the normalized action variable, `dE/dJ=omega`, `0<J<8*pi`, with inverse `omega=cos(J/16)`, `E=16 sin(J/16)` | C-SG-001, C-SG-002, declared action-angle theorem | exact SymPy calculus plus independent high-precision phase-space integral | gradient/Legendre action, semiclassical proposals, effective-action and quantization claims |

## Implementation and Oracle Plan
Pure APIs will extend `src/substrate_framework/sine_gordon.py`: action as a function of frequency, frequency and energy as functions of action, and numeric domain checks. No quantization constant or literature spectrum enters the package.

The proposal verifier will derive `dJ/domega=(dE/domega)/omega`, integrate it with the endpoint condition, verify both action-angle derivatives and inverse maps, test endpoints/monotonicity, and reject coefficient, offset, and inverse-function mutations. The independent review will reconstruct the phase-space integral from the accepted field without importing the new action helpers and will report precision/refinement behavior.

## Attempts and Continuation
Attempt `0001` implements Candidate A. A technical integration failure triggers an equivalent exact ODE representation before any concept rejection. Failure of the action-angle construction activates Candidate B as the primary route; a numerical match alone cannot earn exact status. Candidate C activates only after its own functional dependency is independently accepted.

## Debt Ledger
The campaign begins with explicit, dischargeable debts.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| The additive integration constant could be arbitrary | The exact endpoint check fixes it uniquely and the offset mutation fails | discharged |
| The exact action-angle route could weakly encode the phase-space action | The independent 30/50-digit field integral agrees at four frequencies and rejects a factor-two normalization | discharged |
| HE4 bundles literature claims beyond accepted dependencies | C-SG-003, its APIs, and its review exclude quantization and literature-spectrum conclusions | discharged |

## Review and Promotion Plan
One claim-level review will inspect the exact theorem import, raw derivatives, endpoint condition, mutations, direct field quadrature, API domains, and consumer map. Acceptance requires `symbolic_verified`, `native`, and `active` decisions with no unresolved P002 debt.

Promotion will freeze P002 under `campaigns/`, extend the registry and pinned release without rewriting P001, regenerate docs and accepted memory, replay all accepted sine-Gordon tests and both campaign verifiers, and run one full workflow validation at the unchanged boundary.

## Results and Promotion
Attempt `0001` passed 19 exact checks. The independent phase-space route passed 19 checks, including its analytic spatial antiderivative, 30-to-50 digit refinement, four frequencies, and a factor-two normalization mutation. The full accepted sine-Gordon consumer replay then passed for P001, P002, their independent reviews, and the package tests.

`C-SG-003` was individually accepted as `symbolic_verified`, `native`, and `active` in release `v0.2.0`. The immutable record is `campaigns/P002-sine-gordon-action`; canonical registry, release, generated docs, and accepted memory were synchronized. No semiclassical or literature-spectrum statement was promoted.

## Done Gate
P002 is complete. The positive action variable is importable and exact, its phase-space normalization has an independent field construction, mutations are sensitive, all affected accepted consumers replay, and the campaign debt ledger is empty.
