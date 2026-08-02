# P079 Source Adjudication: AS8

AS8 is qualified. Its neutral exponential limit and raw-amplitude rescaling
algebra survive, but it does not derive a quantum actualization mechanism,
observable absolute amplitude scale, or shared Planck-like granularity.

## Reproduction

The hash-pinned source exits cleanly and prints `ALL 5 CHECKS PASS`. The exact
limit and rescaling expressions reproduce, as do the selected `S=3` and
`S=75` examples. This campaign uses exact symbolic algebra and neither
`np.trapz` nor `np.trapezoid`.

## Continuous Fixation Family

For a separately supplied initial frequency `x in [0,1]` and real selection
ratio `S`, define

```text
U(x,S) = (1-exp(-S*x))/(1-exp(-S))  for S != 0,
U(x,0) = x.
```

The second line is the unique continuous extension. For nonzero `S`, the
frequency derivative is `S*exp(-S*x)/(1-exp(-S))`, which is positive. Hence
the absorbing endpoint values `U(0,S)=0` and `U(1,S)=1` imply
`0<=U<=1`. The exact complement identity is
`U(x,S)+U(1-x,-S)=1`.

For `0<x<1`, differentiation in `S` factors through
`(1-x)+x*exp(S)-exp(S*x)`. Strict convexity of the exponential makes this gap
positive for every nonzero `S`, so `U` is strictly increasing in `S`. Its
selection limits are zero and one. Thus any supplied interior target
probability has one implicit `S` preimage; fitting that target is inverse
inference, not prediction. Near neutrality,

```text
U = x + S*x*(1-x)/2
      + S^2*x*(1-x)*(1-2*x)/12
      - S^3*x^2*(1-x)^2/24 + O(S^4).
```

The sign of the leading deviation is the sign of `S` in the interior. AS8
declares its symbolic `S` positive and does not audit the full real family.

## Conditional Boundary-Value Derivation

For `S != 0`, the same expression is the unique solution of the separately
declared equation `U_xx+S*U_x=0` with absorbing boundary values zero and one.
The two-constant boundary matrix has determinant `exp(-S)-1`, which is nonzero
for real nonzero `S`. At `S=0`, the equation becomes `U_xx=0` and the same
boundaries give `U=x`. Mutating the generator coefficient from `S` to `2*S`
breaks the nonzero-branch residual.

This is a conditional BVP theorem. AS8 supplies no backward generator,
population convention, diffusion coefficient, microscopic noise law, or
derivation distinguishing a Wright--Fisher convention from a Moran one.

## Normalization and Scale Audit

For positive intensities `I1,I2`, write `N=I1+I2`,
`x=I1/N`, and normalized contrast `2*x-1`. The raw contrast is
`I1-I2=N*(2*x-1)`. A declared coordinate `S=kappa*(I1-I2)` therefore contains
both total normalization and the coefficient convention.

Common amplitude rescaling by `lambda` multiplies both intensities, `N`, raw
contrast, and fixed-`kappa` `S` by `lambda^2`, while leaving `x` invariant.
But the coefficient transformation `kappa->kappa/lambda^2` preserves `S`.
Likewise, unit-normalizing the intensities preserves the same `S` when the
normalized coefficient is `kappa_unit=kappa*N`. The algebra cannot decide
whether raw norm, `kappa`, or a particular joint convention is observable.

AS8's examples `(A1,A2)=(2,1)` and `(10,5)` have squared-amplitude totals 5
and 125. Both unit-normalize to intensities `(4/5,1/5)`. The source inserts
`S=3` and `S=75` directly and uses its symbolic `S_expr` only in the earlier
lambda-rescaling calculation. It never derives those values from `Gamma`,
`c_P`, `N_cap`, or `Theta_eff`.

## Source Checks

- AS8.1 proves the neutral limit, not its identification with the Born
  postulate or quantum measurement.
- AS8.2 proves fixed-coefficient raw-coordinate scaling, not an observable
  absolute scale.
- AS8.3 reproduces two unnormalized examples with an inserted coefficient.
- AS8.4 is the direct consequence of subtracting `x` from AS8.1 and supplies
  no independent oracle.
- AS8.5 defines `Theta_form=hbar_med*omega`, substitutes
  `hbar_med=hbar`, and checks the resulting tautology. AST audit finds no
  executable load of `Theta_eff` or cutoff `a`.

No accepted claim supplies a quantum state space, Born postulate, measurement,
collapse, actualization, fixation process, medium action quantum, or empirical
deviation. C-IDN-002 explicitly accepted no Planck or granularity result from
AS7, and pending S3 supplies no authority.

## Terminal Decision

AS8 maps to C-PRB-001's exact conditional fixation, BVP, bias, inverse-target,
and normalization-covariance ledger. C-U1-002, C-OVL-001, C-DIM-008, and
C-IDN-002 supply source-specific interpretation ceilings only. AS8 establishes
no quantum Born derivation, super-Born actualization law, physical stochastic
process, observable raw-amplitude scale, parameter value, action quantum,
cutoff, dimensional instability, or shared substrate granularity.
