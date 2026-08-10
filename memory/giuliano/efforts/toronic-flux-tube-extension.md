---
description: 'Toronic flux-tube extension: structural flat-connection obstruction, validated minimal flux background, Minkowski tube-ensemble analysis (issue #28)'
author: giuliano
created: '2026-08-10T18:05:00+00:00'
updated: '2026-08-10T18:05:00+00:00'
tags:
- effort
- toronic-casimir
- issue-28
category: efforts
confidence: working
status: active
---

## Goal and Success Contract
This effort delivers the extension scope split out of PR #27 by the
2026-08-10 harvest review, behind its own pre-existing issue #28: (1) the
flat-connection obstruction for the Sec. 10 bundle with fundamental matter
as a structural verifier (explicit quotient kernel, exact cover cocycle,
wrong-kernel mutation); (2) the minimal flux background with classical
energy, lattice construction validated by plaquette, total-flux/winding,
gauge-covariance, and refinement checks, plus a continuous no-twist
falsifier; (3) the static-tube/isotropic w = 1/3 atom and the orbit-measure
question with derived invariant measures only. Complete when targeted tests
pass, validate.sh passes once at the boundary, and the PR is open against
issue #28. No claim promotion.

## Baseline
PR #27 head (bf68ee1f) carries the narrowed audit core (two-route twisted
Casimir verification, entrywise commutant, preprint algebra checks). The
extension builds on it via the stacked branch
research/flux-tube-extension. The first-pass versions of these atoms lived
in PR #27 history (commit 61b5810c) and were refuted or narrowed by review:
the boolean obstruction (needs structural encoding), the old "uniform-flux"
construction (carries ZERO net U(1) flux under the plaquette check — the
flux belongs in su(2)), the 0.125-grid no-twist scan (needs a continuous
falsifier), and the stand-in orbit integrals (need derived measures).

## Constraints and Invariants
Write surfaces: `src/substrate_framework/toron_bundle.py`,
`src/substrate_framework/flux_tube_ensemble.py`, their tests,
`src/substrate_framework/__init__.py`, `memory/giuliano/`. No edits to
accepted claims or the #27 core beyond reuse. The reviewer's structural
gate: no hard-coded booleans; every construction claim has a construction-
level check; measure statements only with derived measures.

## Decomposition
Dependency-ordered steps for the effort.

1. [x] Issue #28 opened (predeclared scope).
2. [x] Exact topology: transition-function cocycle (-I, +1) computed symbolically; cover commutator phase-independence; kernel membership with wrong-kernel and no-quotient mutations.
3. [x] Flux background: su(2) and u(1)_Y candidates, minimum at SM couplings, dominance over the one-loop gauge term.
4. [x] Lattice construction checks: exactly uniform interior plaquettes, O(1/N) wrap defect, Wilson winding to -I, gauge covariance, ground-state convergence to the Landau ground 1/(4 pi), continuous no-twist falsifier (differential evolution).
5. [x] Ensemble: pressures, w = 1/3, orientation average; derived H^3 induced-metric measure (divergent volume); derived Gr~(2,4) = S^2 x S^2 volume 16 pi^2 via the self-dual split; modulus instability.
6. [ ] Full suite at the boundary; stacked PR against issue #28.
7. [ ] Report; post-task refinement.

## Preregistered Routes
The obstruction is exact (symbolic cocycle + membership); the lattice is
corroborating evidence, not the proof. The two flux carriers (su(2), u(1))
are both enumerated and the minimum taken, so the energy estimate does not
depend on an unexamined case split.

## Attempts
Append-only record of attempts.

