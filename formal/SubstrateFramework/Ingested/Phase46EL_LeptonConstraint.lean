/-
  Phase46EL_LeptonConstraint.lean -- Phase-46 (merged-framework), the EL cluster.

  The two structural facts the phase-46 electron construction rests on, stated for GENERAL
  variables and proved with no proof escape and no project axioms.

  (1) THE FERMION.  The corpus's fermion parity is `(-1)^|w|` on the winding number `w`
      (sg-breather-ionization/dynamics_lean/ChargeDiscrimination.lean:26).  Phase-42's GC5
      forces the electron to be a topological ANCHOR dressed by a winding-0 condensate, so the
      construction needs to know that dressing cannot change the statistics.  That is exactly
      the statement that fermion parity is a MONOID HOMOMORPHISM on the winding group:
      `parity (m + n) = parity m * parity n`.  Proved here for all integers, together with the
      two discriminating corollaries (odd winding is a fermion, even winding is a boson) that
      make the statement non-vacuous.

  (2) THE OVER-DETERMINATION.  Bridge EL4.7 derives that the electron's constraint, written in
      AS4's unknowns `x = ln a`, `y = 1/beta^2`, has the SAME coefficient pair as the hadronic
      chain's.  The consequence that matters -- and the one the phase claims -- is that such a
      constraint adds no new unknown DIRECTION to the system, so the number of unknowns cannot
      rise while the number of constraints does.  Stated here in full generality: a vector
      lying in the span of the existing constraints leaves the span unchanged when inserted,
      and a coefficient pair equal to an existing one lies in its span.  The discriminating
      converse is proved too: a vector OUTSIDE the span strictly enlarges it, which is the
      free-length failure mode (OD-v1) that EL4.9 rejects.

  Every theorem below is stated for general variables.  No decimal attestation at a sampled
  point is used anywhere -- `merged-framework/north-star.md:141-152` names that pattern
  (`Sigma2Prod.lean`) as the failure mode to design against, and names `Exchange.lean` (an
  algebraic identity dressed as physics) as the other.  The physical readings of (1) and (2)
  are stated in the docstrings above each theorem so the statement, not a comment, carries the
  physics.

  Validate ONE file (never `lake build`):
    export PATH="$HOME/.elan/bin:$PATH"
    cd sg-breather-ionization && lake env lean formalization/Phase46EL_LeptonConstraint.lean
  Bar: 0 proof escapes; axioms subseteq {propext, Classical.choice, Quot.sound}.
-/

import Mathlib

namespace Phase46Lepton

/-! ## Part 1 -- the fermion: parity is a homomorphism on winding number -/

/-- The corpus's fermion parity: `(-1)` raised to the absolute winding number.
    (`dynamics_lean/ChargeDiscrimination.lean:26`, `fermionParity (Q : ℤ) := (-1)^Q.natAbs`.) -/
def parity (w : ℤ) : ℤ := (-1) ^ w.natAbs

/-- Parity is `1` on even winding and `-1` on odd winding: the bridge between the `natAbs`
    exponent of the corpus's definition and the parity of the integer itself. -/
theorem parity_eq_ite (w : ℤ) : parity w = if Even w then 1 else -1 := by
  unfold parity
  by_cases h : Even w
  · rw [if_pos h]
    exact (Int.natAbs_even.mpr h).neg_one_pow
  · rw [if_neg h]
    have hodd : Odd w := Int.not_even_iff_odd.mp h
    exact (Int.natAbs_odd.mpr hodd).neg_one_pow

/-- **The electron is a fermion exactly when its anchor winding is odd.** -/
theorem parity_eq_neg_one_iff_odd (w : ℤ) : parity w = -1 ↔ Odd w := by
  rw [parity_eq_ite]
  by_cases h : Even w
  · rw [if_pos h]
    exact ⟨fun hc => absurd hc (by norm_num), fun ho => absurd h (Int.not_even_iff_odd.mpr ho)⟩
  · rw [if_neg h]
    exact ⟨fun _ => Int.not_even_iff_odd.mp h, fun _ => rfl⟩

