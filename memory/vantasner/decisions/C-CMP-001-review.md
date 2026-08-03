---
description: Independent review of C-CMP-001 exact paired-loss and cycle-factor composition
author: vantasner-review
created: '2026-08-08T05:00:00Z'
updated: '2026-08-08T05:00:00Z'
tags:
- substrate-framework
- claim-review
- factor-composition
- loss-boundary
category: decisions
confidence: established
status: archived
---
# C-CMP-001 Review

## Claim Under Review

C-CMP-001 states an exact conditional theorem for multiplying C-RES-001's
common-loss nonnegative-product magnitude by C-DYN-001's nominal or actual
finite-window cycle factors. It quantifies over a nonempty finite family of
real nonzero detunings, real nonnegative coupling products with at least one
positive member, positive loss and natural frequency, and the explicitly
declared window convention. It governs the cancellation, strict loss
monotonicity, one-sided limits, cutoff extensions, stationary classification,
dimensions, scaling, and non-rate ceiling of the product.

## Sourced Inputs

The review reads v0.95.0, C-RES-001, C-DYN-001, C-RG-002, C-TH-001,
C-SPN-002, the frozen P116 contract, all nine attempts, the canonical module
and tests, the primary verifier, the independent verifier, and every P116
audit. CM2 is pinned at SHA-256
`c75fee880740765d3ef3e32634bf05360fd9789e46bd579fd07af60d29a79fa2`.

CM2's factor identities, endpoint definitions, grid, dependency labels, and
physical prose are reviewed individually. The source's nuclear state, rate,
channel, coherence, sweet-spot, material, yield, heat, and observation claims
remain outside the accepted delta.

## Independence

The independent route imports none of `composite_factors.py`. It constructs a
fresh complete six-state diagonal intermediate block, inverts it exactly,
derives the off-diagonal endpoint element, cancels the inverse-loss factor,
uses the squared-loss coordinate for monotonicity, and rebuilds the nominal
and actual endpoint limits, dimension transformations, grid behavior, and
general loss-power stationary surface.

Five independent-oracle defects are preserved before repair: three SymPy sign
representation failures, one omitted-detuning scaling transformation, and one
algebraically equivalent stationary expression compared structurally. The
repairs change the oracle representation, not the target theorem.

## Verification Status

The maximum verdict is symbolic verified. Forty-six primary checks and twenty-
two independent checks establish exact formulas, derivatives, limits,
piecewise boundary values, scale laws, mutations, and countermodels. Seventeen
focused package tests exercise the reusable API and domain guards. The source's
41-point scan is classified only as regression evidence; no numerical result
is used to prove a theorem already fixed exactly.

CM2 itself passes all 21 checks, but that tally does not validate the headline.
Its symbolic product replaces the Gamma-dependent kernel by K_pos, its zero is
a floating tolerance, its support scan repeats a definition, and its alleged
magnitude-import audit is a hard-coded Boolean marker.

## Sensitivity and Counterexamples

Mutations of the loss numerator power, inverse-loss factor, half-width,
cutoff inequality, actual damped frequency, coupling normalization, and
overall scale change the relevant verdicts. An extra loss power produces the
single-pair stationary point Gamma=2*Delta, whereas the source's linear
opening gives none. Refining the source grid moves the selected node toward
zero instead of converging to an interior optimum.

The source-style nominal extension assigns zero at Gamma=0 although its right
limit is positive, and zero at 2*omega although its left limit is positive.
The actual-cycle alternative removes the upper jump and remains strictly
decreasing. Zero interaction or final-state density gives zero physical rate,
while an arbitrary positive kinetic prefactor fits any positive target.

## Framework Compatibility

The claim is a compatible extension with dependencies C-RES-001 and C-DYN-001.
It preserves C-RES-001's finite-matrix and coupling conventions and
C-DYN-001's nominal-versus-actual cycle distinction. Positive dimensionless
activation, thermal, and count factors may multiply the product without
changing its loss theorem, but their physical interpretations are not
imported.

If detuning, loss, and frequency share one energy or inverse-time dimension
and each coupling product has its square, the composite retains one such
dimension. That typing does not supply Golden-rule dynamics, probability,
state normalization, or a measured rate. Common scaling including coupling
products gives one scale power; fixing the coupling normalization gives the
inverse scale law.

## Dependency and Consumer Replay

BD1, LB2, PN3, PN4, and T1G are admitted only through their accepted claims.
PN2 remains arithmetic-only, B1 remains pending and unused, and the cited H5b
marker supplies no magnitude. CM1's return edge is a source cycle and supplies
no authority.

Seven direct consumers replay 116 checks, and fourteen indirect consumers
replay 576, for 692 clean consumer checks. They remain candidate source units
and inherit only the conditional theorem. No sampled integration occurs, so
P116 has no NumPy trapezoidal compatibility event.

## Competing Candidate Audit

Six candidates were frozen before source execution. Literal reproduction is
retained as source evidence; exact nominal composition, the actual-cycle
alternative, physical countermodels, independent derivation, and governance
closure are selected by dependency closure, exact boundaries, dimensions,
mutation sensitivity, semantic typing, and consumer coverage. No reported
magnitude or grid point selected the result.

## Four-Axis Decision

The claim receives separate accepted axes after claim-level review.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: no challenge or supersession

## Promotion Transaction

Promotion adds `src/substrate_framework/composite_factors.py` and seventeen
tests, archives P116 under campaigns, adds C-CMP-001 to the registry and
v0.96.0 manifest, qualifies CM2 in the editable disposition map, regenerates
the source queue, renders canonical docs and memory, and validates the claim,
release closure, proposal lifecycle, source hashes, and all affected paths.

One integrated repository gate must pass after assembly. The final attempt is
created in progress before that gate and finalized only after clean exit; only
record-sensitive checks follow.

## Continuation if Not Accepted

If the promotion gate fails, P116 remains active and the failing validation,
consumer, registry, or evidence layer is repaired without weakening the exact
claim or importing the rejected rate narrative.

## Done Gate

The claim is accepted only with its importable theorem, independent exact
review, mutation and boundary sensitivity, complete predicate and consumer
audit, synchronized governance state, and empty debt ledger. P116's scientific
ledger is empty before the integrated promotion gate.

## Cross-References

See P116, CM2, C-RES-001, C-DYN-001, C-RG-002, C-TH-001, C-SPN-002,
provisional C-CMP-001, v0.95.0, the P116 audits and verifiers, and the framework-
migration effort.
