---
description: 'Machine-checked reproduction of Preparata essential-instability QCD-vacuum program (two-loop V(Lambda/gB), stability, improved background) with LaTeX+PDF delivery to Luca'
author: giuliano
created: '2026-08-11T15:20:00.000000+00:00'
updated: '2026-08-11T15:20:00.000000+00:00'
tags:
- effort
category: efforts
confidence: working
status: active
---

## Goal and Success Contract
This effort delivers a machine-checked reproduction of Preparata's papers on
the essential instability of the perturbative Yang-Mills/QCD vacuum:
one-loop and two-loop effective potentials with V as a function of the
source's variable (Lambda/gB, convention fixed from the primary sources), a
fluctuation-stability verdict, the color/transverse decomposition of the
energy density, an improved classical background with requantization, and a
LaTeX report + PDF delivered to luca.gamberale@gmail.com. Complete only when
every quantitative claim in the report is backed by a merged SymPy/SciPy
oracle (substrate-framework issues #44-#50), the report builds through
docs/tutorials/build.sh, and the debt ledger is empty.

## Baseline
- Request: Luca email 2026-08-11 (filed Processed UID 67), ack sent
  (Message-ID e948ee0d-82a0-f296-cc25-ab6f3137ede7@vantasner.io).
- Central paper: G. Preparata, Nuovo Cim. A 96 (1986) 366, DOI
  10.1007/BF02833896. Luca co-authored the later Milan program
  (Gamberale-Preparata-Xue 1991/1992/1994).
- Literature extraction delegated (agent PreparataLit, 2026-08-11).
- Method: quantitative-verification skill gates; einbein tutorials show the
  MD -> TeX -> PDF + check-suite pattern that this report reuses.

## Constraints and Invariants
- No hand-rolled math: oracles first, report cites them; delivery after
  merge (Dan, 2026-08-11).
- Private repo posture; canonical coordination in issue #44.
- Conventions must be declared once and typed (metric, gauge, Lambda scheme,
  gB vs B) before any coefficient comparison.

## Decomposition
Dependency-ordered steps; continue after failed attempts.

1. [x] Recall and source location (INSPIRE scan; extraction agent running).
2. [ ] Approach preregistration per child issue (candidates named in issue bodies).
3. [ ] #45 one-loop Savvidy (spectrum, mode sums, V(B), minimum).
4. [ ] #46 two-loop V(Lambda/gB).
5. [ ] #47 stability (Nielsen-Olesen mode, Im V).
6. [ ] #48 color/transverse decomposition.
7. [ ] #49 improved classical background + requantization.
8. [ ] #50 report LaTeX/PDF; email to Luca.

## Attempts
Append-only; failures name mechanism and next materially different attempt.

| Attempt | Approach or repair | Artifact and command | Verdict | Mechanism | Next attempt |
| --- | --- | --- | --- | --- | --- |
| 0001 | One-loop Savvidy: three routes (cutoff proper time, Landau mode sum, operator zeta) | src/substrate_framework/chromomagnetic_background.py, tests/test_chromomagnetic_background.py, PR #51; pytest 21 passed | Passed after repairs | First-pass mode sum had wrong dof counting (zeta per-charge vs complex-field normalization factor 2, caught by cross-route disagreement); MS-bar constant extraction initially scheme-confused (fixed IR mass makes V analytic in gB — ln gB only forms when m2 tracks gB); final: C = 11/(48 pi^2) pinned 1e-10, Im V = (gB)^2/8pi two routes, Savvidy minimum + V_min match literature exactly | #46 |
| 0002 | Two-loop T=0 potential from Bordag-Skalozub defining sums | src/substrate_framework/chromomagnetic_two_loop.py, tests/test_chromomagnetic_two_loop.py, PR #52; pytest 11 passed | Passed | B2 tadpole exact via zeta: G(1)=0 cancellation, B2 = -b(ln2 - i pi)/(16 pi^2); printed eq.(57) two-loop term fails against its own definitions: derived 3g^2 b^2(ln^2 2 - pi^2)/(512 pi^4) vs printed g^2 ln^2 2 b^2/(128 pi^4) (F3); 98 vs 88 exponent typo (F1); Im 8 pi^2 vs 8 pi (F2) | #47, #48, then report #50 |
| 0003 | Sector decomposition + stability verdict | chromomagnetic_sectors.py, PR #53; 10 tests | Passed | Each transverse spin sector carries 11/6 (whole log transverse-paramagnetic); longitudinal (-1/3) cancels ghost (+1/3); SU(3) roots (1,1/2,1/2), log coefficient 3C/2; Im V two-loop -3g^2 b^2 ln2/(256 pi^3); verdict: unstable, ring resummation insufficient at two loops | #49 |
| 0004 | Spaghetti (flux-tube lattice) improved background | spaghetti_vacuum.py, PR #54; 8 tests | Passed after repair | First depth-ratio formula had exponent 24 pi^2/(11 g^2 beta); the (gH_min)^2 square doubles it to 48 — caught by the stationarity test. beta from direct quadrature of the periodic condensate density: square 1.180340, triangular 1.159595, triangular optimal. Review eq.(152) nome convention mismatch documented as frontier | #50 report |
| 0005 | Luca-facing report (Italian, MD->TeX->PDF) + RG-improved V(b/Lambda^2) | docs/reports/preparata_qcd_vacuum/, rg_improved_potential in chromomagnetic_two_loop.py, PR #55 (+3 tests on PR #52, 13 total) | Built, pending merges | Pipeline byte-clean; one-loop RG minimum at x = b/Lambda^2 = 1 exactly; two-loop x^2/ln x coefficients exact (printed vs derived) | Delivery email after merges |

## Validation
Per child issue: strongest practical verifier, shown sensitive by mutation;
records synchronized at push time. Report-level: build.sh byte-clean
regeneration; PDF inspected.

## Debt Ledger
Assumptions, residuals, and narrative inconsistencies; empty at close.

| Debt | Introduced by | Why it is real | Discharge artifact | Status |
| --- | --- | --- | --- | --- |

## Results
Positive verified outcomes with reproduction commands.

## Post-Task Refinement
Answer at close.

## Done Gate
- [ ] Positive object exists and is verified (not just attempted)
- [ ] Debt ledger empty
- [ ] Memory synchronized with landed state
- [ ] Post-task refinement answered

## Cross-References
Issues vantasnerdan/substrate-framework#44 (tracker), #45-#50; Luca thread
("Physical Review Letters referral", Processed UID 67); PreparataLit
extraction report (pending).
