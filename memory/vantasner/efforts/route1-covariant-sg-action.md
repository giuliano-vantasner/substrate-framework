---
description: Deliver an importable covariant 3+1 sine-Gordon action and its Euclidean-Hessian fluctuation operator as the next Route 1 (induced-gravity) rung for issue #12
author: mlops-kelvin
created: '2026-08-10T09:36:42Z'
updated: '2026-08-10T09:36:42Z'
tags:
- substrate-framework
- effort
- route1-induced-gravity
- issue-12
category: efforts
confidence: working
status: active
---

## Goal and Success Contract
This effort delivers one importable, target-blind reusable unit: a covariant 3+1 sine-Gordon action `S = integral sqrt(-g) [ -(1/2) g^{mu nu} d_mu phi d_nu phi - V(phi) - (1/2) xi R phi^2 ]` in the framework's declared mostly-plus convention, together with the exact covariant field equation it generates and the second-variation (Euclidean-Hessian) fluctuation operator. It is complete for this rung when the constructor exists as an importable module with a pure API, the field equation is derived from the action by Euler-Lagrange rather than asserted, the second variation reproduces the fluctuation operator `D = -box_g + V''(phi) + xi R` whose endomorphism `V''(phi) + xi R` is exactly the `D_E = -nabla^2 + xi R + m^2` input already consumed by `scalar_induced_newton.scalar_heat_kernel_a2` (with `m^2 -> V''(phi_bg)`), the flat limit reproduces the accepted 3+1 sine-Gordon equation, and mutation tests show a wrong action measure and a wrong curvature-coupling sign each break a relevant check. It does NOT select a regulator, identify a cutoff, compute a Newton constant, or make any observed-gravity comparison; those remain later rungs and open campaign frontier for #12. A no-go, residual, or obstruction is attempt evidence, not completion.

