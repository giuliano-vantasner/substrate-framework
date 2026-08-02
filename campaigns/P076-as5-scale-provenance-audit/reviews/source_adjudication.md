# P076 Source Adjudication: AS5

AS5 is qualified. Its target-span algebra survives, but its claim to generate
an absolute dimensionful scale from dimensionless content does not.

## Reproduction

The hash-pinned source exits cleanly and prints `ALL 6 CHECKS PASS`. It uses
exact SymPy algebra and no numerical integration or NumPy quadrature alias.
That tally is source behavior, not evidence that its semantic headlines were
tested.

## Dimension-Target Audit

In M,L,T row order, the columns `c=(0,1,-1)` and
`hbar=(1,2,-1)` have rank two. Appending the pure-length target `(0,1,0)`
raises augmented rank to three, so no monomial in `c` and `hbar` has length
dimension. Adjoining `a=(0,1,0)` produces the unique powers `(0,0,1)`: the
calculation simply selects the supplied target primitive. It derives neither
its magnitude nor its physical provenance.

AS5's G discussion does not use its computed span variables in the verdict.
Because `c,hbar,a` span M,L,T, the dimension of G is in their span with powers
`(3,-1,2)`, consistently with C-GRV-001. The displayed Planck expression does
contain a G value, but symbol occurrence is not a provenance oracle.

## Reference-Scale Audit

The source formula is `Lambda=mu0*exp(-X)`. The dimensionful reference `mu0`
is explicit, and its inverse-energy length additionally retains the supplied
conversion `hbar*c0`. At fixed dimensionless flow inputs, replacing `mu0` by
`rho*mu0` replaces Lambda by `rho*Lambda` and the inverse length by its value
divided by rho. Only the ratio `Lambda/mu0` is reference independent.

Conversely, any positive target Lambda is reproduced by choosing
`mu0=Lambda_target*exp(X)`, and any positive inverse-energy target length is
reproduced by choosing `mu0=K*exp(X)/a_target`. Those exact inverse families
make the target a load-bearing input. They establish conditional
reparameterization, not a parameter-free absolute prediction.

## Oracle and Orientation Audit

AS5.1 excludes only `a` and `G` from Lambda. The same predicate accepts the
nontransmutation mutant `mu0*b0*beta2`, so it does not check the exponential
mechanism or absence of a dimensionful boundary. AS5.0 checks only that `a`
and `beta2` remain symbolic and cannot detect a fitted or imported `mu0`.

AS5.5 checks symbol absence and accepts either exponential sign. Under AS1's
executable inverse-energy assignments the lower transmuted energy gives the
longer length, so `a/xi=exp(+X)`. AS5 instead labels `exp(-X)` as `a/xi`. Its
own predicate cannot detect the reciprocal error.

## Unit-Coordinate Audit

For a fixed positive quantity `Q=N*u`, replacing the unit standard by
`u'=rho*u` changes the numeric coordinate to `N'=N/rho` and reconstructs the
same Q. This is coordinate covariance. It neither creates Q nor chooses its
physical magnitude. Calling a supplied dimensionful observation a mere units
choice therefore does not resolve the absolute-scale boundary.

## Terminal Decision

AS5 maps to C-DIM-002, C-RGE-001, C-RGE-003, C-IDN-001, and the new
C-DIM-008 provenance ledger. It does not establish a dimensionless-only
absolute scale, physical QCD transmutation, a beta coefficient or coupling,
an Angstrom or Planck comparator, lattice or soliton scales, or expiry of the
framework's absolute-scale deferral. Later AS6 and operating-point narratives
remain outside the accepted dependency closure.
