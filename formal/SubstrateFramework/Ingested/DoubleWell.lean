/-
The double-well piston and its projection onto the lowest
two-level system.  This is the quantum→classical bridge for R1:
the boundary degree of freedom ψ(t) with

  ℒ_boundary = ½ μ ψ̇² − V(ψ) − g ψ φ(0,t) + J_ext(t) ψ

where V(ψ) = (κ/4)(ψ² − ψ₀²)² is the double well.
-/

import Mathlib
namespace SGDoubleWell


open Real

/--
Double-well potential: V(ψ) = (κ/4)·(ψ² − ψ₀²)².
Minima at ψ = ±ψ₀, barrier height κ ψ₀⁴ / 4.
-/
noncomputable def doubleWellPotential (κ ψ₀ : ℝ) (ψ : ℝ) : ℝ :=
  (κ / 4) * ((ψ ^ 2 - ψ₀ ^ 2) ^ 2)

/--
Barrier height: V(0) − V(±ψ₀) = κ ψ₀⁴ / 4.
-/
theorem barrier_height (κ ψ₀ : ℝ) :
    doubleWellPotential κ ψ₀ 0 - doubleWellPotential κ ψ₀ ψ₀ = (κ / 4) * ψ₀ ^ 4 := by
  dsimp [doubleWellPotential]
  ring

/--
Derivative of the double-well potential: V'(ψ) = κ·ψ·(ψ² − ψ₀²).
-/
noncomputable def doubleWellDerivative (κ ψ₀ : ℝ) (ψ : ℝ) : ℝ :=
  κ * ψ * (ψ ^ 2 - ψ₀ ^ 2)

/--
The classical equation of motion for the piston with coupling to the boundary field:
  μ ψ̈ + V'(ψ) = g φ(0,t) + J_ext(t).

Uses `HasDerivAt` to express the second derivative condition.
-/
def pistonEquationOfMotion
    (μ κ ψ₀ g : ℝ) (φ0 J_ext : ℝ → ℝ) (ψ : ℝ → ℝ) (t : ℝ) (ψ'' : ℝ) : Prop :=
  HasDerivAt ψ (deriv ψ t) t ∧ HasDerivAt (deriv ψ) ψ'' t ∧ μ * ψ'' + doubleWellDerivative κ ψ₀ (ψ t) = g * φ0 t + J_ext t

/-
In the quantum theory, ψ becomes a Hermitian operator ψ̂ with canonical
momentum p̂ = −iℏ ∂/∂ψ.  The Hamiltonian is

  Ĥ(t) = p̂²/(2μ) + V(ψ̂) − g φ(0,t) ψ̂ − J_ext(t) ψ̂.

Projected onto the two lowest-lying states (the symmetric/antisymmetric
combinations of the localized well ground states), ψ̂ reduces to ψ₀ σ_x
in the {|+⟩, |−⟩} basis, giving

  Ĥ_eff(t) = (Δ/2) σ_z − [g φ(0,t) + J_ext(t)] ψ₀ σ_x

where Δ = E_− − E_+ is the tunnel splitting (the minimal gap).
-/

-- Matrix representation of the effective two-level Hamiltonian
-- in the {|+⟩, |−⟩} basis.
noncomputable def hamiltonianEff (Δ gψ₀ : ℝ) (drive : ℝ → ℝ) (t : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![ (gψ₀ / 2) * drive t,  Δ / 2 ;
      Δ / 2,               -(gψ₀ / 2) * drive t ]

/-
In the diabatic basis (rotated by π/4), the LZ form is

  Ĥ_LZ(t) = (ε(t)/2) σ_z + (Δ/2) σ_x

where ε(t) is the sweep (diagonal bias) and Δ is the constant off-diagonal
gap.  This is the standard Landau–Zener Hamiltonian.
-/

/--
The diabatic Landau–Zener Hamiltonian:
  Ĥ_LZ(t) = (ε(t)/2) σ_z + (Δ/2) σ_x.
-/
noncomputable def hamiltonianLZ (Δ : ℝ) (epsilon : ℝ → ℝ) (t : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![ (epsilon t) / 2,  Δ / 2 ;
      Δ / 2,           -(epsilon t) / 2 ]

/-
The relationship between the two representations:
ε(t) = 2·[g φ(0,t) + J_ext(t)]·ψ₀,  Δ = Δ_min (tunnel splitting).

The sweep rate at the crossing (ε(t*)=0) is v_sweep = dε/dt|_*.
-/

/--
Sweep rate at the instant of level crossing.
For ε(t) = α·t (linear sweep): v_sweep = α.
More generally: v_sweep = dε/dt evaluated where ε = 0.
-/
noncomputable def sweepRate (epsilon : ℝ → ℝ) (t : ℝ) : ℝ :=
  deriv epsilon t

end SGDoubleWell
