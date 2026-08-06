# C-MIX-003 Claim Review

## Decision

C-MIX-003 is recommended for acceptance as a symbolically verified compatible
extension depending on C-MIX-001 and C-MIX-002. The accepted object is a
conditional finite-matrix null theorem with explicit degeneracy caveats, not
GC3's universal condensate or physical CP headline.

The proposed statement is:

> Let `R_a` be finite real matrices with a common row dimension N, let
> `theta_a` be real scalars, and set `Y_a=exp(i*theta_a)*R_a` for `a=1,2`.
> Each left Gram is `H_a=Y_a*Y_a^dagger=R_a*R_a^T` and each right Gram is
> `Y_a^dagger*Y_a=R_a^T*R_a`; both are real symmetric positive semidefinite
> and independent of the phases. Real orthogonal matrices `O_a` may be chosen
> to diagonalize the left Grams, so `V=O_1^T*O_2` is real orthogonal and every
> quartet `V_ij*V_kl*conjugate(V_il)*conjugate(V_kj)` has zero imaginary part.
> The commutator `[H_1,H_2]` is real antisymmetric, every odd-power trace
> vanishes, and its determinant vanishes when N is odd. Repeated Gram
> eigenvalues retain enlarged unitary basis freedom: arbitrary complex bases
> inside degenerate subspaces can display nonzero coordinate quartets even
> though a real representative and the commutator null identities remain.
> The hypothesis is the globally phased real matrix form itself; a scalar
> field or condensate label does not enforce real coupling matrices, real
> modes, or a spatially constant phase. These statements establish no Yukawa
> interaction, CKM matrix, physical CP operation or violation, condensate
> ontology, generation count, observed phase, Standard-Model map, or substrate
> realization.

## Dependency Closure

C-MIX-001 owns finite SVD, Gram spectra, noncanonical singular bases, and
relative-basis conventions. C-MIX-002 owns the diagonal-rephasing-invariant
quartet and warns that degenerate spectra have larger basis freedom. C-MIX-003
adds only the exact globally-phased-real composition and its invariant null
consequences. No Q-ball, overlap, Yukawa, generation, observed value, pending
GC unit, or external physical theorem enters the accepted dependency closure.

## Oracle and Verification Axis

The load-bearing statements are exact finite algebra, so SymPy is the
strongest practical oracle. The primary route proves both rectangular Grams,
generic symbolic commutator identities, all-real quartets, exact Fourier
countermodels, dimension mutations, and source provenance in 42 checks. The
independent route imports no new canonical module; it rederives the quadratic
form, uses fresh rational orthogonal bases, and rebuilds the exact Fourier and
degeneracy countermodels in 27 checks.

Verification is `symbolic_verified`; review is `accepted`; compatibility is
`compatible_extension`; epistemic status is `active`.

## Sensitivity and Counterexamples

Changing either harmless scalar global phase leaves both Grams fixed. Adding
entrywise or spatial phase structure makes the Gram complex when the real
source components do not commute. Multiplying one scalar global factor by an
independent complex coupling matrix also retains a complex Gram and exact
nonzero quartet, proving that the physical label alone cannot replace the
matrix premise.

At N=3 a complex symmetric Fourier-Takagi matrix decomposes exactly into two
real symmetric source matrices at phases zero and pi/2. This shows that source
count K and matrix dimension N must remain separate and that K=2 can already
realize the one-dimensional generic phase slot. An identity Gram accepts a
complex Fourier eigenbasis with a nonzero coordinate quartet, showing why the
degeneracy caveat is load bearing.

## Implementation and Consumers

The pure public APIs `common_phase_grams`, `real_gram_relative_basis`, and
`odd_antisymmetric_trace`, with immutable result ledgers, live in
`common_phase_matrices.py`. They execute no simulation or print on import.
Existing C-MIX APIs remain unchanged. Numeric odd-trace regressions use
scale-relative residuals; the exact verdict comes from the symbolic routes.

Direct consumers are the focused tests and P210 verifier. Pending GC4 through
GC6 may use only the conditional matrix theorem and explicit ceilings, not a
condensate ontology, three-source count, stability result, or physical CP
mechanism.

## Promotion Gate

Promotion requires the accepted registry entry, v0.152.0 closed release,
generated documentation and framework memory, GC3 corrected qualification,
the 42-check primary route, 27-check independent route, 13-node graph replay,
focused tests, one integrated release boundary, and an empty debt ledger. The
source's nine-check tally and random ensemble are not promotion oracles.
