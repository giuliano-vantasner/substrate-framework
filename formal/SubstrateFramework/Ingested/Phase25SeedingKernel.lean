import Mathlib

/-!
# Phase 25 — Rung A seeding kernel: DC-null and slew-rising (SA-L)

This file is the Lean oracle's contribution for the Phase-25 Rung-A arc (the seeding
transfer function `N = (1/E_b) ∫ S(ω) χ_b(ω) dω`). It machine-checks the two physical
keystones of the *displacement-weighted* seeding kernel.

The breather oscillates at an internal frequency `ω_b > 0`, so its seeding susceptibility
`χ_b(ω)` is peaked near `ω_b`. We model it concretely by a Gaussian
`χ(ω) = exp(−(ω−ω_b)²/(2σ²))` (peaked at `ω_b`, with width `σ > 0`). The capacitive cell
couples through the displacement current `J ∝ dV/dt`, i.e. with a spectral factor `ω²`, so
the DISPLACEMENT-WEIGHTED seeding kernel is

  `w(ω) = ω² · χ(ω) = ω² · exp(−(ω−ω_b)²/(2σ²))`.

We prove:

1. `seeding_dc_null` : `w 0 = 0` — a pure-DC drive seeds nothing (the kernel is "flat in V":
   adding a DC offset to the drive does not change the seeding, since DC content is killed
   by the `ω²` displacement factor).

2. `seeding_strict_mono` : `w` is `StrictMonoOn` on `Set.Icc 0 ω_b` — seeding rises strictly
   with the slew (`dV/dt`) content on the breather's rising flank `[0, ω_b]`. This holds
   UNCONDITIONALLY in `σ` (no `σ ≥ ω_b` hypothesis needed): on `(0, ω_b)` the derivative
   `w'(ω) = exp(…) · (2ω − ω²(ω−ω_b)/σ²)` is a product of `exp > 0` and a bracket that is
   strictly positive because `2ω > 0` and `−ω²(ω−ω_b)/σ² ≥ 0` there (`ω − ω_b ≤ 0`).

3. `seeding_not_constant` : `w (ω_b/2) ≠ w 0` (`= 0`) — a non-tautology guard: the kernel
   carries real content (the monotonicity statement is not vacuously true on a constant).
-/

namespace Phase25Seeding

open Real

variable (ωb σ : ℝ)

/-- The susceptibility kernel: a Gaussian peaked at the breather frequency `ωb`. -/
noncomputable def χ (ω : ℝ) : ℝ := Real.exp (-(ω - ωb) ^ 2 / (2 * σ ^ 2))

/-- The displacement-weighted seeding kernel `w(ω) = ω² · χ(ω)`.  The `ω²` factor is the
capacitive `J ∝ dV/dt` displacement coupling. -/
noncomputable def w (ω : ℝ) : ℝ := ω ^ 2 * χ ωb σ ω

/-- **SA-L (1) — DC null.**  A pure-DC drive seeds nothing: `w 0 = 0`. -/
theorem seeding_dc_null : w ωb σ 0 = 0 := by
  simp [w]

/-- The exponential factor is always strictly positive. -/
theorem χ_pos (ω : ℝ) : 0 < χ ωb σ ω := Real.exp_pos _

/-- The derivative of `w` at every point.  We record it as a `HasDerivAt` so we can read off
its sign on the rising flank. -/
theorem hasDerivAt_w (hσ : σ ≠ 0) (ω : ℝ) :
    HasDerivAt (w ωb σ)
      (Real.exp (-(ω - ωb) ^ 2 / (2 * σ ^ 2)) *
        (2 * ω - ω ^ 2 * (ω - ωb) / σ ^ 2)) ω := by
  have hσ2 : (σ : ℝ) ^ 2 ≠ 0 := pow_ne_zero 2 hσ
  -- inner argument g(ω) = -(ω - ωb)^2 / (2 σ^2), with g'(ω) = -(ω - ωb)/σ^2
  have hg : HasDerivAt (fun ω : ℝ => -(ω - ωb) ^ 2 / (2 * σ ^ 2))
      (-(ω - ωb) / σ ^ 2) ω := by
    have hbase : HasDerivAt (fun ω : ℝ => -(ω - ωb) ^ 2 / (2 * σ ^ 2))
        ((-(2 * (ω - ωb) ^ 1 * 1)) / (2 * σ ^ 2)) ω := by
      have h1 : HasDerivAt (fun ω : ℝ => (ω - ωb) ^ 2) (2 * (ω - ωb) ^ 1 * 1) ω := by
        have := (hasDerivAt_pow 2 (ω - ωb)).comp ω
          ((hasDerivAt_id ω).sub_const ωb)
        simpa using this
      exact (h1.neg).div_const (2 * σ ^ 2)
    convert hbase using 1
    field_simp
  -- exp ∘ g
  have hexp : HasDerivAt (fun ω : ℝ => Real.exp (-(ω - ωb) ^ 2 / (2 * σ ^ 2)))
      (Real.exp (-(ω - ωb) ^ 2 / (2 * σ ^ 2)) * (-(ω - ωb) / σ ^ 2)) ω :=
    (Real.hasDerivAt_exp _).comp ω hg
  -- ω^2
  have hsq : HasDerivAt (fun ω : ℝ => ω ^ 2) (2 * ω ^ 1 * 1) ω := by
    simpa using (hasDerivAt_pow 2 ω)
  have hprod := hsq.mul hexp
  -- assemble; unfold w and χ, then reconcile the derivative algebraically
  have : HasDerivAt (w ωb σ)
      (2 * ω ^ 1 * 1 * Real.exp (-(ω - ωb) ^ 2 / (2 * σ ^ 2)) +
        ω ^ 2 * (Real.exp (-(ω - ωb) ^ 2 / (2 * σ ^ 2)) * (-(ω - ωb) / σ ^ 2))) ω := by
    simpa [w, χ] using hprod
  convert this using 1
  field_simp
  ring

