# P081 Source Adjudication: WM1

WM1 is qualified. Its supplied-table trace arithmetic survives, but its
physical weak-angle interpretation lacks accepted representation, gauge-action,
normalization, unification, and running premises. One advertised mutation guard
is false.

## Reproduction

The hash-pinned source exits cleanly and prints `ALL 9 CHECKS PASS`. Its fifteen
weighted states give `Tr(T3^2)=2`, `Tr(Y^2)=10/3`, `Tr(T3*Y)=0`,
`Tr(Q^2)=16/3`, and quotient `3/8` exactly. Removing colour multiplicities gives
`9/28`; omitting the charged singlet gives `6/13`. This is exact symbolic work
and uses neither `np.trapz` nor `np.trapezoid`.

## Finite Trace Ledger

For a separately supplied nonempty finite table `(m_i,t_i,y_i)` and exact real
coefficient `c`, define `Q_i=t_i+c*y_i`. Direct expansion gives

```text
T_Q = T_2 + 2*c*T_X + c^2*T_Y,
T_2 = sum_i m_i*t_i^2,
T_X = sum_i m_i*t_i*y_i,
T_Y = sum_i m_i*y_i^2.
```

The reusable ledger retains the cross term and reports `T_2/T_Q` only when the
denominator is provably nonzero. Labels are provenance keys, not physical
representations. Relabeling all states leaves the arithmetic unchanged.

## Abelian Normalization

For positive `rho`, replacing `y_i` by `rho*y_i` while holding `c` fixed gives,
for WM1's zero-cross table,

```text
T_2/T_Q(rho) = 3/(3+5*rho^2).
```

But the covariant coordinate change `c->c/rho` preserves every `Q_i` and the
trace quotient. With `gY->gY/rho`, every product `gY*y_i` and the coupled trace
norm `gY^2*T_Y` is also preserved. Homogeneous moments scale by `rho^p`, so
their zero sets cannot select the positive overall normalization.

## Coupling-Angle Separation

For positive supplied traces and couplings, define

```text
A_g = gY^2/(g2^2+gY^2),
A_T = T_2/(T_2+T_Y).
```

Exact subtraction shows `A_g=A_T` if and only if
`gY^2/g2^2=T_2/T_Y`. For the supplied WM1 table this additional ratio is
`3/5`. Equal subgroup couplings instead give `A_g=1/2`, not `3/8`. A separately
declared common law `1/g_i^2=C*T_i` is sufficient, but unequal coefficients
break the equality. The common law is therefore a premise, not a consequence
of the table sum.

## Primary-Literature Premises

WM1 invokes Georgi, Quinn, and Weinberg (1974). The primary paper obtains its
coupling relation in a larger simple-group embedding with a common normalized
generator convention, an embedding-specific charge relation, and a specified
high-scale footing; lower-scale values require running. No accepted framework
claim supplies those premises. The citation cannot convert WM1's quotient into
an accepted physical angle.

## Source Checks

- WM1.0-WM1.5 correctly evaluate the supplied finite table, but do not derive
  its physical identity or a coupling relation.
- WM1.6 is false as stated. The exact perturbation denominator is
  `16/3+2*delta+delta^2`; both `delta=0` and `delta=-2` give `3/8`. The second
  root flips the charged-singlet sign, preserves squared traces, and makes the
  first and third Abelian moments nonzero.
- WM1.7-WM1.8 correctly show sensitivity to two table mutations, not uniqueness
  or anomaly-forced physical content.

M1, W2, SM2, SM3, WM2, and WM3 remain pending. C-GAU-001 explicitly leaves the
Abelian kinetic coefficient and physical charge map unconstrained, while
C-LIE-001 makes trace values convention- and representation-specific.

## Terminal Decision

WM1 maps to C-REP-001's exact finite-table, normalization-covariance, and
conditional coupling-angle ledger. It establishes no physical matter
representation, anomaly derivation, electroweak action, common induction law,
unification group or scale, weak mixing angle, running prediction, observed
value, Standard Model, or substrate realization.
