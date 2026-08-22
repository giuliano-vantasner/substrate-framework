# Lean corroboration evidence review: C-MIX-002

## Claim Under Review
Accepted claim C-MIX-002 (accepted in v0.31.0) receives Lean verification evidence from the
ingested historical corpus. The claim statement itself is not re-reviewed; only the
evidence scope is.

## Sourced Inputs
Read directly: the registry statement of C-MIX-002 with its assumptions and exclusions, the
Lean source file(s) below with definitions and theorem statements, the P232 census entry,
and the original campaign adjudication for scope comparison.

## Attachment Reviewed
### `formal/SubstrateFramework/Ingested/Phase11Flavor_CPPhaseCount.lean`

Entrypoint theorems: `cpPhases_two`, `cpPhases_three`, `mixingAngles_two`, `mixingAngles_three`, `removablePhases_three`, `param_count_identity`, `cp_requires_three_generations`, `cp_vanishes_below_three`.

Reviewed scope: Corroborates the KM counting arithmetic of C-MIX-002: the N*(N-1)/2 real-orthogonal angle count, the (N-1)*(N-2)/2 irreducible complex-phase count with values zero at N=2 and one at N=3, the 2N-1 effective rephasing orbit dimension (removablePhases N=2N-1), and the decomposition N^2 = angles + removable + phases; CP-violating phases require N>=3. The unitary stabilizer-dimension derivation, quartet invariants, and rotation-chart evaluation remain the claim's SymPy scope; no CKM or quark identification is made, matching the claim's exclusions.

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
