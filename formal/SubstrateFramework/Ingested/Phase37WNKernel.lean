import Mathlib

/-!
# Phase 37 — subdivision-weight crossover kernel (WN-L)

The Lean oracle's decidable-arithmetic contribution to the Phase-37 subdivision-weight
cluster. It certifies the discrete facts underlying WN4's headline crossover — the ones that
reduce to genuinely decidable natural-number arithmetic (Mathlib-backed). It does NOT force
WN3's ladder-algebra derivation, WN1's arbitrary-precision magnitude bound, or WN5's rational
branching fraction into Lean (those are symbolic/numeric).

The derived weight is `w n = S^n / n!`. Over `ℕ` we compare `w (n+1)` against `w n` by
cross-multiplying, which is exact and avoids division:

  `w (n+1) < w n`  ⟺  `S^(n+1) * n! < S^n * (n+1)!`.

We certify:

1. `weight_pos` — for `0 < S`, the cross-multiplied weight `S^n * n!` is strictly positive at
   EVERY order `n`, including even `n`. This is the discrete form of the fact that the derived
   weight has no parity zero — the vanishing at even `n` that refuted the naive candidate
   `|c_n|²` (WN2 R1) is an artifact of the single-mode toy and is absent here.

2. `crossover` — the exact turnover law: `S^(n+1) * n! < S^n * (n+1)!  ↔  S < n + 1`. This is
   WN4's ratio law `w(n+1)/w(n) = S/(n+1)` in cross-multiplied form: the weight falls at order
   `n` precisely when `S < n+1`, and rises precisely when `S > n+1`. Both of Phase-32's named
   candidate regimes are limbs of this one law.

3. `growth_limb` — the rising side, stated separately: `n + 1 < S → S^n * (n+1)! < S^(n+1) * n!`.

4. `halving_tail` — the suppression limb is at least geometric: once `2 * S ≤ n + 1`, each step
   at least HALVES the weight, `2 * (S^(n+1) * n!) ≤ S^n * (n+1)!`. Iterating this is the
   discrete form of "decays at least as fast as `e^(-α n)`" (WN4.4b).

5. `WN_L` — the compound keystone.

