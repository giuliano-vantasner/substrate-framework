import Mathlib

/-!
# Bridge T1-G (Lean side) — the micro→macro thermal gate is an identity

The sg-breather oracle's single-event ionization weight `W_c = 2·P·(1−P)`
(`LandauZener.lean`, `ionizationWeight`) and the pulson oracle's macroscopic
thermal production gate `∝ sech²(ħω/2kT)` (`rung096`) are ONE function, once the
gate probability `P` is taken to be the two-level Boltzmann occupation
`P = 1/(1 + e^x)` with `x = ħω/kT`.  There is no thermal average to perform; the
seam closes as the algebraic identity

    2·P·(1−P) = 1 / (2·cosh²(x/2))   =   (1/2)·sech²(x/2).

The SymPy side is `bridge_T1G_thermal_gate.py` (`ALL 8 CHECKS PASS`); this file is
the Lean side, proving the same identity (axioms ⊆ {propext, Classical.choice,
Quot.sound}) so the bridge holds in BOTH oracles.

The PHYSICAL INPUT (not proved here): `P = 1/(1+e^x)` is the upper-state occupation
of the two-level system, and `W_c = 2P(1−P)` is the single-event gate.  What is
PROVED here is the exact identity these two named objects satisfy.
-/

namespace Phase1ThermalGate

/-- The single-event ionization weight (matches sg-breather `LandauZener.lean`). -/
noncomputable def ionizationWeight (P : ℝ) : ℝ := 2 * P * (1 - P)

/-- The two-level Boltzmann occupation `P = 1/(1 + e^x)`, `x = ħω/kT`. -/
noncomputable def occupation (x : ℝ) : ℝ := 1 / (1 + Real.exp x)

/-- THE BRIDGE: the single-event gate at the two-level occupation equals the
macroscopic `sech²` gate exactly — `2·P·(1−P) = 1/(2·cosh²(x/2))`. -/
theorem thermal_gate_eq_sech_sq (x : ℝ) :
    ionizationWeight (occupation x) = 1 / (2 * Real.cosh (x / 2) ^ 2) := by
  have hsq : Real.exp x = Real.exp (x / 2) * Real.exp (x / 2) := by
    rw [← Real.exp_add]; congr 1; ring
  rw [ionizationWeight, occupation, Real.cosh_eq, Real.exp_neg, hsq]
  have hpos : 0 < Real.exp (x / 2) := Real.exp_pos _
  have hne : Real.exp (x / 2) ≠ 0 := ne_of_gt hpos
  have hsum : Real.exp (x / 2) + (Real.exp (x / 2))⁻¹ ≠ 0 := by positivity
  have hden : (1 : ℝ) + Real.exp (x / 2) * Real.exp (x / 2) ≠ 0 := by positivity
  field_simp
  ring

/-- The Lean gate bound recovered as a function of `x`: the gate never exceeds
`1/2`, with the maximum at `x = 0` (`P = 1/2`) — matching `ionizationWeight_max`. -/
theorem thermal_gate_le_half (x : ℝ) :
    ionizationWeight (occupation x) ≤ 1 / 2 := by
  rw [thermal_gate_eq_sech_sq]
  have h1 : (1 : ℝ) ≤ Real.cosh (x / 2) := Real.one_le_cosh _
  gcongr
  nlinarith [h1]

/-- At `x = 0` (high temperature / small splitting) the gate is fully open: `= 1/2`. -/
theorem thermal_gate_at_zero : ionizationWeight (occupation 0) = 1 / 2 := by
  rw [thermal_gate_eq_sech_sq]
  norm_num [Real.cosh_zero]

end Phase1ThermalGate
