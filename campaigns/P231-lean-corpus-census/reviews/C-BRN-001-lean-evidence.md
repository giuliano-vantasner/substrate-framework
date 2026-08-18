# Lean corroboration evidence review: C-BRN-001

## Claim Under Review
Accepted claim C-BRN-001 (accepted in v0.98.0) receives Lean verification evidence from the
ingested historical corpus. The claim statement itself is not re-reviewed; only the
evidence scope is.

## Sourced Inputs
Read directly: the registry statement of C-BRN-001 with its assumptions and exclusions, the
Lean source file(s) below with definitions and theorem statements, the P231 census entry,
and the original campaign adjudication for scope comparison.

## Attachment Reviewed
### `formal/SubstrateFramework/Ingested/Phase30PNKernel.lean`

Entrypoint theorems: `dicke_rate_not_squared`.

Reviewed scope: Corroborates the linear-not-quadratic collective scaling bar of C-BRN-001: the collective occupation factor N (rate ~N) is strictly below the squared scaling N*N for N>=2, the discrete discrimination behind the claim's rate-fraction N-scaling.

### `formal/SubstrateFramework/Ingested/Phase31CMKernel.lean`

Entrypoint theorems: `collective_exceeds_two_body`, `rate_linear_not_squared`.

Reviewed scope: Corroborates the collective-versus-two-body discrimination of C-BRN-001: for N>=2 the collective factor N strictly exceeds the two-body baseline 1 and the coherent scaling is linear (N) rather than quadratic (N^2) - the discrete occupation bar behind the claim's weighted-rate fractions and their N-monotonicity.

### `formal/SubstrateFramework/Ingested/Phase32GBKernel.lean`

Entrypoint theorems: `enh_grows`, `rate_linear_not_squared`.

Reviewed scope: Corroborates the weighted-branching enhancement content of C-BRN-001: with positive subdivision weight w1>=1 the collective numerator w1*N strictly exceeds the single-quantum numerator w1 for N>=2, so the normalized-robust enhancement w(N)*N/w(1) strictly grows with occupation - the discrete core of the claim's partial_N q_B < 0 for q_B=rho/(w*N+rho).

### `formal/SubstrateFramework/Ingested/Phase38MDKernel.lean`

Entrypoint theorems: `branching_antitone`, `branching_mem_unit`, `branching_antitone_not_vacuous`.

Reviewed scope: Corroborates the branching-fraction content of C-BRN-001 exactly: Bgamma w rho N = rho/(w*N+rho) is strictly decreasing in N, lies strictly between zero and one for positive parameters, and the decrease is non-vacuous - the claim's q_B statement with its partial_N derivative.

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
