# Lean corroboration evidence review: C-REP-001

## Claim Under Review
Accepted claim C-REP-001 (accepted in v0.73.0) receives Lean verification evidence from the
ingested historical corpus. The claim statement itself is not re-reviewed; only the
evidence scope is.

## Sourced Inputs
Read directly: the registry statement of C-REP-001 with its assumptions and exclusions, the
Lean source file(s) below with definitions and theorem statements, the P232 census entry,
and the original campaign adjudication for scope comparison.

## Attachment Reviewed
### `formal/SubstrateFramework/Ingested/Phase23EW_Sin2ThetaW.lean`

Entrypoint theorems: `tr_T3sq_eq`, `tr_Ysq_eq`, `tr_T3Y_eq`, `tr_Qsq_eq`, `qsq_splits`, `sin2thetaW_eq`, `nontautology_guard`.

Reviewed scope: Corroborates the WM1 fifteen-state table evaluation of C-REP-001 exactly: T_2=2, T_Y=10/3, T_X=0, T_Q=16/3, the split T_Q=T_2+T_Y forced by the vanishing cross term, and the table ratio T_2/T_Q=3/8; the drop-color guard evaluates to 9/28 != 3/8, matching the claim's table-sensitivity discipline. The coordinate-change invariance, coupling-angle equality condition (g_Y^2/g_2^2=3/5), and normalization analysis remain the claim's SymPy scope.

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
