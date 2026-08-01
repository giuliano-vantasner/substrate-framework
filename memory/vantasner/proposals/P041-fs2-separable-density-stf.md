---
description: Derive conditional separable-density STF algebra and audit FS2
author: vantasner
created: '2026-08-01T18:52:25Z'
updated: '2026-08-01T19:03:00Z'
tags:
- substrate-framework
- campaign-proposal
- separable-density
- migration-FS2
category: proposals
confidence: working
status: archived
---
# P041 FS2 Separable-Density STF Audit

## Question and Positive Deliverable

P041 must derive a reusable, premise-explicit theorem for the second moment and
STF tensor of a centered longitudinal density times a fixed centered
axisymmetric transverse profile. It must then decide whether FS2 supplies the
additional dynamics needed to identify that declared product as a conserved 3D
breather source or physical gravitational quadrupole. A negative ontology audit
without the positive tensor construction would not complete the campaign.

## Base Release and Provenance

The accepted base is `v0.36.0` at framework commit `dd17b57`, with forty-nine
claims. Relevant authority includes `C-SG-002`, `C-SG-009`, `C-MOM-001`, and
`C-GW-002`. FS2 is a pending candidate unit at `substrate@6d1f4e0`, SHA-256
`9e9edbde8810a9040047d13e328eafbea992a218060de4d10a4118080f20cc31`.
Memory search found no accepted separable transverse-embedding theorem.

## Invariants, Conventions, and Allowed Imports

The longitudinal energy and moment retain their normalized 1+1 meanings. The
transverse profile may be declared normalized, centered, axisymmetric, and
time-independent, with a clearly defined per-axis second moment. Fubini then
constructs density moments, but supplies no momentum density, spatial stress,
local conservation, field action, stability, or physical embedding. Normalized
`I_STF` and triple `Q=3*I_STF` remain distinct.

## Candidate Preregistration

The alternatives are frozen from queue metadata before the full FS2 executable
body or any reported derivative comparison is inspected.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Full separable moment/STF and viewing algebra | Declared centered product density | Monopole, longitudinal moment, per-axis variance | Compatible conditional extension | Direct product integrals, STF derivatives, norms, and TT axis limits |
| B | Diagonal moment and STF only | Same product density | Same three scalar inputs | Minimal compatible extension | Fubini factorization and trace removal |
| C | Physical 3D breather quadrupole/radiation | 3D solution, stress closure, gravity | Added transverse dynamics and coupling | Dependency conflict | Accepted PDE/source conservation and field-law closure |

## Selection Criteria and Blinding

Selection is ordered by explicit profile hypotheses, convention consistency,
exact trace and derivative factors, independence from constant width where
mathematically required, viewing geometry, mutation sensitivity, parameter
economy, and accepted dependency closure. No FS2 decimal derivative or later
radiation result may select a candidate.

## Proposed Claim Delta

Provisional `C-MOM-002` would state the conditional moment and STF tensor of an
axisymmetric separable density and its derivative/projection consequences. It
would depend on `C-MOM-001` and use `C-SG-009` only for the breather
specialization. It will explicitly exclude a conserved physical 3D source,
breather embedding, and gravity.

## Implementation and Oracle Plan

A pure canonical moment API will accept monopole, longitudinal second moment,
and per-axis transverse variance and return both STF conventions. SymPy will
verify Fubini-derived diagonal entries, traces, arbitrary derivatives, norms,
and exact TT axis/perpendicular geometry. An independent route will integrate a
normalized Gaussian transverse profile directly and reconstruct the tensors
without the helper. Mutations will confuse per-axis and radial variance, retain
trace, change the triple factor, or let a constant width enter time derivatives.

## Attempts and Continuation

Attempt `0001` will hash-check and reproduce FS2, inventory its product-density,
width, derivative, TT, source-conservation, FS3, and P3D3 premises, and compare
all conventions to accepted definitions. Failed symbolic representations or
ill-posed physical candidates will remain append-only evidence.

## Debt Ledger

This ledger tracks transverse normalization, centering, variance convention,
STF scaling, time derivatives, projection geometry, and physical-source scope.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| Transverse radial and per-axis widths may be conflated | Define one convention and test its conversion | discharged: the API declares per-axis variance and the independent Gaussian route proves radial variance is twice it |
| A declared product may hide nonzero mixed moments | Require centering/axisymmetry and verify all entries | discharged: explicit centering and axisymmetry make every mixed moment vanish by Fubini |
| Constant width may contaminate time derivatives | Derive general derivative tensors symbolically | discharged: every positive-order derivative depends only on the longitudinal moment derivative |
| Normalized and triple STF conventions may mix | Carry the factor three through norms and projections | discharged: both tensors and their factor-nine norm relation are exact and mutation-sensitive |
| Density may be called a conserved physical source | Supply stress/current closure or explicitly exclude it | discharged: C-MOM-002 excludes conservation, dynamics, and gravity; a constant-mass counterexample fails local continuity |
| Pending FS3/P3D3 may be imported backward | Keep both outside accepted dependencies | discharged: neither appears in the claim dependency closure |

## Review and Promotion Plan

The provisional claim receives an independent direct-product integration
review. Promotion requires pure APIs/tests, immutable attempt evidence, claim-
level review, terminal FS2 disposition, registry/release/docs/memory agreement,
targeted replay, and one unchanged full repository gate.

## Done Gate

P041 closes only when profile hypotheses, all tensor factors, derivative and
projection consequences, mutations, physical boundary, source disposition,
consumers, and every campaign debt row are resolved.

## Adjudication Result

Candidate A is accepted as `C-MOM-002`. Thirty-one primary checks and eight
independent checks establish the exact Fubini moments, normalized and triple
STF tensors, derivative norms, and axis/perpendicular TT geometry. FS2 is
qualified: its density is a declared conditional construction, its spectral
comparison reuses the same sampled data, its width conflicts with an
unaccepted later annotation, and it supplies no closed 3+1 dynamics,
conserved stress tensor, gravity, or radiation theorem. The hash-matched
source-reproduction record avoids rerunning its minute-long dense quadrature
during unchanged verifier replay while preserving an executable source path.
