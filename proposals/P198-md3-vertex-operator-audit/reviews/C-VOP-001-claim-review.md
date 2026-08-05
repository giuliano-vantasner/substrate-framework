# C-VOP-001 Claim Review

## Exact Proposed Statement

On C-OSC-001's standard one-mode Fock space, let `alpha` be a separately
declared complex number, let `S=conjugate(alpha)*alpha`, and define the
norm-convergent vector

`|alpha> = exp(-S/2) sum_{n>=0} alpha^n/sqrt(n!) |n>`.

It is normalized, obeys `a|alpha>=alpha|alpha>`, and has overlap
`<alpha|beta>=exp(-(S_alpha+S_beta)/2+conjugate(alpha)*beta)`. A number-basis
measurement on this declared state has exact Born probability
`p_alpha(n)=exp(-S)S^n/n!`, with mean and variance `S`. Zero displacement has
only vacuum support; nonzero displacement gives positive probability at every
nonnegative occupation. C-CMB-003 supplies the complete factorial-one mode and
tail results, including both adjacent modes `S-1,S` when positive `S` is an
integer. In the standard Weyl representation, the conditional identification
`D(alpha)=exp(alpha*a_dagger-conjugate(alpha)*a)` gives this vector from the
vacuum; for real `lambda` and `alpha=i*lambda`, the generator is
`i*lambda*(a+a_dagger)`.

The number probability concerns the declared state and number observable. It
does not prepare or quantize the accepted classical medium, identify `S` with
a classical peak, RMS phase, or material variance, change the minima of a
cosine potential, derive a Huang-Rhys or Franck-Condon material model, import
PN2's external band, or supply a transition, branching, reaction, or rate.

## Dependency Closure and Natural Fit

The proposed dependencies are C-OSC-001 and C-CMB-003. C-OSC-001 owns the
standard one-mode basis and ladder recurrence; C-CMB-003 owns the normalized
factorial-one mass, moments, complete modes, and tails. C-SG-019 and C-OSC-002
are comparison ceilings keeping classical cosine and amplitude conventions
separate. C-SPN-002 is a distinct finite collective ladder. PN2 has no accepted
mapping and supplies no premise.

The claim is additive. It changes no existing symbol, signature, value,
normalization, or classical-medium invariant. Its novelty is the normalized
state amplitude, annihilation eigenvector, overlap, and Born semantics—not a
duplicate formula for the already accepted mathematical mass.

## Verification and Sensitivity

The primary route passes 48 exact checks through the canonical API. The
independent route imports no coherent-state API and passes 25 raw coefficient,
series, recurrence, PGF, overlap, mode-tie, and compact-multiplier checks. The
22 new package tests pass together with 37 accepted Fock and factorial-one
tests.

Removing the Gaussian half factor changes the norm to `exp(S)`. Replacing
`sqrt(n!)` by `n!` breaks the annihilation recurrence. Erasing conjugation from
the Weyl generator breaks anti-Hermiticity for complex displacement. Treating
a finite truncation's interior commutator as globally central fails through its
top-edge nested commutator. Selecting only `floor(S)` fails the positive-integer
mode tie. A compact multiplication vertex preserves pointwise density and
therefore breaks the inference from generic “vertex” language to coherent
occupation or new classical vacua.

## Source and Consumer Audit

MD3's 41 checks reproduce with exit zero and no NumPy compatibility surface.
The source's infinite-Fock formula is correct, but its finite matrix does not
prove global BCH, its weight helper inserts the normal-ordered coefficient
without exponentiating the matrix, and its integer mode label is incomplete.
The ten-node graph covers 372 native checks with hashes and compatibility
surfaces replayed; MD4, MD5, and MD6 remain pending and inherit no blanket
authority.

## Four-Axis Recommendation

- Verification: symbolic verified.
- Review: accept after the promotion transaction and integrated gate.
- Compatibility: compatible extension.
- Epistemic: active conditional theorem, with every physical realization left unclaimed.

## Promotion Delta

Promotion adds C-VOP-001, the importable coherent-state module and tests, an
immutable P198 campaign, a pinned release, generated documentation and
accepted memory, and a qualified MD3 disposition with a regenerated migration
queue. It does not change C-OSC-001, C-CMB-003, the accepted classical medium,
or any pending consumer.
