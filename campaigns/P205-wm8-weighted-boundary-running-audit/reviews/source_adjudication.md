# WM8 Source Adjudication

## Verdict

WM8 is qualified, not blanket accepted. It is an exact specialization of the
already accepted C-RGE-006 weighted-boundary inverse problem. With

\[
a_{\rm low}=A S+q b,\qquad C a_{\rm low}=d,
\]

the two columns `C*S` and `C*b` determine `A` and `q` when their design is
nonsingular. The canonical API reproduces the source's `N_H=1` amplitude,
scaled span, constraint residuals, and exact readout `0.216221801107...`.
These are conditional inverse-inference results from two supplied low
coordinates and supplied boundary data, not an ab-initio physical prediction.

## Exact scalar-count correction

WM8's counterfactual family changes the boundary vector

\[
S(N_H)=(4+N_H/10,4+N_H/6,4)
\]

but holds the beta vector fixed at its one-scalar value. Its exact readout is

\[
W_{\rm fixed}(N_H)=
\frac{19(91299N_H+1325644)}{452766(7N_H+268)},
\]

which is monotone on the nonnegative domain and gives the reported
`0.232261554419...` at `N_H=3`.

A coherent field-content counterfactual also changes the beta ledger to
`(4+N_H/10,-10/3+N_H/6,-7)`. Its readout is

\[
W_{\rm coherent}(N_H)=
\frac{236383N_H+2211064}{452766(N_H+24)}.
\]

The paths agree only at `N_H=1`; the coherent three-scalar result is
`0.238878442809...`, not the advertised near-hit. This does not select another
count: even the coherent two-scalar value is closer to the comparator, while
C-REP-003 and C-MIX-002 derive no physical multiplicity.

## Comparator, matching, and physical ceiling

AST dataflow confirms that the measured coordinate is absent from
`solve_boundary`. However, WM8.8's named `perturbed` result repeats the same
call with identical arguments; no comparator mutation is executed. A genuine
comparator change affects only the post-solve miss. Independent matching
offsets and either low target change the exact readout. Thresholds, Yukawa
terms, schemes, uncertainties, perturbative-domain evidence, and physical
input provenance are absent. The residual therefore cannot be uniquely
localized in scalar multiplicity.

## Verification, compatibility, and graph closure

The hash-pinned source exits zero with ten checks. The canonical primary route
passes 37 checks after three preserved verifier-construction repairs, and a
raw independent design inversion passes 19. The 13-node graph passes 38 checks
over 118 static predicates and 15 assertions. All dependencies are terminal;
WM7 grants no backward authority, and WM9, WM10, and GC6 remain pending.

WM8, its runtime imports, and mutable P205 contain no quadrature surface.
Immutable S2's legacy syntax is alias-only compatibility evidence and causes
zero scientific failures. WM8 is terminally qualified through C-MIX-002,
C-REP-001, C-REP-003, C-RGE-004, C-RGE-005, C-RGE-006, and C-VAC-003.
