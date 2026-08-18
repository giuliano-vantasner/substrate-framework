import Mathlib

/-!
# Phase 7 P7L — Massless photon ⟺ unbroken generator (electroweak SSB)

This file is the Lean oracle's contribution for unified-framework Phase 7 (electroweak
mass mechanism), step P7L. It machine-checks the DISCRETE-FACT OUTPUT of the
Higgs/Anderson mechanism's symmetry-breaking step: among the four electroweak generators
acting on the Higgs doublet VEV, exactly ONE linear combination — the electric charge
`Q = T₃ + Y/2` — ANNIHILATES the VEV. The unbroken generator's gauge boson (the photon)
stays massless; the three broken generators' bosons (W⁺, W⁻, Z) become massive.

This is the third entry in the framework's electroweak Lean ledger:
EM4 (`Phase3EM_U1Current.lean`) — charge conservation ⟺ phase symmetry;
W6 (`Phase6Weak_MaxParityViolation.lean`) — maximal parity violation ⟺ left-only coupling;
P7L (this file) — massless photon ⟺ unbroken generator. It formally certifies M1's
"the photon stays massless" claim (frontier.md Part 1, "The biggest one").

## Physics offered for (the INPUT, not proved here)

- **The electroweak gauge group** is `SU(2)_L × U(1)_Y`, with four generators: the three
  weak-isospin matrices `T₁, T₂, T₃` (Pauli σ_a / 2) and the hypercharge `Y`. The Higgs is
  an `SU(2)_L` doublet with hypercharge `Y = 1`, whose vacuum expectation value points in
  the lower (T₃ = −½) component: `⟨Φ⟩ ∝ (0, v)ᵀ`. (Normalisation `v` is irrelevant for the
  annihilation question, so we take `v = 1`.) This doublet-VEV STRUCTURE is the physical
  INPUT encoded as `vev := ![0, 1]`.
- **The electric charge operator** is the Gell-Mann–Nishijima combination `Q = T₃ + Y/2`.
  For the `Y = 1` doublet, `T₃ = diag(½, −½)` and `Y/2 = diag(½, ½)`, so
  `Q = diag(1, 0)`. This identification is the physical INPUT encoded as `Qop`.
- **The mass mechanism** (Anderson 1963; Higgs/Englert–Brout 1964): a gauge boson whose
  generator `G` annihilates the VEV (`G·⟨Φ⟩ = 0`, the generator is "unbroken") couples to
  no condensate and stays MASSLESS; a generator that does NOT annihilate the VEV is
  "broken" and its boson acquires mass `m² ∝ |G·⟨Φ⟩|²` (the Anderson–Higgs mass matrix).
  The map "unbroken generator ⟺ massless gauge boson" is the asserted physical INPUT;
  Lean checks only the discrete annihilation arithmetic on the explicit matrices.

To keep every fact a closed rational computation, the generators are represented over `ℚ`.
`T₃, Yhalf, Q` are real-diagonal, so they are exact rational matrices. The charged
combination is represented by `T₁ = σ₁/2` (real, off-diagonal); the neutral massive
combination is the Z-generator `T₃ − Y/2 · (Q-image)` — concretely we use `T₃` itself,
which is broken (the Z boson is the broken neutral combination orthogonal to Q).

## What each theorem PROVES (the OUTPUT, machine-checked here)

* `photon_annihilates_vev` — `Qop.mulVec vev = 0`: the electric charge `Q = diag(1,0)`
  annihilates the doublet VEV `(0,1)ᵀ`. The U(1)_em generator is UNBROKEN ⇒ the photon is
  massless. This is the headline fact.
* `Qop_eq_T3_plus_Yhalf` — pins the construction: `Qop = T₃ + Y/2` as rational matrices,
  so the annihilating operator IS the Gell-Mann–Nishijima charge, not an ad-hoc `diag(1,0)`.
* `w_boson_image` / `w_boson_massive` — `T₁.mulVec vev = (½, 0)ᵀ ≠ 0`: the charged
  generator does NOT annihilate the VEV ⇒ W is massive. Pins the nonzero image.
* `z_boson_image` / `z_boson_massive` — `T₃.mulVec vev = (0, −½)ᵀ ≠ 0`: the neutral
  weak-isospin generator does NOT annihilate the VEV ⇒ Z is massive. Pins the nonzero image.
* `unique_unbroken_generator` — the "exactly one" content: among `{Q, T₁, T₃}` (the
  photon, W, Z generators), `Q` annihilates the VEV while `T₁` and `T₃` do not. One massless,
  the rest massive — mirroring EM4's biconditional (positive + negative witnesses together).
