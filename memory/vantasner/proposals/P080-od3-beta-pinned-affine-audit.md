---
description: Derive an exact affine-pinning and compatibility ledger and audit OD3
author: vantasner
created: '2026-08-03T17:30:00Z'
updated: '2026-08-03T18:15:00Z'
tags:
- substrate-framework
- campaign-proposal
- scale-identifiability
- migration-OD3
category: proposals
confidence: exploratory
status: archived
---
# P080 OD3 Beta-Pinned Affine Audit

## Question and Positive Deliverable

P080 must produce an exact, reproducible affine-pinning ledger for a supplied
four-row, two-coordinate log system after one coordinate is assigned a
separately supplied value. The positive object must expose the transformed
right-hand side, coefficient and augmented ranks, complete compatibility
conditions, conditional solution, reference covariance, and nuisance-
restoration behavior. It must then decide whether OD3 derives a physically
selected absolute scale or only conditions an existing supplied system.

## Base Release and Provenance

The accepted base is `v0.72.0` at scientific commit `52e05eb`; parent-effort
synchronization is commit `8bb113f`. The predecessor is pinned at
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`. OD3 is
`/home/dan/substrate/merged-framework/bridges/phase-22/bridge_OD3_beta_pinned.py`,
20906 bytes, with SHA-256
`af96fa76a30c9ebb863e0a50b605ade5003a7595f28188ce7ca4d0884d67910c`
and predecessor blob `6834f14a12f083b29c7e7ef97d9ceb1ffb5e3e1f`.
The queue marks OD3 pending and names AS1-AS7, CF4, G1, G2, G5, OD, QCD3,
and S5. Release v0.72.0, C-LIN-001, C-IDN-001, C-SYM-002, C-DIM-008,
C-RGE-003, C-GRV-001, C-IDN-002, their canonical linear/scale/duality
modules, the P075 immutable adjudication, git history and clean state,
predecessor status, queue metadata, and repository-scoped memory results were
checked. Only the generated synopsis was opened; the OD3 body, literal
comparators, output, and pending dependency bodies remain closed.

## Invariants, Conventions, and Allowed Imports

Every matrix, right-hand side, pin value, shift, and compatibility residual is
an exact real SymPy object. C-LIN-001 separates a tall coefficient matrix from
consistency and uniqueness. C-IDN-001 makes coordinate identification
conditional on compatibility and preserves row provenance under reference
changes. C-SYM-002 permits the algebraic value `beta^2=4*pi` only after a
reciprocal coefficient and fixed-subfamily restriction are supplied; it does
not select occupancy or a physical coupling normalization. C-DIM-008 denies
AS5's absolute-scale closure. C-RGE-003, C-GRV-001, and C-IDN-002 retain their
accepted coefficients, targets, baselines, conversions, and inverse-
construction ceilings. Pending sector equations, observed values, source
independence labels, metre conventions, fitted offsets, and physical
identifications are not imports.

## Candidate Preregistration

The candidates are frozen before the OD3 source body, output, literal
comparators, or pending dependency bodies are opened.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal OD3 promotion | AS5 generates an absolute scale, AS6 physically pins beta, and all four rows are accepted independent constraints | Source constants and targets | One remaining coordinate is physically identified and overdetermined | Dependency and data-flow audit |
| B | Exact affine substitution | A two-coordinate system and pin value are supplied | One free coordinate and one supplied pin | Pinning moves a known column contribution to the right-hand side | Exact substitution and round trip |
| C | Rank-one compatibility ledger | Four affine rows are supplied | Four transformed right-hand sides | Rank one leaves three left-null relations; a solution is unique only when all hold | Exact nullspace, augmented ranks, and elimination |
| D | Nuisance-restored system | Beta, sector offsets, coefficients, baselines, and references are not silently fixed | Free coordinate plus declared nuisances | Added parameter directions can remove compatibility or reopen nonidentifiability | Expanded-matrix ranks and nullspaces |
| E | Reference-covariant ledger | The same physical rows are represented under a declared log-reference shift | Coordinate shift | Compatibility residuals persist while numeric coordinate and right-hand sides transform | Exact conjugation and wrong-shift mutation |
| F | Same-rank countermodels | Coefficient column is fixed while right-hand sides or row provenance change | Mutated supplied data | Rank one survives both compatible and incompatible/nonphysical cases | Augmented-rank and provenance counterexamples |
| G | Duplicate specialization | Accepted linear and identifiability theorems apply without extra structure | Accepted claims only | OD3's exact surviving content is a specialization, not a new claim | Complete claim/API comparison |

## Selection Criteria and Blinding

Selection is ordered by accepted dependency closure, exact affine and
left-null algebra, explicit parameter and row provenance, distinction between
conditioning and selection, reference covariance, dimensional and limiting
consistency, mutation sensitivity, nuisance economy, and reuse of accepted
APIs. Numerical agreement, supplied observed values, the source verdict, and
later consumer prose cannot select a candidate. They stay blinded until both
contract representations, their hashes, and the pre-source repository gate
are frozen.

## Proposed Claim Delta

No new claim is presumed. OD3's rank, compatibility, and coordinate-status
statements appear to specialize C-LIN-001 and C-IDN-001, while its beta pin and
absolute-scale premise conflict with the ceilings in C-SYM-002 and C-DIM-008.
A provisional affine-parameter-pinning claim may be opened only if the source
reveals a reusable exact object not already entailed by substitution followed
by `diagnose_log_constraints`. No physical gravity, medium, hadronic,
confinement, QCD, duality, coupling-selection, or absolute-scale claim is in
scope without separately accepted closure.

## Implementation and Oracle Plan

SymPy exact algebra is the strongest oracle because the complete advertised
object is a finite affine linear system. The primary route will call
`linear_systems`, `scale_constraints`, and the accepted reciprocal ledger to
derive substitution, round trip, coefficient/augmented ranks, the full
left-nullspace, compatibility residuals, conditional solution, reference
shifts, and nuisance-restored branches. An independent route will reconstruct
the substitution and eliminate rows without importing campaign helpers or any
new canonical function. Mutations will alter the pin, reciprocal coefficient,
one exponent, each dependent right-hand side, a reference shift, an offset,
an induced-gravity baseline, and provenance labels. A same-rank compatible
and inconsistent pair will prevent rank-only validation. No ODE, PDE,
simulation, floating fit, or numerical quadrature is needed; neither
`np.trapz` nor `np.trapezoid` will appear.

## Attempts and Continuation

Attempt 0001 will hash-check and reproduce OD3 only after both contracts and
their freeze metadata validate, then audit its load-bearing data flow. A
failed absolute-scale or beta-selection headline will not close P080;
Candidates B-G continue to the positive exact affine and compatibility
ledger. Technical, representation, candidate, and source-claim failures will
remain append-only with reproduction commands and continuation decisions.

## Debt Ledger

The campaign tracks affine-substitution, compatibility, beta-provenance,
absolute-scale, row-provenance, nuisance, reference, duplication,
verification, and synchronization debt.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| Moving a pinned coordinate to the right-hand side may be called new information | Derive the affine substitution and exact inverse round trip | discharged; exact conditioning adds no row information |
| Rank one in one unknown may be called physical over-determination | Derive augmented-rank branches and all three left-null compatibility relations | discharged; generic source RHS is inconsistent |
| The AS6 fixed coordinate may be treated as selected occupancy | Audit reciprocal coefficient, normalization, and fixed-subfamily provenance | discharged by C-SYM-002 and coordinate-conjugation counterexamples |
| AS5 may be used as an absolute-scale closure | Replay C-DIM-008's reference and conversion ledger against OD3 | discharged; dimensionful reference and conversion remain |
| Four sector rows may be called independent physical constraints | Audit every row, coefficient, right-hand side, provenance label, and covariance premise | discharged; all remain supplied and no covariance exists |
| Fixed offsets, baselines, or beta may hide nuisance directions | Restore representative nuisances and recompute rank and nullity | discharged by re-floating, row-offset, and gravity-baseline branches |
| A coordinate value may be confused with a reference-invariant observable | Derive exact log-reference covariance and residual invariance | discharged; residuals persist while the coordinate shifts |
| A duplicate specialization may be promoted | Compare the complete surviving object with accepted claims and P075 | discharged; C-LIN-001 and C-IDN-001 already own it |
| Sensitive verification, review, and synchronization are incomplete | Complete mutations, independent route, disposition, replay, and generated consistency | discharged by the P080 terminal gate |

## Review and Promotion Plan

An independent reviewer will reconstruct the pinned affine system, all three
compatibility equations, compatible/incompatible branches, pin and reference
covariance, nuisance restoration, and source dependency inventory. OD3 will
receive a structured terminal disposition through
`migration/dispositions.yaml`, followed by generated queue synchronization.
Reusable code and package tests are added only for a nonduplicate surviving
claim; otherwise the campaign reuses accepted APIs and the release remains
unchanged. Any promoted claim requires individual registry review, a pinned
release, generated docs and accepted memory, affected-consumer replay, and one
unchanged full workflow boundary. Final attempt metadata is completed after
that gate and followed only by record-sensitive validation.

## Done Gate

P080 closes only when the positive affine-pinning and compatibility object
exists, every OD3 predicate is mapped or rejected, beta and scale premises
retain provenance, exact mutations and an independent route pass, the unit has
a durable disposition, all affected consumers replay, generated state agrees,
and campaign debt is empty. The parent migration remains active until all 140
currently pending units are adjudicated.

## Outcome

P080 retains OD3 as duplicate evidence for C-LIN-001 and C-IDN-001 without a
new claim, API, or release. Exact affine substitution leaves a rank-one column
with three compatibility conditions; the generic source system is
inconsistent, while a compatible branch identifies one coordinate only
conditionally. Four pi and the source's later 0.245 correction both lack
physical selection closure, b0 and row offsets remain free, and the accepted
gravity baseline can invalidate the first row. Thirty-six primary and twenty-
two independent checks, 102 affected tests, 17 governance tests, and the
integrated 755-test workflow pass. All campaign debt is discharged; the
parent effort continues with 140 pending units.
