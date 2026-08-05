# C-PDE-013 Claim Review

## Claim Under Review

The proposed numerical claim fixes the C-STG-002 reduced model at central
amplitude 3 and dimensionless coupling `alpha=0.03`. It declares IEEE
float64, a regular origin cutoff, finite outer wall, second-order/cubic origin
series, approximate evanescent Robin tail, exterior Schwarzschild lapse
match, adaptive SciPy collocation, residual norms, axis-isolated refinements,
and an independent DOP853-plus-root shooting method. Its object is one
finite-wall phase-averaged branch, not an exact half-line or full-PDE state.

## Sourced Inputs

The review reads C-STG-002's exact proposed object, accepted C-PDE-012 wall
semantics, numeric revisions 0001 and 0002, the frozen thresholds, all failed
and repaired attempts, the complete numerical audit, both solvers, the
primary verifier, independent fresh reviewer, tests, and source check
adjudication. Source-reported digits are comparators only.

## Independence

The primary route uses adaptive collocation through the shared numerical
evidence API. The independent reviewer rewrites the ODE and origin/wall data
without importing the proposed modules and uses DOP853 plus a two-variable
root with wall continuation. Its initial one-shot long-wall failure is
preserved as attempt 0007 before the continuation repair.

## Verification Status

The branch earns `numeric_evidence`, not exact verification. At the finest
declared tolerance with epsilon 0.001, wall 40, and initial mesh 400, the
collocation result is `Omega=0.890839827775792`, outer dimensionless mass
`0.290960714264522`, central lapse exponent `-0.182426921486489`, and minimum
`f=0.879013430362296`. The maximum collocation residual is below `1e-10`, the
boundary residual is zero at reported precision, and the off-grid relative
ODE residual is `7.01e-11`.

## Sensitivity and Counterexamples

All twelve mesh, tolerance, origin, and wall levels pass solver, residual,
tail, and horizon gates. The largest normalized state, frequency, and mass
drifts are `1.84e-8`, `3.14e-10`, and `4.72e-9`, respectively, inside frozen
gates by large margins. Independent shooting gives
`Omega=0.890839827776100`, mass `0.290960714264587`, and central lapse
`-0.182426921486121`. Applying zero coupling to the finite-gravity profile
fails the ODE gate; changing the central amplitude to 2.5 fails the boundary
gate; and the wrong `J1` sign creates an order-one defect. The full-PDE
discarded harmonics remain nonzero regardless of BVP convergence.

## Framework Compatibility

The BVP solves only C-STG-002's accepted reduced equations and uses
C-PDE-012's finite-wall semantics. It never clips nonpositive `f`; a horizon
crossing is a solver failure. The free amplitude and dimensionless coupling
are declared branch coordinates and no physical scale is selected. The
outer Robin condition is approximate finite-wall data, so compatibility is a
qualified extension rather than an infinite-domain existence result.

## Dependency and Consumer Replay

The claim depends on C-STG-002 and C-PDE-012. Direct consumers are the numeric
tests and P179 verifier. The source graph passes 29 checks, and TX1's one-time
native replay remains pending and gains no authority. Mutable scripts use
`numpy.trapezoid`; immutable legacy spelling creates no scientific failure.

## Competing Candidate Audit

Candidate D was frozen before execution with equations, branch data,
precision, walls, cutoffs, meshes, tolerances, residuals, horizon gate, and
independent method. Candidate E's full oscillaton would answer a different
pointwise problem; Candidate F lacks a nonminimal action. D is selected by
residual closure and robustness, not closeness to SC2's printed digits.

## Four-Axis Decision

The four axes preserve the numerical and finite-wall ceilings.

- Verification: `numeric_evidence`
- Review: `accepted`
- Compatibility: `compatible_extension`
- Epistemic: `qualified`
- Relationship: new claim with `challenges=[]` and `supersedes=[]`

## Promotion Transaction

Promotion adds C-PDE-013 separately after C-STG-002, imports the numerical API
and tests, retains complete matrix evidence, qualifies only the matching SC2
subclaims, creates the release, and regenerates docs and memory. No exact or
full-PDE status is inherited from C-STG-002.

## Continuation if Not Accepted

If a solver, residual, refinement, horizon, independent-method, or mutation
gate fails, preserve the attempt and repair the numerical method or reject
the branch; do not widen tolerances or convert comparator digits into inputs.

## Done Gate

The finite-wall numerical claim has a positive solution object, declared
dependency closure, independent method, mutation sensitivity, complete axis
replay, explicit epistemic ceiling, and no open claim-specific debt.

## Cross-References

See P179, C-STG-002, C-PDE-012, SC2, numeric thresholds, numerical audit,
primary verifier, independent review, and `spherical_einstein_scalar_bvp.py`.
