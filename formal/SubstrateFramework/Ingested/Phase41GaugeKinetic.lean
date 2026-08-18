import Mathlib

/-!
# Phase 41 — the 3+1D gauge kinetic term (GK3D-L)

The Lean oracle's contribution to Phase-41. It certifies the ALGEBRAIC core of the
derivation — the parts that are exact real-field identities and order facts, and that
therefore deserve a formal rather than a symbolic oracle. It does NOT force the loop
integral (GK3D1), the Q-ball existence (GK3D5, numeric) or the trace computations
(GK3D4) into Lean; those have SymPy/SciPy oracles and are labelled accordingly.

Certified here:

1. `induced_normalization_closes` — the closure identity of GK3D3: the `8π²` of the
   one-loop measure cancels EXACTLY against the `8π²` of the transmutation exponent,
   `(b/(8π²)) * (8π²/(b₀β²)) = b/(b₀β²)`. This is the single step that turns a
   logarithm into a rational function of the medium coupling.

2. `induced_coupling_is_pure_ratio` — inverting it: `g² = b₀β²/b`.

3. `no_ghost` — GK3D2's positivity: the induced kinetic normalization is positive
   exactly when the cutoff lies above the excitation mass. The framework cannot
   produce a gauge ghost.

4. `ratio_indep_of_scale_choice` — GK3D6's exact cancellation: the ratio of two
   induced couplings is `b_j/b_i` regardless of the O(1) scale choice inside the
   logarithm, and regardless of the logarithm itself.

5. `constant_polarization_forces_D_two` — GK1's uniqueness, formally: `4 - D = 2`
   holds only at `D = 2`, so a constant `Π = e² × (number)` exists in exactly one
   dimension.
-/

namespace Phase41

open Real

/-- **GK3D3, the closure.** The `8π²` of the one-loop measure cancels exactly against
the `8π²` of the dimensional-transmutation exponent, leaving a pure ratio. -/
theorem induced_normalization_closes
    (b b0 beta2 : ℝ) (hb0 : b0 ≠ 0) (hbeta : beta2 ≠ 0) :
    (b / (8 * π ^ 2)) * (8 * π ^ 2 / (b0 * beta2)) = b / (b0 * beta2) := by
  have hpi : (8 : ℝ) * π ^ 2 ≠ 0 := by positivity
  field_simp

/-- **GK3D3, the result.** The induced 3+1D gauge coupling is the pure ratio
`g² = b₀β²/b` of the framework's own derived numbers. -/
theorem induced_coupling_is_pure_ratio
    (b b0 beta2 : ℝ) (hb : b ≠ 0) (hb0 : b0 ≠ 0) (hbeta : beta2 ≠ 0) :
    (b / (b0 * beta2))⁻¹ = b0 * beta2 / b := by
  field_simp

/-- **GK3D2, no ghost.** The induced kinetic normalization `Z = (b/8π²)·log(Λ/μ)` is
positive exactly when `μ < Λ`, i.e. when the excitation mass lies below the substrate's
granularity cutoff. Since the granularity is the UV end of the medium by construction,
the induced Maxwell term is automatically healthy. -/
theorem no_ghost (b lam mu : ℝ) (hb : 0 < b) (hmu : 0 < mu) (hlam : 0 < lam) :
    0 < (b / (8 * π ^ 2)) * Real.log (lam / mu) ↔ mu < lam := by
  have hpi : (0 : ℝ) < 8 * π ^ 2 := by positivity
  have hc : (0 : ℝ) < b / (8 * π ^ 2) := div_pos hb hpi
  rw [mul_pos_iff_of_pos_left hc, Real.log_pos_iff (by positivity), one_lt_div hmu]

/-- **GK3D6, exact cancellation.** The ratio of two induced couplings is `b_j/b_i`,
independent of the logarithm and hence of the O(1) scale choice inside it. -/
theorem ratio_indep_of_scale_choice
    (bi bj Lc : ℝ) (hbi : bi ≠ 0) (hbj : bj ≠ 0) (hL : Lc ≠ 0) :
    (((bi / (8 * π ^ 2)) * Lc)⁻¹) / (((bj / (8 * π ^ 2)) * Lc)⁻¹) = bj / bi := by
  have hpi : (8 : ℝ) * π ^ 2 ≠ 0 := by positivity
  field_simp

/-- **GK1's uniqueness, formally.** `[e²] = 4 - D`, so a constant polarization
`Π = e² × (pure number)` can carry mass dimension 2 in exactly one dimension: `D = 2`. -/
theorem constant_polarization_forces_D_two (D : ℝ) :
    4 - D = 2 ↔ D = 2 := by
  constructor <;> intro h <;> linarith

end Phase41
