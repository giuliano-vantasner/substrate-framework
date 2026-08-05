# P172 KI2 source adjudication

## Decision

KI2 is qualified. Its exact dimension solve, dimension-kernel basis, local
ratio identity, and freedom of that ratio across the accepted positive
`lambda,mu` parameter family survive. Its headline fixed-theory symmetry and
“underdetermined in principle by every present or future derived quantity”
claim are false.

No physical epsilon value, accepted identification with C-BPS-003, new claim,
new API, or release follows.

## Reproduction and oracle scope

The hash-pinned source imports only SymPy and executes all six local predicates.
That tally is incomplete as a headline oracle: KI2.3 checks a dictionary of six
expressions chosen to contain neither `lambda` nor `mu`. It does not transform
the accepted BPS energy density, Bogomolny square, saturation residual, or
bound.

The primary verifier passes 45 checks. A fresh independent derivation that
imports neither KI2 nor the primary verifier passes 21. The twelve-node typed
source graph passes 59 checks while preserving KI1's expected governed failure.
The pinned Lean capstone exits cleanly, but its exact theorem encodes only
`epsilon -> epsilon/t^2` and invariance of `derivedScale := F/e`; it contains no
BPS energy object.

## Predicate decisions

KI2.1 is a valid conditional natural-unit dimension solve. Requiring the
declared L2, L4, L6, and L0 terms to have density dimension four yields the
unique tuple `[F_pi,e,lambda,mu]=[1,0,-1,2]`. This selects no parameter value.

KI2.2 is only partly valid. `lambda*mu` and `F_pi/e` both have energy dimension,
and the locally defined ratio depends on both BPS inputs. Equal dimension does
not prove physical independence: `lambda*mu=c*F_pi/e` is dimensionally allowed.
Moreover, `c_epsilon*(F_pi/e)/(lambda*mu)` has the same dimension for every
dimensionless normalization `c_epsilon`. KI2 supplies neither that
normalization nor a map to C-BPS-003's abstract expansion coordinate.

KI2.3 is refuted in its advertised form. Under the source flow
`lambda -> t*lambda`, `mu -> t*mu`, C-BPS-001's energy density and square scale
by `t^2`, its saturation residual scales by `t`, and its bound scales by `t^2`.
Thus the flow changes a fixed accepted BPS theory. It connects different
members of an allowed theory family and cannot be a symmetry of the complete
fixed-theory content. A finite registry also cannot prove a statement about
every future quantity.

KI2.4 is exact local algebra. The vectors for `e`, `lambda*F_pi`, and
`mu/F_pi^2` form a basis of the dimension-row kernel, and their reciprocal
product is the source's locally defined ratio. This establishes neither values
nor physical identifiability.

KI2.5 survives only as a parameter-family statement. With `F_pi,e` fixed and
positive, every positive target ratio is realized by a positive choice such as
`lambda=F_pi/(e*mu*target)`. The corresponding BPS energy and bound change, so
these are distinct theories.

KI2.6 is a valid substitution guard but its sharpness prose is too strong.
Supplying all four values makes the local definition numeric, yet one need not
import `lambda` and `mu` individually: a relation fixing their product already
fixes the ratio.

## Dependency and consumer decision

Refuted KI1 cannot support the all-content premise. Pending MK1, MK2, and MK3
are counterrelations only and select no accepted coupling or epsilon value.
Accepted C-BPS-001 supplies the positive parameter family and the decisive
fixed-theory counterexample. C-SK-001 supplies only a conditional standard
scale. C-BPS-003 deliberately keeps epsilon abstract and is not silently
identified with KI2's expression.

KI3 and KI4 may consume the positive-family surjectivity only with its local
definition and family-of-theories type; they may not inherit the rejected
fixed-theory symmetry. Their own claims remain pending. An untracked Phase-47
BM11 file is absent from the governed source commit and excluded from authority.

## Nonduplication and implementation

The surviving family freedom is already implicit in C-BPS-001's arbitrary
positive inputs, and the conditional standard scale is already C-SK-001. A
generic parameter-orbit API has no accepted consumer, while encoding the
source flow as a symmetry would encode a false statement. The canonical BPS
API therefore remains unchanged.

## Four-axis review

- Verification: exact symbolic and counterexample evidence for the qualified
  parts; exact refutation of the fixed-theory symmetry.
- Review: audited and qualified at source-unit level; no source sentence is
  promoted wholesale.
- Compatibility: compatible with accepted claims only as a family statement;
  conflict for the fixed-theory headline.
- Epistemic: qualified source evidence, with no new active accepted claim.

## Closure

P172 changes only campaign, disposition, queue, review-memory, and parent-effort
records. The accepted set remains 163 claims and the current release remains
v0.127.0. No generated accepted documentation changes.
