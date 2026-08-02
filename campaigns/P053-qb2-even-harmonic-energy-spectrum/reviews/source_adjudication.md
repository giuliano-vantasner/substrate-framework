# QB2 Source Adjudication

QB2 is qualified. Its half-period selection rule and spherical scalar-moment
identity survive, and a corrected observable on the accepted finite-box branch
has a converged dominant twice-frequency coefficient. The source does not
establish a nonzero STF moment, physical radiation, or an exact full-PDE
periodic eigenfunction.

## Reproduction

The hash-pinned source exits with status zero and `ALL 5 CHECKS PASS` in 2.4
seconds under Python 3.12.2, NumPy 2.5.1, SciPy 1.18.0, and SymPy 1.14.0. It
reports a standalone amplitude-three, single-harmonic shooting frequency
0.965311, even-bin fraction one, twice-frequency share 0.996567, odd/even
power ratio `9.77e-31`, and per-axis variance 6.2786.

The source already handles the NumPy API transition correctly: it selects
`np.trapezoid` when present and falls back to legacy `np.trapz`. The canonical
observable module calls the framework's shared `trapezoid_integral` dispatcher
instead of carrying either version-specific spelling.

## Exact Selection Rule

For a finite odd-cosine field, shifting the common phase by pi reverses the
field, its physical time derivative, and its radial derivative. Canonical
energy density is invariant under that simultaneous sign reversal. It is
therefore half-periodic, and every odd Fourier coefficient of the density or
of any time-independent radial linear functional vanishes exactly.

This is a selection rule, not a nonzero-line theorem. For the local
single-mode field `u=a(r)*cos(tau)`, the complete `cos(2*tau)` coefficient is

`a_r^2/4 - omega^2*a^2/4 + 2*J_2(a)`.

QB2 checks the kinetic and potential contributions but omits the radial-
gradient contribution from its conclusion. At `a=1` and `omega=0.97`, a real
choice of `a_r` cancels the complete coefficient while the fourth harmonic
remains nonzero. Thus neither even selection nor nonzero individual terms
forces the lowest nonconstant line to be twice the fundamental.

## Source Branch and False Oracle

QB2 recomputes a standalone N=1 Bessel shooting construction at central
amplitude three. It is not the accepted amplitude-2.5, N=9, mixed-boundary
finite-box branch of `C-PDE-006`. Neither `solve_ivp` path checks success,
message, finiteness, or endpoint completion before its output is classified or
consumed. Harmonic, radial, domain, tolerance, and transform refinements are
absent.

Exact-period sampling of an imposed odd-harmonic ansatz necessarily produces
even-bin purity. An arbitrary Gaussian radial profile with the same temporal
parity has odd/even power about `4.75e-31` while its radial sine-Gordon
residual RMS is 0.132448. The source's incommensurate-tone guard changes
temporal closure rather than the field equation, so it cannot show that the
purity is an eigenfunction or PDE effect.

## Corrected Finite-Box Scalar Object

The canonical positive object consumes `C-PDE-006` and declares

`S_12(tau)=4*pi*integral_0.001^12 r^4*T00(r,tau) dr`.

At central fundamental 2.5, wall 40, periodic projection 256, BVP tolerance
`1e-8`, a 2401-point exact-cutoff radial audit, and 512 endpoint-excluded
phases, the N=9 coefficient is 591.470484284. The N=1, 3, 5, 7, and 9 ladder
is 666.330281099, 591.504983105, 591.470022142, 591.470478411, and
591.470484284. The N=9 twice-frequency coefficient supplies 0.999865185 of
the resolved even coefficient power.

Temporal samples 256/512/1024 agree below `1e-9`; radial samples
1201/2401/4801 converge; initial BVP meshes 200/300/400 vary the coefficient
by less than 0.005; and tightening the solver from `1e-8` to `1e-9` with 512
projection samples changes it by 0.007 while reducing the collocation
residual by an order of magnitude. The full-box energy relative range falls
from 0.0582 at N=1 to below `9.7e-7` at N=9 alongside the full nonlinear core
remainder from 0.1052 to `1.37e-5`.

Walls 30, 40, 50, and 60 give core coefficients 591.270, 591.470, 598.370,
and 590.990. The bounded but nonconstant scan and the full-box variance spike
near wall 50 preserve the radiative standing-wave boundary ceiling. An
independent Gauss-Legendre phase and Simpson radial construction gives
591.468056462; 96/192/384 phase nodes vary this result by about `1e-9`.

## Moment and Radiation Meaning

QB2's `S(t)` is the radial second energy moment, not total energy. Its positive
time-averaged per-axis variance is a valid scalar output of a declared radial
profile. Exact spherical angular integration gives `I_ij=S*delta_ij/3`, so
the STF tensor is zero at every phase. Calling the scalar bin a “radiating
line” supplies no nonspherical source, source conservation, conditional
gravity map, waveform, flux, physical scale, or detector observable.

## Terminal Disposition

QB2 maps to exact selection and moment theorem `C-PDE-007` and qualified
finite-box scalar-spectrum evidence `C-PDE-008`. It remains qualified for its
universal nonzero and lowest-line claim, eigenfunction-sensitive purity guard,
standalone branch substitution, exact full-PDE periodicity, STF or physical
radiation language, and comparator-based transverse-scale interpretation.
