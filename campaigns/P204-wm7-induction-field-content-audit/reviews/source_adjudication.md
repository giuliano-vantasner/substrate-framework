# WM7 Source Adjudication

## Verdict

WM7 is qualified, not blanket accepted. Its strongest exact content is supplied-
table composition. With the C-RGE-005 three-generation rows, gauge, Weyl, and
one-complex-doublet contributions are

\[
(0,-22/3,-11),\qquad (4,4,4),\qquad (1/10,1/6,0).
\]

Thus `N_H` supplied scalar doublets give

\[
S(N_H)=(4+N_H/10,\;4+N_H/6,\;4),
\]

whose components are equal exactly when `N_H=0`. At `N_H=1` this is
`(41/10,25/6,4)`, with integer ratio `123:125:120` and spread `25/24`.
These are exact accepted composition, not a new common-induction theorem.

## Weight reconstruction

WM7 solves `c_F=2/3` and `c_S=1/3` from SM4 coefficients. The two-column
design has rank two and one left-null consistency relation, but the target
coefficients were constructed using those same imported weights. The operation
is inverse reconstruction. An independent target mutation violates the
consistency relation, and deleting the scalar removes identifiability of
`c_S`. The source's “over-determined derivation” language is rejected.

## Common boundary and normalization

For `a_i=z_i+C_i S_i`, one common nonzero `C` yields the source ratio only
after `z_i=0` is imposed. Nonzero boundaries or independent coefficients break
it. Under the separately supplied inverse-trace law and chosen hypercharge
normalization, `N_H=1` gives the exact coordinate `25/66`; equal independently
supplied couplings give `1/2` instead, and Abelian rescaling moves the raw
coordinate. No preferred normalization, matching action, physical coupling,
or weak-angle observable is derived.

## Counts and gauge-loop guard

C-REP-003 keeps the finite field rows and scalar entry supplied. C-MIX-002's
generic phase count does not derive three physical generations. WM7 therefore
tests sensitivity to `N_H/N_GEN` but does not derive either count. Likewise,
a negative gauge beta contribution is not a negative total kinetic coordinate:
positive affine offsets supply an exact counterexample. WM7 constructs no
determinant, regulator, counterterm, or self-consistent gauge-induction action,
so its gauge-self-induction no-go is unsupported.

## Verification, compatibility, and graph closure

The hash-pinned source exits zero with all ten checks. The primary accepted-API
route passes 38 exact checks, a raw independent route passes 21, and the
26-node graph replay passes 66 while pinning 228 static checks and 31 assertions.
WM7 and mutable P204 code have no quadrature surface. Immutable S2, W1, and W3
retain legacy-name syntax; that is alias-only compatibility evidence and causes
zero scientific failures.

WM8 is the sole pending dependency and forms a two-node source SCC with WM7.
It is excluded from authority. All nine direct reverse consumers remain
pending. WM7 is terminally qualified through C-MIX-002, C-REP-001, C-REP-003,
C-ANO-001, C-RGE-005, and C-VAC-003, with C-RGE-007 unpromoted.
