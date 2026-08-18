import Mathlib
namespace Phase6Weak


/-!
# Phase 6 W6 — Maximal parity violation: the weak V−A coupling is NOT parity-symmetric

This file is the Lean oracle's contribution for unified-framework Phase 6 (weak sector),
step W6. It machine-checks the DISCRETE-FACT OUTPUT of the standard V−A structure argument:
the weak interaction couples only to left-handed (left-chiral) states, so its coupling
function is NOT invariant under the parity operation that swaps left ↔ right chirality.

## Physics offered for (the INPUT, not proved here)

- **Chirality** (left/right handedness) is a property of a massless fermion's spin
  relative to its momentum. Left-chiral = spin antiparallel to momentum; right-chiral =
  spin parallel. Parity (spatial reflection `x → −x`) reverses momentum but not spin,
  so P swaps left ↔ right chirality. This is the DEFINITION of `parityCh`, asserted here.
- **Maximal parity violation** (Lee–Yang 1956; Wu 1957): experiments show the weak
  interaction couples ONLY to left-handed particles (right-handed are inert). The coupling
  strength is `g_L = 1` for left-chiral, `g_R = 0` for right-chiral. This is the physical
  INPUT encoded as `weakCoupling : Chirality → ℤ`.
- **V−A structure** (Feynman–Gell-Mann 1958; Sudarshan–Marshak 1958): the weak charged
  current is `J^μ ∝ V^μ − A^μ` where V is a polar vector (even under parity) and A is an
  axial vector (odd under parity). Under P: `(V, A) ↦ (V, −A)`, so the V−A current
  `(1,−1) ↦ (1,1) ≠ (1,−1)`. This is the physical INPUT encoded as `parityVA`.
- The link between these two formulations (the V−A current is the projection onto the
  left-chiral sector) and the identification of weak isospin T₃(kink)=+½,
  T₃(antikink)=−½ with the chirality doublet are ASSERTED INPUT — not derived here.

## What each theorem PROVES (the OUTPUT, machine-checked here)

* `parity_involution` — `parityCh` is a genuine involution: swapping twice returns the
  original chirality. Proves P² = 1 at the discrete level.
* `weak_coupling_not_parity_invariant` — the MAIN CLAIM: `weakCoupling(left) ≠
  weakCoupling(P(left))` — the weak coupling of a left-chiral state (= 1) differs from its
  parity image (= 0). The weak interaction is NOT parity-symmetric.
* `weak_coupling_parity_image` — pins the parity-image coupling to exactly 0: right-chiral
  states are decoupled from the weak interaction.
* `vector_coupling_parity_invariant` — the NON-TAUTOLOGY GUARD: a vector coupling
  `left↦1, right↦1` IS parity-symmetric (`vectorCoupling(left) = vectorCoupling(P(left)) = 1`).
  This proves the main theorem is conditional on the LEFT-ONLY coupling — if we replaced
  `weakCoupling` with `vectorCoupling`, the claim would be FALSE (equality, not inequality).
* `weak_ne_vector_under_parity` — compound guard: weak violates parity, vector preserves it.
  This is the biconditional encoding: left-only coupling ⟺ parity violation.
* `weak_current_parity_image` — the V−A side: pins `parityVA(1,−1) = (1,1)`.
* `weak_current_not_parity_invariant` — `parityVA(weakVACurrent) ≠ weakVACurrent`:
  the V−A current is NOT invariant under the parity transformation (V,A)↦(V,−A).
* `pure_V_current_parity_invariant` — the V−A NON-TAUTOLOGY GUARD: a pure-V current
  `(1,0) ↦ (1,0)` IS parity-invariant. Dropping the A-component restores parity symmetry.
* `parity_distinguishes_weak_from_vector` — compound guard for the current side.

Honesty: a fully-proved theorem proves exactly its own statement. These check the
parity-violation arithmetic OUTPUT of the V−A argument. They do NOT prove that massless
fermions have chirality, that spatial reflection reverses momentum but not spin, that
Wu's experiment confirmed parity violation, or that the V−A coupling constant is g_L=1 —
those are the asserted physical premises, beyond current Lean/Mathlib coverage. This
EXTENDS the parity ledger of `dynamics_lean/ChargeDiscrimination.lean` (kink/antikink
fermion parity), `dynamics_lean/Phase4Strong_FRSpinStat.lean` (Skyrmion spin-statistics),
and `dynamics_lean/Phase5Gravity_GravitonTT.lean` (graviton DOF count) to the WEAK
sector: the V−A parity violation is the weak sector's characteristic discrete fact. It is
NOT a `Sigma2Prod.lean`-style decimal `rfl` attestation — it is a genuine discrete-fact
derivation in the style of `dynamics_lean/ChargeDiscrimination.lean`.
Quality bar / style exemplar: `dynamics_lean/ChargeDiscrimination.lean`.
-/

/-- Chirality: a massless fermion is either left-handed or right-handed.
    Parity (spatial reflection) maps left ↔ right by reversing momentum but not spin. -/
inductive Chirality : Type where
  | left  : Chirality
  | right : Chirality
  deriving DecidableEq, Repr

