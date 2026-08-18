import Mathlib
namespace Phase22AS


/-!
# Phase 22 AS-L — The SECOND rank reduction: β² pinned ⇒ the residual collapses to ln a

This file is the Lean oracle's contribution for unified-framework Phase 22, step AS-L
(claim C7). It is the SUCCESSOR to `Phase21AS_OverDetermination.lean`: that file certified
the FIRST rank-flip (OD-v1 under-determined → OD-v2 over-determined, the AS1–AS3 reductions);
this file certifies the SECOND rank reduction, OD-v2 → OD-v3, driven by AS6 pinning the lone
dimensionless coupling β².

The SymPy oracle (`merged-framework/bridges/phase-22/bridge_OD3_beta_pinned.py`) ran the
linear algebra over the verified ratio-chains with β² pinned and computed the new rank; this
file certifies the VERDICT LOGIC and the SECOND reduction from those ranks, exactly as
`Phase21AS_OverDetermination.lean` imports the OD-v1/OD-v2 ranks as inputs.

The physics story (verified in the SymPy bridges, asserted here as INPUT):

- **OD-v2 (Phase 21).** The verified scale chains, after AS1–AS3 eliminate three free
  dimensionful columns, reduce to the unknowns `{ln a, 1/β²}` (2 columns) over 4 independent
  constraints, with coefficient-matrix RANK 2. Nullity `2 − 2 = 0`: both `ln a` and `1/β²`
  pinned → OVER-determined (this is `Phase21AS`'s `odV2`).

- **AS6 (Phase 22).** The lone dimensionless coupling β² is PINNED by an internal structural
  condition: the sine-Gordon / 2D-Coulomb-gas electric-magnetic (Kosterlitz-Thouless) duality
  maps `β² ↔ 16π²/β²`, whose self-dual FIXED POINT solves `β⁴ = 16π²`, i.e. `β² = 4π` (the
  Coleman free-fermion point — EXACT algebra, verified in `bridge_AS6_beta_self_dual_pin.py`).
  With β² a known constant, `1/β²` is NO LONGER an unknown column — it moves to the RHS.

- **AS7 (Phase 22) — THE CORRECTION TO AS6, and why nothing below changes.** AS6's self-dual
  `β² = 4π` is FALSIFIED as the framework's operating point by the gravity sector, in the same
  phase: `bridge_AS7_gravity_confrontation_planck_granularity.py` shows that `β² = 4π` gives a
  hierarchy `ξ/a ~ 2.45`, hence a granularity `a ~ 0.6 fm`, which fed into AS3's Sakharov
  relation forces a field count `s_G = (a/ℓ_P)² ~ 10³⁹` — absurd, since `s_G` counts
  integrated-out modes and is `O(1..100)`. Requiring a sane `s_G` instead puts the granularity
  at `a = √(s_G)·ℓ_Planck`, and the resulting Planck→hadron hierarchy `ξ/a ~ 10²⁰`
  OVER-DETERMINES `β² = 8π²/(b₀ ln(ξ/a)) ≈ 0.245`, not `4π ≈ 12.57`.

  **This does not disturb any theorem in this file, and that is itself a result.** Every
  theorem below is rank/nullity arithmetic over `Determination` triples. The second reduction
  happens because `1/β²` becomes *a* known constant — the reduction never reads *which*
  constant. `bridge_OD3_beta_pinned.py` states the same thing directly: the drop and the
  over-determination "hold for ANY pinned beta^2", and "the physical pinned value is AS7's
  ~0.245". That independence is now made explicit rather than left implicit, as
  `reduction_independent_of_pinned_value` and `AS7_pin_gives_same_reduction` below, with
  `value_dependent_map_would_differ` as the non-triviality guard.

- **OD-v3 (Phase 22).** The system over the SINGLE unknown `{ln a}` (1 column), the SAME 4
  constraints, coefficient-matrix RANK 1. Nullity `1 − 1 = 0`: `ln a` pinned, with `4 > 1`
  constraints → STILL over-determined, now even more redundantly (all four chains pin the one
  `ln a`; three are redundant, falsifiable predictions once `a` is fixed by one observation).

- **The SECOND reduction.** Unknown count `2 → 1`: exactly ONE column (`1/β²`) eliminated by
  AS6's self-dual pin. Both OD-v2 and OD-v3 have nullity `0` (both over-determined). The
  residual dimensionful/coupling freedom collapses `5 (OD-v1) → 2 (OD-v2) → 1 (OD-v3)`; the
  lone survivor `ln a` is a UNITS CHOICE (Buckingham: a length needs one observation), NOT a
  physical number.

## Physics offered as INPUT (not proved here — the "physics map")

- **(The ranks.)** That OD-v2 has rank 2 (over 2 unknowns) and OD-v3 has rank 1 (over 1
  unknown), both over 4 constraints, are the SymPy oracle's matrix-rank outputs, ASSERTED here
  as field values — NOT recomputed as a matrix rank inside Lean (matching `Phase21AS`).
- **(That AS6 removes exactly the `1/β²` column.)** That self-duality pins `β² = 4π` and so
  collapses the column count `2 → 1` (one elimination: `1/β²` becomes a known constant) is the
  AS6 content, verified in `bridge_AS6_beta_self_dual_pin.py` and the OD-v3 bridge, asserted
  here. The π-algebra of the fixed point (`β⁴ = 16π²`) stays in SymPy; what is encoded below as
  decidable arithmetic is the integer cancellation `8/(7·4) = 2/7` of the transmutation
  exponent (`8π²/(b₀β²) = 2π/b₀` at `β² = 4π`), which is the clean integer witness of the
  collapse.

## The arithmetic this file PROVES (the OUTPUT, machine-checked here)

A `Determination` packages a linear system's `unknowns`, `constraints`, and `rank` as
naturals (reused from `Phase21AS_OverDetermination.lean`). The verdict logic is decidable
natural-number arithmetic:

- `nullity s = s.unknowns − s.rank` (free-direction count; `0` ⟺ all unknowns pinned).
- `isOverdetermined s` ⟺ `s.rank = s.unknowns ∧ s.constraints > s.unknowns`.

We import the two successor systems as the oracle's rank facts:
`odV2 = ⟨2, 4, 2⟩` (Phase-21 OD-v2) and `odV3 = ⟨1, 4, 1⟩` (Phase-22 OD-v3, β² pinned).

* `odV2_overdetermined` — OD-v2 IS over-determined (`rank 2 = 2` unknowns ∧ `4 > 2`).
* `odV3_overdetermined` — OD-v3 IS over-determined (`rank 1 = 1` unknown ∧ `4 > 1`).
* `the_second_reduction` — THE HEADLINE: `nullity odV2 = 0 ∧ nullity odV3 = 0` (both pinned)
  AND `odV2.unknowns − odV3.unknowns = 1` (exactly ONE column — `1/β²` — eliminated by AS6).
* `residual_collapse` — `5 > 2 > 1`: the residual freedom dropped OD-v1 → OD-v2 → OD-v3, the
  lone survivor `1` being `ln a` (the units choice).
* `self_dual_exponent_cancels` — the EXACT integer witness of the pin: at `β² = 4π`, `b₀ = 7`,
  the transmutation exponent `8π²/(b₀β²)` reduces to `2π/b₀` via `8/(7·4) = 2/7`, encoded as
  the decidable rational identity `(8 : ℚ)/(7*4) = 2/7` (the π-cancellation `π²/(4π) = π/4`
  stays in SymPy; this is its integer core).
* `refloat_not_reduced` — the NON-TAUTOLOGY GUARD: RE-FLOATING β² (adding `1/β²` back as an
  unknown) returns the `⟨2, 4, 2⟩` system — its unknown count is `2 ≠ 1`, so the reduction is
  NOT vacuous; AS6's pin genuinely removed a column (the bridge's G-refloat guard).