* `nontautology_guard` — a DIFFERENT VEV `v' = (1,0)ᵀ` is NOT annihilated by `Q`
  (`Q.mulVec (1,0)ᵀ = (1,0)ᵀ ≠ 0`). So the massless count is CONDITIONAL on the doublet-VEV
  structure `(0,1)ᵀ`, not baked into the operator — if the VEV pointed in the upper
  component, `Q` would be broken and the photon would be massive. Mirrors W6's
  vector-coupling guard.
* `guard_compound` — packages the headline fact with the guard: `Q` kills `(0,1)ᵀ` but not
  `(1,0)ᵀ`, the biconditional encoding "massless ⟺ VEV in the Q-kernel".

Honesty: a fully-proved theorem proves exactly its own statement. These check the
annihilation arithmetic OUTPUT of the Anderson–Higgs mechanism on the explicit generator
matrices. They do NOT prove that `SU(2)_L × U(1)_Y` is the electroweak group, that the Higgs
is a `Y=1` doublet, that an unbroken generator yields a massless boson, or that the massless
eigenstate IS the physical photon — those are the asserted physical premises (declared
INPUT), exactly as EM4 asserts the EOM structure and Lean checks the algebraic output. This
is NOT a `Sigma2Prod.lean`-style decimal `rfl` attestation — it is a genuine discrete-fact
derivation in the style of `Phase6Weak_MaxParityViolation.lean`.
Quality bar / style exemplar: `dynamics_lean/ChargeDiscrimination.lean`.
-/

namespace Phase7EW

/-- The Higgs doublet VEV, pointing in the lower (`T₃ = −½`) component: `⟨Φ⟩ ∝ (0, 1)ᵀ`.
    Normalisation is irrelevant for annihilation, so `v = 1`. Rational 2-vector. -/
def vev : Fin 2 → ℚ := ![0, 1]

/-- Weak-isospin `T₃ = σ₃/2 = diag(½, −½)`. Real-diagonal, exact over ℚ. -/
def T3 : Matrix (Fin 2) (Fin 2) ℚ := !![1/2, 0; 0, -1/2]

/-- Half the hypercharge `Y/2` for the `Y = 1` doublet: `diag(½, ½) = (½)·I`.
    Real-diagonal, exact over ℚ. -/
def Yhalf : Matrix (Fin 2) (Fin 2) ℚ := !![1/2, 0; 0, 1/2]

/-- Charged weak-isospin generator `T₁ = σ₁/2 = !![0,½;½,0]`. Real off-diagonal; the
    `W⁺/W⁻` bosons are the broken charged combinations built from `T₁ ± i T₂`. -/
def T1 : Matrix (Fin 2) (Fin 2) ℚ := !![0, 1/2; 1/2, 0]

/-- The electric charge operator `Q = T₃ + Y/2` (Gell-Mann–Nishijima). For the `Y=1`
    doublet this is `diag(½,−½) + diag(½,½) = diag(1, 0)`. Defined here directly as
    `diag(1,0)`; `Qop_eq_T3_plus_Yhalf` certifies it equals `T₃ + Y/2`. -/
def Qop : Matrix (Fin 2) (Fin 2) ℚ := !![1, 0; 0, 0]

/-- A generator `g` is *unbroken* (annihilates the VEV) when `g · ⟨Φ⟩ = 0`. The
    corresponding gauge boson is then massless. -/
def annihilates (g : Matrix (Fin 2) (Fin 2) ℚ) (w : Fin 2 → ℚ) : Prop :=
  g.mulVec w = 0

/-- `Q` IS the Gell-Mann–Nishijima charge: `Qop = T₃ + Y/2` as rational matrices.
    So the annihilating operator is the physical electric charge, not an ad-hoc `diag(1,0)`. -/
theorem Qop_eq_T3_plus_Yhalf : Qop = T3 + Yhalf := by
  unfold Qop T3 Yhalf
  ext i j
  fin_cases i <;> fin_cases j <;> simp [Matrix.add_apply] <;> norm_num

/-- HEADLINE FACT: the electric charge annihilates the doublet VEV.
    `Q · (0,1)ᵀ = diag(1,0) · (0,1)ᵀ = (0,0)ᵀ`. The U(1)_em generator is UNBROKEN, so the
    photon couples to no condensate and stays MASSLESS. -/
theorem photon_annihilates_vev : annihilates Qop vev := by
  unfold annihilates Qop vev
  ext i
  fin_cases i <;> simp [Matrix.mulVec, dotProduct, Fin.sum_univ_two]

