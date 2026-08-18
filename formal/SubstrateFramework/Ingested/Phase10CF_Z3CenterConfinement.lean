import Mathlib

/-!
# Phase 10 CF-L — the Z₃ center as the confinement order parameter

This file is the Lean oracle's capstone for unified-framework Phase 10 (the strong-sector
confinement build). It machine-checks the DISCRETE-FACT OUTPUT that makes the SU(3) colour
group a CONFINING gauge theory: (i) the SU(3) center / triality group is `Z₃` — a cyclic
group of prime order 3, whose generator has order 3 (the cube-root-of-unity content
`ω³ = 1`); and (ii) the Wilson-loop AREA LAW gives a linear static potential `V(R) = σR`
that is UNBOUNDED for any string tension `σ > 0`, the order-parameter statement of
confinement (area law ⇒ unbounded V ⇒ a quark cannot be pulled to infinity), in contrast to
the perimeter / deconfined law where `V → const` is bounded.

This is the sixth entry in the framework's gauge Lean ledger, alongside
EM4  (`Phase3EM_U1Current.lean`)            — charge conservation ⟺ phase symmetry;
W6   (`Phase6Weak_MaxParityViolation.lean`) — maximal parity violation ⟺ left-only coupling;
P7L  (`Phase7EW_MasslessPhoton.lean`)       — massless photon ⟺ unbroken generator;
QCD4 (`Phase8QCD_SU3GaugeFacts.lean`)       — the eight gluons and the SU(3) Casimir facts;
SM-L (`Phase9SM_AnomalyCancellation.lean`)  — per-generation anomaly cancellation;
CF-L (this file)                            — the Z₃ center + area-law confinement.

## Physics offered for (the INPUT, not proved here)

- **The colour gauge group is `SU(3)`, and its center is `Z(SU(3)) = Z₃`.** The center is the
  subgroup `{ωᵏ I : ω = e^{2πi/3}, k = 0,1,2}` (the scalar matrices `ωᵏ I` with `det = ω³ᵏ = 1`),
  isomorphic to the cyclic group `ℤ/3`. This `Z₃` is the TRIALITY group; it is the symmetry
  whose realisation (unbroken in the confined phase) is the confinement ORDER PARAMETER. That
  `Z(SU(3)) ≅ ℤ/3` is the asserted physical INPUT; Lean checks the arithmetic of `ℤ/3` — its
  cardinality (3), the order of its generator (3, the `ω³ = 1` content), and that it is cyclic
  of prime order. **Mathlib has no `SU(3)` Lie-group type**, so the center is MODELLED as
  `ZMod 3`; this is the arithmetic content of the center, NOT the Lie-group center itself
  (the same DECLARED-as-model + DERIVED-via-Mathlib posture as QCD4 and SM-L).
- **The Wilson loop obeys an area law in the confined phase.** A large `R × T` rectangular
  loop has `⟨W(C)⟩ ∼ e^{−σ·R·T}`, so the static potential `V(R) = −lim_{T→∞}(1/T) ln⟨W(R,T)⟩
  = σ·R` is LINEAR in the separation `R`, with string tension `σ > 0`. That the confined phase
  gives an area law (vs a perimeter law `⟨W⟩ ∼ e^{−μ·perimeter}` ⇒ `V → const` for the
  deconfined / screened phase) is the asserted physical INPUT; Lean checks the resulting
  ARITHMETIC fact — that a linear potential with positive slope is unbounded above, i.e. no
  finite energy suffices to separate the quarks (confinement), whereas a constant potential is
  bounded (deconfinement). The area-law inequality is not in Mathlib; it is modelled here as
  the Archimedean unboundedness of `σ·R` over `R : ℕ`.

## What each theorem PROVES (the OUTPUT, machine-checked here)

* `center_card_three` — the triality / center group has exactly THREE elements:
  `Fintype.card (ZMod 3) = 3` (via `ZMod.card`). The `{I, ωI, ω²I}` count.
* `generator_order_three` — the generator has ORDER 3 (the cube-root-of-unity content
  `ω³ = 1`, `ω ≠ 1`, `ω² ≠ 1`): `addOrderOf (1 : ZMod 3) = 3`.
* `center_is_cyclic` — the center is CYCLIC OF PRIME ORDER, hence `≅ ℤ/3`:
  `IsAddCyclic (ZMod 3)`, derived from `Nat.card = 3` (prime) via `isAddCyclic_of_prime_card`.
