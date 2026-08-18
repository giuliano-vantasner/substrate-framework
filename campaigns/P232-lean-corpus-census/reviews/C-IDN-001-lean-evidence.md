# Lean corroboration evidence review: C-IDN-001

## Claim Under Review
Accepted claim C-IDN-001 (accepted in v0.59.0) receives Lean verification evidence from the
ingested historical corpus. The claim statement itself is not re-reviewed; only the
evidence scope is.

## Sourced Inputs
Read directly: the registry statement of C-IDN-001 with its assumptions and exclusions, the
Lean source file(s) below with definitions and theorem statements, the P232 census entry,
and the original campaign adjudication for scope comparison.

## Attachment Reviewed
### `formal/SubstrateFramework/Ingested/Phase21AS_OverDetermination.lean`

Entrypoint theorems: `odV1_underdetermined`, `odV2_overdetermined`, `the_flip`, `fab_not_over`, `fab_fails_on_rank_not_constraints`.

Reviewed scope: Corroborates the identifiability verdict logic of C-IDN-001 on the supplied OD records: over-determination is the rank-equals-unknowns / zero-nullity criterion (every log-scale coordinate identified), the OD-v1 system with one-dimensional nullspace is under-determined, OD-v2 is over-determined, and the fab guard shows that more constraints than unknowns does not imply over-determination (rank, not row count, decides) - exactly the claim's "can hold without global uniqueness or more rows than columns" guard. The ratio-chain rows, log transformation, and interval intersection machinery remain the claim's scope.

### `formal/SubstrateFramework/Ingested/Phase22AS_BetaPinnedScale.lean`

Entrypoint theorems: `odV2_overdetermined`, `odV3_overdetermined`, `the_second_reduction`, `pin_odV2_is_odV3`, `reduction_independent_of_pinned_value`, `AS7_pin_gives_same_reduction`, `refloat_not_reduced`.

Reviewed scope: Corroborates the conditioning content of C-IDN-001: pinning one coordinate (beta^2) removes exactly one unknown, the reduced system stays over-determined, the reduction is independent of the pinned value (any admissible pin gives the same reduced record), and re-floating the coordinate restores the larger unknown count. The affine left-null compatibility relations remain governed by C-LIN-001/C-IDN-001 as adjudicated in P080.

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
