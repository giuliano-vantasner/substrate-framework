# Review of C-GSK-002

## Claim Under Review

C-GSK-002 claims resolution-bounded evidence for one monotone stationary
branch at each of the declared inputs `(B,I)=(1,1),(2,pi+8/3),
(4,20.6496264884189)` with independently supplied `(c6,c0)=(1/2,1/4)`. It
reports finite-domain energy coefficients and their signed difference under
explicit solver, endpoint, residual, refinement, and independent-method scope.

## Sourced Inputs

The review reads C-GSK-001's exact candidate surface, accepted rational-map
angular claims, P218's numerical freeze, primary refinement record,
independent reviewer, attempts 0003-0007, canonical solver module, focused
tests, source adjudication, and consumer graph. MK5's empirical masses,
`N_c`, ANW coupling, source epsilon, and physical coefficient values are not
inputs to this claim.

## Independence

The canonical route uses adaptive `solve_bvp` collocation through the shared
status-checking wrapper, linear coefficient continuation, regular-origin and
massive Bessel-tail Robin data, and shared trapezoidal integration on an output
grid independent of the solver mesh. The fresh route evolves the
vacuum-complement field with DOP853 amplitude shooting and uses Simpson
quadrature. It imports neither the canonical generalized module nor the
primary verifier.

## Verification Status

The claim earns `numeric_evidence`, not an exact existence theorem. On
`[10^-4,20]` the canonical coefficients are approximately
`1.4326169552`, `2.7988849886`, and `5.1973886988`, giving
`3*pi^2[2 b(2)-b(4)]=11.85481448`. Maximum collocation RMS residual is below
`1.1e-6`, boundary residuals are below `2e-11`, and relative Derrick
residuals are below `2e-6`. Individual energies and the signed difference
stabilize from outer radii 14 through 26.

## Sensitivity and Counterexamples

Output quadrature, solver tolerance, inner cutoff, and outer domain are varied
separately. The B=2 RMS residual decreases from about `1.99e-6` to
`4.94e-7` as tolerance tightens. B=4 changes by less than `3e-11` across
inner cutoffs `2e-4,1e-4,5e-5`. Replacing `I` by `B^2` moves the signed
difference to `8.12019`; removing L6 moves it to `8.85035`; a massless-tail
condition fails on the massive branch. These mutations defeat a copied-value
oracle.

## Framework Compatibility

The numeric claim is conditional on C-GSK-001 and accepted angular inputs. It
does not reuse MK5's rejected physical coefficient derivation. Its branch is a
stationary solution on declared truncated domains, not a claim of global
minimization, half-line existence, or a full three-dimensional field.

## Dependency and Consumer Replay

The repaired independent R=14 route agrees with collocation to less than
`3e-7` per coefficient and `1e-5` in the signed difference. Direct-field
shooting failure at degree four is preserved: the vacuum-complement repair
retains the tiny origin signal without relaxing the residual threshold. All 65
focused tests and nine graph checks pass; later physical consumers gain no
authority.

## Competing Candidate Audit

Candidate selection compared source Dirichlet BVPs, asymptotic Robin
collocation, direct-field and vacuum-complement shooting, exact and biased
angular inputs, coupled and isolated refinements, and rejection on failed
residuals. Structural residual, convergence, method, and scope criteria select
the branch; comparator proximity is unused.

## Four-Axis Decision

The numeric claim remains qualified even though its review is accepted.

- Verification: `numeric_evidence`
- Review: `accepted`
- Compatibility: `compatible_extension`
- Epistemic: `qualified`
- Relationship: depends on C-GSK-001, C-RMAP-001, and C-RMAP-002; challenges and supersedes none

## Promotion Transaction

Promotion records the exact solver settings, coefficients, residual ceilings,
refinement evidence, independent route, exclusions, implementation, tests,
new release, generated docs/memory, and downstream consumer audit. It does not
promote the source's physical number.

## Continuation if Not Accepted

If the repaired route had failed, the next candidate was an independent
variational discretization; source convergence alone would not have completed
P218. The successful repaired route discharges that debt while preserving both
failed attempts.

## Done Gate

C-GSK-002 is accepted only as resolution-bounded evidence with all exclusions,
full package replay, synchronized records, and no unresolved numerical debt.

## Cross-References

See C-GSK-001, P218 primary numerical evidence, attempts 0004-0006,
C-RMAP-001/002, C-RPROF-002, and the source graph.

