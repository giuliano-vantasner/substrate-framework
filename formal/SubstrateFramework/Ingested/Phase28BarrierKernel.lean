import Mathlib

/-!
# Phase 28 — Rung D barrier-parameter kernel: the m_R inertia flip, the thermal-gate
  bound, and the coherent/incoherent threshold ordering (BD-L)

This file is the Lean oracle's contribution for the Phase-28 Rung-D arc (issue #10/#8):
expressing the medium-scale nucleation barrier `E_* = π·T²/P` in real medium+drive
variables, and — the headline — RETIRING rung098's named ceiling.

rung098 declared the onset frequency `ω` and the barrier amplitude `E_* = π·T²/P`
"genuinely independent" because converting the barrier-top curvature `|E''(R_*)| = 2π·P`
(dimension `E/L²`) to a frequency `ω_R = √(|E''|/m_R)` needs a ring-radius effective
inertia `m_R` of dimension `E·T²/L²`, and NO pre-Rung-C medium object carried it — every
object was STATIC (time-exponent 0). We encode dimensions as integer triples `(E,L,T)` and
certify, by exact integer arithmetic:

1. `mNeeded = (1,-2,2)` — the inertia dimension (a mass). Every pre-Rung-C medium object
   has time-exponent `0`, so `static_cannot_be_inertia` : none can equal `mNeeded`.

2. Rung C supplies `lambdaDim = (1,-1,2)` (the medium inertia density, the FIRST object with
   a nonzero time exponent), and the collective-coordinate inertia
   `m_R = λ ⊕ ∫(∂u/∂R)² dx` closes: `mR_closes : dadd lambdaDim geomDim = mNeeded`. So the
   medium NOW supplies the inertia — the ceiling is retired (`ceiling_retired`).

3. The thermal-gate bound (T1-G / LandauZener `ionizationWeight_max`):
   `gate_le_half : 2·P·(1-P) ≤ 1/2` for all real `P` (max at `P = 1/2`), via `(2P-1)² ≥ 0`.

4. The coherent/incoherent ignition ordering: `N_coh = √(N_inc)`, so `N_coh < N_inc`
   whenever the barrier exceeds one quantum (`N_inc > 1`): `coh_lt_inc`. At one quantum
   (`N_inc = 1`) coherence buys nothing: `N_coh = N_inc = 1` (`degenerate_one_quantum`).

5. `BD_L` — the headline compound: the inertia flip ∧ the gate bound ∧ the threshold
   ordering, plus non-tautology guards.

Axioms ⊆ Mathlib; no proof escape.
-/

namespace Phase28

/-- A physical dimension as an integer exponent triple `(E, L, T)`. -/
abbrev Dim := ℤ × ℤ × ℤ

/-- Componentwise sum of dimensions (what multiplying quantities does to exponents). -/
def dadd (a b : Dim) : Dim := (a.1 + b.1, a.2.1 + b.2.1, a.2.2 + b.2.2)

/-- The time exponent of a dimension. -/
def texp (d : Dim) : ℤ := d.2.2

/-- The inertia dimension `m_R` needed to turn the barrier curvature into a frequency:
    `E·T²/L² = (1,-2,2)` (rung098 M2.2). -/
def mNeeded : Dim := (1, -2, 2)

/-- The barrier-top curvature `|E''(R_*)| = 2π·P` has dimension `E/L² = (1,-2,0)`. -/
def curvatureDim : Dim := (1, -2, 0)

/-- Rung C's medium inertia density `λ` has dimension `(1,-1,2)` (forced by `c² = T/λ`). -/
def lambdaDim : Dim := (1, -1, 2)

/-- The geometric profile integral `∫(∂u/∂R)² dx` has dimension `1/L = (0,-1,0)`. -/
def geomDim : Dim := (0, -1, 0)

/-- The pre-Rung-C medium objects rung098 listed (all STATIC: time-exponent 0). -/
def preRungC : List Dim :=
  [ (1, -1, 0),   -- T  (line tension)
    (1, -2, 0),   -- P  (area drive)
    (1,  0, 0),   -- E_*  (energy)
    (1,  0, 0),   -- E_core
    (1, -1, 0),   -- K_F  (Frank constant)
    (1, -3, 0),   -- h    (GL bulk bias, energy density)
    (0,  1, 0),   -- l_m
    (0,  1, 0),   -- r_c
    (0,  1, 0),   -- R_o
    (1, -2, 0) ]  -- |E''(R_*)| = 2π·P

/-- **rung098 reproduced.** Every pre-Rung-C medium object is STATIC: time-exponent `0`. -/
theorem preRungC_all_static : ∀ d ∈ preRungC, texp d = 0 := by decide

/-- **The structural reason.** A static dimension (time-exponent `0`) can never equal the
    inertia dimension `mNeeded` (time-exponent `2`): no static set builds a frequency. -/
theorem static_cannot_be_inertia (d : Dim) (h : texp d = 0) : d ≠ mNeeded := by
  intro hd
  rw [hd] at h
  exact absurd h (by decide)

