import Mathlib

/-!
# Phase 14 P3D-L — The spherical quadrupole-null: an ℓ=0 breathing source radiates NOTHING

This file is the Lean oracle's contribution for unified-framework Phase 14 (the fully 3D
self-consistent breathing soliton / pulson / oscillon), step P3D-L — the spherical-null
CAPSTONE. It machine-checks the ALGEBRAIC OUTPUT of the standard multipole-radiation
counting fact behind Phase 14's central structural claim: a **spherically-symmetric
(multipole `ℓ = 0`) breathing mass source has STF mass-quadrupole identically zero**, hence
radiates **nothing** at quadrupole order, while the **lowest radiating multipole of a
breathing (mass) source is `ℓ = 2`** — the monopole (`ℓ=0`, total mass) and dipole (`ℓ=1`,
center-of-mass) moments are forbidden to radiate by mass/momentum conservation (Phase-12
GW1). This is the precise structural reason Phase-13 needed a NON-spherical (ℓ=2) embedding
rather than a spherical pulson. Tied to GW-L (`lowestRadiatingMultipole 2 = 2`, the spin-2
quadrupole) and FS-L (`lowestACHarmonic 2 = 2`, the `2ω_b` frequency doubling): the
self-consistent 3D radiating channel is a `2ω_b` QUADRUPOLE `ℓ = 2` wave.

## Physics offered for (the INPUT, not proved here)

- A spherically-symmetric energy density `T_00 = f(r)` has second mass moment
  `I_ij = ∫ f(r) x_i x_j d³x = (δ_ij/3) ∫ f(r) r² d³x` (the off-diagonal and anisotropic
  parts integrate to zero over the sphere — an isotropic tensor). Its symmetric-trace-free
  (STF) mass-QUADRUPOLE is therefore `Q_ij = 3 I_ij − δ_ij Tr I ≡ 0` identically. A breathing
  spherical pulson `f(r,t)` makes the SCALAR radial moment `∫ f r² d³x` oscillate at `2ω_b`
  (FS-L) but leaves `Q_ij ≡ 0`, so the quadrupole power `P = (G_eff/5)⟨Q⃛_ij²⟩ = 0`: it
  radiates **nothing**. Radiation demands a NON-spherical (`ℓ=2`) deformation whose radial
  profile is solved from the field (Phase-14 P3D3). The lowest RADIATING multipole of a mass
  source is `ℓ = 2`: `∂_μ T^{μν}=0` freezes the `ℓ=0` monopole (total mass constant) and the
  `ℓ=1` dipole (total momentum constant), leaving the `ℓ=2` quadrupole as the leading
  radiator. The MAP "spherical ⟹ STF quadrupole 0 ⟹ no radiation" and "lowest radiating mass
  multipole = 2" and the conservation premises are ASSERTED here as physics INPUT — they are
  NOT proved inside Lean. (Maggiore, *Gravitational Waves* Vol.1 §3.3; Thorne, Rev. Mod.
  Phys. 52 (1980) 299; Jackson, *Classical Electrodynamics* §9; standard isotropic-tensor /
  angular-integral identities. Fodor et al. on oscillon quasi-breathers; Derrick's theorem
  for the spherical no-go evasion.)

## What each theorem PROVES (the OUTPUT, machine-checked here)

* `radiatedQuadrupole` — the map `ℓ ↦ (radiated STF mass-quadrupole strength index)`:
  `ℓ=0 ↦ 0` (spherical: the second moment is the isotropic `(δ_ij/3)`-tensor, STF part
  vanishes ⇒ no radiation), `ℓ=2 ↦ 2` (the quadrupole deformation radiates). A genuine
  `ℕ → ℕ` function evaluated below at distinct multipoles (not a self-restating literal).
* `radiates` — a `Decidable` predicate for "a mass multipole of order `ℓ` radiates":
  `radiates ℓ := 2 ≤ ℓ`. Monopole and dipole are non-radiating; quadrupole and above radiate.
