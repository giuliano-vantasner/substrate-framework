---
description: Derive EM6's conditional quartic Q-ball profile and charge curve
author: vantasner
created: '2026-08-01T16:33:00Z'
updated: '2026-08-01T16:37:00Z'
tags:
- substrate-framework
- campaign-proposal
- quartic-qball
- stability-audit
- migration-EM6
category: proposals
confidence: exploratory
status: archived
---
# P031 EM6 Quartic Q-Ball

## Question and Positive Deliverable

P031 must derive the exact localized stationary solution of EM6's declared
quartic profile ODE and its `C-U1-001` charge curve, then classify every
stability statement at the strongest level its oracle earns. The positive
deliverable is an importable conditional profile theorem, not a no-go or an
ontology slogan.

## Base Release and Provenance

The accepted base is `v0.26.0` at framework commit `422bcaa`. `C-U1-001`
supplies the independently declared complex scalar, stationary-phase current,
and real-field zero-current statement. `C-GAU-001` adds local gauge algebra but
does not make the scalar physical or dynamically stable. The hash-pinned
candidate is EM6 at
`merged-framework/bridges/phase-3/bridge_EM6_derived_profile_stability.py`,
SHA-256 `926df2dc5014042472b3d47576af06676eb654d9da4634f147c7044d4e91f897`.
Memory search found no accepted Q-ball profile claim.

## Invariants, Conventions, and Allowed Imports

The campaign imports `C-U1-001`, exact ODE and hyperbolic-function calculus,
and `C-GAU-001` only as downstream context. The stationary phase is
`exp(-i*omega*t)`, so charge normalization follows the accepted current. The
quartic ODE and its coefficients remain declared unless EM6 independently
varies an action. A sign of `dQ/domega` may be reported exactly but cannot be
renamed spectral, orbital, or nonlinear stability without a theorem whose
hypotheses and fluctuation operator are checked.

## Candidate Preregistration

The candidates are frozen from migration metadata before the full EM6 body is
read.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Exact sech solution, ansatz-forced coefficients, charge curve, and derivative-sign branches | Declared quartic ODE and C-U1-001 | Frequency | Native conditional result if normalization closes | Full residual, coefficient collection, charge integration, endpoint and branch tests |
| B | Exact profile theorem only | Declared quartic ODE | Frequency | Preferred if charge/stability conventions conflict | Independent current integration and sign audit |
| C | Stable physical excitation with forced complex ontology | Imported VK theorem plus physical sector map | Charge and frequency | Conflicts absent spectral and ontology closure | Linearized operator, theorem hypotheses, and real-sector countermodels |

## Selection Criteria and Blinding

Selection is ordered by exact residual, completeness of the sech coefficient
solve, accepted-current normalization, localization and endpoint behavior,
separation of derivative sign from stability, counterprofile sensitivity,
assumption economy, and downstream FG1 reach. No numeric fit or physical mass
value may select a candidate.

## Proposed Claim Delta

Provisional `C-QBL-001` states the exact positive sech solution of the declared
quartic profile ODE on its frequency domain, its forced width and amplitude
within the nonzero sech ansatz, its exact global-U1 charge, and the sign changes
of the charge derivative. It explicitly excludes existence uniqueness beyond
the ansatz, spectral or nonlinear stability, forced complex ontology, electric
charge, particle identity, and substrate realization.

## Implementation and Oracle Plan

Create a pure quartic-Q-ball module with profile, residual, inverse width,
amplitude, charge, and derivative APIs. SymPy is the exact oracle for the ODE,
sech-power coefficient solve, integration, domain limits, and derivative sign.
Mutations change the cubic coefficient, width, amplitude, charge factor, and
frequency branch; Gaussian and half-amplitude profiles are counterexamples.
Independent review will derive the homoclinic first integral and charge without
importing package helpers.

## Attempts and Continuation

Attempt `0001` will reproduce EM6 and inventory whether the VK theorem and its
hypotheses are actually encoded. A convention failure selects Candidate B. A
missing stability theorem qualifies that interpretation while preserving the
positive exact profile and charge result under Candidate A.

## Debt Ledger

This ledger tracks ODE provenance, coefficient completeness, charge, stability,
and ontology debt.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| The quartic ODE may be declared rather than varied | Identify its exact source status and keep it conditional if needed | discharged: EM6 declares it and C-QBL-001 remains conditional |
| A substituted sech may not show its parameters are forced | Collect independent sech powers and solve both coefficients | discharged: main coefficient solve and independent first integral agree |
| Charge normalization may inherit EM1's old sign | Integrate the C-U1-001 current independently | discharged: both routes give positive density and Q=96*omega*kappa |
| A VK derivative sign may be called a stability proof | Audit theorem statement, hypotheses, and fluctuation oracle | discharged: only the slope sign is accepted; stability is excluded |
| Zero current for a real field may be called forced ontology | Separate charge definition from viability and physical identity | discharged: current identity retained and ontology inference rejected |

## Review and Promotion Plan

The provisional claim receives an independent first-integral and charge review.
Promotion requires pure APIs/tests, immutable attempts, source reproduction and
check-family audit, claim axes, terminal EM6 disposition, registry/release/docs
and memory synchronization, FG1 consumer mapping, focused replay, and one full
unchanged gate.

## Done Gate

P031 closes only when the profile, coefficient solve, charge, domains,
derivative branches, stability boundary, ontology scope, mutations, consumers,
source disposition, and campaign debt all satisfy the framework contract.

## Adjudication Result

Candidate A is accepted in its narrow preregistered scope. Twenty-four main
checks and seven independent checks establish the exact conditional profile,
charge curve, endpoints, maximum, and derivative branches. EM6 is qualified
because its VK and forced-ontology claims have no spectral oracle, and all
campaign debt is discharged.
