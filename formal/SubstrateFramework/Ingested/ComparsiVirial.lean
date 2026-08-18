import Mathlib

/-!
Finite algebraic certificates used by the exact virial proof for Federico Comparsi's PDE.

The PDE differentiation and integration-by-parts identities are checked symbolically in
`derivation/verify_exact_structure.py`. This file proves the finite implications after those
identities:

1. a positive period, positive wave speed, and vanishing period-integrated virial force the total
   nonnegative density to vanish;
2. an affine total density nonnegative for all real times has zero slope;
3. a sum of four real squares that vanishes has all four entries zero;
4. the time-symmetric rms-radius law doubles the radius at one light-crossing time.
-/

namespace ComparsiVirial

theorem periodic_virial_forces_zero
    (c T M : ℝ)
    (hc : 0 < c)
    (hT : 0 < T)
    (hvirial : 6 * c ^ 2 * M * T = 0) :
    M = 0 := by
  have hc2 : 0 < c ^ 2 := sq_pos_of_pos hc
  rcases mul_eq_zero.mp hvirial with hcore | hT0
  · rcases mul_eq_zero.mp hcore with hcoefficient | hM
    · have hpositive : 0 < 6 * c ^ 2 := mul_pos (by norm_num) hc2
      exact (ne_of_gt hpositive hcoefficient).elim
    · exact hM
  · exact (ne_of_gt hT hT0).elim

theorem four_squares_zero
    (a b d e : ℝ)
    (h : a ^ 2 + b ^ 2 + d ^ 2 + e ^ 2 = 0) :
    a = 0 ∧ b = 0 ∧ d = 0 ∧ e = 0 := by
  have ha : a = 0 := by
    nlinarith [sq_nonneg a, sq_nonneg b, sq_nonneg d, sq_nonneg e]
  have hb : b = 0 := by
    nlinarith [sq_nonneg a, sq_nonneg b, sq_nonneg d, sq_nonneg e]
  have hd : d = 0 := by
    nlinarith [sq_nonneg a, sq_nonneg b, sq_nonneg d, sq_nonneg e]
  have he : e = 0 := by
    nlinarith [sq_nonneg a, sq_nonneg b, sq_nonneg d, sq_nonneg e]
  exact ⟨ha, hb, hd, he⟩

theorem globally_nonnegative_affine_has_zero_slope
    (M₀ M₁ : ℝ)
    (hglobal : ∀ t : ℝ, 0 ≤ M₀ + M₁ * t) :
    M₁ = 0 := by
  by_contra hM₁
  have hvalue := hglobal (-(M₀ + 1) / M₁)
  have hid : M₀ + M₁ * (-(M₀ + 1) / M₁) = -1 := by
    field_simp [hM₁]
    ring
  rw [hid] at hvalue
  norm_num at hvalue

theorem one_crossing_time_doubles_rms_squared
    (c R₀ : ℝ)
    (hc : c ≠ 0) :
    R₀ ^ 2 + 3 * c ^ 2 * (R₀ / c) ^ 2 = 4 * R₀ ^ 2 := by
  field_simp [hc]
  ring

#print axioms periodic_virial_forces_zero
#print axioms four_squares_zero
#print axioms globally_nonnegative_affine_has_zero_slope
#print axioms one_crossing_time_doubles_rms_squared

end ComparsiVirial
