import Mathlib

/-!
# Phase 23 EW — the weak mixing angle as a trace ratio, one generation (WM-L)

This file is the Lean oracle's contribution for unified-framework Phase 23 (the
electroweak-normalisation capstone), step WM-L. It machine-checks the DISCRETE-FACT
OUTPUT that, over ONE Standard Model generation (the anomaly-forced charges — exactly the
SM-L content), the canonical weak-mixing-angle trace ratio takes its GUT-normalised value

  sin²θ_W = Tr(T₃²) / Tr(Q²) = 3/8 (exactly, as a rational).

with the supporting traces `Tr(T₃²) = 2`, `Tr(Y²) = 10/3`, `Tr(T₃Y) = 0`, `Tr(Q²) = 16/3`,
and the clean split `Tr(Q²) = Tr(T₃²) + Tr(Y²)` (which holds precisely because the cross term
`Tr(T₃Y)` vanishes over the generation).

This is the companion to `Phase9SM_AnomalyCancellation.lean` (SM-L): SM-L certifies that the
SAME per-generation charge content is anomaly-free; WM-L reads the weak-mixing normalisation
off that very content. Same matter list, same hypercharges, same `Q = T₃ + Y` normalisation.

## Physics offered for (the INPUT, not proved here)

- **The Standard Model gauge group is `SU(3)_c × SU(2)_L × U(1)_Y`** and one generation of
  matter, written entirely as LEFT-handed Weyl fermions (right-handed fields conjugated),
  fills exactly these states, with the standard `(T₃, Y)` charges (normalisation
  `Q = T₃ + Y`); colour is folded into a multiplicity `colorMult`:

  | state   | colour mult `colorMult` | `T₃`   | hypercharge `Y` | `Q = T₃ + Y` |
  |---------|:-:|:----:|:----:|:----:|
  | `u_L`   | `3` | `+1/2` | `+1/6` | `+2/3` |
  | `d_L`   | `3` | `−1/2` | `+1/6` | `−1/3` |
  | `u_Rᶜ`  | `3` |  `0`   | `−2/3` | `−2/3` |
  | `d_Rᶜ`  | `3` |  `0`   | `+1/3` | `+1/3` |
  | `ν_L`   | `1` | `+1/2` | `−1/2` |  `0`   |
  | `e_L`   | `1` | `−1/2` | `−1/2` | `−1`   |
  | `e_Rᶜ`  | `1` |  `0`   | `+1`   | `+1`   |

  That these ARE the gauge group and the matter content, that the hypercharges and isospins
  take these values, and that **the weak-mixing angle at the unification normalisation is the
  trace ratio `sin²θ_W = Tr(T₃²)/Tr(Q²)`** (equivalently the `SU(2)`/electromagnetic current
  normalisation `g'²/(g² + g'²)` with the GUT-canonical `U(1)` embedding), are the asserted
  physical INPUTS. Lean checks only the resulting rational arithmetic.

- **The trace functionals.** Summing over the generation (a state of colour multiplicity
  `colorMult` contributes `colorMult` Weyl components), the relevant traces are
  * `Tr(T₃²)` : `Σ colorMult·T₃²`
  * `Tr(Y²)`  : `Σ colorMult·Y²`
  * `Tr(T₃Y)` : `Σ colorMult·T₃·Y`
  * `Tr(Q²)`  : `Σ colorMult·(T₃ + Y)²`
  These trace formulas, and the identification of `sin²θ_W` with `Tr(T₃²)/Tr(Q²)`, are the
  asserted INPUTS.

To keep every fact a closed computation, the content is a `List` of records carrying
`(colorMult : ℕ, T3 : ℚ, Y : ℚ)`; the trace functionals are `List.sum`/`List.map` over `ℚ`,
and each theorem is a closed evaluation (`by norm_num`) — a general functional applied to the
SM INSTANCE, not a bare decimal `rfl`.

## What each theorem PROVES (the OUTPUT, machine-checked here)

* `tr_T3sq_eq`     — `Tr(T₃²) = Σ colorMult·T₃² = 2` over the generation.
* `tr_Ysq_eq`      — `Tr(Y²)  = Σ colorMult·Y²  = 10/3`.
* `tr_T3Y_eq`      — `Tr(T₃Y) = Σ colorMult·T₃·Y = 0` (the cross term vanishes).
* `tr_Qsq_eq`      — `Tr(Q²)  = Σ colorMult·(T₃+Y)² = 16/3`.
* `qsq_splits`     — `Tr(Q²) = Tr(T₃²) + Tr(Y²)` (clean split, since `Tr(T₃Y) = 0`).
* `sin2thetaW_eq`  — HEADLINE: `Tr(T₃²)/Tr(Q²) = 3/8`.
* `nontautology_guard` — a TRUNCATED/WRONG content (quarks as colour singlets,
  `colorMult = 1`) gives a DIFFERENT value `9/28 ≠ 3/8`: the colour multiplicity / full
  content is load-bearing, not a definitional identity. Proves both the wrong VALUE and `≠ 3/8`.
