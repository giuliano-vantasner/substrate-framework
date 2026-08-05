---
description: Audit SC2 and construct an exact phase-averaged spherical Einstein-sine-Gordon reduction
author: vantasner
created: '2026-08-11T06:58:00Z'
updated: '2026-08-11T06:58:00Z'
tags:
- substrate-framework
- campaign-proposal
- migration-SC2
- einstein-scalar
- harmonic-balance
category: proposals
confidence: exploratory
status: active
---
# P179 SC2 Static Einstein-Scalar Audit

## Question and Positive Deliverable

P179 must determine whether hash-pinned SC2 correctly derives and solves the
static spherical system it advertises. The positive deliverable is an exact,
dimensionally explicit, phase-averaged Einstein-sine-Gordon reduction in
areal gauge with regular origin, constraint, lapse, scalar, gauge, boundary,
and averaging-defect semantics, plus a sensitive verifier and importable API.
If the reduced equations support it, a separately preregistered finite-wall
BVP solution with convergence and independent-method evidence is an additional
numeric object. A bad source equation, failed BVP, or full-PDE no-go is attempt
evidence and cannot complete the campaign by itself.

## Base Release and Provenance

The accepted base is v0.130.0 at clean framework commit `2d9a6f1e20b8`, with
166 accepted claims. Its manifest SHA-256 is
`a13516d2a4de2d8d75b65ef5980c01e5feab408e123279954b4b12bf7dbf2ffb`.
The governed predecessor baseline is
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`. SC2 is pending at
`merged-framework/bridges/phase-36/bridge_SC2_horndeski_selfconsistent_solve.py`,
SHA-256
`64dfc9c31edd8368cb0e2359ca646fc8f62fe306d6af7a326ff8934070b96425`.
The target path is clean at the governed commit and its sole history commit is
`7222eed21720c5174dd35ba8f825d8b7e0a48f3f`. Unrelated later predecessor
worktree changes and phase-47/48 additions have no authority.

The queue exposes SC2's areal metric, single-harmonic field, averaged stress,
Jacobi-Anger functions, advertised equation structure, and done headline.
P178 also executed SC2 as a reverse consumer and checked its seven-predicate
tally and selected prose. P179 therefore claims no fresh conclusion or native-
output blinding. Exact source literals, numerical values, arrays, solver
status, thresholds, and intermediate implementation have not been newly
audited under this contract and remain unopened until the freeze validates and
is committed.

## Invariants, Conventions, and Allowed Imports

C-STG-001 fixes a four-dimensional mostly-plus Einstein-Hilbert action with a
healthy real canonical scalar, its stress sign, `G_ab=kappa*T_ab`, scalar Euler
equation, on-shell conservation identity, and dimension ledger. It supplies no
static localized scalar, sine-Gordon map, preferred coupling, or physical
gravity. If a dimensionless sine-Gordon field `u` is embedded as `phi=F*u`
with positive field scale `F` and mass scale `mu`, the physical potential must
be declared as `mu^2*F^2*(1-cos(u))`; the natural dimensionless gravitational
coordinate is then `alpha=kappa*F^2`. No scale may disappear silently.

C-PDE-005 owns exact flat-space odd-harmonic projection and radiative-tail
semantics. C-PDE-006 owns one free-amplitude finite-wall numeric branch only.
C-PDE-009 owns the exact defect between phase-averaged and full periodic
equations. C-PDE-012 owns regular radial, threshold, wall, and forced-endpoint
typing. C-GOR-002 closes the accepted transverse Gordon scalar match at vacuum
only; SC2's spherical areal metric is a different candidate and inherits no
Gordon or SC1 authority.

The candidate metric uses mostly-plus signature and areal coordinates,
`ds^2=-N(r)^2 dt^2+dr^2/f(r)+r^2 dOmega^2`, with positive lapse `N`,
`f=1-2m/r`, a regular center, and an explicitly horizon-free domain for a
static branch. A scalar `u=a(r) cos(omega*t)` with a static metric cannot be a
pointwise full Einstein solution merely because its stress is phase averaged.
The phase-averaged reduced model, the truncated scalar harmonic equation, and
the full time-dependent PDE remain three distinct objects.

Allowed imports are C-STG-001, C-GOR-001/002, C-PDE-001/003/005/006/009/012,
their canonical modules, exact differential geometry and Bessel identities,
and SciPy BVP or shooting tools only after a numerical proposal revision. The
source units G3, QB1, QB3, BX1, SC1, SC2, and their older named dependencies
remain noncanonical evidence except through explicit accepted mappings.

Mutable numerical integration uses `np.trapezoid` or the canonical
`trapezoid_integral`. Preflight covers direct, imported, dynamic, and eager-
default legacy access. Hash-pinned immutable source may receive only a recorded
alias backed by `np.trapezoid`; a version-only abort cannot reject a candidate.

## Candidate Preregistration

Seven candidates separate literal reproduction, accepted composition, exact
reduction, numerical construction, full periodic dynamics, actual Horndeski
dynamics, and governance.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal SC2 replay | Hash-pinned environment | Source literals and solver data | Evidence only until audited | AST, native/compatibility execution, predicate, assertion, solver, and dataflow inventory |
| B | Accepted composition | C-STG-001 and C-PDE-005/006/009/012 plus C-GOR-002 | None new | May own all valid source content | Exact statement, API, assumption, evidence, and consumer comparison |
| C | Exact averaged areal reduction | Canonical scalar with explicit `F,mu` scaling and static spherical metric | Dimensionless `alpha`, frequency, profile and gauge | Strongest exact positive fit | Independent curvature, stress average, reduced variation, Bianchi/constraint, origin and flat limits |
| D | Corrected finite-wall BVP | Candidate C plus frozen finite-domain data | Central amplitude, alpha, wall, mesh and tolerances | Numeric extension only if the exact system survives | Solver status, residual norms, mesh/wall/tolerance refinement, shooting or second collocation route |
| E | Full oscillaton expansion | Periodic scalar and metric harmonics | Harmonic sets and spacetime resolution | Faithful but substantially larger | Full residual, constraint propagation, time/radial refinement, conservation and independent evolution |
| F | Genuine Horndeski theory | Separately declared nonminimal action | Action-owned couplings only | Different theory, inadmissible by label alone | Variation, degeneracy/order audit, limits, boundary terms and full source match |
| G | Governance closure | Claim-level review | None | Required | Dependency, consumer, disposition, queue, release, docs, memory and debt replay |

## Selection Criteria and Blinding

Selection is ordered by accepted action, signature, stress, and dimension
compatibility; exact variational, constraint, and projected-scalar closure;
separation of reduced averaging from the full PDE; regular origin, horizon,
gauge, outer-boundary, and radiative-tail semantics; assumption, scale,
parameter, and boundary economy; solver status, residual, refinement,
independent method, and mutation sensitivity; novelty beyond accepted claims;
consumer reach; and physical-scope honesty. Exposed source conclusions and any
numerical closeness cannot select a candidate or tolerance.

## Proposed Claim Delta

P179 provisionally reserves C-STG-002 after direct searches of the registry,
campaigns, package, tests, and durable memory found no collision. The proposed
delta is not a pointwise periodic Einstein-scalar solution. Candidate C may
earn an exact compatible-extension theorem only if it derives the scaled
phase-averaged areal-gauge equations, their constraint structure, regular
origin laws, flat and vacuum limits, lapse gauge, and full-versus-averaged
defect from accepted inputs. Candidate D receives numeric status only and
requires a source-aware proposal revision before execution.

Direct consumers include SC2's disposition, SC1's already-qualified narrative
edge, pending TX1, the canonical Einstein-scalar and radial-harmonic modules,
their tests, generated docs, releases, and memory. SC1's accepted mapping is
unchanged and cannot become dependent on SC2 retroactively. TX1 remains
pending until separately adjudicated. No `supersedes` relationship is proposed.

## Implementation and Oracle Plan

The source audit will inventory every definition, import, literal, check,
assertion, phase average, Bessel expression, tensor component, ODE order,
boundary condition, solver call, status use, residual, tolerance, input,
result sentence, dependency, and NumPy compatibility surface. Lexical check
sites, runtime checks, assertions, and solver-status gates remain distinct.

SymPy and direct exact differential geometry are the strongest oracles for the
metric inverse, determinant, Einstein tensor, scalar stress, phase averages,
mass and lapse constraints, projected scalar equation, Bianchi relation,
origin series, dimensionless rescaling, and flat/vacuum limits. A second route
must reconstruct curvature and variation without importing the proposed
reduction helper. Load-bearing mutations change metric signature, `f=1-2m/r`,
mixed versus covariant components, factors of two, derivative order, potential
sign, lapse factors, `J_0`/`J_1` normalization, radial divergence, `alpha`,
time averaging, origin data, horizon domain, and outer tail policy.

If Candidate D survives, a recorded revision will freeze float64 equations,
central amplitude, coupling, frequency parameterization, origin cutoff, outer
radius, gauge condition, wall policy, mesh sequence, tolerances, maximum nodes,
stopping rule, collocation and off-grid residual norms, horizon margin, mass
and constraint errors, and a method-independent shooting or alternate-
collocation route. Mesh, wall, temporal projection, and tolerance refinement
are separate. A zero scalar/Schwarzschild or weak-field soluble control and
load-bearing parameter mutations are mandatory. A source hard zero at the
wall cannot count as decay evidence.

Reusable exact or numerical content will live in a pure package module and
reuse `einstein_scalar.py`, `radial_harmonic_balance.py`, `numerics.py`, and
`verification.py` rather than copying helpers. Imports execute no solver. The
source graph begins with G3, QB1, QB3, BX1, SC1, SC2, pending TX1, every actual
direct import, and every reverse consumer found after freeze.

## Attempts and Continuation

Attempt 0001 freezes v0.130.0, framework commit `2d9a6f1e20b8`, the SC2
hash and history, prior P178 exposure, accepted ceilings, seven candidates,
selection criteria, provisional C-STG-002, exact oracle, conditional numeric
contract, mutations, compatibility policy, and open debt before the new
source-body audit. Every failed implementation, representation, numerical,
candidate, or validation route will remain append-only with a materially
different next action.

## Debt Ledger

The P179 ledger tracks source reachability, dimensional embedding, equation
order and sign, phase-average consistency, constraint closure, solver and
boundary semantics, nonduplication, dependencies, consumers, compatibility,
and governed state.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| SC2's exact implementation and predicate reach are unaudited in P179 | Pin every definition, check, assertion, import, solver, value and result sentence | open |
| The source may erase the scalar mass and field scales | Derive the `phi=F*u`, `x=mu*r`, `alpha=kappa*F^2` ledger and trace every source parameter | open |
| Displayed mass, lapse, or scalar equations may have wrong order, sign, factor, or component | Reconstruct the exact tensor, stress, projected equation and constraints independently | open |
| A phase-averaged system may be called the full PDE | Derive and expose the pointwise and unretained-harmonic defects | open |
| Native solver completion may omit status, residual, refinement, or horizon checks | Inventory the oracle and build a fully declared sensitive route if selected | open |
| Finite-wall zeros or stable core values may be mistaken for localization | Apply accepted channel, wall, threshold and endpoint semantics | open |
| C-STG-002 may duplicate accepted scalar or harmonic claims | Compare exact statements, APIs, assumptions, evidence and consumers | open |
| SC1 or TX1 may inherit blanket authority | Replay the complete dependency and reverse-consumer graph | open |
| Legacy NumPy access may masquerade as science | Preflight and alias-replay immutable compatibility failures | open |
| Governed records may disagree | Synchronize disposition, queue, memory, effort, claim and release state | open |

## Review and Promotion Plan

Every SC2 predicate receives an individual verdict. Exact geometry, averaged
stress, projected scalar dynamics, numeric BVP evidence, full-PDE meaning,
Horndeski terminology, source dependencies, and physical prose receive
separate statuses. Any distinct claim must be independently rederived from raw
artifacts, extracted into a pure tested API, replayed through consumers, and
promoted claim-by-claim. SC2 receives a structured qualified, duplicate, or
other supported disposition with its unaccepted remainder preserved.

The promotion transaction edits only `migration/dispositions.yaml` and
regenerates the queue. Every evidence path is materialized before registration.
Targeted routes run before one integrated `scripts/validate.sh`; record-only
closure is checked narrowly without repeating the unchanged full suite.
Validation and commit remain separate invocations.

## Done Gate

P179 closes only when the positive exact averaged reduction or an equally
strong accepted composition exists, every source equation and predicate is
adjudicated, any selected BVP meets its preregistered numerical contract,
full-versus-averaged scope is explicit, dependencies and consumers replay,
compatibility and nonduplication are classified, governed records agree, and
the debt ledger is empty. A source error, solver failure, no localized state,
or full-PDE obstruction alone keeps the campaign active.

## Cross-References

See C-STG-001, C-GOR-002, C-PDE-005/006/009/012, P052, P054, P143, P177,
P178, G3, QB1, QB3, BX1, SC1, SC2, TX1, `einstein_scalar.py`,
`radial_harmonic_balance.py`, and the framework-migration effort.
