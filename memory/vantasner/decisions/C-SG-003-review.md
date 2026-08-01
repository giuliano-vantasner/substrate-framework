---
description: Independent review of C-SG-003
author: vantasner-review
created: '2026-08-01T11:01:23Z'
updated: '2026-08-01T11:01:23Z'
tags:
- substrate-framework
- claim-review
- sine-gordon
- action-angle
category: decisions
confidence: working
status: archived
---
# Review of C-SG-003

## Claim Under Review
For every real `omega` with `0 < omega < 1`, the normalized canonical action of the accepted sine-Gordon breather is `J(omega)=16 arccos(omega)`. It obeys `dE/dJ=omega`, has range `0<J<8*pi`, and has the inverse parameterization `omega=cos(J/16)` and `E=16 sin(J/16)`. The relationship is additive; it does not challenge or supersede an accepted claim. Quantization, the DHN spectrum, coupling identification, and an empirical action quantum are outside its scope.

## Sourced Inputs
The review read base release `v0.1.0`, accepted claims `C-SG-001/002`, their canonical implementation and evidence, P002's frozen candidate table and criteria, exact attempt `0001`, and the predecessor HE4 file at the pinned `substrate@6d1f4e0` boundary. The sole theorem import beyond accepted claims is the declared Hamiltonian action-angle identity `dJ/dE=T/(2*pi)` for the periodic orbit under the campaign's `J=(1/(2*pi))*closed_integral(p dq)` convention.

## Independence
The exact proposal route integrates the derivative built from accepted `E(omega)` and `T(omega)`. The independent review does not import `breather_action`, `breather_frequency_from_action`, or `breather_energy_from_action`; it reconstructs the breather field, differentiates its canonical momentum, verifies the spatial antiderivative, and evaluates the full phase-space line integral at 30 and 50 decimal places. Thus the exact formula and the field normalization do not share their load-bearing construction.

## Verification Status
The exact SymPy verifier derives `dJ/domega`, fixes the integration constant at the vanishing-amplitude endpoint, proves both action-angle derivatives and the inverse maps, and earns `symbolic_verified`. The high-precision field integral is corroborating numeric evidence, not the basis for upgrading numerical agreement to an exact verdict.

## Sensitivity and Counterexamples
The defining predicate accepts `16*acos(omega)` and rejects coefficient 15, additive offset 1, and the `asin` branch. The direct field route rejects a factor-two error in `1/(2*pi)` at four frequencies. It also verifies the analytic spatial antiderivative and remains stable when working precision increases from 30 to 50 decimal places. Endpoint and monotonicity checks cover `J(1-)=0`, `J(0+)=8*pi`, and the exact negative derivative on the open domain.

## Framework Compatibility
The claim is native to the normalized sine-Gordon sector and introduces no fitted constant or new physical parameter. Its units are dimensionless under the accepted `c=m=beta=1` convention. The endpoint and branch agree with the accepted vanishing-energy and kink-pair limits. No unrelated framework invariant is altered.

## Dependency and Consumer Replay
Direct consumers are the new pure APIs in `src/substrate_framework/sine_gordon.py` and `tests/test_sine_gordon.py`. P001's claims remain unchanged; its verifier and independent rederivation are replayed at promotion. Identified future consumers include the gradient/Legendre functional and separately governed semiclassical proposals. P002 creates no unresolved debt.

## Competing Candidate Audit
Candidates A, B, and C and their criteria were registered before implementation; no empirical comparator exists. A is selected for exact dependency closure and its uniquely fixed endpoint. B is used as the independent physical normalization route. C is deferred because accepting it first would reverse the intended dependency order, not because its numerical value was less close.

## Four-Axis Decision
The claim is accepted as a native active result; its exact verdict rests on the symbolic route, while the field quadrature remains independent corroboration.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: native
- Epistemic: active
- Relationship: additive, with no challenge or supersession

## Promotion Transaction
Promotion freezes P002 in `campaigns/`, adds importable action APIs and tests, adds only `C-SG-003` to the registry, creates release `v0.2.0`, regenerates docs and accepted memory, and replays both accepted campaigns before the single full repository boundary check.

## Continuation if Not Accepted
If downstream replay contradicts this decision before the release transaction closes, acceptance is withdrawn and Candidate B becomes the next primary construction; numeric agreement alone would not retain an exact verdict.

## Done Gate
The claim-level gate is satisfied subject to the recorded promotion replay: the positive object exists, dependencies and theorem import are explicit, two independent routes support the normalization, mutations fail, consumers are importable, and the campaign debt ledger is empty.

## Cross-References
See `campaigns/P002-sine-gordon-action`, `governance/claims.yaml`, `governance/releases/v0.2.0.yaml`, `campaigns/P001-sine-gordon-root`, and the parent `memory/vantasner/efforts/framework-migration.md`.
