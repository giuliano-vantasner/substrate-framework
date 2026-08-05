---
description: Audit TX1 and construct a conditional rational-map intrinsic STF moment
author: vantasner
created: '2026-08-11T07:18:00Z'
updated: '2026-08-11T07:21:00Z'
tags:
- substrate-framework
- campaign-proposal
- migration-TX1
- rational-map
- intrinsic-quadrupole
category: proposals
confidence: exploratory
status: active
---
# P180 TX1 Intrinsic Quadrupole Audit

## Question and Positive Deliverable

P180 must determine what exact or resolution-bounded intrinsic rank-two energy
moment follows from the declared rational-map ansatz and corrected accepted
stationary branch. The positive deliverable is an importable factorization of
an explicitly declared local density into radial integrals and angular STF
tensors, exact symmetry and sign results where the mathematics permits them,
and a separately typed numeric B=2 value if independent refined evidence
supports it. A source error, zero symmetry channel, quadrature discrepancy, or
rejection of physical prose is attempt evidence and cannot complete the
campaign by itself.

## Base Release and Provenance

The accepted base is v0.131.0 at clean framework commit `a7d4fa7`, with 168
accepted claims. Its manifest SHA-256 is
`f3b8587555ca99523213519a2296849978437491566b587bafa554b24d23acf1`.
The governed predecessor baseline is
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`. TX1 is pending at
`merged-framework/bridges/phase-40/bridge_TX1_b2_intrinsic_quadrupole.py`,
SHA-256
`30161731af4e3ffda219adbdc7af9db66f6829fbbd3736a3198ed19a644ac8ff`.
The target path is clean at the governed commit and its sole history commit is
`7222eed21720c5174dd35ba8f825d8b7e0a48f3f`. Unrelated later predecessor
worktree changes have no authority.

The generated queue and P179 reverse-consumer replay already exposed TX1's
B=1 and B=4 null claims, B=2 diagonal sign pattern, printed B=1/2/4 angular
averages and masses, B=2 normalized moment, endpoint exponent, refinement
headlines, native nine-check success, two assertions, and one legacy plus one
current NumPy integration name. P180 therefore claims no fresh result or
runtime-output blinding. Exact source lines, local density construction,
quadrature dataflow, predicates, and assertion targets have not yet been
audited under this contract and remain unopened until the freeze commits.

## Invariants, Conventions, and Allowed Imports

C-RMAP-001 fixes the oriented round-sphere average, conformal Jacobian,
degree-area identity, exact axial family, and `I_2=pi+8/3`, but no physical
Skyrme action, minimizing map, radial profile, state, or mass. C-RMAP-002 gives
numeric integrals for one declared degree-four map without proving full cubic
symmetry or a minimum. C-RPROF-001 starts from a separately declared one-
dimensional radial functional; it does not itself accept an unintegrated
three-dimensional density. C-RPROF-002 gives corrected two-method evidence for
three conditional stationary branches only.

C-MOM-001 fixes `I_STF=I-delta*Tr(I)/3` and `Q=3*I_STF` and keeps moment
kinematics separate from gravity. C-MOM-003 fixes every radial-density null
and one exact `P2` guard. C-GW-001/002 are conditional TT algebra only. Axial
symmetry can force `diag(q,q,-2q)` but does not alone prove `q` is nonzero or
positive, and a static tensor has vanishing positive-order time derivatives.

Any local rational-map density must be displayed, dimensionally and
conventionally typed, and integrate exactly to C-RPROF-001's radial
functional. Its use remains a conditional reduced-model premise, not a
derived physical stress tensor or full three-dimensional solution. Mutable
quadrature uses `np.trapezoid` or `trapezoid_integral`. Hash-pinned immutable
TX1 may receive only a recorded alias backed by `np.trapezoid`; a version-only
abort cannot reject a scientific candidate.

## Candidate Preregistration

Seven candidates separate literal reproduction, accepted composition, exact
factorization, symmetry specialization, numeric evidence, full-field dynamics,
and governance.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal TX1 replay | Hash-pinned environment | Source grids and literals | Evidence only until audited | AST, native/alias execution, predicate, assertion, density, quadrature, and dataflow inventory |
| B | Accepted composition | Current accepted claims | None new | May own all valid content | Exact statement, API, assumption, evidence, and consumer comparison |
| C | General exact factorization | Explicit local rational-map density | Radial coefficient functions and declared map | Strong exact candidate | Sphere/radial separation, trace, dimensions, radial closure, and independent derivation |
| D | B=1, B=2, and degree-four symmetry specialization | Candidate C and declared maps | None beyond map choice | Exact null/form/sign results may survive | Symbolic angular integrals, group action, rotations, wrong-map and wrong-sign mutations |
| E | Corrected B=2 numeric moment | Candidate C plus C-RPROF-002 branch | Frozen domain, solver, grid, tolerances | Numeric extension only | Solver status, radial/angular refinements, independent quadrature/profile route, normalization mutation |
| F | Full field or rotating radiating object | Accepted physical action and dynamics not presently supplied | Action-owned scales and time data | Larger separate project | Full 3D residual or evolution, conservation, refinement, stability, and accepted coupling |
| G | Governance closure | Claim-level review | None | Required | Dependency, consumer, disposition, queue, release, docs, memory, and debt replay |

## Selection Criteria and Blinding

Selection is ordered by accepted sphere, radial-profile, and STF convention
compatibility; explicit local-density and radial-functional closure; exact
symmetry, sign, trace, and axis limits; assumption, scale, parameter, and
state-map economy; separation of exact nulls from resolution-bounded nonzero
values; solver and quadrature refinement, independent routes, and mutation
sensitivity; novelty; physical-scope honesty; and downstream governance.
Exposed source decimals cannot select the concept or set a tolerance. There
is no fresh source-result or runtime-output blind in P180.

## Proposed Claim Delta

P180 provisionally reserves C-RMOM-001 for a conditional exact rational-map
energy-moment factorization and C-RMOM-002 for a separately qualified B=2
numeric branch value. Direct searches of the registry, campaigns, package,
tests, migration records, and durable memory found no collision. Neither
identifier denotes a full-field solution, physical mass quadrupole,
gravitational coupling, rotating configuration, or radiation channel.

Potential dependencies are C-RMAP-001/002, C-RPROF-001/002, and C-MOM-001/003.
Direct consumers include TX1's disposition, pending TX2/TX3, the rational-map
and moment modules, their tests, generated docs, releases, and memory. Already-
accepted claims cannot become dependent on P180 retroactively. No
`supersedes` relationship is proposed.

## Implementation and Oracle Plan

The source audit will inventory every definition, import, literal, local-
density term, angular map, profile solve, boundary condition, grid, quadrature,
moment convention, predicate, assertion, output sentence, dependency, and
NumPy compatibility surface. Lexical check calls, runtime checks, assertions,
solver-status gates, and scientific verdicts remain distinct. The exact hash-
matched P179 execution will be reused rather than repeated ceremonially unless
the body audit identifies an unresolved runtime path.

SymPy and direct exact sphere integration are the strongest oracles for
angular factorization, tensor trace, axial form, B=1 null, R=z^2 moments,
radial-functional recovery, and sign. A second derivation will use Cartesian
or Legendre moments without importing the proposed helper. For the declared
degree-four map, a finite symmetry proof requires exact map equivariance or
an explicit group argument; numeric near-zero alone earns only regression
evidence. Mutations change the Jacobian power, local-density coefficient,
STF convention, polar-axis sign, sphere normalization, degree, map
coefficients, profile derivative, and radial weight.

If Candidate E survives, a source-aware revision must freeze IEEE-754
precision, corrected `(B,I)=(2,pi+8/3)`, radial equation, origin and wall data,
domain, solver, tolerances, maximum step or nodes, sample grids, angular rule,
radial rule, endpoint estimates, tensor norm, scale-relative agreement gates,
and independent profile and quadrature routes before new execution. Radial
domain, grid, solver tolerance, angular polar/azimuthal order, and quadrature
method refinements remain separate. Source digits do not define any gate.

Reusable logic will live in a pure package module and call canonical rational-
map, radial-profile, numerical, and verification APIs. Imports execute no
solver. Dependency and reverse-consumer replay begins from the queue's TX1
edges and must keep TX2/TX3 pending until their own campaigns.

## Source-Aware Revision

Revision 0002 selects Candidates C, D, E, and G after the line-by-line TX1
audit. The source's displayed local density does integrate exactly to
C-RPROF-001's radial functional, and the B=2 sign is analytically tractable.
The source nevertheless computes normalized `I_STF` while calling it `Q`, has
a factor-of-`R^2` error in the `N_c^2` monopole-tail term, treats leading
linearized tail estimates as exact, uses a hard finite-cutoff origin value,
couples wall and initial-mesh changes, and has no independent solver or
quadrature. Its B=4 near-zero does not prove exact cubic equivariance or a
minimal-map theorem.

Candidate E is authorized for `(B,I)=(2,pi+8/3)` only. The canonical route
uses the accepted vacuum-complement DOP853 shooting API with inner radius
`1e-4`, outer radius `24`, 2401 points, `rtol=3e-10`, `atol=3e-12`, and maximum
step `0.05`; sampled radial integration uses `trapezoid_integral` and explicit
leading origin and tail estimates. Isolated axes use outer radii 16, 24, 32,
and 48; inner radii `2e-4`, `1e-4`, and `5e-5`; sample counts 1201, 2401, and
4801; relative tolerances `1e-8`, `3e-10`, and `1e-11`; and maximum steps
0.1, 0.05, and 0.025. Solver success, finite data, both endpoint residuals,
and monotonicity are gates before moments are consumed.

The independent route is a fresh `solve_bvp` collocation from a two-power
analytic guess on a geometric-plus-linear mesh, tolerance `3e-7`, boundary
tolerance `3e-8`, at most 50,000 nodes, and Simpson radial integration. Direct
tensor Gauss-Legendre by periodic-azimuthal sphere rules at 24x48, 48x96, and
96x192 must reproduce the exact B=2 angular tensors; this is a regression and
independence check, not the exact oracle. The canonical and independent
normalized `I_STF_zz/M0` values must agree within `2e-6` relative, every
single-axis finest pair within `3e-6`, and the value must stay below `-0.1`.
Exact B=1 and isotropic nulls stay separate from numerical near-zero tests.

Mutating the normalized tensor into triple `Q` must change the reported ratio
by exactly three; sphericalizing both `N_c` and `N_c^2` must give an exact
null; flipping the axial kernel sign must violate the sign verdict; omitting
the `N_c^2` density term must change the component while retaining trace; and
the source's erroneous monopole tail must be detected dimensionally and by
outer-radius scaling. The exposed `-0.33885166` source literal is a comparator
only and sets no threshold.

## Attempts and Continuation

Attempt 0001 freezes v0.131.0, framework commit `a7d4fa7`, the TX1 hash and
history, complete prior exposure, accepted ceilings, seven candidates,
selection criteria, provisional identifiers, oracle choices, compatibility
policy, and open debt before the new source-body audit. Every failed
implementation, representation, numeric, candidate, or validation route will
remain append-only with a materially different next action.

## Debt Ledger

The P180 ledger tracks source reachability, local-density provenance, angular
and radial factorization, tensor conventions, numerical semantics, scope,
dependencies, consumers, compatibility, and governed state.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| TX1's exact implementation, density, predicates, assertions, and dataflow are unaudited in P180 | Pin every definition, input, quadrature, check, assertion, and result sentence | open |
| The source may not integrate to C-RPROF-001's functional | Derive the local-to-radial reduction term by term | open |
| Symmetry may establish form but not nonzero amplitude or sign | Independently derive all angular STF coefficients and sign conditions | open |
| The numeric value may use biased angular/profile inputs or weak quadrature | Freeze and run corrected independent radial and angular refinement if selected | open |
| An ansatz moment may be called a solved physical Skyrmion quadrupole | Separate reduced ansatz, stationary branch, full field, stress, units, and state-map claims | open |
| A static tensor may be used as a radiation mechanism | Require explicit time dependence and accepted coupling in separate TX2/TX3 audits | open |
| C-RMOM-001/002 may duplicate accepted moment or rational-map claims | Compare exact statements, APIs, assumptions, evidence, and consumers | open |
| Legacy NumPy access may masquerade as science | Reuse native evidence or alias-replay immutable compatibility failures without candidate rejection | open |
| Dependencies, consumers, and governed records may disagree | Replay graph and synchronize disposition, queue, memory, claims, release, and docs | open |

## Review and Promotion Plan

Every TX1 predicate receives an individual verdict. Local-density provenance,
exact factorization, B=1 and degree-four nulls, B=2 tensor form and sign,
numeric magnitude, full-field language, physical state names, no-free-
amplitude prose, static radiation meaning, dependencies, and compatibility
receive separate statuses. Any distinct claim must be independently rederived,
extracted into a pure tested API, replayed through consumers, and promoted
claim by claim. TX1 receives a structured qualified, duplicate, refuted, or
other supported disposition with every unaccepted remainder preserved.

The promotion transaction edits only governed mutable records and generates
canonical queue and docs. Every evidence path is materialized before
registration. Targeted routes run before one integrated `scripts/validate.sh`;
record-only closure is checked narrowly without repeating the unchanged full
suite. Validation and commit remain separate invocations.

## Done Gate

P180 closes only when the positive exact factorization or an equally strong
accepted composition exists, every source predicate is adjudicated, any
selected numeric value meets its preregistered contract, exact and numeric
claims remain separate, full-field and radiation ceilings are explicit,
dependencies and consumers replay, governed records agree, and the debt
ledger is empty. A source error, numeric null, biased input, compatibility
event, or physical-prose rejection alone keeps the campaign active.

## Cross-References

See C-RMAP-001/002, C-RPROF-001/002, C-MOM-001/003, C-GW-001/002, P036,
P038, P045, P104, P105, P177, P179, E1, E2, GW3, P3D2, BX1, SC2, TX1-TX3,
`rational_maps.py`, `rational_map_radial.py`, `conserved_moments.py`, and the
framework-migration effort.
