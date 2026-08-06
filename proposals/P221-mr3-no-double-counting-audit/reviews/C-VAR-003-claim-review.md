# Review of C-VAR-003

## Claim Under Review

Let `X` be nonempty and let `A`, `P`, and `Q` be real-valued functionals for
which the infima of `A`, `A+P`, `A+Q`, and `A+P+Q` are finite real numbers.
C-VAR-003 defines

`I = inf(A+P+Q) + inf(A) - inf(A+P) - inf(A+Q)`.

It claims that the corresponding pointwise mixed expression is zero, that `I`
is invariant under consistent additive constants and symmetric in `P,Q`, that
it can take every real value even within nonnegative continuous coercive
quadratics on the real line, and that a common minimizer of `A,P,Q` is
sufficient but not necessary for `I=0`.

## Exact Verification

Pointwise,

`(A+P+Q)+A-(A+P)-(A+Q)=0`.

Taking four separate infima does not preserve that cancellation because the
optimizers may differ. The canonical ledger therefore computes the mixed
difference only from four caller-supplied actual finite infima; it does not
infer them.

For `A=x^2` and `P=(x-1)^2`, choosing `Q=(x+1)^2` gives `I=1`, while choosing
`Q=(x-1)^2` gives `I=-1/3`. Positive scaling realizes every positive and
negative magnitude. A common-minimizer family such as
`A=x^2, P=2x^2, Q=3x^2` gives zero. Conversely,
`Q=(x-(2+sqrt(3)))^2` gives
`I=(c^2-4c+1)/6=0` while the three component minimizers are distinct.

The primary verifier passes 26 checks. A fresh reviewer imports neither the
source nor the canonical variational API, derives quadratic minima by
completing the square, and passes 18 checks. Center mutations make the exact
zero verdict fail. Fourteen package tests and a package-root import probe pass.

## Nonduplication and Dependencies

C-VAR-002 compares the infimum of one finite sum with the sum of separately
minimized components. It does not own the four-problem mixed difference, its
sign range, or the failure of the zero/common-minimizer converse. C-GSK-001
owns a conditional radial density, while C-RDIFF-001 owns a numerical signed
difference between upper estimates. Neither is this theorem.

C-VAR-003 has no accepted-claim dependency and imports no physical constant,
field model, coefficient, state, comparator, numerical solver, or sampled
integration routine. Its mathematical assumptions are exactly the common
nonempty domain and four finite real infima.

## Framework Fit and Scope

The theorem is a compatible exact extension of the variational module. It
clarifies that a mixed response produced by separate optimization has no
universal sign. It does not prove that any MR3 stationary BVP branch is a
global minimizer, determine the sign or magnitude for a field model, establish
an additive physical observable, or diagnose double counting.

MR5 and MR6 name MR3 in prose but import neither C-VAR-003 nor its API. The
hash-pinned four-node graph passes 10 checks and grants no backward authority
to MR4-MR6. MR3, MR5, and MR6 use current SciPy `trapezoid`; no compatibility
event or legacy NumPy surface enters the claim.

## Four-Axis Decision

- Verification: `symbolic_verified`
- Review: `accepted`
- Compatibility: `compatible_extension`
- Epistemic: `active`
- Dependencies, challenges, and supersedes: none

## Promotion Boundary

Promotion adds C-VAR-003, its pure public API and tests, a qualified MR3
disposition, release v0.159.0, generated documentation and memory, and durable
campaign evidence. Because package, claim, release, test, and generated
consumer surfaces change, one full integrated validation boundary is required.

## Done Gate

C-VAR-003 is accepted only with exact primary and independent derivations,
both-sign and zero counterexamples, mutation sensitivity, nonduplication,
consumer replay, synchronized governed records, and an empty debt ledger.

## Cross-References

See P221, MR3, C-VAR-002, C-GSK-001, C-BPS-001/002, C-RDIFF-001,
`variational.py`, and `tests/test_variational.py`.
