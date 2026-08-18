# C-IGR-004 Claim Review

## Claim Under Review
The claim is the derived usable total gravitational coupling composition and its substrate-internal scheme selection. Conditional on C-GRV-001's independent additive baseline and the accepted constant-mass one-loop families C-IGR-001..003, the governed renormalization condition is `1/G_total = B + N*(1-6*xi)*Lambda^2*J(z)/(12*pi)` with `z = m2/Lambda^2` and `J(z) = I2/Lambda^2` the curvature-class scale factor, the induced shift taken unchanged from the accepted families. Three exact legs output the usable scheme set: L1 strict spectral positivity `0 < J(z) <= J(0) = 1`, L2 strict monotone large-mass decoupling `dJ/dz = -(tau^-1 class) < 0`, and L3 cutoff-ontology closure carrying `E_cut = hbar*c/a`. Sharp and smooth pass; the power-subtracted family fails L1/L2 (sign change at `exp(1-EulerGamma)`) and L3, so the usable set is `{sharp, smooth}` and the residual scheme dependence is the exact spread `R(z) = J_smooth/J_sharp`.

## Sourced Inputs
The review read accepted release v0.161.0, the registry entries for C-GRV-001 and C-IGR-001..003, the P231 proposal and formula freeze, the candidate comparison, dependency, nonduplication, consumer, and literature audits, the primary provenance, all four prior attempt manifests plus the self-adversarial audit, the canonical module `total_gravitational_coupling.py`, `tests/test_total_gravitational_coupling.py`, and both executable verifier routes. The approved primary imports (Vassilevich hep-th/0306138v3, Visser gr-qc/0204062v1) are carried forward from P230 as declared conventions, not silently promoted claims.

## Independence
An independent rederivation rebuilt each load-bearing fact from its defining integral with fresh SymPy and 50-digit mpmath quadrature, importing no `total_gravitational_coupling` symbol: the sharp and smooth scale factors from their proper-time tail integrals, the squeeze `0 < J <= 1` and strict monotone decrease on a quadrature grid, the zeta sign-change root `exp(1-EulerGamma)`, the spread value `R(1) = 2*e*K1(2)/(1-e*E1(1)) = 1.88377257808...`, and the composition `Delta(1/G) = N*(1-6*xi)*J(z)*Lambda^2/(12*pi)` cross-checked against the accepted `scalar_one_loop_mass` API. The independent large-mass decoupling was confirmed by quadrature (`J_sharp = 6.9e-90`, `J_smooth = 3.5e-12` at `z = 200`) rather than by an unevaluated SymPy `E1` limit.

## Verification Status
The claim earns `symbolic_verified`. The selection legs are exact: L1 and L2 follow from the strictly positive integrand of the defining tail integrals, and the `tau^-1` monotone-decoupling class is itself a positive-integrand integral with the exact squeeze `0 < E1(z) <= exp(-z)/z`. The scale-factor identities, the zeta sign-change root, and the spread value are exact symbolic results; quadrature is corroboration only. The composition equals the accepted C-IGR-001 shift exactly.

## Sensitivity and Counterexamples
Load-bearing mutations break the relevant oracle: a doubled prefactor, a flipped conformal weight `1+6*xi`, the wrong Bessel order, the `E1(-z)` branch, and a mutated reference member `J(0)=2` each fail the same oracle the true formula passes. The excluded power-subtracted scheme raises `ValueError` when asked to normalize a total coupling, and the massless boundary returns the accepted continuous extension (`J_sharp(0)=J_smooth(0)=1`, `J_zeta(0)=0`) rather than a NaN. The comparator-blind scan over module and test source finds no observed-G, Planck, or CODATA token.

## Framework Compatibility
The claim is a compatible conditional extension. It reuses the accepted families and C-GRV-001's baseline ledger without redefining them, preserves the local-coefficient ceiling of C-IGR-001 (the `tau^-1` and nonlocal sectors stay in the control ledger with a predeclared domain, never folded into the coupling), and imports no fitted constant. The usable set is an output of the legs, not a chosen regulator; the unbounded spread `R(z)` is quoted as the exact downstream ceiling, so no unique numeric normalization is asserted.

## Dependency and Consumer Replay
The accepted dependencies are C-GRV-001 for the additive ledger and C-IGR-001..003 for the coefficient families. Direct consumers are the new module exports and its tests; the accepted P230 consumer suite (`tests/test_scalar_one_loop_mass.py`) and the C-GRV-001 consumer (`tests/test_induced_gravity.py`) are additive-only and replay green. No existing public contract changed.

## Competing Candidate Audit
Four candidates were registered before comparator inspection with criteria frozen (exactness, L1/L2/L3, scheme-uniformity, assumption economy, comparator blinding). Candidate A (scheme-uniform usable set) was selected on structural grounds; B (point scheme), C (subtraction scale), and D (full determinant) were rejected with recorded reasons, not by numerical closeness. No empirical comparator exists in the campaign.

## Four-Axis Decision
Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active` within the declared conditional model. The relationship is a new claim depending on C-GRV-001 and C-IGR-001..003, with no challenge or supersession edge.

## Promotion Transaction
The transaction materializes the P231 campaign record, the canonical module and its 41 tests, this review, the registry entry, release v0.162.0 and its `current.yaml` update, generated docs and accepted memory, and full replay. The source proposal history remains provenance, not authority.

## Continuation if Not Accepted
Not applicable after acceptance. A unique numeric normalization, a sourced nonflat geometry, or a radiative prediction each requires a separate proposal and a further scheme-selection input no accepted claim supplies.

## Done Gate
The claim is accepted together with the final status-zero campaign verifiers, full repository validation, generated-state checks, and an empty P231 debt ledger.

## Cross-References
See the P231 proposal, formula freeze, `verify.py`, `independent_total_coupling_review.py`, C-GRV-001, C-IGR-001..003, `total_gravitational_coupling.py`, `tests/test_total_gravitational_coupling.py`, base release v0.161.0, and accepted release v0.162.0.
