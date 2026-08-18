# Lean corroboration evidence review: C-SG-017

## Claim Under Review
Accepted claim C-SG-017 (accepted in v0.81.0) receives Lean verification evidence from the
ingested historical corpus. The claim statement itself is not re-reviewed; only the
evidence scope is.

## Sourced Inputs
Read directly: the registry statement of C-SG-017 with its assumptions and exclusions, the
Lean source file(s) below with definitions and theorem statements, the P232 census entry,
and the original campaign adjudication for scope comparison.

## Attachment Reviewed
### `formal/SubstrateFramework/Ingested/Phase27MediumKernel.lean`

Entrypoint theorems: `kappaSq_pos_iff`, `gapless_no_breather`, `above_gap_no_breather`, `breather_exists_example`, `breather_predicate_has_content`.

Reviewed scope: Corroborates the sub-gap tail content of C-SG-017: the squared tail-decay rate kappa^2=(omega_0^2-omega_b^2)/c^2 is positive exactly for sub-gap frequencies omega_b<omega_0, the declared localization predicate is satisfiable and fails for the gapless and at-or-above-gap cases, and the predicate has genuine content (satisfiable and falsifiable instances). The physical-coordinate pullback solution, energy/action scales, and dE/dJ=omega*omega_0 remain the claim's SymPy scope; the claim's exclusion (no proof that every gapless medium lacks every localized periodic solution) is respected - the Lean predicate is the declared sub-gap model.

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
