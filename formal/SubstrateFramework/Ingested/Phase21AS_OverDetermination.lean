import Mathlib
namespace Phase21AS


/-!
# Phase 21 AS-L — The over-determination rank-FLIP that expires the absolute-scale deferral

This file is the Lean oracle's contribution for unified-framework Phase 21, step AS-L.
It machine-checks the DISCRETE-FACT OUTPUT behind the absolute-scale wall (Part 4): the
over-determination instrument's verdict FLIPPED from "NOT over-determined → deferral
correct" (Phase 19, OD-v1) to "OVER-determined → the scale has emerged as a one-parameter
family in the lattice length `a`" (Phase 21, OD-v2). The SymPy oracle
(`merged-framework/bridges/phase-21/bridge_AS4_over_determination_v2.py`) ran the linear-
algebra over the verified ratio-chains and computed the two ranks; this file certifies the
VERDICT LOGIC and the FLIP from those ranks.

The physics story (verified in the SymPy bridge, asserted here as INPUT):

- **OD-v1 (Phase 19).** The verified scale chains, written over the unknowns
  `{ln a, ln m_e, ln κ, ln v, ln c}` (5 columns), produced a coefficient matrix of RANK 4
  over 4 independent constraints, because each chain hid its OWN free dimensionful constant
  (S5's `m_e`, G5's `κ`, M1's `v`, CF4's `c`). Nullity `5 − 4 = 1 > 0`: the direction `ln a`
  is UNPINNED — the system does NOT over-determine the scale, so the deferral was correct.

- **OD-v2 (Phase 21).** The Phase-21 reductions eliminate three free dimensionful columns:
  AS1 ties the IR soliton length `ξ` to `a` by dimensional transmutation
  (`ξ/a = exp(−8π²/(b₀β²))`); AS2 eliminates `kB·T` (Debye `kB·T = ħ c_s / a`); AS3 pins the
  Sakharov stiffness `κ ∼ a²` (`G_eff = a² c₀³/(s_G ħ)`). What survives is `{ln a, 1/β²}`
  (2 columns) — one length and one dimensionless coupling. The matrix now has RANK 2 over
  the SAME 4 independent constraints. Nullity `2 − 2 = 0`: BOTH `ln a` and `1/β²` are PINNED,
  and with `4 > 2` constraints the system is OVER-determined (two chains pin `a`, two pin
  `β²`; the redundancy is a falsifiable prediction relating observables).

- **The FLIP.** Nullity `1` (under-determined, `ln a` free) → nullity `0` (over-determined,
  everything pinned). The number of eliminated free dimensionful columns is exactly
  `5 − 2 = 3` — the three reductions AS1, AS2, AS3.

## Physics offered as INPUT (not proved here — the "physics map")

- **(The two ranks.)** That the OD-v1 system has rank 4 (over 5 unknowns, 4 constraints) and
  the OD-v2 system has rank 2 (over 2 unknowns, 4 constraints) are the SymPy oracle's outputs
  (matrix-rank over the derived `a`-power / RG-exponent coefficient matrices). These integers
  `4` and `2` are ASSERTED here as physics INPUT (computed in the bridge), NOT recomputed as a
  matrix rank inside Lean. The Lean file imports them as the field values of the two systems.
- **(That AS1–AS3 each remove exactly one free dimensionful column.)** That the three
  physical identifications collapse the column count `5 → 2` (three eliminations: `ln m_e` via
  the ξ-tie, `ln κ` via `a²`, `ln v / kB·T` via the medium-constant ride) is the AS1–AS3
  content, verified in the SymPy bridges, asserted here.

## The arithmetic this file PROVES (the OUTPUT, machine-checked here)

A `Determination` packages a linear system's `unknowns`, `constraints`, and `rank` as
naturals. The verdict logic is decidable natural-number arithmetic:

- `nullity s = s.unknowns − s.rank` (the free-direction count; `0` ⟺ all unknowns pinned).
- `isOverdetermined s` ⟺ `s.rank = s.unknowns ∧ s.constraints > s.unknowns` (full column rank
  AND strictly more constraints than unknowns — the redundant, falsifiable over-constraint).

We import the two systems as the oracle's rank facts:
`odV1 = ⟨5, 4, 4⟩` (Phase-19 OD-v1) and `odV2 = ⟨2, 4, 2⟩` (Phase-21 OD-v2).

* `odV1_underdetermined` — OD-v1 is NOT over-determined (rank `4 ≠ 5` unknowns; `ln a` free).
* `odV2_overdetermined` — OD-v2 IS over-determined (rank `2 = 2` unknowns AND `4 > 2`).
* `the_flip` — THE HEADLINE: `nullity odV1 = 1 ∧ nullity odV2 = 0`; the rank-flip from a free
  direction to none.
* `columns_eliminated` — `odV1.unknowns − odV2.unknowns = 3`: the three free dimensionful
  columns AS1–AS3 removed.
* `fab_not_over` — the NON-TAUTOLOGY GUARD: a fabricated system `fab = ⟨3, 4, 2⟩` (rank `2 <`
  unknowns `3`, still a free direction) is NOT over-determined, even though it has `4 > 3`
  constraints. So over-determination is NOT automatic from "4 constraints" — it requires
  `rank = unknowns`. This is OD-v1's failure mode reproduced (the bridge's G-freelength guard:
  a chain carrying its own free length re-opens a null direction).

