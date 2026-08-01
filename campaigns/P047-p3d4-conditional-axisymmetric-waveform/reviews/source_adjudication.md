# P3D4 Source Adjudication

P3D4 is qualified. Its exact axisymmetric polarization geometry maps to the
general arbitrary-axis result proposed as `C-GW-005`, and P047 supplies a
separately corrected finite-time conditional application proposed as
`C-GW-006`. The source's product-field quadrupole, normalization, derivative
convergence, frequency, physical-radiation, and residual-payment claims do not
earn their advertised scope.

## Reproduction and NumPy Compatibility

The hash-pinned source exits with status zero and `ALL 4 CHECKS PASS` in 14.5
seconds under NumPy 2.5.1. Its compatibility branch selects
`numpy.trapezoid` before the removed legacy `numpy.trapz` name. It reports
core frequency 0.8901, constructed-Q frequency 1.8326, band-limited mean power
`1.1723e5`, transverse raw plus amplitude 396.45, exact zero cross and axial
TT projection, and zero power for a frozen trace. Reproduction establishes
only that these computations execute as written.

## Inherited Field-Construction Failure

P3D4 rebuilds P3D3's `u=P*(1+a*P2)` construction rather than importing the
accepted regular mode. `C-PDE-003` gives its exact nonzero full-field residual

`sin(P*(1+a*Y))-(1+a*Y)*sin(P)+6*a*P*Y/r^2`,

and its l=2 coefficient is nonregular at the origin when `P(0,t)` is nonzero.
The P3D4 energy density again contains radial gradients but omits the
nonradial angular-gradient contribution. Consequently its `Q(t)` is a moment
of a prescribed invalid construction, not a self-consistent field solution.
P3D4 cannot import P3D3's rejected premises merely because its own checks run.

## STF Convention and Power Error

The source helper returns `Q=3*I-delta*Tr(I)`, the triple-normalized tensor.
For `Q=diag(-q/2,-q/2,q)`, its third-derivative norm is
`Q'''_ij Q'''_ij=3*q'''^2/2`. `C-GW-001` requires waveform coefficient
`2*G/3` and power coefficient `G/45` for this convention, so the conditional
power is `G*q'''^2/30`. P3D4 instead uses `G/5` directly on the triple tensor,
giving `3*G*q'''^2/10`, exactly nine times too large. Even an otherwise valid
trace would not support its reported normalization.

The source also calls its raw TT-projected `Qddot` coordinate a waveform but
does not multiply it by the convention-correct `2*G/(3*R)` coefficient. Its
reported 396.45 is therefore not a dimensionless strain or an absolute
waveform amplitude. `G_eff=1` and `c0=1` are declarations without an accepted
gravity action, source equation, retarded solution, radiation zone, or unit
map.

## Exact Arbitrary-Axis Geometry

The geometric core is exact after separating it from the invalid source. For
unit symmetry axis `e`, define the normalized tensor
`S=alpha*(e*e^T-delta/3)`. Its norm is `2*alpha^2/3`. For unit line of sight
`n`, with inclination cosine `e.n`, choose the natural meridian vector from
the projection of `e` into the transverse plane and its oriented companion.
The normalized plus coordinate is `alpha*sin(i)^2/sqrt(2)`, the conventional
matrix readout is `alpha*sin(i)^2/2`, cross is zero, and the complete TT tensor
vanishes along the symmetry axis. Scaling the tensor by three and the
waveform coefficient by one third leaves the conditional waveform and power
unchanged. P047 verifies this for arbitrary non-Cartesian axes and by a
separate direct-projector derivation.

## Derivative and Refinement Audit

P3D4 says `N->2N` and `dt->dt/2`, but it does not refine the field mesh or
integrator timestep. The same `dr=0.05`, `dt=0.02` evolution is sampled every
other step and then every step. That tests sampling density only. Its third
derivative is obtained after a cubic detrend and FFT cutoff
`W_BAND=5*omega_p`, where `omega_p` is measured from the observed trace. No
cutoff variation, endpoint treatment study, alternate estimator, spatial
mesh, integrator timestep, domain, boundary, or independent evolution tests
the claimed power.

P047 instead differentiates the accepted regular `C-PDE-004` coefficient
`q(t)=Qzz(t)/epsilon`. It reruns the declared finite-time IVP on meshes
`dr=0.2,0.1,0.05`, with a baseline `dt=0.04`, dense sample interval 0.16, and
interprets only `5<=t<=35`. The reported route downsamples to interval 0.32
and uses a nine-point degree-five local polynomial; a quintic interpolating
B-spline and an independently derived seven-point finite difference are
separate estimators.

Successive second-derivative mesh disagreements are 2.576 and 0.651 percent;
third-derivative disagreements are 4.297 and 1.099 percent. Timestep halving
changes them by 0.566 and 1.029 percent, domain extension by below `1e-11`
percent, and sampling halving by 4.132 and 4.755 percent. Local-polynomial and
spline differences are 4.507 and 5.013 percent. Half amplitude gives exact
half derivatives and quarter power, while zero amplitude preserves an exact
zero moment trace.

The baseline coefficient has RMS values 13.7837762 for `q''` and 19.1706587
for `q'''`. Under the conditional triple convention, the edge-on conventional
coefficient has RMS
`h_plus*R/(G*epsilon)=6.8918881`, cross is zero, and the interpreted-window
mean is `P/(G*epsilon^2)=12.2504719`. These are dimensionless, linearized,
finite-time coefficient traces. They are not an absolute waveform or power.

## Frequency and FS3 Claims

P3D4's constructed-Q peak at 1.8326 is one FFT bin above twice core bin 17;
the comparison tolerance spans two bins. More importantly, that spectrum
belongs to the rejected multiplicative construction and its selected
band-limit. P047 preregistered no frequency comparator and accepts no
frequency or periodicity statement for the corrected regular mode. The exact
linear polarization and axis null are structural properties of every
axisymmetric STF tensor; reproducing those properties does not validate the
source dynamics or establish that FS3 is a leading physical approximation.

The phrases “pays the point-lump residual” and “pays the declared transverse
profile residual” have no mathematical discharge condition. The source does
not derive a controlled limit connecting its invalid finite construction to
FS3, quantify an approximation error, or build a conserved 3+1 source. Those
residual-payment statements are rejected rather than carried as debt.

## Frozen-Trace Guard

The source's frozen nonzero trace has zero third derivative and hence zero
conditional power. This is a valid negative control, independently reproduced
with the canonical derivative machinery. It is a generic consequence of the
derivative formula and does not validate the evolving source, gravity law, or
power coefficient.

## Terminal Disposition

P3D4 maps exact arbitrary-axis linear-polarization and symmetry-null geometry
to `C-GW-005` and the corrected endpoint-qualified application of the accepted
regular l=2 coefficient trace to `C-GW-006`. It remains qualified for its
inherited nonregular field ansatz, omitted angular energy, factor-nine power
normalization, missing waveform prefactor, resampling-only convergence claim,
carrier-selected FFT filter, exact/clean twice-frequency language, FS3
leading-order and residual-payment claims, declared physical gravity,
absolute waveform/power interpretation, and substrate ontology. QB3 and QB4
may import only the accepted conditional tensor conventions and must not
inherit these rejected premises.
