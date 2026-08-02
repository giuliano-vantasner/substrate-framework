# WZ1 Source Adjudication

WZ1 is qualified. Its Maurer-Cartan trace-five closedness, pointwise
nonvanishing, metric-free local density, and ungauged exact boundary variation
survive with stronger exact replacements. Its printed global non-exactness
oracle, even-power guard, Chern-Simons/anomaly-inflow interpretation, period,
level, baryon-current, and physical conclusions do not.

## Reproduction and Provenance

The hash-pinned source at `substrate@6d1f4e0` exits with status zero and
`ALL 12 CHECKS PASS` in 0.51 seconds under NumPy 2.5.1 and SymPy 1.14.0. The
source file matches inventory SHA-256
`87bab354a83a6edd05ed77ed0778e1cdf11cf402f92414664f7a3196df0551b9`.
S3, S4, WZ2, and WZ3 are pending navigation evidence, not authority.

## Surviving Local Algebra

For `theta=U^-1 dU`, Maurer-Cartan gives `d theta=-theta^2`. Graded cyclicity
makes the alternating trace of six one-forms vanish, so
`d Tr(theta^5)=0`. WZ1's finite-difference chart is consistent with this fact,
and its sampled trace-five component is nonzero and imaginary in an
anti-Hermitian convention. P056 replaces both sampled predicates with exact
cochain algebra.

The density is visibly a finite polynomial in `U`, `U^-1`, and first
derivatives with no metric or Hodge star. The source's executable checks do not
validate that statement: its metric oracle substitutes into the stand-in
constant `omega5_weyl=1`, and its locality predicate includes the literal
`uses_first_derivs_only=True`. The mathematical statement survives by direct
construction, not because those checks passed.

For an ungauged variation `delta U=U v`, trace invariance removes the
commutator part of `delta theta=dv+[theta,v]`. Since
`d(theta^4)=0`, the exact identity is
`delta Tr(theta^5)=d(5 Tr(v theta^4))`. This supplies a boundary variation of
the map functional, but no gauge connection or physical current.

## False Even-Power Guard

WZ1's advertised rejection guard is false. Full wedge antisymmetrization gives
`Tr(theta^4)=0`: moving one odd factor cyclically past three others reverses
the sign while preserving the trace. In the exterior derivative, the four
graded Leibniz contributions cancel after cyclic reordering. Thus
`d Tr(theta^4)=0`, not `-4 Tr(theta^5) != 0`.

The executable never evaluates `d Tr(theta^4)`. It samples a separate nonzero
alternating trace of five random matrices and labels that value the derivative,
having omitted the other three Leibniz terms. Its guard therefore passes while
asserting the wrong mathematical result. P056 preserves this as a concrete
validation-theater counterexample.

## Global Non-Exactness Replacement

WZ1 assigns `wzw_period=1` and `exact_period=0`, then checks that they differ.
It constructs neither a closed cycle nor a generator map and performs no
period integral. The check cannot validate global non-exactness or
normalization.

P056 instead builds the exact left-invariant Chevalley-Eilenberg complex from
C-LIE-001. In degrees four through six, `rank d4=35`, `rank d5=20`, and
`dim ker d5=36`, so invariant fifth cohomology is one-dimensional. The real
cochain `Omega5=-i Alt Tr(theta^5)` has nine nonzero components, norm squared
`75/4`, is closed, and raises the rank of `[d4|Omega5]` from 35 to 36. An
independent route shows `Omega5^T d4=0` and
`Omega5^T Omega5=75/4`, directly separating it from every coboundary.

If this left-invariant form had a global primitive on compact SU(3), normalized
Haar averaging of that primitive would give a left-invariant primitive because
averaging commutes with `d` and fixes `Omega5`. The exact non-image result
therefore establishes global non-exactness without importing a numerical or
integer period. It does not fix the period lattice.

## Filling, Descent, and Physical Ceiling

For two oriented extensions, the mathematical gluing identity is
`I(B)-I(B')=integral_{B union -B'} Omega5`. Their phase ratio is
`exp(i c [I(B)-I(B')])`. Filling independence follows only if the declared
coefficient times every period lies in `2*pi*Z`. P056 assigns no generator
period, WZW level, `N_c`, or physical coefficient.

WZ1 supplies no gauge connection, curvature, anomaly polynomial, descent
equations, gauged transformation, or baryon-current map. Its ungauged exact
variation is therefore not a derivation of a Goldstone-Wilczek current,
Callan-Harvey anomaly inflow, or a five-dimensional gauge Chern-Simons action.
Those remain separate WZ2/WZ3 or future campaign obligations.

## Terminal Disposition

WZ1 maps to exact mathematical claim `C-WZW-001`. It remains qualified for
its hard-coded unit period, integer-period or `pi_5` generator construction,
WZW normalization and level, the false even-power guard, any local-4D
Lagrangian impossibility stronger than global non-exactness, gauge
Chern-Simons descent, anomaly inflow, Goldstone-Wilczek baryon current,
`N_c`, representation selection, physical bulk or boundary dynamics,
absolute scale, and substrate realization.
