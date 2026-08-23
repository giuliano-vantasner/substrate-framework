---
description: P243 continuation — finish issue #163's four open criteria (window-background census, B settlement, np/nâ pairing verdict, radiative attempt) on top of the promoted v0.164.0 claims
author: ox-alpha
created: '2026-08-23T13:30:00+00:00'
updated: '2026-08-23T21:30:00+00:00'
tags:
- substrate-framework
- effort
category: efforts
confidence: working
status: active
---

# P243 Continuation Effort — closing issue #163's open letter

## Goal and Success Contract

Issue #163 was reopened on 2026-08-23 because PR #167's auto-close outran the
issue's own closure checklist. Five claims (C-M5S-001..005) are accepted and
stay accepted at their reviewed scopes; what remains is the issue letter:

1. **A — window-background census**: registry-grade bound-channel spectrum of
   the second variation about a confined-clock window background (not the
   aligned vacuum), separated from box-continuum classes, refinement +
   independent-route gates. Either confirms N=3 or redirects everything
   downstream. **First, because Δ(1/G), G_total, and both force laws
   normalize through N.**
2. **B — baseline settlement**: derive/bound the finite counterterm B or show
   it irreducible. Note the physics coupling: 1/G_total = B + Δ(1/G); the
   criterion-3 strong-coupling wall (G_total·M/R ≈ 213 ≫ 1) is computed under
   the B=0 declared reading, so a positive derived B is not bookkeeping — it
   is a candidate escape route for criterion 3.
3. **C — radiative attempt**: honestly attempted or blocked with the missing
   construction named.
4. **D — np/nâ shear-channel verdict**: dedicated sign/power-law answer for
   the H_split = diag(5,3,3,0,0,6)/2 exactly-flat shear channels between two
   clocks (distinct from the massless induced-channel pairing already
   delivered in attempt 0007).

Complete when each lands as an append-only leaf claim (or mechanism-named
refutation/blocking), reviewed individually by a distinct reviewer, promoted,
release-pinned, docs/memory synchronized, and #163 closes against its own
letter. Partial progress harvests; the objective stays open otherwise.

## Accepted Baseline

Release v0.164.0 pinned at c2efa38; main tip 17ec27a (= d90c698 promotion
merge + f80ea20 memory archive). Accepted inputs read at source:
C-M5S-001..005 statements in `governance/claims.yaml`; review records
`memory/vantasner/decisions/C-M5S-00{1..5}-review.md`; adjudication
`campaigns/P243-clock-sourced-induced-coupling/adjudication.yaml`; canonical
modules `src/substrate_framework/{m5_fluctuation_spectrum,m5_induced_coupling}.py`
with unit tests. Dependency canon unchanged: C-IGR-001..004, C-GRV-001/002,
C-STG-001/002.

## Reconciliation Ledger (prior sessions → current standing)

The table below is the assumption audit the continuation is built on: each
row pairs what an earlier session proposed or assumed with what actually
landed after review, and states the consequence this effort acts on. It is
the authoritative answer to "what do we still owe issue #163".

| Prior assumption / proposal prose | What actually landed | Current standing and consequence |
| --- | --- | --- |
| C-M5S-001 proposed as window-background census ("about window backgrounds") | Delivered as aligned-vacuum M0 census (targets 4/1/0.3/0): N=3 massless species, exact gaps; reviewer rescoped claim to aligned vacuum | Claim stands; issue criterion 1 keeps the window-background census OPEN → item A |
| Λ from preregistered gradient-length candidate A | A/B/C/D/E refuted with named mechanisms; F = E_U−E_S selected mid-attempt-0005 under frozen criteria (attestation-based preregistration, commit-verifiably ex ante) | Settled: Λ²=0.26847204181661866, spread 3.23%; order-18 refinement row remains declared-unavailable obstruction (non-blocking) |
| B treated as declared purely-induced reading (B=0 per C-GRV-002) | Attempt 0009: shown IRREDUCIBLE within the composition + quantitative weak-field bound derived (B_min = 212Δ–21339Δ) | SETTLED → item B complete; sharpens criterion 3 into a dichotomy |
| Consumer "controlled static weak-field result" | Solved cleanly (7 checks) with regime verdict G_total·M/R ≈ 213.4 ≫ 1 at ξ=0 — formally valid, physically outside linearized regime | Verdict IS the result; 0009 shows any B-escape is bare-dominated |
| Force question = "exactly-flat channels" | Delivered for massless induced channel (z=0): attractive ξ<1/6, cancellation at ξ=1/6; boxed-static dropped as category mismatch | np/nâ gradient-stiffness shear channels have NO dedicated verdict → item D |
| Radiative check attempted either way | Never attempted | Falls short of criterion 3's bar → item C |
| Campaign memory said "closed end-to-end" | Wrong; corrected, issue reopened with scorecard | This effort file supersedes that status |

