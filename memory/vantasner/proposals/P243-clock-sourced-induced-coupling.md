---
description: P243 clock-sourced induced coupling — derive N and Lambda from the confined-clock fluctuation spectrum and drive Delta(1/G) numeric through the accepted composition
author: ox-alpha
created: '2026-08-22T14:30:00+00:00'
updated: '2026-08-22T14:30:00+00:00'
tags:
- substrate-framework
- campaign-proposal
category: proposals
confidence: exploratory
status: active
---

## Question and Positive Deliverable

This campaign derives the confined-clock substrate's own gravitational
premises. The positive deliverables are: (1) a derived fluctuation census N and
squared-gap spectrum {m_i^2} for the second variation about the relaxed radial
hedgehog in its finite stability window; (2) a cutoff scale Lambda selected
from preregistered substrate-length candidates under frozen structural
criteria; (3) an exact multi-species extension of C-IGR-004 by species
additivity yielding a numeric Delta(1/G) with the exact scheme bracket quoted;
(4) one controlled weak-field consumer driven by that same sourced coupling
with the clock's own density as source; (5) a force verdict for the
exactly-flat channels with sign and power law or a mechanism-named structural
refutation. A no-go, residual, or honest obstruction on any leg is attempt
evidence and redirects the mechanism; it does not complete this campaign.

## Base Release and Provenance

The accepted base is release v0.163.0 at commit fda76ef with a clean tree.
Source claims read directly at source: C-IGR-001..004, C-GRV-001/002, and
C-STG-001/002 statements in governance/claims.yaml lines 9090-9230 and
11961-12085. Canonical modules read: m5_stationary_fields.py (radial relaxation
API, pinned spectral targets 4/1/0.3/0), m5_covariant_action.py (spectrum
potential, LDG coefficients), total_gravitational_coupling.py (J(z) families,
usable schemes, baseline provenance), scalar_induced_newton.py (one-loop shift
coefficient), linearized_einstein.py (weak-field monopole ledger). Committed
P240 attempts 0041-0043 provide the independent torch-autograd Hessian route,
the finite window R in [~8,~34], and the boxed pair-oracle negatives.

## Invariants, Conventions, and Allowed Imports

Allowed imports are exactly the accepted claims C-GRV-001, C-IGR-001..004,
C-GRV-002, C-STG-001 plus the canonical modules listed above; no fitted
constant enters any promoted statement. The usable scheme set stays derived by
legs L1/L2/L3; the baseline B stays declared per C-GRV-001 with the
purely-induced reading B=0 available only as a declared premise per C-GRV-002;
no propagating collective tensor is rescaled into a metric. Units are the
action's own dimensionless units where gaps are O(1) and energies O(50); any
physical-scale statement quotes E_cut=hbar*c/a ontology per C-GRV-001 without
inserting observed values. Comparator blinding holds until the spectrum claim
and scale-selection criteria freeze; J(z) numerics open only after the
structural verdict on Lambda records. Numerics follow
.agents/skills/small-ratio-numerics: declared scale-relative error models
before inspection, second-variation operators rather than gradient methods on
soft directions, mesh/quadrature refinement, two structurally independent
routes at the house 1e-8 standard where exactness is unavailable, pinned BLAS
threads recorded per attempt.

## Candidate Preregistration

This campaign's only genuine mechanism selection is the cutoff scale, and the
candidates below compete only there; every other object follows from one
symmetry-fixed decomposition.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Lambda = 1/L_grad, L_grad the preregistered gradient-energy centroid radius of the relaxed hedgehog | gradient energy density is the object's UV-resolving observable | none new | z_i = m_i^2*L_grad^2 = O(1..10); ontology closes via E_cut=hbar*c/a | box-independence and refinement stability of z_i |
| B | Lambda = pi/R_box quantization scale | box modes realize the cutoff | box radius | expected reject: IR, box-dependent | moves linearly with domain_radius, fails criterion 2 |
| C | Lambda^2 = max pinned spectral target 4.0 | potential pinning carries the UV scale | none new | expected reject unless a length ontology is supplied | no length identification exists in canon |

