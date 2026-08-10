---
description: 'Oracle-backed verification of twisted-torus one-loop vacuum energetics (issue #26): Epstein zeta values, corrected toronic DeltaV sign, preprint algebra checks'
author: giuliano
created: '2026-08-10T15:30:00+00:00'
updated: '2026-08-10T15:30:00+00:00'
tags:
- effort
- toronic-casimir
- issue-26
category: efforts
confidence: working
status: active
---

## Goal and Success Contract
This effort delivers a canonical, tested module `twisted_casimir` computing
zeta-regularized one-loop vacuum-energy densities for twisted spectra on
T^2 x R^2, plus the adjudicated referee verdict on the toronic-condensate
preprint's Sec. 5-7 algebra. Complete only when: two independent oracle routes
agree on the energy difference; every preprint claim under test is either
reproduced or refuted by an explicit oracle with sensitivity evidence; targeted
tests pass; `scripts/validate.sh` passes once at the final boundary; the PR is
open against issue #26. No claim promotion is requested.

## Baseline
Existing state, verified at source. No Epstein/Casimir primitive exists in
`src/substrate_framework/` (grepped: only representation-theory Casimir
operators). Reusable: `verification.py` CheckLedger, `numerics.py`.
Release v0.159.0 is the accepted baseline. Ad-hoc pure-Python numerics
(outside the workflow, 2026-08-10) indicated DeltaV = +5G/(2L^4) > 0 vs the
preprint's -5piG/(8L^4); that result is unverified intuition until the oracles
here reproduce it. Stack: .venv with sympy 1.14, scipy 1.18, numpy 2.5.2,
mpmath 1.3.0. Lean unavailable; no formal claim is registered.

## Constraints and Invariants
Write surfaces: `src/substrate_framework/twisted_casimir.py`,
`tests/test_twisted_casimir.py`, `src/substrate_framework/__init__.py`,
`memory/giuliano/`. No edits to accepted claims, campaigns, generated docs.
Branch `research/toronic-casimir-verification`. Issue-first per repo #23.

## Decomposition
Dependency-ordered steps for the effort.