## Accepted Baseline
Work starts from accepted release `v0.159.0`, framework commit `5dc6d4db` (branch `campaign/route1-covariant-sg-action` off `origin/main`, which contains the #14 harvest `a562568`). Source read at this commit: `AGENTS.md`; `.agents/skills/physics-erdos-loop/SKILL.md`; `governance/releases/current.yaml`; `src/substrate_framework/scalar_induced_newton.py` (rung-1, the operator convention `D_E=-nabla_E^2 + xi R_E + m^2`); `src/substrate_framework/einstein_scalar.py` (declared mostly-plus scalar action and stress convention); `src/substrate_framework/sine_gordon.py` (accepted normalized potential `V=1-cos phi` and 1+1 residual `phi_tt-phi_xx+sin phi`); `src/substrate_framework/dimensional_sine_gordon.py` (dimensional cosine Lagrangian/residual); `src/substrate_framework/radial_sine_gordon.py` (declared 3+1 form `u_tt = u_rr + 2 u_r/r - sin u`); `src/substrate_framework/variational.py`, `optical_geometry.py`, `exact_symbolic.py`. Chronology and memory prose are not authority; every reused fact was verified at source.

## Constraints and Invariants
Signature/convention: mostly-plus `(-,+,+,+)`, matching `einstein_scalar.py`. The kinetic term `-(1/2) g^{mu nu} d_mu phi d_nu phi` in this signature reproduces the accepted `(phi_t^2 - phi_x^2)/2` form, so the flat limit must reproduce `sine_gordon.sine_gordon_residual` (1+1) and `radial_sine_gordon`'s 3+1 form up to an overall sign fixed by the box convention (`box_g phi - V'(phi) = -(phi_tt - lap phi + sin phi)`). Permitted imports: `sympy`, and framework `exact_symbolic`, `sine_gordon` (accepted potential). No new fitted constant, no Newton coupling, no cutoff, no regulator, no comparator may enter this rung (target-blindness is a tested invariant). Reusable geometry (`sqrt(-g)`, inverse metric, Laplace-Beltrami, Ricci scalar) is implemented once in the new module with a pure API and tests; imports must not execute computation. Do not edit accepted claims, `docs/generated/`, or any earlier campaign. Write boundary: `src/substrate_framework/covariant_sine_gordon_action.py`, its `__init__` exports, `tests/test_covariant_sine_gordon_action.py`, and this effort record. Author-does-not-merge (#23): open a PR naming #12; a distinct reviewer/owner harvests and merges.

## Decomposition
1. [x] Recall and source verification (authority, rung-1 convention, accepted SG EOM, mostly-plus convention).
2. [x] Candidate and selection-criteria preregistration (below).
3. [x] Importable implementation of the covariant action, EL field equation, and fluctuation operator (+ reusable exact geometry primitives).
4. [x] Verifier and sensitivity audit (flat-limit reproduction; FLRW covariant EOM; wrong-measure and wrong-xi-sign mutations; rung-1 bridge; target-blindness; and — added in the PR #25 review round — an independent linearized-second-variation oracle for the Hessian plus an exact/Lorentzian metric-contract check) — 18/18 targeted tests pass.
5. [x] Framework-fit and downstream replay. `scripts/validate.sh` (bash; it auto-selects `.venv/bin/python`) aborts at its memory-version parity step — the installed `memory` CLI has no `--version` option (exit 2, environmental, unrelated to this change) — so the script itself never reaches its own pytest step. Every other `validate.sh` gate was therefore run individually and all pass: `validate_repository.py` WORKFLOW VALID (202 claims / 202 accepted / 0 proposals; migration queue 218 units, 0 pending); `render_docs.py --check`; `render_memory.py --check`; the numpy/scipy/sympy/yaml import; `memory validate memory/` (All 908 files valid); `validate_skill.py` (Skill is valid); `compileall` (src + tools/agent-memory/src); full suite `PYTHONPATH=src .venv/bin/python -m pytest -q` = 2020 passed; `git diff --check` clean.
6. [ ] Harvest PR to #12 (issue-first, non-self-merge); reviewer updates #12 with merged/refactor/history disposition once merged.

## Candidate Preregistration and Selection Criteria
Selection criteria frozen before comparison: (1) the EOM and Hessian are *derived from the action* not asserted; (2) verifier sensitivity — the wrong-measure and wrong-curvature-sign mutations must each be able to break a check on a background where the connection term and R are nonzero; (3) fewest new assumptions and no new fitted parameter; (4) correct dimensions/signs/limits and exact reproduction of the accepted SG EOM; (5) reusable importable geometry.

- Candidate A (SELECTED): general symbolic-metric constructor. The covariant field equation is obtained from the `sqrt(-g)` action by `sympy.calculus.euler.euler_equations` and is proven equal to an independently computed `sqrt(-g)*(box_g phi - V'(phi) - xi R phi)` using module-level Laplace-Beltrami and Ricci-scalar primitives. Verified on flat (R=0) and FLRW (R!=0) backgrounds; mutations flip the measure and the xi-sign.
- Candidate B (REJECTED): assert the fluctuation operator `-box + V'' + xi R` directly, without a measure. Rejected against criteria (1) and (2): with no action measure present there is nothing for the "wrong action measure fails" test to mutate, so B cannot satisfy #12's explicit requirement. A dominates on verifier sensitivity and framework fit; B retained only as historical rationale.

## Attempts
Attempts are append-only and individually reproducible; each row names the diagnosed mechanism and the next materially different attempt.

| Attempt | Candidate or repair | Artifact and command | Verdict | Mechanism | Next attempt |
| --- | --- | --- | --- | --- | --- |
| 0001 | A | src/substrate_framework/covariant_sine_gordon_action.py + tests/test_covariant_sine_gordon_action.py | pass | euler_equations EL == sqrt(-g)*(box-V'-xiR) on flat and FLRW; both mutations break the identity; rung-1 bridge exact | none — rung deliverable met; #12 frontier advances to the fluctuation-determinant/regulator rung |
| 0002 | PR #25 review repair (Dan harvest review, CHANGES_REQUESTED) | same module + tests | pass | F1: the Hessian endomorphism was asserted then compared against its own formula (circular); added an independent oracle that linearizes the action-derived field equation at `phi_bg + eps*eta`, takes the eps-linear term, and proves it equals `-(D eta)` — with 4 sign/normalization mutations. F2: `_metric_matrix` accepted inexact (`diag(-1.0,..)`) and Euclidean (`eye(4)`) metrics; now enforces exact-only entries + a mostly-plus Lorentzian signature for constant metrics. F3: reconciled this record's validation provenance to the actual `validate.sh` environmental abort + individually-run gates. 18/18 targeted, 2020 full suite, all boundary gates green. | none — F1/F2/F3 closed; awaiting Dan re-review (non-self-merge, gov #23) |

## Validation
Validation covers the actual objective, verifier sensitivity, limits, conventions, and dependency replay — not merely an exit code.

- Targeted oracle (exact SymPy): `PYTHONPATH=src .venv/bin/python -m pytest tests/test_covariant_sine_gordon_action.py -q` (18 passed) — flat-limit reproduction, FLRW covariant EOM, second-variation endomorphism, rung-1 bridge, the independent linearized-Hessian oracle with sign/normalization mutations (PR #25 F1), and the exact/Lorentzian metric-contract check (PR #25 F2).
- Mutation/counterexample: wrong measure (`sqrt(-g) -> 1`) drops the FLRW connection term; wrong curvature-coupling sign (`xi -> -xi`) flips the R-term; both required to break the equality check.
- Dependency replay: `scripts/validate.sh` (bash) aborts at its memory-version parity step on this host — the installed `memory` CLI lacks `--version` (environmental) — so it cannot itself reach the suite. The full suite and every other gate were therefore run individually and all pass: `PYTHONPATH=src .venv/bin/python -m pytest -q` (2020 passed), `validate_repository.py` (WORKFLOW VALID, 202 claims), `render_docs.py`/`render_memory.py --check`, `memory validate memory/` (908 valid), `validate_skill.py`, `compileall`; then `git diff --check` (separate invocation, clean).
- Target-blindness: assert the action density and field equation carry no Newton coupling, cutoff, regulator, or comparator symbol.

## Debt Ledger
Every new assumption, import, parameter, residual, broken consumer, or narrative inconsistency is recorded here and discharged; this table must be empty at close.

| Debt | Introduced by | Why it is real | Discharge artifact | Status |
| --- | --- | --- | --- | --- |
| (none yet) |  |  |  |  |

## Results
Delivered `src/substrate_framework/covariant_sine_gordon_action.py` (covariant action, EL-verified field equation `box_g phi - V'(phi) - xi R phi`, fluctuation endomorphism `V''(phi_bg) + xi R`, and reusable exact geometry: sqrt(-g), inverse metric, Christoffel, Ricci tensor/scalar, Laplace-Beltrami) plus `tests/test_covariant_sine_gordon_action.py` (18 exact tests — the original 15 plus 3 added in the PR #25 review round: an independent linearized-Hessian oracle, its sign/normalization mutations, and an exact/Lorentzian metric-contract check) and package exports. The second variation is proven identical to rung-1's `D_E = -nabla^2 + xi R + m^2` input with `m^2 -> V''(phi_bg)` (= m^2 at the vacuum), and — after the review — is independently verified as the linearization of the action-derived field equation rather than asserted. Reproduce: `PYTHONPATH=src .venv/bin/python -m pytest tests/test_covariant_sine_gordon_action.py -q` (18 passed) and full `PYTHONPATH=src .venv/bin/python -m pytest -q` (2020 passed). No claim promoted; #12 stays open with the regulator/effective-action rung as the next decisive action.

## Canonicalization
No claim promotion in this rung (reusable-primitive harvest, mirroring #14 "Claims promoted: none"). Extracted API: `src/substrate_framework/covariant_sine_gordon_action.py` + `__init__` exports + tests. No release-manifest or `governance/claims.yaml` change. #12 remains open; its "next decisive action" advances to the fluctuation-determinant / regulator rung after this lands.

## Done Gate
This is a bounded harvest checkpoint, not the #12 objective. The rung is done when steps 3-6 are checked and the debt ledger is empty; the #12 induced-gravity objective stays active with the regulator/effective-action rung as the next frontier.

## Cross-References
Issue: vantasnerdan/substrate-framework#12 (Route 1 campaign). Governance: `#23` (issue-first, non-self-merge). Rung-1: `scalar_induced_newton.py` (PR #13 -> harvest #14 `a562568`). Prior fork adjudication: issue #9 (closed, Route 1 selected). Accepted convention source: `einstein_scalar.py`; accepted SG EOM: `sine_gordon.py`, `radial_sine_gordon.py`.
