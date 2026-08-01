---
description: Audit FG2's quartic fluctuation spectrum and family interpretation
author: vantasner
created: '2026-08-01T16:53:00Z'
updated: '2026-08-01T17:01:00Z'
tags:
- substrate-framework
- campaign-proposal
- fluctuation-spectrum
- poschl-teller
- migration-FG2
category: proposals
confidence: exploratory
status: archived
---
# P033 FG2 Quartic Fluctuation Spectrum

## Question and Positive Deliverable

P033 must derive the exact scalar second variation around `C-QBL-001`, close
its bound spectrum, and separate spectral facts from stability and generation
language. The positive deliverable is a reusable conditional Sturm-Liouville
operator and exact spectrum if completeness closes.

## Base Release and Provenance

The accepted base is `v0.28.0` at framework commit `3bc60b3`.
`C-QBL-001` supplies the conditional quartic profile but explicitly withholds
stability. The hash-pinned candidate is FG2 at
`merged-framework/bridges/phase-11/bridge_FG2_family_tower.py`, SHA-256
`aef0ed225fca1f12fcccb284015d97ce3faa25291f07addda24e82ebbc5ae166`.
Memory search found no accepted fluctuation-spectrum claim.

## Invariants, Conventions, and Allowed Imports

The campaign imports only the accepted quartic profile, exact one-dimensional
spectral calculus, and finite differences as regression evidence when properly
refined. Translation modes are collective-coordinate tangents, negative
Hessian eigenvalues are not positive masses, and a particle family requires a
separate state-space and quantum-number map.

## Candidate Preregistration

The candidates are frozen from migration metadata before the full FG2 body is
read.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Exact operator, two bound eigenpairs, completeness, parity, threshold | Declared quartic energy functional | Frequency | Native conditional extension | Second variation, factorization/Sturm count, L2 norms, continuum limit |
| B | Operator and exhibited eigenpairs only | Same functional | Frequency | Selected if completeness is borrowed | Independent factorization and node audit |
| C | Physical generation tower and masses | State map, quantization, quantum numbers | Multiple new dictionaries | Conflicts absent extra structure | Negative mode, zero mode, missing map and consumer tests |

## Selection Criteria and Blinding

Selection is ordered by exact operator derivation, exact eigenpair residuals,
square integrability, complete bound-state count, continuum threshold, parity,
translation identity, correct negative-mode meaning, and assumption economy.
No preferred count or phenomenological generation comparator may select the
candidate.

## Proposed Claim Delta

Provisional `C-QBL-003` would state the conditional quartic Hessian, its exact
two-dimensional bound subspace with eigenvalues `-3*kappa^2` and zero, and its
continuum threshold `kappa^2`. It excludes Q-ball orbital stability, the full
coupled phase/charge Hessian, positive mass assignments, particle families,
Standard-Model quantum numbers, and substrate identity.

## Implementation and Oracle Plan

SymPy will derive the second variation and verify both eigenfunctions. An
independent factorization or Sturm-node route must close completeness and the
threshold. Sparse finite differences will vary mesh and box and check overlap
with exact modes; mutations change the well depth, constant shift, boundary,
and mode parity. Numeric agreement cannot replace the exact count.

## Attempts and Continuation

Attempt `0001` will reproduce FG2 and inspect its action, operator domain,
finite-difference boundary conditions, refinement, exact spectrum import, and
generation map. A missing completeness proof selects Candidate B. A correct
negative/zero spectrum rejects Candidate C rather than converting eigenvalues
to positive masses.

## Debt Ledger

This ledger tracks action provenance, completeness, numerical sensitivity,
stability scope, and family interpretation.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| The Hessian may be asserted without varying a functional | Derive it from an explicit conditional energy density | discharged: the declared quartic energy differentiates to the profile ODE and Hessian |
| Two displayed modes may not prove completeness | Supply factorization or Sturm-Liouville count and continuum threshold | discharged: the s=2 to s=1 to free factorization terminates after two bound seeds |
| Finite-box eigenvalues may be boundary artifacts | Refine mesh and domain against exact modes and threshold | discharged for the quartic pair; FG2's exact-sine third mode is excluded for failing this gate |
| A negative and zero mode may be called stable massive excitations | Separate unconstrained Hessian, symmetry mode, and constrained dynamics | discharged: exact roles are stated and stability/mass readings excluded |
| Mode count may be called a particle-family tower | Audit every state, mass, and quantum-number mapping premise | discharged: no executable particle, mass, or quantum-number map exists |

## Review and Promotion Plan

The provisional claim receives an independent factorization and node review.
Promotion requires pure APIs/tests, immutable evidence, source adjudication,
claim axes, terminal FG2 disposition, release/docs/memory synchronization,
affected consumer replay, and one unchanged full gate.

## Done Gate

P033 closes only when the functional, operator, domain, bound spectrum,
completeness, threshold, parity, translation, negative-mode meaning, numeric
refinement, interpretation boundary, source disposition, and campaign debt all
satisfy the framework contract.

## Adjudication Result

Candidate A is accepted for the quartic scalar Hessian only. Twenty-seven main
and eight independent checks derive and factor the operator, close its complete
two-level bound spectrum, verify the continuum and mode roles, and refine the
finite-difference regression. FG2 is qualified because its exact-sine
background is not localized at the wall, its third level lacks box refinement,
and negative/zero Hessian levels are not particle generations or positive
masses. All campaign debt is discharged.
