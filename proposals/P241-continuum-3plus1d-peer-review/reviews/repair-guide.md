# P241 Repair Guide — Minimum Honest Corrections, Equation by Equation

Each entry: **defect → replacement text/construct → oracle that guards it.**
Apply top-down; later repairs assume earlier ones (S23 composes everything).

## 1. Units (S02) — replace the Section 2 bullet list

Printed: `u` dimensionless; Θ_ij in N = kg·m·s⁻². Inconsistent with
c0² = Θ0/ρ0 and Z0 = ρ0^{1/3}(detΘ)^{1/3}.

Replace with:

| quantity | dimension | MKS |
|---|---|---|
| u | length | m |
| Θ_ij | energy density = Pa | kg·m⁻¹·s⁻² |
| ρ0 | mass density | kg·m⁻³ |
| c0² = Θ0/ρ0 | speed² | m²·s⁻² |
| Z0 = ρ0^{1/3}(detΘ)^{1/3} | mechanical impedance | kg·m⁻²·s⁻¹ |
| μ0 | inverse length | m⁻¹ |
| M0 | mass | kg |

Guard: `corpus/checks/sympy/S02_dimension_declarations.py`.

## 2. Static existence (S05) — restate Section 3 scope

Add after Eq. (15): "For the uncharged static class Derrick's scaling gives
E(λ)=E_g/λ+E_p/λ³, strictly decreasing in d=3; static finite-energy lumps are
excluded. The localized objects of this paper are time-dependent."

Guard: `corpus/checks/sympy/S05_derrick_obstruction.py`;
Lean `P241PaperChecks.derrick_derivative_negative`.

## 3. Oscillon/pulson language (S06)

Either (a) declare a nonconvex potential explicitly (the sine–Gordon class of
[1] suffices for 1+1D; for 3+1D state the model as open), or (b) weaken to
"time-dependent localized solutions are sought; existence is deferred."
Do not assert oscillons for the displayed convex U(u).

Guard: `corpus/checks/scipy/N01_oscillon_existence.py` (Part A decay +
Part B sine–Gordon breather control).

## 4. Reflectionless claim (S08)

Replace "matched ⇒ reflectionless" with: an interface between media A, B is
reflectionless iff Z_A(n̂) = Z_B(n̂) for the propagation direction n̂, where
Z(n̂)² = ⟨n̂, ρ n̂⟩/⟨n̂, Θ⁻¹n̂⟩. The scalar condition covers isotropic media
only.

Guards: `corpus/checks/sympy/S08_directional_impedance.py`,
`corpus/checks/scipy/N03_impedance_interface.py`.

## 5. Rest-mass constancy (S10)

Insert hypothesis H-M0 before Eq. (21): "H-M0 (adiabatic isolation): the
profile integrals E0(X) are constant along the trajectory." Note explicitly
that without H-M0 the trajectory equations acquire non-geodesic terms.

Guard: `corpus/checks/sympy/S10_rest_mass_variation.py`.

## 6. Newtonian limit (S18) — replace Eq. (43)

Displayed (43): d²X/dt² = −(c0²/2)∇log n̄.
Corrected: `d²X/dt² = +c0² ∇(n̄)/(2 n̄³)` (equivalently +(c0²/2)∇log n̄ /n̄²).
Direction: toward increasing index — as the manuscript's own prose states.
Keep the M0-independence sentence; it is correct.

Guards: `corpus/checks/sympy/S18_newtonian_limit_sign.py`;
Lean `eq43_*`, `corrected_newtonian_law_positive`.

## 7. Massless extension (S19) — rewrite Section 7 close

Delete "including the massless case". Insert: "Massive universality holds:
no M0 enters the acceleration law. Massless probes follow Fermat rays of
index n̄²; their leading transverse acceleration is exactly twice the massive
value (analogue of the GR light-bending factor)."

Guards: `corpus/checks/sympy/S19_massless_factor_two.py`,
`corpus/checks/scipy/N05_null_massive_deflection.py`,
Lean `section7_massless_ratio_is_two`.

## 8. Schwarzschild realization (S20)

Replace implicit profiles with: Ω²(r)=f^{−1/3}, f=1−r_s/r;
n_r=f^{−4/3}; n_t=n_φ=f^{−1/3}; λ_r=c0²f^{8/3}; λ_t=λ_φ=c0²f^{2/3}.
Then g_induced = Ω² · g_Schwarzschild(length coords) componentwise exactly.

Guard: `corpus/checks/sympy/S20_schwarzschild_corrected.py`; Lean probe at
f=8/27 (`omega_cubed_inverts_f`).

## 9. Kerr dictionary (S21) — replace Eqs. (55)-(57)

With r_s = 2GM/c0², Δ=r²−r_s r+a², Σ=r²+a²cos²θ,
𝒜=(r²+a²)²−a²Δsin²θ, X = r_s²c0⁴a²r²sin²θ:

* Ω⁴ = (Δ r⁴/(Σ𝒜))^{1/3} · Σ𝒜/(𝒜Δ+X)   [core identity K(Q+R)=1]
* n_r = Ω²Σ/Δ,  n_θ = Ω²Σ/r²,  n_φ = Ω²𝒜/(Σr²)
* V_φ = −r_s a c0³ r² sinθ/𝒜

All five Kerr components match up to the declared Ω²(r,θ); null geodesics
are exactly Kerr's.

Guards: `corpus/checks/sympy/S21_kerr_dictionary_audit.py` (defects),
`corpus/checks/sympy/S21_kerr_corrected_dictionary.py` (repair);
Lean `kerr_equator_Ag_is_r_squared_G`, `eq56_drops_sigma_squared`,
`eq57_c0_power_slip`, `kerr_corrected_core_identity`.

## 10. Minimal-model naming (S22)

Rename (58)-(60) to "minimal rotating acoustic model" and cite [2] (the
published 2+1D paper) as provenance; note it is not the θ=π/2 slice of the
full construction.

Guard: `corpus/checks/sympy/S22_minimal_model_published.py`.

## 11. Section 10 composition (S23)

Restate the chain with its scopes attached:

> Under H-M0 and a declared nonconvex potential, impedance-matched continua
> whose eikonal reduction closes produce induced metrics realizing special
> relativity kinematically, with universal free fall across massive lumps
> (massless probes follow the doubled null law), realized exactly up to a
> conformal factor for Schwarzschild and Kerr.

Delete or scope the headline sentence ("first fundamental advancement since
Einstein 1907").
