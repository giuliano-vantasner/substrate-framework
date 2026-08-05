# C-VAC-004 Claim Review

## Claim Under Review

C-VAC-004 is an exact conditional composition of C-RGE-003's two-length
one-loop scale map and C-VAC-003's affine matter-induced kinetic family. It
keeps independent length-energy conversions and `Z_ref`, proves cancellation
of consistently paired conversions without assuming they are equal, and
exposes the positive inverse kinetic coordinate only on an explicitly imposed
zero-matching branch. Its role is to make scale matching importable without
promoting physical labels or source-specific parameter selections.

## Sourced Inputs

The review reads v0.138.0, C-RGE-003, C-VAC-003, the C-IDN-002 and C-DIM-009
ceilings, P187's frozen proposal and formulas, the hash-pinned GK3D3 source,
all append-only attempts, canonical module and tests, primary verifier,
independent rederivation, impact report, and eight-node consumer inventory.
The source's physical scale labels, erased boundary, parameter-free coupling,
logarithm uniqueness, and sampled perturbativity claims remain outside the
claim delta.

## Independence

The independent review imports neither `kinetic_scale_matching` nor the
`scale_transmutation` and `vacuum_polarization` parent APIs. It reconstructs
the inverse-length maps, affine derivative, one-loop exponential, paired
lengths, rank nullspace, conditional inverse, and counterfamilies directly in
raw SymPy. Only the shared check ledger and compatibility auditor are reused.

## Verification Status

The maximum verdict is symbolic verified. The primary path passes 31 runtime
checks and the independent raw-SymPy path passes 20. All integrals and quantum
coefficients belong to the already accepted parent claims; P187's new
obligations are tractable exact substitutions, ratios, logarithms, affine
composition, and rank algebra. No unresolved integral, numerical tolerance,
or fitted comparator enters the result.

## Sensitivity and Counterexamples

Fixed-length mutations of either conversion change the log and total, while
paired conversion reparameterizations at fixed energies leave them unchanged.
Changing `Z_ref` changes the total without changing the scale data or slope.
Common length rescaling preserves the ratio and total but shifts both absolute
energies. Unpaired orientation and soliton-coefficient mutations change the
log. Zero matter leaves only `Z_ref` and makes the zero branch noninvertible.
Power zero is a constant, and `log(y)^2`, `1/log(y)`, and rational functions of
`log(y)` are exact counterexamples to source uniqueness. Invalid signs and
hidden floats are rejected.

## Framework Compatibility

The claim is a compatible extension. It changes neither C-RGE-003's
orientation and identifiability ceiling nor C-VAC-003's loop coefficient and
affine boundary. It introduces no new physical field, scale, group,
representation, threshold, comparator, or numerical parameter. The conversion
and matching maps are explicit conditional inputs, and the general family
precedes every specialization.

## Dependency and Consumer Replay

The direct dependencies are C-RGE-003 and C-VAC-003, and their complete
accepted closure is recorded in `evidence/dependency-audit.yaml`. Code impact
is LOW with no affected indexed process. Source governance risk is MEDIUM:
GK3D1 and GK3D2 are already-qualified narrative-cycle predecessors, GK3D4–6
are forward consumers, and EL2/HE5 are transitive. GK3D5's immutable current-
first lazy legacy NumPy fallback is compatibility evidence, not a scientific
failure; every other inventoried node has no trapezoidal surface.

## Competing Candidate Audit

Six candidates were registered before source-body inspection. The generic
conversion map and consistent paired composition win on invariant
compatibility, explicit provenance, boundary preservation, parameter economy,
rescaling covariance, and exact mutation sensitivity. Equal conversions,
physical soliton labels, an erased boundary, and functional uniqueness require
extra assumptions or are false. No numerical comparison selected the result.

## Four-Axis Decision

The four axes support promotion at the exact conditional scope.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: no supersedes edge; composes C-RGE-003 and C-VAC-003 and corrects GK3D3 through qualification

## Promotion Transaction

Promotion adds C-VAC-004 to `governance/claims.yaml`, preserves the pure module
and 51 focused tests, moves the proposal immutably into `campaigns/`, records
GK3D3 as qualified in `migration/dispositions.yaml`, regenerates rather than
edits `migration/source-claims.yaml`, creates v0.139.0, renders generated docs
and accepted memory, and runs primary, independent, source-graph, targeted,
repository, memory, generation, full-suite, and diff gates in separate process
invocations.

## Continuation if Not Accepted

If any dependency, mutation, consumer, or governance gate fails, P187 remains
active and repairs that layer without weakening the claim. A failed physical
scale identification is not accepted as a substitute deliverable.

## Done Gate

Accept only after the positive importable composition, individual source
adjudication, complete dependency and consumer replay, synchronized canonical
records, and empty debt ledger all pass. Until then the review recommendation
does not itself promote the claim.

## Cross-References

See P187, GK3D3, C-RGE-003, C-IDN-002, C-DIM-009, C-VAC-003,
`kinetic_scale_matching.py`, `test_kinetic_scale_matching.py`, the primary and
independent verifiers, source adjudication, impact analysis, and consumer
inventory.
