---
description: Independent review of C-SG-015 exact breather temporal Fourier structure
author: vantasner-review
created: '2026-08-04T02:35:00Z'
updated: '2026-08-04T02:35:00Z'
tags:
- substrate-framework
- claim-review
- sine-gordon
- migration-SA1
category: decisions
confidence: established
status: active
---
# C-SG-015 Review

## Claim Under Review

C-SG-015 states the exact fixed-position temporal parity, half-wave, Fourier-
support, and fundamental-coefficient theorem for the accepted C-SG-001 rest
breather. It explicitly stops at a field trace and excludes response,
susceptibility, deposition, absorption, population, drive, breakdown, engine,
and nuclear interpretations.

## Sourced Inputs

The review reads release v0.75.0, C-SG-001, C-SG-002, C-SG-009, C-SG-010,
C-DIM-002, C-DIM-003, the frozen P087 contract, canonical code and tests,
every attempt, both exact routes, source and consumer audits, candidate
comparison, impact map, and hash-pinned SA1. The engineering mirror and C035
rungs are noncanonical consumer evidence only.

## Independence

The independent reviewer imports none of the new sine-Gordon APIs. Starting
from `4*atan(a*sin(y))`, it derives parity and half-wave transformations,
performs the tangent-substitution and integration-by-parts algebra, checks the
parameter derivative, specializes the on-shell core, and compares 50-digit
direct quadrature at three amplitudes. It separately reconstructs the
finite-Gaussian-DC, overlap-scaling, high-pass-counterfamily, phase-origin,
and dimensional ceilings.

## Verification Status

The claim earns `symbolic_verified`. The primary route passes 42 checks and
the independent route passes 15; focused sine-Gordon tests pass 40. The exact
coefficient is derived in two algebraic forms and checked independently at
high precision. Numerical integration carries no exact verdict.

## Sensitivity and Counterexamples

Adding a cosine term breaks oddness while retaining half-wave behavior; adding
an even sine term preserves oddness while breaking half-wave behavior; a
constant breaks both. The leading `4*a`, a factor-four mutation, and a cubic
correction fail the full coefficient oracle. At `omega=3/5` the exact core
coefficient is 4 while SA1's leading term is 16/3. The finite Gaussian pair is
strictly positive at DC and loses a third-harmonic probe. Two non-derivative
high-pass kernels refute inference from a zero DC value to differentiation.
Spectrum normalization cancels its magnitude while free kernel amplitude
retains arbitrary scaling.

## Framework Compatibility

C-SG-015 is a native exact consequence of C-SG-001 and changes no accepted
equation, field, period, energy, or convention. C-SG-009 and C-SG-010 concern
the even energy second moment; they do not own the field trace's odd temporal
support or fundamental coefficient. Time origin is explicit: a shift rotates
sine and cosine coefficients while preserving zero mean and harmonic support.

## Dependency and Consumer Replay

Direct accepted consumers are the three pure canonical APIs, package exports,
focused tests, P087 verifiers, and this review. Generated governance and
memory are indirect consumers. The external engineering mirror fails under
current NumPy because it calls `np.trapz`; that failure and its six aliases are
preserved. A rename would not repair its physical overclaims. Rungs 174 and
175 still contain inserted Michaelis triggers and import no SA1 implementation.
No external consumer enters the accepted dependency closure.

## Competing Candidate Audit

Eight candidates and ordered structural criteria were frozen before source
opening. Literal promotion fails. The exact parity theorem and corrected
coefficient survive. The response-mechanism requirement, zero-DC
counterfamily, overlap nonidentifiability, source-oracle audit, and
nonduplication test jointly prevent laundering the source narrative into the
claim. SA1's printed overlap values were not selection criteria.

## Four-Axis Decision

The independent axes accept the exact consequence without widening its scope.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: native
- Epistemic: active
- Relationship: new consequence of C-SG-001; no challenge or supersession

## Promotion Transaction

Promotion adds C-SG-015 to the registry and sine-Gordon API, moves P087
unchanged into campaigns, creates v0.76.0, regenerates docs and accepted
memory, records SA1 as qualified, regenerates the source queue, and updates the
parent effort. Targeted replay precedes one unchanged integrated gate and
record-sensitive final validation.

## Continuation if Not Accepted

This section is inactive because the exact theorem is accepted. Its acceptance
does not promote the physical transfer claim or close migration; SA2 remains a
separate pending unit whose dependency on SA1's rejected interpretation must
be audited afresh.

## Done Gate

C-SG-015 may be accepted only after registry/release closure, generated-state
agreement, mutation-sensitive replay, and empty P087 debt. The parent effort
remains incomplete while pending units remain.

## Cross-References

See P087, SA1, C-SG-001, C-SG-002, C-SG-009, C-SG-010, both exact verifiers,
source and consumer evidence, the canonical sine-Gordon APIs/tests, v0.76.0,
and the framework migration effort.