* `area_law_unbounded` — CONFINEMENT ORDER PARAMETER: for any string tension `σ > 0` the
  linear potential `V(R) = σ·R` is UNBOUNDED above — `∀ σ > 0, ∀ C, ∃ R : ℕ, σ·R > C`. No
  finite energy `C` separates the quarks: the area law ⇒ unbounded V ⇒ confinement.
* `perimeter_law_bounded` — the CONTRAST: a constant (perimeter / deconfined) potential
  `V ≡ V₀` IS bounded — `∃ C, ∀ R : ℕ, V₀ ≤ C` — so it does not confine. Together with the
  previous theorem this makes "unbounded V" the genuine order parameter separating the phases.
* `deconfined_sigma_zero` — dropping `σ > 0` BREAKS confinement: at `σ = 0` the potential
  `V ≡ 0` is bounded (`∀ C ≥ 0, ∀ R, 0·R ≤ C`), the deconfined limit. So `area_law_unbounded`
  genuinely uses `σ > 0`; it is not vacuous.
* `nontautology_su3_ne_su2` — NON-TAUTOLOGY WITNESS: the SU(3) center (`Z₃`, generator order 3)
  is DISTINCT from the SU(2) center (`Z₂`, generator order 2): `addOrderOf (1 : ZMod 3) ≠
  addOrderOf (1 : ZMod 2)` (`3 ≠ 2`). The theorem isolates SU(3)'s `Z₃` — it is NOT a vacuous
  arithmetic fact that would hold for any gauge group. Mirrors QCD4's `nontautology_guard`.
* `confinement_compound` — packages the SU(3) center facts (card 3, order 3) with the SU(2)
  guard (`3 ≠ 2`) and the area-law/perimeter-law contrast, the biconditional-flavoured
  encoding "Z₃ center + area law ⟺ confining SU(3), distinct from Z₂/SU(2)".

Honesty: a fully-proved theorem proves exactly its own statement. These check the discrete /
group-arithmetic OUTPUT of the SU(3) center (`Z₃ = ℤ/3`) and the order-theoretic OUTPUT of the
area law (a positive-slope linear function is unbounded). They do NOT prove that `Z(SU(3)) =
ℤ/3` over the actual Lie group (Mathlib has no `SU(3)` type), nor that the confined phase
exhibits an area law — those are the asserted physical premises (declared INPUT), exactly as
QCD4 asserts `dim su(N) = N²−1` and SM-L asserts the matter content. This is the same
discrete-fact posture as the other Phase-8/9 capstones: the arithmetic of the center and the
order-theory of the linear potential, not the field theory itself.
-/

namespace Phase10CF

/-! ## Part 1 — the Z₃ center / triality group (modelled as `ℤ/3`) -/

/-- The SU(3) center / triality group has exactly THREE elements `{I, ωI, ω²I}`, modelled as
    the three residues of `ℤ/3`: `Fintype.card (ZMod 3) = 3`. -/
theorem center_card_three : Fintype.card (ZMod 3) = 3 := ZMod.card 3

/-- The center's GENERATOR has order 3 — the cube-root-of-unity content `ω³ = 1` with
    `ω ≠ 1`, `ω² ≠ 1`. In the `ℤ/3` model the generator is `1` and `addOrderOf 1 = 3`. -/
theorem generator_order_three : addOrderOf (1 : ZMod 3) = 3 := by
  rw [ZMod.addOrderOf_one]

/-- The center is CYCLIC OF PRIME ORDER, hence `≅ ℤ/3`: `IsAddCyclic (ZMod 3)`. Derived from
    `Nat.card (ZMod 3) = 3` (a prime) via `isAddCyclic_of_prime_card` — the structural fact
    that an order-`p` group is cyclic. (`Fact (Nat.Prime 3)` supplies the primality of 3.) -/
theorem center_is_cyclic : IsAddCyclic (ZMod 3) := by
  haveI : Fact (Nat.Prime 3) := ⟨by norm_num⟩
  have hc : Nat.card (ZMod 3) = 3 := by
    rw [Nat.card_eq_fintype_card, ZMod.card]
  exact isAddCyclic_of_prime_card hc

/-! ## Part 2 — the Wilson-loop area law as the confinement order parameter -/

