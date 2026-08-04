---
description: Retain CF1 qualification after current-NumPy alias-only reproduction
author: vantasner-review
created: '2026-08-10T22:34:00Z'
updated: '2026-08-10T22:34:00Z'
tags:
- substrate-framework
- source-review
- migration-CF1
- numpy-compatibility
category: decisions
confidence: established
status: archived
---
# CF1 Current-NumPy Qualified Review

## Source Unit Under Review

CF1 proposes a declared Abelian-Higgs radial vortex, numerical profile and
tension, quantized flux, screened tails, and a zero-vacuum guard, then labels
the construction a dual chromoelectric QCD confinement mechanism.

## Sourced Inputs

The review read v0.127.0, C-DIM-007, C-VTX-001, C-VTX-002, C-FLX-001, the
accepted vortex, numerics, and flux modules, P026/P027 adjudications and
reviews, hash-pinned CF1 and its dossier, the current migration disposition,
local memory, and primary publication records. CF1 and the dossier match
source baseline `6d1f4e0`; unrelated predecessor worktree changes are excluded.

## Compatibility and Reproduction

Native CF1 passes two exact checks and then stops only because NumPy 2.5.1 has
no `np.trapz`. The failure is preserved. An isolated process binds that legacy
name only to `np.trapezoid`, leaves the source unchanged, exits cleanly, and
passes all eight predicates. The version event neither rejects nor selects a
scientific candidate.

Canonical code has zero executable legacy references and uses the shared
`trapezoid_integral`. The expensive P026 refinement and independent
finite-difference evidence is hash-identical to the accepted version; P167
therefore reruns current-environment-sensitive source, canonical, exact,
graph, and focused-consumer gates instead of ceremonially repeating every
unchanged mesh.

## Scientific Closure

C-VTX-001 exactly owns the corrected general-coupling functional, equations,
positive-vacuum finite-energy boundary, flux, ungauged divergence, and inverse
lengths. C-VTX-002 owns only the explicit resolution-bounded profile and
tension evidence. A fresh exact derivation confirms the source's `g=1`
specialization, flux, inverse lengths, zero-vacuum limit, and exact `v^2`
scaling.

The source BVP is not a continuum existence or uniqueness theorem. Its tail
fits regress against exact masses. Its zero-vacuum solve finds the trivial
branch but proves no uniqueness. Its “dual,” “chromoelectric,” “QCD,” and
“confinement” labels have no accepted dependency map or nonperturbative oracle.
C-FLX-001 remains separate because its field-energy and endpoint-work slopes
require independent flux, area, and charge data and agree only under an extra
condition.

## Verification and Sensitivity

The primary, fresh exact, source-graph, and focused-test routes pass 26, 16, 30,
and 39 checks or tests. The graph contains six nodes, 51 lexical and 51 runtime
predicates, and seven assertions. Wrong friction, gauge sign, coupling
normalization, asymptotic boundary, missing flux coupling, zero-vacuum
uniqueness inference, compatibility name, and cross-model identity are all
sensitive or explicitly countered.

## Dependency and Consumer Replay

C-VTX-001 has no accepted scientific dependency; C-VTX-002 depends only on it.
M1 and M2 are nonexecuted narrative templates, while CF2-CF4 are downstream
negative scope. Thirty-nine affected and adjacent tests pass. No public API,
claim, release, or generated accepted document changes.

## Candidate Audit

Candidate A succeeds as the compatibility-neutral reproduction route,
Candidate B supplies the scientific composition, and Candidate G closes
governance. Candidate C is unnecessary because numeric status and regression
gates pass. Candidate D duplicates accepted APIs. Candidate E lacks physical
dependencies. Candidate F lacks the map required to compose C-FLX-001.

## Four-Axis Decision

The accepted claims retain their prior four-axis states.

- C-VTX-001: symbolic verified, accepted, compatible extension, active.
- C-VTX-002: numeric evidence, accepted, compatible extension, qualified.
- CF1 disposition: qualified through their composition.
- Relationship: unchanged accepted composition; no supersession or challenge.

## Qualification Transaction

P167 preserves the immutable source failure and alias replay, materializes
individual predicate verdicts and provenance, updates CF1's stale compatibility
note and evidence paths, regenerates the source queue, archives proposal and
review memory, and synchronizes the parent effort. v0.127.0 and 163 accepted
claims remain unchanged.

## Done Gate

The positive conditional vortex object reproduces under current NumPy, every
source predicate and assertion is typed, accepted scope and independent exact
closure pass, expensive evidence reuse is hash-justified, consumers agree, and
no scientific or governance debt remains.

## Cross-References

See P026, P027, P167, CF1, C-DIM-007, C-VTX-001, C-VTX-002, C-FLX-001,
`abelian_higgs_vortex.py`, and the framework-migration and NumPy-compatibility
efforts.
