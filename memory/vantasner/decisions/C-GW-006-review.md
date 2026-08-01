---
description: Independent review of C-GW-006
author: vantasner-review
created: '2026-08-01T23:31:00Z'
updated: '2026-08-01T23:45:00Z'
tags:
- substrate-framework
- claim-review
- l2-derivatives
- simulation-evidence
category: decisions
confidence: working
status: archived
---
# Review of C-GW-006

## Claim Under Review

The claim records endpoint-qualified second and third derivatives of the
accepted regular l=2 coefficient `q(t)=Qzz(t)/epsilon` and applies
`C-GW-005` to obtain dimensionless conditional coefficients
`h_plus*R/(G*epsilon)` and `P/(G*epsilon^2)`. It fixes the IVP, mesh, timestep,
sampling, estimator, interpreted window, error metric, refinements, and
strictly conditional finite-time scope.

## Sourced Inputs

The review read `v0.41.0`, `C-PDE-003/004`, `C-GW-001/002/004`, P047's
proposal and six attempts, both canonical modules, the 37-check primary
verifier, the independent nine-check direct finite-difference review, source
reproduction, and the P3D4 sentence-level adjudication. The source's product-
field trace and frequency spectrum are not substituted for the corrected
regular-mode trace.

## Independence

The primary derivative uses a nine-point degree-five local polynomial and
cross-checks a quintic interpolating B-spline. The review independently derives
seven-point second- and third-derivative weights from polynomial moment
conditions, differentiates a fresh baseline evolution, and rederives the TT
and flux factors without the new radiation-coefficient API. Both routes carry
the formal `epsilon` normalization explicitly.

## Verification Status

The maximum earned status is `simulation_evidence`. The tensor mapping is
exact, but `q''`, `q'''`, and their RMS/mean values are derivatives of a
finite-grid PDE trace. All solver results are finite and complete; the claim
has spatial, timestep, sampling, domain, estimator, endpoint, boundary, and
amplitude evidence. It remains resolution-bounded rather than exact.

## Sensitivity and Counterexamples

Second-derivative mesh differences decrease from 2.576 to 0.651 percent and
third-derivative differences from 4.297 to 1.099 percent. Timestep errors are
0.566 and 1.029 percent; sampling errors are 4.132 and 4.755 percent; domain
errors are below `1e-11` percent; local/spline differences are 4.507 and 5.013
percent. The independent seven-point route reproduces both derivative and
conditional summaries within ten percent. Half mode coefficient gives exact
half derivatives, half waveform coefficient, and quarter power; zero mode
gives an exact zero trace. A static nonzero trace gives zero power, and the
wrong quadrupole scale gives nine times the power.

## Framework Compatibility

The claim is a compatible conditional consumer of qualified `C-PDE-004` and
exact `C-GW-005`. It inherits the linearized dimensionless model and does not
upgrade its field trajectory to nonlinear stability or periodicity. The
five-unit endpoint exclusion exceeds the derivative stencil support. `G`,
`R`, and `epsilon` are not assigned values, so the claim supplies coefficients
rather than an absolute waveform or luminosity.

## Dependency and Consumer Replay

Dependencies are `C-PDE-004` and `C-GW-005`; their closure includes the radial
model, regular l=2 equation, moment convention, and TT/conditional inputs. The
targeted suite passes 60 tests. P042, P043, and P046 replay with status zero and
37, 26, and 31 checks. QB3 and QB4 are prospective consumers and must not
promote a twice-frequency, physical-radiation, or absolute-scale result from
this coefficient trace. No consumer debt remains.

## Competing Candidate Audit

Candidate A was selected because every preregistered numerical gate closed and
the independent finite difference agreed. Candidate B remains the exact-only
fallback and would have been selected if any derivative gate failed. Candidate
C is rejected by field consistency, convention closure, and derivative
methodology before considering source comparison values.

## Four-Axis Decision

The four axes retain the numerical, finite-time, and conditional ceiling.

- Verification: simulation_evidence
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: qualified
- Relationship: depends on C-PDE-004 and C-GW-005; challenges and supersedes none

## Promotion Transaction

Promotion adds reusable derivative and conditional coefficient APIs, targeted
tests, all failed and passing attempts, independent review, qualified P3D4
mapping, registry and release entries, generated records, and accepted-memory
synchronization. P3D4 remains qualified for every rejected source-specific
subclaim.

## Continuation if Not Accepted

If derivative convergence or estimator agreement failed, Candidate B would
retain `C-GW-005` and omit this numerical claim. The source's band-limited
trace could not rescue it because it uses a rejected source and selected
filter.

## Done Gate

The positive coefficient trace, solver status, refinements, independent route,
mutations, formal normalization, dependencies, consumers, scope, v0.42
registry/release transaction, generated records, reproducible source
disposition, and full gate are closed.

## Cross-References

See P047, P3D4, `C-PDE-003/004`, `C-GW-001/002/005`, the derivative and
conditional coefficient modules, the source adjudication, and the parent
migration effort.
