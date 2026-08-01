---
description: Reconcile FG1 through an exact sine-potential Q-ball audit
author: vantasner
created: '2026-08-01T16:40:00Z'
updated: '2026-08-01T16:49:00Z'
tags:
- substrate-framework
- campaign-proposal
- exact-sine-qball
- asymptotic-reconciliation
- migration-FG1
category: proposals
confidence: exploratory
status: archived
---
# P032 FG1 Exact-Sine Q-Ball

## Question and Positive Deliverable

P032 must determine the strongest exact and numerical theorem supported by
FG1's declared stationary equation `f''=sin(f)/2-omega^2*f`. The positive
deliverable is an importable implicit localized family and controlled quartic
limit if those obligations close, not a reconciliation slogan.

## Base Release and Provenance

The accepted base is `v0.27.0` at framework commit `b429159`.
`C-U1-001` fixes the conditional complex-field current, and `C-QBL-001` fixes
the quartic profile family while explicitly separating it from EM1. The
hash-pinned candidate is FG1 at
`merged-framework/bridges/phase-11/bridge_FG1_charged_soliton_reconciliation.py`,
SHA-256 `f0e655828c2796d9f38aaff0d055dfe8a28562de700f408600e645dce2b2b45b`.
Memory search found only the parent next action and accepted dependency maps,
not an accepted exact-sine profile claim.

## Invariants, Conventions, and Allowed Imports

The campaign imports the accepted current convention, the quartic comparison
family, exact calculus, and numeric tools only when a precise resolution-bounded
claim requires them. The sine-potential ODE remains declared unless FG1 varies
an accepted action. A limiting profile relation does not identify fields,
potentials, amplitudes, or physical objects away from the controlled limit.

## Candidate Preregistration

The candidates are frozen from migration metadata before the full FG1 body is
read.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Exact implicit homoclinic family, charge quadrature, and controlled quartic limit | Declared sine ODE and C-U1-001 | Frequency and translation | Compatible conditional extension | First integral, first-root branch, charge finiteness, scaled asymptotics, independent numeric replay |
| B | First integral and local series only | Declared sine ODE | Frequency | Selected if global/numeric closure fails | Root multiplicity, shooting sensitivity, domain/tolerance refinement |
| C | One physical profile across EM1, EM6, and FG1 | Cross-model ontology map | Multiple incompatible widths/amplitudes | Conflicts with accepted distinctions | Direct residuals, normalization, finite-frequency counterexamples |

## Selection Criteria and Blinding

Selection is ordered by exact sign closure, localized boundary data,
unambiguous first-positive-root selection, finite accepted-current charge,
controlled amplitude and coordinate scaling, real numerical refinement where
needed, and assumption economy. Numerical closeness at one frequency cannot
select the concept.

## Proposed Claim Delta

Provisional `C-QBL-002` would state the exact first integral and implicit
positive homoclinic of the declared sine-potential ODE, its charge quadrature,
and only the precisely controlled limit in which it approaches
`C-QBL-001`. It excludes a closed elementary profile, EM1 object identity,
spectral stability, electric charge, particle identity, and substrate ontology.

## Implementation and Oracle Plan

SymPy will verify the first integral, sine expansion, peak equation, and
quartic scaling. Root and implicit-profile machinery will use pure APIs with
explicit branch and domain guards. If a numerical profile or charge is
promoted, SciPy evidence must vary domain, tolerance, and resolution and compare
an independent quadrature or direct BVP/IVP route. Mutations reverse the cosine
sign, choose a later peak root, change the quartic coefficient, and substitute
EM1's width.

## Attempts and Continuation

Attempt `0001` will reproduce FG1 and audit its shooting initial data,
refinement axes, charge calculation, asymptotic fit, and reconciliation logic.
Weak global evidence selects Candidate B while preserving the positive exact
integral. A direct finite-frequency profile identity failure rejects Candidate
C rather than weakening accepted distinctions.

## Debt Ledger

This ledger tracks the declared action boundary, global branch, numerical
oracle, asymptotic control, and reconciliation scope.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| The exact-sine ODE may be declared rather than varied | Audit provenance and keep the theorem conditional if needed | discharged: the predecessor potential is not accepted, so C-QBL-002 is explicitly conditional |
| The peak equation may have multiple roots | Define and verify the first positive homoclinic root on the stated domain | discharged: the squared-sinc ratio is strictly decreasing on (0,2*pi), giving one root |
| Same-data shooting may masquerade as existence or convergence | Audit solver, varied axes, and independent route | discharged: exact quadrature supplies existence and exposes the source's three-lobe charge contamination |
| A one-point fit may masquerade as an asymptotic theorem | Derive scaled series and test more than one shrinking-amplitude point | discharged: exact scaled operator and peak balance plus three-point approach to the limit |
| Shared sech limits may be called exact object identity | Exhibit finite-frequency residual/normalization distinctions | discharged: EM1's width misses by one-half and its unit profile fails the exact-sine ODE |

## Review and Promotion Plan

The provisional claim receives an independent energy-integral and asymptotic
review. Promotion requires pure APIs/tests, immutable attempts, source and
check-family adjudication, claim-level axes, terminal FG1 disposition,
release/docs/memory synchronization, consumer replay, and one unchanged full
gate.

## Done Gate

P032 closes only when the equation provenance, branch, root, profile, charge,
asymptotics, numerical evidence level, reconciliation scope, mutations,
consumers, source disposition, and campaign debt satisfy the framework
contract.

## Adjudication Result

Candidate A is accepted only as an exact conditional implicit family. Thirty
main and eight independent checks establish the monotone peak root, inverse
profile, finite charge quadrature, and controlled quartic limit. FG1 is
qualified because the pinned source fails at removed `np.trapz`, its long IVP
charge rebounds across the separatrix, its EM1 identity contradicts its own
width residual, and a charge slope is not a stability theorem. All campaign
debt is discharged.
