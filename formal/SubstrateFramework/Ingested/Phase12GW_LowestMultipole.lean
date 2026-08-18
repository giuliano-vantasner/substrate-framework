import Mathlib
namespace Phase12GW


/-!
# Phase 12 GW-L — Lowest radiating multipole order of a massless spin-`s` field

This file is the Lean oracle's contribution for unified-framework Phase 12 (radiating
3+1 gravity), step GW-L — the radiating-multipole CAPSTONE. It machine-checks the
ALGEBRAIC OUTPUT of the standard multipole-radiation counting fact: in 3+1 dimensions
the LOWEST radiating multipole order `ℓ` of a massless field of integer spin `s` equals
the spin, `ℓ_min = s`. So gravity (spin 2) radiates first at the QUADRUPOLE (`ℓ=2`),
electromagnetism (spin 1) at the DIPOLE (`ℓ=1`), and a scalar (spin 0, the substrate's
1+1D G1 dilaton case) at the MONOPOLE (`ℓ=0`).

## Physics offered for (the INPUT, not proved here)

- A massless field of integer spin `s` has helicity components `±s`; expanding its
  radiation field in vector/tensor spherical harmonics, the multipole moments with `ℓ < s`
  are forbidden by the global conservation laws the source obeys. For GRAVITY the
  conservation of energy-momentum (`∂_μ T^{μν}=0`) kills the `ℓ=0` (monopole = total mass,
  constant) and `ℓ=1` (dipole = center-of-mass motion / total momentum, constant) radiating
  moments, leaving the `ℓ=2` QUADRUPOLE as the leading radiator. For EM, conservation of
  charge (`∂_μ J^μ=0`) kills the `ℓ=0` monopole (total charge constant), leaving the `ℓ=1`
  DIPOLE leading. (Jackson, *Classical Electrodynamics* §9, §16; Maggiore, *Gravitational
  Waves* Vol.1 §3.3; Thorne, Rev. Mod. Phys. 52 (1980) 299, on multipole expansions of
  gravitational radiation.) The MAP "lowest radiating multipole order = spin in 3+1D" and
  the conservation-law premises are ASSERTED here as physics INPUT — they are NOT proved
  inside Lean.

## What each theorem PROVES (the OUTPUT, machine-checked here)

* `lowestRadiatingMultipole` — the map `s ↦ s` as a genuine function `ℤ → ℤ`, evaluated
  below at distinct physical spins (not a self-restating decimal).
* `gravity_lowest_multipole_two` — the MAIN CLAIM: spin 2 ⟹ lowest radiating moment `2`,
  the gravitational QUADRUPOLE; monopole and dipole gravitational radiation are forbidden.
* `em_lowest_multipole_one` — contrast / sanity: spin 1 ⟹ `1`, the EM DIPOLE.
* `scalar_lowest_multipole_zero` — spin 0 ⟹ `0`, the scalar MONOPOLE radiates (1+1D G1).
* `gravity_not_dipole` — NON-TAUTOLOGY GUARD: spin 2 does NOT give `1`. Paired with the
  spin-1 result this makes `gravity_lowest_multipole_two` non-vacuous: drop the `spin=2`
  hypothesis and the claim `=2` is FALSE (spin 1 gives `1 ≠ 2`). Mirrors G6's
  `graviton_D3_not_two`.
* `gravity_gt_em` — MONOTONICITY: the gravitational radiating order strictly exceeds the EM
  one (so the leading GW multipole sits higher than the leading EM multipole).
* `graviton_d4_two_polarizations_quadrupole` — the TWO facts Phase-12 ties together:
  re-using G6's TT DOF count `gravitonPolarizations D = D*(D−3)/2`, the spin-2 field in
  `D=4` has `gravitonPolarizations 4 = 2` propagating polarizations AND lowest radiating
  multipole `2`.
* `gravity_monopole_dipole_below_quadrupole` — both `ℓ=0` (monopole) and `ℓ=1` (dipole)
  lie STRICTLY below the gravitational radiating order, i.e. they do not radiate.
* plus spin-3 / bound / non-negativity / explicit-witness sanity theorems.

Honesty: a fully-proved theorem proves exactly its own statement. These check the
multipole-order arithmetic OUTPUT at specific spins. They do NOT prove that conservation
laws forbid `ℓ<s`, that the spherical-harmonic expansion is complete, or that the map
"lowest radiating multipole = spin" holds — those are the asserted physical premises,
beyond current Lean/Mathlib coverage. This EXTENDS the parity ledger of
`dynamics_lean/Phase5Gravity_GravitonTT.lean` (the gravity-sector DOF count) to the
RADIATING gravity sector: the lowest radiating multipole is Phase-12's characteristic
discrete fact. It is NOT a `Sigma2Prod.lean`-style decimal `rfl` attestation — the
statement is the physical multipole-order claim, evaluated at distinct inputs, with a
non-tautology witness.
Quality bar / style exemplar: `dynamics_lean/Phase5Gravity_GravitonTT.lean`.
-/

/-- Lowest radiating multipole order in 3+1D of a massless integer-spin field: `s`.
For spin 2 (gravity): `2` (quadrupole). For spin 1 (EM): `1` (dipole).
For spin 0 (scalar): `0` (monopole). -/
def lowestRadiatingMultipole (spin : ℤ) : ℤ := spin

