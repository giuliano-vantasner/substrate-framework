import Mathlib
namespace Phase4Strong


/-!
# Phase 4 S6 — Finkelstein–Rubinstein spin-statistics for the Skyrmion

This file is the Lean oracle's contribution for unified-framework Phase 4 (strong sector),
step S6. It machine-checks the ALGEBRAIC OUTPUT of the Finkelstein–Rubinstein (1968)
spin-statistics argument: a Skyrmion of baryon number `B` carries fermion parity
`(−1)^|B|`, so `B` odd ⟹ fermion and `B` even ⟹ boson.

## Physics offered for (the INPUT, not proved here)

- Baryon number `B` = degree of the map `S³ → SU(2) ≅ S³` of the Skyrme field `U`;
  `B` is necessarily an integer by continuity of `U` on compact `S³`. This is the
  DEFINITION of `B`, asserted here — NOT proved (it needs π₃(S³)=ℤ, beyond Mathlib 4.28).
- Finkelstein–Rubinstein (1968), J. Math. Phys. 9 (1968) 1762: a Skyrmion of ODD `B`
  acquires phase `−1` under `2π` self-rotation (the spinor lift of `π₁(SO(3)) = ℤ₂`);
  the 3D spin-statistics theorem then forces EXCHANGE phase = spin phase = `−1` (fermion).
  A Skyrmion of EVEN `B` acquires `+1` (boson). This is the SAME ℤ₂ that the SymPy rung
  `rung021_spin_statistics_lock.py` (ALL 8 CHECKS PASS) locks into three independent gauges
  (wall sign, topological spin, exchange statistics), derived via two INDEPENDENT routes
  (SU(2) rotation matrix vs RP² deck element). Lean checks only the parity ARITHMETIC
  output of that argument: `(−1)^|B|`.

## What each theorem PROVES (the OUTPUT, machine-checked here)

* `skyrmionFermionParity` — the parity formula `(−1)^|B|`, mirroring
  `ChargeDiscrimination.lean`'s `fermionParity (Q : ℤ) := (-1)^Q.natAbs`; this is its
  strong-sector (1D kink → 3D Skyrmion) generalization, identical formula and proof shape.
* `skyrmion_odd_is_fermion` — the FR theorem: `B` odd ⟹ parity `= −1` (fermion).
* `skyrmion_even_is_boson` — the companion: `B` even ⟹ parity `= +1` (boson).
* `skyrmion_B2_is_boson_witness` — the NON-TAUTOLOGY GUARD: `B = 2` gives parity `+1`,
  the OPPOSITE conclusion to the odd case. If the `Odd B` hypothesis were dropped,
  `skyrmion_odd_is_fermion` would be FALSE (parity 2 = +1 ≠ −1), so the theorem is not
  vacuously true — it is a genuine biconditional B↔parity, not an identity true of everything.
* `skyrmion_B1_is_fermion` — the positive instance: `B = 1` (the nucleon) gives `−1`.
* `skyrmion_parity_charge_conjugate` — `B` and `−B` have the same parity (particle = antiparticle).

Honesty: a fully-proved theorem proves exactly its own statement. These check the parity
arithmetic OUTPUT of the FR argument. They do NOT prove that π₃(S³)=ℤ, that the Skyrme field
has an integer degree, or that π₁(SO(3))=ℤ₂ — those are the asserted physical premises,
beyond current Lean/Mathlib coverage. This EXTENDS the parity ledger of
`dynamics_lean/ChargeDiscrimination.lean` (the 1D Q=±1 kink fermion parity) to 3D Skyrmions
via the SAME `(-1)^natAbs` formula; it is NOT a `Sigma2Prod.lean`-style decimal `rfl`
attestation (the statement is the physics B↔fermion parity, with a non-tautology witness).
Quality bar / style exemplar: `dynamics_lean/ChargeDiscrimination.lean`.
-/

/-- Skyrmion fermion parity as a function of baryon number `B`: the FR formula `(−1)^|B|`.
Mirrors `fermionParity` in `ChargeDiscrimination.lean` (3D strong-sector generalization). -/
def skyrmionFermionParity (B : ℤ) : ℤ := (-1 : ℤ) ^ B.natAbs

/-- Finkelstein–Rubinstein: a Skyrmion of ODD baryon number is a FERMION (parity `−1`).
Proved via `Int.natAbs_odd` (B odd ↔ B.natAbs odd) and `Odd.neg_one_pow`. -/
theorem skyrmion_odd_is_fermion (B : ℤ) (hB : Odd B) : skyrmionFermionParity B = -1 := by
  unfold skyrmionFermionParity
  exact Odd.neg_one_pow (Int.natAbs_odd.mpr hB)

/-- Companion: a Skyrmion of EVEN baryon number is a BOSON (parity `+1`).
Proved via `Int.natAbs_even` and `Even.neg_one_pow`. -/
theorem skyrmion_even_is_boson (B : ℤ) (hB : Even B) : skyrmionFermionParity B = 1 := by
  unfold skyrmionFermionParity
  exact Even.neg_one_pow (Int.natAbs_even.mpr hB)

/-- NON-TAUTOLOGY GUARD: `B = 2` gives parity `+1` (boson). This is the opposite of the
odd-`B` conclusion, so `skyrmion_odd_is_fermion` is FALSE without its `Odd B` hypothesis —
the relation B↔parity is a genuine biconditional, not vacuously true. -/
theorem skyrmion_B2_is_boson_witness : skyrmionFermionParity 2 = 1 := by
  unfold skyrmionFermionParity; norm_num

/-- Positive instance: `B = 1` (the nucleon) is a fermion (parity `−1`). -/
theorem skyrmion_B1_is_fermion : skyrmionFermionParity 1 = -1 := by
  unfold skyrmionFermionParity; norm_num

/-- Charge conjugation: `B` and `−B` carry the same parity (particle = antiparticle). -/
theorem skyrmion_parity_charge_conjugate (B : ℤ) :
    skyrmionFermionParity B = skyrmionFermionParity (-B) := by
  unfold skyrmionFermionParity; simp [Int.natAbs_neg]

#print axioms skyrmion_odd_is_fermion
#print axioms skyrmion_even_is_boson
#print axioms skyrmion_B2_is_boson_witness
#print axioms skyrmion_B1_is_fermion
#print axioms skyrmion_parity_charge_conjugate

end Phase4Strong
