# Lean corroboration evidence review: C-OVL-002

## Claim Under Review
Accepted claim C-OVL-002 (accepted in v0.65.0) receives Lean verification evidence from the
ingested historical corpus. The claim statement itself is not re-reviewed; only the
evidence scope is.

## Sourced Inputs
Read directly: the registry statement of C-OVL-002 with its assumptions and exclusions, the
Lean source file(s) below with definitions and theorem statements, the P232 census entry,
and the original campaign adjudication for scope comparison.

## Attachment Reviewed
### `formal/SubstrateFramework/Ingested/Phase20MH_OverlapHierarchy.lean`

Entrypoint theorems: `hierarchy_strictMono`, `hierarchy_orders_of_magnitude`, `flat_condensate_equal`, `flat_not_strict`, `capstone`.

Reviewed scope: Corroborates the translated-localization hierarchy content of C-OVL-002 in the geometric-overlap specialization: for a core-localized profile and a tower localizing at growing separation with fixed ratio q in (0,1), the overlaps y0*q^n are strictly decreasing with unbounded generation ratio (orders-of-magnitude hierarchy), while a flat condensate (q=1) gives exactly equal overlaps with no hierarchy. The exact sech-profile expectation formulas, hypergeometric evaluation, and equal-rate a*exp(-alpha*a) class remain the claim's SymPy scope.

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
