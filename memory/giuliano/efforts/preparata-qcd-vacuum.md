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

## Validation
Per child issue: strongest practical verifier, shown sensitive by mutation;
records synchronized at push time. Report-level: build.sh byte-clean
regeneration; PDF inspected.

## Debt Ledger
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
