# Lean corroboration evidence review: C-U1-001

## Claim Under Review
Accepted claim C-U1-001 (accepted in v0.14.0) receives Lean verification evidence from the
ingested historical corpus. The claim statement itself is not re-reviewed; only the
evidence scope is.

## Sourced Inputs
Read directly: the registry statement of C-U1-001 with its assumptions and exclusions, the
Lean source file(s) below with definitions and theorem statements, the P232 census entry,
and the original campaign adjudication for scope comparison.

## Attachment Reviewed
### `formal/SubstrateFramework/Ingested/Phase3EM_U1Current.lean`

Entrypoint theorems: `u1_divergence_identity`, `u1_conservation`, `u1_phase_breaking_witness`.

Reviewed scope: The Lean theorems machine-check the algebraic core of C-U1-001 in a single-point complex encoding: the off-shell current divergence identity i*(psi_conj*Box(psi)-psi*Box(psi_conj)) evaluated on substituted equations of motion Box(psi)=-a*psi, Box(psi_conj)=-b*psi_conj gives i*(b-a)*|psi|^2; equal real coefficients (a=b) give exact conservation u1_conservation=0; unequal coefficients give a nonzero divergence witness. The PDE/Noether derivation itself remains the claim's SymPy scope; the Lean side is the point-identity corroboration.

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
