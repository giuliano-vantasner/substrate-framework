# Lean corroboration evidence review: C-GW-002

## Claim Under Review
Accepted claim C-GW-002 (accepted in v0.34.0) receives Lean verification evidence from the
ingested historical corpus. The claim statement itself is not re-reviewed; only the
evidence scope is.

## Sourced Inputs
Read directly: the registry statement of C-GW-002 with its assumptions and exclusions, the
Lean source file(s) below with definitions and theorem statements, the P232 census entry,
and the original campaign adjudication for scope comparison.

## Attachment Reviewed
### `formal/SubstrateFramework/Ingested/Phase16QB_TwoPolarizations.lean`

Entrypoint theorems: `triaxial_two_polarizations`, `at_most_two_polarizations`, `two_polarizations_iff_cross`, `both_excite_plus`.

Reviewed scope: Corroborates the two-dimensionality content of C-GW-002: the generic (triaxial) source excites both TT basis polarizations and no source exceeds the two-dimensional TT image. The explicit projector, basis tensors, and frame-rotation phases remain the claim's SymPy scope; no physical graviton count or helicity statement is imported, matching the claim's exclusions.

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
