# Source adjudication: CF1 Abelian-Higgs vortex

## Decision

CF1 is qualified. Its imported radial Abelian-Higgs functional supports exact
`C-VTX-001`, and a reconstructed solver with stronger evidence supports numeric
`C-VTX-002`. CF1 does not establish that this conditional Abelian model is the
substrate vacuum, a dual chromomagnetic condensate, a chromoelectric tube, QCD,
or a confinement mechanism.

## Reproduction boundary

The hash-pinned source currently passes CF1.1 and CF1.1b, then exits at its first
energy quadrature because NumPy removed `np.trapz`. It therefore does not
reproduce its advertised `ALL 8 CHECKS PASS` tally. P026 leaves the predecessor
immutable, uses `np.trapezoid`, and reconstructs all accepted content through
the package and campaign evidence.

## Convention correction

CF1 displays `A_theta=a/r` and an energy gauge term with no `g`, but later states
flux `2*pi*n/g` and vector mass `g*v`. Those general-coupling statements require
one convention: P026 defines `A_theta=a/(g*r)` and gauge energy
`(a'/r)^2/(2*g^2)`. Variation gives
`a''-a'/r+g^2*(n-a)*f^2=0`; CF1's displayed equation is exactly its declared
demo specialization `g=1`. Flux is then consistently `2*pi*n/g`.

## Check-family audit

CF1.1 and CF1.1b are accepted in the corrected convention. P026 varies both
fields directly, independently linearizes the vacuum, and rejects five sign,
friction, and coupling-normalization mutations.

CF1.2 is accepted only as bounded numeric evidence. The reference solve uses
`r in [1e-4,20]`, `(v,n,lambda,g)=(1,1,2,1)`, 120 initial points,
`solve_bvp` tolerance `1e-8`, maximum 100000 nodes, Dirichlet data
`f(eps)=a(eps)=0`, `f(R)=a(R)=1`, and reports maximum RMS collocation residual
below `1.1e-8`. P026 varies tolerance, domain, cutoff, and two structurally
different guesses. A separate central finite-difference nonlinear solve at
101, 201, and 401 points converges toward the collocation tension.

CF1.3 and CF1.3b are exact. For positive vacuum amplitude the angular-energy
log coefficient is `v^2*(n-a_infinity)^2`; finiteness uniquely requires
`a_infinity=n`. The declared physical connection then has flux `2*pi*n/g`.
The ungauged positive-winding coefficient remains nonzero.

CF1.4 is accepted numerically only for the declared family. The reference
tension is approximately `4.21160`; the independent finite-difference values
are `4.19212`, `4.20658`, and `4.21037`. Outer-domain variation from 10 to 25,
inner-cutoff refinement from `1e-2` toward `1e-4`, tolerance refinement, and
matched dimensionless `v=1`/`v=2` domains support finiteness, positivity, and
the `v^2` scaling in this convention. No absolute physical tension is derived.

CF1.5's exact vacuum linearization is accepted: inverse lengths are `g*v` and
`v*sqrt(2*lambda)`. Numeric tail fits are regression evidence against those
exact masses, not an independent derivation and not a “dual Meissner” identity.

CF1.6 overstates its oracle. At `v=0`, `f=0` is one solution and both linearized
inverse lengths vanish, but solving from a trivial guess does not prove
uniqueness of every boundary solution or establish a physical deconfined phase.
Only the exact inverse-length limit is retained.

## Exact qualification

Accepted content is the declared conditional Abelian-Higgs model, exact
variation, finite-energy boundary and flux, linearized inverse lengths, and
resolution-bounded nontrivial BVP/tension evidence for explicit parameters.
Physical duality, substrate/QCD identification, chromoelectric interpretation,
confinement, absolute scale, and v=0 uniqueness remain outside the claim delta.
