---
description: Independent review of C-IGR-004 derived usable total gravitational coupling composition and scheme selection
author: vantasner-review
created: '2026-08-18T15:48:27+00:00'
updated: '2026-08-18T15:48:27+00:00'
tags:
- substrate-framework
- claim-review
- induced-gravity
- total-coupling
category: decisions
confidence: working
status: active
---
# C-IGR-004 Claim Review

## Claim Under Review
The claim composes the accepted constant-mass one-loop families into the derived usable total gravitational coupling. Conditional on C-GRV-001's additive baseline and C-IGR-001..003, the governed renormalization condition is `1/G_total = B + N*(1-6*xi)*Lambda^2*J(z)/(12*pi)` with `J(z)` the curvature-class scale factor, and three exact legs (L1 strict spectral positivity, L2 monotone large-mass decoupling, L3 cutoff-ontology closure) output the usable scheme set `{sharp, smooth}` while the power-subtracted family is excluded and retained only as the scale-dependence ledger.

## Sourced Inputs
The review read the accepted registry entries and campaign artifacts directly. Inputs were accepted release v0.161.0, the registry entries for C-GRV-001 and C-IGR-001..003, the P231 proposal and formula freeze, the candidate/dependency/nonduplication/consumer/literature audits, the four prior attempts and the self-adversarial audit, the module `total_gravitational_coupling.py`, `tests/test_total_gravitational_coupling.py`, and both verifier routes; Vassilevich hep-th/0306138v3 and Visser gr-qc/0204062v1 are declared approved imports carried forward from P230.

## Independence
The load-bearing steps were independently rederived without importing the claim's module. A fresh SymPy plus 50-digit mpmath quadrature route rebuilt the sharp and smooth scale factors from their proper-time tail integrals, the squeeze `0 < J <= 1` and strict monotone decrease on a quadrature grid, the zeta sign-change root `exp(1-EulerGamma)`, the exact spread `R(1) = 2*e*K1(2)/(1-e*E1(1)) = 1.88377257808...`, and the composition against the accepted `scalar_one_loop_mass` shift.

## Verification Status
The maximum verdict is `symbolic_verified`. The selection legs are exact consequences of the strictly positive integrand of the defining tail integrals, the `tau^-1` monotone-decoupling class is itself a positive-integrand integral with the exact squeeze `0 < E1(z) <= exp(-z)/z`, and the scale-factor identities, the zeta root, and the spread value are exact; quadrature is corroboration only. The large-mass decoupling was confirmed by quadrature rather than an unevaluated SymPy `E1` limit.

## Sensitivity and Counterexamples
Every load-bearing mutation breaks the relevant oracle. A doubled prefactor, a flipped conformal weight, the wrong Bessel order, the `E1(-z)` branch, and a mutated reference member each fail the oracle the true formula passes; the excluded power-subtracted scheme raises on any attempt to normalize a total coupling; and the massless boundary returns the accepted continuous extension rather than NaN. The comparator-blind scan over module and test source finds no observed-G, Planck, or CODATA token.

## Framework Compatibility
The claim is a compatible conditional extension. It reuses the accepted families and baseline ledger without redefinition, keeps the local-coefficient ceiling of C-IGR-001 by leaving the `tau^-1` and nonlocal sectors in the control ledger with a predeclared domain, imports no fitted constant, and quotes the unbounded spread `R(z)` as the exact ceiling so no unique numeric normalization is asserted.

## Dependency and Consumer Replay
The accepted dependencies close inside the release. They are C-GRV-001 and C-IGR-001..003; direct consumers are the new module exports and its 41 tests, and the accepted P230 and C-GRV-001 consumer suites are additive-only and replay green. No existing public contract changed and no debt was created.

## Competing Candidate Audit
Alternatives were registered before comparator inspection with frozen criteria. Candidate A (scheme-uniform usable set) was selected on structural grounds; B (point scheme), C (subtraction scale), and D (full determinant) were rejected with recorded reasons, not numerical closeness, and no empirical comparator exists.

## Four-Axis Decision
The exact evidence supports acceptance.

- Verification: `symbolic_verified`
- Review: `accepted`
- Compatibility: `compatible_extension`
- Epistemic: `active`
- Relationship: depends on C-GRV-001 and C-IGR-001..003; challenges and supersedes none.

## Promotion Transaction
The transaction materializes the campaign record and release together. It adds C-IGR-004 to the registry and to release v0.162.0 with its `current.yaml` update, lands the campaign adjudication and per-claim reviews, regenerates docs and accepted memory, and passes full validation once at the final boundary.

## Continuation if Not Accepted
Not applicable after acceptance. A unique numeric normalization, a sourced geometry, or a radiative prediction each requires a separate proposal and an input no accepted claim supplies.

## Done Gate
Claim-level debt is closed after canonical synchronization and full replay, with an empty P231 debt ledger.

## Cross-References
See the P231 campaign record, formula freeze, `verify.py`, `independent_total_coupling_review.py`, C-GRV-001, C-IGR-001..003, `total_gravitational_coupling.py`, base release v0.161.0, and accepted release v0.162.0.