* `headline_compound` — packages the `3/8` headline with the truncated-wrong guard.

Honesty: a fully-proved theorem proves exactly its own statement. These check the rational
arithmetic OUTPUT of the standard weak-mixing trace formula evaluated on the chosen
`(T₃, Y)` charges. They do NOT prove that `SU(3)×SU(2)×U(1)` is the gauge group, that these
are the matter reps, that the charges take these values, or that `sin²θ_W` IS the trace ratio
`Tr(T₃²)/Tr(Q²)` — those are the asserted physical premises (declared INPUT), exactly as SM-L
asserts the matter content and the anomaly functionals. This is NOT a decimal `rfl`
attestation: it is a genuine discrete-fact derivation (general trace functionals over a
fermion list, applied to the SM instance, with a non-tautology guard).
-/

namespace Phase23EW

/-- A left-handed Weyl state of one generation: its colour multiplicity (`colorMult`), its
    weak isospin `T₃`, and its `U(1)_Y` hypercharge `Y` (rationals, in `Q = T₃ + Y`). -/
structure Weyl where
  colorMult : ℕ
  T3 : ℚ
  Y : ℚ
deriving DecidableEq

/-- Electric charge `Q = T₃ + Y`. -/
def Weyl.Q (w : Weyl) : ℚ := w.T3 + w.Y

/-- The seven left-handed Weyl states of ONE Standard Model generation (right-handed fields
    conjugated), colour folded into `colorMult`, with standard `(T₃, Y)`. -/
def generation : List Weyl :=
  [ ⟨3, 1/2, 1/6⟩    -- u_L
  , ⟨3, -1/2, 1/6⟩   -- d_L
  , ⟨3, 0, -2/3⟩     -- u_Rᶜ
  , ⟨3, 0, 1/3⟩      -- d_Rᶜ
  , ⟨1, 1/2, -1/2⟩   -- ν_L
  , ⟨1, -1/2, -1/2⟩  -- e_L
  , ⟨1, 0, 1⟩ ]      -- e_Rᶜ

/-! ### General trace functionals over a list of Weyl states (INPUT trace formulas) -/

/-- `Tr(T₃²) = Σ colorMult·T₃²`. -/
def trT3sq (fs : List Weyl) : ℚ :=
  (fs.map (fun w => (w.colorMult : ℚ) * w.T3 ^ 2)).sum

/-- `Tr(Y²) = Σ colorMult·Y²`. -/
def trYsq (fs : List Weyl) : ℚ :=
  (fs.map (fun w => (w.colorMult : ℚ) * w.Y ^ 2)).sum

/-- `Tr(T₃Y) = Σ colorMult·T₃·Y`. -/
def trT3Y (fs : List Weyl) : ℚ :=
  (fs.map (fun w => (w.colorMult : ℚ) * w.T3 * w.Y)).sum

/-- `Tr(Q²) = Σ colorMult·(T₃ + Y)²`. -/
def trQsq (fs : List Weyl) : ℚ :=
  (fs.map (fun w => (w.colorMult : ℚ) * w.Q ^ 2)).sum

/-! ### The Standard Model instance — the trace values (the OUTPUT) -/

/-- `Tr(T₃²) = 2`: `3·(1/2)² + 3·(1/2)² + 1·(1/2)² + 1·(1/2)²
    = 3/4 + 3/4 + 1/4 + 1/4 = 2`. -/
theorem tr_T3sq_eq : trT3sq generation = 2 := by
  unfold trT3sq generation
  norm_num

/-- `Tr(Y²) = 10/3`: `3·(1/6)² + 3·(1/6)² + 3·(−2/3)² + 3·(1/3)²
    + 1·(−1/2)² + 1·(−1/2)² + 1·1² = 1/12 + 1/12 + 4/3 + 1/3 + 1/4 + 1/4 + 1 = 10/3`. -/
theorem tr_Ysq_eq : trYsq generation = 10 / 3 := by
  unfold trYsq generation
  norm_num

/-- `Tr(T₃Y) = 0`: the cross term vanishes —
    `3·(1/2·1/6) + 3·(−1/2·1/6) + 0 + 0 + 1·(1/2·−1/2) + 1·(−1/2·−1/2) + 0
    = 1/4 − 1/4 − 1/4 + 1/4 = 0`. -/
