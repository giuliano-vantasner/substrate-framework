# C-GW-009 Claim Review

## Exact Object

C-GW-009 is an exact kinematic and conditional-TT theorem for a rigidly
rotated axisymmetric STF moment. It fixes the full tensor's repeated
eigenvalue, the perpendicular DC-plus-`2*Omega` decomposition, exact derivative
norms and derivative eigenvalues, the generic-tilt `Omega` plus `2*Omega`
content, and convention-safe conditional readout and power. It explicitly
does not promote a rotating field solution, selected angular speed, physical
gravity, or radiation.

## Sourced Inputs

The review reads v0.132.0; C-MOM-001, C-GW-001/002/008, and the application
inputs C-RMOM-001/002; frozen P181; the TX2 hash and body audit; the new pure
module and tests; all failed representation and schema attempts; the primary
and independent exact routes; and the dependency, consumer, nonduplication,
candidate, compatibility, and graph evidence directly.

## Independence and Sensitivity

The primary route uses the canonical Rodrigues API and accepted conditional
TT functions. The independent route instead constructs the rotation by a
matrix exponential, forms the moment as a dyadic, differentiates with nested
commutators, and projects the transverse plane directly. Both derive the
characteristic polynomials, norms, readouts, power, and tilt formula. Zero
anisotropy, zero speed, wrong quadrupole scale, a genuinely three-eigenvalue
body, and generic tilt all change the relevant verdicts.

## Source Adjudication

TX2's exact orthogonal-conjugation, aligned null, perpendicular component,
and pure-twice-frequency algebra survive with conditions and corrected scope.
Its prose has the opposite `yz` sign from its implementation, carries TX1's
factor-three tensor-name error, mistakes three coordinate diagonals for three
eigenvalues, states a wrong coincidence set, drops eigenvalue multiplicity,
misses the generic-tilt fundamental, and promotes prescribed rotation to an
exact soliton motion and physical radiation without accepted dynamics or
coupling.

## Framework Compatibility

The claim is a compatible extension. The normalized transverse eigenvalue
`q`, convention scale `s`, Cartesian axes, observer basis, coupling and
distance premises, and declared `Omega` remain explicit. Orthogonal invariants
and all zero limits are preserved. The C-RMOM-002 magnitude retains
dimensionless-coordinate-squared units and is not needed to derive any
coefficient.

## Dependency and Consumer Replay

The exact dependency closure passes through C-MOM-001 and C-GW-001/002/008.
C-RMOM-001/002 enter only the TX2 application. The nine-node source graph,
24-check primary route, 10-check independent route, and 89 focused tests pass.
TX3 remains pending and gains no blanket authority for its frame, rank,
Omega-independence, physical-wave, or observation prose. No mutable or source
consumer has a legacy NumPy integration access.

## Competing Concepts

Candidates were frozen before the new body audit. Exact invariant
classification and conditional composition beat coordinate-diagonal
triaxiality structurally, without a numeric comparator. A true rotating field
solution remains a separate candidate requiring action-owned dynamics,
conservation, boundaries, stability, and coupling.

## Verdict

Accept C-GW-009 with verification `symbolic_verified`, review `accepted`,
compatibility `compatible_extension`, and epistemic status `active`. It uses
no `supersedes` relationship. Its physical and dynamical ceilings are part of
the claim, not informal caveats.
