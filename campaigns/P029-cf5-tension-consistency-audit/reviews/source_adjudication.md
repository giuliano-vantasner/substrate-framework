# Source adjudication: CF5 tension consistency

## Decision

CF5 is terminally `duplicate_evidence` for `C-VTX-001`, `C-VTX-002`, and
`C-FLX-001`. Its BVP and flux are reused accepted content; its effective area
is the inversion already classified by `C-FLX-001` as reconstruction. The
source establishes no independent core area, cross-model identity, physical
scale match, or confinement mechanism. No new claim, API, or release is
warranted.

## Reproduction boundary

The pinned source fails before its first check after both BVP solves because it
calls removed `np.trapz`. It exits with `AttributeError`, emits no check pass,
and has no terminal tally. This environment failure is preserved rather than
silently editing the immutable source. P026 already supplies stronger canonical
numeric evidence with solver-status gates, quadrature, tolerance, domain,
cutoff, guess-family, scaling, and independent finite-difference refinements.

## Check-family audit

CF5.1 repeats CF1's demo BVP at the same parameters. Its alleged two-mesh test
changes only the initial collocation mesh; both converged solutions are sampled
on the same 4000-point quadrature, and the current quadrature call fails. Even
if repaired, reproducing the same equations, parameters, solver family, and
tension is regression coverage for `C-VTX-002`, not independent evidence.

CF5.2 repeats `Phi=2*pi*n/g`, accepted exactly in `C-VTX-001`. Calling that
abstract Abelian-Higgs flux chromoelectric or the same flux as CF2 requires the
physical map that both accepted claims explicitly exclude.

CF5.3 defines `A_eff=Phi^2/(2*sigma_CF1)`. Positivity follows immediately from
positive inputs, but every positive alternative tension defines a different
positive area. No smooth profile, energy-density support, flux-containment
fraction, moment, radius, or boundary enters this definition.

CF5.4 rewrites the definition using `lambda_pen=1/(g*v)`, obtaining
`A_eff/lambda_pen^2=2*pi^2*n^2*v^2/sigma`. This is an invertible transform of
the supplied tension, not an independent comparator. The declared interval
`[0.1,100]` spans three decades and, for `n=v=1`, accepts tensions across a
factor of 1000. Tension mutations by factors of one tenth, ten, and forty from
the accepted demo value all pass. The vortex also has a distinct scalar inverse
length, and a free geometric factor such as `pi*lambda_pen^2` rescales the
ratio. The source derives no unique core-area convention.

CF5.5 explicitly notes that back-substitution “MUST” reproduce the supplied
tension. Exact elimination confirms the equality is the inverse-function
identity already stated in `C-FLX-001`; it cannot machine-identify two models.

CF5.6 rejects nonpositive tensions by the declared positive-area domain and
chooses `sigma=1000` to fall just beyond the broad window. That selected
mutation does not rescue sensitivity: numerous orders-different positive
tensions pass, and no independent physical pass threshold was preregistered.

## Exact duplicate disposition

CF5 adds useful downstream replay evidence but no distinct predicate or
consumer. `C-VTX-001/002` subsume its equations, flux, lengths, and demo tension;
`C-FLX-001` subsumes the effective-area inversion and warns that it predicts
nothing. Smooth-to-uniform geometry, physical field identity, core-area
definition, scale matching, string identity, and confinement remain rejected.