## Constraints and Invariants (carried forward)

Allowed imports stay exactly the accepted claim set plus canonical modules;
no fitted constant enters any statement. Blinding discipline is LIFTED
(selection froze in 0005). Units: action dimensionless, gaps O(1), energies
O(50); no observed-value insertion. No propagating collective tensor
rescaled into a metric (Route-2 no-go). Numerics per
`.agents/skills/small-ratio-numerics` — explicitly applied in 0008:
λ_min/λ₂ quoted (~4e-3), box extrapolation run, mesh Richardson via FD
ladder, frozen-field discretization tests, pinned BLAS threads recorded.
Attempts append-only under `campaigns/P243-clock-sourced-induced-coupling/
attempts/`. New claim IDs collision-searched clean (C-M5S-006+ free).

## Decomposition

1. [x] Recall, source verification, reconciliation ledger.
2. [~] A: window-background census — stage 1 COMPLETE (5/5); cross-order =
   named obstruction; stage 2 kinetic metric EXECUTED (positive metric on
   all modes; tangent channel = structural null); FD route G0 PASSED
   (transfer 2e-4) with GRID ARTIFACT x6 verdicts; box trend disfavors
   domain-gift. Remaining in item A: relgrad-consistency note is resolved;
   outstanding = constrained-subspace labels + writing the soft-mode
   adjudication claim (moves to governance as C-M5S-006 draft).
3. [x] B: baseline settlement — COMPLETE (attempt 0009, 5/5 checks):
   B IRREDUCIBLE within the accepted composition + NEW bound: weak-field
   validity requires B ≥ (M/R)/ε* − Δ = 212Δ (marginal) to 21339Δ
   (0.1% field). Criterion-3 dichotomy now exact — induced+strong-coupled
   (B~0) or bare-dominated+weak-field (B≫Δ); middle ground empty.
4. [x] D: np/nâ shear-channel pairing verdict — COMPLETE (attempt 0010,
   7/7 checks): STRUCTURAL REFUTATION with mechanism. Exterior
   factorization lemma (exact): compact-support pinning makes the
   two-clock field outside both supports the exact rank-1 projector
   nn^T(Θ₁+Θ₂); every derivative is a scalar times one generator A with
   [A,A]=0, so exterior static density ≡ 0 (numeric max 1.4e-23 over 150
   configs; mutation contrast ~1e18). No protected flat direction on the
   physical background; only long-range kernel in the accepted composition
   is Newton (0007). First-draft identity lemma refuted by its own check,
   superseded draft recorded verbatim.
5. [x] C: radiative attempt — COMPLETE (attempt 0011, 5/5 checks).
   R1 decay decided STABLE (composition of exact premises: massive
   positive-metric spectrum with grid-artifact light modes excluded;
   static ground state; pure-gauge exterior tail). R2 zero-point mass
   shift BLOCKED with missing construction named — certified
   complete-spectrum table (full-band independent-discretization
   agreement); blockers recorded: 9.9% soft-ω² quadrature drift,
   cross-order 52% stationary-point jump.

## Reasoning Thread and Decision Log

Thread the logic so a fresh session can rebuild the chain without re-deriving:

- **Why N=3 stands but is vacuum-scoped**: exact affine-uniqueness
  certification covers the ALIGNED VACUUM only; the hedgehog background's
  soft-mode count was genuinely open — this effort's item A settles it
  (see FD verdict below): no fourth light species survives scrutiny.
- **Why item A went first**: every downstream number consumes N and {z_i}.
- **Why B matters physically**: 1/G_total = B + Δ(1/G); at B=0 the wall
  GM/R≈213 exists; 0009 proves any B large enough to cross it is
  bare-dominated (≥212Δ), so criterion 3 becomes a clean dichotomy.
