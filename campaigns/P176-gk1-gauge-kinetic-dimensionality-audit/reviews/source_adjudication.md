# P176 GK1 Source Adjudication

GK1 exits cleanly and all eleven implemented checks pass. The tally validates
standard fundamental SU2 and SU3 trace matrices, a source-defined shared 2×2
projector, exact two-form component counts, one narrow power-count equation, a
normalized Riesz expression, and six documentation strings. It does not
validate the whole result prose.

## Surviving exact surface

In natural units with a canonically normalized gauge potential, dimensionless
action and minimal coupling give `[A]=(D-2)/2`, `[g]=(4-D)/2`, `[F_A]=D/2`,
and `[Π̂]=2` for the coefficient of a dimensionless transverse projector in
the quadratic momentum kernel. Therefore the special scale-free ansatz
`Π̂=g² c` with nonzero dimensionless `c` is homogeneous if and only if `D=2`.

The statement is convention sensitive. For the connection field `B=gA`,
`F_B=gF_A`, so `[B]=1`, `[F_B]=2`, and a coefficient multiplying `F_B²` has
dimension `D-4`. The exact density map is
`κ_A F_A²/4=(κ_A/g²)F_B²/4`. Generator scaling also transports the coupling:
`T'=ρT`, `g'=g/ρ`, `T(R)'=ρ²T(R)`, and `g'²T(R)'=g²T(R)`.

These ledgers are promoted as C-DIM-009. They naturally compose with the
accepted two-dimensional scalar-loop claims without changing them.

## Source corrections

GK1 upgrades the narrow pure-coupling result into a universal polarization
no-go. That step fails. Once an independent mass scale is supplied,
`g²M^(D-2)` has dimension two in every `D`. In four dimensions, `Q f(Q/M²)`
also has dimension two for any dimensionless `f`; constant, rational threshold,
and logarithmic examples all satisfy the same homogeneity. Dynamics, regulator,
subtraction, and matching—not dimensions—select a form factor and coefficient.

The predecessor scripts and GK1 share the fermion-shaped `u(1-u)` integrand,
not the accepted complex-scalar `(1-2u)²` bubble-seagull theorem. Their finite
massless value, propagating-boson language, computed unique coupling, and
physical sector readings remain rejected by C-VAC-001 and C-NVP-001/002.
GK1.5 divides out its own trace value rather than taking a convention-preserving
group limit. GK1.8 shows only that a four-dimensional power exponent is zero.
GK1.9 correctly shows its normalized Riesz expression cannot identify an
absent `g_eff`, while leaving source and kinetic amplitudes free. GK1.11 is a
useful documentation regression, not scientific authority.

## Decision

Accept C-DIM-009 as a distinct exact compatible extension. Qualify GK1 through
C-DIM-009 and existing C-REP-002, C-LIE-001, C-VAC-001, C-NVP-001/002, and
C-KRN-001/002. Do not promote a universal constant-polarization obstruction,
unique logarithm, four-dimensional loop, bare or total kinetic coefficient,
propagating gauge particle, physical U1/SU2/SU3 sector, observation, or
substrate mechanism. GK3D1–GK3D4 remain pending and must establish their own
loop, matching, and physical premises.
