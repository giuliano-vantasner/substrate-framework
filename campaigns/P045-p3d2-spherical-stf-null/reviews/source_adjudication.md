# P3D2 Source Adjudication

P3D2 is qualified. Its arbitrary-radial-density angular theorem and exact STF
null map to `C-MOM-003`, and its evolved core energy-radius moment maps to the
cutoff- and resolution-bounded `C-PDE-002`. Its claims of exact frequency
doubling, physical zero gravitational radiation, and a forced radiating
`l=2` channel do not follow from the checked equations.

## Reproduction and Compatibility

The hash-pinned source exits cleanly with four checks in 1.69 seconds under
NumPy 2.5.1. Its compatibility expression selects `numpy.trapezoid` before the
older `numpy.trapz` fallback. It reports a scalar-moment relative half-range
`0.3160`, center FFT frequency `0.8901`, moment FFT frequency `1.7802`, exact
displayed ratio `2.0000`, a constructed spherical STF ratio zero, and a
nonzero deformed triple-STF scale `158431.8189`.

## Exact Spherical Moment Theorem

For any integrable radial density, define
`J=integral rho(r)*r^2 d^3x`. Direct sphere integration gives
`integral n_i*n_j dOmega=(4*pi/3)*delta_ij`, so
`I_ij=(J/3)*delta_ij`. Its trace is `J`; both the normalized STF tensor and
the triple convention `Q=3*I_STF` vanish exactly. Positivity and radial field
dynamics are unnecessary for this angular result.

P045 independently integrates all nine unit-vector products and repeats the
result with Gauss-Legendre polar and uniform azimuthal quadrature. It also
derives the axisymmetric deformation
`rho=f(r)*(1+a*P2(cos(theta)))`. Since the `P2` angular mean vanishes, the
trace stays `J`, while
`I_STF=diag(-a*J/15,-a*J/15,2*a*J/15)` and
`Q=diag(-a*J/5,-a*J/5,2*a*J/5)`. This is a load-bearing exact mutation rather
than a floating-point near-zero comparison.

P3D2's numerical spherical null adds no independent evidence: it explicitly
sets `I=(S/3)*identity` and immediately trace-subtracts it. The result must be
zero by the exact algebra regardless of whether the field evolution or scalar
moment is correct.

## Finite-Time Core Moment

P045 extends the canonical `C-PDE-001` solver to record
`S_R(t)=4*pi*integral_0^R r^4*T00(r,t) dr` at the correctly centered sample
times. For the accepted amplitude-three, width-four branch, baseline
`dr=0.05`, `dt=0.02`, domain 200, time 450, and core radius 30, detrended
Hann/quadratic FFT estimates of the moment frequency are `1.836824895` and
`1.846654767` on windows starting at 220 and 300. Independently interpolated
prominent maxima give `1.833065731` and `1.840263479`.

Relative to the contemporaneous field estimates, the FFT ratios are
`2.000850743` and `2.000303395`, and the time-domain ratios are `1.998749311`
and `1.999259381`. The core moment relative half-ranges exceed `0.26`; this is
a nontrivial breathing diagnostic. The absolute frequencies shift between
windows because the finite-time oscillon chirps slowly, so P045 accepts a
bounded near-two relation, not exact equality.

Meshes `0.1`, `0.05`, and `0.025`, timestep halving, and outer domains 160,
200, and 240 preserve the ratios within the campaign bounds. Core cutoffs 20,
25, and 30 also agree. At cutoff 40, however, the `r^4` weighting amplifies an
outgoing radiative shell and low-frequency drift becomes the dominant FFT
component (`omega` about `0.074` and `0.063` on the two windows), even though
peak timing still finds the core oscillation. The accepted claim is therefore
explicitly restricted to `20<=R<=30`; it is not a global second-moment
frequency theorem.

An independent DOP853 method-of-lines evolution on `dr=0.2`, domain 200, and
time 300 agrees with leapfrog to `1.469e-2` relative moment RMS. A separately
implemented detrended FFT and quadratically interpolated maximum-spacing route
give contemporaneous ratios between `1.9965` and `2.0020`. The weak dispersive
seed supplies no resolved combined persistent-core verdict.

## Source Frequency and Timestamp Defects

P3D2 samples a 120-unit settled window, whose angular FFT bin spacing is about
`0.05236`. It selects center bin 17 and moment bin 34, so the reported ratio is
exactly two because the bin indices are integers. This cannot establish exact
frequency equality. Its copied P3D1 loop also labels the centered `u_curr`
diagnostics one timestep late. P045 corrects the timestamp and uses two
sub-bin spectral estimates plus time-domain peak periods.

## Physical Interpretation Boundary

The exact STF null says a perfectly spherical density has no mass-quadrupole
moment in the declared convention. Under a separately assumed quadrupole-only
waveform or power functional, inserting the zero tensor gives a conditional
zero. P3D2 nevertheless defines no gravitational action, field equations,
retarded solution, conserved gravitational source map, or complete radiation
channel. It therefore does not prove physical gravitational silence.

The null also does not force an actual radiating `l=2` mode. Breaking spherical
symmetry can produce a nonzero `l=2` moment, but the existence, dynamics,
conservation, coupling, and radiation of P3D3's proposed deformation remain
pending. Other multipoles or non-gravitational scalar radiation are not ruled
out by a mass-quadrupole identity.

## Terminal Disposition

P3D2 maps its exact radial moment theorem to `C-MOM-003` and its explicit
finite-time core diagnostic to `C-PDE-002`. It remains qualified for the
tautological numerical STF check, exact-frequency wording, unrestricted core
interpretation, physical no-radiation conclusion, forced `l=2` channel,
gravity normalization, absolute scale, and substrate ontology.