For the spectrum itself the channel decomposition is fixed by the model's
symmetries (radial q, tangent t, split d sectors under polar/azimuthal
exchange); no competing mechanism is being selected there, so one derivation
route plus one independent implementation suffices per fixed-theorem discipline.

## Selection Criteria and Blinding

Scale candidates rank by: (1) cutoff-ontology closure, a genuine substrate
length admissible under C-GRV-001; (2) box-independence; (3) refinement
stability of z_i under control-count and quadrature refinement; (4) assumption
and parameter economy. Criteria were frozen before any candidate's numeric
value was computed; J(z) values and Delta(1/G) numbers stay blinded until the
C-M5S-002 selection record is written.

## Proposed Claim Delta

Collision searches on 2026-08-22 across governance/claims.yaml, proposals/,
campaigns/, and durable memory found zero occurrences of the prefix C-M5S;
reserved historical identifiers C-M5-001..008 remain untouched and unused here.

- C-M5S-001 (numeric): confined-clock second-variation census — bound-channel
  squared gaps and multiplicities about window backgrounds, separated from
  box-continuum classes, with refinement evidence and an independent-route
  agreement gate. Consumers: all later legs.
- C-M5S-002 (numeric + applicability): scale identification Lambda=1/L_grad
  with sensitivity of z_i to reasonable core observables. Consumer:
  C-M5S-003/004 evaluation.
- C-M5S-003 (symbolic_verified): multi-species additivity of the accepted
  one-loop families, Delta(1/G)=sum_i s_i*Lambda^2*J(z_i), s_i=N_i*(1-6*xi_i)/(
  12*pi), with the baseline-status statement that the finite counterterm B is
  not generated by the cutoff leg. Dependencies: C-IGR-001..004, C-GRV-001/002.
- C-M5S-004 (numeric): the sourced weak-field consumer — Poisson solve with
  G_total from C-M5S-003 and the clock's own time-averaged density, exterior
  monopole match against linearized_einstein conventions, acceleration
  observable, mutation and refinement gates; radiative attempt recorded at its
  honest role.
- C-M5S-005 (numeric or structural refutation): flat-channel pairing between
  two clocks via asymptotic matching of massless-channel moments; delivers sign
  and power law or names the missing construction, cross-checked against the
  committed boxed static result +456.6*d^-1.696.

## Implementation and Oracle Plan

New canonical module src/substrate_framework/m5_fluctuation_spectrum.py
(numpy/scipy only; no torch in the package) builds the second-variation form of
the radial energy around relax_m5_radial_hedgehog outputs on modal control
bases, extracts low-lying eigenvalues per sector with nodal census, and reports
refinement diagnostics; attempt scripts import it with PYTHONPATH=src. The
independent route re-executes the committed P240 torch-autograd machinery at
window radii; acceptance requires structural agreement of the bound census and
gap agreement within the declared error model. Scale observables compute from
the same relaxed solutions. Composition verification is sympy-exact, reusing
total_gravitational_coupling and scalar_induced_newton APIs per species plus a
linearity lemma; mutations (wrong xi weight, dropped species, flipped sign)
must fail their gates. The consumer solves the radially symmetric Poisson
problem by scipy.solve_bvp with declared tolerances, refinement ladder, exterior
monopole match, and load-bearing-input mutations. Force pairing follows the
small-ratio skill's multipole-pairing method; energy subtraction at separation
is prohibited as an oracle. Every verifier captures stdout into attempts/000N/
on first execution; check tallies use CheckLedger conventions; solver status is
a prerequisite, never the verdict.

## Attempts and Continuation

Append-only under proposals/P243-clock-sourced-induced-coupling/attempts/.
Execution waves: wave 0 research (complete — this contract), wave 1 spectrum +
scale (independent of composition numbers), wave 2 composition + consumer,
wave 3 force pairing, wave 4 governance. After failure: repair method defects,
change representation on instability, reject reformulated concepts, and reopen
foundations only through a separate challenge if a conflict survives
independently of every candidate here.

