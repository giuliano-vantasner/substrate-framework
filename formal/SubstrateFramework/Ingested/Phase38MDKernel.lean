import Mathlib

/-!
# Phase 38 — mode-density / over-parametrization kernel (MD-L)

The Lean oracle's contribution to the Phase-38 cluster. It certifies the ORDER and ALGEBRAIC
facts underlying MD2, MD4 and MD5 — the ones that are genuinely Mathlib-backed. It does NOT
force MD1's density-of-states integral, MD2's mode sum, or MD3's Fock-space construction into
Lean; those are symbolic (SymPy) results and are labelled as such in the dossier.

The headline Phase-38 corrections are two:

* **MD2** — Phase-37 carried `M` (the participating-mode count) as an outstanding import,
  via the factorization `S = M * A²`. But the only well-defined `A²` is the mean `S / M`,
  and then `M` cancels identically. `overparam_cancel` certifies exactly this: the growth
  condition never depended on `M`. The debt was an over-parametrization, not a missing
  measurement.

* **MD4** — the growth limb `n < S` with `S = b * r²` (`b` the medium's dimensionless
  coupling, `r = ℓ/a` a pure length ratio) is equivalent to a threshold on `r²`, and that
  threshold scales as `√n` — certified in squared form by `threshold_sqrt_scaling`, which
  avoids `Real.sqrt` entirely and is therefore exact.

Phase-32's robustness must survive a derived weight. `branching_antitone` certifies GB4's
headline — the hard-gamma fraction `B_γ = ρ/(w·N + ρ)` is STRICTLY DECREASING in the
collective number `N` — for ALL `ρ > 0` and ALL `w > 0`, with no regime assumption. That is
the property Phase-38 had to preserve rather than trade away, and it is preserved verbatim
because MD2's `S` depends only on the medium, never on `N`.

No proof escapes, no new axioms; every theorem's footprint is a subset of
`{propext, Classical.choice, Quot.sound}`.
-/

namespace Phase38MD

/-! ### 1. MD2 — the over-parametrization cancels -/

/-- **The `M` debt was never a debt.** With the only well-defined per-mode variance
`A² := S / M`, the mode count `M` cancels identically from the growth gap `n - M·A²`.
Phase-37's outstanding import is dissolved rather than supplied. -/
theorem overparam_cancel (S n M : ℝ) (hM : M ≠ 0) :
    n - M * (S / M) = n - S := by
  field_simp

/-- The same statement as an equivalence of the growth CONDITION: comparing `n` against
`M · (S/M)` is comparing `n` against `S`, for any nonzero mode count. So no value of `M`
can change which limb the channel sits on. -/
theorem growth_condition_M_free (S n M : ℝ) (hM : M ≠ 0) :
    (n < M * (S / M)) ↔ (n < S) := by
  rw [mul_div_cancel₀ _ hM]

/-! ### 2. MD4 — the growth threshold and its √n scaling -/

/-- The growth limb `n < S` with `S = b · r²` is a threshold on `r²`. Stated without
`Real.sqrt`, so it is exact. -/
theorem growth_iff (b r n : ℝ) (hb : 0 < b) :
    (n < b * r ^ 2) ↔ (n / b < r ^ 2) := by
  rw [div_lt_iff₀ hb]
  constructor
  · intro h; linarith [h]
  · intro h; linarith [h]

/-- **The threshold scales as `√n`**: quadrupling the subdivision count is exactly
compensated by doubling the length ratio `r = ℓ/a`. Certified in squared form, so no
`Real.sqrt` and no approximation enters. This is why a kinematic count rising by four
decades costs only two decades of `ℓ/a`. -/
theorem threshold_sqrt_scaling (b r n : ℝ) :
    (n < b * r ^ 2) ↔ (4 * n < b * (2 * r) ^ 2) := by
  constructor
  · intro h; nlinarith [h]
  · intro h; nlinarith [h]

/-! ### 3. MD5 — Phase-32's robustness, preserved for ALL ρ and ALL w -/

/-- The hard-gamma branching fraction. `w` is the subdivision weight, `ρ = r_γ/r_s` the
never-valued baseline ratio, `N` the collective (Dicke) number. -/
noncomputable def Bgamma (w rho N : ℝ) : ℝ := rho / (w * N + rho)

/-- **GB4's headline, preserved verbatim.** The hard-gamma fraction is STRICTLY DECREASING
in the collective number `N`, for every `ρ > 0` and every `w > 0` — no regime assumption,
no derived-weight assumption. Phase-38 does not narrow this: its `S` depends only on the
medium, never on `N`, so the derived weight enters as a positive constant in `N`. -/
theorem branching_antitone (w rho N₁ N₂ : ℝ)
    (hw : 0 < w) (hrho : 0 < rho) (hN : 0 < N₁) (hlt : N₁ < N₂) :
    Bgamma w rho N₂ < Bgamma w rho N₁ := by
  unfold Bgamma
  have h1 : 0 < w * N₁ + rho := by nlinarith
  have h2 : 0 < w * N₂ + rho := by nlinarith
  apply div_lt_div_of_pos_left hrho h1
  nlinarith

/-- The branching fraction is a genuine probability: strictly inside `(0,1)`. A fraction in
`[0,1]` is a legitimate probability, NOT a suppressed magnitude — its bound is not a
forbidden efficiency cap. -/
theorem branching_mem_unit (w rho N : ℝ) (hw : 0 < w) (hrho : 0 < rho) (hN : 0 < N) :
    0 < Bgamma w rho N ∧ Bgamma w rho N < 1 := by
  unfold Bgamma
  have hden : 0 < w * N + rho := by nlinarith
  constructor
  · exact div_pos hrho hden
  · rw [div_lt_one hden]; nlinarith

/-! ### 4. Non-vacuity -/

/-- A concrete strict instance, decided by `norm_num` rather than `rfl`: the antitone law has
real content at named positive values. -/
theorem branching_antitone_not_vacuous :
    Bgamma 1 1 2 < Bgamma 1 1 1 := by
  unfold Bgamma; norm_num

/-- The `M`-cancellation likewise has content: at a concrete nonzero `M` the growth gap is
genuinely independent of it. Two different mode counts give the SAME gap. -/
theorem overparam_cancel_not_vacuous (S n : ℝ) :
    n - (7 : ℝ) * (S / 7) = n - (10 ^ 7 : ℝ) * (S / 10 ^ 7) := by
  rw [overparam_cancel S n 7 (by norm_num),
      overparam_cancel S n (10 ^ 7) (by norm_num)]

/-! ### 5. Compound keystone -/

/-- **MD_L** — the Phase-38 keystone: the mode count cancels from the growth condition, the
resulting threshold scales as `√n`, and Phase-32's `N`-antitonicity survives for all `ρ, w > 0`.
Together: the debt is dissolved, the replacement condition is mild, and nothing already
earned is traded away. -/
theorem MD_L (S n M b r w rho N₁ N₂ : ℝ)
    (hM : M ≠ 0) (hb : 0 < b)
    (hw : 0 < w) (hrho : 0 < rho) (hN : 0 < N₁) (hlt : N₁ < N₂) :
    ((n < M * (S / M)) ↔ (n < S))
    ∧ ((n < b * r ^ 2) ↔ (4 * n < b * (2 * r) ^ 2))
    ∧ Bgamma w rho N₂ < Bgamma w rho N₁ :=
  ⟨growth_condition_M_free S n M hM,
   threshold_sqrt_scaling b r n,
   branching_antitone w rho N₁ N₂ hw hrho hN hlt⟩

end Phase38MD
