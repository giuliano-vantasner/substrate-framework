# Lean corroboration evidence review: C-CHI-001

## Claim Under Review
Accepted claim C-CHI-001 (accepted in v0.54.0) receives Lean verification evidence from the
ingested historical corpus. The claim statement itself is not re-reviewed; only the
evidence scope is.

## Sourced Inputs
Read directly: the registry statement of C-CHI-001 with its assumptions and exclusions, the
Lean source file(s) below with definitions and theorem statements, the P231 census entry,
and the original campaign adjudication for scope comparison.

## Attachment Reviewed
### `formal/SubstrateFramework/Ingested/Phase18Chiral_GoldstoneCount.lean`

Entrypoint theorems: `pion_triplet`, `broken_generators_eq_diagonal`, `vector_unbroken`.

Reviewed scope: Corroborates the three-zero-direction count of C-CHI-001: the SU(2)xSU(2) -> SU(2) diagonal breaking leaves exactly three broken generators (6-3=3, the pion triplet) and the unbroken vector subgroup leaves zero; the general identity dim(G)-dim(H) with the SU(3) octet instance (16-8=8) is checked in the same arithmetic. The O(4) Hessian, tangent-rank, and coordinate-model normalizations remain the claim's SymPy scope; no quantum Goldstone-particle theorem is claimed, matching C-SYM-001/C-CHI-001 exclusions.

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
