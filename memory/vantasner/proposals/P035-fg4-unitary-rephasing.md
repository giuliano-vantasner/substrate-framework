---
description: Audit FG4's unitary rephasing counts and CP interpretation
author: vantasner
created: '2026-08-01T17:24:02Z'
updated: '2026-08-01T17:32:26Z'
tags:
- substrate-framework
- campaign-proposal
- unitary-rephasing
- invariant-quartet
- migration-FG4
category: proposals
confidence: exploratory
status: archived
---
# P035 FG4 Unitary Rephasing Audit

## Question and Positive Deliverable

P035 must derive the quotient and invariant structure of an `N`-by-`N`
unitary matrix under independent diagonal phase changes, including the action's
kernel, nongeneric stabilizers, and `N=2,3` limits. The positive deliverable is
reusable exact rephasing mathematics with an explicit boundary between
complex-conjugation-odd algebra and physical CP violation.

## Base Release and Provenance

The accepted base is `v0.30.0` at framework commit `256e784`. `C-MIX-001`
supplies an abstract relative unitary matrix but explicitly excludes CKM,
family, current, and CP-phase interpretations. The pending hash-pinned candidate
is FG4 at `merged-framework/bridges/phase-11/bridge_FG4_cp_kobayashi_maskawa.py`,
SHA-256 `d9ebb32d440fb87540c7cb2d02a846b76dd4ee405288895308561762cd720ceb`.
Bundled-memory search found no accepted framework result for FG4, Jarlskog
quartets, or rephasing quotients; every reused fact will be rederived.

## Invariants, Conventions, and Allowed Imports

The campaign imports `C-MIX-001`, exact finite-dimensional unitary and torus
algebra, and FG4 only as evidence. The rephasing action is frozen as
`V -> D_L V D_R^dagger`. Its common scalar kernel must be factored, and orbit
dimensions may fall when a matrix's nonzero support has extra stabilizers.
Complex conjugation is an algebraic involution here; calling it physical CP
requires separately accepted fields and an interaction. No family count or
empirical phase value may enter the derivation.

## Candidate Preregistration

The alternatives are frozen from queue metadata before the full FG4 body or
any named comparison value is inspected.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Generic rephasing quotient, angle/phase split, N=2 real representative, N=3 invariant quartet | Unitary matrix, declared diagonal action, generic connected support where stated | Integer N and matrix entries | Native extension of C-MIX-001 with explicit strata | Kernel/stabilizer rank, exact low-N construction, invariant and conjugation tests |
| B | Budget identity and quartet invariance only | Formal integer N or one unitary matrix | Integer N and entries | Selected if quotient or representative claims overreach | Counterexamples from zero patterns and residual phase action |
| C | Physical KM mechanism and observed CP violation | Quark families, Yukawas, charged current, physical CP map | Textures, family count, phase values | Dependency conflict | Accepted-claim closure and arbitrary-unitary counterexamples |

## Selection Criteria and Blinding

Selection is ordered by exact action and kernel, generic stabilizer, quotient
dimension, nonnegative integer low-`N` counts, explicit two-dimensional real
representatives, exact three-dimensional unitarity and quartet formula when
used, rephasing invariance, conjugation sensitivity, and assumption economy.
Named measured angles or CP values remain blinded until those structural gates
and the physical interpretation boundary are frozen.

## Proposed Claim Delta

Provisional `C-MIX-002` would state the effective generic dimension of the
left/right diagonal rephasing action on `U(N)`, its conventional decomposition
into orthogonal angles and irreducible phases, the `N=2` real-representative
result, and a rephasing-invariant quartet whose imaginary part changes sign
under conjugation. It will state the generic-stratum qualifier and exclude a
physical CKM matrix, quark rephasing license, generation count, CP symmetry,
CP violation, observed invariant, anomaly statement, or substrate mechanism.

## Implementation and Oracle Plan

Pure APIs will expose count diagnostics, the diagonal rephasing action, support
stabilizer rank, and invariant quartets without particle labels. SymPy will
verify polynomial counts, kernels, low-dimensional representatives, exact
unitarity, rephasing cancellation, and conjugation oddness. Mutations will
remove the common kernel, reverse only one phase, break unitarity, alter a
quartet conjugation, and probe diagonal/permutation support with enhanced
stabilizers. An independent graph-incidence and direct parameterization route
will avoid the proposing implementation.

## Attempts and Continuation

Attempt `0001` will reproduce FG4 and inventory each claimed count, phase
action, `N=2` result, `N=3` matrix, invariant, guard, and physical import.
Failure of a global quotient claim selects a generic-stratum repair or
Candidate B; it will not be hidden by evaluating only dense examples. Failure
of physical closure rejects Candidate C while work continues on the positive
mathematical object.

## Debt Ledger

This ledger tracks group-action effectiveness, strata, parameterization,
invariant sensitivity, and physical interpretation.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| Subtracting `2N-1` may ignore matrix-dependent stabilizers | Derive the action kernel and support-graph stabilizer dimension, then state the generic scope | discharged: incidence rank gives stabilizer dimension c and orbit 2N-c, with 2N-1 only for connected support |
| The angle/phase split may be only a polynomial rearrangement | Relate it to orthogonal dimension and residual quotient dimension | discharged: exact Lie dimensions and the generic quotient derive both terms |
| The `N=2` zero-phase result may be asserted from one real example | Construct rephasings for a general two-by-two unitary or supply an equivalent exact theorem | discharged: the general phase-dressed rotation is rephased to real and its quartet vanishes identically |
| A quartet may be invariant only because phases were numerically fixed | Verify symbolic phase cancellation and mutation sensitivity | discharged: symbolic cancellation passes and wrong conjugation/index mutations fail |
| Algebraic conjugation oddness may be called observed physical CP violation | Audit fields, interactions, family count, and comparators against `v0.30.0` | discharged: no physical dependencies or comparator enter, and the claim excludes the physical reading |

## Review and Promotion Plan

The provisional claim receives an independent support-graph and invariant
review. Promotion requires pure APIs/tests, immutable attempt evidence,
claim-level adjudication, a terminal FG4 disposition, release/docs/memory
synchronization, targeted replay, and one unchanged full repository gate.

## Done Gate

P035 closes only when the action, kernel, strata, dimensions, low-`N` limits,
invariant, conjugation behavior, mutations, dependency boundary, source
disposition, consumers, and debt all satisfy the framework contract.

## Adjudication Result

Candidate A is accepted as `C-MIX-002`. Thirty-one main and nine independent
checks derive the generic quotient, exceptional support stabilizers, low-`N`
structure, exact invariant, and conjugation behavior. FG4 is qualified because
its `2N-1` language omits nongeneric strata and its degenerate-basis, field,
interaction, family, and physical-CP dependencies are absent. All campaign
debt is discharged.
