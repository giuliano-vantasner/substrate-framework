/-
Basin theorem: the basin of outcome (c) — where exactly one breather
constituent is ionized — has non-zero measure in impact-condition space.

STATUS UPDATE (2026-06-16 — PROVED):
`basin_positive_measure` is now proved via IVT + continuity + strict
monotonicity of lzProbPhase on [0, π/2).  The proof constructs:
1. A point x₀ with f(x₀) = P_min² < P_min (using IVT on cos and
   the algebraic relation between exp, log, and P_min).
2. A point δ with f(δ) = P_min (IVT on f between 0 and x₀).
3. Either the symmetric interval (−δ, δ) works (if f(0) < P_max),
   or a subinterval (δ₂, δ) where f(δ₂) = P_max works (if f(0) ≥ P_max).

Requires the additional hypothesis hPmin_lt_Pmax (P_min < P_max) which
is physically necessary since the basin is defined by a nontrivial
probability window (P_min, P_max).

This file is self-contained (duplicates `landauZenerProb` from
LandauZener.lean for compilation independence).
-/

import Mathlib
namespace SGBasin

open Real
open Set

/--
Landau–Zener diabatic transition probability (duplicated from LandauZener.lean
for self-contained compilation).
-/
noncomputable def landauZenerProb (Δ v : ℝ) : ℝ :=
  Real.exp (-((π * Δ ^ 2) / (2 * |v|)))

/--
The effective sweep rate depends on the relative phase Δ = φ_int − ϕ.
For the centred-impact approximation:
  v_sweep(Δ) = v₀ · |cos(Δ)|,
where v₀ = 8 g ψ₀ η w captures the maximal sweep rate.
-/
noncomputable def sweepRatePhase (v₀ : ℝ) (Δ : ℝ) : ℝ := v₀ * |cos Δ|

/--
The LZ probability as a function of the relative phase Δ:
  P_LZ(Δ) = exp(−π · (Δ_min²/(2ℏ)) / (v₀ · |cos Δ|)).

In terms of the dimensionless decay parameter Γ₀ = Δ_min²/(2ℏ v₀):
  P_LZ(Δ) = exp(−π Γ₀ / |cos Δ|).
-/
noncomputable def lzProbPhase (Γ₀ : ℝ) (Δ : ℝ) : ℝ :=
  Real.exp (-π * Γ₀ / |cos Δ|)

/-
Theorem (basin_single_point_exists):
Given Γ₀ > 0 sufficiently small that exp(−π Γ₀) > P_min
for some P_min < 1, there exists at least one phase Δ
(mainly Δ = 0) where P_min < P_LZ(Δ).

This proves the basin of outcome (c) is NONEMPTY — it contains
at least the point Δ = 0.  It does NOT prove μ(basin_c) > 0.

The measure-theoretic claim requires showing that the set
  {Δ : P_min < P_LZ(Δ) < P_max}
has positive Lebesgue measure.  This follows from continuity of
P_LZ(Δ) on (−π/2, π/2) and the intermediate value theorem, plus
the fact that P_LZ(Δ) → 0 as |cos Δ| → 0 (at the poles Δ → ±π/2).
Thus for sufficiently small Γ₀, the preimage of (P_min, exp(−π Γ₀))
is a nonempty open set, hence has positive measure.

The analytical proof is in ../dynamics/04_basin.md.
-/
theorem basin_single_point_exists (Γ₀ P_min : ℝ) (hΓ₀ : 0 < Γ₀) (hP : P_min < Real.exp (-(π * Γ₀))) :
    ∃ Δ : ℝ, P_min < lzProbPhase Γ₀ Δ := by
  have hexp_lt_one : Real.exp (-(π * Γ₀)) < 1 := by
    have hpos : 0 < π * Γ₀ := by
      have hπ : 0 < π := Real.pi_pos; nlinarith
    rw [Real.exp_lt_one_iff]
    linarith
  -- P_LZ(0) = exp(−π Γ₀) > P_min, so Δ = 0 satisfies the condition.
  -- This shows existence of at least ONE point in the basin,
  -- but does NOT prove the basin has positive measure.
  use 0
  dsimp [lzProbPhase]
  have hcos0 : cos (0 : ℝ) = 1 := Real.cos_zero
  simp [hcos0]
  exact hP

/--
The basin of outcome (c) has positive Lebesgue measure.

