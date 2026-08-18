/-
  Phase47BM_RigidTopSpectrum.lean -- Phase-47 (merged-framework), the BM cluster.

  The physical facts the Phase-47 B=1 spectrum rests on, stated for GENERAL variables and
  proved with no proof escape and no project axioms.

  (1) THE SPECTRUM IS ORDERED AND ITS GAP IS EXACT.  For any classical mass `Mcl` and any
      POSITIVE moment of inertia `Λ`, the rigid symmetric top `M(J) = Mcl + J(J+1)/(2Λ)` puts
      the `J = 3/2` member strictly above the `J = 1/2` member, and the gap is exactly `3/(2Λ)`
      -- the Δ–N splitting the corpus derives at `bridge_S2` check S2.3.  The gap does not
      contain `Mcl`, which is why the classical overestimate cancels out of the splitting.

  (2) THE RATIO IS FIVE, AND THAT IS THE QUANTUM STATEMENT.  The two rotational energies stand
      in the ratio `5` for EVERY `Λ`, so that ratio needs no scale at all.  The discriminating
      converse is proved too: the CLASSICAL top `J²/(2Λ)` gives `9`, and its gap `1/Λ` is never
      equal to the quantum gap `3/(2Λ)`, so the `J(J+1)` structure is load-bearing.

  (3) THE FRAMEWORK'S OWN FORM.  With the medium unit `U_med = 4π m_e` (so `Mcl = 48π³ b m_e`)
      and the moment of inertia `Λ = L/(3 e⁴ m_e)` that Phase 47 derives -- `L` standing for the
      shape sum `L + c₆ L₆` of `bridge_BM6_unit_identification.py` BM6.2/BM6.3 -- the `J = 1/2`
      member is exactly `(48π³ b + (9/8) e⁴/L)·m_e` and the `J = 3/2` member is
      `(48π³ b + (45/8) e⁴/L)·m_e`.  The corpus's headline `m_p/m_e = 48π³ b(1)` is the
      `L → ∞` face of that spectrum, not the spectrum.

  (4) WHAT THE UNIT IDENTIFICATION DOES.  Equating the medium member to the CLASSICAL Skyrme
      member determines `F_π/e = 16π m_e` for every `b`: `b` cancels (an iff, so the
      independence is a theorem).  Equating it instead to the QUANTISED `J = 1/2` member is
      solved by `u(b) = 16π m_e/(1 + 3e⁴/(128π³ b L))`, and that solution is STRICTLY
      INCREASING in `b` -- so `b` provably does not cancel.

  (5) THE CLOSURE, AND WHY THE ROOT SELECTION IS FORCED.  `bridge_MR4`'s KSRF relation
      `m_ρ² = 2 e² F_π²`, written for a general unit `u = F_π/e`, is `e⁴ = m_ρ²/(2u²)`.
      Substituting it into (4) turns the quantised identification into the QUADRATIC
      `u² − 16π m_e u + C = 0` with `C = 3 m_ρ²/(256π³ b L)`; that is proved here as an IFF, so
      the substitution loses nothing.  Both roots are then exhibited in closed form and root
      selection becomes a theorem rather than a preference: their product is exactly `C`, so the
      smaller root is below `C/(8π m_e)` and collapses to zero as the rotational term is switched
      off -- it has no classical limit -- while the larger root is pinned STRICTLY between
      `8π m_e` and `16π m_e`.  Collective quantisation therefore lowers the unit `F_π/e`, and by
      less than a factor of two, for every parameter value whatever.

  No decimal attestation at a sampled point is used anywhere -- `merged-framework/north-star.md:141-152`
  names that pattern (`Sigma2Prod.lean`) as the failure mode to design against, and names
  `Exchange.lean` (an algebraic identity dressed as physics) as the other.  Each theorem's
  physical reading is in its own docstring, so the statement carries the physics.

  Validate ONE file (never `lake build`):
    export PATH="$HOME/.elan/bin:$PATH"
    cd sg-breather-ionization && lake env lean \
      ../merged-framework/bridges/phase-47/lean/Phase47BM_RigidTopSpectrum.lean
  Bar: 0 proof escapes; axioms ⊆ {propext, Classical.choice, Quot.sound}.
