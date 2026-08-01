---
description: Derive the action-secant criterion and primitive-set dimensional groups, then adjudicate HE2
author: vantasner
created: '2026-08-01T12:50:47Z'
updated: '2026-08-01T12:53:41Z'
tags:
- substrate-framework
- campaign-proposal
- action-variables
- dimensional-analysis
- migration-HE2
category: proposals
confidence: exploratory
status: archived
---
# P013 Action-Secant and Dimensional-Group Criteria

## Question and Positive Deliverable
P013 delivers two general exact claims. `C-ACT-001` states that for positive
normalized action `J`, differentiable energy `E(J)`, and canonical frequency
`omega=E'(J)>0`, the secant equality `E/omega=J` throughout a connected interval
holds iff `E=CJ`; a rigid rotor instead gives `E/omega=J/2`. `C-DIM-001`
classifies the kernels for primitives `{E,omega}` and `{E,omega,S}` over base
dimensions `(energy,time)`.

## Base Release and Provenance
The accepted base is `v0.12.0` at commit `dad5e56`. `C-SG-006` supplies the
breather counterexample and precise secant semantics. The hash-pinned source is
HE2 at `merged-framework/bridges/phase-45/bridge_HE2_buckingham_breather_primitives.py`,
SHA-256 `88cfd8aae98c81e1b5fc7b556c24e661c8b687443659e98ad2a6fa5660973623`.

## Invariants, Conventions, and Allowed Imports
Canonical action is normalized by `1/(2*pi)`, avoiding HE2's shifting use of
`J` for the raw contour integral. Dimensional conclusions are conditional on
the declared primitive set. An empty kernel cannot prohibit a dimensionless
group after a new independent scale is added.

## Candidate Preregistration

The routes and failure criteria are frozen before implementation.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | General calculus iff plus exact kernel bases | connected positive-action interval | linear coefficient only in solved branch | Reusable and convention-clean | derivative of E/J and matrix kernels |
| B | Harmonic/rotor examples only | two soluble systems | inertia and oscillator scale | Correct but weaker | Cannot establish the iff or general scope |
| C | Permanent ceiling from two primitives | fixed set silently treated as exhaustive | none | Overstates Buckingham analysis | Adding S produces a nonzero kernel |

## Selection Criteria and Blinding
The frozen order is normalized-action consistency, exact global scope,
primitive-set-local conclusions, dependency economy, and sensitivity. Candidate
A is selected structurally; B is independent example evidence; C is a mutation
that must fail. No empirical comparator exists.

## Proposed Claim Delta

The campaign proposes two individually reviewed general claims.

| Claim | Exact statement | Dependencies | Oracle | Consumers |
| --- | --- | --- | --- | --- |
| C-ACT-001 | `E/E'=J` on a connected positive interval iff `E=CJ`, with rotor and harmonic limits | none | SymPy calculus and independent ODE route | action-scale and HE2 audits |
| C-DIM-001 | Kernel zero for `{E,omega}` and span `(-1,1,1)` for `{E,omega,S}` | none | exact matrix rank/nullspace and independent exponent equations | dimensional audits and HE2 |

## Implementation and Oracle Plan
New pure modules will expose generic action-scale helpers and dimensionless-
monomial bases. The exact verifier will prove the iff via `d(E/J)/dJ`, check
harmonic and rotor cases, compute both kernels, and reject normalization,
dimension-column, and primitive-deletion mutations. An independent review will
solve the differential equation by separation and the exponent equations by
elimination without importing the new APIs.

## Attempts and Continuation
Attempt `0001` implements Candidate A. A symbolic ODE representation failure
will be repaired using the quotient derivative identity. A nullspace mismatch
returns to column ordering and base-dimension conventions.

## Debt Ledger

The campaign starts with three debts.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| HE2 switches between raw and normalized action symbols | Canonical APIs and claims use one normalized convention | discharged |
| “harmonic iff” is asserted from examples | C-ACT-001 proves the global iff | discharged |
| Empty two-scale kernel is called permanent | C-DIM-001 limits the conclusion to its primitive set and shows the enlarged kernel | discharged |

## Review and Promotion Plan
Two claim reviews and one source adjudication will audit HE2 check families.
Promotion will freeze P013, add modules/tests and claims, create a release,
terminally adjudicate HE2, regenerate consumers, and run full validation once.

## Results and Promotion
Attempt `0001` passed 21 exact checks. Independent quotient/ODE and exponent-
equation routes passed six checks, and the new modules pass six tests.
`C-ACT-001` and `C-DIM-001` are accepted in `v0.13.0`; HE2 is terminally
qualified at its named-object and permanence interpretations.

## Done Gate
P013 is complete. Both positive claims pass exact, independent, and mutation-
sensitive review; convention and scope corrections are durable; HE2 is
terminally adjudicated; consumers agree; and debt is empty.
