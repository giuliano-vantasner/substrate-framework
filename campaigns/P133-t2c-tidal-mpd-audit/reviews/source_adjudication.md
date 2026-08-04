# T2C Source Adjudication

T2C's thirteen checks reproduce. Its optical Christoffels, Riemann components,
Ricci scalar, and two-dimensional Gaussian-curvature identity are exact under
the declared sign and slot convention. Those geometry results are already
governed by C-OG-001. The source also uses the correct generic Fourier identity
`-w_tilde''(0)=integral y^2 w(y) dy`, but its claimed force does not follow from
either fact.

## Kernel Object and Upstream Response

The hash-pinned phase-three source reproduces with current `np.trapezoid` calls.
At `omega=1/sqrt(2)` its time-averaged coupling kernel has exact mass
`4*sqrt(2)`, raw second moment `sqrt(2)*pi^2`, and normalized variance `pi^2/4`.
The raw kernel moment is not C-SG-009's instantaneous Hamiltonian energy moment;
at phase zero the latter is `4*sqrt(2)*pi^2/3`.

More importantly, phase three derives the fixed-profile force as a convolution
of the centered even kernel with the background gradient. Its long-wavelength
expansion starts with the third spatial derivative of the background. T2C
instead multiplies its second derivative through the scalar curvature. It
therefore does not reproduce the mechanism from which it imports the moment.

## Correct Conditional Finite-Width Alternative

P133 registers a separate, explicit effective prescription. Let
`a(x)=c0^2*n_x/(2*n^3)` be the accepted slow point acceleration and average it
over a normalized centered scaled profile. Differentiation with respect to the
scale gives the leading width term

`(sigma^2/2)*a_xx
 = c0^2*sigma^2*(n_xxx/n^3-9*n_x*n_xx/n^4+12*n_x^3/n^5)/4`.

For `n=1+epsilon*xi`, the coefficient linear in `epsilon` is
`c0^2*sigma^2*xi_xxx/4`, agreeing with the upstream convolution's derivative
order. Curvature times width instead gives
`c0^2*sigma^2*xi_xx/2`. The former has acceleration units; the latter has
velocity-squared units. This exact conditional theorem, its pure API, and tests
are promoted as C-OG-004. It remains a declared profile-average model, not a
field-derived deformation or gravity law.

## Symmetry and Perturbative Countermodels

For the even index `n=1+beta*x^2/2`, the accepted point acceleration is odd.
Every even centered profile therefore has exactly zero averaged acceleration at
`x=0`. C-OG-004 respects that null. T2C predicts the nonzero value
`c0^2*beta*sigma^2/2` there, so its force violates reflection symmetry.

For `n=1+epsilon*x`, the profile-average correction begins at
`3*c0^2*epsilon^3*sigma^2` at the origin. T2C begins at
`-c0^2*epsilon^2*sigma^2`, with different perturbative order and sign. In the
source's own sign sample, the alleged correction has magnitude about 4.65 times
the point acceleration. Checking only that this ratio is finite supplies no
small hierarchy or remainder control for calling it a leading correction.

## Papapetrou and Dixon Equation Audit

Papapetrou's curvature force is the pole-dipole spin term, proportional to
`R_abcd*u^b*S^cd` with antisymmetric spin. Replacing spin by a symmetric
rank-two moment in those antisymmetric slots contracts to zero. T2C's displayed
`R^1_010*J^11` also does not match its own slot labels.

Dixon's quadrupole equation uses a rank-four moment with Riemann symmetries and
a curvature derivative: `-(1/6)*nabla_a R_bcde*J^bcde`. It additionally evolves
momentum and needs mass or momentum-velocity closure and a worldline
prescription before it becomes coordinate acceleration. T2C executes none of
these objects. Its citation to Dixon 1970 is Part I, which defers the equations
of motion to subsequent work; Dixon's Part III equations paper is from 1974.

The point-limit and nonzero guards do not repair this gap. Every arbitrary
coefficient multiplied by a second moment vanishes when that moment is set to
zero, remains linear, and is generically nonzero. Those checks are necessary
scope guards but cannot select a force law.

## Dependencies, Consumers, and Compatibility

Qualified FS1, FS2, P3D3, and T1B and duplicate-evidence FS4 retain their
accepted ceilings; none supplies a typed MPD equation or field-derived optical
finite-size trajectory. T2C's annotation that they close its future work is not
authority. Pending G2 reuses only curvature machinery. Pending G4 narrates the
T2C label but executes a finite-wave-number form factor, not the rejected
curvature-width formula. Both replay, granting no physical-source authority.

T2C contains no NumPy call. The upstream mutable phase-three script uses
`np.trapezoid`. Immutable G4's single legacy `np.trapz` call replays through the
recorded alias `np.trapz=np.trapezoid`; that is a compatibility event, not a
scientific failure.

## Terminal Disposition

T2C is qualified through C-OG-001, C-CC-001, and the corrected conditional
C-OG-004 alternative. Its exact geometry and generic Fourier moment identity
survive. Its curvature-times-rank-two-moment acceleration, MPD/Dixon label,
physical sign reading, leading-correction claim, backward ceiling lift, and
gravity, material, or substrate interpretations are rejected. Release
v0.101.0 promotes only C-OG-004.
