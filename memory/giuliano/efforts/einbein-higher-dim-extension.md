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
| 0001 | 2+1D tutorial draft with hand-written null-rotation generator M | docs/tutorials/einbein_2plus1D/einbein_2plus1D_tutorial.md | Failed (caught pre-review) | Hand-written 3x3 matrix did not annihilate k0; M k0 = (0,0,-kappa) != 0. Wrong generator guessed instead of derived. | 0002: derive M = K2 + J from the boost/rotation basis and verify e^{tM} k0 = k0 symbolically |
| 0002 | Corrected generator M = K2 + J; SymPy check test_eq071 | tests/test_einbein_2plus1d_tutorial.py | Passed | Generator derived from basis, not guessed; exponential verified with sp.exp | - |
| 0003 | 3+1D Christoffel appendix via generator script | docs/tutorials/einbein_3plus1D/generate_christoffel_block.py | Failed on first output (self-caught) | Parenthesization keyed on "+" only; "2 d g - d g" brackets (rho = nu, lam != rho) contain " - " and escaped unwrapped, corrupting the sum scoping | 0004: wrap on " + " or " - "; block-regeneration diff test added |
| 0004 | Regenerated block + test_appendixA_document_block_matches_generator | tests/test_einbein_3plus1d_tutorial.py | Passed | MD block is byte-identical to generator output; 40/40 components match the general formula numerically | - |
| 0005 | Eq. (12) reparametrization justification prose (both docs) | docs/tutorials/einbein_*/: measure/velocity power counting | Failed (caught by 3+1D independent review) | Prose claimed d tau/e invariant (false: picks up f-dot^2) and 1/f-dot from two velocities (correct: 1/f-dot^2) | Fixed in both docs: velocities 1/f-dot^2, measure f-dot, net 1/f-dot cancelled by 1/e -> f-dot/e; invariant combination is e d tau |
| 0006 | Constraint-counting sentences in Sec. 12.1 (both docs) | same | Failed (3+1D review; 2+1D fixed by analogy) | Massive constraint fixes the scale (inhomogeneous), not a ratio; the null-case counting was wrongly imported | Corrected: constraint fixes scale; ratios are free data |
| 0007 | PR #39 pushed after failing test run (twice) | tests/test_einbein_3plus1d_tutorial.py flat-solution check | Failed (self-caught post-push) | Vacuous np.gradient assertion, then marginally tight tolerance (roundoff eps/h^2 > atol); committed on a red run both times | Amended twice with verified green (4 consecutive full runs); rule retained: never commit after a failing run |
| 0008 | 2+1D files accidentally committed to main inside memory commit 60d701ed | main history | Failed (self-caught) | stash pop restored the index; git add of one file + commit swept staged tutorial files | Removal commit on main; rule retained: no cross-branch stash; commit WIP on feature branches |
| 0009 | PR #38/#39 first-submission prose: universal no-internal-state/two-state claims, 1+1 sign-only shell count, covariant p_mu arrays under Lorentz matrices, missing Lambda=0, Weyl-as-root and vDVZ-as-shadow wording | docs/tutorials/einbein_*/*.md | Failed (vantasnerdan requested changes on both PRs, 2026-08-11) | Headline prose overclaimed beyond the declared sectors (trivial-translation for 2+1D massless; parity-complete nonzero-helicity for 3+1D); canonical covector convention mixed with contravariant matrix action; cross-sector analogies stated as causal derivations; vacuum local flatness stated without Lambda=0 | 0010: narrow correction commits, regenerated TeX/PDF, same scoped suites |
| 0010 | Correction commits 66e67282 (2+1D) and 31b8205e (3+1D) | same, plus rebuilt .tex/.pdf | Passed | All eight requested corrections applied point-by-point; MD -> pandoc -> xelatex chain byte-clean; suites re-green on the pushed trees (29/29 2+1D, 25/25 3+1D, validate 6/6) | Awaiting reviewer re-review and merge; delivery to Tiziano only after merge |

