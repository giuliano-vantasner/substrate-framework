# Lean corroboration evidence review: C-WZW-002

## Claim Under Review
Accepted claim C-WZW-002 (accepted in v0.51.0) receives Lean verification evidence from the
ingested historical corpus. The claim statement itself is not re-reviewed; only the
evidence scope is.

## Sourced Inputs
Read directly: the registry statement of C-WZW-002 with its assumptions and exclusions, the
Lean source file(s) below with definitions and theorem statements, the P231 census entry,
and the original campaign adjudication for scope comparison.

## Attachment Reviewed
### `formal/SubstrateFramework/Ingested/Phase17WZW_LevelWinding.lean`

Entrypoint theorems: `wzw_level_integer`, `integer_level_single_valued`, `half_integer_fails_single_valued`, `integrality_is_a_real_cut`.

Reviewed scope: Corroborates the level-integrality cut of C-WZW-002: the coefficient is admissible (single-valued phase on the two fillings) exactly for integer level values - integer levels are single-valued, the half-integer level fails, and the cut is strict. The Puttmann-Rigas generator map, the -480*pi^3 period normalization, and the degree computation remain the claim's SymPy scope; the identification of the level with N_c or baryon winding stays excluded, matching the claim.

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
