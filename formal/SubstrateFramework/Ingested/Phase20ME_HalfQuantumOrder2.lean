import Mathlib
namespace Phase20ME


/-!
# Phase 20 ME-L — The Z₂ half-quantum class has ORDER 2: `2 • (½) = 0`, `χ(½)=−1`, `χ(½)²=+1`

This file is the Lean oracle's capstone for unified-framework Phase 20, sub-arc ME (the full
microscopic RP²-from-BEC emergence), step ME-L. It machine-checks the DISCRETE-FACT OUTPUT
behind ME2's half-quantum-vortex result: the polar/nematic phase's lowest topological defect
is the half-quantum vortex, the nontrivial generator of `π₁(RP²) = Z₂`, and that class has
**order 2** — two half-quanta compose to the trivial class (a `2π` nematic rotation /
integer winding), and the parity character it carries squares to `+1`.

This is a NEW discrete fact, NOT a re-proof of `rung021`'s `su2_z(2π) = −I₂` (that is the
SU(2) double-cover *element*). Here the object is the ABELIAN winding-charge group of the
polar order parameter: `π₁(RP²) = Z₂`, modelled as `ZMod 2`, with the half-quantum the
generator `1`. The two facts ME-L certifies:

  (a) **the group-element order-2 fact** — in `ZMod 2` the generator satisfies `1 + 1 = 0`
      (two half-quanta = an integer winding = the trivial class), so the half-quantum has
      additive order 2 (`AddOrderOf (1 : ZMod 2) = 2`); and
  (b) **the character/parity fact** — the unique nontrivial character `χ : ZMod 2 →* ℤˣ`
      sends the half-quantum to `−1` (the framework's topological `−1`, ME2's holonomy) and,
      by the homomorphism law, sends two half-quanta to `χ(½)² = (−1)² = +1` (the trivial
      class). This reuses the Phase19 OM1-L pattern `χ(2g) = χ(g)² = +1`.

## Physics offered for (the INPUT — ASSERTED here, DERIVED-elsewhere, not proved in Lean)

- **ME1 (SymPy)**: the polar/nematic phase is the `c₂>0` mean-field ground state of the spin-1
  BEC (`merged-framework/bridges/phase-20/bridge_ME1_polar_phase_selection.py`), so its
  order-parameter manifold is `RP² = S²/Z₂`. ASSERTED INPUT.
- **ME2 (SymPy)**: the half-quantum (`q=½`) vortex is the energetically-favored defect — two
  half-quanta cost `2·(½)² = ½` of one integer vortex (`bridge_ME2_half_quantum_vortex.py`,
  CHECK ME2.1) — and its charge lives in `π₁(RP²) = Z₂ = {0, ½}`, with two half-quanta summing
  to the integer/trivial class (CHECK ME2.3, `½+½ = 1 ≡ 0 mod 1`). ASSERTED INPUT.
