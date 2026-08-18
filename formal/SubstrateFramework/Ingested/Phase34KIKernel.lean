import Mathlib

/-!
# Phase 34 — D4: the impossibility and circularity results for the per-event yield
  coefficient `κ` (KI-L)

This file is the Lean oracle's contribution for the Phase-34 D4 arc. It certifies, by exact
algebra over the reals, the load-bearing statements of the SymPy/SciPy bridges KI1–KI5:

1. `eps_flow_scales` / `scale_invariant` — the UNDERDETERMINATION THEOREM (KI2). The flow
   `(F, e, l, m) ↦ (F, e, t·l, t·m)` leaves the framework's derived scale `F/e` exactly
   invariant while the near-BPS parameter `ε = F/(e·l·m)` scales as `ε/t²`. Since `t` ranges
   over all positives, the derived content is compatible with every value of `ε`.

2. `kappa_surjective` — BRACKET SHARPNESS (KI3). Every `y` in the open bracket `Ioo 0 K` is
   attained by an admissible (strictly positive) `ε`. Nothing inside the bracket is excluded.

3. `backsolve_is_identity` — CIRCULARITY, form 1 (KI4). Back-solving `ε` from an empirical
   `y` and pushing it back through the model returns `y` itself — for EVERY `y`. The
   "prediction" equals its own input, identically.

4. `zero_information_gain` — CIRCULARITY, form 2 (KI4). The set of bracket values consistent
   with the model after back-solving is the WHOLE bracket: posterior = prior, so the set of
   empirical values the procedure could exclude is empty.

5. `kappa_error_sign_indeterminate` — KI5. Since `κ` is a DIFFERENCE of two variational upper
   bounds, its error `2δ₂ − δ₄` takes both signs over non-negative `δ`, so `κ` inherits no
   one-sided bound from the energies.

6. `KI` — the headline compound, with the non-tautology guard that the flow genuinely moves
   `ε` (it is not invariant) while genuinely fixing `F/e`.

Axioms ⊆ Mathlib; no proof escape.
-/

namespace Phase33

/-! ## 1. The underdetermination theorem (KI2) -/

/-- The near-BPS parameter as a function of the generalized-Skyrme parameters:
`ε = (F/e)/(l·m)`, the ratio of the standard sector's energy scale `F/e` to the BPS
sector's independent energy scale `l·m`. -/
noncomputable def eps (F e l m : ℝ) : ℝ := F / (e * (l * m))

/-- A parameter point `(F, e, l, m)` of the generalized Skyrme model. -/
abbrev Params := ℝ × ℝ × ℝ × ℝ

/-- The flow `Φ_t : (F, e, l, m) ↦ (F, e, t·l, t·m)`. It rescales ONLY the BPS-sector
couplings, leaving the standard-sector parameters `F` and `e` untouched. -/
def flow (t : ℝ) (p : Params) : Params := (p.1, p.2.1, t * p.2.2.1, t * p.2.2.2)

/-- The framework's derived quantity in this sector: the energy unit `F/e` (NY1/NY2's
`16π·m_e·c²`). It is a function of the standard-sector parameters only. -/
noncomputable def derivedScale (p : Params) : ℝ := p.1 / p.2.1

/-- The near-BPS parameter as a function of a parameter point. -/
noncomputable def epsOf (p : Params) : ℝ := eps p.1 p.2.1 p.2.2.1 p.2.2.2

/-- **The flow fixes every derived quantity.** `Φ_t` does not touch `F` or `e`, so the
derived scale `F/e` — and hence anything the framework builds from it — is exactly
invariant along the flow. This is definitional, which is precisely the point: the derived
content simply does not see the BPS couplings. -/
theorem derivedScale_flow_invariant (t : ℝ) (p : Params) :
    derivedScale (flow t p) = derivedScale p := rfl

/-- **The flow sweeps `ε`.** Under `Φ_t` the near-BPS parameter scales as `ε ↦ ε/t²`.
Combined with `derivedScale_flow_invariant`, the framework's derived content is compatible
with every value of `ε` — it is underdetermined in principle. -/
theorem eps_flow_scales (F e l m t : ℝ) (he : e ≠ 0) (hl : l ≠ 0) (hm : m ≠ 0)
    (ht : t ≠ 0) :
    eps F e (t * l) (t * m) = eps F e l m / t ^ 2 := by
  unfold eps
  field_simp

/-- The scaling is genuinely nontrivial: for `t ≠ 1` and a nonzero `ε` the flow really
moves `ε`. This is the non-tautology guard — without it, "the flow sweeps `ε`" could be
vacuously satisfied by a flow that does nothing. -/
theorem eps_flow_nontrivial (F e l m t : ℝ) (hF : F ≠ 0) (he : e ≠ 0) (hl : l ≠ 0)
    (hm : m ≠ 0) (ht : 0 < t) (ht1 : t ≠ 1) :
    eps F e (t * l) (t * m) ≠ eps F e l m := by
  rw [eps_flow_scales F e l m t he hl hm (ne_of_gt ht)]
  have hε : eps F e l m ≠ 0 :=
    div_ne_zero hF (mul_ne_zero he (mul_ne_zero hl hm))
  have ht2 : (0:ℝ) < t ^ 2 := by positivity
  intro h
  have h1 : eps F e l m = eps F e l m * t ^ 2 := (div_eq_iff (ne_of_gt ht2)).mp h
  have h2 : t ^ 2 = 1 := by
    have h3 : eps F e l m * 1 = eps F e l m * t ^ 2 := by rw [mul_one]; exact h1
    exact (mul_left_cancel₀ hε h3).symm
  have : t = 1 := by nlinarith
  exact ht1 this

/-! ## 2. Bracket sharpness (KI3) and the back-solve (KI4)