- **Why np/nâ was separate work, and its resolution (0010)**: 0007 paired
  massless induced-channel moments; the transverse shear channels needed
  their own verdict. Attempt 0010 proved the exterior-factorization lemma
  (exact): compact support + [A,A]=0 single-generator identity zeroes every
  internal tail beyond overlap; no flat direction survives on confined
  roots; Newton is the only long-range kernel in the composition. The
  issue's H_split/np-nâ labels have NO repo derivation site (scout-verified)
  — the claim draft must state the repo-real channel objects.
- **Why radiative last**: independent of all outcomes; honest-blocked is
  acceptable terminal if construction is named.
- **Grid-mode suspicion → RESOLVED as artifact (0008)**: softest mode had
  13–14 nodes at order 16 with λ_min halving per order (classic grid-mode
  signature). FD route (independent radial discretization, G0 transfer
  2e-4) shows λ₀ collapsing 5.3e-7 → 4.9e-8 → 8.6e-9 across N_r=48/72/96.
  Box trend does NOT rescue it (λ₀ rises with R). Kinetic metric positive
  but quadrature-sensitive. Conclusion: P240's marginal plateau is a
  spectral-resolution artifact; family-S window roots carry no ultra-light
  physical modes. Confidence solid pending independent review.
- **Cross-order obstruction mechanism (0008)**: seeded N=18 converges
  (relgrad 1.8e-14) to a DIFFERENT stationary point (stiff-band drift 52%;
  truncated root at relgrad 0.73 on N=16 functional). Order ladders about
  window roots are dead; use independent discretizations instead.
- **Verifier-defect scars (0008)**: `centered_curvature` normalizes by
  max(1,|E|)≈55.1 not block scale (~18× errors if unnormalized);
  global-top-eigenvalue scales make gates vacuous (use block-local s_b);
  float64 second differences cannot resolve curvatures below ~1e-2·s_b;
  shared (1,N_μ) μ-tensor makes autograd SUM derivatives over radial rows
  (repeat the grid like committed code does); missing −sine/r factors
  inflate θ/φ derivatives ~600×; **the FD grid variable (r/R)² must NOT be
  re-squared inside committed formulas expecting r/R** (root cause of the
  transfer failure); `jac.norm()` is a Hessian operator norm, not a
  gradient norm — label them separately (the phantom relgrad≈50).
- **Tangent-channel structural null (stage 2)**: pure tangent velocity is
  tdot(r)·Identity, commuting with every gradient — kinetic metric
  vanishes identically (trace/constraint direction). Tangent-heavy mixed
  modes need constrained-subspace projection weights for honest labels.

## Attempts

Append-only. Full detail lives in `attempts/000N/` (result.yaml + scripts +
first-execution stdout; superseded verifier runs kept verbatim).

| Attempt | Candidate or repair | Artifact | Verdict | Mechanism / lesson | Next |
| --- | --- | --- | --- | --- | --- |
| 0001 | Aligned-vacuum exact census | attempts/0001 (vacuum_census.py) | PASS (N=3 massless; 4 stiff; 3 inert) | affine-uniqueness certification; mutations gate | vacuum-scoped; window census owed → 0008 |
| 0002 | Scale candidates A/B/C | attempts/0002 | ALL REFUTED | L_grad ~ R^0.5 domain-filling; B IR; C no ontology | candidate D registered |
| 0004 | Candidate D (Λ=1/R*, Morse radius) | attempts/0004 | REFUTED | bisection flip was seed-history across families U/S; hardening protocol born | candidate E registered |
| 0005 | Candidate E refuted; F selected; UNBLIND | attempts/0005 | F PASS (7 checks) | U-family λ₁ never crosses zero; F=E_U−E_S box-stable 3.23% | order-18 row declared-unavailable |
| 0006 | Consumer Poisson BVP | attempts/0006 | PASS + regime INVALID at ξ=0 | GM/R≈213≫1; flux-form FD; GL-sum mass identity | escapes registered |
| 0007 | Massless induced-channel pairing | attempts/0007 | PASS (ξ-structure of attraction/cancellation) | moment pairing, no energy subtraction; endpoint NaN clamp | np/nâ verdict owed → item D |
| 0008 | Census S1 + X-order + S2 kinetic metric + FD route + box trend | attempts/0008 (window_census.py, cross_order.py, kinetic_stage2.py, fd_route.py + jsons/logs) | S1: 5/5 PASS; X-order: OBSTRUCTION; S2: 1/3 gates; FD: G0 PASSED, **GRID ARTIFACT x6**; box: gift disfavored | tangent null; double-square sampling root bug; shared-μ summation; sine/r factors; jac.norm mislabeling | adjudication claim → governance |
| 0009 | B settlement: irreducibility + weak-field bound | attempts/0009 (baseline_settlement.py, baseline-verdict.json) | 5/5 PASS — **B IRREDUCIBLE**; B_min = 212Δ–21339Δ for ε*=1..0.01 | criterion-3 dichotomy: induced+strong-coupled OR bare-dominated+weak-field; middle empty by exact arithmetic | feeds final report criterion-3 wording |
| 0010 | np/nâ shear-channel verdict | attempts/0010 (shear_channel_verdict.py, shear-verdict.json) | 7/7 PASS — **STRUCTURAL REFUTATION**: no long-range np/nâ channel | exterior factorization: pinned field = exact projector nn^T(Θ₁+Θ₂), single-generator [A,A]=0 ⇒ exterior density ≡ 0 (probe 1.4e-23; mutation contrast 1e18); first-draft identity lemma refuted by own check C1a, recorded | criterion-4 wording in final report |
| 0011 | Radiative attempt | attempts/0011 (radiative_stability.py, radiative-verdict.json) | 5/5 PASS — **R1 STABLE** (no decay channel); **R2 BLOCKED** (zero-point shift) | stability = massive spectrum + static ground state + pure-gauge tail; blocker: full-band certified spectrum table missing (9.9% soft drift; 52% cross-order jump) | criterion-3 clause satisfied either-way |

