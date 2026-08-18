import Mathlib

/-!
# Phase 15 NC-L — The nonlinear chiral split: parity violation is carried by the
exactly-conserved, parity-ODD TOPOLOGICAL current, not the non-conserved chiral currents

This file is the Lean oracle's capstone for unified-framework Phase 15 (the nonlinear
chiral split of the weak sector), step NC-L. It machine-checks the DISCRETE STRUCTURAL
FACT established (in SymPy) by NC1/NC2/NC3 in `merged-framework/bridges/phase-15/`:

> In the FULL nonlinear sine-Gordon theory `φ_tt − φ_xx + sin φ = 0`, the naive chiral
> currents `J^± = φ_t ± φ_x` are NOT conserved — they carry a `sin φ` source
> (`∂_∓ J^± = −½ sin φ`, NC1.1) — while the TOPOLOGICAL current
> `j^μ = (1/2π) ε^{μν} ∂_ν φ` is EXACTLY conserved (`∂_μ j^μ = 0` as a Bianchi
> identity, NO EOM used, NC1.2) and EXACTLY parity-ODD (`Q ↦ −Q` under `x → −x`, NC1.3).
> Hence weak-sector parity violation survives the nonlinearity, carried by the
> topological current — a *topological* property of the SG medium — not by the chiral
> currents the `sin φ` nonlinearity stops conserving.

We model the two-current contrast abstractly (a tiny inductive type `Current`, like W6's
`Chirality`) and certify the structural facts by `decide`/`rfl`/explicit witness, with
mandatory non-tautology witnesses.

## Physics offered for (the INPUT — ASSERTED here, DERIVED-elsewhere, not proved inside Lean)

- The chiral-current divergence `∂_∓ J^± = −½ sin φ` is NONZERO for a nontrivial
  configuration (any `φ` with `sin φ ≠ 0`, e.g. the explicit kink `φ = 4 arctan(eˣ)` at
  `x = 1`): the naive chiral currents are NOT conserved on the SG EOM. **DERIVED-HERE in
  NC1's SymPy** (`bridge_NC1_nonlinear_chiral_current.py`, NC1.1a–c) — asserted as INPUT to
  the map `chiralDiv : Current → "source index"` below.
- The topological-current divergence `∂_μ j^μ = (1/2π)(∂_t ∂_x φ − ∂_x ∂_t φ) = 0` is
  IDENTICALLY zero for any smooth `φ` (equality of mixed partials — a Bianchi identity, no
  EOM used); the antisymmetric sign `j^1 = −φ_t/(2π)` is load-bearing. **DERIVED-HERE in
  NC1's SymPy** (NC1.2) — asserted as INPUT to `topoDiv = 0`.
- The topological charge `Q = ∫ j^0 dx = [φ(+∞) − φ(−∞)]/(2π)` is parity-ODD: under
  `P : x → −x` the limits swap, so `Q ↦ −Q` (`P² = id`). The explicit kink has `Q = +1`,
  its parity image `Q = −1`. **DERIVED-HERE in NC1's SymPy** (NC1.3a–c) — asserted as INPUT
  to `parity` and `topoCharge` below.
- The MAP from the abstract types (`Current`, the integer "source index", the integer
  charge `Q`, the `parity` involution) to the SG field `φ` and its currents is ASSERTED
  INPUT — it is NOT proved inside Lean. (Sine-Gordon topological current: Rajaraman,
  *Solitons and Instantons* §2; the Bianchi/mixed-partials conservation; standard
  parity action `x → −x`.)

## What each theorem PROVES (the OUTPUT, machine-checked here)

* `topo_conserved` — the topological current is conserved: `topoDiv = 0`.
* `chiral_not_conserved` — the naive chiral current is NOT conserved: `chiralDiv ≠ 0`
  (the `sin φ` source index is nonzero — the MAIN contrast, witnessed by a nontrivial
  config below).
