import Mathlib

/-!
# Phase 11 FG-L — the discrete flavor parameter counts (CP phases, mixing angles)

This file is the Lean oracle's capstone for unified-framework Phase 11 (the flavor / CP
ledger). It machine-checks the DISCRETE-FACT OUTPUT of the counting argument behind the
Cabibbo–Kobayashi–Maskawa structure: how many physical parameters survive in the unitary
quark-mixing matrix once the unremovable phases are taken out. The headline arithmetic is the
Kobayashi–Maskawa content — with `N` fermion generations a unitary `N×N` mixing matrix carries
`N(N−1)/2` real MIXING ANGLES and `(N−1)(N−2)/2` physical CP-violating PHASES, the rest
(`2N−1` phases) being removable by rephasing the quark fields. The physical punchline is
`cpPhases 2 = 0` (NO CP violation with two generations) and `cpPhases 3 = 1` (exactly ONE
physical CP phase with three generations) — i.e. CP violation in the SM mixing sector REQUIRES
at least three generations.

This is the fifth entry in the framework's gauge / flavor Lean ledger, alongside
QCD4 (`Phase8QCD_SU3GaugeFacts.lean`)        — the eight gluons and the SU(3) Casimir facts;
SM-L (`Phase9SM_AnomalyCancellation.lean`)   — per-generation anomaly cancellation;
CF-L (`Phase10CF_Z3CenterConfinement.lean`)  — the Z₃ center + area-law confinement;
FG-L (this file)                             — the CP-phase / mixing-angle parameter counts.

## Physics offered for (the INPUT, not proved here)

- **The quark-mixing matrix is unitary, `N×N`, for `N` generations.** A general `U(N)` matrix
  has `N²` real parameters. Of these, `N(N−1)/2` are real rotation (Euler) MIXING ANGLES and
  the remaining `N(N+1)/2` are phases. The relative phases of the `2N` quark fields (up-type
  and down-type) can be rephased away, but one overall phase is common and does not act on the
  matrix, so exactly `2N − 1` phases are REMOVABLE. The PHYSICAL CP-violating phases that
  survive are therefore `N(N+1)/2 − (2N − 1) = (N−1)(N−2)/2`. That the mixing matrix is unitary,
  that quark fields may be rephased, and that a CP-violating observable requires a non-removable
  complex phase, are the asserted physical INPUTS (the Kobayashi–Maskawa 1973 counting). Lean
  checks only the resulting integer arithmetic of the counts and the parameter identity.

- **CP violation ⟺ a surviving physical phase.** A non-zero `cpPhases N` is the number of
  irreducible complex phases in the mixing matrix; CP is violated (in this sector) iff at least
  one such phase survives. That this counting IS the criterion for CP violation is the asserted
  INPUT; Lean checks that the count vanishes for `N ≤ 2` and is positive only for `N ≥ 3`.

## What each theorem PROVES (the OUTPUT, machine-checked here)

* `cpPhases_two`   — `cpPhases 2 = 0`: NO physical CP phase at two generations (the
  Kobayashi–Maskawa content / NON-TAUTOLOGY witness — CP violation is impossible with 2 families).
* `cpPhases_three` — `cpPhases 3 = 1`: exactly ONE physical CP phase at three generations (the
  single CKM phase `δ`).
* `mixingAngles_two` / `mixingAngles_three` — `1` / `3`: the one Cabibbo angle (N=2) and the
  three CKM mixing angles `θ₁₂, θ₁₃, θ₂₃` (N=3).
* `param_count_identity` — the LOAD-BEARING general theorem: for every `N`,
  `N² = mixingAngles N + removablePhases N + cpPhases N`, i.e. the `N²` real parameters of a
  unitary `N×N` matrix split EXACTLY into mixing angles, removable phases, and physical CP
  phases. Proved in division-free doubled form to dodge ℕ truncated subtraction/division, by
  case-splitting `N` to expose the successor and closing with `ring`/`omega`.
* `cp_requires_three_generations` — the PHYSICAL HEADLINE: `cpPhases N > 0 → 3 ≤ N`. CP
  violation in the mixing sector requires at least three generations.
* `cp_vanishes_below_three` — the contrapositive form: `N ≤ 2 → cpPhases N = 0`.
* `nontautology_cp_two_ne_three` — NON-TAUTOLOGY GUARD: `cpPhases 2 ≠ cpPhases 3` (`0 ≠ 1`),
  isolating the genuine N=2 vs N=3 distinction; the counts are NOT a vacuous constant.
* `flavor_count_compound` — packages the instances, the parameter identity, the CP-threshold,
  and the non-tautology guard into one fact.