theorem tr_T3Y_eq : trT3Y generation = 0 := by
  unfold trT3Y generation
  norm_num

/-- `Tr(Q²) = 16/3`: with charges `(2/3, −1/3, −2/3, 1/3, 0, −1, 1)` and colour weights,
    `3·(4/9) + 3·(1/9) + 3·(4/9) + 3·(1/9) + 0 + 1·1 + 1·1 = 4/3 + 1/3 + 4/3 + 1/3 + 2
    = 16/3`. -/
theorem tr_Qsq_eq : trQsq generation = 16 / 3 := by
  unfold trQsq generation Weyl.Q
  norm_num

/-- `Tr(Q²) = Tr(T₃²) + Tr(Y²)`: the clean split, holding precisely because the cross term
    `Tr(T₃Y) = 0` over the generation (`16/3 = 2 + 10/3`). -/
theorem qsq_splits : trQsq generation = trT3sq generation + trYsq generation := by
  rw [tr_Qsq_eq, tr_T3sq_eq, tr_Ysq_eq]
  norm_num

/-- HEADLINE: the GUT-normalised weak mixing angle over one Standard Model generation is the
    trace ratio `sin²θ_W = Tr(T₃²)/Tr(Q²) = (2)/(16/3) = 3/8`. -/
theorem sin2thetaW_eq : trT3sq generation / trQsq generation = 3 / 8 := by
  rw [tr_T3sq_eq, tr_Qsq_eq]
  norm_num

/-! ### Non-tautology guard — the full colour-counted content is load-bearing -/

/-- The generation with QUARKS TREATED AS COLOUR SINGLETS (`colorMult = 1` for the four
    quark states) — a WRONG/truncated content used to confirm the ratio is not a definitional
    identity. -/
def generationDropColor : List Weyl :=
  [ ⟨1, 1/2, 1/6⟩    -- u_L  (colour stripped)
  , ⟨1, -1/2, 1/6⟩   -- d_L
  , ⟨1, 0, -2/3⟩     -- u_Rᶜ
  , ⟨1, 0, 1/3⟩      -- d_Rᶜ
  , ⟨1, 1/2, -1/2⟩   -- ν_L
  , ⟨1, -1/2, -1/2⟩  -- e_L
  , ⟨1, 0, 1⟩ ]      -- e_Rᶜ

/-- NON-TAUTOLOGY GUARD: with quarks mis-counted as colour singlets the traces become
    `Tr(T₃²) = 4·(1/2)² = 1` and `Tr(Q²) = 4/9 + 1/9 + 4/9 + 1/9 + 0 + 1 + 1 = 28/9`, so the
    ratio is `9/28 ≠ 3/8`. The full colour multiplicity / matter content is genuine arithmetic
    input, not a tautology that holds for any list. Proves both the WRONG value `9/28` and the
    inequality `≠ 3/8`. -/
theorem nontautology_guard :
    trT3sq generationDropColor / trQsq generationDropColor = 9 / 28 ∧
    trT3sq generationDropColor / trQsq generationDropColor ≠ 3 / 8 := by
  refine ⟨?_, ?_⟩
  · unfold trT3sq trQsq generationDropColor Weyl.Q
    norm_num
  · unfold trT3sq trQsq generationDropColor Weyl.Q
    norm_num

/-- COMPOUND HEADLINE: the full generation gives `sin²θ_W = Tr(T₃²)/Tr(Q²) = 3/8`, but the
    SAME ratio on the colour-stripped content is `9/28 ≠ 3/8`. This is the encoding
    "`sin²θ_W = 3/8` ⟺ the full colour-counted SM content": real representation/charge
    arithmetic, not a definitional tautology. -/
theorem headline_compound :
    (trT3sq generation / trQsq generation = 3 / 8) ∧
    (trT3sq generationDropColor / trQsq generationDropColor = 9 / 28 ∧
       trT3sq generationDropColor / trQsq generationDropColor ≠ 3 / 8) :=
  ⟨sin2thetaW_eq, nontautology_guard⟩

end Phase23EW

-- Axiom audit: each theorem's footprint must be ⊆ {propext, Classical.choice, Quot.sound}.
#print axioms Phase23EW.tr_T3sq_eq
#print axioms Phase23EW.tr_Ysq_eq
#print axioms Phase23EW.tr_T3Y_eq
#print axioms Phase23EW.tr_Qsq_eq
#print axioms Phase23EW.qsq_splits
#print axioms Phase23EW.sin2thetaW_eq
#print axioms Phase23EW.nontautology_guard
#print axioms Phase23EW.headline_compound
