---
description: Independent review of C-RG-001
author: vantasner-review
created: '2026-08-01T11:43:25Z'
updated: '2026-08-01T11:43:25Z'
tags:
- substrate-framework
- claim-review
- radial-energy
- migration-T1A
category: decisions
confidence: working
status: archived
---
# Review of C-RG-001

## Claim Under Review
For positive radius and density, `E_line=2*pi*R*lambda` is homogeneous of degree one, has constant positive derivative, and has no stationary radius. For positive surface density, `E_shell=4*pi*R^2*sigma` is degree two and has a radius-dependent derivative. For positive tension and pressure, `E_cap=2*pi*R*T-pi*R^2*P+C` has the unique strict global maximum `R=T/P`. Conditional line constructions with coefficients `T` and the accepted `E_b(omega)` share this degree-one form, but their energies are equal for every positive radius if and only if `T=E_b(omega)`.

## Sourced Inputs
The review read release `v0.5.0`, `C-SG-002`, P006's frozen candidates and criteria, attempt `0001`, the package implementation/tests, and hash-pinned source unit T1A. T1A's eight executable subclaims are: degree one for both declared ring forms, constant positive marginal energy for both, degree-two and derivative guards for a spherical shell, reuse of the accepted breather coefficient, non-identification of the two coefficients, and absence of a stationary radius for the isolated line term.

The Frank-action interpretation of `T`, the physical breather-to-ring lift, and any ring quantization remain conditional source attributions. T1A does not reproduce their physical derivations, and C-RG-001 does not promote them as unconditional identities.

## Independence
The proposal path calls the new radial-energy APIs and verifies exact identities. The independent review does not import that module. It reconstructs transverse circumference and area energies, obtains powers from both scaling ratios and logarithmic derivatives, completes the capillary square, and solves the coefficient-equality equation directly. It imports only the already accepted breather energy API.

## Verification Status
Exact SymPy algebra and calculus establish every quantified formula on the declared positive domain. Homogeneity and Euler identities agree; derivative and second-derivative routes distinguish line, shell, and capillary forms; completion of the square establishes a global capillary maximum rather than only a local stationary point. The claim earns `symbolic_verified`.

## Sensitivity and Counterexamples
The main predicate rejects a doubled circumference factor and radial powers zero and two. It rejects both a free `T` and twice the breather coefficient as identities, while accepting the equality only after the exact coefficient premise. Positive, negative, and zero pressure mutations distinguish a maximum from a minimum or absent finite critical point. The independent route separately rejects the shell by scaling ratio and nonzero second derivative.

## Framework Compatibility
The claim is a compatible extension. It adds a generic exact geometry utility and depends on `C-SG-002` only for the conditional breather instantiation. It does not identify the pulson and breather objects, import a Frank-tension formula, infer units across programs, fit a coefficient, select a radius, or derive quantization. The full capillary term is kept distinct from its isolated line component.

## Dependency and Consumer Replay
Direct consumers are `src/substrate_framework/radial_energy.py`, package exports, `tests/test_radial_energy.py`, and future governed ring/capillary campaigns. The main and independent verifiers plus package tests pass. Every executable T1A predicate is represented, and its physical lift/import ceiling is explicit, so the bridge unit can be marked migrated without accepting the title's informal object identity.

## Competing Candidate Audit
Candidates A, B, and C were registered before implementation. Exact scaling was selected as the primary structural classifier. Marginal derivatives independently establish the line hallmark, while logarithmic slopes and stationary structure distinguish the capillary form. There is no empirical comparator.

## Four-Axis Decision
The exact generic classification and carefully conditional instantiation support acceptance.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: additive, with no challenge or supersession

## Promotion Transaction
Promotion freezes P006, adds the radial-energy APIs/tests and `C-RG-001`, creates release `v0.6.0`, regenerates docs and accepted memory, marks T1A migrated, regenerates the migration queue, and replays affected consumers.

## Continuation if Not Accepted
Any replay failure withdraws acceptance and returns to the derivative classifier. Coefficient or physical-object identity cannot be recovered by weakening the exact equality condition or treating a declared lift as a derivation.

## Done Gate
The claim gate is satisfied subject to promotion replay: the positive exact classification exists, two independent structural routes agree, mutations distinguish all load-bearing alternatives, and the source ceiling is preserved with no P006 debt.

## Cross-References
See `campaigns/P006-radial-energy`, source unit T1A in `migration/source-claims.yaml`, `C-SG-002`, `governance/claims.yaml`, and the parent migration effort.
