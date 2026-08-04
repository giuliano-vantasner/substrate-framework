# P135 EM5 source adjudication

EM5 reproduces all eleven checks, but its headline is refuted. The script
combines the fermionic Schwinger-model Feynman numerator with bosonic
scalar-QED language, constructs transversality before checking it, drops an
inverse momentum factor when naming a local Maxwell term, and introduces a
bare propagator kernel while claiming none exists. The surviving positive
object is a different, explicitly conditional theorem for a massive complex
scalar loop.

## Surviving exact surface

For nonzero Euclidean momentum, `P=I-q*q.T/q^2` is idempotent and transverse,
and it annihilates longitudinal vectors. These are kinematic identities. They
do not prove that a loop generates `P`, nor that its image is a propagating
physical mode in 1+1 dimensions.

Separately declare `N` identical complex scalars in Euclidean two dimensions,
with `m>0`, charge magnitude `e>0`, operator `-D^2+m^2`, a shift-invariant
gauge-preserving regulator, scalar bubble and seagull, and
`Gamma^(2)=A_mu*Pi_mu_nu*A_nu/2`. For `Q=q_E^2>0`, exact reduction gives

`Pi_mu_nu=(Q*delta_mu_nu-q_mu*q_nu)*Pi_scalar(Q)=P_mu_nu*Pi_hat(Q)`

and

`Pi_hat(Q)=N*e^2/pi*[atanh(z)/z-1]`,
`z=sqrt(Q)/sqrt(Q+4*m^2)`.

The scalar bubble contracts to `+2*N*e^2*q_nu*I_tad` and the seagull to its
negative under the declared shift identity. Their cancellation derives the
Ward identity. Omitting or sign-flipping the seagull produces a nonzero
residual.

At low momentum,

`Pi_hat=N*e^2*Q/(12*pi*m^2)-N*e^2*Q^2/(120*pi*m^4)+...`.

Thus the leading local coefficient is `N*e^2/(48*pi*m^2)` for
`F_mu_nu*F_mu_nu`, or `N*e^2/(24*pi*m^2)` for the single `F_01^2` component.
An independent constant-field proper-time derivation gives the same result.
The fixed-positive-`Q` massless scalar limit diverges in the infrared, while
the heavy-mass limit vanishes.

## Rejected source readings

EM5's integrand proportional to `x*(1-x)` has the finite massless limit
`e^2/pi`; that is the fermion-shaped Schwinger expression, not the scalar
numerator `(1-2*x)^2`. The executable contains no determinant, bubble,
seagull, loop momentum, or regulator. Its Ward test only contracts a tensor
that it already defined to be transverse.

The exact identity is `A*P*A=F_01^2/Q`. Check 6 acknowledges that identity and
then drops `/Q`, turning a nonlocal kernel into a purported local Maxwell
coefficient. In two dimensions the source's bare `e^2` coefficient also has
mass dimension two, whereas a coefficient multiplying local `F^2` must be
dimensionless. The correct massive result contains `e^2/m^2`.

Checks 5, 8, and 11 dress a denominator `Q-Pi_hat`, but the `Q` term is a bare
kinetic kernel excluded by the source premise. A pole additionally requires a
declared analytic continuation, gauge fixing, sign, and field normalization.
Under `A'=lambda*A`, `e'=e/lambda`, and `kappa'=kappa/lambda^2`, the invariant
combination is `e^2/kappa`; `e^2` alone cannot define a physical mass.

Finally, `e->0` removes this loop contribution but does not force `F=0` when no
action constrains the connection. A nonflat connection remains allowed. A
local Maxwell field in 1+1 dimensions has zero massless photon polarizations,
so the claimed propagating photon, dispersion, and 3+1 lift do not follow.

## Decision

C-VAC-001 is accepted only as a conditional imported quantum-field theorem. It
does not quantize C-U1-001's classical field, identify its charge with
electric charge, generate a substrate gauge sector, fix a bare Maxwell
coefficient, or establish a photon or pole. It depends only on C-GAU-001's
connection convention and retains that claim's ontology and no-dynamics
ceilings. EM5 is qualified through its projector identities and the corrected
massive scalar-loop theorem; its central constructive-closure claim is
rejected.
