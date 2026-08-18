# Lean corroboration evidence review: C-GW-005

## Claim Under Review
Accepted claim C-GW-005 (accepted in v0.42.0) receives Lean verification evidence from the
ingested historical corpus. The claim statement itself is not re-reviewed; only the
evidence scope is.

## Sourced Inputs
Read directly: the registry statement of C-GW-005 with its assumptions and exclusions, the
Lean source file(s) below with definitions and theorem statements, the P231 census entry,
and the original campaign adjudication for scope comparison.

## Attachment Reviewed
### `formal/SubstrateFramework/Ingested/Phase16QB_TwoPolarizations.lean`

Entrypoint theorems: `axisym_one_polarization`, `axisym_no_cross`, `only_triaxial_excites_cross`.

Reviewed scope: Corroborates the axisymmetric-waveform core of C-GW-005: an axisymmetric STF source excites exactly one TT polarization with zero cross component for a generic line of sight. The exact tensor projection coordinates, waveform coefficients, and power remain the claim's SymPy scope.

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
