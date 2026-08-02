---
description: Classify AS4's declared over-determination system without promoting supplied rows into physical predictions
author: vantasner
created: '2026-08-02T18:53:16Z'
updated: '2026-08-02T19:08:02Z'
tags:
- substrate-framework
- campaign-proposal
- scale-identifiability
- migration-AS4
category: proposals
confidence: exploratory
status: archived
---
# P075 AS4 Over-Determination-v2 Audit

## Question and Positive Deliverable

P075 must produce an exact, reproducible classification of AS4's declared
four-row, two-coordinate system: coefficient and augmented ranks, right and
left nullspaces, compatibility conditions, coordinate status, nuisance-
parameter sensitivity, and covariance requirements. It must then terminally
adjudicate AS4 and map every surviving predicate to accepted claims or a
genuinely nonduplicate claim without calling supplied physical right-hand
sides predictions.

## Base Release and Provenance

The accepted base is `v0.68.0` at scientific commit `9b5d99d`; parent-effort
synchronization is commit `3321097`. The predecessor is pinned at
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`. AS4 is
`/home/dan/substrate/merged-framework/bridges/phase-21/bridge_AS4_over_determination_v2.py`,
17278 bytes, with SHA-256
`cdcfea3ac26c932a3db792c864baa026c761555d3c0e34c7b1bc025ea962745f`;
the byte count and hash matched the pinned blob before execution. The queue
marked AS4 pending and named AS1-AS3, CF4, G1, G2, G5, M1, M2, OD, QCD3,
QCD5, and S5. Release v0.68.0, C-LIN-001, C-IDN-001, C-GLS-001, C-RGE-003,
C-GRV-001, their canonical modules and accepted reviews, git state, the queue
metadata, and durable-memory search results were inspected on a clean tree
before this contract. Only the generated synopsis and prior accepted claim
summaries were opened at preregistration; no empirical comparator was later
needed or opened.

## Invariants, Conventions, and Allowed Imports

All matrices and right-hand sides are exact real SymPy objects. C-LIN-001
separates equation count, coefficient rank, augmented rank, consistency, and
uniqueness. C-IDN-001 makes coordinate identification conditional on a
consistent supplied log system, keeps row provenance explicit, and treats a
left-null relation as a compatibility condition rather than proof of row
origin or independence. C-GLS-001 requires a declared positive-definite
covariance. C-RGE-003 and C-GRV-001 may supply only their accepted conditional
rows and ceilings. Pending sector narratives, observed values, fitted
constants, source assertions of independence, and later AS5 conclusions are
not imports.

## Candidate Preregistration

The candidates are frozen before the AS4 source body or any comparator is
opened.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal AS4 promotion | Every cited sector fixes its row and the four rows are physically independent | Source coordinates and right-hand sides | Full column rank may identify both coordinates | Dependency and data-flow audit |
| B | Exact declared-system classification | AS4's symbolic matrix and right-hand side are supplied data | Two coordinates | Two directions can coexist with zero, one, or no solutions depending on compatibility | Exact ranks and nullspaces |
| C | Primary rows plus compatibility predictions | Two rows are selected as a spanning basis | Two coordinates and four supplied right-hand sides | Remaining rows impose two left-null conditions, not two new directions | Exact elimination and independent rederivation |
| D | Nuisance-restored model | Sector constants, offsets, or induced coefficients are not silently fixed | Two coordinates plus declared nuisances | Additional null directions can reopen | Expanded-matrix rank and mutation probes |
| E | Covariance-aware crosscheck | A positive-definite covariance is explicitly supplied | Residuals and covariance | GLS can score compatibility but not create row provenance | Whitening and covariance-rescaling tests |
| F | Inconsistent or fabricated rows | Coefficient directions are preserved while right-hand sides or provenance are perturbed | Mutated supplied data | Full column rank survives while consistency or physical inference fails | Augmented-rank and provenance counterexamples |

## Selection Criteria and Blinding

Selection is ordered by accepted dependency closure, exact coefficient and
augmented ranks, explicit right/left nullspaces, parameter and nuisance
inventory, row provenance and covariance, mutation sensitivity, natural
framework fit, and reuse economy. No empirical observable, fitted constant,
later AS5 operating point, or source verdict may select the concept or enter a
right-hand side. The queue synopsis supplies symbolic navigation metadata
only; the source body remains closed until both contract representations are
committed to the working tree and validate.

## Proposed Claim Delta

No new claim is presumed. AS4's coefficient-rank, compatibility,
identifiability, and declared-covariance predicates appear to specialize
C-LIN-001, C-IDN-001, and C-GLS-001. A new claim may be proposed only if the
source contains a reusable exact object not entailed by those accepted claims
and it survives independent mutation-sensitive verification. Physical
gravity, medium, hadronic, confinement, absolute-scale, or operating-point
claims remain outside the delta without accepted dependency closure.

## Implementation and Oracle Plan

SymPy exact algebra is the strongest oracle because every advertised
obligation is a finite symbolic linear-system statement. Thin campaign code
will call `linear_systems` and `scale_constraints`; no duplicate canonical API
will be added unless a nonduplicate object survives. The primary route will
derive coefficient rank, augmented-rank branches, right and left nullspaces,
compatibility residuals, coordinate status, and nuisance expansions. An
independent route will row-reduce and eliminate by hand-coded exact operations
without importing campaign helpers. Mutations will alter a coefficient row,
perturb each dependent right-hand side, restore sector nuisances, duplicate a
row, and change covariance correlations or scale. Provenance counterexamples
will keep the same matrix while replacing the asserted physical origin. No
numerical integration is needed; neither `np.trapz` nor another NumPy
quadrature alias will appear.

## Attempts and Continuation

Attempt 0001 preserves the failed repository-relative interpreter path.
Attempt 0002 reproduces the source with `ALL 7 CHECKS PASS` and exposes its
missing augmented-rank, provenance, nuisance, covariance, and sensitivity
gates. Attempt 0003 preserves a signed-determinant expectation and a
shape-mismatched RREF comparison; both were verifier representations, not
scientific equations. Attempt 0004 records 28 primary and 16 independent exact
checks, 78 affected canonical tests, 17 focused governance tests, and the
single integrated 689-test workflow boundary.

## Debt Ledger

The campaign tracks rank, compatibility, provenance, independence, nuisance,
covariance, dependency, verification, and synchronization debt.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| Tall or full-column-rank structure may be called physical over-determination | Separate row count, coefficient rank, augmented rank, and consistency | discharged by the coefficient/augmented-rank branches |
| Supplied right-hand sides may be called predictions | Trace every right-hand side and distinguish inverse inference from prediction | discharged by the left-null and supplied-data ledger |
| Row provenance and independence may be asserted | Audit every cited dependency and require accepted origin or retain it as source premise | discharged; labels remain noncanonical premises |
| Sector coefficients or offsets may be silently fixed | Restore representative nuisance coordinates and recompute rank/nullity | discharged by the rank-four over five-coordinate countermodel |
| Redundant-row residuals may be treated statistically without covariance | Require declared covariance or limit the verdict to exact compatibility | discharged through the C-GLS-001 ceiling |
| A duplicate specialization may be promoted as a new claim | Compare the complete object against C-LIN-001, C-IDN-001, and C-GLS-001 | discharged; no claim or API is added |
| Sensitive verification, review, and synchronization are incomplete | Complete mutations, independent route, source disposition, replay, generated synchronization, and memory validation | discharged at the terminal AS4 queue boundary |

## Review and Promotion Plan

The review will independently reconstruct the AS4 matrix, derive both
compatibility relations, perturb the right-hand side, restore nuisance
coordinates, and audit source provenance and covariance. AS4 receives a
terminal disposition through `migration/dispositions.yaml`, followed by queue
regeneration. A terminal qualified or duplicate-evidence decision must name
its structured reason and durable campaign evidence. Promotion of any new
claim requires individual review, dependency closure, package tests, a pinned
release, generated documentation and accepted-memory synchronization. If no
new claim survives, the existing release remains current and only the source
disposition and generated queue change.

## Done Gate

P075 is complete. The positive exact classification exists, every source
predicate has a terminal mapping or rejection rationale, 28 primary and 16
independent checks pass, 78 affected canonical and 17 focused governance tests
pass, and the single integrated workflow passes all 689 tests. AS4 is durable
duplicate evidence for C-LIN-001 and C-IDN-001; the regenerated queue reports
145 pending, 65 qualified, and 4 duplicate units. Release v0.68.0 and its 96
accepted claims are unchanged, campaign debt is empty, and parent migration
debt remains active.

## Outcome

Candidates B and C recover AS4's exact two-direction, two-compatibility
specialization, already accepted in C-LIN-001 and C-IDN-001. Candidates D-F
show why the physical headline does not survive: generic right-hand sides are
inconsistent, source predicates miss load-bearing mutations, admitted nuisance
coefficients reopen a mixed null direction, an allowed inverse-G baseline
breaks the gravity row, and neither provenance nor covariance is supplied. No
new claim, API, release, numerical integration, deprecated `np.trapz`, or
version-specific replacement alias is introduced.
