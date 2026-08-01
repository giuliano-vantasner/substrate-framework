# Source adjudication: QCD3 SU(3) one-loop coefficient

## Decision

QCD3 is qualified. Its explicit Gell-Mann representation supports
`C-LIE-001`; composing those invariants with the source's explicitly imported
one-loop weights supports conditional `C-RGE-002`. It does not derive the loop
weights, the substrate's physical gauge/matter content, a unique preference for
SU(3), two-loop running, an absolute scale, or confinement.

## Check-family audit

QCD3.1 through QCD3.5 are exact matrix claims accepted as `C-LIE-001`. The
declared `T_a=lambda_a/2` are Hermitian, traceless, and trace-normalized with
`T_F=1/2`; their commutators give antisymmetric structure constants; explicit
fundamental and adjoint Casimir sums give `C_F=4/3` and `C_A=3`. P024 adds full
commutator reconstruction and normalization/sign mutations.

QCD3.6 is accepted only with its own provenance wording retained. The group
factors are derived, but the gauge-plus-ghost weight `11/3` and Dirac-matter
weight `4/3` are imported perturbative field-theory results. Matrix algebra
then gives the conditional specialization `b0=11-(2/3)n_f`.

QCD3.7 exactly classifies the conditional coefficient: its zero is `33/2`, so
nonnegative integer flavor counts through 16 are positive and 17 onward are
negative. The statement that physical `n_f=6` applies to a substrate sector is
not established by this script or its pending YM1/EM5 dependencies.

QCD3.8 is a correct numerical regression for one chosen positive coefficient
and boundary coupling. It is not independent evidence: `C-RGE-001` and P024's
exact derivative and infinite-log-scale limit already prove the conditional
monotone decrease.

QCD3.9 correctly shows that deleting the declared gauge-loop contribution
leaves a negative matter term for positive flavor count. Calling this the
physical abelian theory additionally assumes its representation normalization
and field content; the accepted content is the conditional algebraic guard.

The source headline's “why SU(3)” language is too strong. Non-abelian groups
other than SU(3) can also have positive one-loop coefficients for appropriate
matter content, as the source itself acknowledges for SU(2). These checks
establish the declared SU(3) representation and conditional sign, not a unique
selection theorem or substrate identification.

## Exact qualification

Accepted content is limited to the exact standard-representation invariants,
the premise-explicit one-loop coefficient specialization, its integer sign
window, and its composition with `C-RGE-001`. Physical field content, uniqueness
of SU(3), loop-weight derivation, and infrared claims remain outside the claim
delta.
