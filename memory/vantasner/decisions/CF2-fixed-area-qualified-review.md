---
description: Retain CF2 qualification after exact fixed-area closure audit
author: vantasner-review
created: '2026-08-10T23:20:00Z'
updated: '2026-08-10T23:20:00Z'
tags:
- substrate-framework
- source-review
- migration-CF2
- fixed-flux-tube
category: decisions
confidence: established
status: archived
---
# CF2 Fixed-Area Qualified Review

## Source Unit Under Review

CF2 proposes a uniform fixed-area flux construction, stored field-energy line,
endpoint constant-force line, Riesz-row interpretation, spherical guard, and a
physical quark-confinement reading.

## Sourced Inputs

The review read v0.127.0, C-FLX-001, separate C-VTX-001/002, C-MAX-001 and
C-WIL-001 boundaries, `flux_tube.py`, P027/P167 adjudications and immutable
evidence, hash-pinned CF2 and its dossier, the current migration disposition,
and local memory. CF2 and the dossier match source baseline `6d1f4e0`;
unrelated predecessor worktree changes are excluded.

## Compatibility and Reproduction

Native CF2 imports only SymPy, exits cleanly, and passes all fifteen
predicates. It and canonical `flux_tube.py` have no NumPy integration surface.
The six-node narrative graph uses isolated aliases backed by `np.trapezoid`
only for immutable CF1 and CF5; compatibility neither rejects nor selects a
scientific candidate.

## Scientific Closure

Uniform cap data and fixed area give `E=Phi/A`. Declared field-energy density
gives `U=Phi^2*L/(2*A)` with slope `Phi^2/(2*A)`. Separately, declared endpoint
force gives `V=q*Phi*L/A` with slope `q*Phi/A`. Equality holds if and only if
`q=Phi/2`; at `q=Phi`, endpoint work is twice field energy. CF2's executable
energy path never uses `q`, so its common-force narrative is qualified.

An expanding area gives logarithmic field energy, while spherical spreading
gives a curved inverse-radius potential. These are conditional geometry
statements, not a physical phase theorem. Riesz exponent matching is arithmetic
only. Effective-area inversion reconstructs a supplied tension, and no
accepted map identifies C-VTX-001/002's smooth vortex with CF2's ideal area.

## Verification and Sensitivity

The primary, fresh exact, source-graph, and focused-test routes pass 39, 19, 31,
and 43 checks or tests. The graph contains six nodes, 66 lexical and 66 runtime
predicates, and eight assertions. Wrong energy coefficient, area power,
charge-flux equality, variable geometry, spherical spreading, supplied-tension
prediction, and physical-label inference are sensitive or explicitly countered.

## Dependency and Consumer Replay

C-FLX-001 has no accepted scientific dependency. C-VTX-001/002, C-MAX-001,
and C-WIL-001 remain separate contexts, and all five source graph links remain
narrative only. Forty-three affected and adjacent tests pass. No public API,
claim, release, or generated accepted document changes.

## Candidate Audit

Candidate A succeeds as literal reproduction, Candidate B supplies the exact
scientific composition, and Candidate H closes governance. Candidate C is
unnecessary because endpoint work survives when kept separate. Candidate D
duplicates accepted geometry guards. Candidate E lacks a vortex-to-tube map.
Candidate F lacks physical dependencies and an oracle. Candidate G supplies
only exponent arithmetic.

## Four-Axis Decision

The accepted claim retains its prior four-axis state.

- C-FLX-001: symbolic verified, accepted, compatible extension, active.
- CF2 disposition: qualified through C-FLX-001.
- Relationship: unchanged accepted composition; no supersession or challenge.

## Qualification Transaction

P168 preserves native source reproduction, materializes individual predicate
verdicts and provenance, expands CF2's qualification evidence, regenerates the
source queue, archives proposal and review memory, and synchronizes the parent
effort. v0.127.0 and 163 accepted claims remain unchanged.

## Done Gate

Both positive conditional linear constructions exist and are independently
derived, their exact distinction is mutation-sensitive, every source predicate
and assertion is typed, settled P027 evidence is hash-reused, consumers and
the graph agree, physical overreach is excluded, and no campaign debt remains.

## Cross-References

See C-FLX-001, C-VTX-001, C-VTX-002, C-MAX-001, C-WIL-001, P027, P167, P168,
CF1, CF2, CF5, EM3, EM7, QCD3, `flux_tube.py`, and the framework-migration and
NumPy-compatibility efforts.