### Attempt 0002 (complete — scale candidates refuted)

Clock branch reproduced in-campaign at R=8/R=10 (R=8 energy matches the
phase1 ladder exactly; R=10 cross-seed from committed largeR-roots
coefficients converges onto the same root at 1.07e-15; order-16
lambda_min matches to 9 digits).  All three preregistered cutoff
candidates refuted under the frozen criteria: the branch's gradient-
energy cloud is domain-filling (L_grad ~ R^0.5, L/R 0.434 -> 0.332 over
R = 8..14, no saturation; core carries 97-99% of weight), so candidate
A fails box-independence at every declared thresholding variant (11-13%
drift vs the 5% gate); B is IR by construction; C lacks length
ontology.  Artifacts: attempts/0002/{window_continuation.py,
scale-results.json, largeR-centroids.json, selection.json, result.yaml}.
Numeric Delta(1/G)/G_total stay blinded (attempts/0003/
numeric_evaluation.py gates on selection.json).  Registered next
construction, candidate D: Lambda = 1/R* with R* the Morse-index
critical radius of the branch (bisection between the certified R=6
index-1 saddle and the R=7.5 index-0 window root) — an action-level
threshold, box-independent by definition.  Negative sub-record: the
canonical energy-minimizing relaxer cannot reach the excited clock
branch from cold starts (selects a droplet branch); continuation
seeding required.

### Attempt 0004 (complete — candidate D refuted; two-family structure discovered)

Candidate D (Lambda = 1/R*, R* the Morse-index critical radius,
preregistered before any solve) is refuted: no such radius exists.
Bisection initially located an index flip inside [6.0, 6.0117],
order-stable (16/18/20) and quadrature-stable at frozen fields (the
certified lambda_1 = -6.255e-2 at R=6 is real, nodes 32..96), but the
flip was seed-history: the certified P240 R=6 root and the stable
window roots lie on TWO distinct stationary-point families.
Family U (certified root): unstable through R=8.0 (lambda_1=-1.38e-2,
E=50.706 vs the certified stable window root E=50.446).  Family S
(all window roots R>=7.5): stable with lambda_1 ~ +8e-6 plateau from
R=14 down through R=5.9, no fold.  Systematic recorded: stable-side
lambda_min halves geometrically per order (N16..N24, no saturation —
marginal-mode-like).  Negative sub-record: fine-quadrature RE-SOLVES
jump families near flat directions; independence checks must evaluate
frozen field values.  Registered candidate E (not yet computed):
Lambda = 1/R_U*, R_U* = stabilization radius of family U, bisection
between measured index>=1 at R=8.0 and the extrapolated crossing
R~8.3-8.5; family identity enforced by continuation seeding from the
certified root.  Flag for user/P240 governance: the certified R=6
kinetic-axis root is an unstable saddle with a stable twin family at
the same radius; family qualifier question left to P240.  Numerics
stay blinded (selection.json still null).

### Attempt 0005 (complete — E refuted, F selected, numerics UNBLINDED)