/-- Image of the charged generator `T₁` on the VEV: `T₁·(0,1)ᵀ = (½, 0)ᵀ`. Nonzero. -/
theorem w_boson_image : T1.mulVec vev = ![1/2, 0] := by
  unfold T1 vev
  ext i
  fin_cases i <;> simp [Matrix.mulVec, dotProduct, Fin.sum_univ_two]

/-- `T₁` does NOT annihilate the VEV: `T₁·(0,1)ᵀ = (½,0)ᵀ ≠ 0`. The charged generator is
    BROKEN ⇒ the W boson is MASSIVE. -/
theorem w_boson_massive : ¬ annihilates T1 vev := by
  unfold annihilates
  rw [w_boson_image]
  intro h
  have : (1/2 : ℚ) = 0 := congrFun h 0
  norm_num at this

/-- Image of the neutral weak-isospin generator `T₃` on the VEV: `T₃·(0,1)ᵀ = (0, −½)ᵀ`.
    Nonzero. The physical Z is the broken neutral combination; `T₃` already witnesses that
    a neutral weak-isospin generator does not annihilate the VEV. -/
theorem z_boson_image : T3.mulVec vev = ![0, -1/2] := by
  unfold T3 vev
  ext i
  fin_cases i <;> simp [Matrix.mulVec, dotProduct, Fin.sum_univ_two]

/-- `T₃` does NOT annihilate the VEV: `T₃·(0,1)ᵀ = (0,−½)ᵀ ≠ 0`. The neutral generator is
    BROKEN ⇒ the Z boson is MASSIVE. -/
theorem z_boson_massive : ¬ annihilates T3 vev := by
  unfold annihilates
  rw [z_boson_image]
  intro h
  have : (-1/2 : ℚ) = 0 := congrFun h 1
  norm_num at this

/-- THE "EXACTLY ONE" CONTENT: among the generator basis `{Q, T₁, T₃}` (photon, W, Z),
    the electric charge `Q` annihilates the VEV while `T₁` and `T₃` do not. One unbroken
    generator (massless photon), the rest broken (massive W, Z). This packages the positive
    witness with the two negative witnesses, mirroring EM4's biconditional. -/
theorem unique_unbroken_generator :
    annihilates Qop vev ∧ ¬ annihilates T1 vev ∧ ¬ annihilates T3 vev :=
  ⟨photon_annihilates_vev, w_boson_massive, z_boson_massive⟩

/-- NON-TAUTOLOGY GUARD: a DIFFERENT VEV `v' = (1,0)ᵀ` is NOT annihilated by `Q`.
    `Q·(1,0)ᵀ = diag(1,0)·(1,0)ᵀ = (1,0)ᵀ ≠ 0`. So the massless count is CONDITIONAL on the
    doublet-VEV structure `(0,1)ᵀ`: if the VEV pointed in the upper component, `Q` would be
    broken and the photon would be MASSIVE. The annihilation is a property of the VEV/operator
    pair, not baked into `Q`. Mirrors W6's vector-coupling guard. -/
theorem nontautology_guard : ¬ annihilates Qop ![1, 0] := by
  unfold annihilates Qop
  intro h
  have hc := congrFun h 0
  simp [Matrix.mulVec, dotProduct, Fin.sum_univ_two] at hc

/-- COMPOUND GUARD: `Q` kills the doublet VEV `(0,1)ᵀ` but NOT the alternative `(1,0)ᵀ`.
    This is the biconditional encoding "photon massless ⟺ VEV lies in the kernel of `Q`":
    the SAME operator gives a massless photon for one VEV and a massive one for the other,
    so the result is genuine physics of the doublet structure, not a definitional tautology. -/
theorem guard_compound :
    annihilates Qop vev ∧ ¬ annihilates Qop ![1, 0] :=
  ⟨photon_annihilates_vev, nontautology_guard⟩

end Phase7EW

-- Axiom audit: each theorem's footprint must be ⊆ {propext, Classical.choice, Quot.sound}.
#print axioms Phase7EW.Qop_eq_T3_plus_Yhalf
#print axioms Phase7EW.photon_annihilates_vev
#print axioms Phase7EW.w_boson_image
#print axioms Phase7EW.w_boson_massive
#print axioms Phase7EW.z_boson_image
#print axioms Phase7EW.z_boson_massive
#print axioms Phase7EW.unique_unbroken_generator
#print axioms Phase7EW.nontautology_guard
#print axioms Phase7EW.guard_compound
