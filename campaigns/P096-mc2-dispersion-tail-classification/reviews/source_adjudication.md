# P096 source adjudication

MC2 is qualified. Its linearized physical sine-Gordon dispersion and exterior
tail coefficient are exact, but its executable checks do not establish the
claimed global bound state, automatic radiation, universal gapless no-go,
material realization, or bounded named input.

Under C-MED-003, differentiating the residual at any vacuum `u=2*pi*n` gives
`lambda*psi_tt-T*psi_xx+mu*psi=0`. A plane wave
`exp(i*(k*x-Omega*t))` therefore gives
`Omega^2=omega_0^2+c^2*k^2`, with
`c=sqrt(T/lambda)` and `omega_0=sqrt(mu/lambda)`. On the positive branch the
floor is `omega_0`; for positive `k`, the phase and group velocities obey
`v_p*v_g=c^2`, `v_p>c`, and `0<v_g<c`. The group velocity tends to zero at the
floor and both velocities tend to `c` at high wavenumber. Unit coefficients
recover the accepted normalized `Omega^2=1+k^2` limit.

For a real-frequency separated field `a(x)*exp(-i*Omega*t)`, the spatial
equation is
`a''=((omega_0^2-Omega^2)/c^2)*a`. It is evanescent below the gap, affine at
threshold, and oscillatory above the gap. This classification concerns the
homogeneous exterior equation. Below the gap there is one decaying solution on
each half-line, but continuity of the field and derivative at the origin gives
the matrix `[[1,-1],[-kappa,-kappa]]`, whose determinant is `-2*kappa`.
Consequently the only smooth whole-line match is zero. The narrated
`exp(-kappa*abs(x))` has derivative jump `-2*kappa` and solves an equation with
a point defect, not the homogeneous equation MC2 checks.

At threshold every solution is affine and hence non-square-integrable on a
half-line unless zero. Above the gap every nonzero sine/cosine combination has
strictly positive norm per period, so repeating periods makes its half-line
norm infinite. The homogeneous constant-coefficient whole-line operator thus
has no nonzero `L2` real-frequency separated mode in any branch. A nonlinear
or defect core can match exterior decay; its existence is additional
structure. C-SG-017 supplies one exact nonlinear breather, and its asymptotic
rate `eta/ell` agrees with the independently derived linear exterior rate.
That agreement is a necessary tail cross-check, not a derivation of existence
from the linear spectrum.

Oscillatory is also narrower than radiative. A standing wave and a directed
traveling wave obey the same above-gap dispersion, but their time-averaged
energy fluxes are respectively zero and nonzero. An outgoing boundary or flux
condition is therefore required before using radiation language.

In the gapless limit the real-frequency separated equation still has no
nonzero whole-line `L2` eigenmode, but the wave equation admits every
d'Alembert profile `F(x-c*t)` and `F(x+c*t)`. The explicit profile
`sech(x-c*t)` is localized and has finite exact energy `2*T/3` in the declared
normalization. This refutes MC2's broader no-localized-dynamics reading while
leaving the precise separated-mode theorem intact.

MC2's source tally cannot repair its oracle gaps. The gap iff is sampled only
at `c=ell=1`; three regime predicates allow finite numeric fallbacks; only the
positive half-line exponential is differentiated; the named frequency's
alleged upper bound is never tested; and absence of a symbol named `a` is not
scale or material closure. P096 therefore promotes only the conditional exact
linear spectrum, exterior classification, whole-line `L2` theorem, nonlinear
tail cross-check, and explicit semantic ceilings. It derives no material,
coefficient value, defect, finite-box mode, nonlinear existence theorem,
radiation condition, 3-D density of states, cutoff, lifetime, population, or
absolute scale.
