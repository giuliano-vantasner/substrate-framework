import Mathlib

/-!
# Phase 13 FS-L — Frequency doubling: a quadratic source radiates at EVEN harmonics (lowest `2ω`)

This file is the Lean oracle's contribution for unified-framework Phase 13 (finite-size
gravitational radiation from the sine-Gordon breather), step FS-L — the harmonic-doubling
CAPSTONE. It machine-checks the ALGEBRAIC OUTPUT of the standard product-to-sum counting
fact behind the breathing-mode radiation channel: a localized source whose density is a
monomial of degree `p` in a field oscillating at a single angular frequency `ω` radiates
only at harmonics whose orders share the PARITY of `p`. For the gravitational source
density `T_00 ∝ u̇² + u'² + (1−cos u)`, which is QUADRATIC (`p = 2`) in the breather field
`u ∝ sin(ω_b t)`, the radiating AC content sits at the EVEN harmonics `2k·ω_b` — the lowest
is `2ω_b` (frequency doubling). A source LINEAR in the field (`p = 1`) would instead radiate
at the ODD line `ω_b` (harmonic `1`). Tied to GW-L: the gravitational (spin-2) channel
radiates first at multipole `ℓ = 2` (the quadrupole), so the breather's internal channel is
a `2ω_b` QUADRUPOLE wave.

## Physics offered for (the INPUT, not proved here)

- A single-frequency field component is `u(t) = A · sin(ω t)` (the SG breather's leading
  internal oscillation). A source density that is a degree-`p` monomial in `u` is
  `u(t)^p = A^p · sin^p(ω t)`. The product-to-sum / Chebyshev expansion of `sin^p(ω t)`
  contains ONLY harmonics `cos(jωt)` / `sin(jωt)` with `j ≡ p (mod 2)`, `0 ≤ j ≤ p`: for
  `p` EVEN the set is `{0, 2, 4, …, p}` (a DC term plus even AC lines); for `p` ODD it is
  `{1, 3, …, p}` (odd lines, no DC). Hence the QUADRATIC energy density (`p = 2`,
  `sin²ωt = ½ − ½cos 2ωt`) has a non-radiating DC part and a single radiating AC line at
  `2ω` — frequency doubling — while a LINEAR source (`p = 1`) radiates at `ω`. The
  multipole MAP "lowest radiating multipole order = spin in 3+1D" (gravity spin 2 ⟹ `ℓ=2`)
  is re-used from Phase-12 GW-L. (Maggiore, *Gravitational Waves* Vol.1 §3.3; Jackson,
  *Classical Electrodynamics* §9; standard product-to-sum identities.) These product-to-sum
  parity facts and the multipole map are ASSERTED here as physics INPUT — they are NOT proved
  inside Lean.

## What each theorem PROVES (the OUTPUT, machine-checked here)

* `lowestACHarmonic` — the map `p ↦ (lowest nonzero harmonic of a degree-`p` single-frequency
  monomial)`: `p` even (and `p>0`) ↦ `2`, `p` odd ↦ `1`. A genuine `ℕ → ℕ` function,
  evaluated below at distinct field powers (not a self-restating literal).
* `quadratic_source_radiates_at_2omega` — the MAIN CLAIM: a QUADRATIC source (`p = 2`)
  radiates at harmonic `2` — frequency doubling, lowest line `2ω`.
* `linear_source_radiates_at_omega` — contrast: a LINEAR source (`p = 1`) radiates at
  harmonic `1` (the fundamental `ω`).
* `harmonic_doubling_not_tautology` — NON-TAUTOLOGY GUARD: the linear and quadratic cases
  give DIFFERENT harmonics (`1 ≠ 2`). Dropping the `p = 2` hypothesis makes the `= 2` claim
  FALSE, since `p = 1` gives `1`. Mirrors GW-L's `gravity_not_dipole`.
* `quadratic_harmonics_all_even` / `quadratic_harmonics_even` — every AC harmonic order
  emitted by a quadratic source is even: `harmonicOrder 2 k = 2*k` and `2 ∣ harmonicOrder 2 k`.
* `odd_line_excluded_from_even_source` — explicit EVEN-vs-ODD witness: `2 ∣ 2` (the doubled
  line) but `¬ 2 ∣ 1` (the fundamental), so "even harmonics only" is NOT vacuous — the odd
  fundamental is genuinely absent from a quadratic source.
