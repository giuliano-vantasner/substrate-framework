---
description: Independent claim-level review and acceptance decision for C-SG-001
author: vantasner-review
created: '2026-08-01T10:44:08Z'
updated: '2026-08-01T10:49:03Z'
tags:
- substrate-framework
- claim-review
- sine-gordon
category: decisions
confidence: working
status: archived
---
# C-SG-001 Review

## Claim Under Review
For every real `omega` with `0 < omega < 1`, set `eta = sqrt(1-omega^2)`. The field
`phi(x,t) = 4 atan(eta sin(omega t)/(omega cosh(eta x)))` is real, spatially localized, periodic with period `2*pi/omega`, and satisfies `phi_tt - phi_xx + sin(phi) = 0` identically on real `x,t`.

The relationship is a new dependency-root claim with no supersession. Its positive role is to provide the exact normalized breather consumed by later energy, action, inertia, radiation, and bridge claims.

## Sourced Inputs
The accepted base is the null release at framework commit `6220237`. The normalized sine-Gordon equation is a declared model import, not a derived law of the empty framework.

Raw inputs read were `proposals/P001-sine-gordon-root/proposal.yaml`, `src/substrate_framework/sine_gordon.py`, `tests/test_sine_gordon.py`, `proposals/P001-sine-gordon-root/verify.py`, attempt `0001`, the isolated source inventory for `substrate@6d1f4e0`, and the predecessor rung147/T1E/Lean evidence named in the proposal.

## Independence
The review rebuilt the field and equation without importing `substrate_framework.sine_gordon`. The separate artifact `proposals/P001-sine-gordon-root/reviews/independent_rederivation.py` reconstructs the profile directly, recomputes the full residual, and checks localization and a wrong-width counterexample. Only the shared `CheckLedger` reporting primitive is reused.

## Verification Status
The maximum earned status is `symbolic_verified`. SymPy differentiates the constructed field and reduces the complete unsampled PDE residual to zero. Separate exact checks establish localization and periodicity. The claim is an exact algebraic/calculus obligation, so symbolic verification is stronger and more appropriate than a grid simulation.

The verifier does not infer the headline from a pass tally: it explicitly checks the full residual and the independent review reconstructs it again without the canonical helper.

## Sensitivity and Counterexamples
The proposal verifier rejects three load-bearing mutations at an exact interior point: coefficient `4 -> 3`, inverse-width relation `sqrt(1-omega^2) -> sqrt(1+omega^2)`, and potential sign `+sin(phi) -> -sin(phi)`. The independent review repeats the wrong-width counterexample. All mutations make a relevant on-shell predicate fail.

Endpoint frequencies `omega=0` and `omega=1`, negative frequencies, and complex numeric frequencies are rejected by the canonical API because the claim is quantified only over the open real interval.

## Framework Compatibility
The claim is native to the selected normalized sine-Gordon root. It adds no fitted constant, empirical comparator, hidden scale, or cross-sector convention. Its only parameter is `omega`; `eta` is derived. The API is pure and performs no calculation or printing at import time.

Compatibility is not evidence that the normalized sine-Gordon model describes nature; that model remains an explicitly declared root assumption for this release.

## Dependency and Consumer Replay
The successor direct consumers are `C-SG-002`, `tests/test_sine_gordon.py`, and the P001 verifier/review artifacts. All targeted commands pass. The isolated source census finds 40 predecessor bridge scripts containing `E0`, `E_breather`, or `breather_energy`; they are a future migration backlog, not accepted consumers, and receive no authority from this claim.

No accepted downstream claim exists yet, so the accepted dependency replay is closed at the root.

## Competing Candidate Audit
Candidates A, B, and C and the ordered structural criteria were registered before implementation. No empirical comparator exists. Candidate A wins because it directly exposes the equation, has no auxiliary branch parameters, and earns an exact verdict. Candidate B remains an exact alternate if a later branch audit finds a defect; Candidate C is resolution-bounded and was not used to select or upgrade the claim.

## Four-Axis Decision
The claim passes all four independent decisions.

- Verification: `symbolic_verified`
- Review: `accepted`
- Compatibility: `native`
- Epistemic: `active`
- Relationship: new root claim; no `challenges` or `supersedes`

## Promotion Transaction
The promotion transaction completed in `v0.1.0`: the exact statement and evidence are in the registry, the API/tests are importable, P001 is frozen under `campaigns/`, and generated documentation plus accepted memory materialize the pinned claim set. Targeted and independent replay passed after the move.

## Continuation if Not Accepted
This decision is acceptance subject to completing the atomic promotion transaction. If any transaction replay fails, P001 remains active and Candidate B is the next exact construction route only when the failure belongs to Candidate A rather than tooling.

## Done Gate
The claim-level scientific debt is empty. Repository-level completion awaits the promotion transaction and does not imply that the parent corpus migration is complete.

## Cross-References
See the P001 proposal memory, `proposals/P001-sine-gordon-root`, `src/substrate_framework/sine_gordon.py`, `tests/test_sine_gordon.py`, and the parent `framework-migration` effort.
