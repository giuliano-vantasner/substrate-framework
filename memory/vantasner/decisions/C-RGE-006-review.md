---
description: Independent review of C-RGE-006 conditional gauge-only boundary running
author: vantasner-review
created: '2026-08-08T22:00:00Z'
updated: '2026-08-08T22:00:00Z'
tags:
- substrate-framework
- claim-review
- renormalization
- numeric-running
- migration-WM6
category: decisions
confidence: established
status: archived
---
# C-RGE-006 Review

## Claim Under Review

C-RGE-006 defines the inverse-coupling flow induced by C-RGE-005, an exact
zero-matrix two-constraint boundary reconstruction, and a status-gated numeric
solution for one fully supplied three-factor specialization. It claims a
conditional inverse solution and reference-scale covariance, not a preferred
boundary, a Standard-Model prediction, unification, or an all-orders result.

## Sourced Inputs

The review reads v0.99.0, C-RGE-004, C-RGE-005, P130's frozen contract, both
attempts, the canonical module and tests, both verifiers, every campaign audit,
and the pinned dependency and consumer records. WM6 is pinned at SHA-256
`6d1ea4245adcf490466974d4a40b24843cd92e883c6e885936fb030cd1b31d57`.

WM6's eleven predicates are reviewed individually. Its conditional numeric
core survives with stronger status, residual, positivity, refinement, and
scope gates. Its rounded exactness check, hard-coded output regression, pending
SM4 scale comparison, comparator-use prose, coefficient-size forecast,
uniform-matrix fit, effect-attribution list, six-point scan, prediction, and
all-orders readings do not survive.

## Independence

The independent reviewer imports neither `gauge_running.py` nor its inverse
solver. It transforms the supplied boundary into direct gauge couplings,
integrates those variables with Radau, shoots positive logarithmic parameters
with a separate hybrid root, and independently reads the frozen proposal and
source AST. A DOP853 replay, sign mutant, exact zero-matrix limit, independent
matrix direction, and finite matching offset are derived in that route.

## Verification Status

The mixed claim earns `numeric_evidence`. SymPy exactly establishes the
zero-matrix affine route, but the nonzero-matrix specialization is a
double-precision ODE and shooting result. Twenty-three primary checks, twelve
independent checks, and twelve focused tests establish the source and freeze
hashes, equations, exact containment, solver statuses, residual and positivity
gates, method and tolerance agreement, scale covariance, and sensitivity.

No copied comparator makes the solve pass. The measured weak coordinate is
absent from the canonical problem and shooting residual. It is retained only
as an explicitly labelled post-solve comparator and inverse-target probe. No
quadrature or NumPy integration alias occurs in WM6 or its replayed consumers.

## Sensitivity and Counterexamples

Changing the two-loop sign, transposing its asymmetric matrix, changing a
boundary ratio, or changing a supplied low coordinate changes the conditional
readout. An impossible residual tolerance fails rather than being rounded into
success. DOP853 tolerance tightening, Radau, distinct initial guesses, and the
fresh direct-coupling formulation agree beyond the reported digits; every
accepted path remains positive and closes its residual gate.

The fitted multiplier is 8.7483 for the exposed comparator but 4.2836 for a
target of 0.22. An independent matrix direction is not proportional to the
two-loop matrix, and a finite matching offset changes the readout without
changing either beta coefficient array. These countermodels reject WM6's
all-orders and effect-attribution readings without being adopted as repairs.

## Framework Compatibility

The claim is a compatible extension of C-RGE-004 and C-RGE-005. Its downward
inverse flow is the declared coordinate transform of the accepted gauge-only
beta polynomial, and its zero-matrix limit is the accepted affine inverse
problem. Supplied positive boundary ratios, two rank-two low constraints, a
reference scale, and a readout map remain visible rather than being renamed as
derived observables.

The accepted surface excludes the same-order Yukawa term, multiple-Abelian
kinetic mixing, thresholds, matching, scheme conversion, input provenance,
uncertainties, a preferred boundary, physical field content, observation,
unification, and substrate realization. Positivity along one supplied
trajectory does not establish a global perturbative domain.

## Dependency and Consumer Replay

WM3 and WM5 reproduce 21 dependency checks from pinned bytes. Pending WM8 and
WM10 reproduce 17 later-consumer checks but gain no authority. The new public
solver has no upstream code callers or affected indexed process, while package
tests and P130 are explicit direct consumers. Generated claim, release, memory,
documentation, disposition, and queue surfaces are synchronized only in the
promotion transaction. The debt ledger is empty.

## Competing Candidate Audit

Literal replay, a canonical inverse solve, a fresh direct-coupling solve, exact
one-loop containment, refinement, data-flow mutations, all-orders
countermodels, and governance closure were registered before P130 source-body
reinspection. P129 had already exposed the source outputs, so pristine blinding
is honestly unavailable. Selection uses structure and verifier sensitivity;
numerical proximity to the exposed comparator selects nothing.

## Four-Axis Decision

The four axes preserve the distinction between exact containment and the
resolution-bounded nonzero-matrix result.

- Verification: numeric_evidence
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: new claim depending on C-RGE-004 and C-RGE-005; no challenge or supersession

## Promotion Transaction

Promotion adds `gauge_running.py` and twelve focused tests, exports its pure
records and functions, archives P130, adds C-RGE-006 to the registry and
v0.100.0 manifest, qualifies WM6, regenerates the queue, and renders canonical
documentation and memory. One integrated repository gate runs after assembly;
the terminal attempt is finalized only after clean exit.

## Continuation if Not Accepted

If the promotion gate fails, P130 remains active and the solver, numeric gates,
claim scope, registry, release, disposition, or generated consumers are
repaired without fitting the exposed comparator or weakening the residual and
positivity requirements.

## Done Gate

C-RGE-006 is accepted only with the importable positive solver, exact
zero-matrix containment, independent direct-coordinate reproduction,
load-bearing mutations, declared omissions, synchronized governance state,
downstream replay, and an empty debt ledger.

## Cross-References

See P083, P129, P130, WM3, WM5, WM6, WM8, WM10, C-RGE-004, C-RGE-005,
C-RGE-006, v0.99.0, v0.100.0, and the framework-migration effort.