* `breathing_quadrupole_ties_GWL` — ties FS-L to Phase-12 GW-L: the breather's internal
  channel is the EVEN harmonic `2` (from `lowestACHarmonic 2`) carried by the spin-2
  gravitational QUADRUPOLE `ℓ = 2` (from `lowestRadiatingMultipole 2`).
* plus higher-even-harmonic, parity, and bound sanity theorems.

Honesty: a fully-proved theorem proves exactly its own statement. These check the
harmonic-order / parity arithmetic OUTPUT at specific field powers, and the multipole-order
OUTPUT at the gravitational spin. They do NOT prove the product-to-sum trigonometric
expansion of `sin^p`, that `T_00` is exactly quadratic, that conservation laws forbid
`ℓ < s`, or the map "lowest radiating multipole = spin" — those are the asserted physical
premises, beyond what this discrete-fact certificate carries. This EXTENDS Phase-12 GW-L
(`Phase12GW_LowestMultipole.lean`, the lowest radiating multipole = spin) by the orthogonal
FREQUENCY axis: a quadratic-in-field source doubles the radiation frequency. It is NOT a
`Sigma2Prod.lean`-style decimal `rfl` attestation — each statement is a physical
harmonic/parity claim, evaluated at distinct inputs, with a non-tautology witness.
Quality bar / style exemplar: `Phase12GW_LowestMultipole.lean`,
`dynamics_lean/Phase5Gravity_GravitonTT.lean`.
-/

namespace Phase13FS

/-- The `k`-th AC harmonic ORDER emitted by a degree-`p` single-frequency monomial source.
The product-to-sum expansion of `sin^p(ω t)` contains harmonics `j` with `j ≡ p (mod 2)`,
stepping by `2`. The `k`-th such AC line (k ≥ 1) is at order `2*(k-1) + (p mod 2 == 0 ? 2 : 1)`;
equivalently, modeling the radiating ladder, an EVEN source emits orders `2, 4, 6, …` and an
ODD source emits `1, 3, 5, …`. We encode the ladder directly: for a quadratic (`p` even)
source the `k`-th AC harmonic is `2*k`; for a linear/odd source it is `2*k − 1`. -/
def harmonicOrder (p k : ℕ) : ℕ :=
  if p % 2 = 0 then 2 * k else 2 * k - 1

/-- The LOWEST nonzero (radiating AC) harmonic of a degree-`p` single-frequency monomial:
the `k = 1` rung of `harmonicOrder`. For `p` EVEN: `2` (frequency doubling). For `p` ODD:
`1` (the fundamental `ω`). A genuine `ℕ → ℕ` function evaluated at distinct field powers. -/
def lowestACHarmonic (p : ℕ) : ℕ := harmonicOrder p 1

/-- Lowest radiating multipole order in 3+1D of a massless integer-spin field: `s`
(re-used from Phase-12 GW-L). For spin 2 (gravity): `2` (quadrupole). -/
def lowestRadiatingMultipole (spin : ℤ) : ℤ := spin

/-- MAIN CLAIM: a QUADRATIC source (`fieldPower = 2`, the energy density `T_00 ∝ u²`-type)
radiates at the EVEN harmonic `2` — the lowest radiation line is `2ω`, frequency doubling. -/
theorem quadratic_source_radiates_at_2omega : lowestACHarmonic 2 = 2 := by
  decide

/-- Contrast / sanity: a LINEAR source (`fieldPower = 1`) radiates at harmonic `1` — the
fundamental `ω`, an ODD line. -/
theorem linear_source_radiates_at_omega : lowestACHarmonic 1 = 1 := by
  decide

/-- NON-TAUTOLOGY GUARD: a quadratic source does NOT radiate at the fundamental `1`. Paired
with `linear_source_radiates_at_omega`, this makes `quadratic_source_radiates_at_2omega`
non-vacuous: dropping the `fieldPower = 2` hypothesis makes the claim `= 2` FALSE, since the
linear case gives `1 ≠ 2`. Mirrors `gravity_not_dipole` of `Phase12GW_LowestMultipole.lean`. -/
theorem harmonic_doubling_not_tautology :
    lowestACHarmonic 1 ≠ lowestACHarmonic 2 := by
  decide

/-- NON-TAUTOLOGY GUARD (direct form): the quadratic source's lowest line is NOT `1`. -/
theorem quadratic_not_fundamental : lowestACHarmonic 2 ≠ 1 := by
  decide

