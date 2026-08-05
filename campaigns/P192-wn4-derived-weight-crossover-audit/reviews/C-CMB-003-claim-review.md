---
description: Independent review of C-CMB-003
author: vantasner-review
created: '2026-08-11T18:55:00Z'
updated: '2026-08-11T19:05:00Z'
tags:
- substrate-framework
- claim-review
- C-CMB-003
category: decisions
confidence: established
status: active
---
# C-CMB-003 Claim Review

## Claim Under Review

C-CMB-003 proposes the exact shape, generating, moment, and tail theorem for
C-OSC-001's normalized all-nonnegative factorial-one mass
`p_S(n)=exp(-S)S^n/n!`. The claim states strict log-concavity while retaining
the positive-integer adjacent mode tie, derives PGF `exp(S(t-1))` and every
falling-factorial moment `S^r`, gives an exact eventual geometric point and
upper-tail majorant, and certifies decay faster than every fixed inverse power.
It explicitly excludes physical Poisson-process, rate, regime, medium,
subdivision, and material readings. The proposed relationship is a dependency
on C-OSC-001 with no challenge or supersession.

## Sourced Inputs

The review reads v0.142.0 at commit `9df59fb`, accepted C-OSC-001 and its
C-SG-019 closure, P192 Attempts 0001 through 0010, the frozen formula and input
inventory, the additive module and focused tests, both serious verifiers, the
hash-pinned WN4 source, and its predicate audit. WN4's exact ratio,
log-concavity quotient, exponential normalization, mean, variance, and tail
ratio survive. Its single-mode-at-integer-S, `S-n` residual, physical regime,
power-law interpolation, and medium-mean conclusions remain outside the claim.

## Independence

The 47-check independent route imports no candidate or accepted scientific
API. It constructs raw factorial coefficients, exact mode grids, the
exponential series, PGF derivatives, geometric majorants, scaled-power ratios,
and zero-coupling and zero-spectral-density countermodels directly in SymPy.
It does not reuse candidate functions, constants, certificate thresholds, or
proof-shaped outputs.

## Verification Status

The maximum warranted status is symbolic verified. The 115-check primary route
evaluates the actual APIs, exact coefficients, derivatives, inequalities,
threshold rejections, and mutations. The 47-check independent route
reconstructs the load-bearing mathematics. All sums and derivatives used for
the claim reduce to explicit exponential or polynomial expressions; no
unevaluated integral, sum, root, or unresolved condition carries a verdict.
Finite grids are used only for regression and counterexamples, not universal
proof. Attempts 0006 through 0009 preserve normal-form and oracle-target
failures rather than weakening the theorem.

## Sensitivity and Counterexamples

The checks reject squared factorials, inverted and unit log-concavity ratios,
single-mode deletion at integer S, PGF sign and normalization changes, confused
falling/raw/variance moments, the one-step-early geometric threshold, wrong
geometric exponents and starting masses, and polynomial thresholds omitting S,
`2^r`, or contraction. Integer S gives the decisive two-mode counterexample.
Zero coupling and zero final-state spectral density independently null any
putative rate while leaving the mathematical mass positive.

## Framework Compatibility

The claim is a compatible extension of C-OSC-001 with one supplied exact
positive dimensionless intensity and no fitted constant. It preserves all
sample-space distinctions and adds no change to C-SG-019, the Fock ladder, the
positive-odd mass, branching, or physical sectors. Rational restrictions in
the constructive mode and polynomial-certificate APIs are exact-decidability
interfaces, not restrictions on the symbolic theorem.

## Dependency and Consumer Replay

The direct claim dependency is C-OSC-001 and the transitive closure is
C-SG-019. The source graph has 17 hash- and compatibility-checked nodes. P191's
immutable 16-node, 637-check execution record is reused because every byte and
predicate inventory is unchanged; PN2 alone is newly relevant and freshly
passes 25 checks. WN2 remains qualified without a forward dependency. WN5,
WN6, WN7, and MD1 through MD6 remain individually pending. No node requires a
legacy NumPy alias, so no compatibility event affects a scientific verdict.

## Competing Candidate Audit

Seven candidates and ordered structural criteria froze before renewed source
execution. Accepted-composition-only candidate B is insufficient because
C-OSC-001 does not own log-concavity, PGF/factorial moments, or quantified
tails. Candidates C, D, and E are selected for exact novelty and cohesion; A
remains source evidence, F supplies physical countermodels, and G is the
governance route. No exposed WN4 sample selects the theorem.

## Four-Axis Decision

The four axes support promotion once the governed transaction passes.

- Verification: symbolic_verified
- Review: accepted contingent on the integrated promotion transaction
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: depends on C-OSC-001; challenges none; supersedes none

## Promotion Transaction

Promotion must register only the reviewed statement and C-OSC-001 dependency,
retain the importable module and tests, move P192 unchanged into campaigns,
create the exact next release, qualify WN4 through C-OSC-001 and C-CMB-003,
generate the migration queue, docs, and accepted memory, add durable claim and
source decisions, and run one integrated gate plus `git diff --check`.

## Continuation if Not Accepted

If any graph, schema, generation, or integrated gate fails, P192 remains active
and the next append-only attempt repairs the failing representation or returns
to another preregistered candidate. A source no-go or physical ceiling does not
complete the campaign.

## Done Gate

The claim is recommended for promotion only with empty P192 debt and exact
agreement among the registry, release, disposition, implementation, tests,
immutable campaign, generated records, and durable memory.

## Cross-References

See P192, C-OSC-001, C-SG-019, WN4, WN5 through WN7, MD1 through MD6,
`bosonic_fock.py`, `test_factorial_one_distribution.py`, and the parent
framework-migration effort.
