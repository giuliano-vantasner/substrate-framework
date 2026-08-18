# C-IGR-001 Claim Review

## Claim Under Review
The claim is the sharp-cutoff constant-mass theorem. Conditional on the frozen P230 real-scalar determinant and heat-kernel conventions, for positive cutoff `Lambda`, constant `m2>=0`, and `z=m2/Lambda^2`, the exact local coefficient integrals are `I2=Lambda^2*(exp(-z)-z*E1(z))` and `I3=Lambda^4*exp(-z)/2-m2*I2/2`. They satisfy `dI3/dm2=-I2`, have massless limits `Lambda^2` and `Lambda^4/2`, and decay for large mass. The displayed inverse-Newton and vacuum shifts are additive conditional coefficients only.

## Sourced Inputs
The review read accepted release v0.160.0, C-GRV-001, the corrected P230 proposal and formula freeze, Vassilevich equations 1.16-1.20, 2.2, 4.26-4.27, Visser equations 7-15, PR #77's failed and repaired heads, PR #82's focused implementation, the canonical module, and all P230 executable evidence.

## Independence
The independent review script imports no `scalar_one_loop_mass` symbol. It solves the sharp tail problem from the boundary derivative, derives I3 by integration by parts, derives the determinant and Einstein-Hilbert factors separately, and only then compares the resulting formulas to the implementation through the primary verifier and tests.

## Verification Status
The claim earns `symbolic_verified`. Exact differentiation proves the I2 tail equation and the I3 derivative bridge. The positive defining integral and the bound by `exp(-z)/z` prove the large-mass I2 limit without relying on SymPy's unevaluated E1 limit. Exact massless limits and dimensions are checked separately. Numerical values are regression evidence only.

## Sensitivity and Counterexamples
Doubling the prefactor or replacing E1 by Ei breaks the tail derivative oracle. Adding `m2*I2` to the mass-resummed vacuum coefficient breaks the determinant-integrand oracle by a nonzero exact term. Flipping the proper-time determinant sign breaks the independent coefficient check. A varying `V''(phi_bg(x))` is a counterexample to factorization and is excluded by the constant-mass API and statement.

## Framework Compatibility
The claim is a compatible conditional extension of C-GRV-001. It preserves the independent additive baseline and treats the field content, positive self-adjoint operator, infrared/reference treatment, regulator, cutoff, and physical interpretation as premises. It establishes neither a total Newton constant nor a full or nonlocal effective action.

## Dependency and Consumer Replay
The accepted dependency is C-GRV-001 for the additive ledger only. The QFT conventions are explicit approved inputs, not hidden accepted claims. Direct consumers are the canonical module exports, tests, and P230 verifier; generated governance and memory consumers are replayed in the promotion transaction. No existing runtime caller depends on the API.

## Competing Candidate Audit
Sharp, smooth, and power-subtracted prescriptions were registered together before empirical comparators. Candidate A is retained for its literal positive tail-integral definition, not because its value is close to a physical target. Candidates B and C remain separate accepted conditional claims.

## Four-Axis Decision
Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active` within the declared conditional model. The relationship is a new claim depending on C-GRV-001, with no challenge or supersession edge.

## Promotion Transaction
The transaction materializes the P230 campaign, canonical API and tests, this review, the registry entry, release v0.161.0, generated docs and accepted memory, and the full replay. The source PRs remain provenance, not authority.

## Continuation if Not Accepted
Not applicable after the exact constant-mass narrowing. Any future varying-mass, nonlocal, physical-regulator, total-coupling, or higher-curvature statement requires a separate proposal and evidence.

## Done Gate
The claim is accepted only together with the final status-zero campaign verifiers, full repository validation, generated-state checks, and empty P230 debt ledger.

## Cross-References
See P230 formula freeze, `verify.py`, `independent_exact_mass_review.py`, PRs #77/#82, C-GRV-001, `scalar_one_loop_mass.py`, and `tests/test_scalar_one_loop_mass.py`.
