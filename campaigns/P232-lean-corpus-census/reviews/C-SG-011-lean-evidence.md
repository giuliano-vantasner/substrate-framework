# Lean corroboration evidence review: C-SG-011

## Claim Under Review
Accepted claim C-SG-011 (accepted in v0.43.0) receives Lean verification evidence from the
ingested historical corpus. The claim statement itself is not re-reviewed; only the
evidence scope is.

## Sourced Inputs
Read directly: the registry statement of C-SG-011 with its assumptions and exclusions, the
Lean source file(s) below with definitions and theorem statements, the P232 census entry,
and the original campaign adjudication for scope comparison.

## Attachment Reviewed
### `formal/SubstrateFramework/Ingested/Phase15NC_NonlinearChiralSplit.lean`

Entrypoint theorems: `topo_conserved`, `chiral_not_conserved`, `conservation_splits_the_currents`, `chiral_source_present`, `topo_charge_parity_odd`, `parity_actually_flips_charge`, `only_topological_matches`, `nonlinear_parity_violation_survives`.

Reviewed scope: Corroborates the structural split of C-SG-011 in a finite discrete encoding: the topological current is conserved identically (no equation of motion), the naive chiral currents are not conserved and carry a nonzero source, the topological charge flips sign under spatial parity while the conservation/parity-odd combination uniquely selects the topological current. The smooth-field PDE identities, kink charges, and boundary-flux conditions remain the claim's SymPy scope.

### `formal/SubstrateFramework/Ingested/ChargeDiscrimination.lean`

Entrypoint theorems: `channels_cp_conjugate`, `charge_step_counts_one`.

Reviewed scope: Corroborates the kink-charge content of C-SG-011: the two charge-discrimination channels carry opposite integer unit charges (cplus = -cminus, |Q|=1), the point-charge analogue of the claim's unit-kink +1 and parity-image -1 charges; the drive-sign mechanism selecting the channel remains conditional physics input, as in the claim.

### `formal/SubstrateFramework/Ingested/Formalization.lean`

Entrypoint theorems: `halfLineCharge_deriv_eq_neg_phi_t_div_2pi`.

Reviewed scope: Corroborates the topological-current content of C-SG-011: the half-line charge Q(t)=(phi(0,t)-phi_vac-related boundary difference) has derivative exactly -phi_t(0,t)/(2*pi), the j^1=-phi_t/(2*pi) component of the claim's identically conserved topological current.

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
