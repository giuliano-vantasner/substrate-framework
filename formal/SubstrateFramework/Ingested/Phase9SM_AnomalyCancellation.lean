import Mathlib

/-!
# Phase 9 SM-L — Standard Model gauge anomaly cancellation, one generation

This file is the Lean oracle's contribution for unified-framework Phase 9 (the Standard
Model consistency capstone), step SM-L. It machine-checks the DISCRETE-FACT OUTPUT that the
chiral gauge anomalies of ONE Standard Model generation cancel: over the left-handed Weyl
content `{Q_L, u_Rᶜ, d_Rᶜ, L, e_Rᶜ}` the four triangle-anomaly sums and the global Witten
parity all take their consistency values. The headline structural fact is that
`U(1)³`, `grav²·U(1)`, `[SU(2)]²·U(1)`, `[SU(3)]²·U(1)` all sum to ZERO and the number of
SU(2) doublets is EVEN — exactly the conditions for a consistent (anomaly-free) chiral gauge
theory.

This is the fifth entry in the framework's gauge Lean ledger, alongside
EM4  (`Phase3EM_U1Current.lean`)        — charge conservation ⟺ phase symmetry;
W6   (`Phase6Weak_MaxParityViolation.lean`) — maximal parity violation ⟺ left-only coupling;
P7L  (`Phase7EW_MasslessPhoton.lean`)   — massless photon ⟺ unbroken generator;
QCD4 (`Phase8QCD_SU3GaugeFacts.lean`)   — the eight gluons and the SU(3) Casimir/Dynkin facts;
SM-L (this file)                        — the per-generation anomaly cancellation.

## Physics offered for (the INPUT, not proved here)

- **The Standard Model gauge group is `SU(3)_c × SU(2)_L × U(1)_Y`** and one generation of
  matter, written entirely as LEFT-handed Weyl fermions (right-handed fields conjugated),
  fills exactly these five irreducible representations, with the standard hypercharges
  (normalisation `Q = T₃ + Y`):

  | field   | colour `SU(3)` | iso `SU(2)` | hypercharge `Y` |
  |---------|:-:|:-:|:---:|
  | `Q_L`   | `3` | `2` | `+1/6` |
  | `u_Rᶜ`  | `3̄` | `1` | `−2/3` |
  | `d_Rᶜ`  | `3̄` | `1` | `+1/3` |
  | `L`     | `1` | `2` | `−1/2` |
  | `e_Rᶜ`  | `1` | `1` | `+1`   |

  That these ARE the gauge group and the matter content, and that **gauge anomaly freedom is
  the quantum-consistency condition** a chiral gauge theory must satisfy (triangle diagrams
  must cancel, and the global SU(2) "Witten" anomaly requires an even number of doublets),
  are the asserted physical INPUTS. Lean checks only the resulting rational arithmetic.

- **The anomaly functionals.** Summing over the multiplet (a field in colour rep of
  dimension `colorMult` and iso rep of dimension `isoMult` contributes `colorMult·isoMult`
  Weyl components), the gauge-anomaly coefficients are the standard traces:
  * `U(1)³`        : `Σ (colorMult·isoMult)·Y³`
  * `grav²·U(1)`   : `Σ (colorMult·isoMult)·Y`   (the mixed gravitational anomaly)
  * `[SU(2)]²·U(1)`: `Σ_{doublets} T(2)·colorMult·Y`,  Dynkin `T(2) = 1/2`
  * `[SU(3)]²·U(1)`: `Σ_{triplets} T(3)·isoMult·Y`,    Dynkin `T(3) = 1/2`
  The `[SU(3)]³` and `[SU(2)]³` pure-nonabelian anomalies vanish automatically for these
  reps (SU(2) is anomaly-free; the SU(3) cubic cancels because the generation is colour-vector
  `3 + 3̄`), and are not re-derived here. These trace formulas are the asserted INPUTS.

