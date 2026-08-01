---
description: Derive canonical sine-Gordon light-cone stress balance and audit NC2
author: vantasner
created: '2026-08-02T00:08:00Z'
updated: '2026-08-02T00:29:00Z'
tags:
- substrate-framework
- campaign-proposal
- sine-gordon
- migration-NC2
category: proposals
confidence: exploratory
status: archived
---
# P049 NC2 Light-Cone Stress Balance Audit

## Question and Positive Deliverable

P049 must derive an importable exact canonical stress tensor for the normalized
real sine-Gordon field, transform it with an explicit light-cone Jacobian, and
factor both local balance laws by the field-equation residual. It must then
separate symmetric potential-mediated exchange between characteristic sectors
from any claimed physical left-right asymmetry. A critique of NC2 without the
positive conserved tensor and balance theorem would not complete the campaign.

## Base Release and Provenance

The accepted base is `v0.43.0` at framework commit `35c4045`; its scientific
transaction is commit `757a509`. `C-SG-001` fixes the normalized equation and
Hamiltonian convention. `C-SG-011` fixes both characteristic-current sources,
the half-normalized light-cone derivatives, and the exact parity-invariance
boundary. NC2 is pending source evidence at `substrate@6d1f4e0`, SHA-256
`6854fafe62ef7c8bfcf558573e3c89fec0d2144cb9a39df2e2ecb6d66d960136`.
Its declared W1 and W7 dependencies remain pending and are not allowed imports.
Memory search found only the P048 handoff and no accepted NC2 result.

## Invariants, Conventions, and Allowed Imports

Use metric `eta=diag(+1,-1)` and scalar Lagrangian density
`L=(phi_t^2-phi_x^2)/2-(1-cos(phi))`. The canonical symmetric covariant tensor
is `T_mu_nu=partial_mu(phi)*partial_nu(phi)-eta_mu_nu*L`; raising both indices
changes the sign of the mixed component. Coordinates are
`x_plus=t+x`, `x_minus=t-x`, hence
`partial_plus=(partial_t+partial_x)/2` and
`partial_minus=(partial_t-partial_x)/2`. Covariant light-cone components must
be obtained from the coordinate Jacobian, not guessed from labels. A conserved
stress tensor, a trace relation, characteristic-sector exchange, parity
covariance, and physical parity violation are distinct claims. Improvement
terms are excluded unless Candidate A fails and their new parameter and
boundary consequences are separately governed.

## Candidate Preregistration

The alternatives are frozen from queue metadata and accepted conventions
before the full NC2 executable is opened.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Canonical Cartesian tensor plus exact half-normalized light-cone transform and residual-factorized balances | Accepted scalar action, metric, and C-SG-011 derivatives | None | Native and minimal | Variational tensor derivation, Jacobian transform, off-shell divergence and balance factorization |
| B | Improved stress-tensor family | Candidate A plus a divergence improvement and boundary control | Improvement coefficient or function | Compatible only if a real unresolved obligation requires it | Show a necessary invariant or consumer that canonical stress cannot satisfy |
| C | Potential-mediated exchange is a physical V-A or parity-violating interaction | Pending W1/W7 and a physical sector dictionary | Coupling and sector-selection inputs | Dependency and symmetry conflict expected | Exact parity transform and accepted-dependency audit |

## Selection Criteria and Blinding

Selection is ordered by exact Lagrangian/EOM/Hamiltonian compatibility,
coordinate and sign closure, off-shell factorization, conservation strength,
zero-potential/vacuum/kink/breather/parity limits, dependency closure,
parameter economy, and reusable API scope. This exact campaign needs no
empirical comparator. NC2's detailed result remains unopened until the tensor,
Jacobian, candidate set, mutations, and interpretation ceiling are frozen here.

## Proposed Claim Delta

Provisional `C-SG-012` will state, if verified, the canonical covariant and
contravariant tensor components, energy and momentum conservation residuals,
light-cone components `T_pp`, `T_mm`, and `T_pm`, their two exact balance laws,
the trace/potential relation, and spatial-parity exchange of `T_pp` and `T_mm`
with `T_pm` even. It will explicitly withhold independently conserved chiral
stresses away from zero potential derivative, physical left-right selection,
V-A dynamics, weak force, bosonization, particle identity, and substrate
ontology.

## Implementation and Oracle Plan

The canonical sine-Gordon module will expose pure potential, Lagrangian,
Cartesian stress, divergence, light-cone component, and balance APIs. SymPy is
the strongest oracle because the obligations are exact differential and
coordinate identities. The primary route will derive the tensor from the
declared Lagrangian and metric, raise indices explicitly, factor its divergence
by the canonical residual, transform with the coordinate Jacobian, and factor
both light-cone balances off shell. Mutations will flip the mixed-component
raising sign, omit the potential, replace the Jacobian half factor, change the
mixed light-cone normalization, and reverse one balance sign. Independent
rederivation will use direct Noether energy/momentum continuity and a separate
matrix Jacobian. Constant vacua, the exact kink, an accepted breather, the
massless potential deletion, and spatial parity supply exact limits and
counterexamples. Targeted replay includes sine-Gordon root and P048 consumers;
the full repository gate runs once at the final promotion boundary.

## Attempts and Continuation

Attempt 0001 reproduced the hash-pinned source successfully and implemented
Candidate A, but three tests compared raw SymPy forms rather than simplified
differences and failed despite exact equality. The failure is preserved with a
minimal reproducer. Attempt 0002 corrected only the representation-sensitive
test oracle; all 37 primary checks and all seven independently implemented
Noether/Jacobian checks pass. Candidate A therefore closes the exact objective,
while Candidate B remains unnecessary and Candidate C is structurally rejected.

## Debt Ledger

This ledger tracks metric signs, coordinate normalization, off-shell closure,
improvement freedom, parity semantics, source mapping, and consumers.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| NC2's executable and normalization have not been audited | Reproduce the hash-pinned source and review every conclusion | discharged: exit zero, all seven source checks, and sentence-level normalization audit |
| No canonical exact stress/light-cone API exists | Implement and independently verify the minimal tensor construction | discharged: pure APIs, exact tests, 37-check verifier, and seven-check independent review |
| Potential exchange may be conflated with physical chirality | Prove the parity map and preserve the interaction ceiling | discharged: exact sector exchange with even mixed component and explicit exclusion ceiling |
| Direct and downstream consumers are not inventoried | Run graph impact and targeted/global replay | discharged: low pre-impact, reviewed line-shift detection, 81 targeted tests, P001/P048, and 346-test full gate |

## Review and Promotion Plan

The exact claim received an individual review from raw verifier and independent
derivation artifacts. Promotion supplies importable implementation and tests,
append-only attempts, source reproduction, sentence-level adjudication,
consumer replay, a structured NC2 qualification, `C-SG-012`, the pinned v0.44
release, and regenerated docs, memory, and queue. The status-zero workflow gate
passes all 346 tests; final diff hygiene passes separately. Mixed source content
remains qualified with its rejected remainder recorded explicitly.

## Done Gate

P049 closes because the positive stress-tensor object, normalization, off-shell
sensitivity, independent derivation, claim review, source disposition, replay,
canonical state, and empty campaign debt ledger pass. The parent corpus-
migration effort continues to NC3 with 171 pending units.
