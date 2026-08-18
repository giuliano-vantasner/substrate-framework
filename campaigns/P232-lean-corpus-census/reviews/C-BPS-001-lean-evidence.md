# Lean corroboration evidence review: C-BPS-001

## Claim Under Review
Accepted claim C-BPS-001 (accepted in v0.91.0) receives Lean verification evidence from the
ingested historical corpus. The claim statement itself is not re-reviewed; only the
evidence scope is.

## Sourced Inputs
Read directly: the registry statement of C-BPS-001 with its assumptions and exclusions, the
Lean source file(s) below with definitions and theorem statements, the P232 census entry,
and the original campaign adjudication for scope comparison.

## Attachment Reviewed
### `formal/SubstrateFramework/Ingested/Phase34KIKernel.lean`

Entrypoint theorems: `derivedScale_flow_invariant`, `eps_flow_scales`, `eps_flow_nontrivial`.

Reviewed scope: Corroborates the positive-parameter-family invariance of C-BPS-001 as adjudicated in P172: the flow (F,e,l,m) |-> (F,e,t*l,t*m) leaves the derived scale F/e exactly invariant while the near-BPS parameter eps=F/(e*l*m) rescales by 1/t^2, so every eps value is compatible with the same derived content - the underdetermination theorem's algebraic core.

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