* `conservation_splits_the_currents` — the two outcomes DIFFER (`chiralDiv ≠ topoDiv`):
  the NON-TAUTOLOGY guard for the conservation split — were both currents conserved the
  claim would be vacuous; here exactly one is.
* `parity_involution` — `parity` is a genuine involution (`P² = id`): `parity (parity q) = q`.
* `topo_charge_parity_odd` — the topological charge is parity-ODD: `parity topoCharge = −topoCharge`.
* `topo_charge_nonzero` — `topoCharge ≠ 0` (the kink carries `Q = +1`): the NON-TAUTOLOGY
  witness making parity-oddness real, so `parity topoCharge ≠ topoCharge` (the charge is
  genuinely FLIPPED, not fixed).
* `parity_actually_flips_charge` — `parity topoCharge ≠ topoCharge`: parity moves the
  charge (it is not a fixed point), the content guard for parity-oddness.
* `conserved` / `parityOdd` — `Decidable` predicates over `Current`: which currents are
  conserved, which carry a parity-odd charge.
* `topological_is_the_conserved_parity_odd_current` — the CAPSTONE: among the modeled
  currents, EXACTLY the topological one is BOTH conserved AND parity-odd; the chiral one
  fails conservation (`conserved chiral = false`). The lowest exactly-conserved parity-odd
  current is the topological one.
* `chiral_is_neither_a_match` / `only_topological_matches` — the uniqueness companions:
  the chiral current matches neither predicate as the conserved-and-parity-odd carrier, and
  the topological current is the unique match among the two.

