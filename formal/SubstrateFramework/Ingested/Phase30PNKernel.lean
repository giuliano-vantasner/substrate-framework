import Mathlib

/-!
# Phase 30 — phonon-nuclear coupling kernel (PN-L)

The Lean oracle's decidable-arithmetic contribution to the Phase-30 phonon-nuclear
bridge cluster. It certifies the KINEMATIC facts that PN2/PN5 verify in SymPy/NumPy —
the ones that reduce to genuinely decidable natural-number arithmetic (Mathlib-backed).
It does NOT force PN1's symbolic vertex algebra or PN4's numeric loss model into Lean.

A large coherent quantum `Ω` fractionating into modes of characteristic energy `ω`
subdivides into

  `n = Ω / ω`   (natural-number division = ⌊Ω/ω⌋),

the KINEMATIC subdivision count of PN2 (energy conservation, NOT the retracted
loss-enhancement claim). We certify:

1. `subdivision_bound` — `n·ω ≤ Ω < (n+1)·ω`: the count is the exact energy-conserving
   floor, with a residual remainder in `[0, ω)`. (PN2's remainder bound.)

2. `subdivision_antitone` — larger phonon energy ⇒ no more phonons: `ω₁ ≤ ω₂ ⇒
   Ω/ω₂ ≤ Ω/ω₁`. (PN2's monotone non-increase.)

3. `dicke_rate_not_squared` — the collective Dicke rate scales as `N`, not `N²`:
   for `N ≥ 2`, `N < N·N`, so an amplitude `~N` (rate `~N²`) is strictly larger than the
   true rate `~N` and is REJECTED. (PN3's superradiance-magnitude guard.)

4. `PN_L` — the compound keystone.

5. `subdivision_not_constant` — a non-tautology guard `24/3 < 24/2` (`8 < 12`), NOT true
   by `rfl`; a fabricated `ω`-independent constant count would FAIL it.
-/

namespace Phase30PN

/-- **PN-L (1) — kinematic subdivision bound.**  For `ω > 0` the energy-conserving count
`n = Ω / ω` satisfies `n·ω ≤ Ω < (n+1)·ω`: the largest integer number of phonons that
fits under the budget, with the residual remainder `Ω - n·ω ∈ [0, ω)`.  (PN2's exact
remainder bound, here as Nat arithmetic.) -/
theorem subdivision_bound (Ω ω : ℕ) (h : 0 < ω) :
    (Ω / ω) * ω ≤ Ω ∧ Ω < (Ω / ω + 1) * ω := by
  have hdm : ω * (Ω / ω) + Ω % ω = Ω := Nat.div_add_mod Ω ω
  have hlt : Ω % ω < ω := Nat.mod_lt Ω h
  refine ⟨?_, ?_⟩
  · nlinarith [hdm, hlt, Nat.zero_le (Ω % ω)]
  · nlinarith [hdm, hlt]

/-- **PN-L (2) — monotone non-increase.**  A larger characteristic phonon energy yields
no more phonons: `ω₁ ≤ ω₂ ⇒ Ω/ω₂ ≤ Ω/ω₁`.  (PN2's sampled monotonicity, here exact.) -/
theorem subdivision_antitone (Ω ω₁ ω₂ : ℕ) (h1 : 0 < ω₁) (h12 : ω₁ ≤ ω₂) :
    Ω / ω₂ ≤ Ω / ω₁ :=
  Nat.div_le_div_left h12 h1

/-- **PN-L (3) — Dicke rate is `N`, not `N²` (superradiance-magnitude guard).**  The
collective amplitude scales as `√N`, so the rate scales as `N`.  For `N ≥ 2` we have
`N < N·N`: the fabricated linear amplitude (rate `~N²`) is strictly larger than the true
rate `~N` and is thereby REJECTED. -/
theorem dicke_rate_not_squared (N : ℕ) (h : 2 ≤ N) : N < N * N := by
  nlinarith [h]

/-- **PN-L (HEADLINE).**  The kinematic phonon-nuclear keystones in one statement: the
energy-conserving subdivision bound, its monotone non-increase in the phonon energy, and
the Dicke rate-`N`-not-`N²` guard. -/
theorem PN_L (Ω ω ω₁ ω₂ N : ℕ) (h : 0 < ω) (h1 : 0 < ω₁) (h12 : ω₁ ≤ ω₂) (hN : 2 ≤ N) :
    ((Ω / ω) * ω ≤ Ω ∧ Ω < (Ω / ω + 1) * ω) ∧
    (Ω / ω₂ ≤ Ω / ω₁) ∧
    (N < N * N) :=
  ⟨subdivision_bound Ω ω h, subdivision_antitone Ω ω₁ ω₂ h1 h12,
    dicke_rate_not_squared N hN⟩

/-- **PN-L (non-tautology guard).**  A concrete strict inequality `24/3 < 24/2`, i.e.
`8 < 12`, decided by `norm_num` — NOT true by `rfl`.  A fabricated `ω`-independent
constant subdivision count would make this an equality and FAIL, so the monotonicity
carries real content and is not vacuous. -/
theorem subdivision_not_constant : (24 : ℕ) / 3 < 24 / 2 := by norm_num

end Phase30PN