* `fab_not_over` — a second NON-TAUTOLOGY GUARD: a rank-deficient system `⟨2, 4, 1⟩` (rank
  `1 < 2` unknowns) is NOT over-determined despite `4 > 2` constraints — so over-determination
  is not automatic from surplus constraints; it requires `rank = unknowns`.

Honesty: a fully-proved theorem proves exactly its own statement. This checks the VERDICT
LOGIC and the SECOND reduction given the two ranks `2` and `1` from the SymPy oracle — that
with full column rank and surplus constraints each system over-determines, that the surviving
unknown count dropped by exactly 1 (the `1/β²` column AS6 pinned), that the residual freedom
collapses `5 → 2 → 1`, that the integer core of the self-dual exponent cancels (`8/(7·4) =
2/7`), and that the predicate genuinely discriminates (the re-floated and rank-deficient
systems fail). It does NOT recompute the matrix ranks, derive the β² = 4π fixed point's
π-algebra, or claim `a` is given a number — over-determination is a ONE-LENGTH family that
still needs one observation to fix the absolute `a` (Buckingham). Those are the asserted
physics premises (verified in the SymPy bridges AS5/AS6/OD-v3), beyond what is recomputed in
Lean.
Quality bar / style exemplar: `merged-framework/bridges/phase-21/lean/Phase21AS_OverDetermination.lean`.
-/

/-- A linear determination system reduced to its three integer invariants: the number of
`unknowns` (columns), the number of independent `constraints` (rows), and the coefficient-
matrix `rank`. The rank is the SymPy oracle's output, imported here as a field value.
(Same structure as `Phase21AS_OverDetermination.lean`.) -/
structure Determination where
  unknowns : ℕ
  constraints : ℕ
  rank : ℕ

