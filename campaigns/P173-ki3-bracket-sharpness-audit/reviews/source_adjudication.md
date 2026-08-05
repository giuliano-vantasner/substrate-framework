# KI3 source adjudication

## Verdict

KI3 is qualified. Its four explicit functions are exact monotone witnesses with
range `(0, kappa_cl)`, and their distinct exact inverses demonstrate that two
endpoint values do not select an inverse function. The universal headline that
`[0, kappa_cl]` is the framework's exact attainable set is not established.

No new accepted claim, canonical API, or release follows. C-XOV-001 already
owns the valid strictly-monotone range theorem under explicit global premises.

## Claim-level findings

KI3.1 verifies the endpoints and nonzero linear terms of four chosen formulas.
Those formulas are not derived from E3 and E4. C-BPS-003 expressly supplies no
global interpolation and permits a positive, zero, or negative first-order
coefficient. C-RDIFF-002's corrected 8.4824 coordinate is conditional numeric
evidence and expressly not a variational bound or BPS limit; KI3 instead
recomputes the stale 8.4563 source value.

KI3.2 is exact for each chosen formula after full differentiation and inversion.
The source oracle itself samples the derivative only at `epsilon=1/2` and solves
only `kappa=kappa_cl/3`. A continuous rational counterexample

`g(epsilon) = epsilon(epsilon+5)/(epsilon+1)^2`

has the same limits zero and one and a positive derivative at the sampled point,
but its derivative becomes negative after `epsilon=5/3`.

KI3.3 overgeneralizes. The counterexample reaches `3/2` at `epsilon=1` and the
level `6/5` at the two positive values `(13-sqrt(145))/2` and
`(13+sqrt(145))/2`. Changing the bump sign produces `-1/2` at `epsilon=1` while
retaining both endpoint limits. Continuity plus endpoint limits therefore gives
interior inclusion by the intermediate value theorem, not range equality,
outside exclusion, or uniqueness. KI3's comment declares codomain
`(0,kappa_cl)` before the check, so its no-overshoot result is also assumed in
the class definition. Because the executable domain is strictly positive and
the four formulas only approach both endpoints, even their exact ranges are
open rather than the closed headline bracket.

KI3.4 contains a valid comparator-free logical witness: at normalized level
`1/2`, the four inverse values are `1`, `log(2)`, `atanh(1/2)`, and
`1/sqrt(3)`, all distinct. This proves only that the stated endpoints do not
select a function or inverse. It does not establish that any witness is a
physical BPS-to-classical map. The native predicate unnecessarily uses 0.929;
that value feeds `ratio`, the back-solves, `spread`, and the pass threshold
`spread > 1.05`. Moving only the comparator level to `1/10000` flips the
threshold verdict.

KI3.5 correctly observes that the local classical expression and four endpoint
calculations do not use the comparator. It incorrectly says no derived result
changes if the comparator block is deleted: KI3.4 cannot execute without it and
its threshold verdict is comparator-sensitive.

## Formal and consumer scope

The unchanged Lean file compiled cleanly in P172 and remains hash-identical. Its
`kappa_surjective` theorem quantifies over `K` and `y` for the one definition
`kappa K e = K*e/(1+e)`. It does not quantify over arbitrary continuous maps or
encode endpoint provenance, a global bound, closed endpoints, or a physical
epsilon identification. Recompilation was intentionally not repeated.

KI4 consumes KI3's whole-open-bracket prior and must be audited without treating
that prior as authority. MK4 and MK5 are pending challenges, while MK6 and MR6
propagate their narrative; chronology and passing local scripts do not promote
them.
