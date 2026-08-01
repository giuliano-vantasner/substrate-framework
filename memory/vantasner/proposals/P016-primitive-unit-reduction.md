---
description: Derive the speed-action-length unit basis and conditionally audit AS2 medium scalings
author: vantasner
created: '2026-08-01T13:28:05Z'
updated: '2026-08-01T13:33:52Z'
tags:
- substrate-framework
- campaign-proposal
- dimensional-analysis
- medium-scaling
- migration-AS2
category: proposals
confidence: exploratory
status: archived
---
# P016 Primitive Unit Reduction

## Question and Positive Deliverable
P016 must deliver an exact reusable solver for monomial dimensions and prove
what a declared primitive set `{c0,S,a}`—speed, action, and length—can and cannot
fix. It must separately classify any AS2 medium scaling as conditional algebra
or unsupported dynamics. Finding a dimensionally admissible energy monomial is
not by itself a derivation of temperature or a material model.

## Base Release and Provenance
The accepted base is `v0.14.0` at commit `30eaca9`. Relevant accepted inputs are
`C-DIM-001` and `C-MED-001`. The hash-pinned candidate source is AS2 at
`merged-framework/bridges/phase-21/bridge_AS2_medium_constants_reduce.py`,
SHA-256 `48ad6312d70248f2fda1cc935a09a567267a78a9494a62cb18312cf79412a631`.
Global memory mentions a related one-length discussion but is not project
authority and contributes no premise.

## Invariants, Conventions, and Allowed Imports
Dimension vectors use row order `(M,L,T)`. The declared columns are
`c0=(0,1,-1)`, `S=(1,2,-1)`, and `a=(0,1,0)`. Full rank means every target
dimension has a unique rational monomial exponent vector relative to this set;
it neither supplies dimensionless coefficients nor selects a physical law.
`C-MED-001` may be composed only under its explicit constitutive premises.

## Candidate Preregistration
The routes and failure criteria are frozen before reading AS2's full check body.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Exact unit basis plus explicitly conditional medium propagation | Declared primitives, then separately declared Debye/constitutive equations | Dimensionless speed ratio and coefficients | Maximum honest reusable content | Solve exponents, mutate dimensions, remove each premise |
| B | Unit basis only | Declared primitives | none | Safest if medium formulas add no reusable content beyond C-MED-001 | Source formulas reduce entirely to prior claims or declarations |
| C | Physical one-length closure | Dimensional availability treated as dynamics | Hidden order-one constants | Conflicts with C-DIM-001 scope | Alternative dimensionless factors leave dimensions unchanged |

## Selection Criteria and Blinding
The frozen order is exact basis rank, premise separation, dimensionless-factor
honesty, accepted-claim compatibility, dependency economy, and sensitivity.
Candidate A is preferred only if AS2 contains distinct reusable conditional
algebra; otherwise B is selected. Candidate C is a required rejection guard.
There is no empirical comparator.

## Proposed Claim Delta
The campaign proposes two separately reviewed claims. `C-DIM-002` is the exact
`{c0,S,a}` dimension-basis theorem and unique
monomial representations for mass, energy, time, and related targets.
`C-MED-002` is provisional: it will be retained only if AS2's conditional
Debye-plus-constitutive propagation is distinct from `C-MED-001`, dependency-
closed, and useful. Claims will be reviewed independently.

## Implementation and Oracle Plan
The dimensional-analysis module will gain a pure exact monomial-exponent solver
that checks target size and matrix consistency. The verifier will calculate
rank, determinant, inverse, target exponents, unit reconstruction, and nullspace;
reject swapped action/speed dimensions and missing primitives; and prove that
arbitrary dimensionless coefficients remain free. If the medium delta survives
source audit, its verifier will substitute the declared Debye and constitutive
equations step by step and mutate each load-bearing exponent and coefficient.
An independent route will solve the exponent equations by elimination without
importing the new API. No numerical rerun is appropriate.

## Attempts and Continuation
Attempt `0001` implements the structurally selected exact route after the full
AS2 source audit. If the medium claim duplicates `C-MED-001` or hides a dynamical
selection, it will be removed from the claim delta and preserved in the source
qualification rather than promoted to complete the campaign.

## Debt Ledger
The campaign starts with four explicit debts.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| Full rank may be misstated as a physical closure | Claim limits the theorem to unique monomial exponents | discharged |
| A dimensionless coefficient such as a sound-speed ratio remains free | API and claim retain it explicitly | discharged |
| Debye energy may be a declaration rather than derivation | Source audit identifies its exact logical status | discharged |
| Constitutive substitutions may duplicate or overextend C-MED-001 | Claim-level comparison decides promotion or qualification | discharged |

## Review and Promotion Plan
Each surviving claim receives an independent review. Source adjudication will
map every AS2 check to exact dimension algebra, conditional substitution,
duplicate evidence, or unsupported physical interpretation. Promotion requires
package APIs/tests, exact and independent evidence, terminal AS2 disposition,
registry/release synchronization if claims are accepted, targeted replay, and
one full validation at the unchanged boundary.

## Results and Promotion
Attempt `0001` passes 29 exact checks. The independent exponent-elimination and
direct-substitution route passes seven checks, and 16 focused package tests
pass. `C-DIM-002` and `C-MED-002` are accepted in `v0.15.0`. The campaign also
finds and corrects AS2's load-bearing missing factor `1/2`: the source declares
`rho_medium=epsilon/2` but its implemented `rho_reduced` equals `epsilon`.
AS2 is qualified at its unproved Debye selection, coefficients, dictionary,
one-length ontology, and physical realization.

## Done Gate
P016 is complete. The positive unit-basis object exists, every promoted medium
relation has explicit premise closure, dimensionless freedom is retained, AS2
is terminally adjudicated, consumers agree, and debt is empty.
