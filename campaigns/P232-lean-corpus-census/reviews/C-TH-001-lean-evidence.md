# Lean corroboration evidence review: C-TH-001

## Claim Under Review
Accepted claim C-TH-001 (accepted in v0.5.0) receives Lean verification evidence from the
ingested historical corpus. The claim statement itself is not re-reviewed; only the
evidence scope is.

## Sourced Inputs
Read directly: the registry statement of C-TH-001 with its assumptions and exclusions, the
Lean source file(s) below with definitions and theorem statements, the P232 census entry,
and the original campaign adjudication for scope comparison.

## Attachment Reviewed
### `formal/SubstrateFramework/Ingested/Phase1Bridge_ThermalGate.lean`

Entrypoint theorems: `thermal_gate_eq_sech_sq`.

Reviewed scope: The Lean entrypoint machine-checks the exact identity core of C-TH-001: with P=1/(1+exp(x)) the two-level gate satisfies 2*P*(1-P)=sech(x/2)^2/2 identically, as a token-level Lean equality over the reals (Complex/Real exponential form exp and cosh), with the two-level occupation premise declared as input exactly as in the claim assumptions.

### `formal/SubstrateFramework/Ingested/Phase28BarrierKernel.lean`

Entrypoint theorems: `gate_le_half`, `gate_eq_half_at_half`.

Reviewed scope: Corroborates the gate-maximum content of C-TH-001: 2*P*(1-P) <= 1/2 for every P with equality exactly at P=1/2, the unique-global-maximum statement of the two-level gate W.

### `formal/SubstrateFramework/Ingested/LandauZener.lean`

Entrypoint theorems: `ionizationWeight_max`, `ionizationWeight_at_half`.

Reviewed scope: Corroborates the gate maximum of C-TH-001: the ionization weight W=2*P*(1-P) satisfies W <= 1/2 with equality exactly at P=1/2 - the unique global maximum of the claim's W=sech(x/2)^2/2 gate at the level-crossing point P(x=0)=1/2.

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