6. `crossover_not_vacuous` — a concrete strict instance decided by `norm_num`, NOT by `rfl`:
   at `S = 3, n = 5` the weight is already falling (`3 < 6`). A weight with no crossover
   (either of Phase-32's monotone named regimes) could not satisfy both this and
   `growth_limb`, so the turnover carries real content.
-/

namespace Phase37WN

/-- **WN-L (1) — no parity zero.**  For `0 < S`, the cross-multiplied derived weight
`S^n * n!` is strictly positive at EVERY order `n`, even and odd alike.  The naive candidate
`|c_n|² = 1/(n!)²` vanishes identically at even `n` (PN1's even-cosine selection rule), which
is one of the three refutations in WN2; the derived weight has no such zero, because the even
orders are opened by the amplitude scale `S`. -/
theorem weight_pos (S n : ℕ) (hS : 0 < S) : 0 < S ^ n * Nat.factorial n :=
  Nat.mul_pos (pow_pos hS n) (Nat.factorial_pos n)

/-- **WN-L (2) — THE CROSSOVER (headline).**  The derived weight `w n = S^n/n!` falls at order
`n` precisely when `S < n + 1`, in exact cross-multiplied form.  This is WN4's ratio law
`w(n+1)/w(n) = S/(n+1)`: the "phase-space growth" and "energy-gap-law decay" regimes that
Phase-32 records as competing candidates are the `S > n+1` and `S < n+1` limbs of this single
law. -/
theorem crossover (S n : ℕ) (hS : 0 < S) :
    S ^ (n + 1) * Nat.factorial n < S ^ n * Nat.factorial (n + 1) ↔ S < n + 1 := by
  have hpos : 0 < S ^ n * Nat.factorial n := weight_pos S n hS
  have hL : S ^ (n + 1) * Nat.factorial n = (S ^ n * Nat.factorial n) * S := by
    rw [pow_succ]; ring
  have hR : S ^ n * Nat.factorial (n + 1) = (S ^ n * Nat.factorial n) * (n + 1) := by
    rw [Nat.factorial_succ]; ring
  rw [hL, hR]
  exact Nat.mul_lt_mul_left hpos

/-- **WN-L (3) — the growth limb.**  Below the turnover the weight strictly RISES: this is the
"more subdivision orders are more favoured" phase-space side. -/
theorem growth_limb (S n : ℕ) (hS : 0 < S) (h : n + 1 < S) :
    S ^ n * Nat.factorial (n + 1) < S ^ (n + 1) * Nat.factorial n := by
  have hpos : 0 < S ^ n * Nat.factorial n := weight_pos S n hS
  have hL : S ^ (n + 1) * Nat.factorial n = (S ^ n * Nat.factorial n) * S := by
    rw [pow_succ]; ring
  have hR : S ^ n * Nat.factorial (n + 1) = (S ^ n * Nat.factorial n) * (n + 1) := by
    rw [Nat.factorial_succ]; ring
  rw [hL, hR]
  exact (Nat.mul_lt_mul_left hpos).mpr h

/-- **WN-L (4) — the suppression limb is at least geometric.**  Once `2 * S ≤ n + 1`, every
further step at least HALVES the weight.  Iterating gives decay at least as fast as any fixed
exponential — the discrete form of WN4.4b's `for every α > 0` energy-gap-law bound. -/
theorem halving_tail (S n : ℕ) (hS : 0 < S) (h : 2 * S ≤ n + 1) :
    2 * (S ^ (n + 1) * Nat.factorial n) ≤ S ^ n * Nat.factorial (n + 1) := by
  have hpos : 0 < S ^ n * Nat.factorial n := weight_pos S n hS
  have hL : 2 * (S ^ (n + 1) * Nat.factorial n) = (S ^ n * Nat.factorial n) * (2 * S) := by
    rw [pow_succ]; ring
  have hR : S ^ n * Nat.factorial (n + 1) = (S ^ n * Nat.factorial n) * (n + 1) := by
    rw [Nat.factorial_succ]; ring
  rw [hL, hR]
  exact Nat.mul_le_mul_left _ h

/-- **WN-L (HEADLINE).**  The discrete subdivision-weight keystones in one statement: the
derived weight is positive at every order (no parity zero), and its rise-or-fall at order `n`
is decided exactly by the sign of `S - (n+1)`. -/
theorem WN_L (S n : ℕ) (hS : 0 < S) :
    (0 < S ^ n * Nat.factorial n) ∧
    (S ^ (n + 1) * Nat.factorial n < S ^ n * Nat.factorial (n + 1) ↔ S < n + 1) :=
  ⟨weight_pos S n hS, crossover S n hS⟩

/-- **WN-L (non-tautology guard).**  A concrete strict instance, decided by `norm_num` — NOT
true by `rfl`.  At `S = 3` the weight is already falling at `n = 5` (since `3 < 6`):
`3^6 * 5! = 87480 < 174960 = 3^5 * 6!`.  Together with `growth_limb` (which gives a strictly
RISING step whenever `n + 1 < S`) this shows the weight genuinely turns over; a monotone
weight — which is what each of Phase-32's three named regimes is in isolation — cannot
satisfy both. -/
theorem crossover_not_vacuous :
    3 ^ 6 * Nat.factorial 5 < 3 ^ 5 * Nat.factorial 6 := by
  norm_num [Nat.factorial]

/-- **WN-L (turnover witness).**  The two limbs are BOTH realized by one and the same weight:
at `S = 10` the step at `n = 3` rises (`4 < 10`) while the step at `n = 20` falls (`10 < 21`).
This is the content a single-limb (monotone) weight cannot reproduce. -/
theorem both_limbs_realized :
    (10 ^ 3 * Nat.factorial 4 < 10 ^ 4 * Nat.factorial 3) ∧
    (10 ^ 21 * Nat.factorial 20 < 10 ^ 20 * Nat.factorial 21) := by
  constructor
  · norm_num [Nat.factorial]
  · exact (crossover 10 20 (by norm_num)).mpr (by norm_num)

end Phase37WN
