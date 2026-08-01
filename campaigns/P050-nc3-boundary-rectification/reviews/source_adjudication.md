# NC3 Source Adjudication

NC3 is qualified. Its fixed-coordinate parity transformation and its
internally used sine-convention harmonic integral are exact and map to the
proposed `C-SG-013`. Its charge-discriminator, physical parity-violation,
parity-even-phase, boundary-orientation, and weak-sector conclusions do not
follow from its checks.

## Reproduction

The hash-pinned source exits with status zero and `ALL 18 CHECKS PASS` in 0.48
seconds under Python 3.12.2 and SymPy 1.14.0. The parity-weight products,
piecewise half-cycle integral, three phase values, bare sinusoidal time
integral, and fabricated-channel guard execute as written. Several checks
repeat the same assigned parity weights, and none tests the dynamics, domain,
boundary condition, state selection, winding implication, or weak-sector map
used by the headline.

## Two Distinct Boundary Functionals

For the right half-line `x>=b`, C-SG-011 gives topological density
`phi_x/(2*pi)`. If the field at positive infinity is time independent, the
actual topological charge change is

`Delta Q=-Delta phi(b)/(2*pi)=-(1/(2*pi))*integral phi_t(b,t) dt`.

This is the predecessor solution's “winding work.” NC3 instead calls the
different sign correlation

`R_b[phi]=integral sign(phi_t(b,t))*phi_x(b,t) dt`

by the same name `W_Q`. The source solution explicitly calls the winding and
mechanical boundary observables independent. No accepted theorem makes `R_b`
a topological charge, quantized quantity, or sufficient winding condition.

NC3's own sinusoidal trace is a decisive counterexample. Over one full period
`phi_t=A*sin(omega*t)` integrates to zero, hence `Delta Q=0`, while choosing
`phi_x=B*sin(omega*t)` gives `R=4*B/omega`, which is nonzero. Conversely a
zero coordinate channel gives `R=0` while a separately declared boundary field
change `2*pi` gives `Delta Q=-1`. Continuous scaling of `B` makes `R` arbitrary,
so it is not quantized. Correlation may be a diagnostic inside a separately
validated boundary model; it is not a model-free charge discriminator.

## Exact Harmonic Correlation and Convention Error

For real traces
`phi_t=A*sin(theta)` and `phi_x=B*sin(theta+delta)` with positive frequency,
direct positive/negative half-cycle integration gives

`R=4*sign(A)*B*cos(delta)/omega`.

This exact conditional formula, its relative-phase character, and its aligned,
opposite, and quadrature values are valid. One NC3 prose equation instead
writes the second trace as `B*cos(theta+delta)` while retaining the sine result.
With that unshifted cosine convention the result is
`-4*B*sin(delta)/omega`; equivalence requires the explicit quarter-cycle phase
conversion. The executable uses sine consistently, so its numeric phase values
validate only that convention.

## Parity and Boundary Orientation

For scalar parity `phi_P(t,x)=phi(t,-x)`, the chain rule gives

`R_b[phi_P]=-R_-b[phi]`.

At the parity center `b=0`, the fixed-coordinate observable is therefore odd.
This is a transformation law, not a proof that the field equation violates
parity; C-SG-011 and C-SG-012 prove the accepted equation and stress sector are
parity covariant.

A physical half-line adds domain orientation. The right-half-line outward
normal at the boundary is `-partial_x`. Parity maps that domain to a left
half-line whose outward normal is `+partial_x`, while the parity-transformed
field contributes its own minus coordinate derivative. The outward-normal
channel is therefore unchanged under the simultaneous field-and-domain map.
Parity is not an internal map of one fixed right half-line unless its boundary
law supplies additional structure. NC3 checks only the fixed coordinate
channel and cannot infer the physical boundary symmetry.

## Exact Accepted-Breather Limit

The accepted rest breather provides another exact guard. At its symmetry
center `phi_x=0` identically. At any other fixed boundary point its time
derivative is even and its spatial derivative odd under reflection about a
full period, so the sign-correlation density is period-antisymmetric and its
complete-period integral is zero. NC3's freely phased harmonic pair is a
declared boundary-trace model, not the unforced accepted breather trace.

## Interpretation Ceiling

A nonzero value of a parity-odd observable means the particular trace is not
fixed by parity. It does not distinguish explicit parity-breaking dynamics
from noninvariant boundary data, a selected member of a parity pair, or a
spontaneously asymmetric state. Likewise a zero odd observable does not prove
that a coupling is parity even. G1, G2, NC4, W1, and W3 remain pending source
units, so integer transfer, epsilon-to-chirality identification, chiral
anomaly, V-A interaction, weak force, particle identity, and substrate
ontology remain outside accepted closure.

## Terminal Disposition

NC3 maps its literal coordinate parity law and sine-convention harmonic
integral into `C-SG-013`. It remains qualified for the cosine transcription,
the shared `W_Q` name, treating the sign correlation as a sufficient winding
discriminator, labeling quadrature as a parity-even coupling, ignoring the
half-line normal and domain map, calling oddness physical parity violation,
and importing integer, chiral, weak, particle, or substrate conclusions.