| Attempt | Approach or repair | Artifact and command | Verdict | Mechanism | Next attempt |
| --- | --- | --- | --- | --- | --- |
| 0001 | hard-coded boolean obstruction (PR #27 v1) | commuting_lifts_exist | refuted by review | no structural content | exact cocycle + kernel membership (landed) |
| 0002 | old "uniform-flux" U(1) links (PR #27 v1) | uniform_flux_lattice_spectrum | refuted by plaquette check | total U(1) flux is zero; flux must live in su(2) | su(2) Landau-gauge links (landed) |
| 0003 | 0.125-grid no-twist scan | grid test | refuted by review | not a continuous falsifier | differential-evolution best-fit residual (landed) |
| 0004 | stand-in orbit integrals | boost_orbit_measure_volume | refuted by review | measures not derived | induced-metric derivation on H^3 and S^2 x S^2 (landed) |
| 0005 | gauge-covariance test v1 | test_toron_bundle | failed as written | zeros_like inherited real dtype, silently dropping imaginary parts | complex-typed buffers (landed; the check has teeth) |

## Validation
Validation covers the actual objective, not an exit code.

- `PYTHONPATH=src .venv/bin/python -m pytest tests/test_toron_bundle.py tests/test_flux_tube_ensemble.py -q` -> 20 passed (5.8s).
- Structural gates: cocycle and commutator exact and phase-independent; kernel membership with mutation sensitivity (wrong kernel flips the verdict); plaquettes uniform to 1e-12 interior with O(1/N) wrap defect decreasing 8/16/24; Wilson holonomy winding to -I under refinement; spectrum exactly gauge-covariant (1e-8); ground converges to 1/(4 pi) with decreasing deviation; continuous twist falsifier residual > 0.05.
- Consumer replay: full suite via `scripts/validate.sh` at the boundary, recorded at push time.

## Debt Ledger
Assumptions and shortcuts introduced by this effort.

| Debt | Introduced by | Why it is real | Discharge artifact | Status |
| --- | --- | --- | --- | --- |
| one-loop matter contribution on the flux background uncomputed | campaign scope | needs a renormalization condition on the magnetic spectrum | issue #28 frontier | open frontier, recorded |
| lattice tower shape beyond the ground state (observed equal spacing ~6/(4 pi)) not identified analytically | lattice evidence | tower identification is not needed for the obstruction or the no-twist verdict | frontier: analytic magnetic spectrum on the Z2-quotient bundle | open frontier, recorded |

## Results
Verified outcomes (reproduce with the commands in Validation).

1. Exact obstruction: the cover cocycle of the declared Sec. 10 transition
   functions is (-I, +1); it lies outside the diagonal Z2 kernel, inside the
   PSU(2) x U(1) wrong-kernel mutation, and outside the trivial kernel. No
   flat connection exists with fundamental matter; the cover commutator is
   (-I,1) for all U(1) lift phases.
2. Minimal flux background: carriers su(2) (2 pi^2/(g^2 L^4)) and u(1)_Y
   (2 pi^2/(g'^2 L^4)); the su(2) representative is minimal at SM couplings
   and exceeds the one-loop gauge term by >10x. Positive, classical,
   unavoidable once fundamentals are included.
3. Lattice: the constant-curvature su(2) representative passes all
   construction checks and its spectrum ground converges to the Landau
   ground 1/(4 pi); no constant-twist spectrum fits under continuous
   optimization.
4. Ensemble: static-tube isotropic average gives w = +1/3 exactly; the
   derived H^3 orbit measure diverges (no normalizable boost-invariant
   ensemble); the derived Gr~(2,4) volume 16 pi^2 is finite but Euclidean;
   no modulus stationary point under either sign.

## Post-Task Refinement
The review cycle worked as designed: two latent defects (commutant reshape,
zero-flux lattice construction) were caught by structural checks, not by
green suites. No template change needed beyond what ~/AGENTS.md already
records.

## Done Gate
Each condition checked individually before closing.

- [x] Positive object exists and is verified (two modules, 20 targeted tests)
- [x] Debt ledger carried to the PR (two open frontiers recorded)
- [ ] Memory synchronized with landed state (this effort + P226; at push)
- [x] Post-task refinement answered

Status stays active until independent review disposes the extension PR.

## Cross-References
Issue #28 (vantasnerdan/substrate-framework); parent audit issue #26 / PR #27;
proposal P226; preprint PDF attached to issue #26 (comment 5243581613).
