# P070 Adjudication of MH1

MH1 reproduces four passing SymPy checks, but its exact overlap arithmetic is
conditional and its generation, Yukawa, condensate, hierarchy, and mass labels
are not constructed by the executable.

## Surviving Source Content

Under whole-line Cartesian `dx`, a normalized mode proportional to
`sech(kappa*x)^2` and a declared matched-width multiplier
`A*sech(kappa*x)` have exact expectation `9*pi*A/32`. The sampled pure-sech
powers one and three likewise give `pi*A/4` and `75*pi*A/256`. A common
external factor cancels from ratios of declared products `y_n*v`. The accepted
negative and zero Hessian eigenvalues remain non-mass objects under C-QBL-003.

## Generalization and Actual-Mode Repair

MH1 claims every `p>=1` after checking only `p=1,2,3`. P070 proves the stronger
exact positive-real-power gamma ratio. More importantly, FG2's actual odd
translation mode is `sech*tanh`, not a pure sech power. Its normalized
squared-density expectation is `3*pi*A/16`; with the even mode the ratio is
`2/3`, and their weighted cross overlap vanishes by parity. These order-one
numbers establish no hierarchy or generation ladder.

## Dimension and Parameter Ceiling

After L2 normalization, the overlap has the dimension of the supplied
multiplier profile. A separately declared product `m=y*v` has the sum of the
two supplied mass dimensions. MH1 declares the product and then differentiates
it, which is not a derivation of an interaction. Its prose fixes
`A=2*sqrt(6)*kappa` while its executable also treats A as independent; either
conditional convention retains an unfixed inverse width or amplitude. The
reciprocal rescaling `y->rho*y`, `v->v/rho` leaves the product unchanged.

## Rejected Physical Readings

No fermion, chirality, interaction term, physical condensate, VEV, generation
assignment, flavor quantum number, hierarchy, mixing matrix, or absolute scale
appears. Rejecting the Hessian eigenvalues as masses does not uniquely select
an overlap functional; many other positive declared functionals exist. Pending
MH2 and MH3 remain unavailable as premises, and Cartesian whole-line formulas
do not transfer automatically to radial measures or mismatched widths.

## Disposition

MH1 is qualified and maps to C-OVL-001 only for its exact p=2 matched-width
ratio, sampled pure-sech fragments, common-scale cancellation, and reuse of
C-QBL-003's mass ceiling. The accepted positive object is independently
completed by P070's general expectation, gamma, actual-mode, dimension, and
rescaling ledgers.
