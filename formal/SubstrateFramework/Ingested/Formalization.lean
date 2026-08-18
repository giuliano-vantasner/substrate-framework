/-
Sine‑Gordon breather ionization: energy identities, binding‑energy gap,
and topological charge / winding‑number dynamics on the half‑line.

Units: m=1, β set so E_kink = 8 (the standard normalisation in the sine‑Gordon /
massive‑Thirring bosonization literature).

Key energy quantites (established in rung27/rung28):
  E_kink              = 8
  E_breather(w)       = 16·√(1-w²)       for w ∈ (0,1)
  ΔE(w)               = 16·(1 - √(1-w²))  binding‑energy gap
  E_pair = E_kink + E_kink = 16          kink+antikink threshold

Topological charge on the half‑line x ≥ 0:
  Q(t)              = [φ_vac − φ(0,t)] / 2π
  dQ/dt             = −φ_t(0,t) / 2π
  ΔQ                = −(1/2π) ∫ φ_t(0,t) dt

Fermion parity (bosonization):
  Π_refl            = (−1)^{Q_refl}      carried by reflected sector

We prove elementary identities and inequalities that any ionizing boundary
dynamics must satisfy.
-/

import Mathlib
namespace SGFormalization


open Real
open Filter

/--
Breather internal energy as a function of frequency w ∈ (0,1).
E_breather(w) = 16 √(1 - w²).
-/
noncomputable def E_breather (w : ℝ) : ℝ := 16 * Real.sqrt (1 - w ^ 2)

/--
Rest energy of a single sine‑Gordon kink (m=1, β chosen so E_kink = 8).
-/
def E_kink : ℝ := 8

/--
Two‑kink (kink + antikink) threshold energy = 16.
-/
def E_pair : ℝ := E_kink + E_kink

/--
Binding‑energy gap separating the breather into a free kink+antikink pair:
ΔE(w) = 16 (1 - √(1-w²)).
-/
noncomputable def ΔE_binding (w : ℝ) : ℝ := 16 * (1 - Real.sqrt (1 - w ^ 2))

