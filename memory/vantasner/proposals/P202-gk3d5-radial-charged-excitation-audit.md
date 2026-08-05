---
description: Derive and audit GK3D5's conditional three-dimensional radial charged branch
author: vantasner
created: '2026-08-05T20:06:00Z'
updated: '2026-08-05T20:06:00Z'
tags:
- substrate-framework
- campaign-proposal
- migration-GK3D5
- radial-qball
- charged-excitation
category: proposals
confidence: exploratory
status: active
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

## Debt Ledger

The P202 ledger tracks every action premise, normalization, boundary,
parameter, solver, residual, refinement, accepted dependency, physical
interpretation, consumer, generated record, and continuation.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| Native tally and samples are still blinded | Reproduce only after the committed freeze | open |
| The potential-to-equation normalization may be wrong | Independently vary the declared complex action | open |
| A BVP solver may converge to the zero solution or a box artifact | Enforce nontriviality and method mesh domain tolerance refinement | open |
| A numerical branch may lack global consistency | Check charge energy tail origin residual and Pohozaev identity | open |
| One-dimensional and real-radial claims may be silently lifted | Test the proposed compositions against their exact equations and ceilings | open |
| Classical charge may be overread as quantum loop matter | Audit quantization state determinant coupling and loop premises | open |
| C-QBL-004 may duplicate an accepted object | Complete claim API theorem and consumer nonduplication review | open |
| Reverse consumers may grant authority cyclically | Replay GK3D6 and EL2 with individual accepted mappings | open |
| Compatibility may masquerade as science | Preflight every mutable and immutable integration-name surface | open |

## Review and Promotion Plan

Every surviving claim receives an individual four-axis review and a fresh
independent derivation. A new API and release are permitted only for a distinct
dependency-closed branch object. GK3D5 receives its own terminal disposition;
GK3D6 stays pending and EL2 retains only its prior accepted mapping. Promotion
requires immutable campaign evidence, registry and release closure if a claim
is accepted, generated documentation and memory, exact graph replay, one
integrated gate, and an empty P202 ledger.

## Done Gate

P202 closes only when the exact conditional object, existence verdict,
mutation-sensitive strongest oracle, independent route, dependencies,
consumers, compatibility, claim review, source disposition, generated state,
and debt ledger agree. A converged shooting trace or a rejection of the
quantum headline alone is not completion.
