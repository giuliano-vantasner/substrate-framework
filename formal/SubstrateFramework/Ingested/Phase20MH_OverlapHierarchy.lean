import Mathlib

/-!
# Phase 20 MH-L — The overlap hierarchy: a geometric (core-localized) overlap gives a
strictly ordered, orders-of-magnitude generation hierarchy; a flat condensate gives EQUAL
overlaps (no hierarchy)

This file is the Lean oracle's capstone for unified-framework Phase-20 sub-arc MH (the fermion
mass hierarchy from the FG2 family tower via the Yukawa-overlap mechanism), step MH-L. It
machine-checks the DISCRETE STRUCTURAL FACT established (numerically) by MH2 in
`merged-framework/bridges/phase-20/`:

> A generation's mass is the Yukawa overlap `y_n = ∫ η_n² Φ_cond dx` of its bound mode `η_n`
> with the medium condensate. In the RADIAL tower, mode `n` is localized at growing radius
> `r_n = n·d`, and the CORE-localized condensate decays as `exp(−κ·x)`, so the overlap is
> GEOMETRIC: `y_n = y₀ · q^n` with `q = exp(−κ·d) ∈ (0,1)`. A geometric overlap with `q < 1`
> gives a STRICTLY DECREASING, strictly ordered sequence of generation couplings spanning
> orders of magnitude — the hierarchy. The NON-TAUTOLOGY witness: a FLAT / delocalized
> condensate gives `q = 1`, so all overlaps are EQUAL (`y_n = y₀` for all `n`) — NO hierarchy.

The physics this certifies (the OUTPUT, machine-checked here):

* `overlap y0 q n = y0 * q^n` — the geometric overlap model (the radial-tower MH2 result):
  the n-th generation's Yukawa coupling, `y₀` the ground overlap, `q = exp(−κd)` the per-rung
  ratio set by the condensate width `κ` (DERIVED in MH2.3, NOT fitted).
* `hierarchy_strictMono` — the HEADLINE: with a core-localized condensate (`0 < q < 1`) and
  `y₀ > 0`, the overlaps are STRICTLY DECREASING in the generation index: `m < n ⇒ overlap n <
  overlap m`. A genuine strictly ordered hierarchy (each generation strictly lighter coupling
  than the next-deeper one).
* `hierarchy_orders_of_magnitude` — the overlap ratio `overlap 0 / overlap n = q^(−n)` grows
  without bound: for `q < 1` and any bound `B`, some generation `n` has `overlap 0 > B *
  overlap n` — orders of magnitude from the O(1) per-rung ratio.
* `flat_condensate_equal` — the NON-TAUTOLOGY WITNESS / GUARD: a FLAT condensate (`q = 1`)
  gives `overlap n = y₀` for EVERY `n` — all generations have EQUAL overlap, NO hierarchy. So
  `hierarchy_strictMono` is NOT vacuously true of every input: it genuinely needs `q < 1` (the
  condensate's core localization). With `q = 1` the strict ordering FAILS (the witness).
* `capstone` — the combined statement: core-localized (`q<1`) ⇒ strict hierarchy, flat (`q=1`)
  ⇒ equal overlaps, and the two are genuinely different (the strict-mono input is discriminating).

## Physics offered for (the INPUT — ASSERTED here, DERIVED-elsewhere, not proved inside Lean)

- The geometric overlap form `y_n = y₀ q^n` is the MH2 numerical result: a bound mode at radius
  `r_n = n d` overlapped with a condensate decaying as `exp(−κ|x|)` gives `y_n ∝ exp(−κ r_n) =
  exp(−κ d)^n`. The map RADIUS-LADDER × CORE-CONDENSATE ↦ GEOMETRIC OVERLAP is the ASSERTED
  INPUT (MH2.2/MH2.3, scipy, converged N→2N); Lean certifies only the resulting ORDERING /
  RATIO-GROWTH arithmetic of the geometric sequence.
- That `q = exp(−κd) ∈ (0,1)` for a core-localized condensate (`κ > 0`, `d > 0`) and `q = 1`
  for a flat condensate (`κ = 0`) is the ASSERTED physical premise (MH2.5 guard).
- The identification of `y_n` with the physical generation Yukawa coupling / mass (m_n = y_n v,
  v scale-deferred) is MH1's overlap mass formula — ASSERTED INPUT, not proved inside Lean.

## What each theorem PROVES (the OUTPUT, machine-checked here)

The theorems prove exactly their own statements about the geometric sequence `y₀ q^n`: strict
monotonicity for `0<q<1`, unbounded ratio growth, and the flat-case (`q=1`) equality witness.
They do NOT prove that the radial overlap IS geometric, that `q = exp(−κd)`, or that `y_n` is
the physical mass — those are the asserted physical premises (DERIVED in MH1/MH2's SymPy/scipy,
beyond Lean/Mathlib coverage). This EXTENDS the discrete-fact ledger of
`Phase18Chiral_GoldstoneCount.lean` (Goldstone count) and `Phase11Flavor_CPPhaseCount.lean`
(CP-phase count) to the MASS-HIERARCHY sector: the strict geometric ordering is the hierarchy
mechanism's characteristic discrete fact, with a non-tautology witness (flat ⇒ equal, a
different input giving a different, correct behaviour).
Quality bar / style exemplar: `Phase18Chiral_GoldstoneCount.lean`.
-/