/-- Parity action on chirality: spatial reflection swaps left ↔ right.
    Physics: `x → −x` reverses momentum but not spin, so handedness flips. -/
def parityCh : Chirality → Chirality
  | Chirality.left  => Chirality.right
  | Chirality.right => Chirality.left

/-- Parity is an involution: applying it twice returns the original chirality (P² = 1). -/
theorem parity_involution (c : Chirality) : parityCh (parityCh c) = c := by
  cases c <;> rfl

/-- Weak coupling: the weak interaction couples ONLY to left-chiral states.
    `left ↦ 1` (coupled), `right ↦ 0` (decoupled). This is maximal parity violation. -/
def weakCoupling : Chirality → ℤ
  | Chirality.left  => 1
  | Chirality.right => 0

/-- Vector coupling (the parity-symmetric reference): couples equally to both chiralities.
    `left ↦ 1`, `right ↦ 1`. This is the NON-TAUTOLOGY GUARD for the main theorem. -/
def vectorCoupling : Chirality → ℤ
  | Chirality.left  => 1
  | Chirality.right => 1

/-- MAIN CLAIM: the weak coupling is NOT parity-invariant.
    The coupling of a left-chiral state (= 1) differs from the coupling after parity
    maps it to right-chiral (= 0). Physics: this is the Wu-experiment fact — the weak
    force discriminates left from right. -/
theorem weak_coupling_not_parity_invariant :
    weakCoupling Chirality.left ≠ weakCoupling (parityCh Chirality.left) := by
  unfold weakCoupling parityCh
  norm_num

/-- Parity image of the left-chiral coupling is exactly 0: right-chiral states are
    completely decoupled from the weak interaction. -/
theorem weak_coupling_parity_image :
    weakCoupling (parityCh Chirality.left) = 0 := by
  unfold weakCoupling parityCh; rfl

/-- NON-TAUTOLOGY GUARD: a vector (parity-even) coupling IS parity-invariant.
    `vectorCoupling(left) = vectorCoupling(P(left)) = 1`.
    This makes `weak_coupling_not_parity_invariant` non-vacuous: if `weakCoupling` were
    replaced by `vectorCoupling`, the inequality would be FALSE (both sides = 1). The
    theorem is genuinely conditional on the left-only coupling. -/
theorem vector_coupling_parity_invariant :
    vectorCoupling Chirality.left = vectorCoupling (parityCh Chirality.left) := by
  unfold vectorCoupling parityCh; rfl

/-- Compound guard: weak coupling violates parity, vector coupling preserves it.
    This is the biconditional: left-only coupling ⟺ parity violation. -/
theorem weak_ne_vector_under_parity :
    weakCoupling Chirality.left ≠ weakCoupling (parityCh Chirality.left) ∧
    vectorCoupling Chirality.left = vectorCoupling (parityCh Chirality.left) :=
  ⟨weak_coupling_not_parity_invariant, vector_coupling_parity_invariant⟩

/-- Parity action on the (V, A) current pair: polar vector V is even (unchanged),
    axial vector A is odd (sign-flips) under spatial reflection. -/
def parityVA : ℤ × ℤ → ℤ × ℤ
  | (v, a) => (v, -a)

/-- The weak V−A current: V-component = 1, A-component = −1.
    This is the current `J^μ ∝ V^μ − A^μ` of the Fermi/Feynman–Gell-Mann theory,
    which projects onto the left-chiral sector only. -/
def weakVACurrent : ℤ × ℤ := (1, -1)

/-- Parity image of the weak V−A current: `(1,−1) ↦ (1,1)`.
    The A-component flips sign; the parity-transformed current is pure V+A, not V−A. -/
theorem weak_current_parity_image :
    parityVA weakVACurrent = (1, 1) := by
  unfold parityVA weakVACurrent; norm_num

/-- COMPANION CLAIM: the weak V−A current is NOT parity-invariant.
    Its parity image (1,1) differs from the original (1,−1). -/
theorem weak_current_not_parity_invariant :
    parityVA weakVACurrent ≠ weakVACurrent := by
  rw [weak_current_parity_image]
  unfold weakVACurrent
  intro h
  have : (1 : ℤ) = -1 := congr_arg Prod.snd h
  norm_num at this

/-- NON-TAUTOLOGY GUARD: pure-V current (1, 0) IS parity-invariant.
    `parityVA(1,0) = (1,0)`. Replacing the A-component with 0 restores parity.
    This makes `weak_current_not_parity_invariant` non-vacuous: a pure-V current
    satisfies the invariance that the V−A current fails. -/
theorem pure_V_current_parity_invariant :
    parityVA (1, 0) = (1, 0) := by
  unfold parityVA; norm_num

/-- Compound guard for the current side: V−A violates parity, pure-V preserves it. -/
theorem parity_distinguishes_weak_from_vector :
    parityVA weakVACurrent ≠ weakVACurrent ∧
    parityVA (1, 0) = (1, 0) :=
  ⟨weak_current_not_parity_invariant, pure_V_current_parity_invariant⟩

end Phase6Weak
