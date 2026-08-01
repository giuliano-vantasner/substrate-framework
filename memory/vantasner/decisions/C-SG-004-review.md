---
description: Independent review of C-SG-004
author: vantasner-review
created: '2026-08-01T11:11:52Z'
updated: '2026-08-01T11:11:52Z'
tags:
- substrate-framework
- claim-review
- sine-gordon
- virial
- gradient-integral
category: decisions
confidence: working
status: archived
---
# Review of C-SG-004

## Claim Under Review
For every real `omega` with `0<omega<1`, the C-SG-001 breather has period-averaged squared-gradient integral `Gbar=(1/T)*int_0^T dt int_R dx phi_x^2=16[sqrt(1-omega^2)-omega arccos(omega)]=E-omega J`. It obeys `dGbar/domega=-J`, tends to 16 at `omega->0+`, and tends to zero at `omega->1-`. `Gbar` is explicitly the full squared-gradient integral; the Hamiltonian gradient contribution is `Gbar/2`.

## Sourced Inputs
The review read release `v0.2.0`, accepted claims `C-SG-001/002/003`, their source APIs and evidence, P003's preregistered candidates and factor convention, both attempt records, and the predecessor closed-form script at pinned `substrate@6d1f4e0`. The review does not import the predecessor's finite series checks as an exact global proof.

## Independence
The proposal route derives the spacetime virial identity from the accepted field equation, audits periodic and localized boundary terms, and combines it with accepted energy and action. The independent route does not import the proposed gradient or action APIs; it reconstructs `phi_x`, differentiates an exact transformed spatial antiderivative, evaluates its period average at two precisions, and performs a direct nested integral of the field at `omega=0.5`.

## Verification Status
The main oracle earns `symbolic_verified`: exact product rules and vanishing boundary terms establish `Vbar=(Kbar+Gbar)/2`; Hamiltonian and action identities then derive `Gbar=E-omega J`, after which exact calculus establishes the formula, derivatives, convexity, limits, and leading harmonic asymptotic. The independent quadrature is correctly retained as numeric corroboration.

## Sensitivity and Counterexamples
The exact defining predicate rejects coefficient 15, additive offset 1, the wrong sign of `omega*arccos(omega)`, and coefficient 8 representing the common half-gradient confusion. The field review rejects the same half-factor at four frequencies and is stable from 30 to 50 digits. Attempt `0001` failed because SymPy could not infer positivity of `sqrt(1-omega^2)` inside a limit; attempt `0002` exposed the already accepted inverse width as a positive symbol for the localization-only checks and passed without changing the claim or threshold.

## Framework Compatibility
The result is native to the accepted normalized sine-Gordon sector, introduces no parameter, and reuses the exact field, Hamiltonian, period, energy, and action conventions. Its endpoint limits agree with the accepted family. Calling it an averaged squared-gradient integral rather than an undifferentiated action prevents a predecessor naming ambiguity from leaking into consumers.

## Dependency and Consumer Replay
Direct consumers are `src/substrate_framework/sine_gordon.py`, the package exports, and `tests/test_sine_gordon.py`. P001 and P002 remain unchanged and are replayed at promotion. Future slow-manifold or effective-action campaigns must import `C-SG-004` rather than duplicate its formula. No campaign debt remains.

## Competing Candidate Audit
Candidates A, B, and C and their structural criteria were frozen before implementation. A was selected because it alone directly and exactly identifies the physical field integral with audited boundaries. C independently reproduces the closed expression after that identification. B provides a separate field construction and numeric refinement without carrying the exact verdict.

## Four-Axis Decision
The exact virial route supports acceptance, and the separate field integration confirms that its load-bearing factor is physically normalized.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: native
- Epistemic: active
- Relationship: additive, with no challenge or supersession

## Promotion Transaction
Promotion freezes P003 under `campaigns/`, adds the pure gradient API and tests, adds only `C-SG-004` to the registry, creates release `v0.3.0`, regenerates docs and accepted memory, and replays all accepted campaigns before one full repository validation.

## Continuation if Not Accepted
Any promotion-replay failure withdraws acceptance and activates Candidate B's exact averaging obligation. The failed representation in attempt `0001` is preserved and does not count as completion.

## Done Gate
The claim-level gate is satisfied subject to promotion replay: the exact positive object exists, dependency closure is accepted, boundary assumptions are discharged, independent field evidence is sensitive, and no P003 debt remains.

## Cross-References
See `campaigns/P003-sine-gordon-gradient`, `governance/claims.yaml`, `governance/releases/v0.2.0.yaml`, accepted campaign records P001/P002, and `memory/vantasner/efforts/framework-migration.md`.
