# TX2 Source Adjudication

TX2 is qualified through C-GW-009 and its accepted static dependencies. The
positive result is an exact prescribed rigid-axis moment path and conditional
TT theorem, not a genuinely triaxial full moment or a solved rotating source.

## Reproduction and Compatibility

The source remains pinned at SHA-256
`7dd6852af20ef060ffa2f17950219fb79d7943e50fc64235a75a10d098f7d3b7`.
P177's exact-hash native graph replay already established clean exit and the
seven-check terminal tally, so P181 does not rerun it ceremonially. Its AST
contains seven check calls and one assertion node. TX2 imports only SymPy and
has no NumPy or quadrature compatibility surface; no version event affects a
scientific verdict.

## Tensor Convention and Components

TX2 inherits TX1's normalized `I_STF=diag(q,q,-2q)` but calls it `Q`. Its
quoted axial ratio `-0.338851663` is the normalized value; accepted triple
`Q=3*I_STF` has axial ratio `-1.016554986815505`. C-GW-009 keeps an explicit
scale `s`, so this naming error cannot enter a waveform or power coefficient.

For TX2's implemented right-handed x rotation, the exact off-diagonal entry
is `+3q sin(Omega t) cos(Omega t)`. The docstring and result prose print the
opposite sign. The sign changes a frame phase but not the invariant norm; it
is nevertheless a source inconsistency and is not silently normalized away.

## Eigenstructure and Triaxiality

Orthogonal conjugation preserves the exact characteristic polynomial
`(lambda-sq)^2(lambda+2sq)`. The full moment therefore remains axisymmetric
about its rotating eigenvector at every phase. Three distinct Cartesian
diagonal entries in a frame with nonzero `yz` do not become three principal
values. TX2.3 samples those entries once and never diagonalizes the tensor.
TX2.5 calls `eigenvals().keys()`, discarding the repeated multiplicity that
would directly refute the headline.

The source's stated diagonal-coincidence values are also wrong. The three
pairwise coincidences occur at `sin^2(Omega t)=0`, `1/2`, and `1`, not at
`1/3`, `2/3`, and `1`. The exact positive replacement recovers the rotating
symmetry axis and classifies the full tensor as axisymmetric. Its second and
third derivatives, by contrast, have principal values `0, plus/minus
6sqOmega^2` and `0, plus/minus 12sqOmega^3`; the radiation-driving derivative
is genuinely three-eigenvalue when `q Omega` is nonzero.

## Harmonics, Tilt, and Conditional TT Algebra

The exactly perpendicular path is DC plus a pure `2*Omega` harmonic. Its
second- and third-derivative Frobenius norms are `72s^2q^2Omega^4` and
`288s^2q^2Omega^6`. A half-period identity alone would not exclude higher
even harmonics, so P181 derives the component decomposition directly.

A generic constant tilt has both fundamental and twice-frequency components:
the xz/yz entries carry `Omega`, while the diagonal difference and xy entry
carry `2*Omega`. Its exact third-derivative norm is
`18s^2q^2Omega^6 sin^2(beta)[cos^2(beta)+16sin^2(beta)]`. It rises monotonically
with `sin^2(beta)` and reaches the pure-`2*Omega` perpendicular maximum. TX2's
general-tilt guard checks only the aligned and perpendicular endpoints and
does not establish its broader prose.

Under C-GW-001/002/008's separately declared premises, perpendicular rotation
has convention-independent conditional power `288Gq^2Omega^6/5`. Along the
rotation axis its conventional readouts are equal-amplitude quadrature,
`-12GqOmega^2 cos(2Omega t)/r_obs` and
`-12GqOmega^2 sin(2Omega t)/r_obs`. Those are exact conditional identities,
not a derived gravity theory or detector waveform.

## Dynamical and Physical Ceiling

A static rotational degeneracy and tangent zero mode do not make an arbitrary
time-dependent rotation an exact full-field solution. TX2 supplies no kinetic
collective-coordinate action, inertia tensor, angular momentum, field
residual, local conserved stress, boundary data, stability analysis, or
dynamical selection of `Omega`. Its perpendicular axis is a special pure-line
limit, not the generic tilted orientation. C-RMOM-001/002 supply a conditional
reduced stationary branch, not the source's “solved B=2 Skyrmion” or an
absolute physical scale.

The aligned and zero-`q` quadrupole nulls cannot establish physical
nonradiation at all multipole orders. B1's rank-two null is exact; P180 kept
the declared B4 null resolution-bounded, so TX2's “exact B4” wording is also
unaccepted.

## Terminal Disposition

Qualify TX2 through C-MOM-001, C-GW-001/002/008, C-RMOM-001/002, and new
C-GW-009. Preserve as unaccepted its full-tensor triaxiality, printed `yz`
sign, diagonal coincidence set, tensor label, exact-full-field motion,
generic-pure-line reading, no-free-parameter claim, exact B4 null, selected
`Omega`, stability, local conservation, gravity, physical waveform,
radiation, absolute scale, state identity, observation, and substrate
realization. TX3 remains pending.
