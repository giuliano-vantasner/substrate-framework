import Mathlib
namespace Phase19OM1


/-!
# Phase 19 OM1-L — The single Z₂ character: `χ(1)=−1`, `χ(1+1)=+1`, `χ ≠ 1`

This file is the Lean oracle's contribution for unified-framework Phase 19, step OM1-L.
It machine-checks the DISCRETE-FACT OUTPUT behind OM1's "identity collapse": four (or
five) independently-built oracles each produce the topological `−1` (the pulson holonomy
`holonomy(1/2,1)`, the SU(2)_L Wilson-loop eigenvalue at a 2π loop, the RP² Berry holonomy
`exp(i∮A_eff)`, and the Lean fermion parity `(−1)^|Q|`), and OM1 asserts they are the SAME
object: the value on the generator of the UNIQUE nontrivial character of Z₂. This file
certifies the group-theoretic fact that makes that collapse an identity rather than four
numerical coincidences — the unique nontrivial character `χ : ZMod 2 →* ℤˣ` satisfies
`χ(1)=−1` on the generator, `χ(1+1)=χ(0)=+1` on its square (the homomorphism law), and is
distinct from the trivial character (which gives `+1` on the generator).

## Physics offered for (the INPUT, not proved here)

- Each oracle's expression equals `−1` by its OWN machinery: the pulson spinor holonomy of
  one odd encirclement of a strength-1/2 RP² disclination (`merged-framework/bridges/phase-1/`
  `bridge_T1Z2_same_minus_one.py`, `holonomy(1/2,1)=exp(iπ)=−1`); the SU(2)_L Wilson loop
  eigenvalue at a 2π internal-rotation loop (`bridge_NA1_su2L_wilson_loop.py`,
  `W_2π=exp(iπσ₃)=−I₂`, the Z₂ center); the RP² disclination Berry holonomy
  (`bridge_B1_disclination_berry_connection.py`, `exp(i∮A_eff)=exp(iπ)=−1`); and the Lean
  fermion parity `(−1)^|Q|` (the CANONICAL `fermionParity` is at
  `sg-breather-ionization/formalization/Formalization.lean:158`, with
  `fermionParity_one : fermionParity 1 = −1` at ~line 181 and the order-2 identity
  `fermionParity_sq_eq_one : fermionParity Q * fermionParity Q = 1` at ~line 164). These
  physical equalities are the ASSERTED INPUT — they are NOT re-derived inside Lean here.
- The IDENTIFICATION "each oracle's `−1` is the value `χ(1)` of the unique nontrivial Z₂
  character, defined homomorphically" is the OM1 physics map, asserted as input.
- This file does NOT duplicate `fermionParity`; it cites the canonical definition and
  re-proves only the abstract Z₂-character arithmetic that OM1's collapse rests on.

## What each theorem PROVES (the OUTPUT, machine-checked here)

* `chiF` — the unique nontrivial character `ZMod 2 →* ℤˣ`, `0 ↦ +1`, `1 ↦ −1`, packaged as
  a genuine `MonoidHom` (so `map_one'`/`map_mul'`, the homomorphism law, are part of its type).
* `chiF_generator` — the MAIN CLAIM on the generator: `χ(1) = −1`. This is the value every
  oracle computes.
* `chiF_double` — the homomorphism law / discriminant: `χ(1+1) = χ(0) = +1`. Because
  `(1:ZMod 2)+1 = 0`, this is forced by `χ` being a homomorphism and is the SAME fact as the
  pulson double-encirclement `holonomy(1/2,2)=+1`, the 4π Wilson loop `+I₂`, and the Lean
  `fermionParity_sq_eq_one`. It is what makes `−1` an order-2 sign, not a free choice.
* `chiF_nontrivial` — `χ(1) ≠ 1`: the character is genuinely nontrivial on the generator.
* `chiF_double_is_square` — the homomorphism law read explicitly as `χ(1) * χ(1) = +1`
  ( = `(−1)·(−1)`), tying the discriminant to the squared generator value.
