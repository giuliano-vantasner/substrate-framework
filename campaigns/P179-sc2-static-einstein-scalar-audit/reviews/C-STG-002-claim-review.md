# C-STG-002 Claim Review

## Claim Under Review

The proposed exact claim fixes the canonical physical scalar by
`phi=F*u`, `V=mu^2 F^2(1-cos(u))`, with positive exact `kappa`, `F`, and
`mu`, and uses `x=mu*r`, `tau=mu*t`, `m=mu*M_geo`, and
`alpha=kappa*F^2`. On a domain with `x>0`, `N=exp(Phi)>0`, and
`f=1-2m/x>0`, the static areal metric and ansatz
`u=a(x)cos(Omega*tau)` define an exact phase-averaged single-harmonic
reduction. The claim states its averaged stress, mass and lapse constraints,
fundamental scalar equation, conservation factorization, regular-origin
series, flat/vacuum limits, and leading discarded scalar and stress harmonics.
It expressly does not state that this reduced object solves the pointwise
time-dependent Einstein-scalar PDE.

## Sourced Inputs

The review reads v0.130.0, C-STG-001, C-PDE-005, C-PDE-009, the frozen P179
proposal and revisions, hash-pinned SC2, every attempt through 0010, both
canonical modules and tests, the primary and independent verifiers, and the
dependency, consumer, compatibility, nonduplication, and source-graph audits.
SC2 is noncanonical evidence and no source decimal enters the exact claim.

## Independence

The independent reviewer does not import either proposed P179 module. It
reconstructs the Christoffel symbols, Ricci tensor, mixed Einstein tensor,
canonical phase-averaged stress, scalar projection, conservation identity,
discarded harmonics, and a direct phase quadrature from fresh expressions.

## Verification Status

The exact equations earn `symbolic_verified`. SymPy reduces the fresh mixed
Einstein components to `G^t_t=-2m'/x^2` and
`G^x_x=2[x(x-2m)Phi'-m]/x^3`. The canonical averaged conservation residual
reduces exactly to `f*a'/2` times the projected scalar residual. The returned
expressions contain no unevaluated integral, derivative obligation, numeric
root, or unresolved condition. The numerical BVP is deliberately excluded
from this claim and reviewed as C-PDE-013.

## Sensitivity and Counterexamples

The primary exact tests make the `J1` sign and radial-divergence coefficient
load bearing; both mutations break the conservation identity. The discarded
scalar coefficient is `2 J3(a)=a^3/24+O(a^5)`, and the pointwise density has
the generally nonzero second harmonic
`-Omega^2 a^2/(4N^2)+f a'^2/4+2J2(a)`. Zero amplitude gives vacuum, while
`alpha=0`, `m=Phi=0` gives the accepted flat radial projection. These are
counterexamples to any blanket full-PDE reading.

## Framework Compatibility

The action, signature, scalar stress, coupling dimension, and conservation
sign are native to C-STG-001. The projection and average-defect semantics are
native compositions of C-PDE-005 and C-PDE-009. The scale ledger leaves
`alpha` dimensionless and introduces no fitted physical `kappa`, `F`, or
`mu`. The result is a compatible extension, not a Horndeski or Gordon theory.

## Dependency and Consumer Replay

The accepted dependency closure is C-STG-001, C-PDE-005, and C-PDE-009.
The implementation is additive, with direct consumers limited to its tests,
P179 verifiers, and package exports. GitNexus finds no pre-existing upstream
caller or affected execution process and rates the change LOW risk. The
29-check source graph replay passes while keeping TX1 pending. Mutable
quadrature uses `numpy.trapezoid`; no version event affects the decision.

## Competing Candidate Audit

Candidates A through G and structural criteria were frozen before the SC2
body audit. Accepted composition alone lacked this exact spherical reduction;
the full oscillaton and nonminimal Horndeski candidates are distinct larger
problems; and numerical closeness did not select Candidate C. Candidate C wins
on exact action fit, scale economy, constraint closure, origin behavior, and
explicit truncation scope.

## Four-Axis Decision

The four axes are independently satisfied for the exact object.

- Verification: `symbolic_verified`
- Review: `accepted`
- Compatibility: `compatible_extension`
- Epistemic: `active`
- Relationship: new claim with `challenges=[]` and `supersedes=[]`

## Promotion Transaction

Promotion adds C-STG-002 to the registry, imports the exact API and tests,
freezes P179, qualifies SC2 only through its individual mappings, creates a
release, regenerates documentation and accepted memory, and replays every
affected validation path. C-STG-002 does not promote C-PDE-013 by implication.

## Continuation if Not Accepted

If an exact sign, scale, factor, or scope check fails, the claim returns to
Candidate C with the failed attempt preserved; a numerical workaround cannot
repair an exact failure.

## Done Gate

The exact claim passes its positive-object, closure, framework-fit,
independence, mutation, consumer, and individual-review gates with no open
claim-specific debt.

## Cross-References

See P179, C-STG-001, C-PDE-005, C-PDE-009, SC2, the primary verifier, the
fresh independent review, `spherical_einstein_scalar.py`, and C-PDE-013.