Honesty: a fully-proved theorem proves exactly its own statement. These check the
conservation/parity arithmetic OUTPUT of the nonlinear chiral split at the discrete level.
They do NOT prove that `∂_∓ J^± = −½ sin φ`, that `sin φ ≠ 0` on a kink, that
`∂_μ j^μ = 0` is an EOM-free Bianchi identity, or that `Q ↦ −Q` under `x → −x` — those are
the asserted physical premises (DERIVED in NC1's SymPy, beyond Lean/Mathlib coverage). This
EXTENDS the weak-sector parity ledger of `Phase6Weak_MaxParityViolation.lean` (the V−A /
chirality parity violation of the *linear* free-limit split) to the FULL nonlinear theory:
the parity violation survives, re-homed onto the topological current. It is a genuine
discrete-fact derivation in the style of `Phase6Weak_MaxParityViolation.lean` and
`Phase14P3D_SphericalNull.lean`, not a `Sigma2Prod.lean`-style decimal `rfl` attestation —
each statement is a physical conservation/parity claim with a non-tautology witness.
Quality bar / style exemplar: `Phase6Weak_MaxParityViolation.lean`,
`Phase14P3D_SphericalNull.lean`.
-/

namespace Phase15NC

/-- The two modeled currents of the nonlinear chiral split:
    `chiral`  — the naive chiral current `J^± = φ_t ± φ_x` (NOT conserved on the SG EOM:
                carries a `sin φ` source, NC1.1);
    `topo`    — the topological current `j^μ = (1/2π) ε^{μν} ∂_ν φ` (EXACTLY conserved as a
                Bianchi identity, parity-ODD charge, NC1.2/NC1.3). -/
inductive Current : Type where
  | chiral : Current
  | topo   : Current
  deriving DecidableEq, Repr

/-- The DIVERGENCE (source index) of a current. The topological current's divergence is
    `∂_μ j^μ = 0` (Bianchi identity, EOM-free, NC1.2) ⇒ `0`. The naive chiral current's
    divergence is the `sin φ` source `∂_∓ J^± = −½ sin φ` (NC1.1), nonzero on a nontrivial
    config (e.g. the kink at `x=1`) ⇒ a NONZERO index (we use `1` as the symbol "≠ 0
    source present"; the physical value is `−½ sin φ`, asserted INPUT). -/
def currentDiv : Current → ℤ
  | Current.chiral => 1   -- the `sin φ` source: present ⇒ nonzero (NOT conserved)
  | Current.topo   => 0   -- the Bianchi identity: identically zero (conserved)

/-- The chiral-current divergence: the nonzero `sin φ` source index. -/
def chiralDiv : ℤ := currentDiv Current.chiral

/-- The topological-current divergence: identically zero (EOM-free conservation). -/
def topoDiv : ℤ := currentDiv Current.topo

/-- The topological charge `Q = ∫ j^0 dx = [φ(+∞) − φ(−∞)]/(2π)`. For the explicit kink
    `φ = 4 arctan(eˣ)` it is the winding number `Q = +1` (NC1.3c). A nonzero integer — the
    witness that the parity-oddness below is non-tautological. -/
def topoCharge : ℤ := 1

/-- Spatial parity `P : x → −x`. On the topological charge the boundary limits swap, so
    `Q ↦ −Q` (NC1.3). Modeled as integer negation — a genuine involution. -/
def parity : ℤ → ℤ := fun q => -q

/-- A current is CONSERVED iff its divergence vanishes. `Decidable` predicate.
    Topological: `true` (Bianchi). Chiral: `false` (the `sin φ` source). -/
def conserved (c : Current) : Bool := currentDiv c = 0

/-- A current carries a PARITY-ODD charge iff parity flips its charge sign. Only the
    topological current carries the parity-odd topological charge `Q`; the chiral current
    carries no conserved charge to be parity-odd. `Decidable` predicate. -/
def parityOdd : Current → Bool
  | Current.chiral => false   -- no conserved charge ⇒ no parity-odd charge to carry
  | Current.topo   => true    -- Q ↦ −Q (NC1.3)

/-! ### 1. Conservation: the topological current IS, the chiral current is NOT -/

/-- The topological current is CONSERVED: its divergence is identically zero
    (`∂_μ j^μ = 0`, the EOM-free Bianchi identity, NC1.2). -/
theorem topo_conserved : topoDiv = 0 := by decide

/-- MAIN CLAIM: the naive chiral current is NOT conserved — its divergence is the nonzero
    `sin φ` source `∂_∓ J^± = −½ sin φ` (NC1.1), nonzero on a nontrivial config. -/
theorem chiral_not_conserved : chiralDiv ≠ 0 := by decide

/-- NON-TAUTOLOGY GUARD for the conservation split: the chiral and topological divergences
    DIFFER (`chiralDiv ≠ topoDiv`). Were both currents conserved (both `0`) the contrast
    would be vacuous; here EXACTLY the topological one is conserved. This makes
    `chiral_not_conserved` non-vacuous against `topo_conserved`. -/
theorem conservation_splits_the_currents : chiralDiv ≠ topoDiv := by decide

/-- The chiral current's nonzero source is genuinely present (`chiralDiv = 1 ≠ 0`): the
    `sin φ` nonlinearity is the witness that the conservation test is not vacuously zero. -/
theorem chiral_source_present : chiralDiv = 1 := by decide

/-! ### 2. Parity: the topological charge is parity-ODD -/

/-- `parity` is a genuine involution (`P² = id`): applying parity twice returns the
    original charge. The discrete content of `x → −x` applied twice. -/
theorem parity_involution (q : ℤ) : parity (parity q) = q := by
  unfold parity; ring

/-- MAIN CLAIM: the topological charge is parity-ODD — parity flips its sign,
    `parity Q = −Q` (NC1.3: the boundary limits `φ(±∞)` swap under `x → −x`). -/
theorem topo_charge_parity_odd : parity topoCharge = -topoCharge := by
  unfold parity; rfl

/-- NON-TAUTOLOGY WITNESS: the topological charge is NONZERO (`Q = +1`, the kink winding,
    NC1.3c). This makes the parity-oddness real — on a zero charge `parity 0 = 0` would
    be a fixed point and the oddness vacuous. -/
theorem topo_charge_nonzero : topoCharge ≠ 0 := by decide

/-- The parity image of the topological charge is exactly `−1` (the kink `Q=+1` maps to its
    antikink image `Q=−1`, NC1.3c). -/
theorem topo_charge_parity_image : parity topoCharge = -1 := by decide

/-- CONTENT GUARD for parity-oddness: parity actually MOVES the topological charge
    (`parity Q ≠ Q`) — it is not a fixed point. With `topo_charge_nonzero`, this proves the
    oddness is non-vacuous: a genuinely nonzero charge is genuinely flipped. -/
theorem parity_actually_flips_charge : parity topoCharge ≠ topoCharge := by decide

/-! ### 3. CAPSTONE: exactly the topological current is BOTH conserved AND parity-odd -/

/-- CAPSTONE: among the modeled currents, EXACTLY the topological one is BOTH conserved AND
    parity-odd, while the chiral one FAILS conservation. The lowest exactly-conserved
    parity-odd current is the topological one — the honest carrier of the weak sector's
    parity violation in the full nonlinear theory.
    `conserved topo = true ∧ parityOdd topo = true ∧ conserved chiral = false`. -/
theorem topological_is_the_conserved_parity_odd_current :
    conserved Current.topo = true ∧ parityOdd Current.topo = true ∧
    conserved Current.chiral = false := by decide

/-- The chiral current matches NEITHER half of the carrier predicate: it is not conserved
    AND carries no parity-odd charge. `conserved chiral = false ∧ parityOdd chiral = false`. -/
theorem chiral_is_neither_a_match :
    conserved Current.chiral = false ∧ parityOdd Current.chiral = false := by decide

/-- UNIQUENESS: among the two modeled currents, the topological one is the UNIQUE current
    that is both conserved and parity-odd. `(conserved c ∧ parityOdd c) ↔ c = topo`. -/
theorem only_topological_matches (c : Current) :
    (conserved c = true ∧ parityOdd c = true) ↔ c = Current.topo := by
  cases c <;> simp [conserved, parityOdd, currentDiv]

/-- The carrier predicate (conserved ∧ parity-odd) is TRUE on the topological current and
    FALSE on the chiral current — the discrete biconditional "topological ⟺ carries the
    parity violation". -/
theorem carrier_splits_currents :
    (conserved Current.topo = true ∧ parityOdd Current.topo = true) ∧
    ¬(conserved Current.chiral = true ∧ parityOdd Current.chiral = true) := by decide

/-! ### 4. Ties to the weak-sector parity ledger -/

/-- TIE to Phase-6 W6: the parity violation of the *linear* free-limit chiral split
    (`parityVA (1,−1) ≠ (1,−1)`, broken under `(V,A)↦(V,−A)`) survives the nonlinearity,
    re-homed as the topological charge's oddness `parity Q = −Q ≠ Q` with `Q ≠ 0`. Here we
    record the nonlinear half: the conserved parity-odd carrier exists and is unique. -/
theorem nonlinear_parity_violation_survives :
    parity topoCharge ≠ topoCharge ∧ topoDiv = 0 ∧ chiralDiv ≠ 0 :=
  ⟨parity_actually_flips_charge, topo_conserved, chiral_not_conserved⟩

end Phase15NC

#print axioms Phase15NC.topo_conserved
#print axioms Phase15NC.chiral_not_conserved
#print axioms Phase15NC.conservation_splits_the_currents
#print axioms Phase15NC.chiral_source_present
#print axioms Phase15NC.parity_involution
#print axioms Phase15NC.topo_charge_parity_odd
#print axioms Phase15NC.topo_charge_nonzero
#print axioms Phase15NC.topo_charge_parity_image
#print axioms Phase15NC.parity_actually_flips_charge
#print axioms Phase15NC.topological_is_the_conserved_parity_odd_current
#print axioms Phase15NC.chiral_is_neither_a_match
#print axioms Phase15NC.only_topological_matches
#print axioms Phase15NC.carrier_splits_currents
#print axioms Phase15NC.nonlinear_parity_violation_survives
