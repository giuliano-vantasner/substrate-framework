# Lean corroboration evidence review: C-KRN-001

## Claim Under Review
Accepted claim C-KRN-001 (accepted in v0.58.0) receives Lean verification evidence from the
ingested historical corpus. The claim statement itself is not re-reviewed; only the
evidence scope is.

## Sourced Inputs
Read directly: the registry statement of C-KRN-001 with its assumptions and exclusions, the
Lean source file(s) below with definitions and theorem statements, the P232 census entry,
and the original campaign adjudication for scope comparison.

## Attachment Reviewed
### `formal/SubstrateFramework/Ingested/Phase19_D3S_LocalityImpliesS1.lean`

Entrypoint theorems: `analytic_even_symbol_power_two_is_s1`, `s1_symbol_power_is_two`, `fractional_symbol_power_one_not_s1`, `analytic_distinguishes_local_from_fractional`, `even_symbol_power_is_integer_order`.

Reviewed scope: Corroborates the symbol-order correspondence of C-KRN-001: an even integer Fourier-symbol power |k|^(2k) corresponds to Riesz order k - in particular the local Laplacian is exactly order s=1 with symbol power |k|^2 - while a fractional symbol power is not a local Laplacian order, and the correspondence is proved for every even power. The kernel Gamma-function evaluation, coefficient bookkeeping, and the d=3,s=1 Coulomb specialization remain the claim's SymPy scope.

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
