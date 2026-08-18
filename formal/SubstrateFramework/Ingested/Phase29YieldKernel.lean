import Mathlib

/-!
# Phase 29 — Rung E per-event yield kernel: the BPS zero-binding resolution, the
  multi-Skyrmion binding hierarchy, and the classical overbinding (E-L)

This file is the Lean oracle's contribution for the Phase-29 Rung-E arc (issue #10/#9):
the per-event nuclear yield O(1) coefficient from multi-Skyrmion (B=2 deuteron / B=4 alpha)
binding. It certifies, by exact arithmetic (and π-bounds), the load-bearing physical
statements of the SymPy/SciPy bridges E1–E5:

1. `bps_zero_binding` — the BPS-Skyrme resolution (E4). When the saturated mass is LINEAR
   in baryon number, `M(B) = B · M(1)`, the classical binding `B·M(1) − M(B) = 0` for every
   `B`. Linearity ⇒ exactly zero classical binding — the structural cure for overbinding.

2. `classical_overbinds_*` — the GUARD/contrast (E3/E4). The standard L2+L4 rational-map
   model has STRICTLY DECREASING per-baryon energy (`b(1) > b(2)/2 > b(4)/4`, from E2's
   solved profiles), so its mass is NOT linear in `B` and its binding COUNT is strictly
   POSITIVE — it overbinds, and is therefore NOT the zero-binding BPS model.

3. `binding_hierarchy` — E2's result: `b(4)/4 < b(2)/2 < b(1)` (the alpha most bound per
   baryon), as exact rationals.

4. `kappa_classical_gt_five` ∧ `kappa_emp_lt_one` — E3's overbinding, dimensionless: the
   classical yield coefficient `κ = 3π²·[2b(2) − b(4)]` exceeds 5 (using `π > 3`), while the
   empirical coefficient `Q_emp/(F_π/e) = 23.86/25.686 < 1` — the ~9× overbinding gap that
   E4's near-BPS regime resolves.

5. `EL` — the headline compound: BPS zero-binding ∧ classical overbinding ∧ hierarchy ∧ the
   κ gap, with the non-tautology guard (linear ⇒ zero, strictly-decreasing ⇒ positive).

Axioms ⊆ Mathlib; no proof escape.
-/

namespace Phase29

/-! ## 1. The BPS zero-binding resolution (E4): linear mass ⇒ zero binding -/

/-- The BPS-saturated Skyrmion mass is LINEAR in baryon number: `M(B) = B · M₁`. -/
def Mbps (M1 : ℝ) (B : ℕ) : ℝ := (B : ℝ) * M1

/-- The classical binding energy `B_E(B) = B · M(1) − M(B)`. -/
def bindingBPS (M1 : ℝ) (B : ℕ) : ℝ := (B : ℝ) * M1 - Mbps M1 B

/-- **BPS zero-binding (E4).** A mass linear in `B` gives EXACTLY zero classical binding for
    every baryon number — the structural resolution of the Skyrme overbinding problem. -/
theorem bps_zero_binding (M1 : ℝ) (B : ℕ) : bindingBPS M1 B = 0 := by
  simp [bindingBPS, Mbps]

/-! ## 2. The standard L2+L4 model overbinds — strictly-decreasing per-baryon energy.
    Per-baryon energies from E2's converged profiles (units of 12π²):
    b(1) = 1.2317, b(2)/2 = 1.2077, b(4)/4 = 1.1363. -/

/-- b(1), the single-Skyrmion per-baryon energy (E2 / corpus B1). -/
def b1 : ℚ := 12317 / 10000
/-- b(2)/2, the deuteron per-baryon energy (E2). -/
def b2pb : ℚ := 12077 / 10000
/-- b(4)/4, the alpha per-baryon energy (E2). -/
def b4pb : ℚ := 11363 / 10000

/-- The B=2 configuration energy count `b(2) = 2·(b(2)/2)`. -/
def b2 : ℚ := 2 * b2pb
/-- The B=4 configuration energy count `b(4) = 4·(b(4)/4)`. -/
def b4 : ℚ := 4 * b4pb

