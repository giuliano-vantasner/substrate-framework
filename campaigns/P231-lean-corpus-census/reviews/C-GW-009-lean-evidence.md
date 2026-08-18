# Lean corroboration evidence review: C-GW-009

## Claim Under Review
Accepted claim C-GW-009 (accepted in v0.133.0) receives Lean verification evidence from the
ingested historical corpus. The claim statement itself is not re-reviewed; only the
evidence scope is.

## Sourced Inputs
Read directly: the registry statement of C-GW-009 with its assumptions and exclusions, the
Lean source file(s) below with definitions and theorem statements, the P231 census entry,
and the original campaign adjudication for scope comparison.

## Attachment Reviewed
### `formal/SubstrateFramework/Ingested/Phase40TX_RotatingTorus.lean`

Entrypoint theorems: `quad_traceless`, `triaxial_generic`, `circular_on_axis`, `perp_radiates`, `axis_null`, `polarization_ratio_free`.

Reviewed scope: Corroborates the rigid-axis-rotation content of C-GW-009: the rotated quadrupole stays traceless (legitimate STF source) with generically pairwise-distinct Cartesian entries, the on-axis transverse readout has equal plus/cross amplitudes (circular polarization, amplitude identity (6*Omega^2*q)^2 summing to 36*Omega^4*q^2), the perpendicular line of sight radiates, and the axial-rotation null cases vanish; the full time-dependent component formulas, derivative norms, and waveform conventions remain the claim's SymPy scope.

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
