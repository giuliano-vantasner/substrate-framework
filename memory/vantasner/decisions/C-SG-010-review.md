---
description: Independent review of C-SG-010
author: vantasner-review
created: '2026-08-01T19:30:00Z'
updated: '2026-08-01T19:30:00Z'
tags:
- substrate-framework
- claim-review
- breather-fourier
- numeric-evidence
category: decisions
confidence: working
status: archived
---
# Review of C-SG-010

## Claim Under Review

The claim records resolution-bounded cycle-average and Fourier-fraction
evidence for the exact `C-SG-009` moment at `omega=1/sqrt(2)`. It does not call
those numerical values exact or identify them with physical radiation.

## Sourced Inputs

The review read `v0.37.0`, `C-SG-009`, its exact canonical formula, P042, and
hash-pinned FS3. The source's sampled FFT values are comparator evidence only.

## Numerical Construction

The primary route differentiates the exact moment symbolically and integrates
its squared third derivative over the exact period with SciPy adaptive
quadrature split into 4, 8, 16, and 32 subintervals. The values are stable
within `2e-11` and the reported final error is below `2e-10`.

## Independent Route

The reviewer derives `mu'''` manually and performs sixty-digit mpmath
quadrature with four subdivision levels. A separate cosine coefficient
construction through sixteen permitted harmonics converges by Parseval to the
same mean without calling the new derivative API.

## Verification Status

The half-period and even-harmonic support are exact consequences of
`C-SG-009`. The displayed mean and first-harmonic fraction remain
`numeric_evidence`, with explicit precision, quadrature, refinement, and
spectral truncation boundaries.

## Sensitivity and Limiting Interpretation

The first permitted coefficient supplies more power than all computed higher
terms combined and the reconstructed tail converges to the direct mean. The
claim is restricted to `omega=1/sqrt(2)`; no family-wide dominance theorem is
inferred from one parameter value.

## Framework Compatibility

This is a native numerical characterization of the already accepted scalar
1+1 moment. It adds no transverse width, quadrupole, coupling, or gravitational
parameter. Its only dependency is `C-SG-009`.

## Source Defects and Scope

FS3 labels an FFT of the same 256 sampled moments a closed-form spectral sum.
Its reported spectral power also contains the factor-nine triple-STF error.
P042 accepts the dimensionless moment-derivative mean and Fourier fraction,
not the source's gravitational label or misnormalized power.

## Dependency and Consumer Replay

The accepted dependency is `C-SG-009`. Direct consumers are the exact
derivative API, P042 numeric evidence, and FS3's qualified mapping. The
conditional power conversion belongs to `C-GW-004`, not this claim.

## Competing Candidate Audit

Candidate A is selected for the refined scalar average because direct and
Fourier routes agree independently. Candidate B would discard reproducible
numeric content. Candidate C cannot turn a scalar numerical functional into a
physical radiation result.

## Four-Axis Decision

The decision applies only to the resolution-bounded special-frequency values.

- Verification: numeric_evidence
- Review: accepted
- Compatibility: native
- Epistemic: active
- Relationship: depends on C-SG-009

## Promotion Transaction

Promotion adds a separately labeled numeric claim beside the exact conditional
wave theorem, freezes its precision and refinement evidence, and synchronizes
the next release. It does not promote FS3's same-data FFT as an independent
oracle.

## Done Gate

Exact input, period, precision, subdivision refinement, independent manual
derivative, Fourier reconstruction, scope, consumers, and claim debt are
closed.

## Cross-References

See P042, FS3, `C-SG-009`, `C-GW-004`, the independent time/Fourier review, and
the parent migration effort.
