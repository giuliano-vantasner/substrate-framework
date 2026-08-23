---
description: P243 continuation — finish issue #163's four open criteria (window-background census, B settlement, np/nâ pairing verdict, radiative attempt) on top of the promoted v0.164.0 claims
author: ox-alpha
created: '2026-08-23T13:30:00+00:00'
updated: '2026-08-23T15:05:00+00:00'
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
| B treated as declared purely-induced reading (B=0 per C-GRV-002) | Same — never derived, bounded, nor shown irreducible | UNSETTLED → item B; interacts with criterion-3 wall (see Goal §B) |
| Consumer "controlled static weak-field result" | Solved cleanly (7 checks) with regime verdict G_total·M/R ≈ 213.4 ≫ 1 at ξ=0 — formally valid, physically outside linearized regime | Verdict IS the result; escapes registered (ξ→1/6, weaker sector, nonlinear). Item B may weaken the wall numerically |
| Force question = "exactly-flat channels" | Delivered for massless induced channel (z=0): attractive ξ<1/6, cancellation at ξ=1/6; boxed-static +456.6·d^−1.696 dropped as category mismatch (static-frame observable, P240) | np/nâ gradient-stiffness shear channels have NO dedicated verdict → item D |
| Radiative check "attempted and recorded either way" | Never attempted; listed as open frontier only | Falls short of criterion 3's bar → item C |
| Campaign memory said "closed end-to-end" | Wrong; corrected in durable memory 2026-08-23, issue reopened with scorecard comment | This effort file supersedes that status |

## Constraints and Invariants (carried forward)

Allowed imports stay exactly the accepted claim set plus canonical modules;
no fitted constant enters any statement. Blinding discipline is LIFTED
(selection froze in 0005; J(z)/Δ(1/G) numbers are public in the record).
Units: action dimensionless, gaps O(1), energies O(50); no observed-value
insertion. No propagating collective tensor rescaled into a metric (Route-2
no-go). Numerics per `.agents/skills/small-ratio-numerics`: scale-relative
error models, frozen-field discretization tests, two independent routes at
1e-8 where exactness unavailable, pinned BLAS threads recorded. Attempts
append-only under `campaigns/P243-clock-sourced-induced-coupling/attempts/`
(0009 next). New claim IDs must collision-search clean before allocation
(C-M5S-006+ verified free 2026-08-23).

## Decomposition

1. [x] Recall, source verification, reconciliation ledger.
2. [~] A: window-background census — STAGE 1 COMPLETE (attempt 0008, 5/5
   checks): bottom-block stiffness spectrum about the frozen R=12 root
   certified; two soft modes + six stiff; route-B FD agrees autograd to
   ~3e-7 relative on the stiff band. Pending inside item A: stage 2
   (fluctuation kinetic metric → propagating-vs-static classification of
   both soft modes) and the cross-order grid-mode adjudication leg.