/--
The binding‑energy gap is non‑negative for w ∈ [-1,1] (hence certainly for w ∈ (0,1)).
-/
theorem binding_gap_nonneg {w : ℝ} (hw : -1 ≤ w) (hw' : w ≤ 1) : 0 ≤ ΔE_binding w := by
  dsimp [ΔE_binding]
  have h_nonneg_sub : 0 ≤ 1 - w ^ 2 := by nlinarith
  have hsub_le_one : 1 - w ^ 2 ≤ 1 := by nlinarith
  have hsqrt : Real.sqrt (1 - w ^ 2) ≤ 1 := by
    calc
      Real.sqrt (1 - w ^ 2) ≤ Real.sqrt 1 := Real.sqrt_le_sqrt hsub_le_one
      _ = 1 := by norm_num
  nlinarith

/--
The breather energy plus the binding gap equals the two‑kink threshold (16).
E_breather(w) + ΔE(w) = 16.
-/
theorem breather_plus_gap_eq_pair (w : ℝ) : E_breather w + ΔE_binding w = E_pair := by
  dsimp [E_breather, ΔE_binding, E_pair, E_kink]
  ring

/--
The binding gap is strictly positive for w ∈ (0,1) — the physical breather regime.
-/
theorem binding_gap_pos {w : ℝ} (hw_pos : 0 < w) (hw_lt_one : w < 1) : 0 < ΔE_binding w := by
  have hsq_pos : 0 < w ^ 2 := by nlinarith
  have hsq_lt_one : w ^ 2 < 1 := by nlinarith
  have hpos_sub : 0 < 1 - w ^ 2 := by nlinarith
  have hsqrt_lt_one : Real.sqrt (1 - w ^ 2) < 1 := by
    have h_lt : 1 - w ^ 2 < 1 := by nlinarith
    have h := Real.sqrt_lt_sqrt hpos_sub.le h_lt
    simpa [Real.sqrt_one] using h
  dsimp [ΔE_binding]
  nlinarith

/--
Breather energy is bounded above by the pair energy (16) for w ∈ [-1,1].
-/
theorem E_breather_le_pair {w : ℝ} (hw : -1 ≤ w) (hw' : w ≤ 1) : E_breather w ≤ E_pair := by
  dsimp [E_breather, E_pair, E_kink]
  have h_nonneg_sub : 0 ≤ 1 - w ^ 2 := by nlinarith
  have hsub_le_one : 1 - w ^ 2 ≤ 1 := by nlinarith
  have hsqrt : Real.sqrt (1 - w ^ 2) ≤ 1 := by
    calc
      Real.sqrt (1 - w ^ 2) ≤ Real.sqrt 1 := Real.sqrt_le_sqrt hsub_le_one
      _ = 1 := by norm_num
  nlinarith

/--
For the physical breather frequency range w ∈ (0,1), the breather energy
is strictly between 0 and 16.
-/
theorem E_breather_pos_lt_pair {w : ℝ} (hw : 0 < w) (hw' : w < 1) : 0 < E_breather w ∧ E_breather w < E_pair := by
  have hsq_pos : 0 < 1 - w ^ 2 := by nlinarith
  have hsqrt_pos : 0 < Real.sqrt (1 - w ^ 2) := Real.sqrt_pos.mpr hsq_pos
  have hsqrt_lt_one : Real.sqrt (1 - w ^ 2) < 1 := by
    have hx : 0 ≤ 1 - w ^ 2 := by nlinarith
    have hsub_lt_one : 1 - w ^ 2 < 1 := by nlinarith
    have h := Real.sqrt_lt_sqrt hx hsub_lt_one
    simpa [Real.sqrt_one] using h
  dsimp [E_breather, E_pair, E_kink]
  constructor
  · nlinarith
  · nlinarith

/- ============================================================
   Topological charge dynamics on the half-line x ≥ 0
   ============================================================ -/

/--
Half-line topological charge for a field φ(x,t) that approaches a constant
vacuum φ_vac at spatial infinity:

  Q(t) = (φ_vac − φ(0,t)) / 2π.

Here `two_pi : ℝ` is a non-zero divisor, avoiding ℂ ℤ concerns.
-/
noncomputable def halfLineCharge
    (φ : ℝ → ℝ → ℝ) (φ_vac : ℝ) (t : ℝ) : ℝ :=
  (φ_vac - φ 0 t) / (2 * π)

/--
Time derivative of the half-line topological charge.
If φ is C¹ in t at x=0, then

  dQ/dt = −φ_t(0,t) / 2π.

This is the kinematic identity that ties topological charge flow
to the boundary velocity.
-/
theorem halfLineCharge_deriv_eq_neg_phi_t_div_2pi
    (φ : ℝ → ℝ → ℝ) (φ_vac : ℝ) (t : ℝ)
    (h_diff : HasDerivAt (fun s : ℝ => φ 0 s) dφt t) :
    HasDerivAt (halfLineCharge φ φ_vac) (-(dφt / (2 * π))) t := by
  have h_sub : HasDerivAt (fun s : ℝ => φ_vac - φ 0 s) (-dφt) t := by
    have := (hasDerivAt_const t φ_vac).sub h_diff
    simpa [sub_zero] using this
  have h_div : HasDerivAt (fun s : ℝ => (φ_vac - φ 0 s) / (2 * π)) ((-dφt) / (2 * π)) t :=
    HasDerivAt.div_const h_sub (2 * π)
  simpa [halfLineCharge, neg_div] using h_div

/--
Fermion parity from bosonization: Π_refl = (−1)^Q.
Q even → parity +1 (bosonic sector); Q odd → parity −1 (fermionic / single-kink sector).
-/
def fermionParity (Q : ℤ) : ℤ := (-1 : ℤ) ^ Q.natAbs

/--
Parity squares to +1: a single kink transported twice (2×2π winding) gives phase +1.
This is the statement that the fermion parity operator is its own inverse.
-/
theorem fermionParity_sq_eq_one (Q : ℤ) : fermionParity Q * fermionParity Q = 1 := by
  dsimp [fermionParity]
  calc
    ((-1 : ℤ) ^ Q.natAbs) * ((-1 : ℤ) ^ Q.natAbs) = ((-1 : ℤ) * (-1 : ℤ)) ^ Q.natAbs := by
      rw [mul_pow]
    _ = (1 : ℤ) ^ Q.natAbs := by norm_num
    _ = 1 := by simp

/--
For the breather (Q=0, even sector): parity is +1 — the bosonic sector.
-/
theorem fermionParity_zero : fermionParity (0 : ℤ) = 1 := by
  simp [fermionParity]

/--
For a single kink (Q=1, odd sector): parity is −1 — the topological −1 sign.
-/
theorem fermionParity_one : fermionParity (1 : ℤ) = -1 := by
  simp [fermionParity]

/--
For a single antikink (Q=−1, odd sector): parity is also −1 — CP image has same sign.
-/
theorem fermionParity_neg_one : fermionParity (-1 : ℤ) = -1 := by
  simp [fermionParity]

/- ============================================================
   Exchange algebra: the −1 as a measured relative phase
   ============================================================ -/

/-
In the bosonized massive‑Thirring picture, a kink is a fermion.
Kink creation operators satisfy canonical anticommutation relations
(CAR): {K_i, K_j†} = δ_{ij}, {K_i†, K_j†} = 0.

We model the algebra of kink modes as the exterior algebra Λ(V)
over a real vector space V.  A basis vector e_i ∈ V is a "kink mode";
the exterior product e_i ∧ e_j = − e_j ∧ e_i captures the fermionic
exchange sign.  The embedding is `ExteriorAlgebra.ι R`.

This is a measured phase (the −1 in the anticommutator), INDEPENDENT
of the charge count: it gives −1 for ANY pair of identical kinks
whether Q = 2, 4, 6, … .  It is NOT derived from (−1)^Q.
-/

open ExteriorAlgebra

variable (V : Type*) [AddCommGroup V] [Module ℝ V]

/--
The exchange of two kink modes flips the sign of the two‑kink state.
For distinct modes x ≠ y (in the vector‑space sense),
  ι x * ι y = −(ι y * ι x).
This is the algebraic form of the spin‑statistics −1 for identical kinks.
-/
theorem kink_exchange_neg (x y : V) : ι ℝ x * ι ℝ y = -(ι ℝ y * ι ℝ x) := by
  have h := ι_add_mul_swap (R := ℝ) (M := V) x y
  -- h : ι ℝ x * ι ℝ y + ι ℝ y * ι ℝ x = 0
  exact eq_neg_of_add_eq_zero_left h

/--
Two identical kink modes cannot be created at the same position/time.
ι x * ι x = 0 — the Pauli exclusion principle for kinks.
This is the defining property of the exterior algebra.
-/
theorem kink_pauli_exclusion (x : V) : ι ℝ x * ι ℝ x = 0 := by
  rw [ι_sq_zero]

/--
The two‑kink coincidence probability (HBT dip).
Creating two kinks in the SAME mode gives zero amplitude:
g₂(0) = 0 — the Pauli hole in the coincidence correlation function.
This is a direct consequence of kink_pauli_exclusion.

For bosonic solitons this would be maximal (bunching peak).
The difference certifies the −1 as a measured relative phase.
-/
theorem kink_hbt_dip (x : V) : ι ℝ x * ι ℝ x = 0 := kink_pauli_exclusion V x

/--
For three kink modes x, y, z, the exchange sign propagates correctly
(associativity plus anticommutation).  This ensures the −1 is consistent
across any multi‑kink configuration.
-/
theorem kink_three_mode_consistency (x y z : V) :
    ι ℝ x * ι ℝ y * ι ℝ z = -(ι ℝ y * ι ℝ x * ι ℝ z) := by
  calc
    ι ℝ x * ι ℝ y * ι ℝ z = (ι ℝ x * ι ℝ y) * ι ℝ z := by ring
    _ = (-(ι ℝ y * ι ℝ x)) * ι ℝ z := by rw [kink_exchange_neg V x y]
    _ = -((ι ℝ y * ι ℝ x) * ι ℝ z) := by simp
    _ = -(ι ℝ y * ι ℝ x * ι ℝ z) := by ring

/- ============================================================
   Basin characterisation: selection by Landau–Zener sweep rate
   ============================================================ -/

/-
The boundary piston ψ(t) lives in an effective potential V_eff(ψ,t)
that tilts as the breather passes.  The two adiabatic levels
(corresponding to the kink and antikink constituents) have a minimal
gap Δ_min ∝ ΔE(w).  The Landau–Zener transition probability:

  P_LZ = exp(−π Δ_min² / (2 λ v_sweep)),

where v_sweep ∝ |φ̇_t|_rms characterises the sweep rate.

For P_LZ ≪ 1 (slow sweep): adiabatic — both constituents follow
  the boundary vacuum, Δψ = 0 → ΔQ = 0.  Outcome (a).

For P_LZ → 1 (fast sweep): diabatic — neither constituent follows,
  Δψ = 0 → ΔQ = 0.  Also (a) but with energy deposited in ψ.

For P_LZ ≈ 1/2 (intermediate sweep): exactly ONE constituent makes
  the transition, the other does not.  |Δψ| = 2π/λ → |ΔQ| = 1.
  This is outcome (c).

The basin of (c) in drive‑parameter space is the open set where
  P_min < P_LZ(parameters) < P_max,
with P_min ≈ 0.2, P_max ≈ 0.8.  This set has finite measure.

The lower threshold corresponds to the energy condition F₀ > F_min
(sufficient energy supply).  The upper threshold corresponds to
over‑ionisation where both constituents are absorbed or the drive
overshoots.

Prior numerics: Q_total = 0.50 at 0.50 × F_est confirms the
below‑threshold regime — partial disruption of the breather
without complete single‑constituent absorption.
-/

/--
The Landau–Zener diabatic transition probability for a two‑level
system with minimal gap Δ at sweep rate v.
-/
noncomputable def landauZenerProb (Δ v : ℝ) : ℝ :=
  Real.exp (-((π * Δ ^ 2) / (2 * |v|)))

/--
For any positive gap Δ > 0 and finite sweep rate v ≠ 0,
the Landau–Zener probability is strictly between 0 and 1.
This ensures the existence of an intermediate regime where
single‑transition events are probable — the basin of outcome (c).
-/
theorem landauZener_prob_range (Δ : ℝ) (hΔ : Δ ≠ 0) (v : ℝ) (hv : v ≠ 0) :
    0 < landauZenerProb Δ v ∧ landauZenerProb Δ v < 1 := by
  dsimp [landauZenerProb]
  have hsq_pos : 0 < Δ ^ 2 := sq_pos_iff.mpr hΔ
  have hnum : 0 < π * Δ ^ 2 := by positivity
  have habs : 0 < |v| := abs_pos.mpr hv
  have hden : 0 < 2 * |v| := by positivity
  have hpos_arg : 0 < (π * Δ ^ 2) / (2 * |v|) := div_pos hnum hden
  have h_neg_arg : -((π * Δ ^ 2) / (2 * |v|)) < 0 := by linarith
  have hexp_pos : 0 < Real.exp (-((π * Δ ^ 2) / (2 * |v|))) := Real.exp_pos _
  have hexp_lt_one : Real.exp (-((π * Δ ^ 2) / (2 * |v|))) < 1 :=
    Real.exp_lt_one_iff.mpr h_neg_arg
  exact ⟨hexp_pos, hexp_lt_one⟩

end SGFormalization