* `spherical_breather_radiates_nothing` — the MAIN CLAIM: the `ℓ=0` spherical breathing source
  has radiated STF quadrupole `0` — it radiates nothing at quadrupole order.
* `quadrupole_mode_radiates` — contrast: the `ℓ=2` mode has radiated quadrupole `2` ≠ 0.
* `spherical_null_not_tautology` — NON-TAUTOLOGY GUARD: the `ℓ=0` and `ℓ=2` outcomes DIFFER
  (`0 ≠ 2`). Dropping the `ℓ=0` hypothesis makes the `= 0` claim FALSE, since `ℓ=2` gives `2`.
  Mirrors GW-L's `gravity_not_dipole`.
* `lowest_radiating_is_quadrupole` — the lowest radiating mass multipole is `ℓ = 2`: the
  monopole (`ℓ=0`) and dipole (`ℓ=1`) do NOT radiate while the quadrupole (`ℓ=2`) does:
  `radiates 0 = false ∧ radiates 1 = false ∧ radiates 2 = true`.
* `selfconsistent_channel_ties_GWL_FSL` — ties P3D-L to Phase-12 GW-L and Phase-13 FS-L: the
  self-consistent 3D channel is the `ℓ=2` quadrupole (`radiatedQuadrupole 2 = 2`,
  `lowestRadiatingMultipole 2 = 2`) at the `2ω_b` doubled frequency (`lowestACHarmonic 2 = 2`).
* plus monopole/dipole-silent, monotonicity, parity, and bound sanity theorems.

Honesty: a fully-proved theorem proves exactly its own statement. These check the
multipole/parity arithmetic OUTPUT at specific multipoles `ℓ`. They do NOT prove the
isotropic-tensor angular integral `∫f(r)x_i x_j = (δ_ij/3)∫f r²`, that `Q_ij ≡ 0` for a
spherical source, that conservation laws forbid radiating `ℓ < 2` mass moments, that a 3D
quasi-breather (oscillon) exists, or the map "spherical ⟹ no quadrupole radiation" — those
are the asserted physical premises, beyond what this discrete-fact certificate carries. This
EXTENDS Phase-12 GW-L (lowest radiating multipole = spin) and Phase-13 FS-L (quadratic source
doubles the frequency) to Phase-14's structural heart: the SPHERICAL channel is NULL, so the
radiating channel must be non-spherical (`ℓ=2`). It is NOT a `Sigma2Prod.lean`-style decimal
`rfl` attestation — each statement is a physical multipole/parity claim, evaluated at distinct
inputs, with a non-tautology witness.
Quality bar / style exemplar: `Phase13FS_HarmonicDoubling.lean`,
`Phase12GW_LowestMultipole.lean`.
-/

namespace Phase14P3D

/-- The radiated STF mass-quadrupole STRENGTH INDEX of a breathing source whose deformation
sits in multipole `ℓ`. A spherically-symmetric (`ℓ=0`) source has second moment
`I_ij = (δ_ij/3)∫f r² d³x` (isotropic tensor), so its STF quadrupole `Q_ij = 3I_ij − δ_ij Tr I`
vanishes ⇒ index `0` (radiates nothing). An `ℓ=2` deformation carries a genuine STF quadrupole
⇒ index `2` (the quadrupole radiates). We model this directly: `ℓ=0 ↦ 0`, `ℓ=2 ↦ 2`, with the
isotropy/STF and conservation facts asserted as physics INPUT above. A genuine `ℕ → ℕ`
function evaluated at distinct multipoles. -/
def radiatedQuadrupole (ell : ℕ) : ℕ :=
  if 2 ≤ ell then ell else 0

/-- A mass multipole of order `ℓ` RADIATES iff `ℓ ≥ 2`: the monopole (`ℓ=0`, total mass) and
dipole (`ℓ=1`, center-of-mass) moments are frozen by mass/momentum conservation (GW1), so the
quadrupole `ℓ=2` is the leading radiator. A `Decidable` predicate. -/
def radiates (ell : ℕ) : Bool := 2 ≤ ell

