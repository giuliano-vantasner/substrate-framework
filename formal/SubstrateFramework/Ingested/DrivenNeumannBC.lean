/-
Driven Neumann boundary condition at x=0.

The non-integrable boundary that replaces the elastic (Neumann φ_x=0
or Dirichlet φ=0) wall and makes breather ionization possible:

  φ_x(0,t) = F₀ · sin(w · t + δ).

Reference: solution.md §1.3, dynamics/01_collective_coordinates.md.
-/

import Mathlib
namespace SGDrivenNeumannBC

open Real

noncomputable def drivenNeumannBC (F₀ w δ t : ℝ) : ℝ :=
  F₀ * Real.sin (w * t + δ)

theorem drivenNeumannBC_periodic (F₀ w δ t : ℝ) (hw : w ≠ 0) :
    drivenNeumannBC F₀ w δ (t + 2 * π / w) = drivenNeumannBC F₀ w δ t := by
  dsimp [drivenNeumannBC]
  have harg : w * (t + 2 * π / w) + δ = (w * t + δ) + 2 * π := by
    field_simp [hw]
    ring
  rw [harg]
  rw [Real.sin_add]
  simp [Real.sin_two_pi, Real.cos_two_pi]

theorem drivenNeumannBC_elastic_wall (w δ t : ℝ) :
    drivenNeumannBC 0 w δ t = 0 := by
  simp [drivenNeumannBC]

theorem drivenNeumannBC_bound (F₀ w δ t : ℝ) :
    |drivenNeumannBC F₀ w δ t| ≤ |F₀| := by
  dsimp [drivenNeumannBC]
  rw [abs_mul]
  have hsin : |Real.sin (w * t + δ)| ≤ 1 := abs_sin_le_one _
  have hnonneg : 0 ≤ |F₀| := abs_nonneg _
  calc
    |F₀| * |Real.sin (w * t + δ)| ≤ |F₀| * 1 :=
      mul_le_mul_of_nonneg_left hsin hnonneg
    _ = |F₀| := mul_one _
end SGDrivenNeumannBC
