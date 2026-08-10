---
description: 'P225: oracle-backed referee verification of the toronic-condensate preprint one-loop energetics, flat-connection obstruction, and flux-tube ensemble analysis (issue #26)'
author: giuliano
created: '2026-08-10T16:05:00+00:00'
updated: '2026-08-10T16:05:00+00:00'
tags:
- substrate-framework
- campaign-proposal
- toronic-casimir
category: proposals
confidence: working
status: active
---

## Question and Positive Deliverable
Does the toronic-condensate preprint's one-loop vacuum-energy computation
survive oracle verification, and can the single-tube T^2 x R x R structure be
extended to a Lorentz-invariant flux-tube vacuum in Minkowski space? The
deliverable is the canonical two-route verification module
`twisted_casimir`, the ensemble module `flux_tube_ensemble`, focused tests,
and this adjudicated record. The verdicts (negative for the preprint's
central claims) are verified results of the audit, not the campaign's
premise; the positive objects are the reusable verified modules.

## Base Release and Provenance
Accepted release v0.159.0, baseline commit 5dc6d4db (main). Modules read:
`verification.py`, `su2_doublets.py` (generators reused), `wilson_loops.py`
(convention reference). Preprint source: PDF received 2026-08-10 (L.
Gamberale); durable copy attached to issue #26 (comment 5243581613).

## Invariants, Conventions, and Allowed Imports
No edits to accepted claims, campaigns, generated docs, or migration queues.
Conventions: T_a = sigma_a/2, square torus side L, twists in R^2/Z^2, Tr ln
one-loop measure. Allowed imports: sympy/mpmath/numpy/scipy stack in .venv;
the preprint's own numbered equations as the object under test.

## Candidate Preregistration
Two computational routes, frozen before comparison. Route selection was about
oracle independence, not about the physics verdict.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Functional-equation route: E2'( -1; alpha) from the symmetric FE and special-value identities | Epstein FE; beta'(-1)=2G/pi as numeric evidence | none | exact closed forms | agreement with B within refinement residual |
| B | Direct Gaussian-regulated lambda ln lambda mode sums | translational invariance of the regulator | regulator Lambda | converges to A | refinement series 100/400/900 |

## Selection Criteria and Blinding
Criteria: exactness, regularization independence, convergence control. The
two routes were implemented from independent formulas (no shared
intermediate); comparison happened only after both were frozen in tests.

## Proposed Claim Delta
None. All public symbols are conditional, unpromoted infrastructure linked to
issue #26; no registry or release change is requested. Refuted preprint
statements are external claims and do not enter the registry.

## Implementation and Oracle Plan
Module `src/substrate_framework/twisted_casimir.py`; tests
`tests/test_twisted_casimir.py`. Oracles: SymPy exact algebra (transition
matrices, entrywise centralizer, Sec. 7 coefficient matching), mpmath
special values (E2, beta, S sums), NumPy adjoint lattice Laplacian (method
validation against the analytic Epstein spectrum), regulator refinement,
mutation probes (twist mutations change DeltaV as predicted; preprint
coefficient measurably fails; nilpotent counterexample verifies the generic
commutant). Replay: targeted pytest plus one full `scripts/validate.sh` at
the final boundary (run as a background process per the long-running-script
convention). Scope note (harvest review 2026-08-10): the fundamental-bundle
obstruction, flux lattice, and flux-tube ensemble were split out of this
campaign into a separate issue-first extension effort.

## Verdicts (verified results of the audit)
Each verdict names its oracle route.

1. Preprint Eq. (46) E2(-1;alpha) = -S(alpha)/(4 pi^2) is false (Eq. (47)
   merely defines S(alpha)):
   E2(-1;alpha) = 0 identically (FE argument; E2 = 4 zeta beta factorization
   with beta(-1) = 0; direct tests to 1e-30).
2. The kept term in Eq. (51) is the one that cancels between sectors; the
   dropped lambda ln lambda term carries the entire difference. Corrected
   gauge-sector result: DeltaV = +5G/(2 L^4) > 0 (route A closed form via
   E2'(-1;alpha) = -S(alpha)/pi^3 and beta'(-1) = 2G/pi; route B regulated
   sums converge to -5G/(2 pi) for D; agreement at 2e-4 and improving under
   refinement). The toronic sector is disfavored; the periodic vacuum is
   preferred.
3. Sec. 7: the paper's own gap ansatz gives lambda_eff = -c g^4/4 (negative,
   unbounded below), not +c g^4/8 (exact SymPy matching).
4. Sec. 6: the stabilizer of {i sigma3, i sigma1} is Z2, not U(1)_em (exact
   entrywise commutant, verified on the nilpotent counterexample); the orbit
   is a gauge orbit.

(The fundamental-bundle obstruction, flux-energy estimate, and Minkowski
tube-ensemble analysis moved to the extension campaign per the 2026-08-10
harvest review; they are not part of this campaign's mergeable scope.)

## Attempts and Continuation
Append-only attempt record.

| Attempt | Route | Verdict | Mechanism | Next |
| --- | --- | --- | --- | --- |
| 0001 | ad-hoc pure-Python sums (outside workflow) | numeric indication only | no oracle governance | canonical module |
| 0002 | naive matrix commutant index map | wrong rank (3 vs 1) | hand-rolled vec map | Kronecker formulation |
| 0003 | Kronecker vec commutant | wrong for generic input | column-major vec reshaped row-major (harvest review, nilpotent counterexample) | entrywise linear-system formulation (landed) |
| 0004 | extension scope inside this campaign | split per harvest review | out of issue #26's predeclared scope | separate extension campaign |

## Debt Ledger
Campaign debt tracked here.

| Debt | Introduced by | Why it is real | Discharge artifact | Status |
| --- | --- | --- | --- | --- |
| beta'(-1) = 2G/pi numeric evidence only | route A closed form | no symbolic derivative oracle | route B agreement without special-value input | discharged for the verdict by the cross-route test; the symbolic identity itself is open mathematical frontier (non-blocking, out of scope) |

## Review and Promotion Plan
No claim promotion requested. PR inventory states the conditional status of
every public symbol. Reviewer focus: the two-route agreement, the entrywise
commutant (with nilpotent counterexample), and the lattice method
validation. Full-suite validation runs once at the final boundary.

## Done Gate
This audit is complete when PR #27 is open with targeted tests green and one
clean full-suite validation recorded, and the harvest-review findings are
disposed. The fundamental-bundle obstruction, flux-background one-loop, and
Minkowski ensemble questions live in the extension campaign, not here.