We work with the representative admissible interpolant `κ(ε) = K·ε/(1+ε)`, which satisfies
both endpoint conditions the corpus derives (`κ(0⁺)=0` from E4's zero BPS binding, and
`κ(∞)=K` from E3's classical value). -/

/-- The model map `ε ↦ κ`, on the representative admissible interpolant. -/
noncomputable def kappa (K e : ℝ) : ℝ := K * e / (1 + e)

/-- The back-solve: given an observed `y`, the `ε` that would produce it. -/
noncomputable def backsolve (K y : ℝ) : ℝ := y / (K - y)

/-- **Bracket sharpness.** Every value in the open bracket `(0, K)` is attained by a strictly
positive — hence admissible (KI2) — `ε`. Nothing inside the bracket is excluded, so the
bracket cannot be narrowed by analysis alone. -/
theorem kappa_surjective (K y : ℝ) (hy : y ∈ Set.Ioo 0 K) :
    ∃ e : ℝ, 0 < e ∧ kappa K e = y := by
  obtain ⟨hy0, hyK⟩ := hy
  refine ⟨backsolve K y, ?_, ?_⟩
  · exact div_pos hy0 (by linarith)
  · unfold kappa backsolve
    have hKy : K - y ≠ 0 := by linarith
    have hK : K ≠ 0 := by linarith
    field_simp
    have hs : K - y + y = K := by ring
    rw [hs, div_self hK]

/-- **Circularity, form 1: the back-solve is the identity.** Feeding an empirical `y` through
the back-solve and back out through the model returns `y` itself — for every `y` in the
bracket. The "prediction" is its own input, so there is no residual to test: the procedure
cannot fail, which is what "assumes what it derives" means formally. -/
theorem backsolve_is_identity (K y : ℝ) (hy : y ∈ Set.Ioo 0 K) :
    kappa K (backsolve K y) = y := by
  obtain ⟨hy0, hyK⟩ := hy
  unfold kappa backsolve
  have hKy : K - y ≠ 0 := by linarith
  have hK : K ≠ 0 := by linarith
  field_simp
  have hs : K - y + y = K := by ring
  rw [hs, div_self hK]

/-- **Circularity, form 2: zero information gain.** The set of bracket values consistent with
the model after back-solving is the WHOLE bracket. Posterior = prior, so the set of empirical
values the procedure could have excluded is empty — it is unfalsifiable by construction. -/
theorem zero_information_gain (K : ℝ) :
    {y ∈ Set.Ioo (0:ℝ) K | ∃ e : ℝ, 0 < e ∧ kappa K e = y} = Set.Ioo (0:ℝ) K := by
  ext y
  constructor
  · rintro ⟨hy, -⟩; exact hy
  · intro hy
    exact ⟨hy, kappa_surjective K y hy⟩

/-! ## 3. `κ` is a difference of upper bounds, so it inherits no bound (KI5) -/

/-- The propagated error in `κ` from the variational errors `δ₂, δ₄ ≥ 0` in the energies,
in units of `3π²`: `κ_ansatz − κ_true = 3π²·(2δ₂ − δ₄)`. -/
def kappaError (d2 d4 : ℝ) : ℝ := 2 * d2 - d4

/-- **The error sign is indeterminate.** Because `κ` is a DIFFERENCE of two variational upper
bounds, its error takes BOTH signs over non-negative `δ₂, δ₄`. So `κ` inherits no one-sided
bound from the energies: `κ_classical` is a point estimate, not a ceiling. -/
theorem kappa_error_sign_indeterminate :
    (∃ d2 d4 : ℝ, 0 ≤ d2 ∧ 0 ≤ d4 ∧ 0 < kappaError d2 d4) ∧
    (∃ d2 d4 : ℝ, 0 ≤ d2 ∧ 0 ≤ d4 ∧ kappaError d2 d4 < 0) := by
  constructor
  · exact ⟨1, 0, by norm_num, le_refl 0, by unfold kappaError; norm_num⟩
  · exact ⟨0, 1, le_refl 0, by norm_num, by unfold kappaError; norm_num⟩

/-! ## 4. The headline compound -/

/-- **KI (capstone).** The four load-bearing D4 statements together:
the flow sweeps `ε` while fixing the derived scale (underdetermination); every bracket value
is attained (sharpness); the back-solve returns its own input (circularity); and `κ`'s
variational error is sign-indeterminate (it is not a bound). -/
theorem KI (K F e l m t : ℝ) (hF : F ≠ 0) (he : e ≠ 0) (hl : l ≠ 0) (hm : m ≠ 0)
    (ht : 0 < t) (ht1 : t ≠ 1) (y : ℝ) (hy : y ∈ Set.Ioo 0 K) (p : Params) :
    eps F e (t * l) (t * m) = eps F e l m / t ^ 2 ∧
    eps F e (t * l) (t * m) ≠ eps F e l m ∧
    derivedScale (flow t p) = derivedScale p ∧
    (∃ e' : ℝ, 0 < e' ∧ kappa K e' = y) ∧
    kappa K (backsolve K y) = y ∧
    (∃ d2 d4 : ℝ, 0 ≤ d2 ∧ 0 ≤ d4 ∧ 0 < kappaError d2 d4) ∧
    (∃ d2 d4 : ℝ, 0 ≤ d2 ∧ 0 ≤ d4 ∧ kappaError d2 d4 < 0) :=
  ⟨eps_flow_scales F e l m t he hl hm (ne_of_gt ht),
   eps_flow_nontrivial F e l m t hF he hl hm ht ht1,
   derivedScale_flow_invariant t p,
   kappa_surjective K y hy, backsolve_is_identity K y hy,
   kappa_error_sign_indeterminate.1, kappa_error_sign_indeterminate.2⟩

end Phase33