/-- The classical binding COUNT (units of 12π²): `B_E(B) = B·b(1) − b(B)`. -/
def bindingCount (bB : ℚ) (B : ℕ) : ℚ := (B : ℚ) * b1 - bB

/-- **L2+L4 overbinds at B=2 (guard).** The classical binding count `2·b(1) − b(2)` is
    strictly POSITIVE — nonzero binding, so the standard model is NOT the BPS (zero-binding)
    submodel. -/
theorem classical_overbinds_B2 : 0 < bindingCount b2 2 := by
  unfold bindingCount b2 b2pb b1; norm_num

/-- **L2+L4 overbinds at B=4 (guard).** `4·b(1) − b(4) > 0` — strictly positive binding. -/
theorem classical_overbinds_B4 : 0 < bindingCount b4 4 := by
  unfold bindingCount b4 b4pb b1; norm_num

/-! ## 3. The multi-Skyrmion binding hierarchy (E2): alpha most bound per baryon -/

/-- **Binding hierarchy (E2).** `b(4)/4 < b(2)/2 < b(1)`: the per-baryon energy decreases
    with baryon number — the B=4 alpha is the most bound per baryon. -/
theorem binding_hierarchy : b4pb < b2pb ∧ b2pb < b1 := by
  refine ⟨?_, ?_⟩ <;> norm_num [b4pb, b2pb, b1]

/-! ## 4. The classical yield coefficient overbinds (E3), dimensionless.
    Q count = B_E(4) − 2·B_E(2) = (4·b1 − b4) − 2·(2·b1 − b2) = 2·b2 − b4 = 2856/10000.
    κ_classical = 3π²·(Q count); κ_emp = 23.86/25.686. -/

/-- The dimensionless reaction-`Q` count `2·b(2) − b(4) = 0.2856` (units of 12π²). -/
def Qcount : ℚ := 2 * b2 - b4

/-- `Qcount = 2856/10000` (exact), confirming the M(1)-cancelled yield count. -/
theorem Qcount_value : Qcount = 2856 / 10000 := by
  unfold Qcount b2 b4 b2pb b4pb; norm_num

/-- **Classical yield coefficient overbinds (E3).** `κ = 3π²·Qcount > 5` (using `π > 3`,
    so `π² > 9` and `3·9·0.2856 = 7.71 > 5`). -/
theorem kappa_classical_gt_five : 5 < 3 * Real.pi ^ 2 * (2856 / 10000) := by
  have h3 : (3 : ℝ) < Real.pi := Real.pi_gt_three
  nlinarith [h3, Real.pi_pos]

/-- **Empirical coefficient is sub-unit (E3).** `Q_emp/(F_π/e) = 23.86/25.686 < 1` — the
    physical per-event release is below one Skyrme unit, near the zero-binding BPS end, not
    the classical overbound `κ ~ 8`. -/
theorem kappa_emp_lt_one : (2386 : ℝ) / 2568.6 < 1 := by norm_num

/-! ## 5. The headline compound (E-L) -/

/-- **E-L headline.** The Phase-29 yield kernel: BPS linearity gives zero classical binding
    (the resolution); the standard L2+L4 model overbinds (strictly positive binding counts at
    B=2 and B=4 — the non-tautology guard, since a linear model would give zero); the
    multi-Skyrmion per-baryon hierarchy `b(4)/4 < b(2)/2 < b(1)` holds (alpha most bound); and
    the classical yield coefficient overbinds (`κ_classical > 5`) while the empirical
    coefficient is sub-unit (`< 1`) — the gap the near-BPS regime closes. -/
theorem EL :
    (∀ (M1 : ℝ) (B : ℕ), bindingBPS M1 B = 0) ∧
    (0 < bindingCount b2 2 ∧ 0 < bindingCount b4 4) ∧
    (b4pb < b2pb ∧ b2pb < b1) ∧
    (5 < 3 * Real.pi ^ 2 * (2856 / 10000) ∧ (2386 : ℝ) / 2568.6 < 1) := by
  refine ⟨bps_zero_binding, ⟨classical_overbinds_B2, classical_overbinds_B4⟩,
    binding_hierarchy, kappa_classical_gt_five, kappa_emp_lt_one⟩

end Phase29
