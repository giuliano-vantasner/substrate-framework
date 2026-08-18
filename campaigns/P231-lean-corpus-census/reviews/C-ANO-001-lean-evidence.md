# Lean corroboration evidence review: C-ANO-001

## Claim Under Review
Accepted claim C-ANO-001 (accepted in v0.127.0) receives Lean verification evidence from the
ingested historical corpus. The claim statement itself is not re-reviewed; only the
evidence scope is.

## Sourced Inputs
Read directly: the registry statement of C-ANO-001 with its assumptions and exclusions, the
Lean source file(s) below with definitions and theorem statements, the P231 census entry,
and the original campaign adjudication for scope comparison.

## Attachment Reviewed
### `formal/SubstrateFramework/Ingested/Phase9SM_AnomalyCancellation.lean`

Entrypoint theorems: `anomaly_U1_cubed`, `anomaly_grav_U1`, `anomaly_SU2_sq_U1`, `anomaly_SU3_sq_U1`, `witten_even`, `all_anomalies_cancel`, `nontautology_guard`.

Reviewed scope: Corroborates the SM-generation evaluation half of C-ANO-001: over the declared five-row left-handed content (Q_L,u_R^c,d_R^c,L,e_R^c) with the displayed standard hypercharges, the four charge-dependent local anomaly sums U(1)^3, grav^2*U(1), [SU(2)]^2*U(1), [SU(3)]^2*U(1) all evaluate to zero and the fundamental SU(2) doublet count is even (four); dropping Q_L breaks grav^2*U(1) (guard), matching the claim's row-sensitivity analysis. The generic coefficient formulas, affine zero-set classification, and charge-conjugation action remain the claim's SymPy scope.

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