Honesty: a fully-proved theorem proves exactly its own statement. These check the INTEGER
arithmetic OUTPUT of the Kobayashi–Maskawa parameter count (the angle / removable-phase /
CP-phase split of `N²`) evaluated on `N` and on the instances `N = 2, 3`. They do NOT prove
that the mixing matrix is unitary, that quark fields may be rephased, or that a surviving phase
is the physical CP-violation criterion — those are the asserted physical premises (declared
INPUT), exactly as SM-L asserts the matter content and CF-L asserts the area law. This is NOT a
decimal `rfl` attestation: it is a genuine discrete-fact derivation — a general parameter
identity over `N`, proved escape-free, applied to the physical instances, with a non-tautology
guard separating N=2 (no CP) from N=3 (one CP phase).
-/

namespace Phase11Flavor

/-! ## Part 1 — the three flavor parameter counts (Kobayashi–Maskawa) -/

/-- The number of real MIXING (Euler / rotation) ANGLES in a unitary `N×N` mixing matrix:
    `N(N−1)/2`. For `N = 2` this is the single Cabibbo angle; for `N = 3` the three CKM angles. -/
def mixingAngles (N : ℕ) : ℕ := N * (N - 1) / 2

/-- The number of physical CP-violating PHASES surviving in a unitary `N×N` mixing matrix after
    rephasing: `(N−1)(N−2)/2`. The Kobayashi–Maskawa count: `0` for `N ≤ 2`, `1` for `N = 3`. -/
def cpPhases (N : ℕ) : ℕ := (N - 1) * (N - 2) / 2

/-- The number of REMOVABLE phases — the relative phases of the `2N` quark fields, minus the one
    overall common phase that does not act on the matrix: `2N − 1`. -/
def removablePhases (N : ℕ) : ℕ := 2 * N - 1

/-! ## Part 2 — the physical instances (the OUTPUT at N = 2 and N = 3) -/

/-- NON-TAUTOLOGY WITNESS: `cpPhases 2 = 0` — there is NO physical CP-violating phase with two
    generations. `(2−1)(2−2)/2 = 1·0/2 = 0`. This is the Kobayashi–Maskawa content: CP
    violation is IMPOSSIBLE in a two-generation mixing matrix. -/
theorem cpPhases_two : cpPhases 2 = 0 := by decide

/-- `cpPhases 3 = 1` — exactly ONE physical CP-violating phase with three generations (the
    single CKM phase `δ`). `(3−1)(3−2)/2 = 2·1/2 = 1`. -/
theorem cpPhases_three : cpPhases 3 = 1 := by decide

/-- `mixingAngles 2 = 1` — the single Cabibbo angle `θ_C`. `2·1/2 = 1`. -/
theorem mixingAngles_two : mixingAngles 2 = 1 := by decide

/-- `mixingAngles 3 = 3` — the three CKM mixing angles `θ₁₂, θ₁₃, θ₂₃`. `3·2/2 = 3`. -/
theorem mixingAngles_three : mixingAngles 3 = 3 := by decide

/-- `removablePhases 3 = 5` — the five rephasable phases for three generations (`2·3 − 1`). -/
theorem removablePhases_three : removablePhases 3 = 5 := by decide

/-! ## Part 3 — the load-bearing parameter identity -/

/-- LOAD-BEARING GENERAL THEOREM: for EVERY `N`, the `N²` real parameters of a unitary `N×N`
    mixing matrix split EXACTLY into the real mixing angles, the removable phases, and the
    physical CP-violating phases:

    `N² = mixingAngles N + removablePhases N + cpPhases N`.

    Proved division-free to dodge ℕ truncated subtraction/division: case-split `N` (the
    `N = 0` and `N = 1` boundary, then the successor `N+2`), exposing the subtractions so the
    divisions become exact, and close with `omega`/`ring`. -/
