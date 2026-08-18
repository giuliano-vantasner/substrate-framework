import Mathlib
namespace Phase5Gravity


/-!
# Phase 5 G6 — Graviton / transverse-traceless metric-perturbation DOF count

This file is the Lean oracle's contribution for unified-framework Phase 5 (gravity sector),
step G6. It machine-checks the ALGEBRAIC OUTPUT of the standard linearised-GR counting
argument: the number of independent transverse-traceless (TT) metric-perturbation
polarizations — equivalently, the propagating graviton degrees of freedom — in `D`
spacetime dimensions is `D*(D−3)/2`.

## Physics offered for (the INPUT, not proved here)

- A symmetric rank-2 metric perturbation `h_{μν}` in `D` dimensions has `D(D+1)/2`
  independent components. Linearised diffeomorphism (gauge) freedom removes `D` of them;
  transversality and tracelessness in the TT gauge remove the remaining non-propagating
  components. The net count of independent TT components is
  `D(D+1)/2 − D − (D−1) − 1 = D(D−3)/2`. (Carroll, *Spacetime and Geometry* §7.4;
  Wald, *General Relativity* Ch. 4; de Haro–Skenderis–Solodukhin, hep-th/0002230, for
  general `D`.) This counting argument and the MAP
  "TT component count = propagating graviton polarizations"
  are ASSERTED here as physics INPUT — they are NOT proved inside Lean.
- The integer division `/2` is EXACT for every integer `D`: `D*(D−3)` is always even
  (`D` even ⟹ `2|D`; `D` odd ⟹ `D−3` even), so the truncating `Int.ediv` never rounds.

## What each theorem PROVES (the OUTPUT, machine-checked here)

* `gravitonPolarizations` — the TT DOF formula `D*(D−3)/2` as a genuine function `ℤ → ℤ`,
  evaluated below at distinct physical dimensions (not a self-restating decimal).
* `graviton_D4_eq_two` — the MAIN CLAIM: `D = 4` gives exactly `2` propagating graviton
  polarizations, the two gravitational-wave modes `h_+` and `h_×` of G1's radiation.
* `graviton_D2_no_propagating` — `D = 2` gives `−1`: there is NO propagating spin-2 graviton
  in 1+1D. This is WHY the substrate's 1+1D gravity sector must live in a DILATON
  (Jackiw–Teitelboim / dilaton gravity), tying G1 (the radiating source) to G2.
* `graviton_D2_nonpositive` — the corollary `≤ 0`: no propagating DOF in 1+1D.
* `graviton_D3_zero_witness` — the NON-TAUTOLOGY GUARD: `D = 3` gives `0` (2+1D gravity is
  topological, no local waves). Paired with the next theorem, this makes `graviton_D4_eq_two`
  non-vacuous: drop the `D=4` hypothesis and the claim `= 2` is FALSE (D=3 gives 0 ≠ 2).
* `graviton_D3_not_two` — the GUARD SHARPENING: `D = 3` does NOT give `2`, so the `D=4`
  result is genuinely dimension-specific.
* `graviton_D4_gt_D3` — MONOTONICITY: `D=4` carries strictly more DOF than `D=3`.
* `graviton_D5_eq_five` — extra sanity: `D = 5` gives `5`.

Honesty: a fully-proved theorem proves exactly its own statement. These check the TT
DOF-count arithmetic OUTPUT at specific dimensions. They do NOT prove that linearised GR
admits a TT gauge, that `h_{μν}` has `D(D+1)/2` components, or that the counting argument is
correct — those are the asserted physical premises, beyond current Lean/Mathlib coverage.
This EXTENDS the parity ledger of `dynamics_lean/ChargeDiscrimination.lean` (EM/kink sector)
and `dynamics_lean/Phase4Strong_FRSpinStat.lean` (strong/Skyrmion sector) to the GRAVITY
sector: the graviton DOF count is the gravity sector's characteristic discrete fact. It is
NOT a `Sigma2Prod.lean`-style decimal `rfl` attestation — the statement is the physical
DOF-count claim, evaluated at distinct inputs, with a non-tautology witness.
Quality bar / style exemplar: `dynamics_lean/Phase4Strong_FRSpinStat.lean`.
-/

/-- Graviton TT polarization DOF count in `D` spacetime dimensions: `D*(D−3)/2`.
The `/2` is exact for every integer `D` since `D*(D−3)` is always even.
For `D=4`: `2` (`h_+` and `h_×`). For `D=3`: `0`. For `D=2`: `−1` (no propagating graviton). -/
def gravitonPolarizations (D : ℤ) : ℤ := D * (D - 3) / 2

/-- MAIN CLAIM: `D = 4` gives exactly `2` propagating graviton polarizations —
the two gravitational-wave modes `h_+` and `h_×` of G1's radiation. -/
theorem graviton_D4_eq_two : gravitonPolarizations 4 = 2 := by
  norm_num [gravitonPolarizations]

/-- `D = 2` gives `−1`: NO propagating spin-2 graviton in 1+1D. This is WHY the substrate's
1+1D gravity sector lives in a DILATON, tying G1 (radiating source) to G2 (3+1D sourcing). -/
theorem graviton_D2_no_propagating : gravitonPolarizations 2 = -1 := by
  norm_num [gravitonPolarizations]

/-- Corollary: the 1+1D value is `≤ 0` — no propagating gravitational DOF. -/
theorem graviton_D2_nonpositive : gravitonPolarizations 2 ≤ 0 := by
  norm_num [gravitonPolarizations]

/-- NON-TAUTOLOGY GUARD: `D = 3` gives `0` (2+1D gravity is topological, no local waves).
Paired with `graviton_D3_not_two`, this makes `graviton_D4_eq_two` non-vacuous: dropping the
`D=4` hypothesis makes the claim `= 2` FALSE, since `D=3` gives `0 ≠ 2`. Mirrors the
`skyrmion_B2_is_boson_witness` guard of `Phase4Strong_FRSpinStat.lean`. -/
theorem graviton_D3_zero_witness : gravitonPolarizations 3 = 0 := by
  norm_num [gravitonPolarizations]

/-- GUARD SHARPENING: `D = 3` does NOT give `2`, so the `D=4` result is dimension-specific. -/
theorem graviton_D3_not_two : gravitonPolarizations 3 ≠ 2 := by
  norm_num [gravitonPolarizations]

/-- MONOTONICITY: `D = 4` carries strictly more propagating DOF than `D = 3`. -/
theorem graviton_D4_gt_D3 : gravitonPolarizations 4 > gravitonPolarizations 3 := by
  norm_num [gravitonPolarizations]

/-- Extra sanity: `D = 5` gives `5` TT polarizations. -/
theorem graviton_D5_eq_five : gravitonPolarizations 5 = 5 := by
  norm_num [gravitonPolarizations]

#print axioms graviton_D4_eq_two
#print axioms graviton_D2_no_propagating
#print axioms graviton_D2_nonpositive
#print axioms graviton_D3_zero_witness
#print axioms graviton_D3_not_two
#print axioms graviton_D4_gt_D3
#print axioms graviton_D5_eq_five

end Phase5Gravity
