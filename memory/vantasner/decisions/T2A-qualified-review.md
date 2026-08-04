---
description: Terminal review of T2A's boosted stress and dilaton-source claim
author: vantasner-review
created: '2026-08-09T00:20:00Z'
updated: '2026-08-09T00:20:00Z'
tags: [substrate-framework, source-review, sine-gordon, stress-tensor, migration-T2A]
category: decisions
confidence: established
status: archived
---
# Review of T2A Terminal Qualification

## Claim Under Review

T2A claims that a uniformly Lorentz-boosted sine-Gordon breather is a new
conserved moving dilaton source with exact boosted charges, nonzero mixed source,
and a time-averaged integrated spatial stress carrying two powers of gamma.

## Sourced Inputs

The review reads v0.100.0, C-SG-001, C-SG-002, C-SG-008, C-SG-012, the P132
frozen proposal, all append-only attempts, both verifiers, hash-pinned T2A,
qualified GW1 and GW4, pending reverse consumers G1 and G4, and the hash-pinned
local Note-13 dilaton specialization. The cited 2D dilaton-gravity review is
checked at its arXiv and publication record. No pending physical conclusion is
imported.

## Independence

The primary route uses canonical breather and stress APIs plus exact source AST
audits. The independent route imports none of those APIs: it constructs the
Lorentz matrix, transforms a generic symmetric tensor and charge vector, derives
the transformed cycle duration, and directly integrates independently coded
breather derivatives with mpmath refinement.

## Verification Status

The accepted surviving surface retains `symbolic_verified` through existing
C-SG-008 and C-SG-012 authority. Thirty-nine primary and nineteen independent
checks reproduce the exact boost, charge, dispersion, tensor signs, divergence,
cycle average, counterexamples, limits, and source typing. Numerical quadrature
is regression evidence only. T2A promotes no new claim and cannot inherit an
exact verdict for its rejected spatial-stress or dilaton-source predicates.

## Sensitivity and Counterexamples

Wrong gamma, velocity sign, rest energy, mixed-index sign, missing lab-period
factor, nonrelativistic charge, pointwise-versus-integrated null, and zero-
acceleration mutations all break the relevant verdict. A generic standing
breather point has nonzero `T_tx` despite zero integrated momentum. At `v=0.8`,
the source's stress formula exceeds the corrected result by `5/3`. Six verifier
representation or resolution failures are preserved; no threshold was widened.

## Framework Compatibility

The exact scalar boost and canonical stress are native to the accepted
sine-Gordon sector. T2A's alleged covariant component uses the contravariant
sign. Its local static dilaton ansatz cannot match the standing field's generic
pointwise mixed stress, and no time-dependent target solution is constructed.
No accepted invariant needs revision.

## Dependency and Consumer Replay

Qualified GW1 and GW4 supply no physical dilaton or radiation premise beyond
their accepted conditional surfaces. Pending G1 and G4 reproduce twenty checks
after aliasing three immutable `np.trapz` calls to `np.trapezoid`; their pending
radiation and self-force claims gain no authority. T2A itself has no NumPy or
compatibility path. No mutable consumer retains `np.trapz`.

## Competing Candidate Audit

Candidates A through H and structural criteria froze before the source body was
opened. Exact Lorentz derivation, accepted-claim composition, independent
spacetime averaging, refined regression, physical countermodels, and governance
closure are selected. Literal replay is evidence only, and the new dilaton-
source candidate fails because the required typed and solved target equation is
absent, not because of numerical disagreement.

## Four-Axis Decision

No new claim is accepted. T2A is audited, compatible with the exact accepted
boost and stress claims, and epistemically qualified. It challenges or
supersedes no accepted claim; C-SG-001, C-SG-002, C-SG-008, and C-SG-012 remain
unchanged.

## Promotion Transaction

The terminal transaction adds immutable P132 evidence, the qualified T2A
disposition, regenerated source queue, archived proposal and decision memory,
and the parent-effort checkpoint. It adds no package API, registry claim,
release, or generated accepted documentation; v0.100.0 remains current.

## Continuation if Not Accepted

A future dilaton-source proposal would need a separately accepted action and
coupling, a time-dependent metric/dilaton ansatz, full local tensor matching,
boundary and initial data, a solved coupled equation, independent review, and
consumer closure. It cannot revive T2A's index error or extra-gamma formula.

## Done Gate

P132 closes only after source, exact, independent, refinement, mutation,
dependency, consumer, nonduplication, provenance, compatibility, generated
queue, integrated workflow, and debt gates pass. The parent corpus migration
continues with the next pending unit.

## Cross-References

See P012, P036, P039, P049, P132, T2A, GW1, GW4, G1, G4, C-SG-001,
C-SG-002, C-SG-008, C-SG-012, reserved C-SG-020, and v0.100.0.
