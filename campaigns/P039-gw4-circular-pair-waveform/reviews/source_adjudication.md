# GW4 Source Adjudication

GW4 is qualified. Its declared equal-point-pair kinematics, corrected
normalized-STF harmonics, and premise-explicit waveform specialization map to
`C-GW-003`. Its hash-pinned executable does not currently finish under NumPy
2.5.1, its quadrupole convention makes its field and power normalization
incorrect, and it does not derive a bound breather binary or physical gravity.

## Source Reproduction

The source reaches four checks and then calls the removed `numpy.trapz` alias.
The current spelling is `numpy.trapezoid`. This version-specific failure is an
implementation defect, not evidence for or against the scientific claim, so
P039 preserves it and uses exact and independently reconstructed oracles.

## Declared Pair and Conserved Moments

For masses `m` at `+/- a(cos(Omega t),sin(Omega t),0)`, the total mass is `2m`
and the center-of-mass dipole is exactly zero. The normalized STF moment
`I_STF=I-delta Tr(I)/3` has derivative norms

`|I_STF''|^2 = 32 m^2 a^4 Omega^4`

and

`|I_STF'''|^2 = 128 m^2 a^4 Omega^6`.

GW4 instead names `Q=3 I_STF`, whose third-derivative norm is nine times larger,
`1152 m^2 a^4 Omega^6`. Its prose headline says the factor is 32 while its
executable later uses 1152. The familiar factor 32 belongs to reduced mass and
pair separation, `32 mu^2 d^4 = 128 m^2 a^4` for `mu=m/2`, `d=2a`; it is not
the triple-normalized norm used by the source.

## Conditional Waveform and Power

For line of sight `n=(sin i,0,cos i)` and transverse frame
`p=(cos i,0,-sin i)`, `v=(0,1,0)`, the declared relation
`h_TT=(A/R) TT(I_STF'')` gives conventional matrix read-offs

`h_plus = -(2 A m a^2 Omega^2/R)(1+cos(i)^2) cos(2 Omega t)`

and

`h_cross = -(4 A m a^2 Omega^2/R)cos(i) sin(2 Omega t)`.

The normalized `C-GW-002` basis coordinates are these values times `sqrt(2)`.
Face-on the two amplitudes are equal and in quadrature; edge-on cross vanishes
and plus has half the face-on amplitude. These are exact consequences of the
declared paths and conditional waveform, not detected physical strains.

Under the particular conditional inputs `A=2G` and `B=1/(32*pi*G)`, the power
is `128 G m^2 a^4 Omega^6/5`. If the source uses `Q=3 I_STF`, covariance requires
waveform coefficient `2G/3` and power coefficient `G/45`. GW4 instead combines
the triple moment with the unscaled coefficient, so its field is three times
and its power nine times the convention-consistent result.

## Physical Scope

The circular paths accelerate, but GW4 supplies no binding force or stress and
no local conservation closure for an isolated binary. The mass is assigned
from the accepted 1+1 breather energy, but no accepted claim embeds that
breather as a compact 3+1 source, proves a stable two-breather orbit, or derives
an orbital law. FS2 and P3D3 are pending source units and their later prose
annotations create no authority. The retarded gravitational waveform and flux
are explicit imports already kept conditional by `C-GW-001`.

## Terminal Disposition

GW4 maps the corrected, premise-explicit circular-pair specialization to
`C-GW-003` and is otherwise qualified. Excluded scope includes a bound
sine-Gordon-breather binary, finite source embedding, binding stress, Kepler
law, physical gravitational action or coupling, retarded dynamics, energy
loss, detector response, astrophysical prediction, and substrate identity.
Durable evidence is the P039 verifier, independent review, failed source
reproduction, and this adjudication.
