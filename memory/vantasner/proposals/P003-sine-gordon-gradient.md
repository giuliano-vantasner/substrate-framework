---
description: Derive and promote the exact averaged spatial-gradient integral of the sine-Gordon breather
author: vantasner
created: '2026-08-01T11:07:07Z'
updated: '2026-08-01T11:15:03Z'
tags:
- substrate-framework
- campaign-proposal
- sine-gordon
- virial
- legendre-transform
category: proposals
confidence: exploratory
status: archived
---
# P003 Sine-Gordon Averaged Gradient Integral

## Question and Positive Deliverable
This campaign derives the exact period average `Gbar(omega)=(1/T)*int_0^T dt int_R dx phi_x^2` of the accepted normalized sine-Gordon breather. The factor convention is load-bearing: `Gbar` is the squared-gradient integral itself, so the Hamiltonian's mean spatial-gradient energy contribution is `Gbar/2`.

The proposed positive claim `C-SG-004` is `Gbar=16[sqrt(1-omega^2)-omega*arccos(omega)]=E-omega*J` on `0<omega<1`, with `dGbar/domega=-J`, `Gbar(0+)=16`, and `Gbar(1-)=0`. It is a classical internal functional statement. No quantization rule, effective coupling, slow-manifold dynamics, or empirical comparator is in scope.

## Base Release and Provenance
The accepted base is `v0.2.0` at framework commit `8f3335f`, providing `C-SG-001/002/003`. The predecessor boundary remains the immutable `substrate@6d1f4e0` snapshot.

The source artifact read directly is `pulson-backreaction-bridge/sympy/imported/soliton-shadow/i_breather_closed_form.py`. Its proposed formula and numerical machinery are candidate evidence only. In particular, its finite coefficient checks are not imported as a general convergence proof.

## Invariants, Conventions, and Allowed Imports
The campaign preserves the accepted localized periodic field, Hamiltonian density, energy, period, canonical action convention, action-angle derivative, normalized units, and open frequency domain. It may use exact differentiation and integration by parts on the accepted field and high-precision quadrature only for an independent corroborating route.

For a localized periodic solution, multiplying the exact field equation by `x*phi_x`, averaging over one period, and integrating by parts gives `Vbar=(Kbar+Gbar)/2`, where `Kbar=<int phi_t^2 dx>` and `Vbar=<int (1-cos(phi)) dx>`. Therefore the accepted Hamiltonian gives `E=Kbar+Gbar`; the canonical action definition gives `Kbar=omega*J`. All boundary and period terms must be checked rather than silently dropped.

## Candidate Preregistration
Three routes are registered before implementation and there is no empirical comparator.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Derive the spacetime virial identity from the accepted equation, then use the accepted phase-space action normalization | Accepted claims and exact localized/periodic integration by parts | none | Directly identifies the physical field integral and fixes every factor | Boundary terms, virial algebra, closed form, derivatives, limits, and mutations all pass |
| B | Derive the fixed-time spatial integral exactly and close its time average | Accepted field plus a justified exact averaging identity | none | Direct but analytically branch-sensitive for `sqrt(1-omega^2)/omega > 1` | General averaging identity, not merely finite series coefficients, must be established |
| C | Construct `E-omega*J` as a Legendre combination | Accepted energy and action | none | Exact and dependency-minimal but does not alone prove it equals the field gradient integral | Independent field integral must identify the Legendre combination |

## Selection Criteria and Blinding
The frozen order is direct identification of the claimed field quantity, accepted dependency closure, exact boundary and factor control, assumption economy, correct limits, mutation sensitivity, then API simplicity. Candidate A is selected because it proves the physical identification exactly using the accepted equation. Candidate C supplies an algebraically independent closed-form route once A identifies the quantity. Candidate B is reserved for the field-level review and must not use finite Taylor checks as if they were a global proof.

## Proposed Claim Delta
The proposal adds one claim and no challenge or supersession relationship.

| Claim | Exact statement | Dependencies | Oracle | Consumers |
| --- | --- | --- | --- | --- |
| C-SG-004 | `Gbar=16[sqrt(1-omega^2)-omega arccos(omega)]=E-omega J`, with `dGbar/domega=-J` and exact endpoint limits | C-SG-001, C-SG-002, C-SG-003 | exact SymPy calculus and integration-by-parts audit, plus independent high-precision direct field quadrature | slow-manifold and effective-action proposals, virial diagnostics, gradient-energy consumers |

## Implementation and Oracle Plan
A pure `breather_mean_gradient_integral(omega)` API will be added to `src/substrate_framework/sine_gordon.py`. It returns the squared-gradient integral, not its half-energy contribution, and reuses accepted energy/action APIs instead of duplicating constants in consumers.

The exact verifier will audit each periodic/localized boundary term, derive the virial algebra, prove equality to the API and Legendre expression, check derivatives, convexity and endpoints, and reject coefficient, offset, sign, and factor-one-half mutations. The independent review will reconstruct `phi_x`, verify the exact fixed-time spatial antiderivative, perform the remaining time average at two precisions at multiple frequencies, and run one direct nested field integral. Numeric agreement remains corroboration; the exact verdict rests on the virial derivation and accepted exact claims.

## Attempts and Continuation
Attempt `0001` implements Candidate A. A failure in symbolic simplification triggers a manually audited integration-by-parts representation before any conceptual rejection. If a non-vanishing boundary term appears, Candidate A is rejected and Candidate B becomes primary. If direct averaging remains only numerical, the claim can retain exact status only if the independently audited virial route succeeds.

## Debt Ledger
The campaign begins with three concrete debts.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| Virial boundary terms could be dropped without justification | The exact verifier checks period cancellation and all six spatial infinity limits | discharged |
| The predecessor calls the quantity an action despite a load-bearing factor convention | C-SG-004, its API, tests, and review define the full squared-gradient integral and distinguish its half-energy contribution | discharged |
| The Legendre formula could be copied without identifying its physical integral | Independent reconstruction, exact spatial antiderivative, refined period quadrature, and a nested field integral agree and reject a half-factor mutation | discharged |

## Review and Promotion Plan
One claim-level review will inspect the raw virial derivation, definitions, mutations, direct field integration, precision refinement, endpoint branches, and consumer map. Acceptance requires `symbolic_verified`, `native`, and `active` decisions with all P003 debts discharged.

Promotion will freeze P003 under `campaigns/`, add only `C-SG-004`, create the next pinned release, regenerate docs and accepted memory, replay every accepted sine-Gordon verifier and package consumer, and run the full repository workflow once at the unchanged promotion boundary.

## Results and Promotion
Attempt `0001` preserved a representation failure in which SymPy could not infer the sign of the accepted inverse width during a limit. Attempt `0002` exposed that width as an explicit positive symbol for localization checks without changing the claim and passed 25 exact checks. The independent direct-field route passed 16 checks, including two-precision period averages, the half-factor mutation, and nested space-time quadrature.

`C-SG-004` was individually accepted as `symbolic_verified`, `native`, and `active` in `v0.3.0`. P003 is frozen under `campaigns/`, generated state is synchronized, every accepted campaign verifier replays, and no slow-manifold or effective-action conclusion was admitted with it.

## Done Gate
P003 is complete. The exact positive field functional is importable, its factor convention and physical identification are independently verified, all downstream paths replay, and the campaign debt ledger is empty.