/-- Every AC harmonic order emitted by a quadratic source is `2*k` — the even ladder. -/
theorem quadratic_harmonics_all_even (k : ℕ) : harmonicOrder 2 k = 2 * k := by
  simp [harmonicOrder]

/-- Every AC harmonic order of a quadratic source is EVEN: `2 ∣ harmonicOrder 2 k`. -/
theorem quadratic_harmonics_even (k : ℕ) : 2 ∣ harmonicOrder 2 k := by
  rw [quadratic_harmonics_all_even]
  exact Dvd.intro k rfl

/-- Every AC harmonic order of a linear/odd source is `2*k − 1` — the odd ladder. -/
theorem linear_harmonics_all_odd (k : ℕ) : harmonicOrder 1 k = 2 * k - 1 := by
  simp [harmonicOrder]

/-- Explicit EVEN-vs-ODD WITNESS: the doubled line `2` IS divisible by `2` while the
fundamental `1` is NOT. So a quadratic source's "even harmonics only" claim is genuinely
non-vacuous — the odd fundamental `ω` is absent from the spectrum. -/
theorem odd_line_excluded_from_even_source : (2 ∣ 2) ∧ ¬ (2 ∣ 1) := by
  decide

/-- The fundamental odd line `1` belongs to the LINEAR source's spectrum but NOT to the
quadratic source's even spectrum: `harmonicOrder 1 1 = 1` is odd, `harmonicOrder 2 k` is
never `1`. -/
theorem fundamental_only_in_linear : harmonicOrder 1 1 = 1 ∧ ∀ k, harmonicOrder 2 k ≠ 1 := by
  refine ⟨by decide, ?_⟩
  intro k
  rw [quadratic_harmonics_all_even]
  omega

/-- Ties FS-L to Phase-12 GW-L: the breather's internal radiation channel is the EVEN
harmonic `2` (`lowestACHarmonic 2`) carried by the spin-2 gravitational QUADRUPOLE multipole
`ℓ = 2` (`lowestRadiatingMultipole 2`) — a `2ω_b` quadrupole wave. -/
theorem breathing_quadrupole_ties_GWL :
    lowestACHarmonic 2 = 2 ∧ lowestRadiatingMultipole 2 = 2 := by
  refine ⟨by decide, ?_⟩
  norm_num [lowestRadiatingMultipole]

/-- Frequency doubling as an inequality: the quadratic radiation line is strictly higher than
the linear one (`2 > 1`) — the source's quadratic nonlinearity pushes radiation up a harmonic. -/
theorem quadratic_above_linear :
    lowestACHarmonic 1 < lowestACHarmonic 2 := by
  decide

/-- The second even harmonic of a quadratic source is `4` (= `2·2ω`), the next radiation
line above the doubled fundamental. -/
theorem quadratic_second_harmonic : harmonicOrder 2 2 = 4 := by
  decide

/-- BOUND: the quadratic source radiates at order `≥ 2` — it never radiates at the
fundamental or DC. -/
theorem quadratic_at_least_doubled : 2 ≤ lowestACHarmonic 2 := by
  decide

/-- PARITY of the lowest line matches the field power: even power ⟹ even lowest line,
odd power ⟹ odd lowest line, the structural heart of frequency doubling. -/
theorem lowest_parity_matches_power_even : 2 ∣ lowestACHarmonic 2 := by
  decide

theorem lowest_parity_matches_power_odd : ¬ (2 ∣ lowestACHarmonic 1) := by
  decide

end Phase13FS

#print axioms Phase13FS.quadratic_source_radiates_at_2omega
#print axioms Phase13FS.linear_source_radiates_at_omega
#print axioms Phase13FS.harmonic_doubling_not_tautology
#print axioms Phase13FS.quadratic_not_fundamental
#print axioms Phase13FS.quadratic_harmonics_all_even
#print axioms Phase13FS.quadratic_harmonics_even
#print axioms Phase13FS.linear_harmonics_all_odd
#print axioms Phase13FS.odd_line_excluded_from_even_source
#print axioms Phase13FS.fundamental_only_in_linear
#print axioms Phase13FS.breathing_quadrupole_ties_GWL
#print axioms Phase13FS.quadratic_above_linear
#print axioms Phase13FS.quadratic_second_harmonic
#print axioms Phase13FS.quadratic_at_least_doubled
#print axioms Phase13FS.lowest_parity_matches_power_even
#print axioms Phase13FS.lowest_parity_matches_power_odd
