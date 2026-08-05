# Source adjudication: CF5 current-NumPy information closure

## Decision

CF5 remains duplicate evidence for unchanged C-VTX-001, C-VTX-002, and
C-FLX-001. P170 adds no claim, API, or release. The source's conditional vortex
equations, flux, inverse lengths, demo tension, fixed-area energy slope, and
effective-area reconstruction are already accepted at more accurate scope.

CF5 does not derive a smooth-profile cross-section, identify the smooth vortex
with a uniform chromoelectric tube, predict a string tension, or establish QCD
confinement or a substrate mechanism. Its exact closure is back-substitution
of an area defined by inverting the supplied tension.

## Reproduction and compatibility

The immutable source is unchanged at SHA-256
`0a449f8b95bc0a83fb0316992fb0d1776a6157e1445029623b4608246dc256f7`.
Under NumPy 2.5.1, native execution stops before CF5.1 because `np.trapz` was
removed. This is a version-only event, not a scientific candidate failure. An
isolated process binds only the missing legacy name to `np.trapezoid`, leaves
the source bytes and equations unchanged, and passes all six predicates.

The four-node graph replays CF1, CF2, CF4, and CF5. Only immutable CF1 and CF5
need aliases, covering four legacy references, all backed solely by
`np.trapezoid`. Mutable campaign and canonical code has no executable legacy
integration call.

## Numeric evidence

The replay gives tensions 4.211567 at both 400 and 800 initial mesh points,
with a reported difference `3.82e-13`. This is a valid regression of one
collocation setup but weaker than C-VTX-002, whose accepted evidence includes
explicit solver diagnostics, domain, cutoff, tolerance, quadrature, initial-
guess, scale, and independent finite-difference refinement.

P170 therefore hash-reuses P026's unchanged refinement matrix and performs one
proportionate current canonical solve. The canonical `trapezoid_integral`
route selects `np.trapezoid` and reproduces tension 4.21160 with the accepted
residual bound. Repeating the full unchanged matrix would add ceremony rather
than information.

## Information audit

For positive flux and supplied tension,

`A_eff = Phi^2/(2*sigma)`.

Substitution into `Phi^2/(2*A_eff)` returns `sigma` identically for every
positive input. Coefficient mutations fail as they should, but alternative
positive tensions each construct different positive areas and close the same
round trip. Thus the identity validates algebraic consistency, not a tension
or area prediction.

With `Phi=2*pi*n/g` and vector inverse length `g*v`, the displayed ratio is

`A_eff/lambda_pen^2 = 2*pi^2*n^2*v^2/sigma`.

The gauge coupling cancels, so this too is a reversible transform of the
supplied tension. The declared interval `[0.1,100]` maps to a factor 1000
tension interval. Mutating the demo tension by 0.1, 10, and 40 leaves it in
the window; the selected value 1000 fails only its lower boundary. This test
does not discriminate the accepted vortex tension from broad alternatives.

The vortex also has a distinct scalar inverse length
`v*sqrt(2*lambda)`. Switching length convention rescales the comparison by
`2*lambda/g^2`, and a free core-area factor rescales it continuously. A true
profile-geometric area requires an independently defined support radius or
moment observable. No such observable enters CF5's `A_eff`.

## Predicate adjudication

CF5.1 is duplicate C-VTX-002 regression evidence. CF5.2 duplicates
C-VTX-001's conditional flux. CF5.3 is the positive reconstruction already
bounded in C-FLX-001. CF5.4 is rejected as an independent physical scale match.
CF5.5 is an exact but non-predictive reconstruction identity. CF5.6 validly
rejects nonpositive area, but its positive-tension discrimination rests only
on the broad window and earns no physical status.

The check-helper assertion is an execution mechanism. The solver-status
assertion is necessary numeric hygiene, but it is not refinement, independent
geometry, or information evidence.

## Independent, graph, and consumer closure

The primary, fresh exact, source-graph, and focused-test routes pass 41, 20,
24, and 39 checks or tests. The independent review imports neither canonical
physics module nor solver. The graph replays 35 lexical and 35 runtime
predicates plus six assertions.

P026 and P029 evidence is hash-identical and reused. C-VTX-001 has no accepted
dependency; C-VTX-002 depends only on it; C-FLX-001 has no accepted dependency.
No accepted edge maps the smooth vortex to a uniform physical tube. No public
API, claim, release manifest, or generated accepted documentation changes.

## Exact duplicate disposition

CF5 remains terminal duplicate evidence. P170 supplies current compatibility,
predicate, information, graph, and consumer evidence while preserving both the
native stop and the failed first graph probe. The accepted four-axis states and
v0.127.0 remain unchanged.
