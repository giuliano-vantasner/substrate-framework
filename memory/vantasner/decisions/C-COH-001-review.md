---
description: Independent review of C-COH-001 conditional phase-ensemble and activation thresholds
author: vantasner-review
created: '2026-08-04T01:40:00Z'
updated: '2026-08-04T01:40:00Z'
tags:
- substrate-framework
- claim-review
- coherence
- migration-NY3
category: decisions
confidence: established
status: active
---
# C-COH-001 Review

## Claim Under Review

C-COH-001 states the exact expected directional quadratic observable for
positive integer `N` iid equal-amplitude unit phasors with pair coherence
`V=|E z|^2`: `I1*(N+N*(N-1)*V)`. It includes the centered-Gaussian
specialization `V=exp(-sigma^2)`, explicit normalization dependence, and the
separately conditional continuous activation scale, unique threshold root,
endpoint ordering, and activated exponential factor. It excludes total-energy,
temperature, stochastic-rate, material-barrier, event-channel, and payload
interpretations.

## Sourced Inputs

The review reads release v0.74.0, C-RG-001, C-DIM-002, C-DIM-003, C-SK-001,
the P086 frozen proposal, canonical module and tests, every attempt, both exact
verifiers, source and consumer audits, candidate comparison, provenance,
impact analysis, and hash-pinned NY3. Rung091/rung092 and pending BD1/BD3 are
evidence only; duplicate NY1/NY2 supply no accepted nuclear channel.

## Independence

The independent reviewer imports none of the new coherence APIs. It counts
diagonal and ordered-pair terms directly, evaluates the Gaussian characteristic
integral, solves and substitutes the threshold quadratic from fresh symbols,
derives endpoint signs and activated-factor derivatives, and recomputes the
capillary relative height.

## Verification Status

The claim earns `symbolic_verified`. The primary route passes 37 exact checks
and the independent route passes 12. All sums, integrals, roots, derivatives,
and limits resolve to explicit expressions; no unevaluated symbolic object or
numerical solver carries the verdict. The NY3 and engineering executions are
source and consumer regression evidence only.

## Sensitivity and Counterexamples

Three wrong population polynomials fail endpoint and one-source identities.
Changing the per-source scale reverses NY3's N=16 crossing verdicts. Fixed-
total normalization reduces the aligned formula by one factor of N; a
deterministic antiphase pair gives zero and exposes the iid ensemble premise.
The fully aligned threshold is lower only for `E/theta>1` and reverses below
one. At `N=1` the coherence derivative is zero. Barrier, activation-scale, and
Gaussian-variance limits all have their declared signs.

## Framework Compatibility

The claim is a compatible exact extension with no accepted dependencies. It
uses exact positive domains and keeps discrete emitter count separate from the
continuous threshold coordinate. Directional intensity, total energy,
effective temperature, and rate remain different logical types. C-RG-001 is
used only to audit NY3's capillary input and is not required by the general
theorem.

## Dependency and Consumer Replay

Direct consumers are the canonical tests, P086 verifier, and source
adjudication. Package-root exports and generated governance artifacts are
indirect consumers. The hash-pinned directional consumer runs directly; after
installing its declared `scikit-fem` dependency in the local environment, its
unchanged full verifier passes 61 checks. It confirms on-axis N-squared and
total N behavior but supplies no barrier or nuclear coupling. No claim debt is
created.

## Competing Candidate Audit

Nine candidates and ordered structural criteria were frozen before the source
body opened. Literal promotion fails closure; conditional interpolation and
activated algebra survive; a dynamical coherence/escape mechanism and nuclear
channel do not exist; normalization and phase countermodels are decisive. The
claim is selected for its distinct exact phase-ensemble and threshold content,
not because NY3's inserted numbers cross or its factor ratio exceeds ten.

## Four-Axis Decision

The four axes preserve the exact conditional theorem without inheriting NY3's
physical narrative.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: new dependency-free claim; no challenge or supersession

## Promotion Transaction

Promotion adds C-COH-001 to `governance/claims.yaml`, retains the pure module
and focused tests, moves P086 unchanged into `campaigns/`, creates v0.75.0,
regenerates docs and accepted memory, records NY3 as qualified, regenerates the
source queue, and updates the parent effort. Targeted replay precedes one
unchanged integrated `scripts/validate.sh` gate and final record-sensitive
validation.

## Continuation if Not Accepted

This section is inactive because the conditional theorem is accepted. Its
acceptance does not promote a physical gate or close the corpus migration; the
next sequential pending unit remains active after P086.

## Done Gate

C-COH-001 may be accepted only after registry/release closure, generated-state
agreement, affected consumers, and the integrated gate pass with empty P086
debt. The parent effort remains incomplete while pending units remain.

## Cross-References

The controlling records are P086, NY3, both exact verifiers, source and
consumer evidence, C-RG-001, C-DIM-002, C-DIM-003, C-SK-001, the canonical
coherence-gate module/tests, v0.75.0, and the framework migration effort.
