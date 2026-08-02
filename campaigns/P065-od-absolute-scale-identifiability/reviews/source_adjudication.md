# P065 OD and AS4 Source Adjudication

OD exits cleanly with `ALL 8 CHECKS PASS`, and the later AS4 annotation exits
cleanly with `ALL 7 CHECKS PASS`. Those tallies are reproduction evidence, not
promotion evidence.

OD's exact 4x5 coefficient matrix has the null vector
`(-1, 1, 1, 1, 1)`. The scale coordinate is indeed unidentifiable, but the
source's description of a free direction “exactly ln(a)” is false: every
nuisance coordinate changes along the same affine direction. No selected
symbolic solve can replace that nullspace test. More importantly, OD declares
its log rows instead of deriving dimensionless reference-ratio equations from
its cited sectors, treats unspecified right-hand sides as known, hard-codes its
independence Boolean, and never computes a physical compatibility residual.

AS4 does not repair those defects. Its four rows have only two coefficient
directions: the medium row is proportional to gravity, and confinement is
proportional to hadronic. The other two rows could be valuable compatibility
tests if their right-hand sides, uncertainties, covariance, and dependency
closure were supplied. They are not. AS4's strongest rejection guard is also
internally inverted: its extra-length matrix has rank three over three unknowns
and nullity zero, exactly as the check asserts, while the surrounding prose says
that nullity reopens and the system becomes underdetermined.

The reusable exact mathematics is separable from those physical claims. P065
therefore rejects candidate A as a derivation and selects B-E conditionally:
positive monomial log conversion with explicit reference ratios, coordinate
identifiability from every null vector, left-null compatibility, incremental
coefficient and augmented rank, exact declared-covariance GLS, and one-coordinate
closed-interval intersection. None of these ledgers manufactures a physical
row, observation, statistical independence, or absolute scale.
