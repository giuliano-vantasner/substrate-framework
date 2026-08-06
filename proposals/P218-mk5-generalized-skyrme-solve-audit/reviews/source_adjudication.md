# P218 MK5 Source Adjudication

## Decision

MK5 is qualified rather than accepted wholesale. Its exact conditional
extended radial model and a replacement supplied-coefficient branch support
C-GSK-001/002. Its physical coupling closure, source numeric kappa, residual
parameter floor, asymptotic bracket claims, debt discharge, and comparator
guard do not enter the accepted claims.

## Source Reproduction and Oracle Scope

The pinned 26,426-byte source at SHA-256 `a5ecb5d...246f8` contains eight
runtime checks and one fail-fast assertion and reaches `ALL 8 CHECKS PASS` once
in 63.93 seconds. It imports current SciPy `trapezoid` and has no legacy NumPy
surface. The run is preserved rather than repeated. Its tally is reproduction,
not authority for solver residuals or physical dependencies.

## MK5.1

MK5.1 contains valid conditional reduction algebra. Requiring equal L2/L4
reduced coefficients gives `L=2/(e F)` and prefactor `F/(4e)`. In the accepted
convention, `c6=lambda_BPS^2 e^4 F^2/8`; the source form
`lambda_A^2 e^4 F^2/(8 pi^4)` is equal only after C-VEC-002's explicit map.
Also `c0=32 mu^2/(e^2 F^4)`. Substituting MK1/MK2 values is not accepted
physical closure.

## MK5.2

MK5.2's structural angular claim survives: squaring the factorized pullback
density produces the normalized average of the squared angular Jacobian,
which is C-RMAP-001's `I`, not `B^2`. The source numeric regression is biased
because it samples endpoint-excluding midpoint grids and then applies
trapezoids; it obtains 0.9975, 5.7937, and 20.6255 instead of accepted inputs
1, `pi+8/3`, and 20.6496264884189.

## MK5.3

MK5.3 is baseline regression only. Its finite Dirichlet-wall classical solve
approximately reproduces the older source numbers, but C-RPROF-001/002 and
C-RDIFF-002 already own a stronger asymptotic-boundary, independently refined
L2+L4 result. Agreement with the weaker corpus implementation does not validate
the extended solver.

## MK5.4

MK5.4's source number is not promoted. Although every continuation stage
checks `solve_bvp` status, the source never inspects RMS/equation residuals,
uses exact `f(epsilon)=pi,f(R)=0` instead of asymptotic Robin data, changes the
initial mesh and output quadrature together, omits inner-cutoff and tolerance
refinement, and checks kappa domain stability without each energy's error. Its
0.496 epsilon and physical coefficients also lack accepted closure. C-GSK-002
replaces this with a clean supplied benchmark and stronger oracles.

## MK5.5

MK5.5 is conditional algebra without a paid residual. For
`epsilon_BPS=(F/e)/(lambda_BPS mu)`, the exact declared coefficient product is
`c6*c0=4/epsilon_BPS^2`. In the source lambda-A coordinate this becomes
`4/(pi^4 epsilon_A^2)`. No accepted claim assigns either local quotient to
C-BPS-003 epsilon or supplies its physical value, so the product and the claim
that exactly one physical residual remains are unaccepted.

## MK5.6

MK5.6 is rejected as a physical residual/floor conclusion. The executable
sweep is `e=2.5,3,4,5.45,7,9`, not the headline `[2,16]`, and every coefficient
on the curve inherits rejected physical inputs. Six solved points establish
neither a global floor nor weak dependence outside the sampled interval.

## MK5.7

MK5.7 supplies finite-scale counterevidence only. Three points at common
coefficient scale factors 1, 4, and 16 increase, but they do not prove an
asymptotic BPS limit, unbounded growth, or a direct mechanism inherited from
MK4. The signed difference is not a variational bound, and the source's
physical bracket has no accepted premises.

## MK5.8

MK5.8 fails its literal headline. The executable constructs
`FORBIDDEN=[929/1000,...]` and reads the reconstructed 0.929 in `guard_clean`.
Scanning only numeric literals after splitting the value does not establish
that no comparator value is present or consulted. C-GSK-002 uses no comparator
in candidate selection or verification.

## Replacement Verification

Twenty-seven primary, twelve independent, and nine graph checks plus 65
focused tests pass. C-GSK-001 is exact. C-GSK-002 uses checked collocation and
independent vacuum-complement shooting, correct angular inputs, asymptotic
Robin data, isolated refinements, residuals, virial balance, and load-bearing
mutations. Direct-field and brittle-wording failures remain append-only.

## Terminal Scope

MK5 maps its conditional functional and angular insight to C-GSK-001 and its
finite-wall numeric idea to the stronger C-GSK-002 replacement. It establishes
no derived physical coefficients, empirical binding prediction, global
minimum, full three-dimensional solution, universal residual floor, BPS-limit
theorem, paid debt, particle or nucleus, or substrate mechanism.