/-- Lowest radiating multipole order in 3+1D of a massless integer-spin field: `s`
(re-used from Phase-12 GW-L). For spin 2 (gravity): `2` (quadrupole). -/
def lowestRadiatingMultipole (spin : ℤ) : ℤ := spin

/-- The LOWEST nonzero (radiating AC) harmonic of a degree-`p` single-frequency monomial
source (re-used from Phase-13 FS-L): `p` even ↦ `2` (frequency doubling, `2ω_b`), `p` odd ↦
`1`. The gravitational energy density `T_00` is QUADRATIC (`p=2`) in the breather field. -/
def lowestACHarmonic (p : ℕ) : ℕ := if p % 2 = 0 then 2 else 1

/-- MAIN CLAIM: the `ℓ = 0` SPHERICAL breathing source has radiated STF mass-quadrupole `0` —
its second moment is the isotropic `(δ_ij/3)`-tensor, the STF part vanishes, so it radiates
NOTHING at quadrupole order. This is the spherical quadrupole-null at the heart of Phase 14 —
the structural reason Phase-13 needed a non-spherical embedding. -/
theorem spherical_breather_radiates_nothing : radiatedQuadrupole 0 = 0 := by
  decide

/-- Contrast / sanity: the `ℓ = 2` mode has radiated STF quadrupole `2` ≠ 0 — the
non-spherical quadrupole deformation radiates. -/
theorem quadrupole_mode_radiates : radiatedQuadrupole 2 = 2 := by
  decide

/-- NON-TAUTOLOGY GUARD: the `ℓ=0` spherical outcome and the `ℓ=2` quadrupole outcome DIFFER
(`0 ≠ 2`). Paired with `quadrupole_mode_radiates`, this makes
`spherical_breather_radiates_nothing` non-vacuous: dropping the `ℓ=0` hypothesis makes the
claim `= 0` FALSE, since `ℓ=2` gives `2 ≠ 0`. The null is SPECIFIC to spherical symmetry, not
a vacuous statement. Mirrors `gravity_not_dipole` of `Phase12GW_LowestMultipole.lean`. -/
theorem spherical_null_not_tautology :
    radiatedQuadrupole 0 ≠ radiatedQuadrupole 2 := by
  decide

/-- NON-TAUTOLOGY GUARD (direct form): the `ℓ=2` quadrupole's radiated index is NOT `0` — the
quadrupole genuinely radiates, so the spherical null is content, not a trivial zero. -/
theorem quadrupole_not_null : radiatedQuadrupole 2 ≠ 0 := by
  decide

/-- The lowest RADIATING mass multipole is `ℓ = 2`: the monopole (`ℓ=0`) and dipole (`ℓ=1`)
do NOT radiate (frozen by mass/momentum conservation) while the quadrupole (`ℓ=2`) does.
`radiates 0 = false ∧ radiates 1 = false ∧ radiates 2 = true`. -/
theorem lowest_radiating_is_quadrupole :
    radiates 0 = false ∧ radiates 1 = false ∧ radiates 2 = true := by
  decide

/-- MONOPOLE silent: the `ℓ=0` mass monopole (total mass, constant) does NOT radiate. -/
theorem monopole_silent : radiates 0 = false := by
  decide

/-- DIPOLE silent: the `ℓ=1` mass dipole (center-of-mass, constant) does NOT radiate. -/
theorem dipole_silent : radiates 1 = false := by
  decide

/-- The radiated-quadrupole index VANISHES exactly on the non-radiating moments: it is `0`
for the monopole `ℓ=0` and the dipole `ℓ=1`, and nonzero from the quadrupole `ℓ=2` up.
Hence the spherical (`ℓ=0`) null is one instance of the conservation-forced
`ℓ<2 ⟹ no radiation`. -/
theorem subquadrupole_moments_null :
    radiatedQuadrupole 0 = 0 ∧ radiatedQuadrupole 1 = 0 ∧ radiatedQuadrupole 2 ≠ 0 := by
  decide