namespace Phase20MH

/-- The geometric overlap model (the radial-tower MH2 result): the n-th generation's Yukawa
    overlap is `y₀ · q^n`, with `y₀` the ground overlap and `q = exp(−κd)` the per-rung ratio
    set by the condensate width `κ` (DERIVED in MH2.3). -/
noncomputable def overlap (y0 q : ℝ) (n : ℕ) : ℝ := y0 * q ^ n

/-! ### 1. The HEADLINE: a core-localized condensate (0 < q < 1) ⇒ a strict hierarchy -/

/-- Positivity: with `y₀ > 0` and `q > 0` every generation overlap is positive (a real Yukawa). -/
theorem overlap_pos {y0 q : ℝ} (hy : 0 < y0) (hq : 0 < q) (n : ℕ) : 0 < overlap y0 q n := by
  unfold overlap
  exact mul_pos hy (pow_pos hq n)

/-- HEADLINE: a CORE-LOCALIZED condensate (`0 < q < 1`, i.e. `q = exp(−κd)` with `κ,d > 0`) and
    `y₀ > 0` give STRICTLY DECREASING overlaps: deeper generation index ⇒ strictly smaller
    overlap. `m < n ⇒ overlap n < overlap m` — a genuine strictly ordered generation hierarchy. -/
theorem hierarchy_strictMono {y0 q : ℝ} (hy : 0 < y0) (hq0 : 0 < q) (hq1 : q < 1) :
    ∀ {m n : ℕ}, m < n → overlap y0 q n < overlap y0 q m := by
  intro m n hmn
  unfold overlap
  apply mul_lt_mul_of_pos_left _ hy
  exact pow_lt_pow_right_of_lt_one₀ hq0 hq1 hmn

/-! ### 2. Orders of magnitude: the overlap ratio grows without bound -/

/-- ORDERS OF MAGNITUDE: for a core-localized condensate (`0 < q < 1`) the ground-to-n overlap
    ratio `overlap 0 / overlap n = q^(−n)` exceeds ANY bound `B` for large enough `n`. Concretely:
    for every `B`, there is a generation `n` with `overlap y0 q 0 > B * overlap y0 q n`. The O(1)
    per-rung ratio `q` compounds into an unbounded (orders-of-magnitude) spread across the tower. -/