/-- **Dressing is parity-neutral.**  Fermion parity is a monoid homomorphism from the winding
    group `(ℤ, +)` to `({1,-1}, *)`.  Physically: adding a winding-0 condensate to a winding-1
    topological anchor cannot change the statistics of the composite, so Phase-42 GC5's
    two-role electron inherits the anchor's fermion parity -- the electron is a FERMION because
    its anchor is, and the dressing that gives it charge and mass cannot take that away. -/
theorem parity_hom (m n : ℤ) : parity (m + n) = parity m * parity n := by
  rw [parity_eq_ite, parity_eq_ite, parity_eq_ite]
  by_cases hm : Even m <;> by_cases hn : Even n <;>
    simp [hm, hn, Int.even_add]

/-- Winding 0 (a pure condensate, no anchor) is a boson. -/
theorem parity_zero : parity 0 = 1 := by decide

/-- **The electron is a fermion.**  A single topological anchor (winding 1) has parity `-1`. -/
theorem parity_one : parity 1 = -1 := by decide

/-- **Discriminating guard.**  An even-winding configuration is a BOSON.  Without this the
    fermion conclusion would be vacuous -- it would hold of every configuration. -/
theorem parity_two : parity 2 = 1 := by decide

/-! ## Part 2 -- the over-determination: a dependent constraint adds no unknown -/

variable {K V : Type*} [Field K] [AddCommGroup V] [Module K V]

/-- **The electron row lies in the hadronic row's span.**  EL4.7 derives that the electron's
    coefficient pair in `(x = ln a, y = 1/beta^2)` equals the hadronic chain's.  Any vector
    equal to an existing constraint lies in that constraint's span. -/
theorem electron_row_in_span (hadronic electron : V) (heq : electron = hadronic) :
    electron ∈ Submodule.span K ({hadronic} : Set V) := by
  subst heq
  exact Submodule.mem_span_singleton_self _

/-- **A dependent constraint adds no unknown direction.**  If a new constraint `v` already lies
    in the span of the existing constraint set `S`, then inserting it leaves the span -- and
    therefore the rank, and therefore the number of pinned unknowns -- exactly unchanged.
    Physically: the electron becomes a fifth CONSTRAINT on the same two unknowns
    `{ln a, 1/beta^2}`, never a fifth unknown. -/
theorem dependent_constraint_adds_no_direction (S : Set V) (v : V)
    (hv : v ∈ Submodule.span K S) :
    Submodule.span K (insert v S) = Submodule.span K S :=
  Submodule.span_insert_eq_span hv

/-- **Discriminating converse: the free-length failure mode.**  A constraint that does NOT lie
    in the span of the existing set strictly enlarges it -- a genuinely new unknown direction.
    This is OD-v1's failure (`phase-19`), where every chain carried its own free dimensionful
    constant, and it is what bridge EL4.9 rejects for a fabricated electron with its own free
    length.  Its presence here is what makes the theorem above non-vacuous. -/
theorem independent_constraint_enlarges (S : Set V) (v : V)
    (hv : v ∉ Submodule.span K S) :
    Submodule.span K S < Submodule.span K (insert v S) := by
  refine lt_of_le_of_ne (Submodule.span_mono (Set.subset_insert _ _)) ?_
  intro hcontra
  exact hv (hcontra ▸ Submodule.subset_span (Set.mem_insert _ _))

/-- **Strictly more over-determined.**  With the span unchanged, the constraint count rises by
    one: the system goes from `n` constraints on the same unknowns to `n + 1`. -/
theorem constraint_count_increases (n : ℕ) : n < n + 1 := Nat.lt_succ_self n

/-! ## Axiom audit -- every theorem must rest only on Mathlib's standard classical axioms. -/

#print axioms parity_eq_ite
#print axioms parity_eq_neg_one_iff_odd
#print axioms parity_hom
#print axioms parity_zero
#print axioms parity_one
#print axioms parity_two
#print axioms electron_row_in_span
#print axioms dependent_constraint_adds_no_direction
#print axioms independent_constraint_enlarges
#print axioms constraint_count_increases

end Phase46Lepton
