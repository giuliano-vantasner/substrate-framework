# C-IGR-002 Claim Review

## Claim Under Review
The claim is the smooth-weight constant-mass theorem. With P230's declared operator and positive cutoff, weight `exp(-1/(Lambda^2*tau))`, constant `m2>=0`, and `z=m2/Lambda^2`, the exact local coefficient integrals are `I2=2*Lambda^2*sqrt(z)*K1(2*sqrt(z))` and `I3=2*Lambda^4*z*K2(2*sqrt(z))`, continuously extended at zero. They satisfy `dI3/dm2=-I2`, have massless limits `Lambda^2` and `Lambda^4`, and decay for large mass. Their conditional additive shifts use the same independently typed determinant and matching factors.

## Sourced Inputs
The review read v0.160.0, C-GRV-001, the P230 proposal and formula freeze, the primary heat-kernel sources, the reviewed PR implementations, the module, tests, and both campaign verifiers.

## Independence
The independent script instantiates the standard modified-Bessel integral family directly, proves its differential recurrence, boundary data, and large-mass behavior, and corroborates both integrals by 60-digit adaptive quadrature at three preregistered positive z values. It imports no P230 scientific implementation.

## Verification Status
The claim earns `symbolic_verified`. The standard exact K-integral identity is an explicit mathematical import; raw SymPy differentiation verifies the required K1/K2 recurrence and exact boundary and decay limits. High-precision quadrature is corroboration rather than the source of the verdict.

## Sensitivity and Counterexamples
Replacing K1 by K2 in I2 breaks the exact differential recurrence. A wrong determinant sign breaks the independently typed vacuum coefficient. Removing the constant-mass premise would introduce derivative endomorphism terms and invalidate factorization; that stronger statement is excluded.

## Framework Compatibility
The claim is a compatible conditional extension. It introduces an explicit smooth regulator premise rather than presenting the result as regulator independent. The exact massless I3 value differs from the sharp value by a factor of two, so no universal normalization is inferred. C-GRV-001's independent baseline remains untouched.

## Dependency and Consumer Replay
The accepted dependency is C-GRV-001 only for the additive ledger. The smooth weight, determinant convention, positive self-adjoint operator, and infrared/reference treatment are declared inputs. Consumers are the canonical module, package exports, tests, verifier, generated docs, and accepted memory; no preexisting runtime process is affected.

## Competing Candidate Audit
Candidate B survives on exact structural criteria. It is retained alongside A and C because P230 compares declared schemes; no numeric closeness or empirical gravity value selects it.

## Four-Axis Decision
Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active` within its conditional model. The relationship is a new claim depending on C-GRV-001, with no challenge or supersession.

## Promotion Transaction
The implementation, tests, immutable campaign, this review, registry, release v0.161.0, generated docs, accepted memory, and full validation form one promotion boundary.

## Continuation if Not Accepted
Not applicable. Extensions to other weights, varying masses, full determinants, or physical regulator choice require new claims.

## Done Gate
Acceptance is conditional on the final integrated status-zero gate and empty debt ledger recorded in P230 attempt 0003.

## Cross-References
See P230, C-IGR-001, C-IGR-003, the two campaign verifiers, `scalar_one_loop_mass.py`, and PRs #77/#82.
