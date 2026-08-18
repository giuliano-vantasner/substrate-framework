/-
Action-quantum structure of the sine-Gordon breather family.

Companion to `Energy.lean` (which defines `E_breather w = 16 √(1 - w²)` and
proves the binding-gap ledger). This file formalizes the Phase-45 result
(`merged-framework/bridges/phase-45/`): the breather family's genuine action
variable is `J(w) = 16 arccos w`, and the corpus's `hbar_eff w = E_breather w / w`
is its harmonic (secant) surrogate, exact only in the vanishing-amplitude limit.

Every theorem here is stated for GENERAL real `w` on the physical range
`0 < w < 1` (or `-1 ≤ w ≤ 1` where that is the natural hypothesis). No decimal
attestation at a single sampled point is used anywhere — `north-star.md:143-145`
names that pattern (`Sigma2Prod.lean`) as the failure mode to design against.

Units: m = 1, β set so `E_kink = 8` (inherited from `Energy.lean`).
-/
import Mathlib
import SubstrateFramework.Ingested.Energy
open SGEnergy

open Real

namespace ActionQuantum

/-- The breather's orbit action variable, `J(w) = 16 arccos w`.
    Derived in `bridge_HE4_dhn_action_variable.py` by two independent routes:
    the field's abbreviated action `∮ p dq = 32π arccos w`, and the exact
    action-angle identity `dE₀/dJ = w`. -/
noncomputable def J_action (w : ℝ) : ℝ := 16 * Real.arccos w

/-- The corpus's effective action quantum, `ħ_eff(w) = E_breather(w) / w`
    (soliton-shadow `reverse_probe2_de_broglie_clock.py:81`). -/
noncomputable def hbar_eff (w : ℝ) : ℝ := E_breather w / w

/-- The global U(1) Noether charge of the complex-enriched breather,
    `Q(w) = 4w / √(1 - w²)` (merged-framework `bridge_EM1_u1_noether_charge.py`). -/
noncomputable def Q_charge (w : ℝ) : ℝ := 4 * w / Real.sqrt (1 - w ^ 2)

/-- soliton-shadow note-08's gradient-only action,
    `I(w) = 16 (√(1 - w²) − w arccos w)`. -/
noncomputable def I_breather (w : ℝ) : ℝ :=
  16 * (Real.sqrt (1 - w ^ 2) - w * Real.arccos w)

