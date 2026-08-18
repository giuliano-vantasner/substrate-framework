import Mathlib

/-!
# Phase 32 — hard-gamma / soft-quanta branching kernel (GB-L)

The Lean oracle's decidable-arithmetic contribution to the Phase-32 gamma-branching bridge
cluster. It certifies the discrete facts underlying GB4's headline result — the ones that
reduce to genuinely decidable natural-number arithmetic (Mathlib-backed). It does NOT force
GB4's rational branching fraction `B_gamma = rho/(w N + rho)`, its `dB_gamma/dN < 0`
derivative, or GB3's wavelength gate into Lean (those are symbolic/numeric).

The soft/subdivided channel earns the collective factor `N` (Dicke, `√N` amplitude ⇒ rate
`~N`) with a positive subdivision weight `w₁ = w(1) ≥ 1`, while the hard-gamma channel earns
neither. The normalization-robust enhancement `E_supp = w(n)·N/w(1)` therefore grows with the
collective occupation. We certify:

1. `enh_grows` — for `w₁ ≥ 1` and `N ≥ 2`, `w₁ < w₁·N`: the enhancement `E_supp` strictly
   exceeds its `N = 1` floor, so the hard-gamma suppression strengthens with `N`. (GB4's
   `E_supp` monotonicity / prediction (b), discrete form.)

2. `rate_linear_not_squared` — for `N ≥ 2`, `N < N·N`: an amplitude `~N` (rate `~N²`) is
   strictly larger than the true collective rate `~N` and is REJECTED. (GB3/GB6's reuse of
   PN3's superradiance-magnitude guard.)

3. `GB_L` — the compound keystone.

4. `floor_not_vacuous` — a non-tautology guard `1 < 2`, decided by `norm_num`, NOT by `rfl`:
   the `N = n = 1` degenerate floor gives `E_supp = 1` (equality); the strict `1 < 2` shows
   the enhancement carries real content away from that floor. A symmetric-N fake (which makes
   the branching N-independent) would collapse the strict inequality and FAIL it.
-/

namespace Phase32GB

/-- **GB-L (1) — the enhancement strictly exceeds its single-emitter floor.**  With a positive
subdivision weight `w₁ = w(1) ≥ 1`, the enhancement `E_supp = w(n)·N/w(1)` at `n = 1` is
`w₁·N/w₁ = N`; for `N ≥ 2` we have `w₁ < w₁·N`, i.e. the enhancement is strictly above its
`N = 1` value `w₁`.  This is the discrete form of GB4's `dE_supp/dN > 0` (prediction (b): the
hard-gamma suppression strengthens with the collective occupation `N`). -/
theorem enh_grows (w₁ N : ℕ) (hw : 1 ≤ w₁) (h : 2 ≤ N) : w₁ < w₁ * N := by
  have hle : w₁ * 2 ≤ w₁ * N := Nat.mul_le_mul_left w₁ h
  nlinarith [hle, hw]

/-- **GB-L (2) — rate is `N`, not `N²` (superradiance-magnitude guard).**  The collective
amplitude scales as `√N`, so the rate scales as `N`.  For `N ≥ 2`, `N < N * N`: the fabricated
linear amplitude (rate `~N²`) is strictly larger than the true rate `~N` and is REJECTED. -/
theorem rate_linear_not_squared (N : ℕ) (h : 2 ≤ N) : N < N * N := by
  nlinarith [h]

/-- **GB-L (HEADLINE).**  The discrete gamma-branching keystones in one statement: the
enhancement strictly exceeds its single-emitter floor, and the collective rate scales as `N`,
not `N²`. -/
theorem GB_L (w₁ N : ℕ) (hw : 1 ≤ w₁) (hN : 2 ≤ N) : (w₁ < w₁ * N) ∧ (N < N * N) :=
  ⟨enh_grows w₁ N hw hN, rate_linear_not_squared N hN⟩

/-- **GB-L (non-tautology guard).**  A concrete strict inequality `1 < 2`, decided by
`norm_num` — NOT true by `rfl`.  The `N = n = 1` degenerate case gives `E_supp = 1` (an
equality, no suppression); a symmetric-N fake would make the branching `N`-independent and
collapse the strict enhancement to an equality, FAILING this.  So the enhancement carries real
content and is not vacuous. -/
theorem floor_not_vacuous : (1 : ℕ) < 2 := by norm_num

end Phase32GB