## Validation Plan (per item)

Each numeric leg: solver status prerequisite, refinement ladder, mutation
that must fail, scale-relative thresholds, independent route where exactness
unavailable; stdout captured to attempts/000N/ on FIRST execution. Symbolic
legs: sympy-exact + mutation probes. Memory-only PRs: frontmatter checks +
`git diff --check`. Promotion transactions: `scripts/render_memory.py`
BEFORE `scripts/validate.sh`; scoped-vs-full per AGENTS.md triggers
(additive leaf claim + new module tests → likely scoped; anything touching
shared numerics or existing contracts → full).

## Resume Mechanics (crash recovery)

This section exists so any fresh session can resume without re-deriving
session history. Follow it top to bottom; every entry earned its place by
bite-mark.

- Working dir `/home/dan/substrate-framework`, branch off latest origin/main.
- Verifiers: `PYTHONPATH=src python campaigns/P243-clock-sourced-induced-coupling/attempts/NNNN/<script>.py`.
- Module semantics: `numeric_induced_shift(...)` takes cutoff=**Λ** (value ∝ Λ²)
  and rejects floats (`exact_real`) — pass exact rationals/`sp.sqrt`;
  `MINKOWSKI_MOSTLY_PLUS` = (−,+,+,+); m5_* modules NOT re-exported in `__init__`.
- torch grids need `requires_grad_()` before elementwise derivatives; system
  numpy is 1.26 (no `np.trapezoid`) on the torch host — use canonical
  `trapezoid_integral` or two-step fallback.
- After any `governance/claims.yaml` edit: `scripts/render_memory.py` then
  validate. Author never merges own PR: **PRs stay OPEN — the user reviews
  and merges next session (user directive 2026-08-23).**
- Update THIS file (updated timestamp + attempt row + reasoning additions)
  at every milestone; push via memory-status PR so state survives crashes.
- Edit discipline learned many times over here and in scripts: NEVER chain
  anchored edits from remembered line numbers — re-read immediately before
  editing, one content-exact hunk per call, and after two failed patch
  rounds switch to a single full-file rewrite. YAML plain scalars must not
  contain ": " — quote or rephrase.

## Debt Ledger

Empty inside promoted scopes. Open items above are campaign frontier (issue
letter), not debt. Named non-blocking follow-ups live in review files
(literal-True tally relabels, float-signature wart in
`numeric_induced_shift`, order-18 obstruction, R>14 loophole).

## Cross-References

Proposal (archived):
`memory/vantasner/proposals/P243-clock-sourced-induced-coupling.md`;
campaign: `campaigns/P243-clock-sourced-induced-coupling/`;
claims: `governance/claims.yaml` (C-M5S-001..005);
release: `governance/releases/v0.164.0.yaml`;
reviews: `memory/vantasner/decisions/C-M5S-00{1..5}-review.md`;
issue: https://github.com/vantasnerdan/substrate-framework/issues/163
(scorecard comment 2026-08-23); PRs #167/#168 merged;
continuation PR: #169 (this file + attempts 0008..0011 artifacts).
