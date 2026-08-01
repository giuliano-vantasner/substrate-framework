# Source adjudication: EL2 winding labels and charged-lepton composite

## Decision

EL2 is qualified. Its integer winding-sign algebra supports `C-TOP-001`, and
its complex-field current is duplicate evidence for conditional `C-U1-001`.
It does not derive fermionic statistics, baryon number for the claimed
composite, a unit-normalized or electric charge, 3+1 stability, a Standard Model
slot, or an electron identification.

## Check-family audit

EL2.1 and EL2.2 calculate the exact character `p(w)=(-1)^w`. The source tests a
finite integer grid; P019 supplies a residue-class proof for all integers and an
independent quotient derivation. Adding even winding preserves the label and
adding odd winding flips it. Calling label `-1` “fermion” and `+1` “boson” is
not a consequence of the group character; it requires a separately proved
spin-statistics representation that no accepted claim supplies.

EL2.3 differentiates the standard hedgehog antiderivative correctly and checks
one full sweep and one constant profile. That does not define the proposed
composite's target map or its boundary data. A non-full symbolic sweep is not
shown, and the constant example cannot prove the composite has degree zero.

EL2.4 correctly shows that a map whose third target coordinate is functionally
dependent has zero Jacobian determinant. The source declares rather than derives
that its composite has this rank. Its prose alternates between a union of a
one-dimensional path and a two-dimensional disc and a path times a disc; the
latter can be three-dimensional. No canonical composite field is implemented
for the Jacobian test.

EL2.5 and EL2.6 rederive `C-U1-001`'s conditional current and real-field zero.
They neither construct the claimed anchor-condensate composite nor normalize
its charge. Under the accepted declared sech profile, `Q=4*A^2*omega/eta`
varies with amplitude and frequency; nonzero is not “exactly one unit,” and an
internal U1 charge is not automatically electric charge.

EL2.7 solves the declared Derrick scaling derivative but misclassifies the
stationary point. Writing `E_pot=-P` with `P>0`, the source has
`E(lambda)=lambda*E_grad-lambda^3*P`; at its root,
`E''=-6*P*lambda<0`, and the energy tends to minus infinity as lambda grows.
The point is a maximum, not a stable minimum. A fixed-charge Q-ball variation
would require the correct constrained energy functional and its additional
scaling term.

EL2.8 correctly notes monotonicity for the separately declared positive-potential
real-field expression. It does not convert the negative-potential maximum into
a stability proof.

EL2.9 provides one numerical shooting solution, but it inherits the incorrect
stability oracle. The script checks tolerance sensitivity of the shooting
parameter, not domain, mesh, energy error, an independent method, or solver
success before consuming output. Its near-exact virial relation establishes a
stationary profile for the declared truncated problem, not nonlinear or
fixed-charge stability and not the existence of the claimed composite.

EL2.10 selects a row from a table built with the desired target tuple. Its
inputs are not established: parity label is not fermion statistics, the
composite baryon number is not derived, the internal charge is not electric,
and absence of an SU(3) identifier is not proof of a colour-singlet
representation. Relabeling the matching row would preserve the check.

EL2.11 is a functioning forbidden-mass-literal guard. Avoiding an electron mass
input cannot establish that the constructed object exists or is an electron.

## Exact qualification

Accepted content is limited to the winding character, its even-dressing
invariance, the odd-dressing counterexample, and the already-conditional U1
current. The source's baryonless fermion, unit charge, 3D stability, charged
lepton, and electron conclusions remain unsupported. The failed stability
interpretation is preserved as reusable attempt evidence rather than presented
as the positive result.