To keep every fact a closed computation, the content is a `List` of records carrying
`(colorMult : ℕ, isoMult : ℕ, Y : ℚ)`; the anomaly functionals are `List.sum`/`List.map`
over `ℚ`, and each theorem is a closed evaluation (`by decide` on ℕ / `by norm_num`,
`by native_decide`-free) — a general functional applied to the SM INSTANCE, not a bare
decimal `rfl`.

## What each theorem PROVES (the OUTPUT, machine-checked here)

* `anomaly_U1_cubed`   — `Σ (colorMult·isoMult)·Y³ = 0` over the generation.
* `anomaly_grav_U1`    — `Σ (colorMult·isoMult)·Y = 0` (mixed gravitational anomaly).
* `anomaly_SU2_sq_U1`  — `Σ_{doublets} (1/2)·colorMult·Y = 0`.
* `anomaly_SU3_sq_U1`  — `Σ_{triplets} (1/2)·isoMult·Y = 0`.
* `witten_even`        — `Even (Σ_{doublets} colorMult)` (`= Even 4`): the global SU(2)
  anomaly vanishes because the number of colour-counted SU(2) doublets is even.
* `all_anomalies_cancel` — the conjunction of all five: the headline "the generation is
  anomaly-free".
* `nontautology_guard` — dropping the quark doublet `Q_L` leaves
  `Σ (colorMult·isoMult)·Y = −1 ≠ 0`: cancellation is a REAL property of the FULL content,
  not an automatic identity. Mirrors P7L/QCD4's `nontautology_guard`.
* `guard_compound` — packages the cancellation with the truncated-nonzero guard, the
  encoding "the full generation cancels, but a truncated content does not".

Honesty: a fully-proved theorem proves exactly its own statement. These check the rational
arithmetic OUTPUT of the standard anomaly traces evaluated on the chosen hypercharges. They
do NOT prove that `SU(3)×SU(2)×U(1)` is the gauge group, that these are the matter reps, that
the hypercharges take these values, or that gauge anomalies must physically cancel for
consistency — those are the asserted physical premises (declared INPUT), exactly as QCD4
asserts the SU(N) representation theory and P7L asserts the Higgs-doublet structure. This is
NOT a decimal `rfl` attestation: it is a genuine discrete-fact derivation (a general anomaly
functional over a fermion list, applied to the SM instance, with a non-tautology guard).
-/

namespace Phase9SM

/-- A left-handed Weyl fermion multiplet: its `SU(3)_c` representation dimension
    (`colorMult`), its `SU(2)_L` representation dimension (`isoMult`), and its `U(1)_Y`
    hypercharge `Y` (rational, in the `Q = T₃ + Y` normalisation). -/
structure Weyl where
  colorMult : ℕ
  isoMult : ℕ
  Y : ℚ
deriving DecidableEq

/-- Total number of Weyl components in a multiplet: `colorMult · isoMult`. -/
def Weyl.mult (w : Weyl) : ℕ := w.colorMult * w.isoMult

/-- The five left-handed Weyl multiplets of ONE Standard Model generation
    (right-handed fields conjugated), with standard hypercharges. -/
def generation : List Weyl :=
  [ ⟨3, 2, 1/6⟩    -- Q_L   : colour triplet, iso doublet,  Y = +1/6
  , ⟨3, 1, -2/3⟩   -- u_Rᶜ  : colour anti-triplet, singlet, Y = −2/3
  , ⟨3, 1, 1/3⟩    -- d_Rᶜ  : colour anti-triplet, singlet, Y = +1/3
  , ⟨1, 2, -1/2⟩   -- L     : colour singlet, iso doublet,  Y = −1/2
  , ⟨1, 1, 1⟩ ]    -- e_Rᶜ  : colour singlet, singlet,      Y = +1