3. [ ] B: baseline settlement (attempt 0009+, may parallel A after its background exists).
4. [ ] D: np/nâ shear-channel pairing verdict (needs A's channel structure).
5. [ ] C: radiative attempt (independent; last).
6. [ ] Governance: individual reviews, promotion, release bump, docs/memory sync, close #163 against its letter.

## Reasoning Thread and Decision Log

Thread the logic so a fresh session can rebuild the chain without re-deriving:

- **Why N=3 stands but is vacuum-scoped**: the census certified exact affine
  uniqueness of the kinetic matrix dP against its defining system (exact
  rationals; mutations move coefficients/gaps). That certifies the ALIGNED
  VACUUM answer only. The hedgehog clock background has different symmetry
  breaking (radial profile breaks O(3)-ish structure), so its soft-mode count
  is genuinely open — not a formality: if the window census finds a fourth
  light species or demotes one, Δ(1/G) = Σ_i s_i Λ² J(z_i) changes value and
  possibly z-structure (J(z_i) ≠ 1 for massive species).
- **Why item A goes first**: every downstream number (Δ(1/G), G_total=46.807,
  Φ(R)=−213.397, force normalization) consumes N and {z_i}. A change ripples
  everywhere; running B/D/C first risks rework.
- **Why B matters physically, not just bookkeeping**: 1/G_total = B + Δ(1/G).
  At B=0, G_total=46.8 makes the clock's own field strong (GM/R≈213). Any
  positive derived B lowers G_total toward the weak-field regime and could
  dissolve criterion 3's wall without exotic escapes. Conversely, proving B
  irreducible-with-bound pins the wall as real sector physics. Either outcome
  advances criterion 3.
- **Why np/nâ is separate work**: 0007 paired MASSLESS induced-channel
  moments (z=0, J(0)=1 fixes Newton-kernel normalization). The H_split
  shear channels are exactly potential-flat with gradient-generated stiffness
  — their mediated interaction, if any, is a different object; P240's boxed
  oracle resolved overlap channels negatively and the static-frame
  +456.6·d^−1.696 is another observable class entirely (dropped as
  cross-check during review for category mismatch).
- **Why radiative last**: fully independent of A/B/D outcomes; nothing
  downstream consumes it; honest-blocked is an acceptable terminal if the
  construction is named.
- **Decision rule carried from 0004/0005 scars**: near-flat directions jump
  stationary families under re-solve; all discretization/order tests run at
  FROZEN field values; acceptance guards need energy-continuity bounds, not
  λ-sign + relgrad alone (a diverged root once passed both).
- **Grid-mode suspicion (attempt 0008; must survive into stage 2)**: the
  softest window-background mode is split-channel-dominant with 13–14 radial
  nodes at basis order 16, and family-S λ_min halves per order across the
  committed R=8 ladder (4.5e-5 → 2.0e-5 → 9.7e-6). Nodal count ≈ order plus
  geometric halving is the classic spectral grid-scale-artifact signature —
  i.e. P240's "marginal plateau" may be a resolution artifact rather than
  near-flat physics. Adjudicate via cross-order re-solves under the
  0004/0005 hardening protocol BEFORE trusting any soft-mode count
  downstream.
- **Verifier-defect scars from 0008 runs 1–2**: `centered_curvature`
  normalizes by max(1,|E|)≈55.1, not by block scale — un-normalize by that
  exact factor or FD cross-routes are off by ~18×; global-top-eigenvalue
  scales make preregistered gates vacuous (use block-local s_b); float64
  second differences of E≈55 cannot resolve curvatures below ~1e-2·s_b at
  any stable step (soft-band FD exclusion is permanent).

## Attempts

Append-only. Full detail lives in `attempts/000N/` (result.yaml + scripts +
first-execution stdout; superseded verifier runs kept verbatim).

| Attempt | Candidate or repair | Artifact | Verdict | Mechanism / lesson | Next |
| --- | --- | --- | --- | --- | --- |
| 0001 | Aligned-vacuum exact census | attempts/0001 (vacuum_census.py) | PASS (N=3 massless; 4 stiff; 3 inert) | affine-uniqueness certification; mutations gate | vacuum-scoped; window census owed → 0008 |
| 0002 | Scale candidates A/B/C | attempts/0002 | ALL REFUTED | L_grad ~ R^0.5 domain-filling (11–13% drift vs 5% gate); B IR; C no ontology | candidate D registered |
| 0004 | Candidate D (Λ=1/R*, Morse radius) | attempts/0004 | REFUTED | bisection flip was seed-history across TWO coexisting families U/S; hardening protocol born | candidate E registered |
| 0005 | Candidate E refuted; F selected; UNBLIND | attempts/0005 | F PASS (all 7 checks) | U-family λ₁ asymptote −2e-4 never crosses; F=E_U−E_S box-stable 3.23% | order-18 row declared-unavailable (named obstruction) |
| 0006 | Consumer Poisson BVP | attempts/0006 | PASS + regime INVALID at ξ=0 | GM/R≈213≫1; flux-form FD; GL-sum mass identity (never trapezoid over weights) | escapes registered |
| 0007 | Massless induced-channel pairing | attempts/0007 | PASS (attractive/cancel/repulsive ξ-structure) | moment pairing, no energy subtraction; chebyshev endpoint NaN clamp | np/nâ verdict owed → item D |
| 0008 | Window census STAGE 1: stiffness bottom-block about frozen R=12 root, banded gates | attempts/0008 (window_census.py, census-v3.json) | 5/5 PASS | route-B units scar; base-quad bias bound 8.9e-6 < 1e-5·s_b; GRID-MODE SUSPICION on softest mode (13–14 nodes @ order 16) | stage 2 kinetic metric + cross-order adjudication |

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
  and merges next session (user directive 2026-08-23, supersedes earlier
  distinct-merger practice).**
- Update THIS file (updated timestamp + attempt row + reasoning additions)
  at every milestone; push via memory-status PR so state survives crashes.
- Edit discipline learned twice over in this file: NEVER chain anchored
  edits from remembered line numbers here — re-read, then either one
  content-exact hunk per call or a full-file rewrite.

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
continuation PR: #169 (this file + attempt 0008 artifacts).
