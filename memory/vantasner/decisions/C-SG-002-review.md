---
description: Independent claim-level review and acceptance decision for C-SG-002
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
# C-SG-002 Review

## Claim Under Review
For the `C-SG-001` breather in normalized units, the conserved Hamiltonian
`E = integral[(phi_t^2+phi_x^2)/2 + 1-cos(phi)] dx` equals `16 sqrt(1-omega^2)` for every `0 < omega < 1`. It approaches the two-kink threshold `16` as `omega -> 0+` and vanishes as `omega -> 1-`.

The relationship is a new claim depending only on `C-SG-001` and the declared normalized Hamiltonian.

## Sourced Inputs
The review read the null base release, P001 manifest and prose contract, the canonical field/energy APIs, unit tests, exact verifier, attempt `0001`, source inventory, predecessor rung147 and T1E, and the separate review rederivation artifact.

The predecessor `Energy.lean` result was treated correctly as definition-backed consequence evidence, not as a derivation of the coefficient `16`.

## Independence
The proposal verifier derives the energy on the `t=0` slice, where the field and potential vanish and the density is `8 eta^2 sech^2(eta x)`. The independent review does not import the canonical sine-Gordon module and instead uses the quarter-period static slice, retains gradient plus potential energy, changes variables with `y=tanh(eta x)`, verifies the exact antiderivative, and independently obtains `16 eta`.

The two routes share only the declared field equation, field construction, and real calculus; they do not share an energy helper or copied density formula.

## Verification Status
The maximum earned status is `symbolic_verified`. Exact integration derives the normalization and frequency dependence, and exact limits establish both endpoints. SciPy quadrature of the full nonzero-phase density at three frequencies is corroboration only and is not used to promote a numerical result as exact.

The expected energy is not the derivation input: the field is differentiated, the resulting density is integrated, and only then is the independently obtained expression compared with the canonical API.

## Sensitivity and Counterexamples
Energy coefficients `16 -> 15` and `16 -> 32` fail against the field-derived integral. The field coefficient, width relation, and potential sign mutations already fail the dependency claim. Numeric full-density checks use IEEE-754 binary64, `scipy.integrate.quad`, `epsabs=epsrel=1e-11`, and domains measured in inverse widths; domain refinement at 6, 10, and 14 inverse widths strictly reduces truncation error, with the final error below `2e-10`.

The independent review verifies the quarter-period antiderivative and endpoints and rejects a wrong-width field. These checks are sensitive to the load-bearing normalization and dynamics.

## Framework Compatibility
The claim introduces no parameter beyond `omega`, no empirical input, and no dimensionful scale in normalized units. The energy function is a pure importable API and composes directly with later action, mass/inertia, binding, and radiation claims. The normalization convention is encoded once rather than mixed with dimensionful predecessor readings.

## Dependency and Consumer Replay
The accepted dependency and successor consumer closure is explicit.

`C-SG-001` is the only scientific dependency and passed its independent review. The canonical module, seven sine-Gordon unit tests, P001 exact verifier, and independent review all pass. The 40 source bridge references identified by the pinned census are not accepted consumers; they remain queued for later claim-by-claim migration against this API.

No accepted consumer is broken, and the claim adds no unresolved assumption or residual beyond the normalized root model already declared by `C-SG-001`.

## Competing Candidate Audit
The same three candidates and frozen criteria apply. Candidate A earns exact symbolic verification with the fewest assumptions. Candidate B was not needed to repair a defect; its role is covered in part by the independent quarter-period derivation. Candidate C supplies only a corroborating numerical pattern and did not select the formula or tolerance.

## Four-Axis Decision
The claim passes all four independent decisions.

- Verification: `symbolic_verified`
- Review: `accepted`
- Compatibility: `native`
- Epistemic: `active`
- Relationship: new claim depending on `C-SG-001`; no `challenges` or `supersedes`

## Promotion Transaction
The atomic transaction added both claims to the registry, preserved the package API/tests, pinned `v0.1.0` to `substrate@6d1f4e0`, froze P001 as an adjudicated campaign, generated canonical docs and accepted memory, and replayed the moved targeted artifacts successfully.

## Continuation if Not Accepted
This decision is acceptance subject to successful promotion. A verifier or dependency failure reopens P001 at the diagnosed layer; it does not turn the result into a reduced numerical claim without a separate proposal revision.

## Done Gate
The claim-level debt ledger is empty. Parent corpus migration debt remains open after this root release and therefore the overall effort continues.

## Cross-References
See the C-SG-001 review, P001 proposal memory, attempt `0001`, independent review script, canonical sine-Gordon module, generated source inventory, and parent migration effort.
