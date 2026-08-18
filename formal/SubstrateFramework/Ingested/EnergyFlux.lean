/-
Energy flux at the driven boundary.

From the stress-energy tensor T₀₁ = −φ_t φ_x, the power flowing
from the bulk into the boundary at x=0 is

  dE/dt = −φ_t(0,t) · φ_x(0,t).

For the piston coupling φ_x(0,t) = g ψ(t):
  dE/dt = −g · φ_t(0,t) · ψ(t).

The total energy transferred during the breather impact is
  ΔE = ∫ dE/dt dt.

Reference: dynamics/01_collective_coordinates.md eq (1.7–1.8).
-/

import Mathlib
namespace SGEnergyFlux

open Real

/--
Energy flux (power) from the bulk into the boundary at x=0.
Positive flux = energy flows from boundary into bulk (drive pumping).
Negative flux = energy absorbed from bulk by boundary.
-/
def energyFlux (φ_t φ_x : ℝ) : ℝ :=
  -(φ_t) * φ_x

/--
Energy flux through a piston boundary: φ_x(0,t) = g ψ(t).

  dE/dt = −g · φ_t · ψ.
-/
def energyFluxPiston (g φ_t ψ : ℝ) : ℝ :=
  -g * φ_t * ψ

/--
When φ_t and φ_x have the same sign, energy flows INTO the boundary
(negative flux, the boundary absorbs energy from the field).
-/
theorem energyFlux_sign_absorbing (φ_t φ_x : ℝ) (hφ_t : 0 < φ_t) (hφ_x : 0 < φ_x) :
    energyFlux φ_t φ_x < 0 := by
  dsimp [energyFlux]
  nlinarith

/--
When φ_t and φ_x have opposite signs, energy flows OUT of the boundary
(positive flux, the boundary pumps energy into the field).
This is the regime needed for ionization — the boundary supplies ΔE(w).
-/
theorem energyFlux_sign_pumping (φ_t φ_x : ℝ) (hφ_t : 0 < φ_t) (hφ_x : φ_x < 0) :
    0 < energyFlux φ_t φ_x := by
  dsimp [energyFlux]
  nlinarith

/--
Zero energy flux if either φ_t or φ_x vanishes at the boundary.
-/
theorem energyFlux_zero_if_either_zero (φ_t φ_x : ℝ) (h : φ_t = 0 ∨ φ_x = 0) :
    energyFlux φ_t φ_x = 0 := by
  rcases h with h | h
  · simp [energyFlux, h]
  · simp [energyFlux, h]

/--
The energy flux through the piston is proportional to g, φ_t, and ψ.
If any factor is zero, no energy is transferred.
-/
theorem energyFluxPiston_zero_if_any_zero (g φ_t ψ : ℝ)
    (h : g = 0 ∨ φ_t = 0 ∨ ψ = 0) : energyFluxPiston g φ_t ψ = 0 := by
  rcases h with h | h | h
  · simp [energyFluxPiston, h]
  · simp [energyFluxPiston, h]
  · simp [energyFluxPiston, h]
end SGEnergyFlux
