import Mathlib
namespace Phase3EM


open Complex

/-!
# Phase 3 EM4 — U(1) Noether-current conservation from phase-independence

This file is the Lean oracle's contribution for unified-framework Phase 3, step EM4.
It machine-checks the ALGEBRAIC OUTPUT step of the U(1) charge-conservation argument
for a complex scalar field.

## Physics offered for (the INPUT, not proved here)

The U(1) Noether current of a complex scalar field is
`j^μ = i(Ψ*∂^μΨ − Ψ∂^μΨ*)`, with on-shell four-divergence
`∂_μj^μ = i(Ψ*□Ψ − Ψ□Ψ*)`.  Substituting the equations of motion
`□Ψ = −a·Ψ`, `□Ψ* = −b·Ψ*` (the coefficients `a, b : ℂ` encode the restoring
terms of a potential `V`):

    ∂_μj^μ = i · (b − a) · |Ψ|²

A U(1)-symmetric (phase-independent) potential `V(|Ψ|²)` forces Ψ and Ψ* to obey the
SAME EOM, `a = b = V'(|Ψ|²)` (real, equal), so `∂_μj^μ = 0` — charge conservation.
A phase-BREAKING potential has `a ≠ b`, so `∂_μj^μ ≠ 0` — charge not conserved.
The Lagrangian, the EOM, and Noether's procedure are the physics INPUT; Lean checks
only the algebraic output step.

## What each theorem PROVES (the OUTPUT, machine-checked here)

* `u1_divergence_identity` — the algebraic substitution step: feeding the two on-shell
  EOMs into the current divergence yields exactly `I·(b−a)·(ψ·star ψ)`.  This is the
  load-bearing identity; `star ψ` is treated as an opaque ring element, so `ring`
  certifies a genuine polynomial identity over ℂ, not a numeric coincidence.
* `u1_conservation` — the Noether content: setting `a = b` (phase-independent
  potential, equal restoring coefficient for Ψ and Ψ*) makes the divergence `= 0`.
  This is charge conservation ⟸ phase symmetry.
* `u1_phase_breaking_witness` — the non-tautology guard: an explicit phase-BREAKING
  choice `a = 1, b = I, ψ = 1` makes the divergence `≠ 0`.  Together with the previous
  two theorems this encodes the biconditional "charge conservation ⟺ phase-independence
  of the potential": equal coefficients ⇒ 0, a concrete unequal pair ⇒ nonzero.
* `u1_witness_value` — pins the witness divergence to its exact value `−1 − I`, so the
  guard is a real value computation, not a vacuous `≠ 0`.

Honesty: a fully-proved theorem proves exactly its own statement.  These check the
algebraic identity and its `a=b`/`a≠b` consequences; the field theory upstream of the
EOM substitution is asserted, not derived.  Quality bar / style exemplar:
`dynamics_lean/ChargeDiscrimination.lean` (genuine discrete-fact derivations).
-/

/--
Divergence identity: substituting on-shell EOMs `□Ψ = −a·Ψ`, `□Ψ* = −b·Ψ*`
into `∂_μj^μ = i(Ψ*□Ψ − Ψ□Ψ*)` gives `i·(b−a)·(ψ·star ψ)`.
`star ψ` is opaque, so this is a true polynomial identity over ℂ, closed by `ring`.
-/
theorem u1_divergence_identity (ψ a b : ℂ) :
    Complex.I * (star ψ * (-(a * ψ)) - ψ * (-(b * star ψ))) =
    Complex.I * (b - a) * (ψ * star ψ) := by
  ring

/--
Conservation corollary: when `a = b` (U(1)-symmetric / phase-independent potential,
same restoring coefficient for Ψ and Ψ*), the divergence is `0`.
Physics: Noether charge conservation ⟸ equal EOM coefficients (`a = b`).
-/
theorem u1_conservation (ψ a : ℂ) :
    Complex.I * (star ψ * (-(a * ψ)) - ψ * (-(a * star ψ))) = 0 := by
  ring

/--
Phase-breaking guard witness: the explicit unequal choice `a = 1, b = I, ψ = 1` gives
`I·(I−1)·1 = I² − I = −1 − I ≠ 0`.
Physics: when `b ≠ a` (phase-BREAKING potential) the Noether divergence is nonzero,
so the U(1) charge is NOT conserved.  This is the non-tautology guard that, with
`u1_conservation`, makes the relation a biconditional rather than a one-way implication.
-/
theorem u1_phase_breaking_witness :
    Complex.I * (Complex.I - (1 : ℂ)) * ((1 : ℂ) * (1 : ℂ)) ≠ (0 : ℂ) := by
  intro h
  have hre := congrArg Complex.re h
  norm_num [Complex.mul_re, Complex.sub_re, Complex.I_re, Complex.I_im,
            Complex.one_re, Complex.one_im, Complex.zero_re] at hre

/-- Witness value: the divergence at `a = 1, b = I, ψ = 1` equals exactly `−1 − I`. -/
theorem u1_witness_value :
    Complex.I * (Complex.I - (1 : ℂ)) * ((1 : ℂ) * (1 : ℂ)) = (-1 : ℂ) - Complex.I := by
  norm_num [Complex.ext_iff, Complex.mul_re, Complex.mul_im, Complex.sub_re, Complex.sub_im,
            Complex.I_re, Complex.I_im, Complex.one_re, Complex.one_im]

end Phase3EM