* `trivialChar_generator` — the NON-TAUTOLOGY GUARD: the trivial character `1 : ZMod 2 →* ℤˣ`
  gives `+1` on the generator. So `χ(1) = −1` is NOT true of every character — it is the
  defining feature of the nontrivial one. If the oracles' shared object were the trivial
  character, every reading would be `+1`, contradicting the observed `−1`.
* `chiF_ne_trivial` — compound guard: the nontrivial and trivial characters DISAGREE on the
  generator (`−1 ≠ +1`), so OM1's `−1` selects the nontrivial character uniquely.
* `chiF_is_unique_nontrivial` — the order-2 fact: ANY monoid hom `ZMod 2 →* ℤˣ` whose value
  on the generator is `≠ 1` must equal `chiF`. This is the "unique nontrivial character"
  statement — there is exactly one, so the four oracles cannot be landing on different
  Z₂ characters; they land on this one.

Honesty: a fully-proved theorem proves exactly its own statement. These check the
Z₂-character arithmetic OUTPUT of the OM1 collapse. They do NOT prove that the pulson
holonomy, the Wilson eigenvalue, the Berry phase, or the fermion parity each equal `χ(1)` —
those oracle-by-oracle equalities are the asserted physical input (verified numerically in
the SymPy bridges T1-Z2 / NA1 / B1 and via `fermionParity_one` in `Formalization.lean`).
This EXTENDS the parity ledger of `dynamics_lean/ChargeDiscrimination.lean` (kink/antikink
fermion parity), `dynamics_lean/Phase4Strong_FRSpinStat.lean` (Skyrmion spin-statistics),
and `dynamics_lean/Phase6Weak_MaxParityViolation.lean` (V−A parity violation): all of those
`−1`'s are the value of THIS character on the generator, and the uniqueness theorem here is
why they collapse to one object. Quality bar / style exemplar:
`dynamics_lean/Phase4Strong_FRSpinStat.lean`.
-/

/-- The unique nontrivial character of `Z₂ = ZMod 2` into the units `ℤˣ = {+1,−1}`:
`0 ↦ +1` (identity), `1 ↦ −1` (generator). Packaged as a `MonoidHom` so the homomorphism
law `χ(a+b)=χ(a)·χ(b)` is part of its type (here the source's `+` is the Z₂ group operation,
sent to `·` in `ℤˣ`). The value `−1` on the generator is the OM1 `−1`. -/
def chiF : Multiplicative (ZMod 2) →* ℤˣ where
  toFun n := if (n.toAdd = 0) then 1 else -1
  map_one' := by decide
  map_mul' := by decide

/-- MAIN CLAIM: the character's value on the generator is `−1`.
This is the single `−1` that the pulson holonomy, the SU(2)_L Wilson eigenvalue, the RP²
Berry holonomy, and the fermion parity each compute by their own machinery. -/
theorem chiF_generator : chiF (Multiplicative.ofAdd 1) = -1 := by decide

/-- The homomorphism law / discriminant: `χ(1+1) = χ(0) = +1`. In `Multiplicative (ZMod 2)`
the squared generator is the identity (`ofAdd 1 * ofAdd 1 = ofAdd 0 = 1`), so this is forced
by `χ` being a homomorphism: `χ(g²)=χ(g)²=(−1)²=+1`. This is the SAME order-2 fact as the
pulson double-encirclement `holonomy(1/2,2)=+1`, the 4π Wilson loop `+I₂`, and the Lean
`fermionParity_sq_eq_one`. It is what makes `−1` an order-2 sign rather than a free phase. -/
theorem chiF_double :
    chiF (Multiplicative.ofAdd 1 * Multiplicative.ofAdd 1) = 1 := by decide

/-- The discriminant read explicitly as the squared generator value `χ(1)·χ(1) = +1`
( = `(−1)·(−1)`), via the homomorphism law `map_mul`. Ties `chiF_double` to `(−1)²`. -/
theorem chiF_double_is_square :
    chiF (Multiplicative.ofAdd 1) * chiF (Multiplicative.ofAdd 1) = 1 := by
  rw [chiF_generator]; decide

