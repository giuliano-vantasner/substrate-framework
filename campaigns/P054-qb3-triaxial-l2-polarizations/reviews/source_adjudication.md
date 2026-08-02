# QB3 Source Adjudication

QB3 is qualified. Its real (m=2) angular shape does generate an exactly
triaxial first-order energy-moment tensor when paired with a genuine regular
radial (ell=2) solution. Its computed radial function, finite-amplitude field,
and two-mode interpretation do not establish the stronger claims in the
source.

## Reproduction and NumPy Compatibility

The hash-pinned source exits with status zero and `ALL 4 CHECKS PASS` in 5.6
seconds under Python 3.12.2, NumPy 2.5.1, SciPy 1.18.0, and SymPy 1.14.0. It
reports core frequency 0.965311, averaged-mode frequency 1.0877, sampled
averaged-operator residual ratio `8.98e-6`, and diagonal triple-STF entries
438.49, 115.03, and -553.52.

The source already handles the NumPy API change correctly: it selects current
`np.trapezoid` and falls back to legacy `np.trapz`. Canonical P054 code does no
quadrature; established framework modules continue to use the shared
version-dispatching `trapezoid_integral` helper.

## Radial Operator, Origin, and Wall

The accepted linearized equation has the time-dependent coefficient
`cos(P(r,t))`. QB3 replaces it with `J0(a1(r))`, the phase average of a
single-harmonic background. The omitted full-equation term is exactly

`(cos(P)-<cos(P)>)*psi`.

For `P=a*cos(tau)`, its leading nonstatic coefficient is
`-a^2*cos(2*tau)*psi/4`. A converged eigenpair of the averaged operator is
therefore not a Floquet solution of the original equation.

QB3 also imposes `g(0.01)=0` and `g'(0.01)=1e-4`. A nonzero regular
ℓ=2 series instead has `g=C*r^2+O(r^4)` and obeys
`r*g'-2*g=O(r^4)`; the source pair has mismatch `1e-6` and no nonzero regular
continuation to the origin. Its localization predicate is additionally
tautological because the evaluated solution is manually overwritten with zero
beyond `R_mode` before the final-tail test.

P054 solved the corrected self-adjoint averaged `v=r*psi` operator on the
accepted C-PDE-006 N=9 background. Meshes with 800, 1600, and 3200 intervals
converge to lowest eigenvalue 1.02070369329 with relative eigenpair residual
`1.15e-10`. The independent vacuum spherical-`j2` box limit is reproduced to
`2.04e-9`. The value lies above the unit continuum threshold, about 0.249 of
the transformed norm remains in the outer quarter, and moving the wall from
30 to 40 changes the eigenvalue by 0.01587. This is a finite-wall standing
wave, not a localized state. It is not promoted as a Floquet no-go theorem;
other genuinely time-periodic spectra remain a separate question.

## Exact Real-ℓ=2 Tensor

For the unnormalized real basis

`P2(nz), nx^2-ny^2, 2nx*ny, 2nx*nz, 2ny*nz`,

let each `H` be `4*pi*integral(r^4*h(r),r)` for its declared first-order
energy-density coefficient. Independent sphere integration and an isotropic
Cartesian fourth-moment derivation give the triple-STF tensor

```text
[-H20/5+2H2c/5,  2H2s/5,          2H1c/5]
[ 2H2s/5,        -H20/5-2H2c/5,   2H1s/5]
[ 2H1c/5,         2H1s/5,          2H20/5]
```

A pure nonzero real-(m=2) cosine coefficient therefore gives
`diag(2H/5,-2H/5,0)`, with three distinct eigenvalues. This positive result is
exact and does not rely on QB3's radial eigenvalue or finite deformation.

All five real ℓ=2 shapes have angular eigenvalue -6. The radial linearized
equation is consequently independent of `m`. Pairing the already accepted
regular C-PDE-004 radial solution with `nx^2-ny^2` gives a genuine finite-time,
first-order nonaxisymmetric solution. If `q(t)` is the accepted P2 `Qzz`
coefficient, the real-(m=2) tensor is exactly `diag(q,-q,0)`. It inherits
C-PDE-004's resolved nonzero trace without rerunning or refitting that IVP.

## Energy and Temporal-Rank Audit

QB3 calls its density full `T00` but omits the angular-gradient term
`|grad_Omega u|^2/(2*r^2)`. It then evaluates nonlinear energy at finite
deformation amplitude from a first-order perturbation without the required
second-order field corrections. Its reported finite-amplitude tensor values
therefore are not self-consistent nonlinear field evidence, even though the
linear real-(m=2) cross term has the correct triaxial structure.

Along the natural z sightline, the exact conventional plus and cross readouts
are `2H2c/5` and `2H2s/5`; normalized unit-Frobenius coordinates are larger by
`sqrt(2)`. Two nonzero coordinate readouts do not prove two source modes. A
fixed triaxial tensor multiplied by one scalar trace has temporal coefficient
rank one in every polarization frame. Rank two requires two nonproportional
time traces, such as independently supplied quadrature-phase cosine and sine
coefficients. QB3 evaluates one phase pair and supplies no such rank-two
trajectory, TT time series, or source dynamics.

## Terminal Disposition

QB3 maps to exact m-degeneracy and averaging-ceiling claim `C-PDE-009` and
exact real-ℓ=2 STF/TT/temporal-rank claim `C-GW-007`. It remains qualified
for regular localized averaged or Floquet eigenmode, finite-amplitude
self-consistency, the reported nonlinear moment values, two independent
temporal modes, graviton counting, physical radiation, gravity, waveform,
flux, absolute scale, particle identity, and substrate realization.
