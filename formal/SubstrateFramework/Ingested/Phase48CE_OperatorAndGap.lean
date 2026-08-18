/-
  Phase48CE_OperatorAndGap.lean -- Phase-48 (merged-framework), the CE cluster (ladder row CE11).

  The structural content Phase 48 adds to the `B = 1` spectrum, stated for GENERAL variables and
  proved with no proof escape and no project axioms.  Three groups.

  (1) THE ONE-LOOP VACUUM ENERGY CANCELS FROM THE N-Delta SPLITTING, AND THE INERTIA CORRECTION
      DOES NOT.  Write the collective spectrum with a one-loop vacuum energy added to the
      classical mass, `M(J) = Mcl + E1 + J(J+1)/(2Λ)`.  The `J = 3/2` minus `J = 1/2` difference
      is exactly `3/(2Λ)` for every `Mcl` and every `E1`: the splitting is a function of the
      moment of inertia ALONE, its derivative in `E1` is zero, and two different vacuum energies
      give the SAME splitting.  The discriminating converse is proved in the same idiom: written
      in the framework's own form `3/(2Λ) = (9/2) e⁴ m_e / (L (1 + λ₁))` -- the one-loop-corrected
      inertia of `Λ = L(1+λ₁)/(3e⁴m_e)` -- the splitting is STRICTLY DECREASING in `λ₁`, so two
      different inertia corrections NEVER give the same splitting.  Meanwhile the mass ratio
      observable `M(1/2)` is strictly increasing in `E1`.  Phase 47's single residual is therefore
      TWO INDEPENDENT one-loop questions -- the vacuum energy is the mass ratio's business and the
      inertia correction is the splitting's, and neither can be traded against the other.

  (2) THE FLUCTUATION OPERATOR'S MASS WEIGHT EQUALS ITS GRADIENT WEIGHT IN EXACTLY ONE CHANNEL.
      For a unit fluctuation direction with longitudinal fraction `α` (the component along
      `e₁ = ∂n/∂f`, so `α² = 1` is `bridge_S2`'s radial-profile channel and `α = 0` is a purely
      transverse one), the gradient weight and the kinetic weight of the reduced radial problem
      differ by exactly `(1 − α²) p² (x² + c₆ s²)`, with `p = f′` the background gradient.  Hence:
      at `α² = 1` the two weights agree IDENTICALLY, for every background and every sextic
      coupling -- which DISCHARGES `bridge_S2`'s *assumed* `W = A_kin` as derived in the one
      channel it builds; and off that channel they agree only where the background is flat.  The
      physical payload is the local refractive index `√(K/A)`: exactly `1` longitudinally, and
      STRICTLY GREATER than `1` in every other channel wherever `p ≠ 0`, which is why the
      longitudinal phase shift decays while every transverse one grows at a positive eikonal
      slope.

  (3) THE FREE LIMIT OF THE COUPLED GRAND-SPIN BLOCK IS TWO CENTRIFUGAL BARRIERS.  With
      `κ = K(K+1)` the coupled block's undifferentiated matrix `[[κ+2, −2√κ], [−2√κ, κ]]` has
      characteristic determinant factoring EXACTLY over `K(K−1)` and `(K+1)(K+2)`, with
      eigenvectors exhibited and discriminant exactly `4(2K+1)²`.  Both eigenvalues are
      centrifugal: `K(K−1) = l(l+1)` at `l = K−1` and `(K+1)(K+2) = l(l+1)` at `l = K+1`.  At
      `K = 0` the surviving value is `2 = l(l+1)` at `l = 1`, NOT `0` at `l = 0`, so a channel
      matched to `j₀, y₀` is matched to the wrong free problem.  The degeneracy bookkeeping at
      fixed asymptotic `l` closes: `(2l+1) + (2(l+1)+1) + (2(l−1)+1) = 3(2l+1)`, three isospin
      polarisations per orbital multiplet.

  Not attempted here, deliberately: the operator spectrum, the phase shifts, and the
  Seeley-DeWitt coefficient `a₂`.  Those are numeric or analytic objects with no practical Lean
  oracle; they are settled by the phase's bridges, not dressed up as theorems.

  No decimal attestation at a sampled point is used anywhere -- `merged-framework/north-star.md:141-156`
  names that pattern (`sg-breather-ionization/dynamics_lean/Sigma2Prod.lean`) as the failure mode
  to design against, and names `Exchange.lean` (an algebraic identity dressed as physics) as the
  other.  Every theorem here quantifies over the physical variables, and each carries its physical
  reading in its own docstring.  The only statement at a fixed argument is
  `K_zero_channel_free_momentum_is_one`, and `K = 0` there is a channel label, not a sample point.

  DECLARED DUPLICATE.  This file is mirrored byte-identically at
  `sg-breather-ionization/formalization/Phase48CE_OperatorAndGap.lean`, because
  `merged-framework/bridges/*/lean/` is not a Lake project and loose files are elaborated against
  `sg-breather-ionization/`.  The mirror is the in-project copy; this is the phase-local copy.

  Validate ONE file (never `lake build`):
    export PATH="$HOME/.elan/bin:$PATH"
    cd sg-breather-ionization && lake env lean \
      ../merged-framework/bridges/phase-48/lean/Phase48CE_OperatorAndGap.lean
  Bar: 0 proof escapes; axioms ⊆ {propext, Classical.choice, Quot.sound}.
