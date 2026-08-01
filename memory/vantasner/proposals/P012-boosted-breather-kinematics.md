---
description: Derive boosted breather vector proportionality and adjudicate HE1
author: vantasner
created: '2026-08-01T12:43:23Z'
updated: '2026-08-01T12:46:13Z'
tags:
- substrate-framework
- campaign-proposal
- sine-gordon
- migration-HE1
category: proposals
confidence: exploratory
status: archived
---
# P012 Boosted Breather Kinematics

## Question and Positive Deliverable
P012 derives a positive Lorentz-kinematic claim for the accepted breather. With
`gamma=(1-v^2)^-1/2`, the boosted phase has `(Omega,k)=(gamma*omega,
gamma*omega*v)` and energy-momentum is `(E,P)=(gamma*E0,gamma*E0*v)`.
The proposed `C-SG-008` states the vector identity
`(E,P)=H(omega)*(Omega,k)`, where `H=E0/omega` is the accepted secant scale,
and records both invariant norms and the nonzero-velocity ratio corollaries.

## Base Release and Provenance
The accepted base is `v0.11.0` at framework commit `e46beca`. `C-SG-001`
supplies the rest phase frequency, `C-SG-002` the rest energy, and `C-SG-006`
the exact family-dependent secant scale and its rejection as canonical action.

The hash-pinned source unit is HE1 at
`merged-framework/bridges/phase-45/bridge_HE1_hbar_eff_from_corpus_E0.py`,
SHA-256 `2fe4ed7ab9ec7dcc699461679a97754a74ad4d699b759bb003c0801afcb8543a`.
It is pending. Its first five checks duplicate accepted field/energy results;
its remaining checks combine a boost construction with secant-scale properties.

## Invariants, Conventions, and Allowed Imports
The boost is in normalized units `c=1`, with real `|v|<1` and
`gamma=1/sqrt(1-v^2)`. The phase convention is `Omega*t-k*x`. Vector
proportionality remains primary because it is meaningful at `v=0`; `P/k` and
phase velocity require `v!=0`. No Planck constant or quantum premise is imported.

## Candidate Preregistration

The following alternatives are frozen before implementation.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Full boosted-vector proportionality and invariant norms | accepted rest objects and Lorentz boost | velocity only | Native exact consequence | Both components, norms, rest limit, mutations |
| B | Component-ratio equality only | Candidate A away from rest | velocity excluding zero | True but singular and weaker | Fails well-defined rest-limit criterion |
| C | Universal Planck interpretation | family-independent scale | extra constant | Conflicts with C-SG-006 | Derivative and two-frequency counterexample |

## Selection Criteria and Blinding
The frozen order is Lorentz covariance and rest-limit regularity, accepted
dependency closure, exact invariants/signs, semantic precision, then mutation
sensitivity. Candidate A is preferred. Candidate B remains a corollary for
nonzero velocity. Candidate C conflicts with the accepted global variation of
the secant scale. No empirical comparator exists.

## Proposed Claim Delta

The campaign proposes one individually reviewed kinematic consequence.

| Claim | Exact statement | Dependencies | Oracle | Consumers |
| --- | --- | --- | --- | --- |
| C-SG-008 | Boosted phase and energy-momentum vectors are proportional by the secant scale and retain their rest invariant norms | C-SG-001/002/006 | exact SymPy Lorentz algebra, rapidity rederivation, mutations | boosted-breather and HE1/HE3 audits |

## Implementation and Oracle Plan
The sine-Gordon module will add pure Lorentz-factor, boosted phase-vector, and
boosted energy-momentum APIs. Numeric velocity domains will be enforced.

The main verifier will derive both vector components, invariant norms, ratios,
phase/group velocity corollaries, the rest limit, and constant-scale rejection.
It will mutate the phase sign, momentum boost factor, frequency, and energy
coefficient. The independent review will use rapidity `v=tanh(rapidity)` and
hyperbolic identities without importing the new boost APIs.

## Attempts and Continuation
Attempt `0001` implements Candidate A. If sign conventions fail, the phase
covector and contravariant energy-momentum conventions will be separated before
retrying. Candidate B cannot repair a vector mismatch by excluding rest.

## Debt Ledger

The campaign starts with three semantic debts.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| HE1's ratio form divides by zero at rest | Accepted claim uses vector proportionality as primary | discharged |
| “de Broglie” language could imply quantum derivation | Registry describes exact Lorentz kinematics only | discharged |
| `hbar_eff` could be mistaken for a universal constant | Claim depends on C-SG-006 secant semantics and preserves its family dependence | discharged |

## Review and Promotion Plan
One claim review and one source adjudication will audit every HE1 check family.
Promotion will freeze P012, add APIs/tests and `C-SG-008`, create a pinned
release, give HE1 a terminal evidence-backed disposition, regenerate canonical
records, replay sine-Gordon consumers, and run full validation once.

## Results and Promotion
Attempt `0001` passed 17 exact checks. The independent rapidity construction
passed five checks and retains a regular rest vector without component division.
`C-SG-008` is accepted in `v0.12.0`. HE1's exact field, energy, secant, and boost
content maps to accepted claims; its quantum terminology is terminally qualified.

## Done Gate
P012 is complete. The positive vector claim passes exact, independent, and
mutation-sensitive review; the rest and semantic guards are durable; HE1 is
terminally adjudicated; consumers agree; and debt is empty.
