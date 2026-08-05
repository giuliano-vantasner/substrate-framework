# C-BRN-002 Claim Review

## Exact Proposed Statement

Let `N>0` be a continuous population parameter, let `rho>0` be a declared
dimensionless ratio of two common-dimension positive rate normalizations, and
let `w(N)>0` be a differentiable dimensionless weight. For the comparison
fraction

`B_c(N)=rho/(N*w(N)+rho)`,

the exact total derivative is

`B_c'(N)=-rho*(w(N)+N*w'(N))/(N*w(N)+rho)^2`.

Because the other factors have fixed positive sign, `B_c` is locally
decreasing, stationary, or increasing exactly as `w+N*w'` is positive, zero,
or negative. A constant positive weight gives the C-BRN-001 specialization
`B_c'=-rho*w/(N*w+rho)^2<0`. Positive weight alone is insufficient:
`w=N^(-1/2)`, `w=N^(-1)`, and `w=N^(-2)` produce the three respective
verdicts.

The theorem is about a declared differentiable continuation. If `N` denotes
only integer counts, the derivative is not silently imported; discrete
monotonicity instead follows from the ordering of `N*w(N)` at adjacent
integers. The caller remains responsible for deriving the weight law, common
rate dimensions, exhaustive channel set, and physical meaning of the inputs.
The theorem supplies no material population law, state preparation,
interaction, isotope map, reaction, branching observable, or rate.

## Dependency Closure and Natural Fit

The proposed accepted dependency is C-BRN-001, which owns the exact normalized
two-input allocation and its physical ceilings. C-BRN-002 changes only the
constant-weight partial derivative into the correct total derivative for a
separately supplied `w(N)`. C-CMB-003 is static composition context for MD5's
factorial-one examples, not a dependency of the derivative theorem.

P193 previously reserved the same identifier for a possible order-resolved
WN5 claim and rejected that proposed surface as duplicate accepted
composition. It never entered the accepted registry. P200 freezes and reviews
a different statement: the general `w+N*w'` necessity-and-sufficiency
criterion, which neither C-BRN-001 nor the WN5 composition owns.

The claim is additive. It changes no existing allocation result, signature,
normalization, convention, or accepted value. Its API explicitly returns the
derivative control, total derivative, trichotomy, and the two physical-premise
ceilings.

## Verification and Sensitivity

The primary verifier passes 19 exact API, source-AST, chain-rule,
specialization, sign-trichotomy, mode, premise, and mutation checks. The
independent route imports no claim API and passes 12 direct SymPy function
differentiation, inverse-power, static-mass, and isotope-ceiling checks. All 21
focused branching tests pass.

Removing the `N*w'` term makes the slow, inverse, and faster-inverse weight
families indistinguishable and is caught by the coefficient mutation. The
positive counterexample `w=N^(-2)` makes the comparison fraction increase;
`w=N^(-1)` supplies the exact stationary boundary. An undecidable symbolic
control sign is rejected rather than assigned a verdict. Exact inputs are
required, so floating approximations cannot manufacture sign evidence.

## Source and Consumer Audit

MD5's 63 native predicates reproduce with exit zero and no NumPy compatibility
surface. Its constant-weight derivative, positive factorial-one membership,
and conditional rearrangements are valid only under their declared premises.
The source does not test a population-dependent weight. Omitting `N` from a
selected expression is not a derivation of the material map, and positive
integer factorial-one intensity has two adjacent modes rather than one.

The ten-node graph covers 354 native predicates with source and record hashes,
exact dependency mappings, compatibility surfaces, and no duplicate native
execution. MD6 remains pending and inherits no blanket authority.

## Four-Axis Recommendation

- Verification: symbolic verified.
- Review: accept after the promotion transaction and integrated gate.
- Compatibility: compatible extension.
- Epistemic: active conditional theorem, with every physical realization left unclaimed.

## Promotion Delta

Promotion adds C-BRN-002, the importable branching API and tests, an immutable
P200 campaign, a pinned release, generated documentation and accepted memory,
and a qualified MD5 disposition. It does not change C-BRN-001, C-CMB-003, any
accepted material claim, or pending MD6.
