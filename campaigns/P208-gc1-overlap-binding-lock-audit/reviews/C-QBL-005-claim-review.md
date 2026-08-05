# C-QBL-005 Claim Review

## Decision

C-QBL-005 is recommended for acceptance as a symbolically verified compatible
extension depending on C-QBL-003, C-OVL-001, and C-OVL-002. The accepted object
is a conditional local curvature/coupling composition and its exact
non-implications, not GC1's universal hierarchy no-go.

The proposed statement is:

> Conditional on C-QBL-003's declared quartic whole-line energy, write its
> field potential as V_kappa(f)=kappa^2*f^2/2-f^4/48. For any real field value
> f, V_kappa''(0)-V_kappa''(f)=f^2/4. If, independently, a nonzero real lambda
> and local multiplier c=lambda*f are declared, then the exact conditional
> relation is D=c^2/(4*lambda^2). The multiplier declaration and its
> normalization do not follow from the potential. On C-QBL-001's profile
> f0=sqrt(24)*kappa*sech(kappa*(x-x0)), D=6*kappa^2*sech^2 and the associated
> fluctuation potential has one global minimum at x0. For the actual two
> C-QBL-003 bound-mode shapes and multiplier f0, the C-OVL-001 normalized
> expectations are 9*pi*sqrt(24)*kappa/32 and
> 3*pi*sqrt(24)*kappa/16, with fixed ratio 2/3; both tend to zero as kappa
> tends to zero while the two levels remain below the positive continuum
> threshold for every kappa>0. Thus the local identity neither states that a
> nonzero shallow one-dimensional well has no bound state nor makes small
> absolute overlap and binding contradictory. Independently, C-OVL-002's
> exact Pöschl--Teller ground eigenvalue is negative for every positive well
> depth. Replacing c by a nonlinear or independent multiplier, rescaling its
> lambda, or deforming the potential changes the relation. These statements
> derive no stability, physical condensate or Yukawa interaction, generation,
> mass hierarchy, mixing, multisoliton solution, Standard-Model map, or
> substrate realization.

## Dependency Closure

C-QBL-003 owns the declared quartic energy, exact fluctuation potential,
complete two-level spectrum, continuum threshold, and non-generation ceiling.
C-OVL-001 owns the two normalized multiplier expectations and their supplied
amplitude. C-OVL-002 owns the exact positive-depth Pöschl--Teller ground state
and translated-well isospectrality. C-QBL-001 is already in C-QBL-003's
closure and supplies the profile. No pending GC unit is imported.

The linear local multiplier `c=lambda*f` remains a separate declared premise.
No hidden measured value, fitted threshold, scalar count, generation count,
spacing, physical scale, or stability premise enters the theorem.

## Oracle and Verification Axis

The load-bearing relations are tractable exact identities, so SymPy is the
strongest practical oracle. The primary verifier differentiates the declared
potential, checks the normalized coefficient, substitutes the exact profile,
tests the analytic center, composes the accepted exact overlaps and spectrum,
and evaluates the exact shallow-well ledger. It also audits the source AST and
model boundary. The result is 23 passing primary checks.

The independent verifier does not import the new ledger or accepted overlap
and Pöschl helper APIs. It directly differentiates the potential, evaluates
the whole-line normalized integrals, applies the differential operator to an
arbitrary-positive-index Pöschl eigenfunction, and derives the moment
inequality. It passes nine checks.

Verification is `symbolic_verified`; review is `accepted`; compatibility is
`compatible_extension`; epistemic status is `active`.

## Sensitivity and Counterexamples

The exact identity changes under every preregistered load-bearing mutation.
For `c=lambda*f`, omitting lambda changes the coefficient. For `c=f^2` or an
independent c, the source-normalized residual is nonzero. Adding
`epsilon*f^6` to the potential changes the deficit to
`f^2/4-30*epsilon*f^4`.

The source no-go fails two exact counterexamples. A positive-depth
Pöschl--Teller well has a negative ground eigenvalue for arbitrarily small
depth in one dimension. Within the exact quartic scale family, the accepted
bound levels remain below threshold for every positive kappa while both
declared profile overlaps tend to zero with kappa. The latter does not produce
a hierarchy—the ratio remains 2/3—but it refutes “small absolute coupling and
bound are contradictory.”

## Source Corrections

GC1's pointwise object is `c(x)=f0(x)`, while `y_n` is the integrated
expectation `integral |eta_n|^2*c dx`. The claim does not write `D=y_n^2/4`.
The source's numeric section solves the exact-sine background, for which the
curvature deficit is `(1-cos(f))/2`, differing from `f^2/4` beginning at order
`f^4`; it is not an exact measurement of the quartic identity.

The source's `rms/centroid>=1` predicate is a universal consequence of
`E[|X|^2]>=E[|X|]^2`. It even passes an exactly relocated point density with
equality and therefore cannot diagnose relocation. Eight frequencies and the
source-selected `0.1` and `10` cutoffs remain finite evidence, not an
all-frequency theorem.

## Implementation and Consumers

The pure public APIs `quartic_curvature_deficit` and
`quartic_binding_coupling_ledger`, with the immutable
`QuarticBindingCouplingLedger`, live in `qball_fluctuations.py`. Existing
symbols are unchanged. Focused tests cover exact derivation, normalization,
profile substitution, potential and coupling mutations, invalid scale guards,
the accepted overlap composition, and the translated shallow-well
counterexample.

Direct source consumers GC2 through GC6 may use only this conditional identity
and its explicit ceilings. They may not inherit GC1's rejected universal
no-go, stability window, multisoliton identity, or generation narrative.

## Promotion Gate

Promotion requires the accepted registry entry, v0.151.0 closed release,
generated documentation and framework memory, GC1 corrected qualification,
the 23-check primary route, nine-check independent route, 38-check graph
replay, focused tests, one integrated release boundary, and an empty debt
ledger. A terminal source tally by itself is not a promotion oracle.
