---
description: Derive and audit exact conditional Goldstone Hessian zero modes
author: vantasner
created: '2026-08-02T18:10:00Z'
updated: '2026-08-02T19:00:00Z'
tags:
- substrate-framework
- campaign-proposal
- goldstone-hessian
- migration-PG1
category: proposals
confidence: established
status: archived
---
# P060 PG1 Goldstone-Hessian Audit

## Question and Positive Deliverable

P060 must deliver a reusable exact theorem that begins with an actually
invariant scalar potential and an actual nonzero stationary vacuum, derives
the Hessian kernel along independent broken-generator tangents, and states the
additional kinetic premise needed to call those quadratic modes massless. It
must specialize the theorem to a declared O(4) radial quartic model and derive
the quadratic SU(2) derivative-action normalization. It must separately decide
whether PG1 establishes the physical pion identification advertised in its
headline. A source failure, a scope ceiling, or a no-go for that physical
identification cannot complete the campaign; the exact conditional symmetry
object remains the positive deliverable.

## Base Release and Provenance

The accepted base is `v0.53.0` at framework commit `c041831`, whose scientific
transaction is `2740073`. The pinned predecessor is
`substrate@6d1f4e0`; PG1 is
`/home/dan/substrate/merged-framework/bridges/phase-18/bridge_PG1_pion_goldstone_massless.py`
with verified SHA-256
`a51ecc1833cd166bbef5aa799d2ab9eacc453b088660dbb98426591a7157aa74`.
The predecessor's later uncommitted artifacts remain outside this source unit.
PG1 is pending. Its named PG2, PG4, and S2 dependencies are pending and supply
no accepted premise. The fresh skill preflight passes seven checks without
warnings, the framework worktree is clean, and memory supplies only the
accepted frontier and next-unit pointer. The generated inventory synopsis
necessarily exposes PG1's claimed O(4) Hessian, derivative-only SU(2) action,
and broken-dimension count; the executable's equations, conventions, checks,
and values remain unopened at this contract boundary.

## Invariants, Conventions, and Allowed Imports

The accepted framework contains no chiral group action, O(4) scalar
multiplet, condensate, pion field, decay constant, QCD vacuum, explicit
breaking term, or physical pion spectrum. That absence is invariant rather
than a gap that may be filled by names. A stationary-potential Hessian zero, a
zero generalized mass eigenvalue after supplying a kinetic metric, a
derivative-only field coordinate, a quantum Goldstone particle, and the
physical pion are separate obligations.

Allowed mathematics is exact multivariate calculus, real finite-dimensional
linear algebra, linear continuous symmetry generators, positive-definite
quadratic kinetic metrics, Pauli traces, and exact symbolic series. Primary
Goldstone literature may delimit the external theorem's hypotheses and
conclusion, but it cannot supply a physical framework sector by citation.
PG2, PG4, S2, physical `F_pi`, a condensate value, measured masses, QCD
dynamics, and a substrate-to-chiral-field map are forbidden inputs.

## Candidate Preregistration

The candidate set is frozen before opening PG1's executable internals.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal PG1 reproduction | Every headline noun must resolve to a computed field, transformation, vacuum, action, and spectrum | Source symbols only | May prove model algebra while importing the physical identification through names | Hash-pinned execution, data-flow audit, and coefficient/name mutations |
| B | General infinitesimal-symmetry Hessian theorem | Differentiable potential invariant under declared linear generators; stationary vacuum | Potential, fields, vacuum, generators, optional positive kinetic metric | Every independent nonzero orbit tangent lies in the Hessian kernel; rank of the tangent matrix counts the certified zero directions | Differentiate the invariance residual, evaluate gradient/Hessian/tangents, and break invariance or stationarity |
| C | Explicit O(4) orbit and radial quartic | Four real fields, all six antisymmetric O(4) generators, potential `lambda*(phi.phi-v^2)^2`, nonzero chosen vacuum | `lambda`, `v`, kinetic normalization | Three broken tangents and Hessian spectrum `(8*lambda*v^2,0,0,0)` for the declared convention; symmetric and explicitly broken mutations change the result | Direct Cartesian Hessian, orbit-tangent rank, stabilizer kernel, characteristic polynomial, and mass-term mutation |
| D | SU(2) exponential derivative action | Declared `U=exp(i*tau.pi/F)` coordinate model and action prefactor | `F` and prefactor | Generator traces derive the quadratic kinetic metric; no potential means zero mass Hessian, while another prefactor rescales kinetics and an added mass term lifts it | Independent Pauli expansion, trace Gram matrix, prefactor conversion, and potential mutation |

## Selection Criteria and Blinding

Selection is ordered by accepted-invariant compatibility, proof from actual
symmetry and stationarity objects, explicit kinetic/potential normalization,
assumption and parameter economy, tangent-rank completeness, correct
dimensions and limits, mutation sensitivity, and independent rederivation. No
empirical mass, decay constant, or phenomenological comparator is needed or
permitted to select this exact structural theorem. Inventory-exposed target
values are barred from fixing the potential coefficient, vacuum direction,
kinetic prefactor, or physical field dictionary.

## Proposed Claim Delta

Provisional C-SYM-001 may state the exact linear-symmetry theorem: if the
directional invariance identities vanish identically and the vacuum gradient
vanishes, differentiating those identities forces the Hessian to annihilate
every generator tangent. The rank of the tangent matrix is the number of
independent certified zero directions; a positive kinetic metric converts
them into zero generalized quadratic masses. It will state failure at a
nonstationary point and under explicit symmetry breaking.

