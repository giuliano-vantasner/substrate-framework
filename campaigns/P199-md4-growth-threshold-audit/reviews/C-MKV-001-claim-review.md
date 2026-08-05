# C-MKV-001 Claim Review

## Exact Proposed Statement

Let `N_t` be a separately declared continuous-time Markov chain on the
nonnegative integers. Let `S>0` be a dimensionless stationary mean and let
`r>0` have inverse-time units. For rates

`lambda_n=r*S` and `mu_n=r*n`, with `mu_0=0`,

the exact generator is

`L f(n)=r*S*(f(n+1)-f(n))+r*n*(f(n-1)-f(n))`.

The normalized factorial-one mass
`pi_n=exp(-S)*S^n/n!` is reversible because
`pi_n*lambda_n=pi_(n+1)*mu_(n+1)`. The identity-function local drift is
`L n=r*(S-n)`. For a separately declared initial law with finite mean `m0`,
the mean is `S+(m0-S)*exp(-r*t)`. If its probability generating function is
`G0`, then

`G(z,t)=G0(1+(z-1)*exp(-r*t))*exp(S*(z-1)*(1-exp(-r*t)))`.

For deterministic initial state `n0`, this is the law of the independent sum
`Binomial(n0,exp(-r*t))+Poisson(S*(1-exp(-r*t)))`, which supplies the exact
transition kernel.

The stationary law alone does not select these dynamics. Detailed balance
fixes only `lambda_n/mu_(n+1)=S/(n+1)`. The distinct rates
`lambda_n=r*S/(n+1)` and `mu_n=r` for positive `n`, with `mu_0=0`, have the same
stationary mass but different holding rates, drift, and transients. A positive
local drift does not imply monotone sample paths because death jumps remain
possible at every positive state.

This theorem begins only after the state space, generator, initial law, `S`,
and `r` are declared. It does not infer them from a static factorial-one mass,
a coherent-state number measurement, a continuum mode count, a vacuum
variance, or a material medium. It supplies no state preparation, granularity
map, participation law, physical growth, open or rescued channel, transition
matrix element, branching fraction, isotope effect, reaction, or rate.

## Dependency Closure and Natural Fit

The proposed accepted dependency is C-CMB-003, which owns the normalized
all-nonnegative factorial-one mass and its adjacent ratio. C-OSC-001 and
C-VOP-001 are state-space and one-time measurement context only; they do not
supply a time process. C-DOS-001, C-QFL-001, the accepted medium, lattice, and
cosine claims are nondynamical comparison ceilings. PN2 has no accepted
mapping.

The claim is additive. It changes no existing symbol, signature, value,
normalization, or medium invariant. Its novelty is the explicit positive
generator, boundary, time scale, PGF, transition kernel, and constructive
nonuniqueness result—not another wrapper around the accepted static mass.

## Verification and Sensitivity

The primary route passes 54 exact API, source-AST, detailed-balance, PGF,
transition, competitor, and interpretation checks. The independent route
imports no claim API and passes 37 raw stationary-current, forward-equation,
moment, convolution, nonuniqueness, and mutation checks. The 25 new package
tests pass with 28 accepted bosonic/factorial-one dependency tests.

Replacing `n+1` by `n` leaves nonzero stationary current. Giving state zero a
positive death rate creates uncompensated probability outflow from the
declared state space. Replacing `r*n` by a constant changes the selected
generator. Changing `r` changes transients without changing the stationary
mass. The explicit alternative generator has the same adjacent stationary
ratio but a different local drift and holding rate. At a state below `S`, the
selected process has both positive drift and positive death rate, directly
rejecting monotone sample-path growth.

## Source and Consumer Audit

MD4's 34 native checks reproduce with exit zero and no NumPy compatibility
surface. Its conditional threshold rearrangement and static point-mass samples
are arithmetically correct, but accepted dependencies do not supply its
material parameter map. One discrimination predicate is literally `True`,
the WN6 comparator is hard-coded, and a point mass does not establish an open
channel or event rate.

The eleven-node graph covers 347 native checks with hashes and compatibility
surfaces replayed and no duplicate native execution. MD5 and MD6 remain
pending and inherit no blanket authority.

## Four-Axis Recommendation

The claim-level recommendation is as follows.

- Verification: symbolic verified.
- Review: accept after the promotion transaction and integrated gate.
- Compatibility: compatible extension.
- Epistemic: active conditional theorem, with every physical realization left unclaimed.

## Promotion Delta

Promotion adds C-MKV-001, the importable birth-death module and tests, an
immutable P199 campaign, a pinned release, generated documentation and
accepted memory, and a qualified MD4 disposition with a regenerated migration
queue. It does not change C-CMB-003, C-VOP-001, the accepted classical medium,
or either pending consumer.
