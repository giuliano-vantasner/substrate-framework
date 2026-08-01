# Source adjudication: CF2 fixed-flux linearity

## Decision

CF2 is qualified. Its fixed-area field-energy derivation supports
`C-FLX-001`, but its narrative conflates that energy slope with endpoint
test-charge force without the required `q=Phi/2` premise. It establishes no
quark, chromoelectric, QCD, Riesz-dynamics, area-law, or confinement identity.

## Check-family audit

CF2.i-a through CF2.iii-c correctly derive `E=Phi/A` and stored field energy
`U(L)=Phi^2*L/(2A)` for a uniform fixed-area tube with energy density `E^2/2`.
The slope `Phi^2/(2A)` is exact and symbolic. P027 makes the one-half and Gauss
area power mutation-sensitive.

The question and prose also declare endpoint force `F=qE`, whose work is
`q*Phi*L/A`. The executable linear-tube path never uses `q`; it simply calls the
field-energy derivative the force. The two slopes agree exactly only if
`q=Phi/2`. In particular `q=Phi` gives a factor of two. No charge-flux relation
is derived or declared by CF2, CF1, or an accepted dependency.

CF2.iv's exponent arithmetic is correct but does not dynamically realize
pending EM7 or turn an ideal geometry into a physical sector. The accepted
claim needs no Riesz dependency.

CF2.v correctly contrasts fixed area with spherical spreading. P027 strengthens
the guard with `A(L)=A0*(1+L/L0)`, which gives logarithmic rather than linear
field energy. The physical words confinement and deconfinement remain outside
the algebra.

CF2's “same object CF1 computes” statement is not established. Given a separate
tension, `A_eff=Phi^2/(2*sigma)` reconstructs it by definition and remains
dependent on the supplied tension. A smooth vortex does not independently
supply CF2's ideal uniform fixed area.

## Exact qualification

Accepted content is limited to the two conditional linear constructions, their
distinct slopes, exact equality condition, and variable-area/spherical guards.
Physical charges, fixed-tube realization, CF1 tension identity, QCD, Riesz
dynamics, area law, and confinement remain outside the claim delta.
