---
description: Derive conditional U1 current and declared-profile charge reciprocity, then adjudicate EM1 and HE3
author: vantasner
created: '2026-08-01T12:58:56Z'
updated: '2026-08-01T13:07:00Z'
tags:
- substrate-framework
- campaign-proposal
- u1-current
- charge-reciprocity
- migration-EM1-HE3
category: proposals
confidence: exploratory
status: archived
---
# P014 Conditional U(1) Charge and Reciprocity

## Question and Positive Deliverable
P014 must deliver a reusable, exact conditional global-U(1) current theorem and
a separately scoped exact charge for the declared stationary profile
`Psi=A*sech(eta*x)*exp(-i*omega*t)`. It must then state exactly what follows
when that declared profile is parameterized by the accepted sine-Gordon
frequency and composed with accepted breather energy, secant scale, and boost
kinematics. A stationary ansatz alone, a predecessor pass tally, or the name
“Noether charge” is not the positive result.

## Base Release and Provenance
The accepted base is `v0.13.0` at commit `2b00560`. The hash-pinned source units
are EM1 at `merged-framework/bridges/phase-3/bridge_EM1_u1_noether_charge.py`,
SHA-256 `2f5c6e0236748bc6f3a8ce4a77bd18dc26b3cef235038d57bc71310361ea4850`,
and HE3 at `merged-framework/bridges/phase-45/bridge_HE3_charge_action_reciprocity.py`,
SHA-256 `fd646799b03b8463463dc200bcfaeb2ce397ccbc9412aa9ee7c6d9a04bfd7fbc`.
Both are pending candidate evidence, not authority. The source equations were
inspected to decompose their claims; there is no empirical comparator in this
campaign.

## Invariants, Conventions, and Allowed Imports
The current convention is
`j^mu=i*(Psi_conj*d^mu(Psi)-Psi*d^mu(Psi_conj))` with metric signature
`(+,-)`. General conservation is on-shell and conditional on an independently
declared complex scalar equation `Box(Psi)=F(|Psi|^2)*Psi` with real `F`; it is
not a consequence of the accepted real sine-Gordon equation. The stationary
profile, amplitude `A`, inverse width `eta=sqrt(1-omega^2)`, and shared frequency
parameter are explicit additional premises. `C-SG-002`, `C-SG-006`, and
`C-SG-008` are the only accepted scientific imports.

## Candidate Preregistration
The routes and failure criteria are frozen before canonical implementation.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | General conditional theorem, declared-profile specialization, then exact composition | Complex U(1) theory and separately declared profile | `A`, `omega` | Preserves the real-SG boundary and exposes normalization | Off-shell identity, symmetry-breaking mutation, exact integral and composition |
| B | Stationary ansatz continuity only | Declared profile but no EOM | `A`, `omega` | Kinematically true but too weak for the Noether headline | Cannot establish conservation for arbitrary on-shell fields |
| C | Physical charged breather with universal constant 64 | Hidden complex ontology, profile dynamics, normalization, and charge map | Suppressed | Conflicts with accepted scope and parameter honesty | `A` rescaling changes 64 and the real field has zero current |

## Selection Criteria and Blinding
The frozen order is theorem/profile separation, accepted dependency closure,
signature and phase convention consistency, amplitude and symmetry sensitivity,
regular Lorentz composition, and reusable API fit. Candidate A is structurally
preferred; B remains a kinematic subcheck and C is a required rejection guard.
No empirical comparator exists, so there is no numerical selection gate.

## Proposed Claim Delta
The campaign proposes two individually reviewable conditional claims.

| Claim | Exact statement | Dependencies | Oracle | Consumers |
| --- | --- | --- | --- | --- |
| C-U1-001 | Off-shell divergence identity and on-shell conservation for a declared global-U(1) complex scalar, with real-field and phase-breaking guards | none | SymPy arbitrary-field calculus and polar-coordinate rederivation | EM1 and later gauge audits |
| C-U1-002 | For the declared sech profile, `Q=4*A^2*omega/sqrt(1-omega^2)`, `Q*E=64*A^2*omega`, `Q*H=64*A^2`, their limits and conditional boosted vector forms | C-U1-001, C-SG-002, C-SG-006, C-SG-008 | exact integration, lattice nullspace, mutations, direct antiderivative | HE3 and charge/action consumers |

## Implementation and Oracle Plan
A pure `substrate_framework.u1_charge` module will expose the current,
divergence, stationary density, sech-profile charge, and exact composition
helpers without executing simulations. The exact verifier will use arbitrary
real and imaginary field components for the divergence identity, explicit
on-shell substitutions, real-field and phase-breaking counterexamples, direct
sech integration, limits, log derivatives, amplitude scaling, boosted vector
composition, and the complete exponent-kernel classification. Mutations change
the current coefficient/sign, profile-width power, amplitude power, and secant
normalization. An independent polar-field and tanh-antiderivative route will not
import the proposed APIs. A numerical rerun is unnecessary because every
load-bearing quantity has an exact symbolic oracle.

## Attempts and Continuation
Attempt `0001` implements Candidate A. A convention mismatch returns to the
raised-index definition rather than changing accepted boost signs. Failure of
the profile specialization rejects or reforms that profile; it cannot weaken
the general theorem or alter the accepted sine-Gordon energy.

## Debt Ledger
The campaign starts with four explicit debts.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| Complex enrichment could be mistaken for accepted sine-Gordon ontology | Claim and API state it is an independent conditional theory | discharged |
| Stationary continuity could be mistaken for general Noether conservation | Arbitrary-field off-shell identity and on-shell premise are separately verified | discharged |
| Profile and amplitude are not derived from a named complex-field potential | Every specialization and source disposition names them as declarations | discharged |
| The number 64 could be mistaken for a universal physical constant | Retain `A` and prove `Q*H=64*A^2`; exclude physical-charge and quantum maps | discharged |

## Review and Promotion Plan
Each proposed claim receives a separate claim review. A source adjudication
will audit EM1 and HE3 independently and preserve their unclosed ontology,
potential, stability, gauge-charge, and universal-quantum interpretations.
Promotion requires package extraction, unit tests, exact and independent
verifiers, individual terminal source dispositions, registry/release updates,
generated consumer synchronization, targeted replay, and one full validation
run at the unchanged promotion boundary.

## Results and Promotion
Attempt `0001` preserved a SymPy square-root branch failure at the upper charge
limit. Attempt `0002` repaired the limit oracle with `Abs(Q)` and passed 38
checks. The final strengthened attempt `0003` also proves the necessity step
behind the complete exponent classification and passes 39 checks. The
independent polar, tanh-antiderivative, rapidity, and elimination route passes
nine checks; seven focused package tests pass. `C-U1-001` and `C-U1-002` are
accepted in `v0.14.0`, while EM1 and HE3 are qualified at their unproved
ontology and universal-physics interpretations.

## Done Gate
P014 is complete. Both positive conditional claims pass exact, independent,
and mutation-sensitive review; their dependency closure and scope are explicit;
EM1 and HE3 each have a durable terminal disposition; generated consumers
agree; and the campaign debt ledger is empty.