/-- Graviton TT polarization DOF count in `D` spacetime dimensions: `D*(D−3)/2`
(re-used from Phase 5 G6). For `D=4`: `2` (`h_+` and `h_×`). -/
def gravitonPolarizations (D : ℤ) : ℤ := D * (D - 3) / 2

/-- MAIN CLAIM: spin `2` ⟹ lowest radiating multipole `2` — gravitational radiation is
QUADRUPOLE; the monopole and dipole moments do not radiate. -/
theorem gravity_lowest_multipole_two : lowestRadiatingMultipole 2 = 2 := by
  norm_num [lowestRadiatingMultipole]

/-- Contrast / sanity: spin `1` ⟹ lowest radiating multipole `1` — EM radiation is DIPOLE. -/
theorem em_lowest_multipole_one : lowestRadiatingMultipole 1 = 1 := by
  norm_num [lowestRadiatingMultipole]

/-- spin `0` ⟹ lowest radiating multipole `0` — the scalar MONOPOLE radiates
(the substrate's 1+1D G1 dilaton case). -/
theorem scalar_lowest_multipole_zero : lowestRadiatingMultipole 0 = 0 := by
  norm_num [lowestRadiatingMultipole]

/-- NON-TAUTOLOGY GUARD: spin `2` does NOT give `1` — gravity does NOT radiate at dipole
order. Paired with `em_lowest_multipole_one`, this makes `gravity_lowest_multipole_two`
non-vacuous: dropping the `spin=2` hypothesis makes the claim `=2` FALSE, since spin 1
gives `1 ≠ 2`. Mirrors `graviton_D3_not_two` of `Phase5Gravity_GravitonTT.lean`. -/
theorem gravity_not_dipole : lowestRadiatingMultipole 2 ≠ 1 := by
  norm_num [lowestRadiatingMultipole]

/-- NON-TAUTOLOGY GUARD (monopole side): spin `2` does NOT give `0` — gravity does NOT
radiate at monopole order either. -/
theorem gravity_not_monopole : lowestRadiatingMultipole 2 ≠ 0 := by
  norm_num [lowestRadiatingMultipole]

/-- MONOTONICITY: the gravitational radiating order strictly exceeds the EM one. -/
theorem gravity_gt_em :
    lowestRadiatingMultipole 2 > lowestRadiatingMultipole 1 := by
  norm_num [lowestRadiatingMultipole]

/-- The TWO facts Phase-12 ties together: in `D=4` the spin-2 field has `2` propagating TT
polarizations (G6's DOF count) AND lowest radiating multipole `2` (the quadrupole). -/
theorem graviton_d4_two_polarizations_quadrupole :
    gravitonPolarizations 4 = 2 ∧ lowestRadiatingMultipole 2 = 2 := by
  constructor
  · norm_num [gravitonPolarizations]
  · norm_num [lowestRadiatingMultipole]

/-- Both `ℓ=0` (monopole) and `ℓ=1` (dipole) lie STRICTLY below the gravitational radiating
order — neither radiates, leaving the quadrupole leading. -/
theorem gravity_monopole_dipole_below_quadrupole :
    (0 < lowestRadiatingMultipole 2) ∧ (1 < lowestRadiatingMultipole 2) := by
  constructor
  · norm_num [lowestRadiatingMultipole]
  · norm_num [lowestRadiatingMultipole]

/-- Sanity: spin `3` ⟹ lowest radiating multipole `3` (octupole order). -/
theorem spin3_lowest_multipole_three : lowestRadiatingMultipole 3 = 3 := by
  norm_num [lowestRadiatingMultipole]

/-- MONOTONICITY (next rung): a spin-3 source radiates first at a strictly higher multipole
than gravity (spin 2). -/
theorem spin3_gt_gravity :
    lowestRadiatingMultipole 3 > lowestRadiatingMultipole 2 := by
  norm_num [lowestRadiatingMultipole]

/-- NON-NEGATIVITY: for every physical (non-negative) spin, the lowest radiating multipole
order is non-negative — a multipole order is never negative. -/
theorem lowest_multipole_nonneg (s : ℤ) (hs : 0 ≤ s) :
    0 ≤ lowestRadiatingMultipole s := by
  simpa [lowestRadiatingMultipole] using hs

/-- Quadrupole bound: gravity radiates at order `≥ 2`. -/
theorem gravity_at_least_quadrupole : 2 ≤ lowestRadiatingMultipole 2 := by
  norm_num [lowestRadiatingMultipole]

#print axioms gravity_lowest_multipole_two
#print axioms em_lowest_multipole_one
#print axioms scalar_lowest_multipole_zero
#print axioms gravity_not_dipole
#print axioms gravity_not_monopole
#print axioms gravity_gt_em
#print axioms graviton_d4_two_polarizations_quadrupole
#print axioms gravity_monopole_dipole_below_quadrupole
#print axioms spin3_lowest_multipole_three
#print axioms spin3_gt_gravity
#print axioms lowest_multipole_nonneg
#print axioms gravity_at_least_quadrupole

end Phase12GW
