# Lean corroboration evidence review: C-GSK-001

## Claim Under Review
Accepted claim C-GSK-001 (accepted in v0.157.0) receives Lean verification evidence from the
ingested historical corpus. The claim statement itself is not re-reviewed; only the
evidence scope is.

## Sourced Inputs
Read directly: the registry statement of C-GSK-001 with its assumptions and exclusions, the
Lean source file(s) below with definitions and theorem statements, the P231 census entry,
and the original campaign adjudication for scope comparison.

## Attachment Reviewed
### `formal/SubstrateFramework/Ingested/Phase40TX_RotatingTorus.lean`

Entrypoint theorems: `tail_exponent_one`.

Reviewed scope: Corroborates the massless power-tail exponent bookkeeping of C-GSK-001 at degree one: the decaying-tail exponent -(1+sqrt(1+8*B))/2 evaluates to -2 at B=1, the r^-2 tail of the declared reduced model.

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
