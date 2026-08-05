# GK3D1 Source Adjudication

GK3D1 executes cleanly and all nineteen source checks pass, but that tally does
not validate the full headline. The source defines
`Pi_up=(q^2*g_up-q_up*q_up.T)*Pi_s` and then contracts it, so its Ward check is
a tensor identity rather than a derivation from the loop numerator and
regulator. Its `2**(Dval//2)` helper is valid at integer Clifford endpoints but
is not an analytic spinor-trace prescription in continued dimension. Its
Gamma-function pole is dimensional or analytic regularization, not a
regulator-free result.

The scoped positive content is qualified through C-VAC-002: after separately
declaring a charged Dirac action, fermionic loop, shift-invariant regulator,
tensor convention, integration dimension, and integer spinor trace, the exact
master has the source normalization. The D=2 `n_gamma=2` massless endpoint at
nonzero spacelike momentum yields `q^2*Pi2=e^2/pi`. The fixed-`n_gamma=4`,
`d=4-2 epsilon` endpoint has pole residue `-e^2/(12*pi^2)` in the source tensor
convention. MS-bar subtraction leaves
`e^2*log(M2/mu2)/(12*pi^2)+c_fin`, with `c_fin` arbitrary, and the finite
below-threshold subtraction begins
`-e^2/(2*pi^2)*(w/30+w^2/280+w^3/1890)` with radius four.

GK3D1 does not derive a physical charged excitation, scalar/fermion identity,
preferred dimension, physical three-polarization photon, gauge group, bare
coefficient, finite matching condition, total kinetic normalization, observed
coupling, or substrate dimensional lift. GK3D2 through GK3D6 must be audited on
their own premises; their later prose cannot retroactively close GK3D1.

The source disposition is therefore `qualified`, with C-VAC-002 as its sole
accepted claim. Every per-check limitation is recorded in
`evidence/check-adjudication.yaml`.