theorem param_count_identity (N : ℕ) :
    N ^ 2 = mixingAngles N + removablePhases N + cpPhases N := by
  unfold mixingAngles removablePhases cpPhases
  -- Expose the truncated subtractions: handle N = 0, N = 1, then N = k + 2.
  match N with
  | 0 => decide
  | 1 => decide
  | (k + 2) =>
    -- Now N - 1 = k + 1, N - 2 = k, and the divisions are exact.
    have h1 : (k + 2) - 1 = k + 1 := by omega
    have h2 : (k + 2) - 2 = k := by omega
    rw [h1, h2]
    -- Both products are even (consecutive-integer products), so the /2 is exact.
    -- Pin the doubled value of each halved product, then close with omega: the only
    -- nonlinear terms ((k+2)^2, the two products) are supplied as facts, leaving omega
    -- a purely linear problem (incl. the truncated `2*(k+2) - 1`).
    have evA : Even ((k + 2) * (k + 1)) := by
      have h : (k + 2) * (k + 1) = (k + 1) * (k + 2) := by ring
      rw [h]; exact Nat.even_mul_succ_self (k + 1)
    have evB : Even ((k + 1) * k) := by
      have h : (k + 1) * k = k * (k + 1) := by ring
      rw [h]; exact Nat.even_mul_succ_self k
    have hAval : 2 * ((k + 2) * (k + 1) / 2) = (k + 2) * (k + 1) :=
      Nat.two_mul_div_two_of_even evA
    have hBval : 2 * ((k + 1) * k / 2) = (k + 1) * k :=
      Nat.two_mul_div_two_of_even evB
    -- The two halved products sum to (k+1)² (both doubled then added: 2(A+B)=2(k+1)²).
    have hsum : 2 * ((k + 2) * (k + 1) / 2) + 2 * ((k + 1) * k / 2) = 2 * (k + 1) ^ 2 := by
      rw [hAval, hBval]; ring
    -- The square splits as (k+1)² plus the (truncated) removable term 2(k+2) − 1 = 2k+3.
    have hsplit : (k + 2) ^ 2 = (k + 1) ^ 2 + (2 * (k + 2) - 1) := by
      have : 2 * (k + 2) - 1 = 2 * k + 3 := by omega
      rw [this]; ring
    omega

/-! ## Part 4 — the CP threshold (the physical headline) -/

/-- PHYSICAL HEADLINE: CP violation in the mixing sector REQUIRES at least three generations —
    `cpPhases N > 0 → 3 ≤ N`. A surviving physical phase exists only for `N ≥ 3`. -/
theorem cp_requires_three_generations (N : ℕ) : cpPhases N > 0 → 3 ≤ N := by
  intro h
  by_contra hlt
  push_neg at hlt
  interval_cases N <;> simp_all [cpPhases]

/-- The contrapositive form: with at most two generations there is NO physical CP phase —
    `N ≤ 2 → cpPhases N = 0`. -/
theorem cp_vanishes_below_three (N : ℕ) : N ≤ 2 → cpPhases N = 0 := by
  intro h
  interval_cases N <;> decide

/-! ## Part 5 — non-tautology guard and the compound statement -/

/-- NON-TAUTOLOGY GUARD: the CP-phase count genuinely DISTINGUISHES two from three generations —
    `cpPhases 2 ≠ cpPhases 3` (`0 ≠ 1`). The counts are NOT a vacuous constant; the N=2 (no CP)
    vs N=3 (one CP phase) distinction is real. Mirrors CF-L's `nontautology_su3_ne_su2`. -/
theorem nontautology_cp_two_ne_three : cpPhases 2 ≠ cpPhases 3 := by decide

/-- COMPOUND STATEMENT: the physical instances hold (`cpPhases 2 = 0`, `cpPhases 3 = 1`,
    `mixingAngles 3 = 3`), the parameter identity holds for all `N`, CP violation requires
    `N ≥ 3`, and the count genuinely separates N=2 from N=3. Packages "the Kobayashi–Maskawa
    counting ⟹ CP needs three generations, distinct from the two-generation case". -/
theorem flavor_count_compound :
    (cpPhases 2 = 0 ∧ cpPhases 3 = 1 ∧ mixingAngles 3 = 3) ∧
    (∀ N : ℕ, N ^ 2 = mixingAngles N + removablePhases N + cpPhases N) ∧
    (∀ N : ℕ, cpPhases N > 0 → 3 ≤ N) ∧
    (cpPhases 2 ≠ cpPhases 3) :=
  ⟨⟨cpPhases_two, cpPhases_three, mixingAngles_three⟩,
   param_count_identity,
   cp_requires_three_generations,
   nontautology_cp_two_ne_three⟩

end Phase11Flavor

-- Axiom audit: each theorem's footprint must be ⊆ {propext, Classical.choice, Quot.sound}.
#print axioms Phase11Flavor.cpPhases_two
#print axioms Phase11Flavor.cpPhases_three
#print axioms Phase11Flavor.mixingAngles_two
#print axioms Phase11Flavor.mixingAngles_three
#print axioms Phase11Flavor.removablePhases_three
#print axioms Phase11Flavor.param_count_identity
#print axioms Phase11Flavor.cp_requires_three_generations
#print axioms Phase11Flavor.cp_vanishes_below_three
#print axioms Phase11Flavor.nontautology_cp_two_ne_three
#print axioms Phase11Flavor.flavor_count_compound