-/

import Mathlib

namespace Phase47BM

open Real

/-- The rigid symmetric-top energy of the `B = 1` collective sector:
    `M(J) = Mcl + J(J+1)/(2Λ)`, with `Mcl` the classical soliton mass and `Λ` the moment of
    inertia computed from the same solved profile. -/
noncomputable def M (Mcl Λ J : ℝ) : ℝ := Mcl + J * (J + 1) / (2 * Λ)

/-- The classical (non-quantum) rigid top `Mcl + J²/(2Λ)`: the rejected alternative. -/
noncomputable def Mcl' (Mcl Λ J : ℝ) : ℝ := Mcl + J ^ 2 / (2 * Λ)

/-- **(1) The Δ–N gap is exactly `3/(2Λ)`**, independent of the classical mass. -/
theorem gap_eq (Mcl Λ : ℝ) (hΛ : Λ ≠ 0) :
    M Mcl Λ (3 / 2) - M Mcl Λ (1 / 2) = 3 / (2 * Λ) := by
  unfold M
  field_simp
  ring

/-- **(1') The spectrum is ordered when the moment of inertia is positive.** -/
theorem delta_above_nucleon (Mcl Λ : ℝ) (hΛ : 0 < Λ) :
    M Mcl Λ (1 / 2) < M Mcl Λ (3 / 2) := by
  have h : M Mcl Λ (3 / 2) - M Mcl Λ (1 / 2) = 3 / (2 * Λ) := gap_eq Mcl Λ (ne_of_gt hΛ)
  have hpos : 0 < 3 / (2 * Λ) := by positivity
  linarith

/-- **(2) The two rotational energies stand in the ratio five, for every `Λ`.** -/
theorem rot_ratio_five (Mcl Λ : ℝ) (hΛ : Λ ≠ 0) :
    M Mcl Λ (3 / 2) - Mcl = 5 * (M Mcl Λ (1 / 2) - Mcl) := by
  unfold M
  field_simp
  ring

/-- **(2') The classical top gives nine, not five.** -/
theorem classical_ratio_nine (Mcl Λ : ℝ) (hΛ : Λ ≠ 0) :
    Mcl' Mcl Λ (3 / 2) - Mcl = 9 * (Mcl' Mcl Λ (1 / 2) - Mcl) := by
  unfold Mcl'
  field_simp
  ring

/-- **(2'') The quantum gap `3/(2Λ)` and the classical gap `1/Λ` are never equal**, so the
`J(J+1)` structure changes the prediction rather than restating it. -/
theorem quantum_gap_ne_classical (Mcl Λ : ℝ) (hΛ : 0 < Λ) :
    M Mcl Λ (3 / 2) - M Mcl Λ (1 / 2) ≠ Mcl' Mcl Λ (3 / 2) - Mcl' Mcl Λ (1 / 2) := by
  have hne : Λ ≠ 0 := ne_of_gt hΛ
  have h1 : M Mcl Λ (3 / 2) - M Mcl Λ (1 / 2) = 3 / (2 * Λ) := gap_eq Mcl Λ hne
  have h2 : Mcl' Mcl Λ (3 / 2) - Mcl' Mcl Λ (1 / 2) = 1 / Λ := by
    unfold Mcl'; field_simp; ring
  rw [h1, h2]
  intro h
  have h3 : (3 : ℝ) = 2 := by
    field_simp at h
    linarith
  norm_num at h3

/-- **(3) The framework's `J = 1/2` member** is `(48π³ b + (9/8) e⁴/L) m_e`. -/
theorem nucleon_member (b L e me : ℝ) (hL : L ≠ 0) (hme : me ≠ 0) :
    M (48 * π ^ 3 * b * me) (L / (3 * e ^ 4 * me)) (1 / 2)
      = (48 * π ^ 3 * b + (9 / 8) * e ^ 4 / L) * me := by
  unfold M
  field_simp
  ring

/-- **(3') The framework's `J = 3/2` member** is `(48π³ b + (45/8) e⁴/L) m_e`. -/
theorem delta_member (b L e me : ℝ) (hL : L ≠ 0) (hme : me ≠ 0) :
    M (48 * π ^ 3 * b * me) (L / (3 * e ^ 4 * me)) (3 / 2)
      = (48 * π ^ 3 * b + (45 / 8) * e ^ 4 / L) * me := by
  unfold M
  field_simp
  ring

/-- **(4) The classical unit identification eliminates `b`.**  `12π² b U_med = 12π² b (u/4)`
with `U_med = 4π m_e` holds **iff** `u = 16π m_e`, for every nonzero `b`. -/
theorem classical_identification (b me u : ℝ) (hb : b ≠ 0) :
    12 * π ^ 2 * b * (4 * π * me) = 12 * π ^ 2 * b * (u / 4) ↔ u = 16 * π * me := by
  have hpi : (0 : ℝ) < π := Real.pi_pos
  have hne : (12 : ℝ) * π ^ 2 * b ≠ 0 := by
    have h12 : (0 : ℝ) < 12 * π ^ 2 := by positivity
    exact mul_ne_zero (ne_of_gt h12) hb
  constructor
  · intro h
    have h2 : (4 : ℝ) * π * me = u / 4 := mul_left_cancel₀ hne h
    linarith
  · intro h; rw [h]; ring

/-- The solution of the quantised identification, `u(b) = 16π m_e/(1 + 3e⁴/(128π³ b L))`. -/
noncomputable def uQ (b L e me : ℝ) : ℝ :=
  16 * π * me / (1 + 3 * e ^ 4 / (128 * π ^ 3 * b * L))

/-- **(4') `uQ` solves the quantised identification.**  The medium member `48π³ b m_e` equals
the classical Skyrme mass `3π² b u` plus the `J = 1/2` rotational energy
`3/(8Λ) = 9 e⁴ u/(128 π L)` exactly at `u = uQ b L e me`. -/
theorem quantised_solution (b L e me : ℝ) (hb : 0 < b) (hL : 0 < L) :
    48 * π ^ 3 * b * me
      = 3 * π ^ 2 * b * uQ b L e me + 9 * e ^ 4 * uQ b L e me / (128 * π * L) := by
  have hpi : (0 : ℝ) < π := Real.pi_pos
  have hb' : b ≠ 0 := ne_of_gt hb
  have hL' : L ≠ 0 := ne_of_gt hL
  have hpi' : (π : ℝ) ≠ 0 := ne_of_gt hpi
  have hden : (128 : ℝ) * π ^ 3 * b * L ≠ 0 := by positivity
  have hsum : 1 + 3 * e ^ 4 / (128 * π ^ 3 * b * L) ≠ 0 := by
    have : (0 : ℝ) < 1 + 3 * e ^ 4 / (128 * π ^ 3 * b * L) := by positivity
    exact ne_of_gt this
  unfold uQ
  field_simp
  ring

/-- **(4'') The solution is STRICTLY INCREASING in `b`, so `b` does not cancel.**  For
`0 < b₁ < b₂` and a positive electron mass, `uQ b₁ < uQ b₂`.  Contrast
`classical_identification`, where the value is the same for every `b`. -/
theorem uQ_strictMono (L e me b₁ b₂ : ℝ) (hL : 0 < L) (he : e ≠ 0) (hme : 0 < me)
    (h1 : 0 < b₁) (h12 : b₁ < b₂) :
    uQ b₁ L e me < uQ b₂ L e me := by
  have hpi : (0 : ℝ) < π := Real.pi_pos
  have h2 : 0 < b₂ := lt_trans h1 h12
  have hnum : (0 : ℝ) < 16 * π * me := by positivity
  have he4 : (0 : ℝ) < e ^ 4 := by positivity
  have hd1 : (0 : ℝ) < 128 * π ^ 3 * b₁ * L := by positivity
  have hd2 : (0 : ℝ) < 128 * π ^ 3 * b₂ * L := by positivity
  have hlt : 3 * e ^ 4 / (128 * π ^ 3 * b₂ * L) < 3 * e ^ 4 / (128 * π ^ 3 * b₁ * L) := by
    apply div_lt_div_of_pos_left (by positivity) hd1
    have : (0 : ℝ) < 128 * π ^ 3 * L := by positivity
    nlinarith [this]
  have hden1 : (0 : ℝ) < 1 + 3 * e ^ 4 / (128 * π ^ 3 * b₂ * L) := by positivity
  unfold uQ
  exact div_lt_div_of_pos_left hnum hden1 (by linarith)

/-! ## Part 5 -- the KSRF closure, and root selection as a theorem -/

/-- **(5) The closure turns the quantised identification into a quadratic -- an iff.**
Substituting `bridge_MR4`'s KSRF relation in the form `e⁴ = m_ρ²/(2u²)` into the quantised
identification of `quantised_solution` is EQUIVALENT to
`u² − 16π m_e u + 3 m_ρ²/(256π³ b L) = 0`.  Because it is an equivalence and not just an
implication, no solution is created or destroyed by the substitution: the quantised unit
`F_π/e` is exactly a root of that quadratic, in which `b` survives and `m_ρ` has entered. -/
theorem ksrf_quadratic (u b L me mrho : ℝ) (hu : 0 < u) (hb : 0 < b) (hL : 0 < L) :
    3 * π ^ 2 * b * u + 9 * (mrho ^ 2 / (2 * u ^ 2)) * u / (128 * π * L)
        = 48 * π ^ 3 * b * me
      ↔ u ^ 2 - 16 * π * me * u + 3 * mrho ^ 2 / (256 * π ^ 3 * b * L) = 0 := by
  have hpi : (0 : ℝ) < π := Real.pi_pos
  have key : 3 * π ^ 2 * b * u + 9 * (mrho ^ 2 / (2 * u ^ 2)) * u / (128 * π * L)
      - 48 * π ^ 3 * b * me
      = (3 * π ^ 2 * b / u)
        * (u ^ 2 - 16 * π * me * u + 3 * mrho ^ 2 / (256 * π ^ 3 * b * L)) := by
    field_simp
    ring
  have hfac : (3 : ℝ) * π ^ 2 * b / u ≠ 0 := by positivity
  constructor
  · intro h
    have h0 : (3 * π ^ 2 * b / u)
        * (u ^ 2 - 16 * π * me * u + 3 * mrho ^ 2 / (256 * π ^ 3 * b * L)) = 0 := by
      rw [← key]; linarith
    exact (mul_eq_zero.mp h0).resolve_left hfac
  · intro h
    have hk := key
    rw [h, mul_zero] at hk
    linarith

/-- The larger root of `u² − 16π m_e u + C = 0`: the branch continuous with the classical
    identification.  `C` stands for `3 m_ρ²/(256π³ b L)`. -/
noncomputable def rootPlus (me C : ℝ) : ℝ := 8 * π * me + Real.sqrt ((8 * π * me) ^ 2 - C)

/-- The smaller root: the spurious branch. -/
noncomputable def rootMinus (me C : ℝ) : ℝ := 8 * π * me - Real.sqrt ((8 * π * me) ^ 2 - C)

/-- **(5a) The larger root solves the quadratic.** -/
theorem rootPlus_solves (me C : ℝ) (hC : C ≤ (8 * π * me) ^ 2) :
    rootPlus me C ^ 2 - 16 * π * me * rootPlus me C + C = 0 := by
  have hD : (0 : ℝ) ≤ (8 * π * me) ^ 2 - C := by linarith
  have hs : Real.sqrt ((8 * π * me) ^ 2 - C) ^ 2 = (8 * π * me) ^ 2 - C := Real.sq_sqrt hD
  unfold rootPlus
  nlinarith [hs]

/-- **(5a') The smaller root solves it too** -- which is why the selection has to be made on a
    physical criterion and cannot be made by algebra alone. -/
theorem rootMinus_solves (me C : ℝ) (hC : C ≤ (8 * π * me) ^ 2) :
    rootMinus me C ^ 2 - 16 * π * me * rootMinus me C + C = 0 := by
  have hD : (0 : ℝ) ≤ (8 * π * me) ^ 2 - C := by linarith
  have hs : Real.sqrt ((8 * π * me) ^ 2 - C) ^ 2 = (8 * π * me) ^ 2 - C := Real.sq_sqrt hD
  unfold rootMinus
  nlinarith [hs]

/-- **(5b) Vieta: the product of the two roots is exactly `C`.**  Since `C ∝ 1/L`, this is the
    statement that the spurious root is driven to zero as the rotational term is switched off. -/
theorem roots_prod (me C : ℝ) (hC : C ≤ (8 * π * me) ^ 2) :
    rootPlus me C * rootMinus me C = C := by
  have hD : (0 : ℝ) ≤ (8 * π * me) ^ 2 - C := by linarith
  have hs : Real.sqrt ((8 * π * me) ^ 2 - C) ^ 2 = (8 * π * me) ^ 2 - C := Real.sq_sqrt hD
  unfold rootPlus rootMinus
  nlinarith [hs]

/-- **(5c) The physical root is pinned between `8π m_e` and `16π m_e`.**  For any strictly
positive rotational coefficient `C` below the discriminant floor, the classical-continuous root
lies STRICTLY below the classical unit `16π m_e` and strictly above half of it.  Physically:
identifying the medium expression with the QUANTISED `J = 1/2` member always lowers `F_π/e`,
and always by less than a factor of two -- no parameter choice can make it raise the unit. -/
theorem rootPlus_between (me C : ℝ) (hme : 0 < me) (hC0 : 0 < C) (hC : C < (8 * π * me) ^ 2) :
    8 * π * me < rootPlus me C ∧ rootPlus me C < 16 * π * me := by
  have hpi : (0 : ℝ) < π := Real.pi_pos
  have h8 : (0 : ℝ) < 8 * π * me := by positivity
  have hD : (0 : ℝ) < (8 * π * me) ^ 2 - C := by linarith
  constructor
  · have : 0 < Real.sqrt ((8 * π * me) ^ 2 - C) := Real.sqrt_pos.mpr hD
    unfold rootPlus; linarith
  · have h1 : Real.sqrt ((8 * π * me) ^ 2 - C) < Real.sqrt ((8 * π * me) ^ 2) :=
      Real.sqrt_lt_sqrt (le_of_lt hD) (by linarith)
    have h2 : Real.sqrt ((8 * π * me) ^ 2) = 8 * π * me := Real.sqrt_sq (le_of_lt h8)
    unfold rootPlus; rw [h2] at h1; linarith

/-- **(5d) The spurious root has no classical limit.**  It is bounded above by `C/(8π m_e)`, so
switching the rotation off (`C → 0`, i.e. `L → ∞`) sends it to zero rather than to `16π m_e`.
That is what excludes it: root selection is settled by continuity with the classical
identification, not by preference. -/
theorem rootMinus_small (me C : ℝ) (hme : 0 < me) (hC0 : 0 < C) (hC : C < (8 * π * me) ^ 2) :
    rootMinus me C < C / (8 * π * me) := by
  have hpi : (0 : ℝ) < π := Real.pi_pos
  have h8 : (0 : ℝ) < 8 * π * me := by positivity
  obtain ⟨hlo, _⟩ := rootPlus_between me C hme hC0 hC
  have hP : 0 < rootPlus me C := lt_trans h8 hlo
  have hprod : rootPlus me C * rootMinus me C = C := roots_prod me C (le_of_lt hC)
  have hEq : rootMinus me C = C / rootPlus me C := by
    field_simp
    linarith [hprod]
  rw [hEq]
  exact div_lt_div_of_pos_left hC0 h8 hlo

/-! ## Axiom audit -- every theorem must rest only on Mathlib's standard classical axioms. -/

#print axioms gap_eq
#print axioms delta_above_nucleon
#print axioms rot_ratio_five
#print axioms classical_ratio_nine
#print axioms quantum_gap_ne_classical
#print axioms nucleon_member
#print axioms delta_member
#print axioms classical_identification
#print axioms quantised_solution
#print axioms uQ_strictMono
#print axioms ksrf_quadratic
#print axioms rootPlus_solves
#print axioms rootMinus_solves
#print axioms roots_prod
#print axioms rootPlus_between
#print axioms rootMinus_small

end Phase47BM
