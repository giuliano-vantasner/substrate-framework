# Lean corroboration evidence review: C-TOP-001

## Claim Under Review
Accepted claim C-TOP-001 (accepted in v0.17.0) receives Lean verification evidence from the
ingested historical corpus. The claim statement itself is not re-reviewed; only the
evidence scope is.

## Sourced Inputs
Read directly: the registry statement of C-TOP-001 with its assumptions and exclusions, the
Lean source file(s) below with definitions and theorem statements, the P232 census entry,
and the original campaign adjudication for scope comparison.

## Attachment Reviewed
### `formal/SubstrateFramework/Ingested/Phase4Strong_FRSpinStat.lean`

Entrypoint theorems: `skyrmion_odd_is_fermion`, `skyrmion_even_is_boson`, `skyrmion_parity_charge_conjugate`.

Reviewed scope: Corroborates the winding-parity character content of C-TOP-001: the map B |-> (-1)^|B| takes value -1 on every odd integer and +1 on every even integer, and is even under charge conjugation B |-> -B. The Skyrmion/baryon/fermion identification remains conditional interpretation explicitly excluded by C-TOP-001; only the mathematical character values are machine-checked.

### `formal/SubstrateFramework/Ingested/Phase20ME_HalfQuantumOrder2.lean`

Entrypoint theorems: `halfQuantum_add_self`, `halfQuantum_ne_zero`, `halfQuantum_addOrderOf`.

Reviewed scope: Corroborates the order-two winding-class arithmetic adjacent to C-TOP-001: the nontrivial winding class has additive order exactly two (1+1=0, 1!=0), the setting for the parity character (1)^w of C-TOP-001; the anyon third-root contrast (order three, value != -1) is a supporting distinctness check.

### `formal/SubstrateFramework/Ingested/Phase46EL_LeptonConstraint.lean`

Entrypoint theorems: `parity_hom`, `parity_eq_ite`, `parity_zero`, `parity_one`, `parity_two`.

Reviewed scope: Corroborates the homomorphism statement of C-TOP-001 exactly: parity(m+n)=parity(m)*parity(n) for all integers, with values +1 on even winding (0,2) and -1 on odd winding (1) - the monoid-homomorphism property the claim states for p(w)=(-1)^w.

### `formal/SubstrateFramework/Ingested/ChargeDiscrimination.lean`

Entrypoint theorems: `both_channels_parity_minus_one`, `reflectedCharge_parity_is_minus_one`.

Reviewed scope: Corroborates the odd-winding parity value of C-TOP-001: both discrimination channels carry fermion parity -1 (odd unit charge), for either drive sign.

### `formal/SubstrateFramework/Ingested/Formalization.lean`

Entrypoint theorems: `fermionParity_sq_eq_one`, `fermionParity_zero`, `fermionParity_one`, `fermionParity_neg_one`.

Reviewed scope: Corroborates the parity character of C-TOP-001: fermionParity squares to +1 with values +1 at 0 and -1 at +/-1 - the sign character on winding charge.

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
