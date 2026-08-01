---
description: Independent review of C-MED-002
author: vantasner-review
created: '2026-08-01T13:33:52Z'
updated: '2026-08-01T13:33:52Z'
tags:
- substrate-framework
- claim-review
- medium-scaling
category: decisions
confidence: working
status: archived
---
# Review of C-MED-002

## Claim Under Review
Conditional on positive `S,c,a,kappa`, declared `n=a^-3` and
`Theta=kappa*S*c/a`, and `C-MED-001`'s response laws, exact substitution gives
`epsilon=kappa*S/(a^4*c)`, `mu_inverse=kappa*S*c/a^4`, and wave speed `c`.
Under the separate declared dictionary `rho_medium=epsilon/2`, mass density is
`kappa*S/(2*a^4*c)`. The ratios and model equations are premises, not outputs of
dimensional analysis.

## Sourced Inputs
The review read `v0.14.0`, `C-MED-001`, proposed `C-DIM-002`, P016 and its
attempt, constitutive APIs/tests, both verifiers, and hash-pinned AS2. No Debye
dynamics, sound speed, density dictionary, or physical scale is imported as an
accepted fact.

## Independence
The main route composes canonical response APIs. The review directly substitutes
the four declared equations and simplifies them without importing the proposed
lattice helpers.

## Verification Status
Exact substitution and cancellation establish the conditional formulas. The
oracle separately checks dimensions and every coefficient, including the source
implementation's missing one-half. The claim earns `symbolic_verified`.

## Sensitivity and Counterexamples
Wrong Debye length power, number-density power, or mass-density ratio breaks the
predicate. A thermal symbol independent of `a` cannot be eliminated without the
Debye premise. Varying `kappa` or the density conversion changes the outputs
while preserving dimensions, proving those coefficients remain free.

## Framework Compatibility
The claim is a compatible extension of `C-MED-001` and uses `C-DIM-002` only for
unit classification. It preserves the accepted conclusion that co-scaling
alone produces no index variation. No medium realization or absolute scale is
asserted.

## Dependency and Consumer Replay
Dependencies are `C-MED-001` and `C-DIM-002`. Consumers are the constitutive
APIs/tests, AS2's disposition, and later absolute-scale audits.

## Competing Candidate Audit
Conditional composition, basis-only promotion, and physical closure were
registered. AS2 contains distinct reusable substitutions, so conditional
composition is retained. The source's own free `kappa_s` and Debye residual
reject physical closure.

## Four-Axis Decision

The corrected premise-explicit composition supports acceptance.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: conditional composition of C-MED-001 and C-DIM-002

## Promotion Transaction
Promotion adds lattice-response APIs/tests, `C-MED-002`, frozen P016 evidence,
`v0.15.0`, qualified AS2 disposition, and regenerated consumers.

## Continuation if Not Accepted
A substitution failure would reject the medium candidate while leaving the
dimension-basis theorem intact. Dimensions could not repair a wrong coefficient.

## Done Gate
The positive conditional formulas, independent route, coefficient-sensitive
mutations, premise ceiling, and consumers are complete with no claim debt.

## Cross-References
See `C-MED-001`, `C-DIM-002`, P016, AS2, the constitutive module/tests, and the
parent migration effort.
