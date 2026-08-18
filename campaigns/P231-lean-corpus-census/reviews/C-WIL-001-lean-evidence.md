# Lean corroboration evidence review: C-WIL-001

## Claim Under Review
Accepted claim C-WIL-001 (accepted in v0.25.0) receives Lean verification evidence from the
ingested historical corpus. The claim statement itself is not re-reviewed; only the
evidence scope is.

## Sourced Inputs
Read directly: the registry statement of C-WIL-001 with its assumptions and exclusions, the
Lean source file(s) below with definitions and theorem statements, the P231 census entry,
and the original campaign adjudication for scope comparison.

## Attachment Reviewed
### `formal/SubstrateFramework/Ingested/Phase10CF_Z3CenterConfinement.lean`

Entrypoint theorems: `area_law_unbounded`, `perimeter_law_bounded`, `deconfined_sigma_zero`.

Reviewed scope: Corroborates the separation-dependence contrast inside C-WIL-001: for every positive sigma the linear area-law potential sigma*R is unbounded in R (for every bound C there is R with sigma*R>C), while the perimeter-law potential is bounded and the sigma=0 area law is bounded below by any constant - the order-parameter contrast between the two loop laws whose extraction identities C-WIL-001 states. The loop-expectation extraction itself and the center-algebra selection remain excluded, as in the claim.

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
