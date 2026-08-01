# Source adjudication: T1B optical-dilaton bridge

## Decision

T1B is qualified. Its exact 1+1 geometry and conditional drift map are already
accepted as `C-OG-001/002`. P010 adds the exact conditional source-operator
pullback as `C-OG-003`. The source does not derive a matter field equation, the
coupling normalization `kappa=8*pi*G_eff`, a physical identity between sectors,
or a positive 3+1 gravity construction.

## Check-family audit

T1B.1 and T1B.1b reconstruct `Box_g(log(n))=R` for the declared 1+1 metric.
They map to `C-OG-001`. T1B.2a and T1B.2b correctly reject `phi=n` on one
profile, but rejecting one alternative does not prove uniqueness. P004 supplied
the stronger arbitrary-composition proof that the full solution class is
`log(n)+C`; the source checks are supporting evidence for that accepted claim.

T1B.3 substitutes the imported TF relation and expands `log(n)` at weak field.
It maps to the conditional relation in `C-OG-002`. It establishes a formula
between declared variables, not an independent physical identity between the
named programs.

T1B.4a derives the flat-background scalar operator. T1B.4b then substitutes
`phi=-2*Phi/c0^2` and correctly obtains `-Box(phi)=2*Phi''`. P010 strengthens
this limited route: direct substitution into the full curved operator gives
`-Box_g(log(n(Phi)))=2*Phi''` exactly, with no weak-field approximation. That
positive statement is `C-OG-003`.

The remainder of T1B.4b is not a derivation of a sourced equation. After the
operator calculation, the source prose states that “the dilaton EOM sourced by
matter reads” `-Box(phi)=kappa*rho`; no matter action is varied and no equation
linking the checked operator to `rho` appears in the code. Likewise,
`kappa=8*pi*G_eff` is assigned and `kappa/2=4*pi*G_eff` is then simplified. The
algebraic equivalence to `Phi''=(kappa/2)*rho` is valid conditional on the
separate source equation, but neither that dynamics nor its physical coupling
normalization is accepted.

T1B.5a–T1B.5c derive the metric drift, the exact TF index derivative, and the
weak-field acceleration. These map to the stronger exact conditional drift in
`C-OG-002`; the source's leading-order check is not a new dynamics.

T1B.6 supplies a nonzero residual for one declared 3+1 optical metric. It
correctly prevents extending the 1+1 identity, but a counterexample is a scope
guard, not a sourced 3+1 field equation or gravity construction.

## Exact qualification

Accepted mappings are `C-OG-001`, `C-OG-002`, and `C-OG-003`. T1B is terminally
qualified because its verified kinematic content is now represented precisely,
while its matter-source law, `8*pi*G_eff` normalization, cross-program “same
object” language, and positive 3+1 interpretation lack dependency-closed
derivations. Those exclusions do not weaken the accepted exact operator
identity; they delimit what it proves.
