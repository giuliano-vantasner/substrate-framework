/-
Topological charge discrimination via drive sign.

  sign(F₀) < 0  →  antikink absorbed, kink reflects   (Q=+1)
  sign(F₀) > 0  →  kink absorbed, antikink reflects   (Q=−1)

Both outcomes carry the topological −1 sign.

Reference: solution.md §1.3, §2, dynamics/04_basin.md.

STATUS UPDATE (2026-06-15):
Previously this file redefined `fermionParity`, duplicating the
canonical definition in formalization/Formalization.lean.  We keep
this file self-contained (no cross‑module imports) to preserve
compilation independence.  The canonical `fermionParity` is in
Formalization.lean; this file uses an identical definition for
self‑contained compilation.

The duplication is acknowledged in `CAMPAIGN_SUMMARY.md` §6.
-/

import Mathlib
namespace SGChargeDiscrimination


-- Self-contained definition (duplicated from Formalization.lean
-- for compilation independence).
def fermionParity (Q : ℤ) : ℤ := (-1 : ℤ) ^ Q.natAbs

def reflectedCharge_cplus : ℤ := 1

def reflectedCharge_cminus : ℤ := -1

theorem channels_cp_conjugate : reflectedCharge_cplus = -reflectedCharge_cminus := by
  unfold reflectedCharge_cplus reflectedCharge_cminus
  norm_num

noncomputable def reflectedChargeFromDrive (F₀ : ℝ) : ℤ :=
  if F₀ < 0 then reflectedCharge_cplus else reflectedCharge_cminus

theorem reflectedCharge_negative_F₀ (F₀ : ℝ) (hF₀ : F₀ < 0) :
    reflectedChargeFromDrive F₀ = reflectedCharge_cplus := by
  dsimp [reflectedChargeFromDrive]
  simp [hF₀]

theorem reflectedCharge_positive_F₀ (F₀ : ℝ) (hF₀ : 0 < F₀) :
    reflectedChargeFromDrive F₀ = reflectedCharge_cminus := by
  dsimp [reflectedChargeFromDrive]
  have h : ¬ (F₀ < 0) := by linarith
  simp [h]

theorem both_channels_parity_minus_one :
    fermionParity reflectedCharge_cplus = -1 ∧ fermionParity reflectedCharge_cminus = -1 := by
  unfold fermionParity reflectedCharge_cplus reflectedCharge_cminus
  norm_num

theorem reflectedCharge_parity_is_minus_one (F₀ : ℝ) (hF₀ : F₀ ≠ 0) :
    fermionParity (reflectedChargeFromDrive F₀) = -1 := by
  by_cases hneg : F₀ < 0
  · rw [reflectedCharge_negative_F₀ F₀ hneg]
    unfold reflectedCharge_cplus fermionParity
    norm_num
  · have hpos : 0 < F₀ := by
      by_contra! h
      have : F₀ = 0 := by linarith
      exact hF₀ this
    rw [reflectedCharge_positive_F₀ F₀ hpos]
    unfold reflectedCharge_cminus fermionParity
    norm_num

theorem charge_step_counts_one :
    |(reflectedCharge_cplus : ℝ)| = 1 ∧ |(reflectedCharge_cminus : ℝ)| = 1 := by
  unfold reflectedCharge_cplus reflectedCharge_cminus
  norm_num
end SGChargeDiscrimination
