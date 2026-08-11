---
description: 'Deliver 2+1D and 3+1D einbein smooth-massless-limit tutorials (MD->LaTeX->PDF)
  extending Tiziano Fulceri''s 1+1D preprint (issue #32)'
author: giuliano
created: '2026-08-11T08:05:28.863682+00:00'
updated: '2026-08-11T08:05:28.863682+00:00'
tags:
- substrate-framework
- einbein
- tiziano
category: efforts
confidence: working
status: active
---

## Goal and Success Contract
This effort delivers two pedagogical tutorials extending DOI 10.5281/zenodo.21879560 to 2+1D and 3+1D, each as the chain MD -> LaTeX -> PDF, committed to vantasnerdan/substrate-framework, independently reviewed, merged via PR, and sent to Tiziano. Complete only when both PDFs compile, every claim is referenced or derived, the review closes, and Tiziano has the artifacts.

## Accepted Baseline
Work starts from main after PR #31. Source artifact actually read: incoming/einbein_1plus1D_tutorial.pdf (md5 b1e5605cd094532b94735133b683ef4f, matches Zenodo record 21879560).

## Constraints and Invariants
Tiziano's constraints: every logical step explicit (no "obvious"); every external fact referenced with author/title/year/stable URL; audience 1st/2nd-year math-physics students; output chain MD, LaTeX, PDF per document. Style invariants from the preprint: signature (-,+,...), c0 explicit, einbein e(tau) > 0, step-numbered derivations, footnoted technical terms.

## Decomposition
Dependency-ordered steps; continue after failed attempts.

1. [x] Recall and source verification (preprint read in full).
2. [ ] Toolchain (pandoc + TeX Live) installed and smoke-tested.
3. [ ] 2+1D tutorial: MD -> LaTeX -> PDF.
4. [ ] 3+1D tutorial: MD -> LaTeX -> PDF.
5. [ ] Independent review of both documents.
6. [ ] PR, merge, delivery to Tiziano, memory synchronization.

## Attempts
Append-only; failures name mechanism and next materially different attempt.

| Attempt | Candidate or repair | Artifact and command | Verdict | Mechanism | Next attempt |
| --- | --- | --- | --- | --- | --- |

## Validation
Validation is document-level: every displayed equation either derived in-line or cited; dimensional claims (little groups, Christoffel counts, null-cone structure) checked against cited sources; LaTeX compiles clean; PDF page-count and structure inspected.

- Symbolic spot-check of key algebra (SymPy where tractable):
- Independent reviewer pass (axis/reviewer agent) before PR:
- `scripts/validate.sh` at promotion boundary only (long-running, per team convention):

## Debt Ledger
Assumptions, residuals, and narrative inconsistencies; empty at close.

| Debt | Introduced by | Why it is real | Discharge artifact | Status |
| --- | --- | --- | --- | --- |

## Results
Positive verified outcomes with reproduction commands.

## Canonicalization
PR, merged docs paths, generated PDFs, memory sync. No proposal prose into canonical memory.

## Done Gate
Artifacts exist, reviewed, merged, delivered; Tiziano acknowledged.

## Cross-References
Issue vantasnerdan/substrate-framework#32; preprint incoming/einbein_1plus1D_tutorial.pdf.