/-- Fundamental Dynkin index `T(F) = 1/2`, shared by the `SU(2)` doublet and the `SU(3)`
    triplet (same normalisation as QCD4's `dynkinF`). -/
def dynkin : ℚ := 1 / 2

/-! ### General anomaly functionals over a list of Weyl fermions (INPUT trace formulas) -/

/-- The `U(1)³` triangle anomaly coefficient: `Σ (colorMult·isoMult)·Y³`. -/
def anomU1cubed (fs : List Weyl) : ℚ :=
  (fs.map (fun w => (w.mult : ℚ) * w.Y ^ 3)).sum

/-- The mixed gravitational `grav²·U(1)` anomaly coefficient: `Σ (colorMult·isoMult)·Y`. -/
def anomGravU1 (fs : List Weyl) : ℚ :=
  (fs.map (fun w => (w.mult : ℚ) * w.Y)).sum

/-- The `[SU(2)]²·U(1)` anomaly coefficient: `Σ_{doublets} T(2)·colorMult·Y`, summing only
    over `SU(2)` doublets (`isoMult = 2`), with Dynkin weight `T(2) = 1/2`. -/
def anomSU2sqU1 (fs : List Weyl) : ℚ :=
  (fs.map (fun w => if w.isoMult = 2 then dynkin * (w.colorMult : ℚ) * w.Y else 0)).sum

/-- The `[SU(3)]²·U(1)` anomaly coefficient: `Σ_{triplets} T(3)·isoMult·Y`, summing only
    over `SU(3)` triplets (`colorMult = 3`), with Dynkin weight `T(3) = 1/2`. -/
def anomSU3sqU1 (fs : List Weyl) : ℚ :=
  (fs.map (fun w => if w.colorMult = 3 then dynkin * (w.isoMult : ℚ) * w.Y else 0)).sum

/-- Colour-counted number of `SU(2)` doublets: `Σ_{doublets} colorMult`. The global
    (Witten) `SU(2)` anomaly cancels iff this is EVEN. -/
def doubletCount (fs : List Weyl) : ℕ :=
  (fs.map (fun w => if w.isoMult = 2 then w.colorMult else 0)).sum

/-! ### The Standard Model instance — each anomaly sum vanishes (the OUTPUT) -/

/-- `U(1)³` anomaly cancels: `Σ (colorMult·isoMult)·Y³ = 0`.
    `6·(1/6)³ + 3·(−2/3)³ + 3·(1/3)³ + 2·(−1/2)³ + 1·1³ = 0`. -/
theorem anomaly_U1_cubed : anomU1cubed generation = 0 := by
  unfold anomU1cubed generation Weyl.mult
  norm_num

/-- Mixed gravitational `grav²·U(1)` anomaly cancels: `Σ (colorMult·isoMult)·Y = 0`.
    `6·(1/6) + 3·(−2/3) + 3·(1/3) + 2·(−1/2) + 1·1 = 1 − 2 + 1 − 1 + 1 = 0`. -/
theorem anomaly_grav_U1 : anomGravU1 generation = 0 := by
  unfold anomGravU1 generation Weyl.mult
  norm_num

/-- `[SU(2)]²·U(1)` anomaly cancels: summing the Dynkin-weighted hypercharge over the two
    `SU(2)` doublets (`Q_L` colour-3, `L` colour-1) gives
    `(1/2)·3·(1/6) + (1/2)·1·(−1/2) = 1/4 − 1/4 = 0`. -/
theorem anomaly_SU2_sq_U1 : anomSU2sqU1 generation = 0 := by
  unfold anomSU2sqU1 generation dynkin
  norm_num

/-- `[SU(3)]²·U(1)` anomaly cancels: summing the Dynkin-weighted hypercharge over the three
    `SU(3)` triplets (`Q_L` iso-2, `u_Rᶜ` iso-1, `d_Rᶜ` iso-1) gives
    `(1/2)·2·(1/6) + (1/2)·1·(−2/3) + (1/2)·1·(1/3) = 1/6 − 1/3 + 1/6 = 0`. -/
theorem anomaly_SU3_sq_U1 : anomSU3sqU1 generation = 0 := by
  unfold anomSU3sqU1 generation dynkin
  norm_num

/-- The colour-counted doublet number is `Even`: `3 (from Q_L) + 1 (from L) = 4`, so the
    global (Witten) `SU(2)` anomaly cancels. -/
theorem witten_even : Even (doubletCount generation) := by
  decide

/-- Explicit value of the colour-counted doublet number: `4`. -/
theorem doublet_count_four : doubletCount generation = 4 := by
  decide

/-- HEADLINE: ONE Standard Model generation is ANOMALY-FREE — all four triangle anomalies
    vanish and the global `SU(2)` parity is even. The conjunction of the consistency
    conditions a chiral gauge theory must satisfy, here verified for the SM hypercharges. -/
theorem all_anomalies_cancel :
    anomU1cubed generation = 0 ∧
    anomGravU1 generation = 0 ∧
    anomSU2sqU1 generation = 0 ∧
    anomSU3sqU1 generation = 0 ∧
    Even (doubletCount generation) :=
  ⟨anomaly_U1_cubed, anomaly_grav_U1, anomaly_SU2_sq_U1, anomaly_SU3_sq_U1, witten_even⟩

/-! ### Non-tautology guard — the cancellation is a property of the FULL content -/

/-- The generation with the quark doublet `Q_L` REMOVED (`u_Rᶜ, d_Rᶜ, L, e_Rᶜ`). -/
def generationDropQL : List Weyl :=
  [ ⟨3, 1, -2/3⟩, ⟨3, 1, 1/3⟩, ⟨1, 2, -1/2⟩, ⟨1, 1, 1⟩ ]

/-- NON-TAUTOLOGY GUARD: dropping `Q_L` BREAKS cancellation — the truncated gravitational
    anomaly is `3·(−2/3) + 3·(1/3) + 2·(−1/2) + 1·1 = −2 + 1 − 1 + 1 = −1 ≠ 0`. So the
    full-generation cancellation is a genuine arithmetic property of the COMPLETE matter
    content, not an identity that holds for any list. Mirrors QCD4's `nontautology_guard`. -/
theorem nontautology_guard : anomGravU1 generationDropQL = -1 ∧ anomGravU1 generationDropQL ≠ 0 := by
  unfold anomGravU1 generationDropQL Weyl.mult
  norm_num

/-- COMPOUND GUARD: the full generation cancels ALL anomalies, but the SAME functional on the
    `Q_L`-truncated content is `−1 ≠ 0`. This is the encoding "anomaly-free ⟺ the full
    matter content": the cancellation is real representation/hypercharge arithmetic, not a
    definitional tautology. -/
theorem guard_compound :
    (anomU1cubed generation = 0 ∧ anomGravU1 generation = 0 ∧
       anomSU2sqU1 generation = 0 ∧ anomSU3sqU1 generation = 0 ∧
       Even (doubletCount generation)) ∧
    (anomGravU1 generationDropQL = -1 ∧ anomGravU1 generationDropQL ≠ 0) :=
  ⟨all_anomalies_cancel, nontautology_guard⟩

end Phase9SM

-- Axiom audit: each theorem's footprint must be ⊆ {propext, Classical.choice, Quot.sound}.
#print axioms Phase9SM.anomaly_U1_cubed
#print axioms Phase9SM.anomaly_grav_U1
#print axioms Phase9SM.anomaly_SU2_sq_U1
#print axioms Phase9SM.anomaly_SU3_sq_U1
#print axioms Phase9SM.witten_even
#print axioms Phase9SM.doublet_count_four
#print axioms Phase9SM.all_anomalies_cancel
#print axioms Phase9SM.nontautology_guard
#print axioms Phase9SM.guard_compound