/-- On the physical range, `√(1 - w²) > 0`. -/
theorem sqrt_one_sub_sq_pos {w : ℝ} (hw : 0 < w) (hw' : w < 1) :
    0 < Real.sqrt (1 - w ^ 2) := by
  apply Real.sqrt_pos.mpr
  nlinarith

/-- **Charge–action reciprocity.** `Q(w) · ħ_eff(w) = 64` for every `0 < w < 1`.
    The effective action quantum is the exact reciprocal of the U(1) charge, so
    `ħ_eff`'s drift across the breather family is precisely `Q`'s drift inverted.
    (`bridge_HE3_charge_action_reciprocity.py`, check HE3.3.) -/
theorem charge_action_reciprocity {w : ℝ} (hw : 0 < w) (hw' : w < 1) :
    Q_charge w * hbar_eff w = 64 := by
  have hs : 0 < Real.sqrt (1 - w ^ 2) := sqrt_one_sub_sq_pos hw hw'
  unfold Q_charge hbar_eff E_breather
  field_simp
  ring

/-- `ħ_eff` is the reciprocal of the charge, in the explicit form `ħ_eff = 64 / Q`. -/
theorem hbar_eff_eq_sixtyfour_div_charge {w : ℝ} (hw : 0 < w) (hw' : w < 1) :
    hbar_eff w = 64 / Q_charge w := by
  have hs : 0 < Real.sqrt (1 - w ^ 2) := sqrt_one_sub_sq_pos hw hw'
  have hQ : Q_charge w ≠ 0 := by
    unfold Q_charge
    positivity
  field_simp
  rw [mul_comm]
  exact charge_action_reciprocity hw hw'

/-- **The breather energy is a sine of its own action.** `E_breather w =
    16 sin (J(w)/16)` for `-1 ≤ w ≤ 1`. Parametrized by action rather than
    frequency, the whole family is a single sine — the structural origin of the
    Dashen–Hasslacher–Neveu mass tower `M_n = 2 M_sol sin (n γ / 16)`.
    (`bridge_HE4_dhn_action_variable.py`, checks HE4.7–HE4.8.) -/
theorem E_breather_eq_sin_action (w : ℝ) :
    E_breather w = 16 * Real.sin (J_action w / 16) := by
  unfold E_breather J_action
  rw [show (16 : ℝ) * Real.arccos w / 16 = Real.arccos w by ring, Real.sin_arccos]

/-- **The frequency is the cosine of the action.** `cos (J(w)/16) = w` on
    `-1 ≤ w ≤ 1`; together with the previous theorem this inverts the family
    completely. -/
theorem cos_action_eq_freq {w : ℝ} (hw : -1 ≤ w) (hw' : w ≤ 1) :
    Real.cos (J_action w / 16) = w := by
  unfold J_action
  rw [show (16 : ℝ) * Real.arccos w / 16 = Real.arccos w by ring]
  exact Real.cos_arccos hw hw'

/-- **The action is bounded, hence the quantized tower is finite.**
    `0 < J(w) < 8π` for `0 < w < 1`. With the DHN condition `J = n ħ` this
    forces `n < 8π / ħ` — exactly the standard truncation `n < 8π / γ`.
    (`bridge_HE4_dhn_action_variable.py`, check HE4.9.) -/
theorem action_pos_lt_eight_pi {w : ℝ} (hw : 0 < w) (hw' : w < 1) :
    0 < J_action w ∧ J_action w < 8 * Real.pi := by
  constructor
  · unfold J_action
    have : 0 < Real.arccos w := Real.arccos_pos.mpr hw'
    linarith
  · unfold J_action
    have h : Real.arccos w < Real.pi / 2 := Real.arccos_lt_pi_div_two.mpr hw
    linarith

/-- **Non-universality, in general form.** `ħ_eff` is STRICTLY DECREASING on
    `(0,1)`: for `0 < w₁ < w₂ < 1` we have `ħ_eff w₂ < ħ_eff w₁`. This is the
    general-`w` statement of what the soliton-shadow scripts check at two
    sampled points; no decimal appears. (`bridge_HE1`, check HE1.12.) -/
theorem hbar_eff_strict_anti {w₁ w₂ : ℝ} (h1 : 0 < w₁) (h12 : w₁ < w₂) (h2 : w₂ < 1) :
    hbar_eff w₂ < hbar_eff w₁ := by
  have hw2pos : 0 < w₂ := lt_trans h1 h12
  have h1lt : w₁ < 1 := lt_trans h12 h2
  have hs1 : 0 < Real.sqrt (1 - w₁ ^ 2) := sqrt_one_sub_sq_pos h1 h1lt
  have hs2 : 0 < Real.sqrt (1 - w₂ ^ 2) := sqrt_one_sub_sq_pos hw2pos h2
  -- the square root is strictly smaller at the larger frequency
  have hsqrt_lt : Real.sqrt (1 - w₂ ^ 2) < Real.sqrt (1 - w₁ ^ 2) := by
    apply Real.sqrt_lt_sqrt (by nlinarith)
    nlinarith
  unfold hbar_eff E_breather
  rw [div_lt_div_iff₀ hw2pos h1]
  nlinarith

/-- **`ħ_eff` is not a universal constant.** It takes different values on
    different breather families — an immediate consequence of strict
    antitonicity, stated without reference to any particular numeric anchor. -/
theorem hbar_eff_not_constant {w₁ w₂ : ℝ} (h1 : 0 < w₁) (h12 : w₁ < w₂) (h2 : w₂ < 1) :
    hbar_eff w₁ ≠ hbar_eff w₂ :=
  ne_of_gt (hbar_eff_strict_anti h1 h12 h2)

/-- **The Legendre pair.** note-08's gradient-only action is the Legendre
    transform of the energy with respect to the action variable:
    `I(w) = E_breather w − w · J(w)`. This is why
    `bridge_T1E_E0_triple_oracle.py` has to guard `I_breather` as distinct from
    `E₀`: they are conjugates, not competitors.
    (`bridge_HE4_dhn_action_variable.py`, check HE4.14.) -/
theorem I_breather_eq_legendre (w : ℝ) :
    I_breather w = E_breather w - w * J_action w := by
  unfold I_breather E_breather J_action
  ring

/-- The action variable is genuinely a different functional of the orbit from
    `ħ_eff`: their ratio is `Π(w) = w · arccos w / √(1 - w²)`, which is what the
    Buckingham analysis forces as the breather sector's unique dimensionless
    group (`bridge_HE2`, check HE2.10; `bridge_HE4`, check HE4.11). -/
theorem action_over_hbar_eff {w : ℝ} (hw : 0 < w) (hw' : w < 1) :
    J_action w / hbar_eff w = w * Real.arccos w / Real.sqrt (1 - w ^ 2) := by
  have hs : 0 < Real.sqrt (1 - w ^ 2) := sqrt_one_sub_sq_pos hw hw'
  unfold J_action hbar_eff E_breather
  field_simp

end ActionQuantum
