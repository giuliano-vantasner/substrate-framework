# QB4 Source Adjudication

QB4 is qualified. Exact conditional scaled-STF waveform, power, and
polarization-rank formulas survive, including the nonaxisymmetric z-direction
readout and the axisymmetric null. The inherited source, reported power,
twice-frequency dominance, elliptical two-mode label, graviton count, and
physical-radiation narrative do not.

## Reproduction and NumPy Compatibility

The hash-pinned source exits with status zero and `ALL 5 CHECKS PASS` in 10.5
seconds under Python 3.12.2, NumPy 2.5.1, SciPy 1.18.0, and SymPy 1.14.0. It
reports core frequency 0.965311, averaged-mode frequency 1.0877, average
dimensionless power `1.3703e4`, and one generic-frame instantaneous readout
`(0.3124,2.8702)`.

The source already handles the NumPy API change correctly: it selects current
`np.trapezoid` and uses `np.trapz` only as a legacy fallback. P055 adds no new
quadrature path. The first reproduction command incorrectly treated the queue
path as framework-relative; the preserved repair resolves it against the
pinned `/home/dan/substrate` root, verifies checkout commit `6d1f4e0`, and
checks the exact inventory hash before execution.

## Inherited Source and Moment

QB4 recomputes QB3's amplitude-three single-harmonic core and averaged,
super-threshold, finite-wall l=2 mode. P054 already established that this is
not the accepted finite-box background, a regular localized mode, or a
Floquet solution. QB4 again evaluates a finite `b=0.8` field assembled from a
first-order perturbation. Its energy density omits
`|grad_Omega u|^2/(2r^2)` and its field lacks the second-order corrections
required for a self-consistent nonlinear deformation.

The returned tensor is explicitly the triple moment
`Q=3I-delta*trace(I)`. The literal finite-b array has numerical rank two in
its diagonal STF coefficient plane, with second-to-first singular ratio
0.00736; its generic TT array has ratio 0.00528. Those measurements describe
only the qualified array. They do not promote its dynamics, and QB4's own
classifier never computes either rank.

## Periodicity and Twice-Frequency Power

QB4 calls `2*pi/omega` a common period while its second input frequency has
`omega_2/omega=1.1267678549`. The ratio is not integral, the nonlinear moment
contains mixed frequencies, and the tensor at the two window endpoints differs
by 9.61 percent in Frobenius norm. Its rFFT therefore differentiates a forced
discontinuous periodic extension, not the physical quasiperiodic series.

The displayed equality between the `Qzz` line amplitude times
`(2*omega)^3` and the spectral derivative is true to `4.70e-15`, but both
sides use the same FFT coefficient and the derivative is defined by that
multiplication. It is representation self-consistency, not an independent
derivative oracle. The nominal `2*omega` bin supplies only 4.17 percent of the
third-derivative norm on the source's own interior slice, far below the frozen
50-percent dominance gate. The printed total is therefore not validated as
power dominated by that line.

## Quadrupole Convention

Under C-GW-001, the normalized moment `I_STF` uses waveform coefficient `2G`
and power coefficient `G/5`. For `Q_s=sI_STF`, the same conditional field and
power require

`h_TT=(2G/(sR))*TT(Q_s'')`,

`P=G*|Q_s'''|^2/(5s^2)`.

QB4 applies `G/5` directly to its triple tensor, overstating any conditional
power from the granted array by exactly nine. Its `1.3703e4` would become
`1.5225e3` after this convention repair alone, but neither value is promoted
because the source and derivative premises fail independently. The source
also prints raw projected `Qddot` coordinates rather than a distance-scaled
waveform.

## Polarization and Rank

For a triple real-m2 tensor

`Q=[[q_c,q_s,0],[q_s,-q_c,0],[0,0,0]]`,

the exact natural-z conventional readouts are conditionally
`h_plus R/G=2q_c''/3` and `h_cross R/G=2q_s''/3`, while
`P/G=2[(q_c''')^2+(q_s''')^2]/45`. A nonzero cosine component does radiate
conditionally along z, whereas the axisymmetric tensor is TT-null along its
symmetry axis. Those structural contrasts survive.

QB4 evaluates plus and cross at one representative time. Two nonzero numbers
at one time do not establish temporal rank, phase difference, or an ellipse;
they also depend on the transverse basis. If `Q(t)=q(t)T` with fixed `T`, both
coordinates are proportional to `q''`, their temporal rank is one, and a
spin-two frame rotation sets cross to zero. A genuine rank-two natural-z
comparison needs two nonproportional real-m2 traces. Equal-amplitude
quadrature traces yield the exact circular conditional limit, but accepted
scalar dynamics supplies no such pair.

The source's axisymmetric check uses a frame aligned with the projected z
axis, so zero cross is a correct adapted-frame linear-polarization result. It
does not make a nonzero cross coordinate in another source/frame an invariant
mode or graviton counter. The frozen-tensor guard is also a valid zero-
derivative limit but is insensitive to every load-bearing source,
periodicity, convention, and polarization defect above.

## Terminal Disposition

QB4 maps to exact conditional claim `C-GW-008`. It remains qualified for the
QB3 eigenmode and finite deformation, the reported power and amplitudes,
twice-frequency dominance, periodic spectral derivative, physical waveform,
elliptical or rank-two radiation from the accepted source, gravity, flux,
graviton count, detector observable, backreaction, absolute scale, particle
identity, and substrate realization.
