---
description: Certify the confined-clock full-band kinetic-normalized spectrum about the committed R=12 family-S root via independent quadrature families, then compute the blocked zero-point mass shift with an honest error budget
author: ox-alpha
created: '2026-08-25T19:30:00+00:00'
updated: '2026-08-25T21:45:00+00:00'
tags:
- substrate-framework
- campaign-proposal
category: proposals
confidence: exploratory
status: active
---

## Question and Positive Deliverable

C-M5S-009 delivered radiative stability but blocked its quantitative half on one named
construction: a certified complete kinetic-normalized spectrum table with
independent-discretization agreement at a declared scale-relative tolerance across the
full band. This campaign constructs exactly that object about the committed R=12
family-S window root (order-16 basis), certifies the fluctuation frequencies whose
quadrature sensitivity was recorded as gate G2 failure in P243 attempt 0008, and
computes the renormalized zero-point mass shift delta-E = (1/2)*sum_i omega_i over the
certified propagating set within the committed model class, carrying an itemized error
budget.

## Base Release and Provenance

Base release v0.165.0, main tip dbf44fa (merge of PR #171, small-ratio-numerics
hardening). Accepted inputs read at source: C-M5S-001..009 statements; C-M5S-006 root
provenance for the R=12 family-S window root with stiffness block scale s_b =
2.982251210281484; C-M5S-009 missing-construction wording; attempt artifacts of
campaigns/P243-clock-sourced-induced-coupling/attempts/0008; committed infrastructure
proposals/P240-m5-kinetic-axis/attempts/0041 cpu_energy.py and solve_radial_1d.py plus
attempts/0042 largeR-roots.json; canonical modules under src/substrate_framework/.

## Invariants, Conventions, and Allowed Imports

The background is FROZEN once and never re-solved; refinement varies only the
discretization of the fluctuation operator about identical field data. Committed
functional conventions are preserved verbatim: envelope factors x^2(1-x^2), (1-x^2),
x^4(1-x^2); potential V(S) = -0.5 tr S^2 - tr S^3 + (tr S^2)^2 + 0.5; measure
2*pi*r^2 dr dmu; Frobenius product; fixed director frames. The tangent-channel family
is an exact kinetic null deflated analytically; the kappa projector-current term stays
excluded with its recorded bias direction; no fitted constants enter any statement;
the Route-2 no-go is respected. Numerics follow the hardened small-ratio-numerics
skill: pinned BLAS threads, compensated reductions feeding quoted quantities,
observed-order checks before extrapolation, per-quantity budgets, zero-mode gauges.
Allowed imports: C-M5S-001/002/006/009 as accepted context and protocols; P240 0041
and 0042 helper APIs and roots as source-audited committed infrastructure; canonical
package modules read-only.

## Candidate Preregistration

Route A is the committed modal machinery itself with autograd-exact derivatives on
Gauss-Legendre nodes. Route B candidates registered: Chebyshev-family quadrature via
rule injection into the verbatim committed machinery (selected once FD ladders proved
derivative-discretization cross-checks floor at their own truncation), with the FD
radial route retained as supplementary coarse consistency evidence.

## Selection Criteria and Blinding

Route selection is structural: the selected second family shares no node set and no
weight rule with route A while keeping every other construction byte-identical, which
isolates the quadrature rule as the only variable between families. Gates were
declared before any route-B value existed. G0 transfer within 1e-6 relative per rung.
G1 symmetry and PSD hygiene at 1e-12 and 1e-11. G2 repaired per-band scale-relative
omega agreement with bands by stiffness decades of s_b and tolerances soft 5 percent,
mid 2 percent, stiff 1 percent of band-local maximum omega. G3 mutations: coefficient
mutation moves the pencil, channel rays pairwise distinct above 1 percent, R10-root
sensitivity in the scale-free form recorded in the attempts table. G4 artifact
adjudication follows C-M5S-006 where applicable. G5 certification margin omega at
least ten sigma with itemized budgets. G6 cross-family entry exactness with its
measured floor recorded rather than assumed.

## Proposed Claim Delta