1. [x] Recall and source verification (preflight, governance, module search).
2. [x] Route preregistration (see below).
3. [x] Canonical module + proposal record (P225).
4. [x] Two-route verification with mutation and refinement evidence (29 tests green).
5. [x] Preprint algebra checks (SymPy): Wilson commutator, centralizer, Sec. 7 coefficient matching.
6. [x] Scope extension per L. Gamberale 2026-08-10: fermion-sector question resolved structurally (no flat connection with fundamentals; magnetic spectrum on the minimal flux connection; classical flux energy 2 pi^2/(g'^2 L^4) dominates); Minkowski tube-ensemble analysis landed (`flux_tube_ensemble`: w = 1/3, boost-measure obstruction, modulus instability).
7. [ ] Targeted tests green; one full `scripts/validate.sh` at the final boundary (running as background process `sf-validate`).
8. [ ] PR against issue #26; report back to Luca/Dan; send email addendum only with Luca's consent.
9. [ ] Post-task refinement.

## Preregistered Routes
Two independent computational routes, frozen before comparison. Route 1
(functional equation): E2'( -1; alpha) from the symmetric functional equation
plus special-value identities (E2 = 4 zeta beta at alpha=0; beta'(-1) = 2G/pi).
Route 2 (direct regulated mode sums): smoothed-cutoff lattice sums of the
lambda ln lambda spectral moment, regulator-refined. Selection criteria:
exactness, independence of regularization artifacts, convergence control. The
verdict is accepted only if both routes agree within refinement residuals.

## Attempts
Append-only record of attempts.

| Attempt | Approach or repair | Artifact and command | Verdict | Mechanism | Next attempt |
| --- | --- | --- | --- | --- | --- |
| 0001 | Ad-hoc pure-Python sums (outside workflow) | chat session 2026-08-10 | numeric indication only | no oracle governance; not a deliverable | 0002 canonical module |
| 0002 | Canonical two-route module + tests | this branch | landed |  |  |
| 0003 | Naive commutant index map | matrix_commutant_basis | wrong rank (3 vs 1) | hand-rolled vec map | Kronecker formulation (landed) |
| 0004 | Candidate fundamental twists (1/4,1/2) | secular truncation | refuted by lattice spectra | bundle admits no flat frame | obstruction theorem + uniform-flux lattice (landed) |
| 0005 | Fermion DeltaV via candidate twists | withdrawn | premise false | flat fundamental bundle does not exist | frontier: flux-background one-loop with renormalization condition |

## Validation
Validation covers the actual objective, not an exit code.

- `PYTHONPATH=src .venv/bin/python -m pytest tests/test_twisted_casimir.py tests/test_flux_tube_ensemble.py -q` -> 29 passed (5.8s).
- `PYTHONPATH=src .venv/bin/python scripts/validate_repository.py` -> WORKFLOW VALID: 202 claims, 202 accepted, 1 proposals.
- Sensitivity: twist mutation changes DeltaV as both routes predict; the preprint coefficient -5piG/8 fails by O(1) in both routes; adjoint lattice validates the lattice method (refinement 12/18/24, max low-mode deviation < 0.02 and decreasing); fundamental spectrum fits no constant-twist candidate (best residual > 0.05) and is stable under refinement.
- Consumer replay: full suite via `scripts/validate.sh` (background `sf-validate`), recorded at PR time.

## Debt Ledger
Assumptions and shortcuts introduced by this effort.

| Debt | Introduced by | Why it is real | Discharge artifact | Status |
| --- | --- | --- | --- | --- |
| beta'(-1) = 2G/pi is numeric evidence, not symbolic proof | route 1 closed form | no symbolic oracle available for the derivative identity | cross-check vs route 2 which needs no special-value input | open |

## Results
Verified outcomes (reproduce with the commands in Validation).

1. E2(-1; alpha) = 0 identically (preprint Eq. 47 refuted); verified to 1e-30
   via the functional-equation route and the 4 zeta(s) beta(s) factorization.
2. Corrected gauge-sector one-loop difference: DeltaV = +5G/(2 L^4) > 0
   (route A closed form; route B regulated sums converge to D = -5G/(2 pi);
   agreement 2e-4 at regulator 900 and improving). The toronic sector is
   energetically disfavored; the periodic vacuum is preferred. The preprint's
   -5piG/8 is an artifact of the false Eq. (47) and the dropped
   lambda ln lambda term.
3. Sec. 7 gap ansatz yields lambda_eff = -c g^4/4 (negative; unbounded
   below), not the asserted +c g^4/8 (exact SymPy matching).
4. Stabilizer of {i sigma3, i sigma1} is Z2, not U(1)_em (exact commutant);
   the coset in Eq. (66) is a gauge orbit.
5. No flat connection exists on the Sec. 10 bundle with fundamental matter
   (exact: cover commutator (-I,1) not in the diagonal Z2 kernel); minimal
   connection carries quantized flux with classical density
   2 pi^2/(g'^2 L^4) (~155/L^4 at g' = 0.357), dwarfing one-loop terms.
   Lattice confirms the fundamental spectrum is magnetic, not twisted-flat.
6. Minkowski tube ensemble: w = +1/3 exactly (not a Lorentz vacuum); no
   normalizable boost-invariant measure (divergent rapidity volume; compact
   Euclidean Gr(2,4) contrast); no stationary point in L under either sign.

## Post-Task Refinement
Pending.

## Done Gate
Each condition checked individually before closing.

- [ ] Positive object exists and is verified (not just attempted)
- [ ] Debt ledger empty or explicitly carried to the PR
- [ ] Memory synchronized with landed state
- [ ] Post-task refinement answered

## Cross-References
Issue #26 (vantasnerdan/substrate-framework); referee report artifact at
~/downloads/prl-ref-2026-08-10/referee-report.md; email thread in Waiting
(Luca, 2026-08-10).
