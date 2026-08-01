---
description: Independent review of C-U1-002
author: vantasner-review
created: '2026-08-01T13:07:00Z'
updated: '2026-08-01T13:07:00Z'
tags:
- substrate-framework
- claim-review
- u1-charge
- charge-reciprocity
category: decisions
confidence: working
status: archived
---
# Review of C-U1-002

## Claim Under Review
Conditional on the independent complex profile
`Psi=A*sech(eta*x)*exp(-i*omega*t)`, `A>0`, and the shared parameterization
`eta=sqrt(1-omega^2)` for `0<omega<1`, its `C-U1-001` charge is
`Q=4*A^2*omega/eta`. Composing with accepted breather energy and secant scale
gives `Q*E=64*A^2*omega` and `Q*H=64*A^2`; the boosted vector composition is
division-free. The complete integer exponent kernel for `(Q,H,E,omega)` has
the two stated generators, whose difference is the definition `H=E/omega`.

## Sourced Inputs
The review read `v0.13.0`, `C-SG-002/006/008`, proposed `C-U1-001`, P014 and
its attempt history, the module/tests and verifiers, and hash-pinned EM1 and
HE3. No complex-field equation that produces the profile, physical charge map,
or quantum premise is imported.

## Independence
The main route uses the canonical closed-form API and SymPy definite integral.
The review instead obtains the norm from the antiderivative
`tanh(eta*x)/eta`, derives the current in polar coordinates, reconstructs the
boost with rapidity, and solves the exponent conditions by elimination without
importing the proposed U(1) APIs.

## Verification Status
Exact integration, differentiation, one-sided limits, vector algebra, and
integer linear equations establish every statement. The first attempt exposed
only a square-root branch representation issue in the bare upper limit; attempt
`0002` uses `Abs(Q)` for that magnitude statement while retaining the exact
positive-domain derivative. Attempt `0003` additionally proves that
`omega^p*eta^q` is constant on the linked family only for `p=q=0`, closing the
necessity step behind the exponent classification. The claim earns
`symbolic_verified`.

## Sensitivity and Counterexamples
Changing the charge coefficient, amplitude power, width power, energy
coefficient, or secant frequency power breaks the coupled charge and product
predicate. In particular `A` rescaling changes 64 to `64*A^2`; this rejects a
normalization-independent numeral while preserving frequency-independence.
The zero-frequency and threshold limits and the regular rest-frame vector form
also pass.

## Framework Compatibility
The claim composes naturally with `C-SG-002/006/008` only after declaring a
shared parameterization. It does not identify the complex profile with the real
breather. Calling `H` a secant scale preserves the accepted rejection of a
universal Planck interpretation. The conditional internal charge is not mapped
to electric charge.

## Dependency and Consumer Replay
Dependencies are `C-U1-001`, `C-SG-002`, `C-SG-006`, and `C-SG-008`. Direct
consumers are the U(1) APIs/tests, EM1 and HE3 dispositions, and future gauge
audits. The existing sine-Gordon formulas are imported unchanged.

## Competing Candidate Audit
The proposal registered separated theorem/profile composition, ansatz-only
continuity, and universal physical identification. Exact dependency closure and
normalization sensitivity select the first. The second cannot support the
general charge language; the third fails the amplitude and real-field guards.

## Four-Axis Decision

The normalization-honest conditional composition supports acceptance.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: additive conditional consequence of C-U1-001 and C-SG-002/006/008

## Promotion Transaction
Promotion adds the declared-profile charge APIs/tests, exact and independent
evidence, `C-U1-002`, the frozen P014 record, `v0.14.0`, qualified EM1/HE3
dispositions, and regenerated canonical consumers.

## Continuation if Not Accepted
A profile failure would reject or reformulate the declared specialization; it
would not alter the general current theorem or accepted breather energy.

## Done Gate
The positive charge and composition formulas, exhaustive exponent solution,
independent route, mutations, normalization ceiling, dependencies, and
consumers are complete with no claim debt.

## Cross-References
See `C-U1-001`, `C-SG-002/006/008`, P014, EM1, HE3, the U(1) module/tests, and
the parent migration effort.