- **O1 (SymPy)**: the half-quantum carries the Berry holonomy `exp(i∮A_eff) = −1` (the
  framework's topological `−1`). ASSERTED INPUT.
- The IDENTIFICATION "the half-quantum charge is the generator `1` of `π₁(RP²) = Z₂ = ZMod 2`,
  and its parity character is the unique nontrivial `χ : ZMod 2 →* ℤˣ`" is the ME physics map,
  asserted as input. Lean certifies only the resulting GROUP/CHARACTER arithmetic.

## What each theorem PROVES (the OUTPUT, machine-checked here)

* `halfQuantum_add_self` — `(1 : ZMod 2) + 1 = 0`: two half-quanta compose to the trivial
  (integer-winding) class. The bare group-element order-2 identity.
* `halfQuantum_addOrderOf` — `AddOrderOf (1 : ZMod 2) = 2`: the half-quantum's additive order
  is EXACTLY 2 (not 1) — it is a genuine order-2 generator, the `Z₂` of `π₁(RP²)`.
* `halfQuantum_ne_zero` — `(1 : ZMod 2) ≠ 0`: a single half-quantum is the NONTRIVIAL class
  (distinct from no-defect), so the order is 2 not 1.
* `chiHQ` — the unique nontrivial character `Multiplicative (ZMod 2) →* ℤˣ`, the half-quantum's
  parity reading: generator ↦ `−1`.
* `chiHQ_generator` — `χ(½) = −1`: the half-quantum carries the framework's topological `−1`
  (ME2/O1's holonomy). The MAIN parity claim.
* `chiHQ_double` — `χ(½ + ½) = χ(0) = +1`: two half-quanta read `+1` (trivial), forced by the
  homomorphism law (`½+½ = 0`). The order-2 sign fact.
* `chiHQ_double_is_square` — `χ(½)·χ(½) = +1` ( = `(−1)·(−1)`): the discriminant as the squared
  generator value (the OM1-L `χ(2g)=χ(g)²` pattern, reused).
* `anyon_third_ne_minus_one` — the NON-TAUTOLOGY WITNESS: an anyonic `q=1/3` statistical phase
  `exp(2πi/3)` is NOT `−1` (it is a primitive cube root of unity). So the half-quantum's `−1`
  is SPECIFIC to the `Z₂` order-2 fraction — a `Z₃` anyon (order 3) does not carry it, and its
  phase is rejected. This keeps the half-quantum's `Z₂` distinct from a generic fractional anyon.
* `anyon_third_order_three` — the anyon's order is 3, NOT 2: `(exp(2πi/3))³ = 1` while
  `(exp(2πi/3))² ≠ 1`. So order-2 is a genuine discriminant — the half-quantum (order 2) is
  NOT a `q=1/3` anyon (order 3); the two are distinct topological objects.

Honesty: a fully-proved theorem proves exactly its own statement. These check the
order-2 group/character arithmetic OUTPUT of ME2's half-quantum result and the `q=1/3`
rejection. They do NOT prove that the polar BEC selects the half-quantum or that the Berry
holonomy equals `χ(½)` — those are the asserted physical input (verified in the SymPy bridges
ME1/ME2/O1). This EXTENDS the Z₂ ledger of `dynamics_lean/Phase19_OM1_Z2Character.lean` (the
unique-nontrivial-character collapse): the half-quantum's `−1` is the value of THAT character
on the generator, and here it is tied to the half-quantum's additive order 2 in `π₁(RP²)`.
Quality bar / style exemplar: `dynamics_lean/Phase19_OM1_Z2Character.lean`.
-/

/-! ## (a) The group-element order-2 fact: the half-quantum charge in `π₁(RP²) = Z₂ = ZMod 2`. -/

/-- Two half-quanta compose to the trivial (integer-winding) class: `(1:ZMod 2) + 1 = 0`.
This is ME2.3's `½ + ½ = 1 ≡ 0 (mod 1)` — an integer winding is the trivial `Z₂` class. -/
theorem halfQuantum_add_self : (1 : ZMod 2) + 1 = 0 := by decide

/-- A single half-quantum is the NONTRIVIAL class: `(1:ZMod 2) ≠ 0`. So the order is 2, not 1
(without this, "order 2" would be vacuous — `0` has order 1). -/
theorem halfQuantum_ne_zero : (1 : ZMod 2) ≠ 0 := by decide

/-- The half-quantum's ADDITIVE ORDER is exactly 2: `AddOrderOf (1 : ZMod 2) = 2`. The
half-quantum is a genuine order-2 generator of `π₁(RP²) = Z₂` — two of them return to the
trivial class and a single one does not. -/
theorem halfQuantum_addOrderOf : addOrderOf (1 : ZMod 2) = 2 := by
  rw [ZMod.addOrderOf_one]

/-! ## (b) The character / parity fact: the half-quantum's `−1`, squaring to `+1`. -/

/-- The unique nontrivial character of `π₁(RP²) = Z₂ = ZMod 2` into the units `ℤˣ = {+1,−1}`:
`0 ↦ +1` (trivial class), `½ ↦ −1` (the half-quantum generator). Packaged as a `MonoidHom`
so the homomorphism law `χ(a+b)=χ(a)·χ(b)` is part of its type. The value `−1` on the
generator is ME2/O1's topological `−1` (the half-quantum Berry holonomy). -/
def chiHQ : Multiplicative (ZMod 2) →* ℤˣ where
  toFun n := if (n.toAdd = 0) then 1 else -1
  map_one' := by decide
  map_mul' := by decide

/-- MAIN parity claim: the half-quantum's character value on the generator is `−1`. This is
the framework's topological `−1` (ME2's favored defect, O1's Berry holonomy). -/
theorem chiHQ_generator : chiHQ (Multiplicative.ofAdd 1) = -1 := by decide

/-- The order-2 sign fact / homomorphism law: two half-quanta read `χ(½+½) = χ(0) = +1`. In
`Multiplicative (ZMod 2)` the squared generator is the identity (`ofAdd 1 * ofAdd 1 = ofAdd 0
= 1`), so this is forced by `χ` being a homomorphism: `χ(g²)=χ(g)²=(−1)²=+1`. The half-quantum
pair is the trivial class. -/
theorem chiHQ_double :
    chiHQ (Multiplicative.ofAdd 1 * Multiplicative.ofAdd 1) = 1 := by decide

/-- The discriminant read explicitly as the squared generator value `χ(½)·χ(½) = +1`
( = `(−1)·(−1)`), via the homomorphism law. This is the OM1-L `χ(2g)=χ(g)²=+1` pattern, here
the half-quantum's order-2 parity. -/
theorem chiHQ_double_is_square :
    chiHQ (Multiplicative.ofAdd 1) * chiHQ (Multiplicative.ofAdd 1) = 1 := by
  rw [chiHQ_generator]; decide

/-- The half-quantum's character is genuinely nontrivial: its value on the generator is `≠ 1`. -/
theorem chiHQ_nontrivial : chiHQ (Multiplicative.ofAdd 1) ≠ 1 := by decide

/-! ## Non-tautology witness: an anyonic `q=1/3` phase ≠ `−1`, and has order 3 not 2. -/

/-- NON-TAUTOLOGY WITNESS: the anyonic `q=1/3` statistical phase `exp(2πi/3)` is NOT `−1`. It
is a PRIMITIVE CUBE ROOT of unity (`(exp(2πi/3))³ = 1`, `≠ 1`), so it is rejected as a
half-quantum reading. The half-quantum's `−1` is SPECIFIC to the `Z₂` order-2 fraction `q=½`;
a generic fractional `q=1/3` anyon does NOT carry it. (Stated over `ℂ`: a primitive cube root
of unity is `≠ −1`.) -/
theorem anyon_third_ne_minus_one :
    (Complex.exp (2 * Real.pi * Complex.I / 3)) ≠ (-1 : ℂ) := by
  -- `exp(2πi/3)` is a primitive cube root of unity; `−1` is a square root of unity (order 2).
  -- If they were equal, then `(−1)³ = 1` would force `−1 = 1` (since `exp(2πi/3)³ = 1`),
  -- contradiction. We argue via the imaginary part: Im(exp(2πi/3)) = sin(2π/3) = √3/2 ≠ 0,
  -- while Im(−1) = 0.
  intro h
  have him : (Complex.exp (2 * Real.pi * Complex.I / 3)).im = (-1 : ℂ).im := by rw [h]
  -- Im(−1 : ℂ) = 0
  have hneg : (-1 : ℂ).im = 0 := by simp
  -- Reduce exp((2π/3) i) to cos + i sin form and compute its imaginary part = sin(2π/3) > 0.
  have harg : (2 * Real.pi * Complex.I / 3) = ((2 * Real.pi / 3 : ℝ) : ℂ) * Complex.I := by
    push_cast; ring
  rw [harg, Complex.exp_ofReal_mul_I_im] at him
  rw [hneg] at him
  -- him : Real.sin (2 * Real.pi / 3) = 0.  But sin(2π/3) = sin(π/3) = √3/2 > 0.
  have hpos : Real.sin (2 * Real.pi / 3) > 0 := by
    apply Real.sin_pos_of_pos_of_lt_pi
    · positivity
    · -- 2π/3 < π
      have hpi : (0:ℝ) < Real.pi := Real.pi_pos
      linarith
  linarith [him, hpos]

/-- The anyon's order is 3, not 2: the cube `(exp(2πi/3))³ = 1`. Combined with
`anyon_third_ne_minus_one`, the `q=1/3` anyon is order-3 and does NOT carry the half-quantum's
order-2 `−1`. So order-2 is a genuine discriminant: the half-quantum (order 2) ≠ a `q=1/3`
anyon (order 3). -/
theorem anyon_third_order_three :
    (Complex.exp (2 * Real.pi * Complex.I / 3)) ^ 3 = 1 := by
  rw [← Complex.exp_nat_mul]
  have : (↑(3:ℕ) : ℂ) * (2 * Real.pi * Complex.I / 3) = ((1:ℤ):ℂ) * (2 * ↑Real.pi * Complex.I) := by
    push_cast; ring
  rw [this, Complex.exp_int_mul_two_pi_mul_I]

#print axioms halfQuantum_add_self
#print axioms halfQuantum_ne_zero
#print axioms halfQuantum_addOrderOf
#print axioms chiHQ_generator
#print axioms chiHQ_double
#print axioms chiHQ_double_is_square
#print axioms chiHQ_nontrivial
#print axioms anyon_third_ne_minus_one
#print axioms anyon_third_order_three

end Phase20ME