Formally: there exists an open interval (a,b) of positive length
such that for all Δ ∈ (a,b), P_min < P_LZ(Δ) < P_max, with
0 < P_min < P_max < 1.

Proof uses the intermediate value theorem, continuity of lzProbPhase on
(−π/2, π/2) where cos Δ > 0, and strict monotonicity derived from the
monotonicity of cos on [0, π/2].

We require P_min < P_max (hPmin_lt_Pmax) since otherwise the interval
(P_min, P_max) would be empty and no Δ could satisfy both bounds.
-/
theorem basin_positive_measure (Γ₀ P_min P_max : ℝ) (hΓ₀ : 0 < Γ₀) (hPmin : 0 < P_min)
    (hPmax : P_max < 1) (hPmin_lt : P_min < Real.exp (-(π * Γ₀)))
    (hPmin_lt_Pmax : P_min < P_max) :
    ∃ (a b : ℝ), a < b ∧ (∀ Δ : ℝ, a < Δ → Δ < b → P_min < lzProbPhase Γ₀ Δ ∧ lzProbPhase Γ₀ Δ < P_max) := by
  set f := lzProbPhase Γ₀ with hf
  -- f(0) = exp(−π Γ₀)
  have hf0 : f 0 = Real.exp (-(π * Γ₀)) := by
    dsimp [f, lzProbPhase]; simp [Real.cos_zero]
  -- f(Δ) = f(|Δ|) since |cos Δ| = |cos|Δ||
  have hf_abs (Δ : ℝ) : f Δ = f |Δ| := by
    dsimp [f, lzProbPhase]
    have hcos : cos |Δ| = cos Δ := by
      rcases em (0 ≤ Δ) with (h | h)
      · rw [abs_of_nonneg h]
      · rw [abs_of_neg (by linarith : Δ < 0), Real.cos_neg]
    simp [hcos]
  -- sign facts
  have hπΓ₀_pos : 0 < π * Γ₀ := by
    have hπ : 0 < π := Real.pi_pos; nlinarith
  have hπΓ₀_neg : -(π * Γ₀) < 0 := by linarith
  have hPmin_lt_one : P_min < 1 := by
    have h : Real.exp (-(π * Γ₀)) < 1 := Real.exp_lt_one_iff.mpr hπΓ₀_neg
    linarith
  have hlog_neg : Real.log P_min < 0 := Real.log_neg hPmin hPmin_lt_one
  have hlog_lt : Real.log P_min < -(π * Γ₀) := by
    rw [Real.log_lt_iff_lt_exp hPmin]; exact hPmin_lt
  -- f is strictly decreasing on [0, π/2)
  have hf_strictMono {a b : ℝ} (ha : 0 ≤ a) (hab : a < b) (hb : b < π/2) : f b < f a := by
    have hcos_lt : cos b < cos a :=
      Real.cos_lt_cos_of_nonneg_of_le_pi_div_two ha (by linarith) hab
    have hpos_a : 0 < cos a := Real.cos_pos_of_mem_Ioo ⟨by linarith, by linarith⟩
    have hpos_b : 0 < cos b := Real.cos_pos_of_mem_Ioo ⟨by linarith, by linarith⟩
    dsimp [f, lzProbPhase]
    rw [abs_of_pos hpos_a, abs_of_pos hpos_b]
    -- exp(−πΓ₀ / cos b) < exp(−πΓ₀ / cos a)  ↔  −πΓ₀/cos b < −πΓ₀/cos a
    -- Since −πΓ₀ < 0, this is equivalent to 1/cos a < 1/cos b ↔ cos b < cos a
    refine Real.exp_lt_exp.mpr ?_
    have h_inv : (cos a)⁻¹ < (cos b)⁻¹ :=
      by simpa using (one_div_lt_one_div hpos_a hpos_b).mpr hcos_lt
    have h_mul : (-(π * Γ₀)) * (cos b)⁻¹ < (-(π * Γ₀)) * (cos a)⁻¹ := by
      nlinarith
    simpa [div_eq_mul_inv] using h_mul
  -- find x₀ ∈ (0, π/2) with f(x₀) = P_min² < P_min
  set η := -(π * Γ₀) / Real.log P_min with hη
  have hη_pos : 0 < η := div_pos_of_neg_of_neg hπΓ₀_neg hlog_neg
  have hη_lt_one : η < 1 := by
    dsimp [η]; rw [div_lt_one_of_neg hlog_neg]; exact hlog_lt
  set ε := η / 2 with hε
  have hε_pos : 0 < ε := by linarith
  have hε_lt_one : ε < 1 := by linarith
  -- cos is continuous on [0, π/2]; ε ∈ (cos(π/2), cos(0)) = (0, 1)
  have h0_le_pi2 : (0 : ℝ) ≤ π/2 := by nlinarith [Real.pi_pos]
  have hcos_contOn : ContinuousOn cos (Icc (0 : ℝ) (π/2)) :=
    Real.continuous_cos.continuousOn
  have hx₀_img : ε ∈ cos '' Icc (0 : ℝ) (π/2) :=
    (intermediate_value_Icc' h0_le_pi2 hcos_contOn)
      (by rw [Real.cos_pi_div_two, Real.cos_zero]; exact ⟨by linarith, by linarith⟩)
  rcases hx₀_img with ⟨x₀, hx₀, hx₀cos⟩
  rcases hx₀ with ⟨hx₀_low, hx₀_high⟩
  have hx₀_pos : 0 < x₀ := by
    by_contra! H; have : x₀ = 0 := by linarith
    rw [this, Real.cos_zero] at hx₀cos; linarith
  have hx₀_lt_pi2 : x₀ < π/2 := by
    by_contra! H
    have hle : cos x₀ ≤ cos (π/2) :=
      Real.cos_le_cos_of_nonneg_of_le_pi (by nlinarith [Real.pi_pos]) (by
        have : x₀ ≤ π := hx₀_high.trans (by nlinarith [Real.pi_pos])
        exact this) H
    rw [Real.cos_pi_div_two] at hle; linarith
  have hcos_x₀_pos : 0 < cos x₀ := by rw [hx₀cos]; exact hε_pos
  -- compute f(x₀) = P_min²
  have hfx₀_sq : f x₀ = P_min ^ 2 := by
    dsimp [f, lzProbPhase]
    rw [abs_of_pos hcos_x₀_pos, hx₀cos]
    dsimp [ε, η]
    have hlog_ne_zero : Real.log P_min ≠ 0 := by linarith
    have hnum_ne_zero : -(π * Γ₀) ≠ 0 := by linarith
    field_simp [hlog_ne_zero, hnum_ne_zero]
    rw [mul_comm, show (2 : ℝ) * Real.log P_min = Real.log P_min + Real.log P_min by ring]
    rw [Real.exp_add, Real.exp_log hPmin]
    ring
  have hfx₀_lt_Pmin : f x₀ < P_min := by
    rw [hfx₀_sq]; nlinarith
  -- continuity of f on [0, x₀]
  have hcos_pos_on_int : ∀ x ∈ Icc (0 : ℝ) x₀, 0 < cos x := by
    intro x hx; rcases hx with ⟨hx0, hxx₀⟩
    exact Real.cos_pos_of_mem_Ioo ⟨by linarith, by linarith⟩
  have h_f_contOn : ContinuousOn f (Icc (0 : ℝ) x₀) := by
    dsimp [f, lzProbPhase]
    have hnum : ContinuousOn (λ _ : ℝ => (-π) * Γ₀) (Icc (0 : ℝ) x₀) :=
      continuous_const.continuousOn
    have hden : ContinuousOn (λ x : ℝ => |cos x|) (Icc (0 : ℝ) x₀) :=
      (Continuous.abs Real.continuous_cos).continuousOn
    have hden_ne_zero : ∀ x ∈ Icc (0 : ℝ) x₀, |cos x| ≠ 0 := by
      intro x hx; rw [abs_of_pos (hcos_pos_on_int x hx)]; exact ne_of_gt (hcos_pos_on_int x hx)
    have hdiv : ContinuousOn (λ x : ℝ => (-π) * Γ₀ / |cos x|) (Icc (0 : ℝ) x₀) :=
      ContinuousOn.div hnum hden hden_ne_zero
    refine ContinuousOn.comp (Real.continuous_exp.continuousOn (s := Set.univ)) hdiv ?_
    intro x _; exact Set.mem_univ _
  -- IVT: find δ ∈ (0, x₀) with f(δ) = P_min
  have hPmin_mem : P_min ∈ Icc (f x₀) (f 0) := by
    rw [hf0, hfx₀_sq]; exact ⟨by nlinarith, hPmin_lt.le⟩
  have hδ_img : P_min ∈ f '' Icc (0 : ℝ) x₀ :=
    (intermediate_value_Icc' (by linarith) h_f_contOn) hPmin_mem
  rcases hδ_img with ⟨δ, hδ_mem, hδval⟩
  rcases hδ_mem with ⟨hδ_low, hδ_high⟩
  have hδ_pos : 0 < δ := by
    by_contra! H; have : δ = 0 := by linarith
    rw [this, hf0] at hδval; linarith
  have hδ_lt_x₀ : δ < x₀ := by
    by_contra! H
    have h_eq : δ = x₀ := by linarith
    rw [h_eq, hfx₀_sq] at hδval; nlinarith
  -- CASE SPLIT: f(0) < P_max vs f(0) ≥ P_max
  by_cases h_exp_lt_Pmax : Real.exp (-(π * Γ₀)) < P_max
  · -- Case 1: f(0) < P_max.  Take symmetric interval (−δ, δ).
    refine ⟨-δ, δ, by linarith, λ Δ hlow hhigh => ?_⟩
    have habs_lt_δ : |Δ| < δ := abs_lt.mpr ⟨by linarith, by linarith⟩
    have habs_nonneg : 0 ≤ |Δ| := abs_nonneg Δ
    -- lower bound: P_min < f(|Δ|)
    have hlower : P_min < f |Δ| := by
      rcases eq_or_lt_of_le habs_nonneg with (hzero | hpos)
      · rw [hzero.symm, hf0]; exact hPmin_lt
      · have : f δ < f |Δ| :=
          hf_strictMono habs_nonneg habs_lt_δ (by linarith)
        rw [hδval] at this; exact this
    -- upper bound: f(|Δ|) < P_max
    have hupper : f |Δ| < P_max := by
      rcases eq_or_lt_of_le habs_nonneg with (hzero | hpos)
      · rw [hzero.symm, hf0]; exact h_exp_lt_Pmax
      · have : f |Δ| < f 0 :=
          hf_strictMono (by norm_num) hpos (by linarith)
        rw [hf0] at this; linarith
    rw [hf_abs Δ]; exact ⟨hlower, hupper⟩
  · -- Case 2: f(0) ≥ P_max.  Find δ₂ ∈ [0, δ] with f(δ₂) = P_max.
    have hf0_ge_Pmax : P_max ≤ f 0 := by linarith
    have hPmax_mem : P_max ∈ Icc (f δ) (f 0) := by
      rw [hf0] at hf0_ge_Pmax
      rw [hδval, hf0]
      exact ⟨hPmin_lt_Pmax.le, hf0_ge_Pmax⟩
    have h_f_contOn_δ : ContinuousOn f (Icc (0 : ℝ) δ) :=
      h_f_contOn.mono (λ x hx => ⟨hx.1, hx.2.trans hδ_high⟩)
    have hδ₂_img : P_max ∈ f '' Icc (0 : ℝ) δ :=
      (intermediate_value_Icc' (by linarith) h_f_contOn_δ) hPmax_mem
    rcases hδ₂_img with ⟨δ₂, hδ₂_mem, hδ₂val⟩
    rcases hδ₂_mem with ⟨hδ₂_low, hδ₂_high⟩
    -- δ₂ < δ strictly (since f(δ) = P_min < P_max = f(δ₂))
    have hδ₂_lt_δ : δ₂ < δ := by
      by_contra! H; have heq : δ₂ = δ := by linarith
      rw [heq, hδval] at hδ₂val; linarith
    refine ⟨δ₂, δ, hδ₂_lt_δ, λ Δ hδ₂_lt h_lt_δ => ?_⟩
    have hΔ_nonneg : 0 ≤ Δ := by linarith
    have hΔ_lt_pi2 : Δ < π/2 := by linarith
    -- lower bound: P_min = f(δ) < f(Δ) (strict monotonicity)
    have hlower : P_min < f Δ := by
      have : f δ < f Δ := hf_strictMono hΔ_nonneg h_lt_δ (by linarith)
      rw [hδval] at this; exact this
    -- upper bound: f(Δ) < f(δ₂) = P_max
    have hupper : f Δ < P_max := by
      have : f Δ < f δ₂ := hf_strictMono hδ₂_low hδ₂_lt hΔ_lt_pi2
      rw [hδ₂val] at this; exact this
    exact ⟨hlower, hupper⟩

end SGBasin
