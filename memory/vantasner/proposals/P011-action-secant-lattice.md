---
description: Classify the breather secant scale and conditional action lattice, then adjudicate HE4
author: vantasner
created: '2026-08-01T12:30:56Z'
updated: '2026-08-01T12:37:56Z'
tags:
- substrate-framework
- campaign-proposal
- sine-gordon
- migration-HE4
category: proposals
confidence: exploratory
status: archived
---
# P011 Breather Secant Scale and Conditional Action Lattice

## Question and Positive Deliverable
P011 delivers two exact objects. `C-SG-006` classifies the energy-frequency
secant scale `H=E/omega` relative to the accepted canonical action `J`, including
their ratio, endpoints, monotonicity, and the decisive derivative
`dE/dH=omega^3`. `C-SG-007` derives the energy, frequency, admissible range,
continuous interpolation derivative, and true adjacent finite difference that
follow if a fixed action lattice `J_n=n*h` is separately imposed.

The claims will not call `H` a Planck constant, derive the lattice premise,
identify its spacing with a renormalized coupling, or promote a literature
spectrum. HE4's comparison can be audited after the exact candidate is frozen.

## Base Release and Provenance
The accepted base is `v0.10.0` at framework commit `3ab45d5`. `C-SG-002`
supplies `E=16*sqrt(1-omega^2)`. `C-SG-003` supplies
`J=16*acos(omega)`, `dE/dJ=omega`, `0<J<8*pi`, and the inverse energy/action
map. `C-SG-004` supplies the exact gradient Legendre transform.

The hash-pinned source unit is HE4 at
`merged-framework/bridges/phase-45/bridge_HE4_dhn_action_variable.py`, SHA-256
`0fae1f54748a5206214afaeb1fb7293f46c04c6146e1779c41837fddaf245f29`.
It is partially migrated through `C-SG-003/004`. HE1, HE2, and T1E are cited
source evidence, not accepted dependencies. Charge reciprocity is asserted by
the distinct pending unit HE3 and will not be silently adjudicated as HE4.

## Invariants, Conventions, and Allowed Imports
The classical domain is real `0<omega<1`. The normalized action is
`J=(1/(2*pi))*closed_integral(p dq)`. `H=E/omega` is named a secant action scale,
not an effective Planck constant. A lattice quantum `h` is fixed and positive,
and a level `n` is a positive integer satisfying `0<n*h<8*pi`.

The cited DHN and Zamolodchikov results are quarantined comparators. They cannot
select the formulas or become dependencies of the proposed claims. Only primary
literature may support the source-comparison audit.

## Candidate Preregistration

The following routes are frozen before external comparator inspection.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Compose accepted energy and action formulas directly | C-SG-002/003 | fixed lattice scale `h` only for C-SG-007 | Minimal exact closure | Global derivatives, limits, bounds, and finite difference |
| B | Repeat HE4's full field phase-space integration | C-SG-001 plus numerical quadrature | integration precision | Valid but duplicates accepted C-SG-003 | Compare dependency cost and evidence independence |
| C | Infer formulas from DHN spectrum/truncation | external semiclassical interpretation | coupling map | Comparator-led and non-native | Fails if accepted E/J already fix the answer or coupling map is undeclared |

## Selection Criteria and Blinding
The frozen order is accepted dependency closure, exact global behavior,
classical-versus-quantum separation, correct discrete calculus, assumption and
parameter economy, then independent rederivation. Candidate A is structurally
preferred. Candidate B is regression evidence for the already accepted action,
not an independent basis for these new consequences. Candidate C is excluded
from selection; literature is inspected only after this freeze.

## Proposed Claim Delta

The campaign proposes two individually reviewed consequences.

| Claim | Exact statement | Dependencies | Oracle | Consumers |
| --- | --- | --- | --- | --- |
| C-SG-006 | Exact secant scale, canonical-action ratio, global behavior, and `dE/dH=omega^3` rejection | C-SG-002/003 | SymPy calculus, angle-coordinate rederivation, mutations | action interpretation and HE1/HE2/HE4 audits |
| C-SG-007 | Conditional fixed action lattice, sine energy, cosine frequency, finite level domain, continuous derivative, and adjacent gap | C-SG-003 | SymPy trigonometry and independent finite-difference route | future quantization proposals and HE4 audit |

## Implementation and Oracle Plan
The sine-Gordon module will add pure APIs for the secant scale, action/secant
ratio, lattice energy/frequency, and adjacent gap. Domain guards will distinguish
continuous symbolic derivations from numeric admissibility.

The main verifier will derive both claims through accepted APIs, prove endpoints
and derivative identities, derive the adjacent difference rather than label a
derivative as a spacing, and reject coefficient, frequency-power, lattice-scale,
and off-by-one mutations. The independent review will use the angle coordinate
`theta=acos(omega)` and direct trigonometric finite differences without importing
the new APIs. No numerical integration will be counted as independent evidence
because `C-SG-003` already fixes `J` exactly.

## Attempts and Continuation
Attempt `0001` implemented Candidate A but failed when SymPy retained
branch-sensitive roots in the proposed circle-area antiderivative certificate.
Attempt `0002` repaired the positivity representation but failed on structural
expression equality for the correct polynomial identity `omega^3-omega =
-omega*(1-omega^2)`. Attempt `0003` normalizes that residual explicitly. A
failed lattice identity returns to action-domain and integer-index conventions;
a literature match cannot repair it.

## Debt Ledger

The campaign starts with four interpretive debts.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| `hbar_eff` naming could imply a universal constant | Canonical API and registry use secant-scale semantics | discharged |
| HE4 labels `dE_n/dn` as level spacing | Claim and review separate interpolation derivative from adjacent gap | discharged |
| The action lattice is imposed, not derived | C-SG-007 remains explicitly conditional | discharged |
| Literature matching and charge reciprocity could leak into authority | Source audit quarantines primary comparators and routes reciprocity to HE3 | discharged |

## Review and Promotion Plan
Two claim reviews and one source adjudication will audit all HE4 check families.
Promotion will freeze P011, add APIs/tests and accepted claims, create a pinned
release, terminally qualify HE4 with durable evidence, regenerate canonical
records, replay sine-Gordon consumers, and run full validation once at the
unchanged boundary.

## Results and Promotion
Attempts `0001` and `0002` preserved two representation-level failures before
attempt `0003` passed 25 exact checks. The independent angle route passed seven
checks, and 18 sine-Gordon tests pass. `C-SG-006` accepts the exact secant-scale
classification and `C-SG-007` accepts the conditional lattice with the corrected
adjacent gap. Primary publisher records confirm the cited papers' subject matter
but do not supply HE4's missing convention/coupling map. HE4 is terminally
qualified, and charge reciprocity remains routed to HE3.

## Done Gate
P011 is complete. Both positive claims pass exact, independent, and mutation-
sensitive review; the discrete-spacing correction and semantic ceilings are
durable; HE4 has terminal evidence; consumers agree; and debt is empty.