/-- The nullity (free-direction count): `unknowns − rank` (natural subtraction; for a
well-posed system `rank ≤ unknowns`). Nullity `0` ⟺ every unknown is pinned. -/
def nullity (s : Determination) : ℕ := s.unknowns - s.rank

/-- A system is OVER-determined iff it has FULL column rank (`rank = unknowns`, nullity `0`)
AND strictly MORE constraints than unknowns (`constraints > unknowns`, the surplus = redundant
constraints that become falsifiable predictions). Both conjuncts required. -/
def isOverdetermined (s : Determination) : Prop :=
  s.rank = s.unknowns ∧ s.constraints > s.unknowns

/-- Phase-21 OD-v2: after AS1–AS3, the system over `{ln a, 1/β²}` (2 unknowns), 4 constraints,
coefficient-matrix rank 2 (SymPy oracle). The starting point of the second reduction. -/
def odV2 : Determination := ⟨2, 4, 2⟩

/-- Phase-22 OD-v3: AS6 pins `β² = 4π` by self-duality, so `1/β²` is a known constant — the
system collapses to the SINGLE unknown `{ln a}` (1 unknown), the SAME 4 constraints,
coefficient-matrix rank 1 (SymPy oracle). -/
def odV3 : Determination := ⟨1, 4, 1⟩

/-- OD-v2 IS over-determined: full column rank (`rank 2 = 2` unknowns, nullity `0`) AND surplus
constraints (`4 > 2`). Both `ln a` and `1/β²` pinned. (Re-certified here as the predecessor.) -/
theorem odV2_overdetermined : isOverdetermined odV2 := by
  unfold isOverdetermined odV2
  decide

/-- OD-v3 IS over-determined: full column rank (`rank 1 = 1` unknown, nullity `0`) AND surplus
constraints (`4 > 1`). The lone `ln a` is pinned; with β² fixed, all four chains pin it. -/
theorem odV3_overdetermined : isOverdetermined odV3 := by
  unfold isOverdetermined odV3
  decide

/-- THE HEADLINE — the SECOND rank reduction: BOTH OD-v2 and OD-v3 have nullity `0` (both
over-determined, everything pinned), AND the unknown count dropped from `2` to `1` — exactly
ONE column (`1/β²`) eliminated by AS6's self-dual pin of `β² = 4π`. -/
theorem the_second_reduction :
    nullity odV2 = 0 ∧ nullity odV3 = 0 ∧ odV2.unknowns - odV3.unknowns = 1 := by
  unfold nullity odV2 odV3
  decide

/-- The residual-freedom collapse `5 → 2 → 1`: OD-v1 had 5 free dimensionful constants, OD-v2
reduced to 2 (one length + one coupling), OD-v3 to 1 (just `ln a`). The lone survivor `1` is
`ln a`, the units choice (Buckingham). Stated as the strict chain `5 > 2 > 1`. -/
theorem residual_collapse :
    (5 : ℕ) > odV2.unknowns ∧ odV2.unknowns > odV3.unknowns ∧ odV3.unknowns = 1 := by
  unfold odV2 odV3
  decide

/-- The EXACT integer witness of the SELF-DUAL CASE specifically: at `β² = 4π` and `b₀ = 7`,
the AS1 transmutation exponent `8π²/(b₀β²)` reduces to `2π/b₀` because the integer factors
cancel — `8/(7·4) = 2/7`. The π-algebra (`π²/(4π) = π/4`) stays in SymPy; this is its
decidable rational core.

**Scope — read this before citing the theorem.** This is arithmetic about the self-dual value
`4π`, and it remains true as such. It is NOT a statement about the framework's operating
point: AS7 falsifies `β² = 4π` there (see the header), and the physical pinned value is
`≈ 0.245`, for which the analogous exponent has no clean rational core — no counterpart of
this witness is claimed for it, and none is manufactured here. The reduction proved in this
file does not depend on this witness or on the value it concerns; see
`reduction_independent_of_pinned_value`. -/
theorem self_dual_exponent_cancels : (8 : ℚ) / (7 * 4) = 2 / 7 := by
  norm_num

/-- Pinning a coupling: the reduction map that AS6 (or AS7, or any other pin) performs on the
system — one unknown column becomes a known constant and moves to the RHS, so both the unknown
count and the rank drop by one. The pinned VALUE is taken as an argument and deliberately never
used, which is precisely the content being certified: the instrument reads only *that* the
coupling is pinned, never *which* value it is pinned to. -/
def pinBeta (s : Determination) (_value : ℚ) : Determination :=
  ⟨s.unknowns - 1, s.constraints, s.rank - 1⟩

/-- Pinning OD-v2 at any value reproduces OD-v3 exactly. -/
theorem pin_odV2_is_odV3 (b : ℚ) : pinBeta odV2 b = odV3 := by
  unfold pinBeta odV2 odV3
  rfl

