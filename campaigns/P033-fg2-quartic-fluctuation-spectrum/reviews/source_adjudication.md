# Source adjudication: FG2 fluctuation tower

## Decision

FG2 is qualified. Its quartic scalar second variation and complete two-level
Pöschl–Teller spectrum are accepted as `C-QBL-003`. Its exact-sine third level,
stability language, positive-mass ordering, and particle-generation tower are
not accepted.

## Check-family audit

Check 1 correctly differentiates the conditional quartic energy potential and
obtains `L=-d_x^2+kappa^2-6*kappa^2*sech^2(kappa*x)`. P033 rederives the
functional, verifies both eigenfunctions directly, and closes completeness by
the `s=2 -> s=1 -> free` partner factorization rather than importing a spectrum
table.

Checks 2 and 3 reproduce the two finite-box levels and their exact values. The
mesh and box studies are suitable regression evidence because the exact
spectrum is independently known. The even nodeless level has eigenvalue
`-3*kappa^2`; the odd zero level is precisely the translation derivative.
Both are square-integrable and the continuum begins at `kappa^2`.

Check 4's exact-sine third level is not reliable. Its background is obtained by
long forward shooting on a homoclinic separatrix. At the declared
`omega=0.45` and wall `28/kappa`, the field first falls below `3e-6` and then
grows back to about `0.29` at the wall. Thus the potential does not approach
the declared vacuum boundary on that box. The reported third eigenvalue is
only about `0.0042` below threshold, and FG2 refines mesh but not box size for
this calculation. Neither the count nor the claimed drop near the quartic
limit is established.

Check 5 orders raw Hessian eigenvalues and calls them masses. A negative
eigenvalue and a symmetry zero mode are not a strictly positive particle-mass
hierarchy. The source constructs no quantized states, common Standard-Model
quantum numbers, Yukawa map, or identification of the collective translation
coordinate as a generation.

Checks 6 and 7 correctly show that shallow and flat comparison wells have
fewer bound levels. They validate the generic eigencount machinery but do not
supply the missing particle map or repair the exact-sine boundary.

## Exact qualification

Accepted content is the conditional quartic energy, scalar Hessian, complete
two-mode bound spectrum, eigenfunctions, parity, translation identity, and
continuum threshold. The negative mode is an unconstrained scalar-Hessian
fact; the full complex phase/charge-constrained operator and VK hypotheses are
not present, so Q-ball stability remains unproved. Exact-sine mode counts,
positive masses, particle families, flavor generations, quantum numbers,
physical ratios, and substrate identity remain outside the claim delta.