Honesty: a fully-proved theorem proves exactly its own statement. This checks the VERDICT
LOGIC and the FLIP given the two ranks `4` and `2` from the SymPy oracle — that with full
column rank and surplus constraints the system over-determines, that the surviving column
count dropped by 3, and that the predicate genuinely discriminates (the fabricated rank-
deficient system fails). It does NOT recompute the matrix ranks, derive the AS1–AS3
reductions, or claim `a` is given a number — over-determination is a ONE-LENGTH family that
still needs one observation to fix the absolute `a` (Buckingham). Those are the asserted
physics premises (verified in the SymPy bridges AS1–AS4), beyond what is recomputed in Lean.
This sits alongside the other Phase capstones' "physics map asserted as input" framing (cf.
`dynamics_lean/Phase19_D3S_LocalityImpliesS1.lean`'s symbol-power arithmetic and
`dynamics_lean/Phase5Gravity_GravitonTT.lean`'s TT-DOF counting).
Quality bar / style exemplar: `dynamics_lean/Phase19_D3S_LocalityImpliesS1.lean`.
-/

/-- A linear determination system reduced to its three integer invariants: the number of
`unknowns` (columns), the number of independent `constraints` (rows), and the coefficient-
matrix `rank`. The rank is the SymPy oracle's output, imported here as a field value. -/
structure Determination where
  unknowns : ℕ
  constraints : ℕ
  rank : ℕ

/-- The nullity (free-direction count) of a determination system: `unknowns − rank` (natural
subtraction; for a well-posed system `rank ≤ unknowns`, so this is the genuine free count).
Nullity `0` ⟺ every unknown is pinned. -/
def nullity (s : Determination) : ℕ := s.unknowns - s.rank

/-- A system is OVER-determined iff it has FULL column rank (`rank = unknowns`, every unknown
pinned, nullity `0`) AND strictly MORE constraints than unknowns (`constraints > unknowns`,
the surplus = redundant constraints that become falsifiable predictions). Both conjuncts are
required: full rank alone is just "determined"; surplus constraints alone (with rank
deficiency) is still under-determined. -/
def isOverdetermined (s : Determination) : Prop :=
  s.rank = s.unknowns ∧ s.constraints > s.unknowns

/-- Phase-19 OD-v1: the UN-reduced scale system over `{ln a, ln m_e, ln κ, ln v, ln c}`
(5 unknowns), 4 independent constraints, coefficient-matrix rank 4 (SymPy oracle). -/
def odV1 : Determination := ⟨5, 4, 4⟩

/-- Phase-21 OD-v2: after AS1–AS3 eliminate three free dimensionful columns, the system over
`{ln a, 1/β²}` (2 unknowns), the SAME 4 constraints, coefficient-matrix rank 2 (SymPy
oracle). -/
def odV2 : Determination := ⟨2, 4, 2⟩

/-- OD-v1 is NOT over-determined: its rank `4` is not full (`4 ≠ 5` unknowns), so the
direction `ln a` is free (nullity `1`). The Phase-19 deferral was correct. -/
theorem odV1_underdetermined : ¬ isOverdetermined odV1 := by
  unfold isOverdetermined odV1
  decide

/-- OD-v2 IS over-determined: full column rank (`rank 2 = 2` unknowns, nullity `0`) AND
surplus constraints (`4 > 2`). Both `ln a` and `1/β²` are pinned, with two redundant chains. -/
theorem odV2_overdetermined : isOverdetermined odV2 := by
  unfold isOverdetermined odV2
  decide

/-- THE HEADLINE — the rank-FLIP: OD-v1 has nullity `1` (a free direction, `ln a`), OD-v2 has
nullity `0` (everything pinned). The deferral's expiry condition is MET: the scale has emerged
as a one-parameter family in the lattice length `a`. -/
theorem the_flip : nullity odV1 = 1 ∧ nullity odV2 = 0 := by
  unfold nullity odV1 odV2
  decide

/-- The three free dimensionful columns the AS1–AS3 reductions removed: the surviving unknown
count dropped from `5` to `2`, a difference of `3` (AS1 the ξ-tie eliminating `ln m_e`; AS2
the medium-constant ride eliminating `kB·T`/`ln v`; AS3 the Sakharov pin eliminating `ln κ`). -/
theorem columns_eliminated : odV1.unknowns - odV2.unknowns = 3 := by
  unfold odV1 odV2
  decide

/-- A fabricated system: 3 unknowns, 4 constraints, rank 2. It has surplus constraints
(`4 > 3`) but is RANK-DEFICIENT (`rank 2 < 3` unknowns), so a null direction survives. -/
def fab : Determination := ⟨3, 4, 2⟩

/-- NON-TAUTOLOGY GUARD: the fabricated system `fab = ⟨3, 4, 2⟩` is NOT over-determined,
DESPITE having `4 > 3` constraints — because its rank `2 ≠ 3` is not full (a free direction
remains, nullity `1`). So over-determination is NOT automatic from "more constraints than
unknowns"; it strictly requires `rank = unknowns`. This is OD-v1's failure mode (a chain
carrying its own free length re-opens a null direction — the bridge's G-freelength guard);
the predicate genuinely discriminates, so OD-v2's verdict is a real finding, not a definition. -/
theorem fab_not_over : ¬ isOverdetermined fab := by
  unfold isOverdetermined fab
  decide

/-- The discriminating witness, spelled out: `fab` HAS surplus constraints (`4 > 3`) yet FAILS
over-determination — pinpointing that the failure is exactly the rank condition (`rank ≠
unknowns`), not the constraint-count condition. -/
theorem fab_fails_on_rank_not_constraints :
    fab.constraints > fab.unknowns ∧ fab.rank ≠ fab.unknowns := by
  unfold fab
  decide

#print axioms odV1_underdetermined
#print axioms odV2_overdetermined
#print axioms the_flip
#print axioms columns_eliminated
#print axioms fab_not_over
#print axioms fab_fails_on_rank_not_constraints

end Phase21AS
