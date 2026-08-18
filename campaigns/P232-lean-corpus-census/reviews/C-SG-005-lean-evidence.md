# Lean corroboration evidence review: C-SG-005

## Claim Under Review
Accepted claim C-SG-005 (accepted in v0.9.0) receives Lean verification evidence from the
ingested historical corpus. The claim statement itself is not re-reviewed; only the
evidence scope is.

## Sourced Inputs
Read directly: the registry statement of C-SG-005 with its assumptions and exclusions, the
Lean source file(s) below with definitions and theorem statements, the P232 census entry,
and the original campaign adjudication for scope comparison.

## Attachment Reviewed
### `formal/SubstrateFramework/Ingested/Gates.lean`

Entrypoint theorems: `gate1_energy_budget`.

Reviewed scope: Corroborates the threshold partition of C-SG-005: E_breather + DeltaE = 2*E_kink with positive DeltaE forces E_breather < 2*E_kink strictly below the two-kink threshold, the claim's exact partition E+Delta=16 with 0<Delta.

### `formal/SubstrateFramework/Ingested/Energy.lean`

Entrypoint theorems: `binding_gap_nonneg`, `binding_gap_pos`, `breather_plus_gap_eq_pair`, `E_breather_le_pair`.

Reviewed scope: Corroborates the threshold-gap content of C-SG-005: the deficit Delta=16-E satisfies 0<Delta<16 on the family, E+Delta=16 exactly, and E<=16 with equality only at the endpoints - the claim's strict partition.

### `formal/SubstrateFramework/Ingested/Formalization.lean`

Entrypoint theorems: `binding_gap_nonneg`, `binding_gap_pos`, `breather_plus_gap_eq_pair`, `E_breather_le_pair`, `E_breather_pos_lt_pair`.

Reviewed scope: Corroborates the threshold-gap content of C-SG-005 in the superset ledger: Delta=16-E with 0<Delta<16, E+Delta=16, E<16 on the open family.

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
