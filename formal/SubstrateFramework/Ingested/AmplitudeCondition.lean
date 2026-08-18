/- Amplitude condition for ionization. -/
import Mathlib
namespace SGAmplitudeCondition

open Real

noncomputable def driveEnergyDelivered (χ η v F₀ : ℝ) : ℝ :=
  (π * (χ ^ 2) * (F₀ ^ 2)) / (2 * η * v)

def amplitudeCondition (ΔE χ η v F₀ : ℝ) : Prop :=
  driveEnergyDelivered χ η v F₀ ≥ ΔE

theorem amplitudeCondition_feasible (ΔE χ η v : ℝ)
    (hΔE : 0 < ΔE) (hη : 0 < η) (hv : 0 < v) (hχ : χ ≠ 0) :
    ∃ F₀ : ℝ, amplitudeCondition ΔE χ η v F₀ := by
  have hχ_sq : 0 < χ ^ 2 := sq_pos_iff.mpr hχ
  have hπχ : 0 < π * χ ^ 2 := by positivity
  have hden : 0 < 2 * η * v := by positivity
  let F₀ : ℝ := Real.sqrt ((2 * ΔE * η * v) / (π * χ ^ 2) + 1)
  use F₀
  dsimp [F₀, amplitudeCondition, driveEnergyDelivered]
  have hsq : (Real.sqrt ((2 * ΔE * η * v) / (π * χ ^ 2) + 1)) ^ 2
           = (2 * ΔE * η * v) / (π * χ ^ 2) + 1 :=
    Real.sq_sqrt (by positivity)
  rw [hsq]
  field_simp [hπχ.ne', hden.ne']
  nlinarith
end SGAmplitudeCondition