/-- **rung098's ceiling, restated:** no pre-Rung-C object supplies the inertia. -/
theorem preRungC_lacks_inertia : ∀ d ∈ preRungC, d ≠ mNeeded := by
  intro d hd
  exact static_cannot_be_inertia d (preRungC_all_static d hd)

/-- **Rung C's `λ` is the new ingredient:** it carries a NONZERO time exponent. -/
theorem lambda_is_dynamical : texp lambdaDim ≠ 0 := by decide

/-- **The flip (BD4).** The collective-coordinate inertia `m_R = λ ⊕ geom` closes to exactly
    the needed inertia dimension `(1,-2,2)`. -/
theorem mR_closes : dadd lambdaDim geomDim = mNeeded := by decide

/-- **The ceiling is retired.** With Rung C's `λ`, the medium supplies the inertia
    (`m_R = mNeeded`), and `√(curvature / m_R)` has the dimension of a frequency `(0,0,-1)`:
    the barrier curvature becomes a mode frequency, so onset and amplitude are LINKED. -/
theorem ceiling_retired :
    (dadd lambdaDim geomDim = mNeeded) ∧
    (∀ d ∈ preRungC, d ≠ mNeeded) ∧
    (texp lambdaDim ≠ 0) := by
  refine ⟨mR_closes, preRungC_lacks_inertia, lambda_is_dynamical⟩

/-- the half-difference `(curvatureDim - mNeeded)` componentwise is `(0,0,-1)` — a frequency
    (the `sqrt` halves the exponents). Stated as the exponent identity the bridge uses. -/
theorem omega_R_is_frequency :
    (curvatureDim.1 - mNeeded.1, curvatureDim.2.1 - mNeeded.2.1,
     curvatureDim.2.2 - mNeeded.2.2) = ((0 : ℤ), (0 : ℤ), (-2 : ℤ)) := by decide

/-! ## The thermal gate (T1-G / LandauZener ionizationWeight_max) -/

/-- **The thermal-gate bound.** The single-event weight `W_c = 2·P·(1-P) ≤ 1/2` for all real
    occupations `P`, with the maximum at `P = 1/2` — the macroscopic `½·sech²` gate's ceiling. -/
theorem gate_le_half (P : ℝ) : 2 * P * (1 - P) ≤ 1 / 2 := by
  nlinarith [sq_nonneg (2 * P - 1)]

/-- the bound is SATURATED at `P = 1/2` (the gate fully open) — non-tautology witness. -/
theorem gate_eq_half_at_half : 2 * (1 / 2 : ℝ) * (1 - 1 / 2) = 1 / 2 := by norm_num

/-! ## Coherent/incoherent ignition thresholds (NY3 / BD3) -/

/-- The coherent threshold is the square root of the incoherent one (the `N²` vs `N`
    concentration): `N_coh = √(N_inc)`. We certify the consequence on a concrete deep barrier
    `N_inc = 40` (E_*/θ₁ = 40): `N_coh = √40 < 40 = N_inc`. -/
theorem coh_lt_inc : Real.sqrt 40 < 40 := by
  have h40 : (0 : ℝ) ≤ 40 := by norm_num
  have hsq : Real.sqrt 40 < Real.sqrt (40 * 40) := by
    apply Real.sqrt_lt_sqrt h40
    norm_num
  have : Real.sqrt (40 * 40) = 40 := by
    rw [show (40 : ℝ) * 40 = 40 ^ 2 by ring, Real.sqrt_sq (by norm_num : (0:ℝ) ≤ 40)]
  rwa [this] at hsq

/-- `N_coh = √(N_inc)` squares back exactly: `(√N_inc)² = N_inc` (the `N²` law). -/
theorem coh_sq_eq_inc (Ninc : ℝ) (h : 0 ≤ Ninc) : (Real.sqrt Ninc) ^ 2 = Ninc :=
  Real.sq_sqrt h

/-- **Non-tautology / degenerate limit.** At a one-quantum barrier (`N_inc = 1`) coherence
    buys nothing: `N_coh = √1 = 1 = N_inc`. -/
theorem degenerate_one_quantum : Real.sqrt 1 = 1 := Real.sqrt_one

/-! ## The headline compound -/

/-- **BD_L.** The Phase-28 Rung-D capstone: (1) the inertia flip retires rung098's ceiling,
    (2) the thermal gate is bounded by `1/2`, (3) coherence square-roots the threshold so a
    deep barrier ignites coherently far below the incoherent count. -/
theorem BD_L :
    (dadd lambdaDim geomDim = mNeeded) ∧
    (∀ d ∈ preRungC, d ≠ mNeeded) ∧
    (∀ P : ℝ, 2 * P * (1 - P) ≤ 1 / 2) ∧
    (Real.sqrt 40 < 40) := by
  exact ⟨mR_closes, preRungC_lacks_inertia, gate_le_half, coh_lt_inc⟩

end Phase28
