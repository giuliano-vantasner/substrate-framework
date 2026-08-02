---
description: Independent review of C-SYM-002 reciprocal-coupling involution and normalization covariance
author: vantasner-review
created: '2026-08-03T13:00:00Z'
updated: '2026-08-03T13:00:00Z'
tags:
- substrate-framework
- claim-review
- coupling-duality
category: decisions
confidence: established
status: archived
---
# C-SYM-002 Claim Review

## Claim Under Review

C-SYM-002 states an exact conditional theorem for positive reciprocal maps:
their involution, orbit product, fixed coordinate, arbitrary-target inverse
family, and covariance under coupling-coordinate rescaling. It explicitly
separates those algebraic facts from a physical action duality, restriction to
a self-dual subfamily, or parameter-selection mechanism.

## Sourced Inputs

The review reads release `v0.69.0`, C-SG-001, C-RGE-001, C-RGE-003,
C-DIM-008, C-TOP-002, their canonical modules and reviews, P077's frozen
contract, attempts 0001 and 0002, the hash-pinned AS6 reproduction and source
audit, candidate comparison, impact map, new canonical module, focused tests,
both verifier routes, and the two primary papers recorded in the provenance
ledger. Pending AS7 and every later operating-point narrative supply no
accepted premise.

## Independence

The independent route imports no `coupling_duality`, `scale_transmutation`,
`scale_provenance`, `renormalization`, or `sine_gordon` API. It rebuilds the
reciprocal map, double application, fixed solve, coefficient mutation,
arbitrary-target family, coordinate conjugation, off-fixed counterexample,
phase counterexample, and hierarchy orientation from fresh SymPy expressions,
then audits the immutable source text separately.

## Verification Status

The maximum verdict is `symbolic_verified`. The primary route passes 30 exact
checks, the independent route passes 23 exact checks, and 105 affected
canonical tests pass. Every promoted quantity is an exact SymPy expression.
No simulation, fit, unresolved integral, numerical quadrature, deprecated
`np.trapz`, or replacement NumPy alias is used.

## Sensitivity and Counterexamples

Changing `A` from `16*pi^2` to `25*pi^2` moves the fixed coordinate from
`4*pi` to `5*pi`. Setting `A=t^2` makes any supplied positive `t` fixed,
exposing inverse construction rather than selection. The explicit pair
`2 <-> 9/2` under `D_9` is dual but not self-dual. Rescaling the coordinate
without the required `A'=rho^2*A` fails conjugation. Finally,
`exp(i*x/4)=-1` at both `4*pi` and `12*pi`, so AS6's phase check does not
uniquely select its point.

## Framework and Literature Compatibility

The exact ledger is a compatible algebraic extension and changes no accepted
invariant. Coleman's quantum result supports a `beta^2=4*pi` free-fermion
point only in his explicit sine-Gordon/massive-Thirring normalization. The
primary self-dual sine-Gordon model is a two-cosine extension with a dual field
and equal amplitudes. Its N=2 normalization conditionally realizes
`x->16*pi^2/x`, so it is a valid external model for the algebra, but those
extra action premises are absent from AS6 and C-SG-001's normalized classical
root. C-RGE-003 supplies the opposite inverse-energy length orientation from
AS6, and C-TOP-002 excludes the physical baryon identity used in its selection
analogy.

## Dependency and Consumer Replay

The accepted claim has no claim dependency: its reciprocal theorem uses only
declared positive real algebra. The AS6 source disposition additionally maps
C-SG-001, C-RGE-003, C-DIM-008, and C-TOP-002 for source-specific
interpretation ceilings. The new consumers are package code
and exports, focused tests, P077 verification, governance records, generated
claim/release memory, and the AS6 disposition. GitNexus reports LOW impact for
the inspected neighboring and shared APIs with no affected execution flow;
direct search covers the additive unindexed module.

## Competing Candidate Audit

Candidates B-F survive the predeclared criteria as a conditional
specialization, general family, coordinate-covariance theorem,
action-dependency ceiling, and off-fixed counterfamily. Candidate A remains
source regression evidence only. The source's hierarchy and two numerical
guards were opened after freeze and did not select the coefficient, theorem,
normalization, tolerance, or verdict.

## Four-Axis Decision

The exact evidence supports acceptance.

- Verification: `symbolic_verified`
- Review: `accepted`
- Compatibility: `compatible_extension`
- Epistemic: `active`
- Relationship: no claim dependencies and challenges no accepted claim; the AS6 disposition separately maps existing interpretation ceilings

## Promotion Transaction

Promotion adds C-SYM-002 to `v0.70.0`, qualifies AS6 through the editable
disposition source, regenerates the queue, and synchronizes code, tests,
immutable campaign evidence, registry, release manifests, generated docs, and
accepted memory. One integrated workflow gate includes the complete pytest
suite; record-only synchronization receives targeted validation rather than a
duplicate full-suite ceremony.

## Done Gate

Claim-level debt closes only after registry, release, queue, docs, memory,
campaign, affected consumers, and integrated validation agree. The parent
migration remains active because later source units remain pending.

## Cross-References

See P077, AS6, C-SG-001, C-RGE-003, C-DIM-008, C-TOP-002,
`coupling_duality.py`, `test_coupling_duality.py`, base release `v0.69.0`, and
the parent migration effort.
