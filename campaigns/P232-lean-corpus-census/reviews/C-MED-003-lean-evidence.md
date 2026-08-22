# Lean corroboration evidence review: C-MED-003

## Claim Under Review
Accepted claim C-MED-003 (accepted in v0.81.0) receives Lean verification evidence from the
ingested historical corpus. The claim statement itself is not re-reviewed; only the
evidence scope is.

## Sourced Inputs
Read directly: the registry statement of C-MED-003 with its assumptions and exclusions, the
Lean source file(s) below with definitions and theorem statements, the P232 census entry,
and the original campaign adjudication for scope comparison.

## Attachment Reviewed
### `formal/SubstrateFramework/Ingested/Phase27MediumKernel.lean`

Entrypoint theorems: `isotope_ratio`, `isotope_ratio_DH`, `isotope_shift_nontrivial`.

Reviewed scope: Corroborates the dimensional scale map of C-MED-003: the on-site gap omega_0=sqrt(mu/lambda) with mu proportional to the site mass gives the isotope ratio omega_0(m_1)/omega_0(m_2)=sqrt(m_2/m_1) (in particular sqrt(2) for the mass-doubling case), a nontrivial shift; the coefficient-column rank, coordinate map, and common-multiplier family remain the claim's SymPy scope.

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
