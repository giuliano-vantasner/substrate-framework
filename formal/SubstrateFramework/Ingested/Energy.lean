/-
Energy definitions and inequalities for sine‑Gordon breather ionisation.
Units: m=1, β set so E_kink = 8.
-/
import Mathlib
namespace SGEnergy


open Real

/-- Breather internal energy: E_breather(w) = 16 √(1 − w²). -/
noncomputable def E_breather (w : ℝ) : ℝ := 16 * Real.sqrt (1 - w ^ 2)

/-- Rest energy of a single sine‑Gordon kink. -/
def E_kink : ℝ := 8

/-- Two‑kink threshold energy = 16. -/
def E_pair : ℝ := E_kink + E_kink

/-- Binding‑energy gap: ΔE(w) = 16 (1 − √(1−w²)). -/
noncomputable def ΔE_binding (w : ℝ) : ℝ := 16 * (1 - Real.sqrt (1 - w ^ 2))

theorem binding_gap_nonneg {w : ℝ} (hw : -1 ≤ w) (hw' : w ≤ 1) : 0 ≤ ΔE_binding w := by
  dsimp [ΔE_binding]
  have h_nonneg_sub : 0 ≤ 1 - w ^ 2 := by nlinarith
  have hsub_le_one : 1 - w ^ 2 ≤ 1 := by nlinarith
  have hsqrt : Real.sqrt (1 - w ^ 2) ≤ 1 := by
    calc
      Real.sqrt (1 - w ^ 2) ≤ Real.sqrt 1 := Real.sqrt_le_sqrt hsub_le_one
      _ = 1 := by norm_num
  nlinarith

theorem breather_plus_gap_eq_pair (w : ℝ) : E_breather w + ΔE_binding w = E_pair := by
  dsimp [E_breather, ΔE_binding, E_pair, E_kink]
  ring

theorem binding_gap_pos {w : ℝ} (hw_pos : 0 < w) (hw_lt_one : w < 1) : 0 < ΔE_binding w := by
  have hsq_pos : 0 < w ^ 2 := by nlinarith
  have hsq_lt_one : w ^ 2 < 1 := by nlinarith
  have hpos_sub : 0 < 1 - w ^ 2 := by nlinarith
  have hsqrt_lt_one : Real.sqrt (1 - w ^ 2) < 1 := by
    have h_lt : 1 - w ^ 2 < 1 := by nlinarith
    have h := Real.sqrt_lt_sqrt hpos_sub.le h_lt
    simpa [Real.sqrt_one] using h
  dsimp [ΔE_binding]
  nlinarith

theorem E_breather_le_pair {w : ℝ} (hw : -1 ≤ w) (hw' : w ≤ 1) : E_breather w ≤ E_pair := by
  dsimp [E_breather, E_pair, E_kink]
  have h_nonneg_sub : 0 ≤ 1 - w ^ 2 := by nlinarith
  have hsub_le_one : 1 - w ^ 2 ≤ 1 := by nlinarith
  have hsqrt : Real.sqrt (1 - w ^ 2) ≤ 1 := by
    calc
      Real.sqrt (1 - w ^ 2) ≤ Real.sqrt 1 := Real.sqrt_le_sqrt hsub_le_one
      _ = 1 := by norm_num
  nlinarith

theorem E_breather_pos_lt_pair {w : ℝ} (hw : 0 < w) (hw' : w < 1) :
    0 < E_breather w ∧ E_breather w < E_pair := by
  have hsq_pos : 0 < 1 - w ^ 2 := by nlinarith
  have hsqrt_pos : 0 < Real.sqrt (1 - w ^ 2) := Real.sqrt_pos.mpr hsq_pos
  have hsqrt_lt_one : Real.sqrt (1 - w ^ 2) < 1 := by
    have hx : 0 ≤ 1 - w ^ 2 := by nlinarith
    have hsub_lt_one : 1 - w ^ 2 < 1 := by nlinarith
    have h := Real.sqrt_lt_sqrt hx hsub_lt_one
    simpa [Real.sqrt_one] using h
  dsimp [E_breather, E_pair, E_kink]
  constructor
  · nlinarith
  · nlinarith

end SGEnergy