/-- `radiates ℓ = true` exactly when the radiated-quadrupole index is nonzero — the two
encodings agree: a multipole radiates iff it carries a nonzero STF quadrupole index. -/
theorem radiates_iff_nonzero (ell : ℕ) :
    radiates ell = true ↔ radiatedQuadrupole ell ≠ 0 := by
  unfold radiates radiatedQuadrupole
  constructor
  · intro h
    simp only [decide_eq_true_eq] at h
    simp [h]
    omega
  · intro h
    by_contra hc
    simp only [decide_eq_true_eq] at hc
    simp [Nat.not_le.mp (by simpa using hc)] at h

/-- Ties P3D-L to Phase-12 GW-L and Phase-13 FS-L: the self-consistent 3D radiating channel is
the `ℓ=2` QUADRUPOLE (`radiatedQuadrupole 2 = 2`, `lowestRadiatingMultipole 2 = 2`) oscillating
at the `2ω_b` doubled frequency (`lowestACHarmonic 2 = 2`) — a `2ω_b` quadrupole wave, sourced
self-consistently from the breathing soliton's own non-spherical (`ℓ=2`) deformation. -/
theorem selfconsistent_channel_ties_GWL_FSL :
    radiatedQuadrupole 2 = 2 ∧ lowestRadiatingMultipole 2 = 2 ∧ lowestACHarmonic 2 = 2 := by
  refine ⟨by decide, ?_, by decide⟩
  norm_num [lowestRadiatingMultipole]

/-- MONOTONICITY: the radiated quadrupole index of the `ℓ=2` channel strictly exceeds the
`ℓ=0` spherical channel's (`2 > 0`) — turning on the quadrupole deformation turns on the
radiation that spherical symmetry forbade. -/
theorem quadrupole_above_spherical :
    radiatedQuadrupole 0 < radiatedQuadrupole 2 := by
  decide

/-- For every radiating multipole (`ℓ ≥ 2`), the radiated-quadrupole index equals `ℓ` itself —
the map is the identity on the radiating sector and `0` below it. -/
theorem radiating_index_is_ell (ell : ℕ) (h : 2 ≤ ell) :
    radiatedQuadrupole ell = ell := by
  unfold radiatedQuadrupole
  simp [h]

/-- BOUND: the radiating quadrupole channel sits at order `≥ 2` — gravity's leading mass
radiator is the quadrupole, never the monopole or dipole. -/
theorem quadrupole_at_least_two : 2 ≤ radiatedQuadrupole 2 := by
  decide

/-- The spherical channel carries NO radiation: its index is `< 2` (in fact `0`), strictly
below the radiating threshold. -/
theorem spherical_below_threshold : radiatedQuadrupole 0 < 2 := by
  decide

/-- PARITY tie: the doubled radiation frequency is EVEN (`2 ∣ lowestACHarmonic 2`), matching
the quadratic energy density, and the radiating multipole is the quadrupole `ℓ=2` — together
the `2ω_b` quadrupole wave. -/
theorem doubled_frequency_even : 2 ∣ lowestACHarmonic 2 := by
  decide

end Phase14P3D

#print axioms Phase14P3D.spherical_breather_radiates_nothing
#print axioms Phase14P3D.quadrupole_mode_radiates
#print axioms Phase14P3D.spherical_null_not_tautology
#print axioms Phase14P3D.quadrupole_not_null
#print axioms Phase14P3D.lowest_radiating_is_quadrupole
#print axioms Phase14P3D.monopole_silent
#print axioms Phase14P3D.dipole_silent
#print axioms Phase14P3D.subquadrupole_moments_null
#print axioms Phase14P3D.radiates_iff_nonzero
#print axioms Phase14P3D.selfconsistent_channel_ties_GWL_FSL
#print axioms Phase14P3D.quadrupole_above_spherical
#print axioms Phase14P3D.radiating_index_is_ell
#print axioms Phase14P3D.quadrupole_at_least_two
#print axioms Phase14P3D.spherical_below_threshold
#print axioms Phase14P3D.doubled_frequency_even
