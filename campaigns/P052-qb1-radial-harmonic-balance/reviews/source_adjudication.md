# QB1 Source Adjudication

QB1 is qualified. Its projected radial mode equation and its finite-box branch
are reproducible, but its free-amplitude inversion, all-mode wall condition,
and frequency-only truncation check do not establish a unique localized
quasibreather or recover the accepted IVP frequency from the equation alone.

## Reproduction

The hash-pinned source exits with status zero and `ALL 6 CHECKS PASS` in about
99 seconds under Python 3.12.2, NumPy 2.5.1, and SciPy 1.18.0. At central
amplitudes 1.5 through 4.0 it reports frequencies 0.992221, 0.985753,
0.976909, 0.965311, 0.950525, and 0.932080. At amplitude 2.5 its N=1, N=3,
and N=5 values are 0.976909, 0.976877, and 0.976874. Solver success enters the
aggregate BVP check, but the separate shooting event result is consumed
without an explicit solver-success or finiteness guard.

QB1 uses a periodic discrete sum and does not call `np.trapz`. The canonical
projection uses the explicit periodic DFT normalization `2/N`, so this unit
does not require either NumPy trapezoidal-integration spelling.

## Exact Projection and Origin Rule

For the odd-cosine ansatz

`u(r,tau)=sum_(n odd) a_n(r)*cos(n*tau)`, with `tau=omega*t`,

projection of `u_tt-u_rr-2*u_r/r+sin(u)=0` gives

`a_n''+2*a_n'/r+(n*omega)^2*a_n-S_n[a]=0`,

where `S_n=(1/pi)*integral_0^(2*pi) sin(u)*cos(n*tau) dtau`. The factor two
in the equivalent periodic sum is load-bearing and is independently matched
to the Jacobi-Anger coefficients. Even radial regularity gives
`3*a_n''(0)+(n*omega)^2*a_n(0)-S_n(0)=0`; merely placing `a_n'=0` at a small
positive radius omits that second-order origin correction.

## Far-Field Channels

Linearization gives

`a_n''+2*a_n'/r+((n*omega)^2-1)*a_n=0`.

For `n*omega<1` the channel is evanescent, proportional to
`exp(-sqrt(1-(n*omega)^2)*r)/r`. At threshold it has the radial zero-mode
form. For `n*omega>1` it is oscillatory, proportional to
`sin(sqrt((n*omega)^2-1)*r+delta)/r`. A nonzero radiative tail has positive
asymptotic energy per unit radial length and therefore infinite integrated
three-dimensional energy. On the source-like branch the fundamental is
evanescent while every retained harmonic `n>=3` is radiative. Setting all of
them to zero at `R=40` fixes standing-wave phases in a finite box; it is not an
infinite-domain localization condition.

## Corrected Finite-Box Object

The canonical solver declares `a_1(0)=2.5` as a free branch coordinate rather
than an equation-derived constant. It applies a decaying Robin condition to
the evanescent fundamental and finite-wall Dirichlet conditions to radiative
channels. Through N=1, 3, 5, 7, and 9 the fitted frequency converges to
0.976873921394, while the full nonlinear core remainder falls from 0.10542 to
1.3719e-5. The final collocation residual is below 1e-8. Initial radial meshes
200/300/400, temporal samples 256/512, and tolerances 1e-8/1e-9 preserve the
branch.

Domain variation is deliberately not summarized by frequency alone. Walls at
R=30, 40, 50, and 60 move the core frequency by less than 6.5e-5, but the
third-harmonic `r*a_3` tail RMS rises from order 7e-4 to 1.53e-2 near R=50 and
falls again. This nonmonotone resonance is the expected standing-wave wall
sensitivity and sets the finite-box epistemic ceiling.

## Comparator Calibration

QB1 inserts the accepted P3D1 value 0.921 as a target and bisects the free
central amplitude to about 4.2575. That operation calibrates a family
coordinate; it does not predict the comparator from the equation alone. The
canonical N=9 branch at amplitude 2.5 was selected and converged without using
the P3D1 frequency as a boundary condition, threshold, or fit target.

## Independent Evidence and Failed Routes

The independent review uses DOP853 event shooting for N=1, Gauss-Legendre
temporal projection with a separately written BVP through N=9, and centered
finite differences with nonlinear least squares on 81, 121, and 161 radial
points. Its second-order zero-spacing extrapolate 0.976871246116 agrees with
the Gauss N=5 value 0.976873950083, and its N=9 remainder is 1.3759e-5. It does
not call the canonical harmonic-balance APIs.

Cold unconstrained BVP seeding, an incorrect static source spelling, a raw-grid
comparison that ignored second-order error, and least-squares runs that hit
their iteration limit are preserved as attempts 0002, 0006, 0008, and 0009.
Each was repaired at the responsible numerical or verifier layer without
loosening the physical residual or solver-success criteria.

## Terminal Disposition

QB1 maps to the exact projection/channel theorem `C-PDE-005` and the explicit
finite-box numerical branch `C-PDE-006`. It remains qualified for calling the
fitted frequency a unique nonlinear eigenvalue, treating the all-mode wall as
localization, measuring harmonic convergence only by frequency shifts,
recovering P3D1 after fitting amplitude to P3D1, and implying an exact,
finite-energy, infinite-domain, or eternal quasibreather.