/-- The character is genuinely nontrivial: its value on the generator is `≠ 1`. -/
theorem chiF_nontrivial : chiF (Multiplicative.ofAdd 1) ≠ 1 := by decide

/-- NON-TAUTOLOGY GUARD: the TRIVIAL character `1 : Multiplicative (ZMod 2) →* ℤˣ` sends the
generator to `+1`, NOT `−1`. So `χ(1) = −1` is not automatic for every character — it is the
defining feature of the nontrivial one. If the oracles' shared object were the trivial
character, every reading would be `+1`, contradicting the observed `−1`. -/
theorem trivialChar_generator :
    (1 : Multiplicative (ZMod 2) →* ℤˣ) (Multiplicative.ofAdd 1) = 1 := by decide

/-- Compound guard: the nontrivial and trivial characters DISAGREE on the generator
(`−1 ≠ +1`). This is why OM1's observed `−1` selects the nontrivial character — the `−1`
is a genuine discriminant between the two characters of Z₂, not shared by both. -/
theorem chiF_ne_trivial :
    chiF (Multiplicative.ofAdd 1) ≠ (1 : Multiplicative (ZMod 2) →* ℤˣ) (Multiplicative.ofAdd 1) := by
  decide

/-- The "unique nontrivial character" fact: ANY monoid hom `Multiplicative (ZMod 2) →* ℤˣ`
that is nontrivial on the generator (value `≠ 1`) must EQUAL `chiF`. Hence Z₂ has exactly one
nontrivial character, so the four oracles' `−1`'s cannot be landing on different Z₂
characters — they land on this one. (Proved by extensionality over the two elements of Z₂,
using the homomorphism law to pin the value on `1` from the value on the generator.) -/
theorem chiF_is_unique_nontrivial
    (ψ : Multiplicative (ZMod 2) →* ℤˣ)
    (hψ : ψ (Multiplicative.ofAdd 1) ≠ 1) :
    ψ = chiF := by
  -- The generator value of ψ is `≠ 1` in `ℤˣ = {±1}`, hence `= −1`.
  have hgen : ψ (Multiplicative.ofAdd 1) = -1 := by
    have hsign : ∀ u : ℤˣ, u ≠ 1 → u = -1 := by decide
    exact hsign _ hψ
  -- It suffices to check agreement on each of the two elements of `Multiplicative (ZMod 2)`,
  -- which are exactly `ofAdd 0 = 1` (identity) and `ofAdd 1` (generator). Reduce to the
  -- underlying `ZMod 2` value and case on it.
  apply MonoidHom.ext
  intro x
  obtain ⟨a, rfl⟩ : ∃ a : ZMod 2, Multiplicative.ofAdd a = x := ⟨Multiplicative.toAdd x, rfl⟩
  -- Every `a : ZMod 2` is `0` (identity) or `1` (generator).
  fin_cases a
  · -- a = 0: `ofAdd 0` is the identity, both homs send it to `1`.
    show ψ (Multiplicative.ofAdd (0 : ZMod 2)) = chiF (Multiplicative.ofAdd (0 : ZMod 2))
    have e0 : (Multiplicative.ofAdd (0 : ZMod 2)) = 1 := rfl
    rw [e0, map_one, map_one]
  · -- a = 1: ψ gives −1 (hgen), chiF gives −1 (chiF_generator).
    show ψ (Multiplicative.ofAdd (1 : ZMod 2)) = chiF (Multiplicative.ofAdd (1 : ZMod 2))
    rw [hgen, chiF_generator]

#print axioms chiF_generator
#print axioms chiF_double
#print axioms chiF_double_is_square
#print axioms chiF_nontrivial
#print axioms trivialChar_generator
#print axioms chiF_ne_trivial
#print axioms chiF_is_unique_nontrivial

end Phase19OM1
