# Lean corroboration evidence review: C-SG-012

## Claim Under Review
Accepted claim C-SG-012 (accepted in v0.44.0) receives Lean verification evidence from the
ingested historical corpus. The claim statement itself is not re-reviewed; only the
evidence scope is.

## Sourced Inputs
Read directly: the registry statement of C-SG-012 with its assumptions and exclusions, the
Lean source file(s) below with definitions and theorem statements, the P231 census entry,
and the original campaign adjudication for scope comparison.

## Attachment Reviewed
### `formal/SubstrateFramework/Ingested/EnergyFlux.lean`

Entrypoint theorems: `energyFlux_sign_absorbing`, `energyFlux_sign_pumping`, `energyFlux_zero_if_either_zero`, `energyFluxPiston_zero_if_any_zero`.

Reviewed scope: Corroborates the boundary-flux sign structure of C-SG-012's energy balance dE/dt = boundary_flux - Gamma*integral phi_t^2 dx: the boundary power -phi_t(0,t)*phi_x(0,t) is negative (absorbing) when both factors share sign, positive (pumping) when they oppose, and zero when either factor vanishes - including the piston coupling factorization - in the point-value encoding. The stress-tensor identities and null-component balances remain the claim's SymPy scope.

## Scope Match Audit
For each attached theorem the review checked, clause by clause, that the Lean statement
machine-checks content already inside the accepted claim's statement (its exact algebraic
core in the file's declared encoding), that every physics premise the file asserts as
input is recorded in the scope rather than claimed as proved, and that content the
accepted claim explicitly excludes (physical identifications, mechanisms, empirical
readings) is not imported by the attachment. The scope strings above are the reviewed
record of that match.

## Verdict
Accepted as verification_evidence (method: lean): kernel-checked at the pinned toolchain
inside the repository library gate that passed at the ingestion commit; the formal surface
is unchanged by the evidence transaction. The attachment does not alter the claim's four
status axes, its dependencies, or its accepted scope.