-/

import Mathlib

namespace Phase48CE

open Real

/-! ## Part 1 -- the splitting sees the inertia and not the vacuum energy -/

/-- The `B = 1` collective spectrum with a one-loop vacuum energy included:
    `M(J) = Mcl + E1 + J(J+1)/(2Λ)`, with `Mcl` the classical soliton mass, `E1` the one-loop
    (Casimir) vacuum energy of the same background, and `Λ` the moment of inertia. -/
noncomputable def Mtot (Mcl E1 Λ J : ℝ) : ℝ := Mcl + E1 + J * (J + 1) / (2 * Λ)

/-- **The N-Delta splitting is exactly `3/(2Λ)` -- the vacuum energy cancels.**  Neither the
classical mass nor the one-loop vacuum energy appears on the right-hand side, because both are
`J`-independent. -/
theorem gap_independent_of_vacuum_energy (Mcl E1 Λ : ℝ) (hΛ : Λ ≠ 0) :
    Mtot Mcl E1 Λ (3 / 2) - Mtot Mcl E1 Λ (1 / 2) = 3 / (2 * Λ) := by
  unfold Mtot
  field_simp
  ring

/-- **Two different vacuum energies give the same splitting.**  The `∀`-form of the cancellation:
the splitting is not a function of `E1` at all. -/
theorem gap_same_for_every_vacuum_energy (Mcl E1 E1' Λ : ℝ) (hΛ : Λ ≠ 0) :
    Mtot Mcl E1 Λ (3 / 2) - Mtot Mcl E1 Λ (1 / 2)
      = Mtot Mcl E1' Λ (3 / 2) - Mtot Mcl E1' Λ (1 / 2) := by
  rw [gap_independent_of_vacuum_energy Mcl E1 Λ hΛ, gap_independent_of_vacuum_energy Mcl E1' Λ hΛ]

/-- **`d(gap)/dE₁ = 0` as an actual derivative.**  The dossier states the cancellation in this
form; here it is, with the derivative taken at an arbitrary point. -/
theorem gap_deriv_vacuum_zero (Mcl Λ E₁ : ℝ) (hΛ : Λ ≠ 0) :
    deriv (fun t : ℝ => Mtot Mcl t Λ (3 / 2) - Mtot Mcl t Λ (1 / 2)) E₁ = 0 := by
  have h : (fun t : ℝ => Mtot Mcl t Λ (3 / 2) - Mtot Mcl t Λ (1 / 2))
      = fun _ : ℝ => 3 / (2 * Λ) := by
    funext t
    exact gap_independent_of_vacuum_energy Mcl t Λ hΛ
  rw [h]
  exact deriv_const E₁ _

/-- **The mass ratio observable DOES move with the vacuum energy.**  `M(1/2)` -- the nucleon
member, hence `m_p/m_e` -- is strictly increasing in `E₁`.  Together with the previous three
theorems this is the two-questions statement: one observable is blind to `E₁`, the other is not. -/
theorem nucleon_strictMono_in_vacuum_energy (Mcl Λ E₁ E₁' : ℝ) (h : E₁ < E₁') :
    Mtot Mcl E₁ Λ (1 / 2) < Mtot Mcl E₁' Λ (1 / 2) := by
  unfold Mtot
  linarith

/-- The splitting in the framework's own variables: with the one-loop-corrected inertia
`Λ = L(1+λ₁)/(3e⁴m_e)`, the gap `3/(2Λ)` reads `(9/2) e⁴ m_e/(L(1+λ₁))`. -/
noncomputable def gapFrame (e L lam1 me : ℝ) : ℝ := (9 / 2) * e ^ 4 * me / (L * (1 + lam1))

/-- **The framework form is the gap.**  Substituting the derived inertia into `3/(2Λ)` gives
`gapFrame` identically -- so the theorems below are theorems about the N-Delta splitting. -/
theorem gap_eq_gapFrame (e L lam1 me : ℝ) (hL : L ≠ 0) (he : e ≠ 0) (hme : me ≠ 0)
    (hlam : 1 + lam1 ≠ 0) :
    3 / (2 * (L * (1 + lam1) / (3 * e ^ 4 * me))) = gapFrame e L lam1 me := by
  unfold gapFrame
  field_simp
  ring

/-- **The splitting is STRICTLY DECREASING in the one-loop inertia correction.**  This is the
discriminating converse of `gap_independent_of_vacuum_energy`: the vacuum energy cancels from the
splitting, the inertia correction does not.  A positive `λ₁` always lowers the splitting. -/
theorem gapFrame_strictAnti (e L me lam1 lam1' : ℝ) (he : e ≠ 0) (hL : 0 < L) (hme : 0 < me)
    (h1 : -1 < lam1) (h12 : lam1 < lam1') :
    gapFrame e L lam1' me < gapFrame e L lam1 me := by
  have hnum : (0 : ℝ) < (9 / 2) * e ^ 4 * me := by positivity
  have hd1 : (0 : ℝ) < L * (1 + lam1) := by
    have : (0 : ℝ) < 1 + lam1 := by linarith
    exact mul_pos hL this
  have hd2 : (0 : ℝ) < L * (1 + lam1') := by
    have : (0 : ℝ) < 1 + lam1' := by linarith
    exact mul_pos hL this
  have hlt : L * (1 + lam1) < L * (1 + lam1') := by nlinarith
  unfold gapFrame
  exact div_lt_div_of_pos_left hnum hd1 hlt

/-- **Different inertia corrections never give the same splitting.**  The `≠`-form, matching
`gap_same_for_every_vacuum_energy` term for term: there the splitting was the same for every
`E₁`; here it is different for every distinct `λ₁`. -/
theorem gapFrame_ne_of_ne (e L me lam1 lam1' : ℝ) (he : e ≠ 0) (hL : 0 < L) (hme : 0 < me)
    (h1 : -1 < lam1) (h1' : -1 < lam1') (hne : lam1 ≠ lam1') :
    gapFrame e L lam1 me ≠ gapFrame e L lam1' me := by
  rcases lt_or_gt_of_ne hne with h | h
  · exact ne_of_gt (gapFrame_strictAnti e L me lam1 lam1' he hL hme h1 h)
  · exact ne_of_lt (gapFrame_strictAnti e L me lam1' lam1 he hL hme h1' h)

/-- **The headline: Phase 47's residual is two independent one-loop questions.**  The splitting is
blind to the vacuum energy (first conjunct, for every pair of vacuum energies) and injective in the
inertia correction (second conjunct, for every distinct pair) -- so no choice of `E₁` can be traded
against a choice of `λ₁`. -/
theorem two_independent_one_loop_questions (Mcl e L me Λ E₁ E₁' lam1 lam1' : ℝ)
    (hΛ : Λ ≠ 0) (he : e ≠ 0) (hL : 0 < L) (hme : 0 < me)
    (h1 : -1 < lam1) (h1' : -1 < lam1') (hne : lam1 ≠ lam1') :
    (Mtot Mcl E₁ Λ (3 / 2) - Mtot Mcl E₁ Λ (1 / 2)
        = Mtot Mcl E₁' Λ (3 / 2) - Mtot Mcl E₁' Λ (1 / 2))
      ∧ gapFrame e L lam1 me ≠ gapFrame e L lam1' me :=
  ⟨gap_same_for_every_vacuum_energy Mcl E₁ E₁' Λ hΛ,
   gapFrame_ne_of_ne e L me lam1 lam1' he hL hme h1 h1' hne⟩

/-! ## Part 2 -- the mass weight and the gradient weight of the fluctuation operator -/

/-- The GRADIENT (stiffness) weight of the reduced radial fluctuation problem: the coefficient of
`ξ′²` in the second variation of the static energy `tr g + e₂(g) + c₆ det g`, for a unit
fluctuation direction whose component along `e₁ = ∂n/∂f` is `α`.  `x` is the reduced radius,
`s = sin f`, `c₆` the sextic coupling.  The chiral mass term carries no derivative of the
fluctuation and so appears in neither weight. -/
noncomputable def Aw (x s c6 α : ℝ) : ℝ :=
  x ^ 2 * (1 + (1 + α ^ 2) * (s / x) ^ 2 + α ^ 2 * c6 * (s / x) ^ 4)

/-- The KINETIC (mass) weight of the same problem: the coefficient of `ξ̇²` in the reduced kinetic
energy `g₀₀ + (g₀₀ tr g − g₀ᵢg₀ᵢ) + 4π⁴c₆ Σₖ(Bᵏ)²`.  It carries the background gradient `p = f′`
through the Skyrme cross term and the sextic, each weighted by `1 − α²` -- the part of the
fluctuation NOT aligned with the background. -/
noncomputable def Kw (x s p c6 α : ℝ) : ℝ :=
  x ^ 2 * (1 + (1 - α ^ 2) * p ^ 2 + (1 + α ^ 2) * (s / x) ^ 2
            + α ^ 2 * c6 * (s / x) ^ 4 + (1 - α ^ 2) * c6 * p ^ 2 * (s / x) ^ 2)

/-- **The weight mismatch, in closed form.**  `K − A = (1 − α²) p² (x² + c₆s²)`: it is carried
entirely by the background gradient and by the non-longitudinal fraction of the fluctuation. -/
theorem weight_gap (x s p c6 α : ℝ) (hx : x ≠ 0) :
    Kw x s p c6 α - Aw x s c6 α = (1 - α ^ 2) * p ^ 2 * (x ^ 2 + c6 * s ^ 2) := by
  unfold Kw Aw
  field_simp
  ring

/-- **The gradient weight is strictly positive** off the origin, for a nonnegative sextic
coupling -- so the Sturm-Liouville problem is regular and the refractive index below is defined. -/
theorem Aw_pos (x s c6 α : ℝ) (hx : x ≠ 0) (hc6 : 0 ≤ c6) : 0 < Aw x s c6 α := by
  have hx2 : (0 : ℝ) < x ^ 2 := by positivity
  have h1 : (0 : ℝ) ≤ (1 + α ^ 2) * (s / x) ^ 2 := by positivity
  have h2 : (0 : ℝ) ≤ α ^ 2 * c6 * (s / x) ^ 4 := by positivity
  unfold Aw
  have : (0 : ℝ) < 1 + (1 + α ^ 2) * (s / x) ^ 2 + α ^ 2 * c6 * (s / x) ^ 4 := by linarith
  exact mul_pos hx2 this

/-- **(2) `A₁ = K₁` -- `bridge_S2`'s assumed weight, DERIVED.**  In the longitudinal channel
(`α² = 1`, the radial-profile fluctuation `bridge_S2` builds) the mass weight equals the gradient
weight identically: for every reduced radius, every background gradient `p`, and every sextic
coupling.  The assumption `W = A_kin` is therefore discharged, not carried as debt. -/
theorem weight_eq_gradient_longitudinal (x s p c6 α : ℝ) (hx : x ≠ 0) (hα : α ^ 2 = 1) :
    Kw x s p c6 α = Aw x s c6 α := by
  have h := weight_gap x s p c6 α hx
  rw [hα] at h
  simp at h
  linarith

/-- **(2') The identity FAILS in every other channel on a non-flat background.**  If the
fluctuation is not purely longitudinal and the background gradient does not vanish, the mass
weight and the gradient weight differ -- so injecting `W = A` into a transverse channel is
wrong. -/
theorem weight_ne_gradient_transverse (x s p c6 α : ℝ) (hx : x ≠ 0) (hc6 : 0 ≤ c6)
    (hα : α ^ 2 ≠ 1) (hp : p ≠ 0) :
    Kw x s p c6 α ≠ Aw x s c6 α := by
  have hx2 : (0 : ℝ) < x ^ 2 := by positivity
  have hcs : (0 : ℝ) ≤ c6 * s ^ 2 := by positivity
  have hsum : (0 : ℝ) < x ^ 2 + c6 * s ^ 2 := by linarith
  have hp2 : (0 : ℝ) < p ^ 2 := by positivity
  have hα' : (1 : ℝ) - α ^ 2 ≠ 0 := sub_ne_zero_of_ne (Ne.symm hα)
  have h := weight_gap x s p c6 α hx
  intro hEq
  rw [hEq] at h
  have hzero : (1 - α ^ 2) * p ^ 2 * (x ^ 2 + c6 * s ^ 2) = 0 := by linarith
  rcases mul_eq_zero.mp hzero with h1 | h2
  · rcases mul_eq_zero.mp h1 with ha | hb
    · exact hα' ha
    · exact (ne_of_gt hp2) hb
  · exact (ne_of_gt hsum) h2

/-- **(2'') The weights agree exactly when the channel is longitudinal or the background is
flat.**  The iff, so nothing is lost: `α² = 1` is `bridge_S2`'s channel and `p = 0` is the vacuum;
everywhere else the operator's mass and stiffness weights are different functions. -/
theorem weight_gap_zero_iff (x s p c6 α : ℝ) (hx : x ≠ 0) (hc6 : 0 ≤ c6) :
    Kw x s p c6 α = Aw x s c6 α ↔ (α ^ 2 = 1 ∨ p = 0) := by
  constructor
  · intro hEq
    by_contra hcon
    push_neg at hcon
    exact weight_ne_gradient_transverse x s p c6 α hx hc6 hcon.1 hcon.2 hEq
  · intro h
    rcases h with hα | hp
    · exact weight_eq_gradient_longitudinal x s p c6 α hx hα
    · subst hp
      have hg := weight_gap x s (0 : ℝ) c6 α hx
      have hz : (1 - α ^ 2) * (0 : ℝ) ^ 2 * (x ^ 2 + c6 * s ^ 2) = 0 := by ring
      rw [hz] at hg
      linarith

/-- **(2''') The mass weight EXCEEDS the gradient weight off the longitudinal channel.**  For a
genuine direction cosine (`α² < 1`) on a non-flat background the mismatch has a definite sign. -/
theorem kinetic_exceeds_gradient (x s p c6 α : ℝ) (hx : x ≠ 0) (hc6 : 0 ≤ c6)
    (hα : α ^ 2 < 1) (hp : p ≠ 0) :
    Aw x s c6 α < Kw x s p c6 α := by
  have hx2 : (0 : ℝ) < x ^ 2 := by positivity
  have hcs : (0 : ℝ) ≤ c6 * s ^ 2 := by positivity
  have hsum : (0 : ℝ) < x ^ 2 + c6 * s ^ 2 := by linarith
  have hp2 : (0 : ℝ) < p ^ 2 := by positivity
  have hα' : (0 : ℝ) < 1 - α ^ 2 := by linarith
  have h := weight_gap x s p c6 α hx
  have hpos : (0 : ℝ) < (1 - α ^ 2) * p ^ 2 * (x ^ 2 + c6 * s ^ 2) :=
    mul_pos (mul_pos hα' hp2) hsum
  linarith

/-- **(2a) The longitudinal refractive index is exactly one.**  `√(K/A) = 1` everywhere, so the
longitudinal channel's phase shift has no linear (eikonal) growth: it decays. -/
theorem refractive_index_longitudinal_one (x s p c6 α : ℝ) (hx : x ≠ 0) (hc6 : 0 ≤ c6)
    (hα : α ^ 2 = 1) :
    Real.sqrt (Kw x s p c6 α / Aw x s c6 α) = 1 := by
  have hApos : 0 < Aw x s c6 α := Aw_pos x s c6 α hx hc6
  have hEq : Kw x s p c6 α = Aw x s c6 α :=
    weight_eq_gradient_longitudinal x s p c6 α hx hα
  rw [hEq, div_self (ne_of_gt hApos), Real.sqrt_one]

/-- **(2b) Every other channel has refractive index strictly greater than one** wherever the
background is not flat.  This is the mechanism behind the phase-shift asymptotics: the eikonal
integrand `√(K/A) − 1` is strictly positive pointwise, so the transverse phase shift grows
linearly instead of decaying, and the growth cannot be removed by a choice of channel. -/
theorem refractive_index_transverse_gt_one (x s p c6 α : ℝ) (hx : x ≠ 0) (hc6 : 0 ≤ c6)
    (hα : α ^ 2 < 1) (hp : p ≠ 0) :
    1 < Real.sqrt (Kw x s p c6 α / Aw x s c6 α) := by
  have hApos : 0 < Aw x s c6 α := Aw_pos x s c6 α hx hc6
  have hlt : Aw x s c6 α < Kw x s p c6 α :=
    kinetic_exceeds_gradient x s p c6 α hx hc6 hα hp
  have hratio : (1 : ℝ) < Kw x s p c6 α / Aw x s c6 α := (one_lt_div hApos).mpr hlt
  have h := Real.sqrt_lt_sqrt (by norm_num : (0 : ℝ) ≤ 1) hratio
  rwa [Real.sqrt_one] at h

/-! ## Part 3 -- the free limit of the coupled grand-spin block -/

/-- `κ = K(K+1)`, the grand-spin Casimir. -/
noncomputable def kap (K : ℝ) : ℝ := K * (K + 1)

/-- `√κ`, the off-diagonal coupling of the free block. -/
noncomputable def rt (K : ℝ) : ℝ := Real.sqrt (kap K)

/-- The coupled block's undifferentiated matrix in the free limit `f → 0`:
    `[[κ+2, −2√κ], [−2√κ, κ]]`. -/
noncomputable def Cfree (K : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![kap K + 2, -2 * rt K; -2 * rt K, kap K]

/-- **(3) The characteristic determinant factors EXACTLY over `K(K−1)` and `(K+1)(K+2)`.**  Since
`det(C − λ) = (K(K−1) − λ)((K+1)(K+2) − λ)` for every `λ`, those two numbers are the eigenvalues
and there are no others -- an exact statement, with no root-finding and no sampled point. -/
theorem free_charpoly_factors (K lam : ℝ) (hK : 0 ≤ K) :
    (Cfree K - lam • (1 : Matrix (Fin 2) (Fin 2) ℝ)).det
      = (K * (K - 1) - lam) * ((K + 1) * (K + 2) - lam) := by
  have hknn : (0 : ℝ) ≤ kap K := by
    unfold kap
    exact mul_nonneg hK (by linarith)
  have hs : rt K ^ 2 = kap K := by
    unfold rt
    exact Real.sq_sqrt hknn
  simp only [Matrix.det_fin_two, Cfree, Matrix.sub_apply, Matrix.smul_apply,
    Matrix.one_apply_eq, Matrix.cons_val', Matrix.cons_val_zero,
    Matrix.cons_val_one, Matrix.empty_val', Matrix.cons_val_fin_one, Matrix.of_apply]
  unfold kap at hs ⊢
  norm_num
  nlinarith [hs]

/-- **(3a) The discriminant of that quadratic is exactly `4(2K+1)²`** -- a perfect square, which
is why the eigenvalues are polynomial in `K` even though the coupling `√κ` is not. -/
theorem free_discriminant (K : ℝ) :
    (kap K + 2 + kap K) ^ 2 - 4 * ((kap K + 2) * kap K - 4 * kap K) = 4 * (2 * K + 1) ^ 2 := by
  unfold kap
  ring

/-- **(3b) An eigenvector for the lower eigenvalue `K(K−1)`**, exhibited: `(√κ, K+1)`.  The two
conjuncts are the two components of `C v = K(K−1) v` written out, so the lower eigenvalue is
realised by an actual vector and not only by the characteristic polynomial. -/
theorem free_eigenvector_lower (K : ℝ) (hK : 0 ≤ K) :
    (kap K + 2) * rt K + (-2 * rt K) * (K + 1) = (K * (K - 1)) * rt K
      ∧ (-2 * rt K) * rt K + kap K * (K + 1) = (K * (K - 1)) * (K + 1) := by
  have hknn : (0 : ℝ) ≤ kap K := by
    unfold kap
    exact mul_nonneg hK (by linarith)
  have hs : rt K ^ 2 = kap K := by
    unfold rt
    exact Real.sq_sqrt hknn
  unfold kap at hs ⊢
  refine ⟨by ring, by nlinarith [hs]⟩

/-- **(3b') An eigenvector for the upper eigenvalue `(K+1)(K+2)`**, exhibited: `(√κ, −K)`. -/
theorem free_eigenvector_upper (K : ℝ) (hK : 0 ≤ K) :
    (kap K + 2) * rt K + (-2 * rt K) * (-K) = ((K + 1) * (K + 2)) * rt K
      ∧ (-2 * rt K) * rt K + kap K * (-K) = ((K + 1) * (K + 2)) * (-K) := by
  have hknn : (0 : ℝ) ≤ kap K := by
    unfold kap
    exact mul_nonneg hK (by linarith)
  have hs : rt K ^ 2 = kap K := by
    unfold rt
    exact Real.sq_sqrt hknn
  unfold kap at hs ⊢
  refine ⟨by ring, by nlinarith [hs]⟩

/-- **(3b'') The two eigenvectors are distinct directions** whenever the coupling is present
(`K > 0`), so the two eigenvalues belong to genuinely different modes rather than to one repeated
root.  `(√κ, K+1)` and `(√κ, −K)` are parallel only if `K + 1 = −K`. -/
theorem free_eigenvectors_independent (K : ℝ) (hK : 0 < K) : K + 1 ≠ -K := by
  intro h
  linarith

/-- **(3c) Both eigenvalues are centrifugal barriers.**  `K(K−1) = l(l+1)` at `l = K−1` and
`(K+1)(K+2) = l(l+1)` at `l = K+1`: the free orbital momenta of the coupled block are `K ∓ 1`. -/
theorem free_eigen_are_centrifugal (K : ℝ) :
    K * (K - 1) = (K - 1) * ((K - 1) + 1) ∧ (K + 1) * (K + 2) = (K + 1) * ((K + 1) + 1) := by
  constructor <;> ring

/-- **(3d) The `K = 0` channel's free orbital momentum is `l = 1`, not `l = 0`.**  At `K = 0` only
the surviving `(K+1)(K+2)` value is realised, and it is `2 = l(l+1)` at `l = 1`, never the `l = 0`
value `0`.  A `K = 0` channel matched to `j₀, y₀` is matched to the wrong free problem.  `K = 0` is
a channel label here, not a sampled point. -/
theorem K_zero_channel_free_momentum_is_one :
    ((0 : ℝ) + 1) * ((0 : ℝ) + 2) = 1 * (1 + 1) ∧ ((0 : ℝ) + 1) * ((0 : ℝ) + 2) ≠ 0 * (0 + 1) := by
  norm_num

/-- **(3e) The degeneracy bookkeeping closes at fixed asymptotic `l`.**  The three grand spins
`K = l` (single channel), `K = l+1` and `K = l−1` (the two coupled eigenvalues) contribute
`2K+1` states each, and the total is exactly three isospin polarisations per orbital multiplet. -/
theorem grand_spin_degeneracy (l : ℝ) :
    (2 * l + 1) + (2 * (l + 1) + 1) + (2 * (l - 1) + 1) = 3 * (2 * l + 1) := by
  ring

/-! ## Axiom audit -- every theorem must rest only on Mathlib's standard classical axioms. -/

#print axioms gap_independent_of_vacuum_energy
#print axioms gap_same_for_every_vacuum_energy
#print axioms gap_deriv_vacuum_zero
#print axioms nucleon_strictMono_in_vacuum_energy
#print axioms gap_eq_gapFrame
#print axioms gapFrame_strictAnti
#print axioms gapFrame_ne_of_ne
#print axioms two_independent_one_loop_questions
#print axioms weight_gap
#print axioms Aw_pos
#print axioms weight_eq_gradient_longitudinal
#print axioms weight_ne_gradient_transverse
#print axioms weight_gap_zero_iff
#print axioms kinetic_exceeds_gradient
#print axioms refractive_index_longitudinal_one
#print axioms refractive_index_transverse_gt_one
#print axioms free_charpoly_factors
#print axioms free_discriminant
#print axioms free_eigenvector_lower
#print axioms free_eigenvector_upper
#print axioms free_eigenvectors_independent
#print axioms free_eigen_are_centrifugal
#print axioms K_zero_channel_free_momentum_is_one
#print axioms grand_spin_degeneracy

end Phase48CE
