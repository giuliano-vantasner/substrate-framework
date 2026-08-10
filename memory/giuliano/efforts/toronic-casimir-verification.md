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
4. [x] Two-route verification with mutation and refinement evidence.
5. [x] Preprint algebra checks (SymPy): Wilson commutator, centralizer, Sec. 7 coefficient matching.
6. [x] Harvest review 2026-08-10 (PR #27): extension scope (fundamental-bundle obstruction, flux lattice, tube ensemble) moved to its own issue-first effort; this effort narrowed to the audit core.
7. [x] Review fixes: entrywise commutant rewrite (+ nilpotent counterexample test), Eq. (46)/(47) citations, scheme-independence narrowed to the twist difference with periodic-vacuum baseline, durable PDF provenance, beta'(-1) debt reconciled.
8. [ ] Targeted tests green (22 passed); one full `scripts/validate.sh` re-run at the final boundary; push and reply on PR #27.
9. [ ] Report back to Luca/Dan; send email addendum only with Luca's consent.
10. [ ] Post-task refinement.

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
| 0003 | Naive commutant index map | matrix_commutant_basis | wrong rank (3 vs 1) | hand-rolled vec map | Kronecker formulation |
| 0004 | Kronecker vec formulation | matrix_commutant_basis | wrong for generic input | column-major vec reshaped row-major (found in harvest review; nilpotent counterexample) | entrywise linear-system formulation (landed) |
| 0005 | Extension scope inside this PR | flux_tube_ensemble, obstruction/flux helpers | split per harvest review | out of issue #26's predeclared scope | new issue-first extension effort |
| 0006 | Candidate fundamental twists (1/4,1/2); fermion DeltaV via flat twists | extension effort | withdrawn | premise false (no flat fundamental bundle) | carried to extension effort frontier |

## Validation
Validation covers the actual objective, not an exit code.

- `PYTHONPATH=src .venv/bin/python -m pytest tests/test_twisted_casimir.py -q` -> 22 passed (4.3s) after the review split.
- `PYTHONPATH=src .venv/bin/python scripts/validate_repository.py` -> WORKFLOW VALID: 202 claims, 202 accepted, 1 proposals.
- Sensitivity: twist mutation changes DeltaV as both routes predict; the preprint coefficient -5piG/8 fails by O(1) in both routes; adjoint lattice validates the lattice method (refinement 12/18/24, max low-mode deviation < 0.02 and decreasing); nilpotent counterexample verifies the generic commutant.
- Consumer replay: full suite via `scripts/validate.sh` (background `sf-validate`) at the final boundary: 2031 passed pre-split; re-run post-split recorded at push time.

## Debt Ledger
Assumptions and shortcuts introduced by this effort.

| Debt | Introduced by | Why it is real | Discharge artifact | Status |
| --- | --- | --- | --- | --- |
| beta'(-1) = 2G/pi is numeric evidence, not symbolic proof | route 1 closed form | no symbolic oracle available for the derivative identity | route 2 needs no special-value input and agrees with route 1 under refinement | discharged for the verdict by the cross-route test; a symbolic proof of the identity itself remains open mathematical frontier (non-blocking, out of campaign scope) |

## Results
Verified outcomes (reproduce with the commands in Validation).

1. E2(-1; alpha) = 0 identically (preprint Eq. 46 refuted; Eq. 47 defines
   S(alpha)); verified to 1e-30 via the functional-equation route and the
   4 zeta(s) beta(s) factorization.
2. Corrected gauge-sector one-loop difference: DeltaV = +5G/(2 L^4) > 0
   (route A closed form; route B regulated sums converge to D = -5G/(2 pi);
   agreement 2e-4 at regulator 900 and improving). The toronic sector is
   energetically disfavored; the periodic vacuum is preferred. The preprint's
   -5piG/8 (Eq. 63) is an artifact of the false Eq. (46) and the dropped
   lambda ln lambda term. The asserted quantity is the twist difference with
   the periodic vacuum as subtraction baseline; an alpha-independent local
   counterterm can shift any absolute density by C/L^4.
3. Sec. 7 gap ansatz yields lambda_eff = -c g^4/4 (negative; unbounded
   below), not the asserted Eq. (83) +c g^4/8 (exact SymPy matching).
4. Stabilizer of {i sigma3, i sigma1} is Z2, not U(1)_em (exact entrywise
   commutant, incl. nilpotent counterexample); the coset in Eq. (66) is a
   gauge orbit.
(Items on the fundamental-bundle obstruction, flux energy, and the Minkowski
tube ensemble moved to the extension effort per the 2026-08-10 harvest
review.)

## Post-Task Refinement
The task exposed one process defect and one environment friction.

1. Defect: the referee verdict was first delivered from ad-hoc pure-Python
   numerics outside the substrate workflow. Corrected in place: ~/AGENTS.md
   Team-operations section now forbids hand-rolled math and requires
   SymPy/SciPy/Lean-backed, issue+PR-recorded verification before any
   quantitative answer is delivered (Dan directive 2026-08-10).
2. Friction: system python3 has no pip/numpy; the repo .venv has the full
   stack. Recorded in long-term memory; no template change needed.

## Done Gate
Each condition checked individually before closing.

- [x] Positive object exists and is verified (narrowed core module + 22 targeted tests; full suite green pre-split 2031 passed, post-split re-run pending)
- [x] Debt ledger reconciled (beta'(-1) discharged for the verdict by cross-route independence; symbolic identity noted as out-of-scope frontier)
- [x] Memory synchronized with landed state (P225 narrowed to audit scope; extension carried to its own effort)
- [x] Post-task refinement answered

Status stays active until independent review disposes PR #27 (no self-merge).

## Cross-References
Issue #26 (vantasnerdan/substrate-framework); the preprint PDF is durably
attached to issue #26 (comment 5243581613); referee report draft emailed
2026-08-10, thread in Waiting (Luca).
