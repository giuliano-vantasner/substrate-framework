import Mathlib

/-!
# Phase 27 — Rung C medium↔breather constitutive kernel: existence-requires-gap + isotope shift (MC-L)

This file is the Lean oracle's contribution for the Phase-27 Rung-C arc (the medium↔breather
constitutive map). It machine-checks the physical keystones already verified in SymPy
(MC1/MC2/MC3).

The localized sine-Gordon breather lives in a NONLINEAR medium with an on-site coupling that
opens a spectral GAP `ω₀ = c/ℓ > 0`. A localized (exponentially bound) breather EXISTS iff the
medium is gapped (`ω₀ > 0`) AND the breather frequency is sub-gap (`0 < ω_b < ω₀`). The bound
state is carried by a real-positive tail-decay rate

  `κ² = (ω₀² − ω_b²)/c²`        (κ real-positive ⟺ ω_b < ω₀ ⟺ sub-gap),

so a gapless medium (`ω₀ = 0`) or an above-gap frequency hosts NO localized breather (MC1/MC2).

The per-medium gap is the Frenkel–Kontorova on-site curvature over the loaded mass,

  `ω₀(V₀, m) = sqrt(V₀ / m)`,

so the ISOTOPE SHIFT is `ω₀(m₁)/ω₀(m₂) = sqrt(m₂/m₁)`; with `m_D = 2 m_H` this is exactly
`sqrt 2` (D:H) (MC3).

We certify the physics:

1. `BreatherExists` — the decidable existence predicate `ω₀ > 0 ∧ 0 < ω_b ∧ ω_b < ω₀`; it
   HOLDS on a concrete sub-gap example and FAILS for the gapless case.

2. `gapless_no_breather` : `∀ ω_b, ¬ BreatherExists 0 ω_b` — a gapless medium hosts no breather
   (the mandated MC2 rejection guard), and `above_gap_no_breather` : `ω_b ≥ ω₀ ⇒ ¬ BreatherExists`.

3. `kappaSq_pos_iff` : `κ²(c,ω₀,ω_b) > 0 ⟺ ω_b < ω₀` (for `ω₀,ω_b ≥ 0`, `c > 0`) — the analytic
   localized-tail / bound-state condition (MC1).

4. `isotope_ratio_DH` : `ω₀(V₀,m_H)/ω₀(V₀,m_D) = sqrt 2` for `m_D = 2 m_H`; and the general
   `isotope_ratio` : `ω₀(V₀,m₁)/ω₀(V₀,m₂) = sqrt(m₂/m₁)` (MC3).

5. `MC_L` : the HEADLINE compound — existence-requires-gap (gapless ⇒ none) AND the D:H
   isotope shift `= sqrt 2`.

6. NON-TAUTOLOGY guards: `isotope_shift_nontrivial` : `ω₀(V₀,m_H) ≠ ω₀(V₀,2 m_H)` (the D mode is
   strictly lower; a fabricated "no isotope shift" model FAILS this), proved by sqrt
   monotonicity NOT by `rfl`; and `breather_predicate_has_content` : the predicate is neither
   always-true nor always-false.
-/

namespace Phase27Medium

/-- **MC1/MC2 existence predicate.** A localized sine-Gordon breather EXISTS iff the medium is
gapped (`ω₀ > 0`) and the breather frequency is strictly sub-gap (`0 < ω_b < ω₀`). -/
def BreatherExists (ω₀ ωb : ℝ) : Prop := ω₀ > 0 ∧ 0 < ωb ∧ ωb < ω₀

/-- The per-medium spectral gap `ω₀(V₀, m) = sqrt(V₀ / m)` (Frenkel–Kontorova on-site curvature
over the loaded mass) (MC3). -/
noncomputable def ω₀ (V₀ m : ℝ) : ℝ := Real.sqrt (V₀ / m)

/-- The squared tail-decay rate `κ² = (ω₀² − ω_b²)/c²` (MC1). The bound-state tail decays as
`exp(−κ |x|)`, so a real-positive κ (κ² > 0) is exactly the localized-breather condition. -/
noncomputable def kappaSq (c ω₀ ωb : ℝ) : ℝ := (ω₀ ^ 2 - ωb ^ 2) / c ^ 2

/-- **MC-L (existence, concrete).** A concrete gapped, sub-gap medium DOES host a breather:
`ω₀ = 2`, `ω_b = 1` satisfies the predicate. -/
theorem breather_exists_example : BreatherExists 2 1 := by
  refine ⟨by norm_num, by norm_num, by norm_num⟩

/-- **MC-L (2) — gapless rejection guard (mandated).** A GAPLESS medium (`ω₀ = 0`) hosts NO
localized breather, for any frequency. This is the MC2 rejection guard as a theorem: a model
claiming a bound state in a gapless (linear) medium is REJECTED. -/
theorem gapless_no_breather : ∀ ωb : ℝ, ¬ BreatherExists 0 ωb := by
  intro ωb h
  exact absurd h.1 (by norm_num)

/-- **MC-L (2′) — above-gap rejection guard.** An above-gap frequency (`ω_b ≥ ω₀`) hosts no
localized breather: such a mode radiates into the band rather than binding. -/
theorem above_gap_no_breather (ω₀ ωb : ℝ) (h : ωb ≥ ω₀) : ¬ BreatherExists ω₀ ωb := by
  intro hb
  exact absurd hb.2.2 (not_lt.mpr h)

