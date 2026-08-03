---
description: Independent review of the exact conditional signed energy-difference theorem
author: vantasner-review
created: '2026-08-07T16:50:00Z'
updated: '2026-08-07T16:50:00Z'
tags:
- substrate-framework
- claim-review
- energy-difference
- exact-algebra
category: decisions
confidence: established
status: archived
---
# Review of C-RDIFF-001

## Claim Under Review

C-RDIFF-001 states that for positive energy scale `U`, positive normalization
`alpha`, positive integer initial degree `A` and multiplicity `n`, and real
dimensionless coefficients, the declared masses `M(k)=alpha*b(k)*U` and
bindings `B_E(k)=k*M(1)-M(k)` obey
`n*M(A)-M(nA)=B_E(nA)-n*B_E(A)=alpha*U*(n*b(A)-b(nA))`. The normalized
coefficient, inverse, sign and zero surfaces, monotone rectangular interval
image, and limitation on differencing separate upper bounds are part of the
claim. It challenges and supersedes no accepted claim.

## Sourced Inputs

The review reads release v0.89.0, C-DIM-002, C-RPROF-001/002, P106's initial
freeze and proposal revision 0001, attempts 0001 through 0004, primary and
independent verifiers, source reproduction and predicate audit, candidate and
dependency ledgers, consumer map, importable module, focused tests, and E3 at
SHA-256 `aa76b9e675d4fbb45594e9d3df5107af175e927a24840260ca71ffda1bad3315`.
E3's physical action, state, reaction, empirical scale, BPS, and overbinding
subclaims are outside this claim.

## Independence

The primary route constructs the direct declared masses and derives the signed
difference. The independent reviewer imports no P106 expression or canonical
energy-difference API; it starts from fresh one-body, degree-two, degree-four,
normalization, and scale symbols, forms both binding energies, and cancels the
one-body mass. The independent route also rederives interval endpoints and
upper-bound counterexamples.

## Verification Status

The maximum verdict is `symbolic_verified`. SymPy simplification proves the
direct and binding routes identical, removes the shared scale and one-body
term, solves the inverse, and derives sign and zero surfaces. All exact outputs
are resolved expressions with no unevaluated integral, derivative, root, or
condition. The canonical float API is regression coverage rather than the
exact oracle.

## Sensitivity and Counterexamples

Changing `3*pi^2` to `12*pi^2`, multiplicity two to one, or subtraction to
addition breaks the baseline identity check. Positive, zero, and negative
examples test the sign surface. For separate upper bounds `x<=X` and `y<=Y`,
the exact slack ledger gives `x-y=(X-Y)-(delta_x-delta_y)`; valid examples put
the actual difference on either side of `X-Y`. Only the zero-slack limit
recovers the difference of bounds. Attempts 0002 and 0004 preserve verifier
representation mistakes—structural SymPy equality and bit-level float
equality—and repair them without changing the theorem or thresholds.

## Framework Compatibility

C-DIM-002 supplies only the dimensional ceiling that coefficients and physical
primitive choices remain free. C-RDIFF-001 is a compatible exact
transformation with all normalization, scale, coefficient, and binding
definitions explicit. It identifies no degree with a baryon or nucleus and
does not supply a physical action, minimum, mass, reaction, or measurement.

## Dependency and Consumer Replay

The theorem depends on C-DIM-002 and exact real algebra. E4 and KI2 through KI5
may reuse the transform but gain no BPS interpolation, endpoint, or physical
premise. MK5, MR2, and MR5 gain a canonical regression function but their
generalized models remain pending. GitNexus finds LOW additive impact, one
direct and one transitive internal caller, and no affected execution process.
No claim debt remains.

## Competing Candidate Audit

Candidates were frozen before E3 body inspection. Literal reproduction failed
scientific closure; direct and independent algebra, interval propagation,
upper-bound counterexamples, and physical-premise audit were selected by exact
closure and sensitivity rather than comparator values. Nonduplication found no
accepted registry theorem and multiple divergent downstream copies, justifying
proposal revision 0001 and the minimal API.

## Four-Axis Decision

The exact claim is accepted on four independent axes.

- Verification: `symbolic_verified`
- Review: `accepted`
- Compatibility: `compatible_extension`
- Epistemic: `active`
- Relationship: depends on C-DIM-002; challenges and supersedes none

## Promotion Transaction

Promotion adds C-RDIFF-001, the pure `energy_differences.py` implementation and
tests, immutable P106 evidence, qualified E3 disposition, release v0.90.0,
generated claim documentation and memory, and an updated parent effort. The
primary verifier, independent reviewer, focused tests, repository validator,
generated-state checks, one full workflow gate, and diff check must pass.

## Continuation if Not Accepted

If any exact identity, mutation, dependency, or consumer gate fails, the claim
returns to P106 for a recorded repair while E3 remains pending. A missing
physical map does not weaken this exact conditional theorem or complete the
physical objective.

## Done Gate

Acceptance requires the actual exact object, independent derivation,
mutation-sensitive checks, upper-bound counterexamples, importable API, tests,
source and consumer adjudication, synchronized canonical records, and an empty
claim ledger. A source tally or comparator mismatch cannot substitute.

## Cross-References

See P106, E3, C-RDIFF-002, C-DIM-002, C-RPROF-001/002, P085, P105,
`energy_differences.py`, release v0.90.0, and the framework-migration effort.
