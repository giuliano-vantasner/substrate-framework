---
description: Derive a reference-explicit scale-provenance ledger and audit AS5's no-import claim
author: vantasner
created: '2026-08-02T19:12:00Z'
updated: '2026-08-03T11:30:00Z'
tags:
- substrate-framework
- campaign-proposal
- scale-provenance
- migration-AS5
category: proposals
confidence: exploratory
status: archived
---
# P076 AS5 Scale-Provenance Audit

## Question and Positive Deliverable

P076 must produce an exact, importable provenance ledger for the formal one-
loop scale `Lambda`, its inverse-energy length, the M,L,T span of `c` and
`hbar`, finite reference rescaling, arbitrary-target reconstruction, and unit-
coordinate covariance. It must terminally determine whether AS5 predicts an
absolute dimensionful scale or instead transforms a supplied boundary scale
and dimensionless inputs.

## Base Release and Provenance

The accepted base is `v0.68.0` at scientific commit `4d68afc`; parent-effort
synchronization is commit `e73d2e5`. The predecessor is pinned at
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`. AS5 is
`/home/dan/substrate/merged-framework/bridges/phase-22/bridge_AS5_scale_generated_not_imported.py`,
16696 bytes, with SHA-256
`7b2399f5fb61dad1ac692fb8a809e8a0429359b2264ee1b8a3899de504ab3bea`.
The queue marks AS5 pending and names AS1, AS4, CF4, and QCD3. Release
v0.68.0, C-DIM-001, C-RGE-001, C-RGE-003, C-IDN-001, their canonical modules,
tests, reviews, P025 and P073 evidence, git state, queue metadata, and durable-
memory search results were inspected on a clean tree before this contract.
Only the generated synopsis was opened; AS5's source body and later values
remain closed.

## Invariants, Conventions, and Allowed Imports

Dimensions use M,L,T row order. The primitive columns are `c=(0,1,-1)` and
`hbar=(1,2,-1)`; a length target is `(0,1,0)`. Dimensionless numbers add no
dimension column. C-RGE-001 retains positive `mu0`, `g0`, and `b0` and gives a
formal scale relative to `mu0`; C-RGE-003 retains conversion factors and a
common absolute rescaling. C-IDN-001 does not turn a supplied reference or
coordinate equation into a physical prediction. AS4 has no accepted physical
scale row. A unit coordinate, a physical dimensionful quantity, and a
parameter-free prediction remain distinct. No Angstrom, Planck, QCD,
confinement, lattice, soliton, or later AS6 input is allowed.

## Candidate Preregistration

The candidates are frozen before the AS5 source body or any later comparator
is opened.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal AS5 promotion | Its reductions eliminate every dimensionful boundary and `a` is only a unit choice | Source inputs | An absolute scale may emerge | Hash-pinned execution and data-flow audit |
| B | Reference-explicit transmutation | Declared one-loop flow and positive boundary data | `mu0,g2,b0` plus conversion | Only `Lambda/mu0` is dimensionless and boundary independent | Exact substitution and finite rescaling |
| C | M,L,T target-span theorem | Declared `c,hbar` primitive set | No dimensionful addition | A length target is outside the span; adding `a` assumes it | Exact rank and augmented-rank solve |
| D | Scale-coordinate covariance | Fixed dimensionless inputs and positive rescaling | `rho` | `Lambda` scales with `mu0`, inverse length oppositely, ratios stay fixed | Symbolic family and log-null direction |
| E | Arbitrary-target/circular family | A desired positive scale or length may be chosen | Target plus dimensionless inputs | The reference can reproduce any target, so no absolute prediction follows | Exact inverse construction and circularity probe |
| F | Unit-coordinate audit | A physical quantity and unit standard are separately declared | Positive unit factor | Coordinate changes do not change physics or derive the quantity | Unit-rescaling mutation |

## Selection Criteria and Blinding

Selection is ordered by accepted dependency closure, dimensionful-input
provenance, exact M,L,T span and RG rescaling, correct energy-length
orientation, explicit free-parameter count, unit covariance, mutation
sensitivity, natural framework fit, and reuse economy. The queue synopsis
exposes the rejected 3.62 Angstrom and Planck-length comparators; neither may
set a scale, convention, threshold, or verdict. The source body remains closed
until both contract representations validate.

## Proposed Claim Delta

Provisional C-DIM-008 may state that `c`, `hbar`, and dimensionless inputs
cannot span a length in M,L,T dimensions; that adjoining a length primitive
assumes rather than derives that dimension; and that a formal one-loop
transmutation scale and inverse length rescale with their supplied reference
while only ratios remain invariant. It may be promoted only if this exact
composition adds a reusable object beyond C-RGE-001 and C-RGE-003. It may not
establish a physical beta function, QCD, confinement, lattice scale, observed
number, or privileged unit system.

## Implementation and Oracle Plan

SymPy exact algebra is the strongest oracle. The campaign will first reuse
`renormalization`, `scale_transmutation`, `dimensional_analysis`, and the shared
verification ledger. A new pure `scale_provenance` module is allowed only if
the target-span, reference-rescaling, arbitrary-target, and unit-coordinate
composition is genuinely nonduplicate. The independent route will solve the
dimension equations, integrate or substitute the one-loop relation, build
finite rescaling and inverse families, and audit source data flow without
importing that module. Mutations will remove or rescale `mu0`, reverse the
inverse-energy map, insert `a` among inputs, perturb the exponent, hide a
target in a unit symbol, and confuse coordinate change with physical change.
No numerical integration is required; neither `np.trapz` nor another NumPy
quadrature alias will appear.

## Attempts and Continuation

Attempt 0001 will reproduce all six hash-pinned AS5 checks and audit their
load-bearing data flow. Technical or representation failures will be
preserved append-only. If literal scale generation fails, Candidates B-F
continue to the positive provenance ledger and terminal source mapping; the
campaign does not stop at rejection of the headline.

## Debt Ledger

The campaign tracks reference-scale, dimension-span, circularity, units,
dependency, duplication, verification, and synchronization debt.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| `mu0` may be hidden while calling Lambda generated from dimensionless input | Trace every factor and test finite reference rescaling | discharged by exact `mu0 -> rho*mu0` covariance |
| Including `a` may be used to claim `a` was derived | Compare target membership before and after adjoining the target primitive | discharged by rank 2 versus augmented rank 3 and the `(0,0,1)` solve |
| A numerical coordinate may be called a physical units choice | Separate physical rescaling from inverse unit-coordinate rescaling | discharged by the fixed-quantity unit-coordinate ledger |
| Dimensional transmutation may be called a parameter-free absolute prediction | Construct arbitrary-target reference families and retain all boundary data | discharged by exact target round trips containing the target in `mu0` |
| Existing C-RGE-001/C-RGE-003 content may be duplicated | Compare the complete proposed object and consumers against accepted claims | discharged; C-DIM-008 adds target-span, inverse-target, and unit-coordinate composition |
| Sensitive verification, review, and synchronization are incomplete | Complete mutations, independent route, source disposition, claim review if needed, replay, and generated synchronization | discharged at the v0.69.0 promotion boundary |

## Review and Promotion Plan

Any nonduplicate claim receives an independent dimension, reference-scaling,
unit-covariance, arbitrary-target, and dependency review. AS5 receives a
terminal disposition through `migration/dispositions.yaml`, followed by queue
regeneration. Accepted reusable logic moves into package code with tests only
if its claim delta survives. Promotion then requires a claim-level review,
pinned release, generated docs and accepted memory, affected-consumer replay,
one integrated validation boundary, and a separate diff check. A no-new-claim
result still requires a structured terminal reason and durable campaign
evidence.

## Outcome

P076 derives the positive provenance ledger and accepts it as C-DIM-008.
The exact package tests pass, the primary route passes 32 checks, and a fresh
independent route passes 21 checks. AS5 is qualified: its no-length theorem
survives, but the displayed scale retains `mu0`, arbitrary targets can be
reconstructed by choosing that reference, and its hierarchy label has the
inverse-energy orientation reversed.

## Done Gate

P076 is complete after the v0.69.0 transaction synchronizes the canonical
module, 16 focused tests, both exact routes, claim review, AS5 disposition,
queue, registry, release, generated docs, and accepted memory. The integrated
workflow passes at the unchanged promotion boundary and campaign debt is
empty. The parent migration remains active because later source units remain
pending.
