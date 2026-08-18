/-
Algebraic kink exchange algebra (exterior algebra representation).

⚠ TAUTOLOGY — the exterior algebra assumes fermionic anticommutation.
The physics‑carrying derivation is in `../dynamics_lean/Bridge.lean` §2
(derived from bosonic commutator via BCH, not assumed).

This file provides algebraic identities about ExteriorAlgebra that are
TRUE as statements about exterior algebras, but they do NOT prove that
sine‑Gordon kinks satisfy these relations — they ASSUME it through the
choice of ExteriorAlgebra as the algebraic model.

The genuine physics bridge is Bridge.lean: starting from the bosonic CCR
[φ_L(x), φ_L(y)] = (i/4) sgn(x−y) and applying BCH to the vertex operator
:exp(i β φ_L(x)): to derive the exchange phase Θ = β²/4.  At the free‑fermion
point β² = 4π, Θ = π gives the fermionic −1.  At the problem coupling
β² = 1, Θ = 1/4 rad gives an anyonic exchange phase.

SEE: dynamics_lean/Bridge.lean (6 genuine Lean theorems, 0 unresolved goals; BCH identity verified in Python `numerical/sMatrix_verify.py`)
SEE: ../bridge.md §2 (full analytical derivation)
-/

import Mathlib
namespace SGExchange

open ExteriorAlgebra

variable (V : Type*) [AddCommGroup V] [Module ℝ V]

/--
Exchange of two kink modes: ιx·ιy = −ιy·ιx (exterior algebra fact).
⚠ TAUTOLOGY — derived from `ι_add_mul_swap`, which is a basic
property of ExteriorAlgebra.  This proves that exterior algebra
generators anticommute, which is true by definition.  It does NOT
prove that sine‑Gordon kink creation operators satisfy this — that
requires Bridge.lean.
-/
theorem kink_exchange_neg (x y : V) : ι ℝ x * ι ℝ y = -(ι ℝ y * ι ℝ x) := by
  have h := ι_add_mul_swap (R := ℝ) (M := V) x y
  exact eq_neg_of_add_eq_zero_left h

/--
Pauli exclusion: ιx·ιx = 0 (exterior algebra fact).
⚠ TAUTOLOGY — derived from `ι_sq_zero`.  This is true for exterior
algebra generators.  It does NOT prove kink Pauli exclusion at β²=1
(where the actual kink anticommutator does NOT vanish because the
exchange phase Θ = 1/4 rad ≠ π).
-/
theorem kink_pauli_exclusion (x : V) : ι ℝ x * ι ℝ x = 0 := by rw [ι_sq_zero]

/--
g₂(0) = 0 — HBT dip in the exterior algebra model.
⚠ TAUTOLOGY — identical to kink_pauli_exclusion.  The particle-counting
HBT observable (arrival-time correlation) gives g₂(0) = 0 for ALL β² —
see `hbt_observable_gate.md` and `dynamics_lean/HBT_Approach.lean`.
The old "shallow hole ≈ 0.70" followed from conflating local OPE with HBT.
-/
theorem kink_hbt_dip (x : V) : ι ℝ x * ι ℝ x = 0 := kink_pauli_exclusion V x

/--
Three‑mode consistency of the exchange sign.
⚠ TAUTOLOGY — derived from kink_exchange_neg, which itself is a
tautology from the exterior algebra fact.
-/
theorem kink_three_mode_consistency (x y z : V) :
    ι ℝ x * ι ℝ y * ι ℝ z = -(ι ℝ y * ι ℝ x * ι ℝ z) := by
  calc
    ι ℝ x * ι ℝ y * ι ℝ z = (ι ℝ x * ι ℝ y) * ι ℝ z := by ring
    _ = (-(ι ℝ y * ι ℝ x)) * ι ℝ z := by rw [kink_exchange_neg V x y]
    _ = -((ι ℝ y * ι ℝ x) * ι ℝ z) := by simp
    _ = -(ι ℝ y * ι ℝ x * ι ℝ z) := by ring

/-
## Honest classification of Exchange.lean theorems

| Theorem | What it proves | Physics status |
|---|---|---|
| kink_exchange_neg | ExteriorAlgebra generators anticommute (ι_add_mul_swap) | Tautology — assumes fermionic stats |
| kink_pauli_exclusion | ExteriorAlgebra generators square to 0 (ι_sq_zero) | Tautology — assumes fermionic stats |
| kink_hbt_dip | Alias of kink_pauli_exclusion | Tautology — identical to above |
| kink_three_mode_consistency | Associativity + exchange propagate correctly | Corollary — follows from the tautologies |

None of these theorems derive fermionic statistics from the sine‑Gordon
bosonic commutator.  They are all algebraic identities about the
ExteriorAlgebra type, which has fermionic anticommutation built into its
definition.

The physics derivation is in:
- dynamics_lean/Bridge.lean: 6 genuine Lean theorems (0 unresolved goals, 0 extra assumptions); BCH exchange identity numerically verified in `numerical/sMatrix_verify.py`
- ../bridge.md §2: Full analytical derivation of the exchange phase
- ../gate_free_fermion_check.md: Free‑fermion limit gate check

A proof that ιx·ιy = −ιy·ιx in an ExteriorAlgebra does NOT prove that
sine‑Gordon kink creation operators anticommute.  That is a statement
about quantum field operators, not about algebraic data types.
-/

end SGExchange
