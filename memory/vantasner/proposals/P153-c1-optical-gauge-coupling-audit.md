---
description: Derive and audit C1's conditional optical-metric gauge coupling
author: vantasner
created: '2026-08-10T05:10:00Z'
updated: '2026-08-10T05:50:00Z'
tags:
- substrate-framework
- campaign-proposal
- migration-C1
- optical-gauge-coupling
category: proposals
confidence: exploratory
status: archived
---
# P153 C1 Optical Gauge Coupling Audit

## Question and Positive Deliverable

P153 must deliver an exact importable classification of a charged scalar on
the accepted static optical metric, including the declared action or equation,
charge and gauge convention, invariant momentum, local pure-gauge limit, and
any topology or boundary data needed for a genuine spectral effect. The
positive result must separate exact conditional dispersion from a physical
medium interaction, gravity effect, or observation.

## Base Release and Provenance

The accepted base is v0.118.0 at framework and scientific commit `41a5d33`.
The source baseline is `/home/dan/substrate` commit
`6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`; later dirty Phase 47/48,
engineering, framework-prose, and memory files remain excluded. C1 is pinned at
`merged-framework/bridges/phase-7/bridge_C1_Aeff_optical_metric_coupling.py`,
SHA-256 `6c0b625cbfd8396104f185e4e3785956f66989a10d9fddf9d553fe433c39f0f5`.
Its dossier is `merged-framework/bridges/phase-7/dossiers/C1-dossier.md`,
SHA-256 `dcaf85bc1855d772a6f4c766a765ec5cfd606444f635fb90fb241bc1f744d5ef`.

The queue exposes dependencies B1, G1, and G2, nine static check calls of which
eight are literal and one dynamic, one assertion, and the broad dispersion.
P152 necessarily executed C1 once as a semantic consumer and exposed all nine
runtime descriptions, the metric, momentum shift, and printed interpretation.
That exposure is recorded rather than hidden and cannot select a candidate.
The remaining source and dossier bodies and exact data flow remain unopened.

## Invariants, Conventions, and Allowed Imports

C-OG-001 supplies the static metric but no charged wave equation. C-GAU-001
supplies `D=partial-i*e*A` and its phase law but no optical medium. C-BER-001
supplies a projective-loop local representative and corrected holonomy but no
physical vector potential or new coupling. C-GOR-001 and C-RAD-001 enforce the
effective-geometry and declared-action ceilings. Qualified B1, G1, and G2
grant no additional authority.

The metric signature, inverse and volume density, scalar action or equation,
mass sign, positive charge, connection components, gauge transformation,
constant versus varying coefficient domain, spatial topology, boundary
condition, and plane-wave labels must be explicit. On the line a constant
`A_x` is pure gauge and only `k-e*A_x` is invariant. A circle can retain its
holonomy only after its global section and boundary data are declared.

## Candidate Preregistration

The candidates are frozen despite the unavoidable P152 runtime preexposure.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal C1 audit | Hash-pinned source and dossier | Source formulas | Retains only evaluated conditional objects | AST, data-flow, process, guard, and mutation audit |
| B | Charged optical Klein-Gordon theorem | Declared exact action on constant optical metric | `n,c0,m,e,A` | Dispersion depends on invariant momentum | Action variation, plane wave, and gauge covariance |
| C | Pure-gauge line classification | Simply connected line and constant `A_x` | Gauge phase | Apparent shift is a relabeling | Explicit gauge removal and unchanged invariant momentum |
| D | Global holonomy spectrum | Circle or bundle and boundary condition | Length and holonomy | Spectral shift may survive | Large-gauge and boundary-condition audit |
| E | Accepted composition only | C-OG-001 and C-GAU-001 | None beyond declarations | No new claim if definition-level | Nonduplication and API audit |
| F | Variable-background boundary | Nonconstant metric or connection | Profile derivatives | C1 operator needs derivative terms | Covariant Laplacian and curvature mutation |
| G | Physical countermodels | Same mathematical ledger with free dictionaries | External interpretation | No medium or gravity follows | Same-dispersion countermodels |
| H | Governance closure | Frozen graph and registry | None | Pending or green sources grant no authority | Dependency, consumer, queue, release, docs, and memory replay |

## Selection Criteria and Blinding

