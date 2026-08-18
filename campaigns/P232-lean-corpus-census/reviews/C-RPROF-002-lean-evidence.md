# Lean corroboration evidence review: C-RPROF-002

## Claim Under Review
Accepted claim C-RPROF-002 (accepted in v0.89.0) receives Lean verification evidence from the
ingested historical corpus. The claim statement itself is not re-reviewed; only the
evidence scope is.

## Sourced Inputs
Read directly: the registry statement of C-RPROF-002 with its assumptions and exclusions, the
Lean source file(s) below with definitions and theorem statements, the P232 census entry,
and the original campaign adjudication for scope comparison.

## Attachment Reviewed
### `formal/SubstrateFramework/Ingested/Phase29YieldKernel.lean`

Entrypoint theorems: `binding_hierarchy`, `classical_overbinds_B2`, `classical_overbinds_B4`.

Reviewed scope: Corroborates the stationary-branch per-degree ordering of C-RPROF-002 in exact rational arithmetic: the accepted per-degree coefficients (1.2314..., 1.2081..., 1.1365...) give the strict hierarchy b4 < b2 < b1 and positive classical binding at B=2 and B=4 on the declared stationary branches; the float64 route comparison, refinement, and collocation cross-check remain the claim's numeric-evidence scope.

### `formal/SubstrateFramework/Ingested/Phase40TX_RotatingTorus.lean`

Entrypoint theorems: `fission_bound`.

Reviewed scope: Corroborates the fission-threshold comparison against the accepted per-degree stationary-branch coefficients of C-RPROF-002: the declared fission bound 1.208 is strictly below the accepted B=2 per-degree value (rounded 1.2317 in the Lean bound), the ordering the claim's resolution-bounded evidence establishes.

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
