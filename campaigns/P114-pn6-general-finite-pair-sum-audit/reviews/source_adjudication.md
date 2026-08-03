# PN6 source adjudication

PN6 reproduces all thirty runtime predicates and its equal-product pair and
finite-sum formulas are exact. The surviving statement is

`-i*Gamma*sum_j(c_j/(Delta_j^2+Gamma^2/4))`

for finite symmetric pairs with a common shift and equal products inside each
pair. This is a block-diagonal corollary of accepted C-RES-001, not a distinct
claim or API.

The source's positive-loss headline needs a missing premise. For real
nonnegative products `c_j=g_j^2`, common `Gamma>0`, and real nonzero
detunings, the sum is strictly negative imaginary exactly when at least one
product is positive. All-zero couplings refute unrestricted strictness. Signed
or complex products can cancel, including equal detunings with products `1`
and `-1`. A complex coupling square `g^2` is not interchangeable with the
Hermitian product `conjugate(g)*g`.

At zero loss an individual pair cancels exactly when its two complex products
match. A full sum can cancel across pairs even when neither pair cancels. If
each pair shares its own positive loss, nonuniform pair losses preserve the
negative-imaginary sign for nonnegative products; unequal shifts inside a
pair break the simple common-phase identity.

The finite sum has exact small-loss coefficient
`-i*sum_j(c_j/Delta_j^2)` and large-loss coefficient
`-4i*sum_j(c_j)`. Its positive-loss stationary equation is the sum of the
pair derivatives. Unequal detunings do not inherit either one-pair optimum.
Adding finite pairs changes the model; fixed-per-pair and fixed-total product
normalizations are distinct and neither is numerical refinement.

The uniform-ladder digamma base and recurrence are exact but specialized. The
seven floating-point block sizes are regression of an exact diagonal inverse.
The named arXiv v2 record contains no explicit retraction wording supporting
PN6's stronger narrative. No microscopic bath, open-system dynamics, physical
loss, exchange channel, probability, rate, nuclear or phonon mechanism,
material magnitude, or observation follows.

Every predicate is individually classified in `evidence/check-adjudication.yaml`.
The queue has no PN6 consumer. The terminal disposition is qualified through
C-RES-001 with release v0.94.0 unchanged.