Selection is ordered by explicit action and conventions, gauge covariance,
invariant variables, topology and boundary sufficiency, constant and varying
limits, accepted-framework compatibility, mutation sensitivity, assumption
economy, reusability, nonduplication, and semantic-consumer closure. P152's
preexposed half value, dispersion coefficients, and electrogravitic comparison
do not select a theorem or threshold. The remaining body and dossier stay
closed until this contract and matching manifest are committed.

## Proposed Claim Delta

Source-aware nonduplication reserves `C-OG-005` through frozen revision 0001.
It depends on C-OG-001, C-GAU-001, and C-BER-001 and states the exact
charged-scalar optical action and Euler operator, invariant constant-background
dispersion, pure-gauge line limit, circle spectrum with boundary phase and
large-gauge relabeling, variable-index divergence term, and the sign and
pullback required to map C-BER-001's one-form into the U(1) convention. No
physical medium, breather, electromagnetic, analog-gravity, or real-gravity
dictionary is included.

## Source-Aware Classification

The unchanged source passes all nine predicates. C0 duplicates C-OG-001; C1,
C2, C3, G1, and C4 retain exact conditional algebra only after restoring the
charge, action, invariant momenta, and gauge/topology qualifications. C3b is
vacuous because G was never in the declaration. G2 is dimensionally unclosed:
the declared `eps0` is unused and neither comparator is derived from an
accepted material action. G2b checks symbols inserted by construction.

On the line the constant connection is removed by
`chi=-A_t*t-A_x*x`. On a circle, the mode spectrum depends on the declared
boundary phase and flat-connection holonomy and is invariant under simultaneous
large-gauge connection and mode relabeling. For varying `n(x)`, C1's simple
operator misses `-c0^2*n_x*D_x(Psi)/n^2`. With C-BER-001's same section phase,
the consistent declared pullback is `e*A_x=-B_phi*partial_x(phi)`; the source's
direct dimensionless positive-half substitution is not that map.

## Implementation and Oracle Plan

SymPy exact action variation, covariant derivatives, plane waves, and phase
transformations are the primary oracle. A fresh route will derive the
constant-coefficient operator from the metric and action without importing a
new helper. Exact calculus is stronger than numeric dispersion sampling, so no
numeric rerun counts as independent evidence.

Mutations change the metric inverse, mass sign, charge, phase sign, connection
gradient, time component, topology, boundary condition, and constant-index
assumption. Countermodels remove the constant connection on the line, retain a
circle holonomy, and preserve the dispersion while changing or omitting every
physical medium or gravity dictionary. Compatibility is audited through the
AST: mutable code uses exact algebra, `trapezoid_integral`, or `np.trapezoid`,
never executable `np.trapz`; immutable aliases are used only if a pinned source
actually needs them.

## Attempts and Continuation

Every action, equation, gauge, topology, boundary, compatibility, dependency,
consumer, or verifier failure is append-only with its mechanism and a
materially different next attempt. Invocation errors are repaired without
altering the science; source overclaims yield to another registered candidate.

## Debt Ledger

The ledger tracks source, dossier, proposal, and preexposure hashes; all nine
predicates and one assertion; metric, inverse, determinant, action, equation,
mass, charge, connection, phase, gauge, topology, boundary, constant and
varying limits; B1, G1, and G2 authority; semantic and lexical consumers;
compatibility; nonduplication; disposition; generated state; and parent
continuation. Every item must be derived, declared, rejected, or excluded.

## Review and Promotion Plan

Every affected claim receives individual review. C1 receives a terminal
disposition retaining exact conditional algebra while naming gauge and
physical ceilings. Any distinct theorem is extracted into pure APIs and
focused tests only after a frozen revision. Primary, independent, graph,
compatibility, dependency, consumer, nonduplication, release, queue, docs, and
memory paths are replayed. One integrated gate runs at the final boundary.

## Done Gate

P153 closes only when the action or equation premise, optical operator,
dispersion, invariant momentum, pure-gauge and global-holonomy limits, all nine
source predicates, physical content, compatibility, semantic consumers,
generated state, and debt ledger close through accepted APIs or a reviewed
addition. A physical medium or gravity effect additionally requires a governed
material action, field dictionary, topology or source, coupling, preparation,
observable, and evidence; a substituted half connection cannot replace them.

## Cross-References

See C1, C1-dossier, B1, G1, G2, C-OG-001, C-GAU-001, C-BER-001, C-GOR-001,
C-RAD-001, P004, P030, P141, P142, P152, `optical_geometry.py`, `gauge_u1.py`,
`berry_holonomy.py`, and the parent migration effort.
