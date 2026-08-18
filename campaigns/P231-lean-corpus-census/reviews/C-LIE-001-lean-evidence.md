# Lean corroboration evidence review: C-LIE-001

## Claim Under Review
Accepted claim C-LIE-001 (accepted in v0.21.0) receives Lean verification evidence from the
ingested historical corpus. The claim statement itself is not re-reviewed; only the
evidence scope is.

## Sourced Inputs
Read directly: the registry statement of C-LIE-001 with its assumptions and exclusions, the
Lean source file(s) below with definitions and theorem statements, the P231 census entry,
and the original campaign adjudication for scope comparison.

## Attachment Reviewed
### `formal/SubstrateFramework/Ingested/Phase8QCD_SU3GaugeFacts.lean`

Entrypoint theorems: `dynkin_fundamental`, `casimir_adjoint_three`, `casimir_fundamental_value`, `casimir_dynkin_consistency_general`.

Reviewed scope: Corroborates the exact representation invariants of C-LIE-001 through their group-theoretic identities rather than the explicit Gell-Mann matrices: T_F=1/2, C_F=4/3, C_A=3 at N=3, the general-N formulas adjointDim N=N^2-1, casimirF N=(N^2-1)/(2N), casimirAdj N=N, the normalization identity C_2(F)*N=T_F*(N^2-1), and the structural contrast 8 != 3 with the N=2 guard. No physical gauge-sector identification is made, matching the claim's exclusion.

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