Provisional C-CHI-001 may state only the declared O(4) radial-quartic and SU(2)
derivative-action specializations with their precise coefficients and
convention conversions. Neither claim may identify a field as a physical pion,
derive chiral symmetry or its vacuum breaking from the substrate, establish a
quantum particle theorem, select `F_pi`, include explicit breaking, predict a
mass, or import PG2/PG4/S2.

## Implementation and Oracle Plan

A pure `src/substrate_framework/symmetry_breaking.py` module will expose
actual invariance residuals, gradients, Hessians, generator-tangent matrices,
kernel residuals and ranks, the O(N) radial-quartic specialization, and the
leading group-coordinate kinetic metric derived from generator traces. It
will print nothing and execute no simulation on import. SymPy exact algebra is
the strongest oracle because every obligation is a finite derivative, matrix,
rank, series, or polynomial identity.

The canonical route will differentiate the supplied potential and generators.
An independent review will derive the Hessian theorem from the differentiated
Noether identity without importing canonical helpers, build all six O(4)
generators from index pairs, and reconstruct the Pauli kinetic Gram matrix
from explicit matrices. Mutations add an anisotropic or isotropic mass term,
move off the stationary vacuum, set the vacuum to the symmetric point, remove
or change the quartic normalization, use dependent or unbroken generators,
and change the SU(2) prefactor. Each relevant verdict must respond. Exact
dimensions will keep field, vacuum, derivative, potential, and Hessian mass
dimensions separate in four spacetime dimensions.

GitNexus impact analysis precedes the additive canonical module, followed by
focused tests, both campaign verifiers, affected governance consumers, one
full promotion-boundary workflow gate, and `git diff --check`. No numerical
simulation or quadrature is planned because exact algebra decides the claims.

## Attempts and Continuation

The append-only ledger contains three attempts. Attempt 0001 reproduces PG1's
native four-check tally and rejects it as a positive physical-pion route while
preserving the exact declared-model algebra. Attempt 0002 implements Candidates
B through D canonically and passes twelve focused tests; two initial SymPy
expression-tree comparisons were repaired by exact simplified residuals
without changing any result. Attempt 0003 independently derives the arbitrary-
potential identity, complete O(4) orbit and stabilizer, Pauli normalization,
classical mode equation, and mutations without canonical helpers. Its two
initial representation defects are preserved, and the repaired route passes
24 checks. B, C, and D are selected; A remains rejected as the advertised
physical mechanism.

## Debt Ledger

This ledger tracks source provenance, actual symmetry identities, stationarity,
generator completeness, tangent rank, Hessian and kinetic conventions,
explicit-breaking sensitivity, Goldstone interpretation, pending dependencies,
independent evidence, consumers, and canonical synchronization.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| PG1's literal action, symmetry, vacuum, Hessian, kinetic convention, count, and tally are unaudited | Hash-check, execute, trace every subclaim to its defining object, and preserve output or failure | discharged by source reproduction, audit, and attempt 0001 |
| The positive symmetry-Hessian theorem is not implemented | Derive invariance residuals, stationarity, tangent matrix, Hessian kernel, rank, and generalized kinetic conclusion in a tested importable API | discharged by `symmetry_breaking.py`, focused tests, and attempts 0002/0003 |
| The advertised count may be dimension-label arithmetic | Construct every generator and compute the actual vacuum-tangent rank and stabilizer kernel | discharged by the six-generator tangent map and independent nullspace review |
| O(4) coefficients and SU(2) normalization may be copied | Independently differentiate the radial potential and derive the Pauli trace Gram matrix under both prefactor conventions | discharged by canonical and independent exact derivations |
| Zero Hessian curvature may be mislabeled a physical particle | Audit the theorem hypotheses and maintain the classical quadratic, quantum, and physical-pion interpretation ceilings | discharged by separate C-SYM-001/C-CHI-001 reviews and source adjudication |
| Explicit breaking, symmetric vacuum, or nonstationarity may defeat the result | Require load-bearing mutations and preserve their changed Hessians or failed kernel residuals | discharged by tilt, anisotropy, symmetric-vacuum, and off-stationary mutations |
| Pending PG2/PG4/S2 or phenomenological pion data may leak into the result | Keep the accepted dependency closure empty unless a separately accepted claim is genuinely required | discharged by C-SYM-001's empty closure and C-CHI-001's sole C-SYM-001 dependency |
| Downstream impact and independent evidence are unknown | Complete graph impact analysis, independent rederivation, targeted consumer replay, and source qualification | discharged by LOW additive risk, 24 independent checks, focused replay, and PG1 qualification |
| Registry, release, docs, migration queue, and durable memory are unsynchronized | Review claims individually, regenerate canonical consumers, and empty this ledger | discharged by the v0.54.0 promotion transaction and canonical generators |

## Review and Promotion Plan

C-SYM-001 and C-CHI-001 received separate claim reviews over the raw residuals,
generator matrices, Hessian kernels, ranks, kinetic Gram matrices, mutations,
source data flow, and primary-theorem scope. Both exact claims move into the
package and release v0.54.0 with generated docs and accepted memory. PG1 is
qualified because conditional model mathematics survives but its physical
pion, quantum, GMOR, and substrate narratives do not. The editable migration
disposition is the only hand-authored queue input; `source-claims.yaml` is
regenerated mechanically.

## Done Gate

P060 closes with C-SYM-001 and C-CHI-001 accepted in v0.54.0 and PG1 qualified
after the positive exact theorem, O(4) and SU(2) specializations, sensitivity,
independent review, source adjudication, dependency replay, canonical
synchronization, and empty campaign debt ledger pass. The parent corpus
migration remains active because 160 queue units remain pending.
