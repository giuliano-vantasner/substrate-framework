# FS1 Source Adjudication

FS1 is qualified. Its finite, time-dependent 1+1 energy-density second moment
maps to `C-SG-009`, strengthened from a special-frequency grid/FFT result to an
exact family formula. Its physical internal-quadrupole and radiation language,
some oracle descriptions, and its static-kink normalization do not survive
claim-level review.

## Reproduction and NumPy Compatibility

The hash-pinned source exits cleanly with four checks under NumPy 2.5.1. Unlike
several earlier units, FS1 already defines a compatibility alias that selects
`numpy.trapezoid` when available and falls back to `numpy.trapz`. Its numerical
values reproduce. Each source check nevertheless aggregates many predicates,
so the terminal tally alone cannot establish the headline claim.

## Exact Scalar Moment

For the accepted rest breather with `eta=sqrt(1-omega^2)`, the centered scalar
energy-density moment has the exact full-line value

`mu(t) = 4*pi^2/(3*eta) + (16/eta)*asinh((eta/omega)*sin(omega*t))^2`.

P040 derives this by reducing the Hamiltonian density to two rational kernels
and differentiating their exact spatial Fourier transform. Independent
adaptive quadrature across the frequency family and scaled-domain refinement
agree with the formula.

The moment is even in time, nonconstant, and invariant under
`t -> t + pi/omega`. Because its nonconstant dependence is an injective
function of `sin(omega*t)^2`, its fundamental period is `pi/omega` and its base
angular frequency is `2*omega`. It is not a pure sinusoid: higher even harmonics
are present. At FS1's `omega=1/sqrt(2)`, the exact range is

`4*sqrt(2)*pi^2/3 <= mu <= 4*sqrt(2)*pi^2/3 + 16*sqrt(2)*asinh(1)^2`.

The source's FFT correctly identifies the dominant special-case `2*omega`
component. The absence of odd harmonics follows from the exact field-sign and
density half-period symmetry, not simply from calling the full nonlinear
Hamiltonian density quadratic.

## Mean Decomposition and Comparator

Splitting the Hamiltonian density into kinetic-gradient and potential terms and
then averaging the same sampled arrays makes the source identity
`<mu>=mu_kernel+mu_potential` linear bookkeeping. It is correct but not an
independent derivation. The special sampled values reproduce
`<mu>=2*sqrt(2)*pi^2` and equal halves `sqrt(2)*pi^2`, including the reported
`13.957728` form-factor comparator; P040 treats that as regression evidence,
not as an input to or selection of the exact instantaneous theorem.

## Static-Kink Guard

The conceptual static counterexample is sound: a time-independent density has
a constant moment. FS1's implementation, however, differentiates
`4*atan(exp(x))` as `4*sech(x)`; the correct derivative is `2*sech(x)`. The
correct kink energy density is `4*sech(x)^2` and its centered second moment is
`2*pi^2/3`. The source's wrong derivative changes that normalization, although
its fabricated seven-entry constant series remains constant by construction.
Neither version proves a radiation theorem.

## Physical Scope

The accepted object is a centered scalar width functional of a normalized 1+1
energy density. FS1 constructs no 3+1 mass-density tensor, transverse profile,
STF moment, isolated conserved stress tensor, gravitational action, retarded
solution, flux, or detector observable. Its own connectivity routes embedding
to pending FS2. A changing scalar second moment therefore does not establish a
physical internal mass quadrupole, gravitational radiation, a “monopole silent”
radiation theorem, or a finite-size channel invisible to GW4.

## Terminal Disposition

FS1 maps the exact scalar moment and its corrected temporal structure to
`C-SG-009` and is otherwise qualified. Excluded scope includes a 3+1 source or
STF quadrupole, gravitational wave or power, form-factor force identity,
monopole-radiation inference, physical breather size, and substrate realization.
Durable evidence is the P040 exact verifier, independent quadrature review,
source reproduction, and this adjudication.
