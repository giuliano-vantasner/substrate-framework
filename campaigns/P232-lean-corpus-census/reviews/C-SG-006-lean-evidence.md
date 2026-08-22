# Lean corroboration evidence review: C-SG-006

## Claim Under Review
Accepted claim C-SG-006 (accepted in v0.11.0) receives Lean verification evidence from the
ingested historical corpus. The claim statement itself is not re-reviewed; only the
evidence scope is.

## Sourced Inputs
Read directly: the registry statement of C-SG-006 with its assumptions and exclusions, the
Lean source file(s) below with definitions and theorem statements, the P232 census entry,
and the original campaign adjudication for scope comparison.

## Attachment Reviewed
### `formal/SubstrateFramework/Ingested/ActionQuantum.lean`

Entrypoint theorems: `hbar_eff_strict_anti`, `hbar_eff_not_constant`, `action_over_hbar_eff`.

Reviewed scope: Corroborates the secant-scale content of C-SG-006: the surrogate hbar_eff(w)=E(w)/w is strictly decreasing on the family and the canonical-to-secant ratio Pi=J/H=w*arccos(w)/sqrt(1-w^2) - the claim's displayed ratio.

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
