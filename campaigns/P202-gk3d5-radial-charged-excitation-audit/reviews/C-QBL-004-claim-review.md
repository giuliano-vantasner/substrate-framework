# C-QBL-004 Claim Review

## Claim Under Review

The reviewed object is a conditional dimensionless complex scalar in flat
3+1 spacetime with signature `(+---)`, density `rho=Psi*Psi.conjugate()`, and
declared action density

`partial_mu(Psi.conjugate()) partial^mu(Psi) - [1-cos(sqrt(rho))]`.

The potential is analytic at `rho=0`. For
`Psi(t,r)=f(r)*exp(-i*omega*t)` on a real nonnegative radial branch, the exact
profile equation is

`f''+2*f'/r=sin(f)/2-omega^2*f`,

with `f'(0)=0`, `f(infinity)=0`, and localization domain
`0<omega<1/sqrt(2)`. In the C-U1-001 current convention,
`Q=2*omega*4*pi*integral(r^2*f^2 dr)`. The energy is
`4*pi*integral r^2*(f'^2+omega^2*f^2+1-cos(f)) dr`, the tail rate is
`kappa=sqrt(1/2-omega^2)`, and the stationary scaling identity is
`T+3*(U-omega^2*I)=0`.

At the single declared branch coordinate `omega=1/2`, independently refined
collocation and transformed shooting supply numerical evidence for a
nontrivial nodeless monotone finite-energy radial branch. This is not a proof
of a global existence interval, uniqueness, or stability. It does not
quantize the configuration, turn its Noether charge into physical electric
charge, identify it with a determinant field or asymptotic particle, or make
it a substrate excitation.

## Sourced Inputs

The review reads base release v0.149.0, C-U1-001, C-QBL-001 through C-QBL-003,
C-PDE-001, C-VAC-002 through C-VAC-004, the P202 freeze, the hash-pinned GK3D5
source, all four append-only attempts, the source audit, the candidate
comparison, the numerical construction record, and the exact dependency and
consumer graph. The proposed claim declares its own smooth action. It imports
only C-U1-001's current convention as accepted authority.

GK3D5's classical radial equation and a finite fixed-domain shooting trace
survive. Its VK-stability, accepted one-to-three-dimensional lift, infinite-
domain existence theorem, quantum-loop mass, physical charged excitation,
and no-new-ontology statements remain outside the claim delta.

## Independence

The primary path uses the importable adaptive-collocation API and an
origin-series DOP853 shoot. The independent review does not import that claim
module or solver. It transforms to `h=r*f`, derives
`h''=r*(sin(h/r)/2-omega^2*h/r)`, and uses direct SciPy DOP853 plus Brent root
finding at four outer radii. This representation removes the explicit
`2*f'/r` singular term. It independently derives the potential series,
Noether normalization, scaling identity, charge, energy, and tail condition.

## Verification Status

The maximum whole-claim verdict is `numeric_evidence`. SymPy exactly verifies
the potential series and origin limit, action variation, charge and energy
normalizations, origin series, small-amplitude tail equation, exponential
finite-norm tail, Pohozaev scaling, and failure of the one-dimensional lift.
Those exact substatements do not make numerical branch existence exact.

The primary verifier passes 30 checks. The transformed independent review
passes 16 checks. The corrected source-graph replay passes 28 checks. The
focused API suite passes five tests. The first graph run's incorrect aggregate
of 126 rather than 116 static sites is preserved as attempt 0004; all nine
per-file counts were correct, and the repair changes only their arithmetic
sum.

## Sensitivity and Counterexamples

The collocation sequence uses outer radii 20, 30, and 40, initial meshes 1001,
2001, and 4001, and tolerances from `1e-6` to `1e-8`. Fine-to-finer core error
is `1.69e-10` in the declared absolute norm; relative charge and energy
changes are below `6e-11`. The fine normalized Pohozaev residual is below
`5e-12`, and the fitted tail rate `0.4999492` agrees with the analytic `0.5`.

Direct DOP853 shooting gives central amplitude `6.106677965138643`; charge and
energy differ from the radius-20 collocation values by less than `4e-7`
relative. The independent `h=r*f` route converges over radii 16, 18, 20, and
22. Removing radial geometry, changing the sine coefficient, erasing the
frequency term, or reversing the tail sign makes the corresponding verdict
fail. The zero collocation solution is rejected explicitly. A radius-eight
box changes energy by more than one percent and leaves normalized Pohozaev
residual above eight percent.

## Framework Compatibility

The claim is a compatible conditional extension. It changes no accepted
real-sine-Gordon, one-dimensional Q-ball, vacuum-polarization, determinant,
or gauge-sector invariant. Its sole model parameter is `omega`, a branch
coordinate rather than an empirically fitted constant. All quantities are in
the declared dimensionless action normalization; no physical scale or matter
species is inferred.

## Dependency and Consumer Replay

The nine-node graph covers six qualified dependencies, GK3D5, pending GK3D6,
and already-qualified EL2. It checks 116 static call sites and 13 assertions
without a duplicate native execution. GK3D6 remains pending. EL2 retains only
`[C-TOP-001,C-U1-001]` and grants no backward authority.

Mutable quadrature is routed through `trapezoid_integral` or direct
`np.trapezoid`. Immutable GK3D5's current-first lazy legacy fallback is the
sole compatibility surface and causes zero scientific failures.

## Competing Candidate Audit

Eight candidates and structural criteria were committed before source
execution. Exact action closure and a genuinely refined branch select A and
B. Candidate C remains an unearned analytic upgrade. D fails because no
accepted dimensional lift exists. E is unnecessary because a distinct branch
survives. F lacks every quantization and determinant premise. G has no
independent foundation inconsistency. H is required for terminal source
governance. No comparator value selected the branch.

## Four-Axis Decision

The review decision keeps the exact and numerical statuses separate.

- Verification: numeric evidence, with exact symbolic substructure.
- Review: accepted.
- Compatibility: compatible extension.
- Epistemic: qualified.
- Relationship: additive claim depending on C-U1-001; no supersession.

## Promotion Transaction

Promotion adds C-QBL-004, `radial_qball.py`, focused tests, immutable P202,
release v0.150.0, generated documentation and accepted memory, and a qualified
GK3D5 disposition mapped to `[C-U1-001,C-QBL-004]`. The queue is regenerated
from `migration/dispositions.yaml`; it is never hand-edited. Primary,
independent, graph, focused, repository, release-closure, generated-state, and
diff checks must pass after the stage-aware mapping changes.

## Continuation if Not Accepted

If any promotion gate fails, P202 remains active. Numerical failures return to
the solver, representation, boundary, or target statement without weakening
the frozen thresholds. A global analytic existence interval or a stability
theorem would require a separate positive campaign and independent oracle.

## Done Gate

Acceptance requires the exact conditional model, numerical branch evidence,
interpretation ceiling, source mapping, consumers, generated records, and
empty P202 debt ledger to agree. A source pass tally or classical localized
profile alone is insufficient.

## Cross-References

The governing records are P202's proposal, formula freeze, numerical
construction, candidate comparison, three verifiers, source adjudication,
C-U1-001, release v0.150.0, the generated claim index, and the accepted claim
and release memory.