/-- THE β²-AGNOSTICISM OF THE SECOND REDUCTION: for ANY two pinned values — in particular
AS6's falsified `4π` and AS7's physical `≈0.245` — the reduced system is the SAME object, and
it is over-determined. So AS7's correction to AS6 leaves the second reduction, and every rank
verdict in this file, completely intact. This is the formal counterpart of
`bridge_OD3_beta_pinned.py`'s "the drop and the over-determination hold for ANY pinned
beta^2". -/
theorem reduction_independent_of_pinned_value (b₁ b₂ : ℚ) :
    pinBeta odV2 b₁ = pinBeta odV2 b₂ ∧ isOverdetermined (pinBeta odV2 b₁) := by
  constructor
  · rfl
  · unfold isOverdetermined pinBeta odV2
    decide

/-- AS7's physical pin, stated concretely: taking `β² ≈ 0.245` (as the rational `245/1000`)
gives exactly the same OD-v3 reduction that AS6's `4π` gave. The framework's corrected
operating point costs it nothing structurally. -/
theorem AS7_pin_gives_same_reduction :
    pinBeta odV2 (245 / 1000) = odV3 ∧ pinBeta odV2 (245 / 1000) = pinBeta odV2 4 := by
  constructor
  · unfold pinBeta odV2 odV3; rfl
  · rfl

/-- NON-TAUTOLOGY GUARD for the agnosticism claim: value-independence is NOT automatic for an
arbitrary map. A fabricated map that genuinely READS the pinned value — here, one whose rank
field is the value's numerator — returns DIFFERENT systems for AS6's and AS7's values. So
`reduction_independent_of_pinned_value` says something real about `pinBeta`'s construction,
rather than being a triviality that any map would satisfy. -/
def valueDependentMap (s : Determination) (value : ℚ) : Determination :=
  ⟨s.unknowns - 1, s.constraints, value.num.toNat⟩

theorem value_dependent_map_would_differ :
    valueDependentMap odV2 4 ≠ valueDependentMap odV2 (245 / 1000) := by
  intro h
  have hrank : ((4 : ℚ).num).toNat = (((245 : ℚ) / 1000).num).toNat :=
    congrArg Determination.rank h
  norm_num at hrank
  exact absurd hrank (by decide)

/-- A re-floated system: `1/β²` added back as an unknown returns OD-v2's `⟨2, 4, 2⟩`. -/
def refloat : Determination := odV2

/-- NON-TAUTOLOGY GUARD: RE-FLOATING β² (adding `1/β²` back as an unknown) returns the
`⟨2, 4, 2⟩` system, whose unknown count `2 ≠ 1` differs from OD-v3 — so the reduction is NOT
vacuous: AS6's pin genuinely removed a column. (The bridge's G-refloat guard: the rank changes
1 → 2 when β² is re-floated, proving the pin is load-bearing.) -/
theorem refloat_not_reduced : refloat.unknowns ≠ odV3.unknowns := by
  unfold refloat odV2 odV3
  decide

/-- A fabricated rank-deficient system: 2 unknowns, 4 constraints, rank 1. Surplus constraints
(`4 > 2`) but RANK-DEFICIENT (`rank 1 < 2`), so a null direction survives. -/
def fab : Determination := ⟨2, 4, 1⟩

/-- NON-TAUTOLOGY GUARD: the fabricated `fab = ⟨2, 4, 1⟩` is NOT over-determined DESPITE
`4 > 2` constraints — because its rank `1 ≠ 2` is not full (nullity `1`, a free direction).
So over-determination is NOT automatic from surplus constraints; it strictly requires
`rank = unknowns`. The predicate genuinely discriminates, so OD-v3's verdict is a real finding,
not a definitional artifact. -/
theorem fab_not_over : ¬ isOverdetermined fab := by
  unfold isOverdetermined fab
  decide

/-- The discriminating witness spelled out: `fab` HAS surplus constraints (`4 > 2`) yet FAILS
over-determination — pinpointing that the failure is exactly the rank condition
(`rank ≠ unknowns`), not the constraint-count condition. -/
theorem fab_fails_on_rank_not_constraints :
    fab.constraints > fab.unknowns ∧ fab.rank ≠ fab.unknowns := by
  unfold fab
  decide

#print axioms odV2_overdetermined
#print axioms odV3_overdetermined
#print axioms the_second_reduction
#print axioms residual_collapse
#print axioms self_dual_exponent_cancels
#print axioms refloat_not_reduced
#print axioms fab_not_over
#print axioms fab_fails_on_rank_not_constraints
#print axioms pin_odV2_is_odV3
#print axioms reduction_independent_of_pinned_value
#print axioms AS7_pin_gives_same_reduction
#print axioms value_dependent_map_would_differ

end Phase22AS
