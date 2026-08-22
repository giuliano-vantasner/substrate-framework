# Lean corroboration evidence review: C-CHR-001

## Claim Under Review
Accepted claim C-CHR-001 (accepted in v0.60.0) receives Lean verification evidence from the
ingested historical corpus. The claim statement itself is not re-reviewed; only the
evidence scope is.

## Sourced Inputs
Read directly: the registry statement of C-CHR-001 with its assumptions and exclusions, the
Lean source file(s) below with definitions and theorem statements, the P232 census entry,
and the original campaign adjudication for scope comparison.

## Attachment Reviewed
### `formal/SubstrateFramework/Ingested/Phase19_OM1_Z2Character.lean`

Entrypoint theorems: `chiF_generator`, `chiF_double`, `chiF_nontrivial`, `chiF_is_unique_nontrivial`.

Reviewed scope: Corroborates the cyclic sign-character content of C-CHR-001 at n=2: the nontrivial character takes value -1 on the generator and +1 on its square (homomorphism law), is distinct from the trivial character, and is the unique nontrivial character of the cyclic group of order two. The general-n character classification remains the claim's SymPy scope.

### `formal/SubstrateFramework/Ingested/Phase20ME_HalfQuantumOrder2.lean`

Entrypoint theorems: `chiHQ_generator`, `chiHQ_double`, `chiHQ_nontrivial`.

Reviewed scope: Corroborates the n=2 instance of C-CHR-001 in the half-quantum-vortex encoding: the ZMod-2 parity character takes -1 on the generator, +1 on its square, and is nontrivial.

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