/-- On the open rising flank `(0, ωb)` the derivative bracket `2ω − ω²(ω−ωb)/σ²` is strictly
positive (unconditionally in `σ`). -/
theorem deriv_bracket_pos (_hωb : 0 < ωb) (hσ : σ ≠ 0)
    {ω : ℝ} (h0 : 0 < ω) (hb : ω < ωb) :
    0 < 2 * ω - ω ^ 2 * (ω - ωb) / σ ^ 2 := by
  have hσ2 : 0 < σ ^ 2 := by positivity
  have hterm : 0 ≤ -(ω ^ 2 * (ω - ωb) / σ ^ 2) := by
    have hneg : ω - ωb ≤ 0 := by linarith
    have : ω ^ 2 * (ω - ωb) / σ ^ 2 ≤ 0 := by
      apply div_nonpos_of_nonpos_of_nonneg
      · exact mul_nonpos_of_nonneg_of_nonpos (by positivity) hneg
      · exact le_of_lt hσ2
    linarith
  have h2ω : 0 < 2 * ω := by linarith
  linarith

/-- **SA-L (2) — slew-rising / strict monotonicity.**  The displacement-weighted seeding
kernel `w` is strictly increasing on the breather rising flank `[0, ωb]`.  Holds for ANY
width `σ ≠ 0` (no `σ ≥ ωb` hypothesis). -/
theorem seeding_strict_mono (hωb : 0 < ωb) (hσ : σ ≠ 0) :
    StrictMonoOn (w ωb σ) (Set.Icc 0 ωb) := by
  apply strictMonoOn_of_deriv_pos (convex_Icc 0 ωb)
  · -- continuity on the closed interval
    exact (Continuous.continuousOn (by
      have : Continuous (w ωb σ) := by
        unfold w χ
        fun_prop
      exact this))
  · intro ω hω
    rw [interior_Icc] at hω
    obtain ⟨h0, hb⟩ := hω
    rw [(hasDerivAt_w ωb σ hσ ω).deriv]
    have hbr := deriv_bracket_pos ωb σ hωb hσ h0 hb
    have hexp : 0 < Real.exp (-(ω - ωb) ^ 2 / (2 * σ ^ 2)) := Real.exp_pos _
    positivity

/-- **SA-L (3) — non-tautology guard.**  The kernel is genuinely non-constant: at the
midpoint of the rising flank it strictly exceeds its DC value `w 0 = 0`.  (`σ ≠ 0` and
`ωb > 0` only.) -/
theorem seeding_not_constant (hωb : 0 < ωb) (_hσ : σ ≠ 0) :
    w ωb σ (ωb / 2) ≠ w ωb σ 0 := by
  rw [seeding_dc_null]
  have hpos : 0 < w ωb σ (ωb / 2) := by
    unfold w
    have hsq : 0 < (ωb / 2) ^ 2 := by positivity
    have hχ : 0 < χ ωb σ (ωb / 2) := χ_pos ωb σ _
    positivity
  exact ne_of_gt hpos

/-- Headline compound: all three SA-L facts together, for any `ωb > 0`, `σ ≠ 0`. -/
theorem SA_L (hωb : 0 < ωb) (hσ : σ ≠ 0) :
    w ωb σ 0 = 0 ∧
    StrictMonoOn (w ωb σ) (Set.Icc 0 ωb) ∧
    w ωb σ (ωb / 2) ≠ w ωb σ 0 :=
  ⟨seeding_dc_null ωb σ, seeding_strict_mono ωb σ hωb hσ,
    seeding_not_constant ωb σ hωb hσ⟩

end Phase25Seeding
