/-
Phase condition for resonant power transfer.

Maximum power transfer occurs when δ − δ_br = π/2.
At δ = δ_br (zero phase offset), ⟨P⟩ = 0.

Reference: solution.md §1.3, dynamics/01_collective_coordinates.md.
-/

import Mathlib
namespace SGPhaseCondition

open Real

noncomputable def instantaneousPower (F₀ φ_t₀ w δ δ_br t : ℝ) : ℝ :=
  -(φ_t₀ * Real.cos (w * t + δ_br)) * (F₀ * Real.sin (w * t + δ))

def phaseCondition (δ δ_br : ℝ) : Prop :=
  δ = δ_br + π/2

theorem optimal_phase_satisfies_condition (δ_br : ℝ) :
    phaseCondition (δ_br + π/2) δ_br := rfl

theorem instantaneousPower_optimal (F₀ φ_t₀ w δ_br t : ℝ) :
    instantaneousPower F₀ φ_t₀ w (δ_br + π/2) δ_br t
    = -(φ_t₀ * F₀ / 2) * (1 + Real.cos (2 * w * t + 2 * δ_br)) := by
  set θ := w * t + δ_br
  dsimp [instantaneousPower]
  have hsin : Real.sin (θ + π/2) = Real.cos θ := Real.sin_add_pi_div_two θ
  have hcos2 : Real.cos θ ^ 2 = (1 + Real.cos (2 * θ)) / 2 := by
    linarith [Real.cos_two_mul θ]
  calc
    -(φ_t₀ * Real.cos (w * t + δ_br)) * (F₀ * Real.sin (w * t + (δ_br + π/2)))
        = -(φ_t₀ * Real.cos θ) * (F₀ * Real.sin (θ + π/2)) := by
          dsimp [θ]; ring
    _ = -(φ_t₀ * Real.cos θ) * (F₀ * Real.cos θ) := by rw [hsin]
    _ = -(φ_t₀ * F₀) * (Real.cos θ ^ 2) := by ring
    _ = -(φ_t₀ * F₀) * ((1 + Real.cos (2 * θ)) / 2) := by rw [hcos2]
    _ = -(φ_t₀ * F₀ / 2) * (1 + Real.cos (2 * θ)) := by ring
    _ = -(φ_t₀ * F₀ / 2) * (1 + Real.cos (2 * w * t + 2 * δ_br)) := by
      dsimp [θ]; ring

theorem phaseCondition_zero_offset_not_optimal (δ_br : ℝ) :
    ¬ phaseCondition δ_br δ_br := by
  dsimp [phaseCondition]
  nlinarith [pi_pos]

theorem power_bounded_by_amplitudes (F₀ φ_t₀ w δ δ_br t : ℝ) :
    |instantaneousPower F₀ φ_t₀ w δ δ_br t| ≤ |φ_t₀| * |F₀| := by
  dsimp [instantaneousPower]
  rw [abs_mul, abs_mul, abs_neg, abs_mul]
  -- Goal: |φ_t₀| * |cos| * (|F₀| * |sin|) ≤ |φ_t₀| * |F₀|
  have hcos : |Real.cos (w * t + δ_br)| ≤ 1 := abs_cos_le_one _
  have hsin : |Real.sin (w * t + δ)| ≤ 1 := abs_sin_le_one _
  have ha : 0 ≤ |φ_t₀| := abs_nonneg _
  have hb : 0 ≤ |F₀| := abs_nonneg _
  have hs : 0 ≤ |Real.sin (w * t + δ)| := abs_nonneg _
  have hprod : |Real.cos (w * t + δ_br)| * |Real.sin (w * t + δ)| ≤ 1 :=
    calc
      |Real.cos (w * t + δ_br)| * |Real.sin (w * t + δ)|
          ≤ 1 * |Real.sin (w * t + δ)| := mul_le_mul_of_nonneg_right hcos hs
      _ ≤ 1 * 1 := mul_le_mul_of_nonneg_left hsin (by norm_num)
      _ = 1 := by norm_num
  calc
    |φ_t₀| * |Real.cos (w * t + δ_br)| * (|F₀| * |Real.sin (w * t + δ)|)
        = (|φ_t₀| * |F₀|) * (|Real.cos (w * t + δ_br)| * |Real.sin (w * t + δ)|) := by ring
    _ ≤ (|φ_t₀| * |F₀|) * 1 := mul_le_mul_of_nonneg_left hprod (mul_nonneg ha hb)
    _ = |φ_t₀| * |F₀| := mul_one _
end SGPhaseCondition