/-- CONFINEMENT ORDER PARAMETER (the AREA LAW): for any string tension `σ > 0`, the linear
    static potential `V(R) = σ·R` is UNBOUNDED above — for every energy budget `C` there is a
    separation `R` with `σ·R > C`. Physically: no finite energy can pull a quark to infinity,
    so colour is confined. Proved by the Archimedean property of `ℚ` (`exists_nat_gt`). -/
theorem area_law_unbounded :
    ∀ (σ : ℚ), 0 < σ → ∀ (C : ℚ), ∃ (R : ℕ), σ * (R : ℚ) > C := by
  intro σ hσ C
  obtain ⟨n, hn⟩ := exists_nat_gt (C / σ)
  refine ⟨n, ?_⟩
  rw [gt_iff_lt]
  rw [div_lt_iff₀ hσ] at hn
  linarith

/-- THE CONTRAST (the PERIMETER / DECONFINED law): a constant potential `V ≡ V₀` (the
    `V → const` of the perimeter law) IS bounded above — taking `C = V₀` works for every `R`.
    A bounded potential does NOT confine: a finite energy separates the charges. This pins
    "unbounded V" as the genuine order parameter distinguishing the two phases. -/
theorem perimeter_law_bounded :
    ∀ (V₀ : ℚ), ∃ (C : ℚ), ∀ (R : ℕ), V₀ ≤ C := by
  intro V₀
  exact ⟨V₀, fun _R => le_refl V₀⟩

/-- DROPPING `σ > 0` BREAKS confinement: at `σ = 0` the potential `V(R) = 0·R = 0` is bounded
    (deconfined limit), so `area_law_unbounded` genuinely depends on the positivity of the
    string tension and is not a vacuous quantifier statement. -/
theorem deconfined_sigma_zero :
    ∀ (C : ℚ), 0 ≤ C → ∀ (R : ℕ), (0 : ℚ) * (R : ℚ) ≤ C := by
  intro C hC _R
  simpa using hC

/-! ## Part 3 — non-tautology witness and the compound order-parameter statement -/

/-- NON-TAUTOLOGY WITNESS: the SU(3) center (`Z₃`, generator order 3) is DISTINCT from the
    SU(2) center (`Z₂`, generator order 2): `addOrderOf (1 : ZMod 3) ≠ addOrderOf (1 : ZMod 2)`
    because `3 ≠ 2`. The theorem isolates SU(3)'s `Z₃`; it is NOT a vacuous arithmetic fact
    that holds for every gauge group. Mirrors QCD4's `nontautology_guard`. -/
theorem nontautology_su3_ne_su2 :
    addOrderOf (1 : ZMod 3) ≠ addOrderOf (1 : ZMod 2) := by
  rw [ZMod.addOrderOf_one, ZMod.addOrderOf_one]; decide

/-- COMPOUND ORDER-PARAMETER STATEMENT: the SU(3) center facts (`card = 3`, generator order 3)
    hold, the SU(2) center is genuinely different (`3 ≠ 2`), AND the area law confines
    (unbounded `V` for `σ > 0`) while the perimeter law does not (bounded constant `V`). This
    packages "Z₃ center + area law ⟺ confining SU(3), distinct from Z₂/SU(2)" into one fact. -/
theorem confinement_compound :
    (Fintype.card (ZMod 3) = 3 ∧ addOrderOf (1 : ZMod 3) = 3) ∧
    (addOrderOf (1 : ZMod 3) ≠ addOrderOf (1 : ZMod 2)) ∧
    (∀ (σ : ℚ), 0 < σ → ∀ (C : ℚ), ∃ (R : ℕ), σ * (R : ℚ) > C) ∧
    (∀ (V₀ : ℚ), ∃ (C : ℚ), ∀ (R : ℕ), V₀ ≤ C) :=
  ⟨⟨center_card_three, generator_order_three⟩,
   nontautology_su3_ne_su2, area_law_unbounded, perimeter_law_bounded⟩

end Phase10CF

-- Axiom audit: each theorem's footprint must be ⊆ {propext, Classical.choice, Quot.sound}.
#print axioms Phase10CF.center_card_three
#print axioms Phase10CF.generator_order_three
#print axioms Phase10CF.center_is_cyclic
#print axioms Phase10CF.area_law_unbounded
#print axioms Phase10CF.perimeter_law_bounded
#print axioms Phase10CF.deconfined_sigma_zero
#print axioms Phase10CF.nontautology_su3_ne_su2
#print axioms Phase10CF.confinement_compound
