---
description: Derive and audit GK3D5's conditional three-dimensional radial charged branch
author: vantasner
created: '2026-08-05T20:06:00Z'
updated: '2026-08-05T20:41:45Z'
tags:
- substrate-framework
- campaign-proposal
- migration-GK3D5
- radial-qball
- charged-excitation
category: proposals
confidence: established
status: archived
---
# P202 GK3D5 Radial Charged Excitation Audit

## Question and Positive Deliverable

P202 must determine whether the conditional smooth 3+1 complex-scalar action
with `U(|Psi|^2)=1-cos(sqrt(|Psi|^2))` has a verified finite-energy stationary
radial charged branch. The positive deliverable is its exact action, equation,
boundary, current, energy, tail, virial, and existence ledger plus a genuinely
refined branch construction if existence is numerical. A failed source branch
or an honest quantum-interpretation ceiling is attempt evidence, not the
requested completion.

## Base Release and Provenance

The accepted base is v0.149.0 at clean framework commit `72968f3`, with 189
accepted claims. GK3D5 is pending at the pinned predecessor baseline
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`; its source SHA-256 is
`201d4fd2594a73c7b59dbe81e0e66f1d3d43a52605a26174c70bd072626992e2`.
The queue exposes the claimed radial equation, 13 static check-call sites, two
assertions, and its high-level derivation categories but not the native tally
or numerical samples. Those uninspected values remain blinded through the
committed freeze.

EM1, EM2, EM6, GK3D1, GK3D3, and GK3D4 are qualified only through their exact
accepted mappings. Memory search and source verification found C-QBL-001 and
C-QBL-002 as the nearest one-dimensional stationary branches and C-PDE-001 as
a separate real radial IVP. No accepted radial complex Q-ball claim or
`C-QBL-004` identifier exists. GK3D6 remains pending; EL2's accepted mapping
does not include GK3D5 and therefore supplies no backward authority.

## Invariants, Conventions, and Allowed Imports

The real sine-Gordon field, conditional complex U1 scalar, classical localized
configuration, quantized particle, and free field inside a determinant are
different objects until governed maps connect them. C-QBL-001 and C-QBL-002
do not lift their one-dimensional profiles or stability to three dimensions.
C-PDE-001 contributes only regular radial geometry and numerical controls.
C-VAC-002 through C-VAC-004 explicitly declare their loop matter and derive no
charged substrate excitation.

Allowed tools are exact SymPy variation, series, limits, and identities plus
SciPy collocation, DOP853 shooting, root finding, and quadrature with explicit
solver success, tolerances, meshes, domains, and error norms. Mutable
quadrature uses `np.trapezoid` or the shared helper; immutable compatibility
events never reject a scientific candidate.

## Candidate Preregistration

Eight candidates separate exact conditional structure, numerical branch
construction, analytic existence, an alleged accepted lift, no new surface,
the quantum-loop headline, exceptional foundation repair, and terminal source
governance.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Exact radial action ledger | independently declared smooth complex action | omega | native conditional extension | exact variation boundary charge energy tail and virial closure |
| B | Refined radial BVP branch | Candidate A plus nodeless branch | omega and numerical controls | plausible distinct positive object | collocation shooting mesh domain tolerance and observable agreement |
| C | Analytic existence interval | effective-potential and radial-friction hypotheses | omega | preferred if proof closes naturally | overshoot undershoot theorem with all boundary hypotheses |
| D | Accepted-claim composition | exact dimension-lift theorem | none | predicted invalid | substitute accepted 1D and real-radial objects into the claimed equation |
| E | No new claim or API | no distinct branch survives | none | fallback only after positive routes fail | nonduplication and failed-object audit |
| F | Quantum loop excitation | quantization normalized states determinant and coupling | additional quantum data | predicted unsupported | dependency closure from accepted premises |
| G | Foundational revision | independent accepted inconsistency | repair alternatives | predicted unnecessary | inconsistency without assuming GK3D5 |
| H | Terminal source closure | complete object and graph audits | none | required | individual disposition and consumer replay |

## Selection Criteria and Blinding

Selection prioritizes exact normalization, smoothness, radial regularity,
finite charge and energy, solver status, residual and refinement convergence,
independent-method agreement, Pohozaev and tail consistency, assumption
economy, novelty, and quantum-interpretation discipline. No numerical
closeness selects a candidate. The native tally, branch values, source solver
settings, and comparators stay blinded until this contract, formula freeze,
provenance record, and repository preflight are committed.

## Proposed Claim Delta

Provisional C-QBL-004 may state an exact conditional 3+1 radial complex-scalar
equation and a verified nodeless finite-energy branch, with numeric or stronger
verification assigned according to the surviving oracle. It depends on
C-U1-001 for the current convention and otherwise declares its action rather
than pretending that C-QBL-002 or C-PDE-001 supplies a lift. It cannot include
quantization, particle identity, loop insertion, physical electric charge, or
substrate realization.

## Implementation and Oracle Plan

If Candidate A or B survives, reusable action, residual, origin-series, tail,
observable, and solver logic belongs in a pure package module with focused
tests. The primary route derives the equation, normalization, finite
integrals, tail, and three-dimensional Pohozaev identity before evaluating the
branch. At omega one-half, collocation uses outer radii 20, 30, and 40, meshes
of 1001 through 4001 representative points, and tolerances from `1e-6` to
`1e-8`; independent DOP853 shooting uses `rtol=1e-10` and `atol=1e-12`.

The declared gates require solver success, nontriviality, origin and boundary
closure, decreasing mesh error below `1e-3`, radius-30-to-40 observable change
below `1e-3`, method agreement below `2e-3`, normalized Pohozaev residual
below `1e-4`, and a tail exponent within five percent on a non-roundoff window.
Mutations remove radial geometry, double the potential force, erase frequency,
substitute the 1D profile, accept the zero branch, truncate the domain, or
promote a classical solution into quantum loop matter. Exact derivation and a
fresh numerical formalism remain separate evidence routes.

## Attempts and Continuation

Attempt 0001 freezes authority, provenance, eight candidates, equations,
numeric protocols, thresholds, mutations, the compatibility rule, and all
initial debt before source execution or body inspection. Later attempts stay
append-only and change method, representation, candidate, or target when a
route fails without weakening the positive objective.

Attempt 0002 reproduces all 13 native predicates in 13.28 seconds with exit
zero. The immutable source safely selects `np.trapezoid` in the current
environment; its unevaluated short-circuit fallback is compatibility evidence
only. Exact potential, series, scaling, and tail identities survive, as does a
finite fixed-domain shooting trace. The accepted registry supplies neither
EM6 stability nor a complex P3D lift. The source never checks solver success,
truncates observables at numerical turnaround, holds the domain and method
fixed, tests positivity rather than monotonicity, and identifies a tail inverse
length with a quantum loop mass. Those overreads are rejected before an
independent branch construction.

Attempts 0003 and 0005 select A, B, and H, add the canonical radial API, and
close 30 primary, 16 transformed-independent, 28 corrected graph, and five
focused checks or tests. Collocation over radii 20, 30, and 40 and independent
shooting converge to central amplitude `6.1066779651`; the fine observable,
Pohozaev, and tail gates exceed the frozen margins. Attempt 0004 preserves a
graph aggregate bookkeeping error—116 static sites were initially summed as
126—then corrects only that arithmetic without changing any per-file result.

## Debt Ledger

The P202 ledger tracks every action premise, normalization, boundary,
parameter, solver, residual, refinement, accepted dependency, physical
interpretation, consumer, generated record, and continuation.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| Native tally and samples are still blinded | Reproduce only after the committed freeze | discharged by attempt 0002 |
| The potential-to-equation normalization may be wrong | Independently vary the declared complex action | discharged by exact action variation and independent current derivation |
| A BVP solver may converge to the zero solution or a box artifact | Enforce nontriviality and method mesh domain tolerance refinement | discharged by zero-branch rejection and radii 20, 30, and 40 |
| A numerical branch may lack global consistency | Check charge energy tail origin residual and Pohozaev identity | discharged by attempts 0003 and 0005 |
| One-dimensional and real-radial claims may be silently lifted | Test the proposed compositions against their exact equations and ceilings | discharged; both proposed lifts leave distinct residuals or field models |
| Classical charge may be overread as quantum loop matter | Audit quantization state determinant coupling and loop premises | discharged by the claim and source reviews with those readings unpromoted |
| C-QBL-004 may duplicate an accepted object | Complete claim API theorem and consumer nonduplication review | discharged; the smooth complex 3D stationary branch is distinct |
| Reverse consumers may grant authority cyclically | Replay GK3D6 and EL2 with individual accepted mappings | discharged by the 28-check graph replay |
| Compatibility may masquerade as science | Preflight every mutable and immutable integration-name surface | discharged with zero scientific version failures |

## Review and Promotion Plan

Every surviving claim receives an individual four-axis review and a fresh
independent derivation. A new API and release are permitted only for a distinct
dependency-closed branch object. GK3D5 receives its own terminal disposition;
GK3D6 stays pending and EL2 retains only its prior accepted mapping. Promotion
requires immutable campaign evidence, registry and release closure if a claim
is accepted, generated documentation and memory, exact graph replay, one
integrated gate, and an empty P202 ledger.

## Done Gate

P202 promotes qualified C-QBL-004 in v0.150.0 and qualifies GK3D5 through
C-U1-001 and C-QBL-004. The exact conditional object and resolution-bounded
existence verdict agree across the primary, transformed-independent, graph,
and focused routes. GK3D6 remains pending, EL2 is unchanged, every physical
and quantum overread remains unpromoted, mutable integration uses the current
NumPy name or shared helper, generated authority is synchronized, and the P202
debt ledger is empty. Attempt 0006 records the single integrated promotion
gate: all 1,815 tests pass in 172.62 seconds, all 829 memory files validate,
and the process exits zero after 185.55 wall seconds at 217,480 KiB peak RSS.
