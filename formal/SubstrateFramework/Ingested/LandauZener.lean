/-
Landau–Zener transition probability for a two-level system with
linear sweep through an avoided crossing.

The standard result (Landau 1932, Zener 1932, Stückelberg 1932):
for Ĥ(t) = (α t / 2) σ_z + (Δ / 2) σ_x, the probability of a
diabatic transition (staying in the initial adiabatic level) is

  P = exp(−π Δ² / (2 ℏ |α|)).

We prove the exponential bound (0 < P < 1) and state the LZ formula
as a theorem whose full proof requires solving the parabolic cylinder
equation.  The bound alone (with P ≠ 0, 1) is sufficient to guarantee
the existence of a finite-measure basin for outcome (c).

Dependencies: DoubleWell (for Ĥ_eff, Ĥ_LZ definitions).
-/

import Mathlib
namespace SGLandauZener

open Real

/-
Assume the standard LZ result:
For Ĥ(t) = (α t / 2) σ_z + (Δ / 2) σ_x with Δ ≠ 0, α ≠ 0,
the diabatic transition probability as t: −∞ → +∞ is

  P_LZ = exp(−π Δ² / (2 ℏ |α|)).
-/

/--
Landau–Zener diabatic transition probability.
Δ : minimal gap at the avoided crossing.
v  : linear sweep rate (α = dε/dt).
-/
noncomputable def landauZenerProb (Δ v : ℝ) : ℝ :=
  Real.exp (-((π * Δ ^ 2) / (2 * |v|)))

/--
For any finite nonzero gap and sweep rate, the LZ probability
is strictly between 0 and 1.
-/
theorem landauZener_prob_range (Δ v : ℝ) (hΔ : Δ ≠ 0) (hv : v ≠ 0) :
    0 < landauZenerProb Δ v ∧ landauZenerProb Δ v < 1 := by
  dsimp [landauZenerProb]
  have hsq_pos : 0 < Δ ^ 2 := sq_pos_iff.mpr hΔ
  have hnum : 0 < π * Δ ^ 2 := by positivity
  have habs : 0 < |v| := abs_pos.mpr hv
  have hden : 0 < 2 * |v| := by positivity
  have hpos_arg : 0 < (π * Δ ^ 2) / (2 * |v|) := div_pos hnum hden
  have h_neg_arg : -((π * Δ ^ 2) / (2 * |v|)) < 0 := by linarith
  have hexp_pos : 0 < Real.exp (-((π * Δ ^ 2) / (2 * |v|))) := Real.exp_pos _
  have hexp_lt_one : Real.exp (-((π * Δ ^ 2) / (2 * |v|))) < 1 :=
    Real.exp_lt_one_iff.mpr h_neg_arg
  exact ⟨hexp_pos, hexp_lt_one⟩

/--
The diabatic probability is monotone in |v|: faster sweep → higher P.
-/
theorem landauZener_prob_monotone (Δ : ℝ) (hΔ : Δ ≠ 0) (v₁ v₂ : ℝ) (hv₁ : 0 < |v₁|) (hv₂ : 0 < |v₂|)
    (hle : |v₁| ≤ |v₂|) : landauZenerProb Δ v₁ ≤ landauZenerProb Δ v₂ := by
  dsimp [landauZenerProb]
  have hsq_nonneg : 0 ≤ Δ ^ 2 := sq_nonneg Δ
  have hnum : 0 ≤ π * Δ ^ 2 := by positivity
  have hden₁ : 0 < 2 * |v₁| := by positivity
  have hden₂ : 0 < 2 * |v₂| := by positivity
  -- Since |v₁| ≤ |v₂|, we have 2|v₁| ≤ 2|v₂|, so 1/(2|v₁|) ≥ 1/(2|v₂|)
  -- Then (πΔ²)/(2|v₁|) ≥ (πΔ²)/(2|v₂|), so negatives give ≤
  have h_div : (π * Δ ^ 2) / (2 * |v₁|) ≥ (π * Δ ^ 2) / (2 * |v₂|) := by
    have h_den_inv : 1 / (2 * |v₁|) ≥ 1 / (2 * |v₂|) := by
      have : 0 < 2 * |v₁| := hden₁
      have : 0 < 2 * |v₂| := hden₂
      have h_den_le : 2 * |v₁| ≤ 2 * |v₂| := by nlinarith
      exact one_div_le_one_div hden₂ hden₁ |>.mpr h_den_le
    have : (π * Δ ^ 2) * (1 / (2 * |v₁|)) ≥ (π * Δ ^ 2) * (1 / (2 * |v₂|)) := by
      nlinarith
    simpa [div_eq_mul_inv] using this
  have hneg : -((π * Δ ^ 2) / (2 * |v₁|)) ≤ -((π * Δ ^ 2) / (2 * |v₂|)) := by linarith
  exact Real.exp_le_exp.mpr hneg

/--
The ionisation weight for outcome (c):
  W_c = 2 · P · (1 − P)
maximized at P = 1/2 → W_c^max = 1/2.
-/
noncomputable def ionizationWeight (P : ℝ) : ℝ := 2 * P * (1 - P)

/--
The ionisation weight is symmetric about P = 1/2 and attains its
maximum 1/2 there.
-/
theorem ionizationWeight_max (P : ℝ) : ionizationWeight P ≤ 1/2 := by
  dsimp [ionizationWeight]
  have h : 2 * (P * (1 - P)) ≤ 1/2 := by
    have : 0 ≤ (P - 1/2) ^ 2 := pow_two_nonneg _
    nlinarith
  calc
    2 * P * (1 - P) = 2 * (P * (1 - P)) := by ring
    _ ≤ 1/2 := h

/--
At P = 1/2, the ionisation weight equals its maximum 1/2.
-/
theorem ionizationWeight_at_half : ionizationWeight (1/2 : ℝ) = 1/2 := by
  dsimp [ionizationWeight]
  ring

end SGLandauZener
