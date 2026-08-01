# GW1 Source Adjudication

GW1 is qualified. Its abstract localized conserved-stress identities and STF
algebra map to `C-MOM-001`. Its explicit momentum example does not satisfy the
local equation it invokes, its binary is externally held without a closed
stress tensor, and its gravitational radiation, TT-coupling, and lowest-order
claims are imported or hard-coded.

## GW1.1 and GW1.2: Monopole

For a localized tensor satisfying `partial_t T^{00}+partial_j T^{j0}=0`, the
integrated `T^{00}` monopole is constant when the surface energy flux vanishes.
The source breathing Gaussian correctly illustrates continuity in one spatial
dimension. The accepted theorem states the general boundary condition. Calling
the zero first or second derivative “no gravitational monopole radiation”
requires a source-to-field and radiation map and is excluded.

## GW1.3 and GW1.4: Dipole and Momentum

The abstract integration by parts is correct only when `T^{i0}=T^{0i}` and the
relevant surface terms vanish: `dot D_i=P_i`, `dot P_i=0`, and `ddot D_i=0`.
GW1's purported explicit realization instead chooses
`pi=g(t) exp(-x^2)` and `Txx=S(t) exp(-x^2)` independently. The compact stress
has zero integrated divergence, while the current has
`dot P=sqrt(pi)*g'(t)`; local momentum conservation therefore forces `g'=0`.
The source never enforces that equation, so those checks validate the abstract
surface identity but not their displayed current/stress pair.

## GW1.5: Binary Second Moment

The point-mass moment algebra and center-of-mass cancellation are exact, and a
circular coordinate path has nonzero second moment derivatives. GW1 declares
an external mechanism holding the orbit and supplies no binding-field stress,
so its particle source alone is not the isolated locally conserved tensor used
earlier. A nonzero kinematic `ddot I` is not a gravitational radiation oracle.
P036 instead verifies `ddot I_ij=2 integral T^{ij}` on a fully conserved
translating three-dimensional Gaussian and an independent inertial-particle
system.

## GW1.6: STF Reduction

The tensor `3I-delta*Tr(I)` is symmetric and traceless. It is exactly three
times the normalized STF tensor `I-delta*Tr(I)/3`; both conventions are encoded
and tested. The claim that only it couples to a TT graviton is a forward import
from an unaccepted gravitational field sector and is not promoted.

## GW1.7 and Guard

The `lowest_radiating_ell` function is a two-case lookup returning the desired
zero and two; it derives neither value. The one-particle versus two-particle
acceleration guard correctly demonstrates center-of-mass cancellation for the
declared paths but not a radiation theorem. Conservation can suppress lower
moment derivatives; it neither proves a quadrupole field exists nor that it is
nonzero in a wave zone.

## Terminal Disposition

GW1 maps its boundary- and symmetry-qualified moment ladder to `C-MOM-001` and
is otherwise qualified. Excluded scope includes monopole/dipole radiation
statements, a lowest radiating multipole, linearized gravity, a retarded Green
function, TT coupling or polarizations, waveform or power, the `1+1` contrast,
and substrate identity. Durable evidence is the P036 verifier, independent
review, source reproduction, and this adjudication.
