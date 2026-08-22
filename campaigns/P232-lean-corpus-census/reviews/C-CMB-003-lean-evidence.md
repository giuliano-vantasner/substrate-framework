# Lean corroboration evidence review: C-CMB-003

## Claim Under Review
Accepted claim C-CMB-003 (accepted in v0.143.0) receives Lean verification evidence from the
ingested historical corpus. The claim statement itself is not re-reviewed; only the
evidence scope is.

## Sourced Inputs
Read directly: the registry statement of C-CMB-003 with its assumptions and exclusions, the
Lean source file(s) below with definitions and theorem statements, the P232 census entry,
and the original campaign adjudication for scope comparison.

## Attachment Reviewed
### `formal/SubstrateFramework/Ingested/Phase37WNKernel.lean`

Entrypoint theorems: `weight_pos`, `crossover`, `growth_limb`, `halving_tail`, `crossover_not_vacuous`, `both_limbs_realized`.

Reviewed scope: Corroborates the consecutive-ratio crossover of C-CMB-003 for the factorial-one weight family: cross-multiplied, w(n+1) < w(n) iff S < n+1 - weights grow below the crossover and strictly decrease above it, both limbs realized (growth limb, halving tail beyond 2S) and every weight positive; this is the exact log-concavity/mode content of the claim's p_S(n)=exp(-S)*S^n/n! family in division-free arithmetic. The generating function, factorial moments, and tail-exponential bounds remain the claim's SymPy scope.

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
