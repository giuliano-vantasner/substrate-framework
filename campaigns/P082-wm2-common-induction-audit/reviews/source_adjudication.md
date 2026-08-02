# P082 Source Adjudication: WM2

WM2 is duplicate evidence. Its valid trace and conditional coupling algebra is
already accepted in C-REP-001 and C-LIE-001. It does not derive the common
physical induction coefficient on which every advertised result depends.

## Reproduction

The hash-pinned source exits cleanly and prints `ALL 10 CHECKS PASS`. Its
supplied state table gives `S2=2` and `SY=10/3`; a supplied count of four colour
triplet copies with `T(F)=1/2` gives `S3=2`. With zero additive baselines and one
declared coefficient, it obtains `gY^2/g2^2=3/5`, the reciprocal canonical
conversion `g1^2/gY^2=5/3`, and the conditional angle `3/8`. This is exact
symbolic work and uses neither `np.trapz` nor `np.trapezoid`.

## What the Common Law Actually Proves

For positive supplied traces and couplings, C-REP-001 already proves that

```text
1/g2^2 = C*S2,
1/gY^2 = C*SY
```

implies `gY^2/g2^2=S2/SY`. On WM2's supplied table the right side is `3/5`,
and the associated two-coupling coordinate is `3/8`. The common law is a
premise. WM2 never computes a loop determinant, regulator, cutoff, field
measure, profile, action, counterterm, or matching condition; its executable
imports only SymPy and declares `C` as a positive symbol. The prose explicitly
labels one common `C` as `DECLARED` and calls it the new physics.

Every advertised mechanism source—EM5, YM1, QCD1, S2, S3, SM3, SM4, and W2—is
pending with an empty accepted-claim mapping. C-GAU-001 separately establishes
that local U(1) covariance leaves the kinetic coefficient unconstrained.

## Abelian Coordinate Counterfamily

The common law does not fix an overall Abelian normalization even if granted.
For any positive `rho`, transform

```text
Y' = rho*Y,
gY' = gY/rho.
```

Then `SY'=rho^2*SY`, every coupled charge `gY*Y` is invariant, and
`1/gY'^2=C*SY'` remains true with the same `C`. But the squared-coupling
coordinate becomes

```text
gY'^2/g2^2 = (3/5)/rho^2.
```

Choosing `rho=sqrt((3/5)/r)` realizes any positive target `r`. Thus the
source's numeric 3/5 belongs to its preselected `Y` coordinate; the common law
does not select that coordinate from anomaly homogeneity or physical charge.

The special `rho=sqrt(3/5)` makes `SY'=S2=2` and `g1^2/g2^2=1`. That equality is
a canonical coordinate construction. With the reciprocal electric-charge
coefficient, the original `Q=T3+Y` and its 3/8 trace quotient remain unchanged.
Calling unscaled `Y` “wrong” and the equal-trace coordinate “required” confuses
a useful convention with physical selection.

## Omitted Affine Baselines

A provenance-complete inverse-coupling law has the form

```text
1/g_i^2 = K_i + C_i*S_i.
```

WM2 supplies `K_i=0` and `C_i=C`. Independent positive coefficients retain the
free factor `C2/CY`, as its own WM2.8 guard admits. A nonzero sector baseline
also breaks the 3/5 ratio while leaving all traces and the common loop term
unchanged. No source check derives zero tree terms or equal counterterms.

## Source Checks

- WM2.1 and WM2.3 duplicate C-REP-001's supplied-table traces.
- WM2.2 composes a supplied triplet count with C-LIE-001's convention-specific
  `T(F)=1/2`; it derives no physical spectrum.
- WM2.4 and WM2.7 duplicate C-REP-001's conditional common-law result.
- WM2.5 and WM2.6 are exact reciprocal generator/coupling coordinate changes,
  not a derived unified action or GUT boundary.
- WM2.8 correctly exposes independent coefficients and thereby confirms the
  missing premise is load bearing.
- WM2.9 compares two conventions and incorrectly labels one physically wrong.
- WM2.10 shows sensitivity to supplied colour content, not derivation of that
  content or its induction mechanism.

The free symbol `C` leaves the absolute coupling magnitude unpredicted, and no
executable boundary scale or running prescription exists.

## Terminal Decision

WM2 adds no claim or canonical API. Its exact content is duplicate evidence for
C-REP-001's finite traces, Abelian covariance, common-coefficient condition,
and coupling angle, plus C-LIE-001's fundamental Dynkin convention. It
establishes no common physical loop coefficient, gauge actions, counterterm
matching, physical hypercharge normalization, unified coupling boundary, weak
mixing angle, running, observed value, Standard Model, or substrate mechanism.