## Validation
Validation is document-level: every displayed equation either derived in-line or cited; dimensional claims (little groups, Christoffel counts, null-cone structure) checked against cited sources; LaTeX compiles clean; PDF page-count and structure inspected.

- Symbolic spot-check of key algebra (SymPy): done — einbein chain, square-root recovery, Hamiltonian (general 3x3 and 4x4 metric), all 18 (2+1D) Christoffels symbolic + all 40 (3+1D) numeric plus byte-identical generator block, null-rotation exponentials (sp.exp), Weyl and reparametrization invariance, exact induced metric diag(1, sinh^2 a).
- Independent reviewer passes: two reviewer agents recomputed independently (own derivations, own parser for Appendix A). Verdicts: approve-with-fixes (both). All findings applied and re-verified.
- Targeted suites during implementation: `pytest tests/test_einbein_2plus1d_tutorial.py` 29/29 green (two consecutive runs on the pushed tree); `pytest tests/test_einbein_3plus1d_tutorial.py` 25/25 green (four consecutive runs on the pushed tree).
- `scripts/validate.sh` at promotion boundary only (long-running, per team convention): deferred to merge time per Dan (pre-merge runs are the merger's responsibility; run in background if needed).
- `git diff --check`: clean on every commit.

## Debt Ledger
Assumptions, residuals, and narrative inconsistencies; empty at close.

| Debt | Introduced by | Why it is real | Discharge artifact | Status |
| --- | --- | --- | --- | --- |

## Results
Positive verified outcomes with reproduction commands.

- 2+1D tutorial merged via PR #38 (merge commit 5071e14f6ded5ef072a4d03f2a9446250a8a7f68), closing issue #34. Reproduce: `pytest tests/test_einbein_2plus1d_tutorial.py` (29 passed); `docs/tutorials/build.sh docs/tutorials/einbein_2plus1D` regenerates MD -> TeX -> PDF.
- 3+1D tutorial merged via PR #39 (merge commit 6b836fa52f543fc463aa57df01eaa4b17731d000), closing issue #35. Reproduce: `pytest tests/test_einbein_3plus1d_tutorial.py` (25 passed); `docs/tutorials/build.sh docs/tutorials/einbein_3plus1D`.
- Dan's final corrected-head reviews approved both PRs; harvest dispositions recorded on issues #34/#35; tracker #32 closed 2026-08-11 with all three child issues closed.
- Delivered to Tiziano by email 2026-08-11 (Message-ID 8482ad9e-17fc-3699-d3c5-e325a04ab075@vantasner.io): work summary, repo links (no attachments), invite notice (vantasner-T invited by Dan), workflow onboarding, Zwiebach DOI erratum.

## Canonicalization
PR, merged docs paths, generated PDFs, memory sync. No proposal prose into canonical memory.

- Merged docs: docs/tutorials/einbein_2plus1D/ (MD/TeX/PDF), docs/tutorials/einbein_3plus1D/ (MD/TeX/PDF + generate_christoffel_block.py); pipeline docs/tutorials/build.sh + README.md (PR #36, 4a837128); effort-contract rules (PR #37, 62baea91).
- Claim promotion: none (per reviewer disposition — tutorial/test provenance only, no governance/claims.yaml changes).
- Memory sync: session-state.md updated 2026-08-11; base + repo memory trees validate clean.

## Done Gate
Artifacts exist, reviewed, merged, delivered; Tiziano acknowledged.

- [x] Artifacts exist and are machine-checked (29 + 25 suites green on merged heads)
- [x] Reviewed (two independent passes + owner final review) and merged (PRs #38/#39)
- [x] Delivered to Tiziano (2026-08-11, with repo invite and onboarding)
- [ ] Tiziano acknowledged — awaiting his reply/invite acceptance

## Cross-References
Issue vantasnerdan/substrate-framework#32; preprint incoming/einbein_1plus1D_tutorial.pdf.