theorem hierarchy_orders_of_magnitude {y0 q : ℝ} (hy : 0 < y0) (hq0 : 0 < q) (hq1 : q < 1)
    (B : ℝ) : ∃ n : ℕ, overlap y0 q 0 > B * overlap y0 q n := by
  -- overlap y0 q 0 = y0; overlap y0 q n = y0 q^n. Since q^n → 0, B * y0 q^n < y0 eventually.
  -- Use that q^n → 0: ∃ n, q^n < 1/(|B|+1), hence B*y0*q^n ≤ (|B|+1)*y0*q^n < y0.
  obtain ⟨n, hn⟩ := exists_pow_lt_of_lt_one (show (0:ℝ) < 1/(|B|+1) by positivity) hq1
  refine ⟨n, ?_⟩
  unfold overlap
  simp only [pow_zero, mul_one]
  have hqn : 0 < q ^ n := pow_pos hq0 n
  have hB : B ≤ |B| + 1 := le_trans (le_abs_self B) (by linarith)
  calc B * (y0 * q ^ n) ≤ (|B| + 1) * (y0 * q ^ n) := by
        apply mul_le_mul_of_nonneg_right hB (le_of_lt (mul_pos hy hqn))
    _ = (|B| + 1) * y0 * q ^ n := by ring
    _ < (|B| + 1) * y0 * (1/(|B|+1)) := by
        apply mul_lt_mul_of_pos_left hn (by positivity)
    _ = y0 := by field_simp

/-! ### 3. The NON-TAUTOLOGY WITNESS / GUARD: a flat condensate (q = 1) gives EQUAL overlaps -/

/-- GUARD / NON-TAUTOLOGY WITNESS: a FLAT / delocalized condensate (`q = 1`, i.e. `κ = 0`) gives
    `overlap y0 1 n = y₀` for EVERY generation `n` — all overlaps EQUAL, NO hierarchy. This makes
    `hierarchy_strictMono` non-vacuous: with `q = 1` the strict ordering FAILS (the overlaps are
    equal, not strictly decreasing), so the strict hierarchy genuinely requires `q < 1` (the
    condensate's core localization), exactly the MH2.5 flat-condensate rejection guard. -/
theorem flat_condensate_equal (y0 : ℝ) (n : ℕ) : overlap y0 1 n = y0 := by
  unfold overlap; simp

/-- The flat case is NOT a strict hierarchy: with `q = 1`, `overlap y0 1 1 = overlap y0 1 0`
    (the two generations have EQUAL overlap), so the strict inequality `overlap 1 < overlap 0`
    is FALSE — the witness that `hierarchy_strictMono` needs `q < 1`. -/
theorem flat_not_strict (y0 : ℝ) : ¬ (overlap y0 1 1 < overlap y0 1 0) := by
  rw [flat_condensate_equal, flat_condensate_equal]; exact lt_irrefl y0

/-! ### 4. Capstone -/

/-- The complete Phase-20 MH overlap-hierarchy structural statement in one theorem: a
    core-localized condensate (`0 < q < 1`) gives positive, STRICTLY DECREASING overlaps with an
    unbounded (orders-of-magnitude) spread — a genuine generation hierarchy — while a FLAT
    condensate (`q = 1`) gives EQUAL overlaps (no hierarchy). The strict-ordering input is
    discriminating (the flat case is a non-tautology witness). -/
theorem capstone {y0 q : ℝ} (hy : 0 < y0) (hq0 : 0 < q) (hq1 : q < 1) :
    (∀ n : ℕ, 0 < overlap y0 q n) ∧
    (∀ {m n : ℕ}, m < n → overlap y0 q n < overlap y0 q m) ∧
    (∀ B : ℝ, ∃ n : ℕ, overlap y0 q 0 > B * overlap y0 q n) ∧
    (∀ n : ℕ, overlap y0 1 n = y0) ∧
    (¬ (overlap y0 1 1 < overlap y0 1 0)) := by
  refine ⟨overlap_pos hy hq0, ?_, hierarchy_orders_of_magnitude hy hq0 hq1,
          flat_condensate_equal y0, flat_not_strict y0⟩
  intro m n hmn; exact hierarchy_strictMono hy hq0 hq1 hmn

end Phase20MH

#print axioms Phase20MH.overlap_pos
#print axioms Phase20MH.hierarchy_strictMono
#print axioms Phase20MH.hierarchy_orders_of_magnitude
#print axioms Phase20MH.flat_condensate_equal
#print axioms Phase20MH.flat_not_strict
#print axioms Phase20MH.capstone