/-- **MC-L (3) — localized-tail / bound-state condition (MC1).** For a gapped medium
(`ω₀ ≥ 0`), non-negative frequency (`ω_b ≥ 0`), and a real propagation speed (`c > 0`), the
tail-decay rate is real-positive (`κ² > 0`) iff the breather is SUB-GAP (`ω_b < ω₀`). This is
the analytic content of "sub-gap ⇒ exponentially bound state". -/
theorem kappaSq_pos_iff (c ω₀ ωb : ℝ) (hc : 0 < c) (hω₀ : 0 ≤ ω₀) (hωb : 0 ≤ ωb) :
    kappaSq c ω₀ ωb > 0 ↔ ωb < ω₀ := by
  simp only [kappaSq]
  rw [gt_iff_lt, div_pos_iff]
  constructor
  · rintro (⟨hnum, _⟩ | ⟨_, hden⟩)
    · -- ω₀² − ω_b² > 0 and ω_b,ω₀ ≥ 0 ⇒ ω_b < ω₀
      nlinarith [hnum, hω₀, hωb]
    · -- c² < 0 impossible for c > 0
      nlinarith [sq_nonneg c, hc]
  · intro hlt
    left
    refine ⟨by nlinarith [hω₀, hωb, hlt], by positivity⟩

/-- **MC-L (4, general) — isotope ratio (MC3).** The gap ratio of two isotopic loadings is the
square root of the inverse mass ratio: `ω₀(V₀,m₁)/ω₀(V₀,m₂) = sqrt(m₂/m₁)`, for `V₀ > 0`,
`m₁ > 0`, `m₂ > 0`. Heavier loading ⇒ lower gap. -/
theorem isotope_ratio (V₀ m₁ m₂ : ℝ) (hV : 0 < V₀) (h1 : 0 < m₁) (h2 : 0 < m₂) :
    ω₀ V₀ m₁ / ω₀ V₀ m₂ = Real.sqrt (m₂ / m₁) := by
  simp only [ω₀]
  -- split each sqrt of a quotient, then combine: (√V₀/√m₁)/(√V₀/√m₂) = √m₂/√m₁
  rw [Real.sqrt_div (le_of_lt hV), Real.sqrt_div (le_of_lt hV),
      Real.sqrt_div (le_of_lt h2)]
  have hsV : 0 < Real.sqrt V₀ := Real.sqrt_pos.mpr hV
  have hs1 : 0 < Real.sqrt m₁ := Real.sqrt_pos.mpr h1
  have hs2 : 0 < Real.sqrt m₂ := Real.sqrt_pos.mpr h2
  field_simp

/-- **MC-L (4, D:H) — the deuterium/hydrogen isotope shift (MC3).** With `m_D = 2 m_H`, the gap
ratio is exactly `sqrt 2`: the hydrogen gap is `sqrt 2` times the deuterium gap. -/
theorem isotope_ratio_DH (V₀ mH : ℝ) (hV : 0 < V₀) (hH : 0 < mH) :
    ω₀ V₀ mH / ω₀ V₀ (2 * mH) = Real.sqrt 2 := by
  rw [isotope_ratio V₀ mH (2 * mH) hV hH (by positivity)]
  rw [mul_div_assoc, div_self (ne_of_gt hH), mul_one]

/-- **MC-L (HEADLINE).** The medium↔breather constitutive law in one statement: a localized
breather requires a GAPPED medium (a gapless `ω₀ = 0` medium hosts none — the MC2 rejection
guard), and the deuterium/hydrogen gap ratio is exactly `sqrt 2` (the MC3 isotope shift). -/
theorem MC_L (V₀ mH : ℝ) (hV : 0 < V₀) (hH : 0 < mH) :
    (∀ ωb : ℝ, ¬ BreatherExists 0 ωb) ∧
    (ω₀ V₀ mH / ω₀ V₀ (2 * mH) = Real.sqrt 2) :=
  ⟨gapless_no_breather, isotope_ratio_DH V₀ mH hV hH⟩

/-- **MC-L (non-tautology guard, isotope).** The deuterium gap is STRICTLY lower than the
hydrogen gap: `ω₀(V₀,m_H) ≠ ω₀(V₀,2 m_H)`. A fabricated "no isotope shift" model (same gap for
both masses) would FAIL this. Proved by strict monotonicity of `sqrt` on the strictly smaller
argument `V₀/(2 m_H) < V₀/m_H`, NOT by `rfl`. -/
theorem isotope_shift_nontrivial (V₀ mH : ℝ) (hV : 0 < V₀) (hH : 0 < mH) :
    ω₀ V₀ mH ≠ ω₀ V₀ (2 * mH) := by
  simp only [ω₀]
  -- V₀/(2 mH) < V₀/mH (heavier mass ⇒ smaller argument), so sqrt is strictly smaller
  have hlt : V₀ / (2 * mH) < V₀ / mH := by
    apply div_lt_div_of_pos_left hV hH
    linarith
  have hmono : Real.sqrt (V₀ / (2 * mH)) < Real.sqrt (V₀ / mH) :=
    Real.sqrt_lt_sqrt (by positivity) hlt
  exact ne_of_gt hmono

/-- **MC-L (non-tautology guard, predicate content).** The existence predicate is neither
always-true nor always-false: there is a gapped sub-gap medium that DOES host a breather and a
gapless one that does NOT. So `BreatherExists` carries real content (it is not vacuous). -/
theorem breather_predicate_has_content :
    (∃ a b : ℝ, BreatherExists a b) ∧ (∃ a b : ℝ, ¬ BreatherExists a b) :=
  ⟨⟨2, 1, breather_exists_example⟩, ⟨0, 1, gapless_no_breather 1⟩⟩

end Phase27Medium

#print axioms Phase27Medium.MC_L
#print axioms Phase27Medium.kappaSq_pos_iff
#print axioms Phase27Medium.isotope_ratio
#print axioms Phase27Medium.isotope_shift_nontrivial
#print axioms Phase27Medium.breather_predicate_has_content
#print axioms Phase27Medium.gapless_no_breather
