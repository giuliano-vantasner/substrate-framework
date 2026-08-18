# Lean corroboration evidence review: C-SG-016

## Claim Under Review
Accepted claim C-SG-016 (accepted in v0.78.0) receives Lean verification evidence from the
ingested historical corpus. The claim statement itself is not re-reviewed; only the
evidence scope is.

## Sourced Inputs
Read directly: the registry statement of C-SG-016 with its assumptions and exclusions, the
Lean source file(s) below with definitions and theorem statements, the P232 census entry,
and the original campaign adjudication for scope comparison.

## Attachment Reviewed
### `formal/SubstrateFramework/Ingested/Phase26LifetimeKernel.lean`

Entrypoint theorems: `lifetime_strictAntiOn`, `lifetime_unbounded_as_lossless`.

Reviewed scope: Corroborates the 1/Gamma scale content of C-SG-016: the declared lifetime scale tau(Gamma)=1/Gamma is strictly decreasing in the loss rate and diverges as Gamma -> 0+, the monotonicity/divergence behaviour of the energy e-fold scale that C-SG-016 identifies as the tangent/asymptotic time; the exact damping form factor D(omega), the reduced e-fold time log(theta0/asin(sin(theta0)/e))/Gamma, and the finite-amplitude PDE comparison remain the claim's scope.

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