C-M5S-010 (numeric_evidence): certified full-band kinetic-normalized spectrum table
about the committed R=12 family-S root by cross-family agreement under gates G0-G6,
with per-mode classification and itemized budgets. Dependencies: C-M5S-006.
C-M5S-011 (numeric_evidence): renormalized zero-point mass shift delta-E =
(1/2)*sum_i omega_i over certified propagating modes within the committed order-16
sector about that root, discharging the missing construction that C-M5S-009 names.
Dependencies: C-M5S-010 and C-M5S-009. Identifier collision search executed 2026-08-25
over governance, campaigns, proposals, and memory: all three identifiers free.
C-M5S-009 itself is neither rewritten nor challenged; its stability half stands and
its blocked half is completed downstream.

## Implementation and Oracle Plan

Attempts are append-only under proposals/P244-clock-full-band-spectrum/attempts/.
All verifiers run with PYTHONPATH=src against committed helper modules; stdout is
captured into the attempt directory on first execution.

## Attempts (2026-08-25 session)

Eight append-only attempts separate defect discovery from repair and each
verdict below is backed by captured stdout and JSON artifacts in its directory.

| Attempt | Content | Verdict |
| --- | --- | --- |
| 0001 | Route-A ladder on committed machinery; exposed non-converging M while H saturated at 1.4e-15 | VERIFIER DEFECT FOUND: P243-0008 kinetic_functional reduced as T=4(sum w)(sum rho) instead of per-cell weighting; positive-scalar scaling preserves all scale-free stage-2 verdicts; P240 inertia path verified clean; no accepted claim invalidated |
| 0002 | Corrected per-cell reduction; M saturates at 1.5e-15 like H; mp congruence bug produced a spurious uncertified population | implementation defects recorded; G0/G1 pass all rungs |
| 0003 | mp congruence repaired via Z^T H Z with L Z = I; band labels from per-mode stiffness Rayleigh quotients | all 32 kept modes certified; dE = 72.58859646 plus minus 3.7e-7 |
| 0004 | Scale-free sensitivity gate (R10 max relative shift 0.253 above 0.1); spectrum-table.json artifact | 7 of 7 CHECKS PASS |
| 0005/0006 | FD radial-discretization pencil ladders, second and fourth order stencils | cross-route agreement floors near median 4 percent because pointwise channel oscillation limits grid derivative accuracy regardless of stencil order; FD route demoted to supplementary consistency |
| 0007 | G6 quadrature-exactness by rule injection into the verbatim committed machinery using interior second-kind Chebyshev nodes with solved weights: M entries machine-exact at 3.1e-14; H entries floor at 4.5e-7 from algebraic pole content in the azimuthal channel; pencil 1.04e-7; delta-E replicates to 9.1e-10 | mechanism named; family floor folded into budgets |
| 0008 | Final certified table with cross-family budgets | 4 of 4 CHECKS PASS; all 32 kept modes certified; dE = 72.58859646 plus minus 3.9e-7 RSS and 9.2e-7 linear; the soft band is EMPTY and every certified frequency is O(1) or above with omega_min = 1.0464, independently reinforcing the C-M5S-006 no-fourth-species verdict at frequency level |

The scheme-spread frontier item of issue #170 was quantified from accepted canon with
no new claim: R(z) = J_smooth/J_sharp equals one exactly at z=0 with leading
difference EulerGamma*z; the unit-mass value is 2 e K_1(2)/(1 - e E_1(1)) =
1.8837726; R(4) = 15.61; regulator dependence for massive species reopens gradually
and is unbounded.

## Debt Ledger

Empty inside the proposed scopes. Declared hypotheses (frozen background, excluded
kappa term, order-16 sector scope) and measured mechanisms (algebraic endpoint content
of H densities) are recorded hypotheses or mechanisms, not debt.

## Review and Promotion Plan

One claim-level review per proposed claim by a reviewer without authorship, against
raw attempt artifacts. Then registry entries, release manifest bump, rendered docs,
memory synchronization, scoped validation. The pull request is opened, not self-merged,
per the standing user directive of 2026-08-23.

## Done Gate

Done when both claims pass individual review, enter the registry and a pinned release,
docs and memory agree, and issue #170's frontier item 2 comment carries the certified
result. If review refutes a statement, the objective stays open with the next
registered repair named.
