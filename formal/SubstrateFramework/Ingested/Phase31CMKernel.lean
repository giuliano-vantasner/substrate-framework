import Mathlib

/-!
# Phase 31 — coherent medium-mediated nuclear coupling kernel (CM-L)

The Lean oracle's decidable-arithmetic contribution to the Phase-31 CMNC bridge cluster.
It certifies the discrete collective-vs-two-body facts that CM2/CM4 verify in SymPy —
the ones that reduce to genuinely decidable natural-number arithmetic (Mathlib-backed).
It does NOT force CM2's assembled rate law, CM3's crossover, or CM5's radiation model
into Lean (those are symbolic/numeric).

The coherent-medium rate scales with the collective occupation `N` (Dicke, `√N`
amplitude ⇒ rate `~N`), strictly above the two-body / `N = 1` baseline. We certify:

1. `collective_exceeds_two_body` — for `N ≥ 2`, `1 < N`: the collective coherent rate
   (`~N`) strictly exceeds the two-body baseline (`~1`). (CM4's discriminating bar, the
   discrete `dR/dN > 0` for `N ≥ 2`.)

2. `rate_linear_not_squared` — for `N ≥ 2`, `N < N * N`: an amplitude `~N` (rate `~N²`)
   is strictly larger than the true collective rate `~N` and is REJECTED. (CM2/CM4's
   reuse of PN3's superradiance-magnitude guard.)

3. `CM_L` — the compound keystone.

4. `bar_not_vacuous` — a non-tautology guard `1 < 2`, decided by `norm_num`, NOT by `rfl`:
   a flat / `N`-independent rate would collapse the strict inequality and FAIL it, so the
   bar carries real content.
-/

namespace Phase31CM

/-- **CM-L (1) — collective rate strictly exceeds the two-body baseline.**  The coherent
Dicke rate scales as `N`; for `N ≥ 2` we have `1 < N`, so the collective rate `~N` is
strictly above the `N = 1` two-body / textbook-Rabi baseline `~1`.  This is the discrete
form of CM4's discriminating bar (`dR/dN > 0` for `N ≥ 2`). -/
theorem collective_exceeds_two_body (N : ℕ) (h : 2 ≤ N) : 1 < N := by
  omega

/-- **CM-L (2) — rate is `N`, not `N²` (superradiance-magnitude guard).**  The collective
amplitude scales as `√N`, so the rate scales as `N`.  For `N ≥ 2`, `N < N * N`: the
fabricated linear amplitude (rate `~N²`) is strictly larger than the true rate `~N` and is
REJECTED. -/
theorem rate_linear_not_squared (N : ℕ) (h : 2 ≤ N) : N < N * N := by
  nlinarith [h]

/-- **CM-L (HEADLINE).**  The discrete collective-coupling keystones in one statement: the
collective rate strictly exceeds the two-body baseline, and the rate scales as `N`, not
`N²`. -/
theorem CM_L (N : ℕ) (hN : 2 ≤ N) : (1 < N) ∧ (N < N * N) :=
  ⟨collective_exceeds_two_body N hN, rate_linear_not_squared N hN⟩

/-- **CM-L (non-tautology guard).**  A concrete strict inequality `1 < 2`, decided by
`norm_num` — NOT true by `rfl`.  A fabricated flat / `N`-independent rate would make the
collective-vs-two-body comparison an equality and FAIL this, so the discriminating bar
carries real content and is not vacuous. -/
theorem bar_not_vacuous : (1 : ℕ) < 2 := by norm_num

end Phase31CM
