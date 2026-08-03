---
description: Independent review of the exact conditional BPS topological bound
author: vantasner-review
created: '2026-08-03T16:32:00Z'
updated: '2026-08-03T16:32:00Z'
tags:
- substrate-framework
- claim-review
- bps-bound
- topological-degree
category: decisions
confidence: established
status: archived
---
# Review of C-BPS-001

## Claim Under Review

C-BPS-001 states an exact conditional theorem. Let `X` be a closed connected
oriented three-manifold with volume form `dvol`, let the target be the oriented
unit round `S^3` with volume form `Omega` and integral `2*pi^2`, and let a
sufficiently regular map `U:X->S^3` have nonzero signed degree `B`. Define its
normalized pullback density by `U*Omega/(2*pi^2)=B0*dvol`. For positive
`lambda,mu`, nonnegative target potential `V` with integrable square root, and
`W=(1/(2*pi^2))*integral_S3 sqrt(V) Omega`, the declared energy
`E=integral_X[(lambda*pi^2*B0)^2+mu^2*V(U)]dvol` obeys
`E>=2*lambda*mu*pi^2*abs(B)*W`. Equality holds exactly when
`lambda*pi^2*B0=sign(B)*mu*sqrt(V(U))` almost everywhere. The claim asserts no
existence or physical interpretation.

## Sourced Inputs

The review reads release v0.90.0, P107's frozen contract, E4 at SHA-256
`f1815eefc73e577734992a3147d9ec6cea2b50fad8532e9f436e1afb465dfea7`,
attempts 0001 through 0005, primary and independent exact verifiers, source and
predicate audits, dependency and consumer ledgers, the package module, focused
tests, and the later hash-pinned convention consumers only as noncanonical
evidence. E4's universal saturation and physical yield statements are outside
this claim.

## Independence

The primary route completes the square in both orientation branches and then
uses the normalized degree pairing. The independent reviewer imports no P107
BPS package helper. It rederives the unit target volume from hyperspherical
measure, uses pointwise AM-GM plus the triangle inequality, checks identity and
orientation-reversal maps, and evaluates an explicit target potential.

## Verification Status

The maximum verdict is `symbolic_verified`. Exact algebra resolves both square
identities and their equality equations. The standard oriented degree theorem
is a declared mathematical import, not an unevaluated symbolic integral
mistaken for proof. The independent route derives `integral Omega=2*pi^2` and
`W=32*sqrt(2)/(15*pi)` for `V=1-cos(chi)` exactly, confirming the displayed
normalization without making that potential part of the general claim.

## Sensitivity and Counterexamples

Changing the target divisor, dropping or changing `pi^2`, or using the wrong
orientation breaks a relevant check. Signed pairings reverse under degree
reversal while the lower bound remains unchanged. With `V=0`, the equality
equation forces `B0=0` almost everywhere and cannot be satisfied at nonzero
degree; this proves that a correct lower bound does not imply universal
saturation. Attempt 0002 preserves two test-representation defects and repairs
them without changing the theorem.

## Framework Compatibility

The claim introduces one declared mathematical energy surface with all
normalizations and dimensions explicit. It changes no accepted invariant and
selects no action, coupling, potential, map degree, physical baryon, nucleus,
or empirical scale. It is a compatible extension and not evidence that the
framework realizes the model physically.

## Dependency and Consumer Replay

C-BPS-001 has no accepted-claim dependency; it imports the standard oriented
degree/pullback theorem. C-BPS-002 may use its bound and equality condition.
KI and MK consumers gain no coupling values or interpolation. The exact
convention replay gives `lambda_A=pi^2*lambda_B`: E4's displayed bound is
correct for convention B, while applying it to convention-A lambda adds one
spurious `pi^2`.

## Competing Candidate Audit

Literal E4 reproduction, two-branch square completion, independent AM-GM,
sector attainment, counterexamples, asymptotic algebra, convention audit, and
nonduplication were frozen before source execution. Candidates B and C were
selected by exact closure and normalization sensitivity, not by an empirical
mass or binding comparator.

## Four-Axis Decision

The exact conditional bound is accepted on four independent axes.

- Verification: `symbolic_verified`
- Review: `accepted`
- Compatibility: `compatible_extension`
- Epistemic: `active`
- Relationship: challenges and supersedes none

## Promotion Transaction

Promotion adds C-BPS-001, the pure `bps_energy.py` implementation and tests,
immutable P107 evidence, qualified E4 disposition, release v0.91.0, generated
documentation and memory, and the parent migration update. The integrated gate
must pass once at the final boundary.

## Continuation if Not Accepted

If the degree normalization, orientation, equality, mutation, or consumer gate
fails, the claim returns to P107 for an append-only repair while E4 remains
pending. Missing physical realization does not weaken the exact conditional
theorem or complete the broader source narrative.

## Done Gate

Acceptance requires the exact bound, independent normalization route,
counterexample, sensitive mutations, package API, tests, source and consumer
ceilings, synchronized records, and an empty claim ledger.

## Cross-References

See P107, E4, C-BPS-002, C-BPS-003, C-RDIFF-001, `bps_energy.py`, release
v0.91.0, and the framework-migration effort.