Candidate E (Lambda = 1/R_U*, family-U stabilization) is REFUTED: U's
soft eigenvalue rises from -6.26e-2 (R=6.05) to only -1.42e-3 at
R=14 with geometrically decaying increments (ratio ~0.85 rising), whose
partial sums bound all future rise below |lambda_1(14)| — negative
asymptote ~-2e-4, no crossing in the certifiable regime.  Chain replay
of the whole 0004 route was bit-exact (thread-pinned).  Candidate F,
registered mid-attempt before its comparators ran:
Lambda^2 := E_U - E_S (same-order U-S stationary-family splitting),
mean over R in {8,10,12,14} = 0.26847204181661866, Lambda =
0.5181428778016915, bounds +-1.7%.  Frozen criteria: box-independence
3.23% spread (<5%); quadrature rows (frozen fields, 48x24) shift
Delta_E by 2.0e-4/2.45e-4; order-18 row DECLARED UNAVAILABLE — every
U-leaning order-18 solve lands in S18 or diverges (named obstruction,
documented, not silently substituted).  ALL 7 SELECTION CHECKS PASS.
UNBLINDED via exact-symbolic boundary (nsimplify rationals; floats
never cross; canonical modules reject float cutoffs AND float zeros):
Delta(1/G) xi=0 N=3 = 0.02136432626854447 (=Lambda^2/4pi exact to
1e-12); G_total(B=0) = 46.80699908016004 (=4pi/Lambda^2); band
[0.9686, 1.0323].  total_inverse_newton field IS 1/G_total when
baseline=0 — invert for G_total.  Method scars: coefficient-vector
length IS the order (order changes cannot be tested at frozen fields —
quadrature can); re-solve ladders near flat directions jump families a
third time; acceptance guards on solver output need energy-continuity
bounds, not just lambda sign + relgrad (a diverged root passed both).
### Attempts 0006-0007 (complete — consumer BVP solved; force verdict ATTRACTIVE; regime INVALID at xi=0)

Consumer BVP (0006): the committed R=12 order-16 window root's own
static density sources Poisson with G_total=46.807; second-order
flux-form FD, regular origin, Robin exterior match.  ALL 7 CHECKS
PASS (mass identity via plain GL sum — never trapezoid over weighted
values; drifts 1.15e-5->4.63e-6; Gauss law <5e-3; Phi(R)=-213.397=
-GM/R exact; mutation linear to solver floor).  HEADLINE: G*M/R=
213.4 >> 1 — at xi=0 the sector is STRONGLY coupled to its own
gravity; linearized consumer formally solved but outside its regime.
Escape routes: xi near 1/6 (Delta->0), weaker sector, or nonlinear
treatment.  Force pairing (0007): moment-pairing method (no energy
subtraction): F = G_total M1 M2/d^2, ATTRACTIVE at xi=0,
G_total = 1/Delta(1/G) = 46.807; flat channel (z==0, J(0)=1) adds no
independent term; Delta(xi) sign structure: attraction <1/6,
cancellation AT 1/6, repulsion >1/6.  ALL 6 CHECKS PASS.  Scars:
chebyshev_stack acos-backward NaNs at Chebyshev endpoints r=R exactly
(clamp evaluation inside domain); torch grids need requires_grad_
for elementwise_derivative; HERE.parents[3] not [4] from attempt dirs;
solver-acceptance gates must sit above sparse-solve roundoff (~1e-9).


## Debt Ledger

Empty at instantiation. Declared hypotheses live in the manifest; honest
exclusions (boxed-model limits, single-window background family, conventional
core-observable definition with quoted sensitivity) are named surfaces of the
claims themselves, not hidden assumptions.

## Review and Promotion Plan

One claim-level review per proposed claim by a distinct reviewer agent with raw
artifacts and acceptance criteria, using memory-templates/claim-review.md; the
proposing agent neither reviews nor merges. Evidence attachments carry explicit
roles (exact_proof for C-M5S-003, regression/applicability for refinements).
On acceptance: extract reusable logic into src/substrate_framework/ with tests,
update governance/claims.yaml, pin release v0.164.0, run scripts/render_docs.py,
synchronize accepted-claim memory, record one content-addressed validation
receipt via scripts/validate_changed.py scope selection, and move the
adjudicated record into campaigns/. Validation and commit run as separate
process invocations.

## Done Gate

The campaign closes when all five claims pass their applicable gates with
individual reviews, the promotion set enters the registry and a pinned release,
generated docs and memory agree, and the in-boundary debt ledger is empty —
or when a leg terminates at a named gate whose mechanism is recorded, in which
case the objective stays open with the next construction queued. Each next
step states what becomes true in the record when it succeeds.
