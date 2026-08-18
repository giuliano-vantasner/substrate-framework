# Lean corroboration evidence review: C-SG-009

## Claim Under Review
Accepted claim C-SG-009 (accepted in v0.36.0) receives Lean verification evidence from the
ingested historical corpus. The claim statement itself is not re-reviewed; only the
evidence scope is.

## Sourced Inputs
Read directly: the registry statement of C-SG-009 with its assumptions and exclusions, the
Lean source file(s) below with definitions and theorem statements, the P231 census entry,
and the original campaign adjudication for scope comparison.

## Attachment Reviewed
### `formal/SubstrateFramework/Ingested/Phase13FS_HarmonicDoubling.lean`

Entrypoint theorems: `quadratic_source_radiates_at_2omega`, `quadratic_harmonics_all_even`, `quadratic_harmonics_even`, `quadratic_not_fundamental`, `quadratic_at_least_doubled`, `lowest_parity_matches_power_even`, `lowest_parity_matches_power_odd`.

Reviewed scope: Corroborates the doubling/even-harmonic core of C-SG-009: a source density quadratic in a field oscillating at omega has its AC content on the even harmonic line, lowest order 2*omega (frequency doubling), while a linear source sits on the odd line with lowest order omega; the parity split and the 2*omega base frequency are machine-checked as the discrete harmonic-index arithmetic. The exact asinh second-moment formula, its range, and the 1+1 moment functional remain the claim's SymPy scope; no three-dimensional source or gravitational coupling is derived, matching the claim's exclusions.

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
