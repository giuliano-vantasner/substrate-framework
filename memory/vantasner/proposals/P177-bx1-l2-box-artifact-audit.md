---
description: Audit BX1 and construct a reusable l2 finite-box spectral classification
author: vantasner
created: '2026-08-11T05:16:00Z'
updated: '2026-08-11T06:02:00Z'
tags:
- substrate-framework
- campaign-proposal
- migration-BX1
- l2-spectrum
- finite-box
category: proposals
confidence: established
status: archived
---
# P177 BX1 l2 Box-Artifact Audit

## Question and Positive Deliverable

P177 must determine whether hash-pinned BX1 correctly classifies QB3's
time-averaged l2 radial object as a finite Dirichlet-box state rather than a
localized half-line mode. The positive deliverable is a reusable, convention-
typed spectral theorem or classifier that distinguishes averaged finite-box,
half-line, and full periodic-coefficient problems. A box-artifact diagnosis or
absence of a bound state is evidence, not completion by itself.

## Base Release and Provenance

The accepted base is v0.128.0 at clean framework commit `7a3c85c`, with 164
accepted claims. The governed source baseline is
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`. BX1 is pending at
`merged-framework/bridges/phase-36/bridge_BX1_l2_mode_box_artifact.py`, SHA-256
`a80364df834f23b5ad006b54e7097e0a38d846405ba40408e558a8773aa74fb3`.
The source path is clean at the governed baseline and its sole history commit
is `7222eed21720c5174dd35ba8f825d8b7e0a48f3f`. No separate BX1 dossier or
formalization is present.

The generated queue already exposes BX1's box-artifact result and selected
numbers. P054's accepted memory and numerical audit also expose an above-
threshold, wall-following averaged state. P177 therefore claims no fresh
result blinding, but freezes its concepts and structural criteria before
opening or executing the BX1 body.

## Invariants, Conventions, and Allowed Imports

C-PDE-003 fixes the exact l2 linearized radial equation and regular origin
order. C-PDE-009 fixes real-m degeneracy and proves that replacing the full
time-dependent coefficient by its phase average defines a different equation
unless its pointwise defect vanishes or an independent Floquet construction
closes the gap. C-PDE-005 fixes the unit far-field mass threshold, while
C-PDE-006 is one finite-box harmonic-balance family point with a free central
amplitude and wall-sensitive radiative tails.

The campaign must distinguish four operators: QB3's supplied averaged finite-
wall BVP, its transformed finite-wall self-adjoint operator, the corresponding
regular half-line operator, and the full periodic-coefficient perturbation
equation. Each requires its own domain, origin law, outer data, norm,
continuum threshold, and evidence verdict. A positive Dirichlet eigenvalue
above the half-line continuum edge is not a localized bound state, but it does
not prove a universal Floquet or nonlinear no-go.

Allowed scientific imports are C-PDE-003/004/005/006/009, C-GW-001/002/007/008,
and the accepted package modules that implement them. C-MOD-001/002 may be
used only as a structurally analogous self-adjoint radial-spectrum workflow,
not as a premise about sine-Gordon. P052 and P054 records supply scoped
provenance and prior evidence. BX1, GW3, P3D2, QB1, QB3, and QB4 remain source
evidence only through their accepted mappings and qualifications.

Mutable numerical code must use `np.trapezoid` or the canonical
`trapezoid_integral`. Direct, imported, and dynamic legacy access, including
eager nested defaults, is preflighted before execution. Immutable legacy
source receives only an explicit alias backed by `np.trapezoid`; such a
version event cannot reject a scientific candidate.

## Candidate Preregistration

The candidates separate literal reproduction, existing accepted coverage,
exact half-line structure, refined spectral classification, full Floquet
dynamics, a regular finite-time positive object, generic artifact diagnostics,
and governed closure.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal BX1 replay | Hash-pinned source environment | Source literals and meshes | Evidence only until audited | AST, native/compatibility execution, solver and dataflow inventory |
| B | Accepted composition and nonduplication | C-PDE-009 plus scoped P054 evidence | None new | May cover every valid BX1 result | Exact statement, API, evidence, and consumer comparison |
| C | Exact transformed half-line theorem | Declared averaged potential and regular domain | l and asymptotic mass | Strong native fit | Liouville transform, norm, boundary form, continuum edge, vacuum limit |
| D | Refined finite-box classifier | Accepted background and typed wall problem | Domain, mesh, tolerance, level index | Numeric claim only if novel and closed | Residual, mesh/wall/tolerance refinement, nodes, independent Sturm/FEM route |
| E | Full Floquet problem | Periodic accepted background and monodromy domain | Time/radial resolution and phase | Most faithful but costliest | Multiplier residual, reciprocal structure, time/mesh/wall refinement, direct evolution |
| F | Regular finite-time l2 dynamics | Accepted C-PDE-004 IVP | Its declared data only | Existing positive dynamical fallback | Exact accepted composition; no duplicate simulation |
| G | Generic box-artifact diagnostics | Self-adjoint finite-wall family and known threshold | Scaling and compact-norm metrics | Reusable if not already canonical | Free soluble controls and bound/wall mutations |
| H | Governance closure | Claim-level review | None | Required | Dependency, consumer, queue, docs, memory, release replay |

## Selection Criteria and Blinding

Selection is ordered by accepted operator, domain, and boundary compatibility;
separation of averaged, finite-box, half-line, and Floquet objects; exact
regular-origin, norm, threshold, and node typing; solver status and residual;
independent mesh, wall, tolerance, and method evidence; assumption economy;
positive reusable API novelty; mutation sensitivity; consumer reach; and
physical-scope honesty. Queue and P054 exposure are recorded, and neither
numerical closeness nor the advertised artifact conclusion can select a route.

## Proposed Claim Delta

No claim identifier is assigned at the freeze. P054 already reserved
`C-PDE-010`, so it is unavailable even though it was never accepted.
Source-aware nonduplication must determine whether Candidates C, D, or G add a
distinct theorem or API. Any later identifier requires a recorded proposal
revision and a repository-wide registry, campaign, and durable-memory
collision search before implementation.

Direct consumers include BX1's disposition and any reverse unit that imports
its spectral classification. QB3 and QB4 remain qualified and cannot gain
authority from a later source synopsis. Existing C-PDE-004/005/006/009 APIs and
claims must remain unchanged unless a separately reviewed additive theorem is
actually needed.

## Source-Aware Revision and Adjudication

After source inspection, proposal revision 0001 assigns C-PDE-012 to Candidate
C plus the exact part of Candidate G. The new theorem combines the central-
radial Liouville and norm transport, regular-origin power, spherical-Bessel
Dirichlet-ball calibration, conditional threshold form bound, and forced-zero
endpoint non-discrimination. Candidate D is rejected as duplicate
implementation because the framework already has a generic FEM and P054 owns
the scoped accepted-background numeric audit. Candidate E remains a separate
unresolved Floquet problem.

P177 accepts C-PDE-012 in v0.129.0 and qualifies BX1 through C-PDE-003,
C-PDE-005, C-PDE-009, and C-PDE-012. The source's sampled global premise,
every-branch and linear-node claims, genuine full-periodic l0 mode, only-mode,
nonlinear, physical-radiation, gravity, and substrate conclusions remain
unaccepted.

## Implementation and Oracle Plan

The primary source audit will inventory every BX1 definition, import, literal,
check, assertion, solver call, boundary condition, background input, node
counter, spectrum, result dependency, and NumPy compatibility surface.
SymPy and direct exact algebra fit the radial Liouville transform
`chi=r*g`, the regular-origin map, norm equality, boundary form, far-field
threshold, and vacuum spherical-Bessel calibration.

If numeric Candidate D survives source audit and nonduplication, a proposal
revision will freeze its exact float64 operator, background reconstruction,
domain family, origin and outer data, finite-difference or finite-element
assembly, meshes, eigenvalue selection, residual norm, node convention,
tolerances, wall sequence, and stopping criteria before it runs. Solver success
and finite output are prerequisites. At least three mesh levels, independent
wall movement, and a separately assembled Sturm-shooting or FEM route must
agree within a scale-relative error model. Vacuum spherical-Bessel levels and
an explicit attractive-well bound-state control must make the classifier
sensitive. A full Floquet route requires a separate revision with monodromy,
time refinement, reciprocal or energy structure, and direct-evolution checks.

Load-bearing mutations change the angular barrier six, regular origin order,
field transformation, radial norm, asymptotic mass, wall location, eigen-index,
node counter, background amplitude, time-averaging convention, hard-zero tail,
and bound-state threshold. Numerical reruns of exact results count only as
regression. Canonical APIs will be added only for distinct reusable content;
campaign orchestration must reuse `verification.py`, accepted background
providers, and `numerics.py` where they fit.

The dependency graph will include BX1, GW3, P3D2, QB1, QB3, QB4, every direct
source import, and every reverse consumer found after freeze. Lexical check
sites, runtime executions, and assertions remain separate inventories.

## Attempts and Continuation

Attempt 0001 freezes v0.128.0, commit `7a3c85c`, source hash and history,
prior result exposure, eight competing candidates, structural criteria, empty
initial claim delta, oracle choices, and compatibility policy before opening
BX1's body. Any failed source, solver, representation, or candidate route will
be preserved append-only with a materially different next attempt.

Attempts 0002 through 0018 preserve native and instrumented reproduction,
source-aware selection, two focused implementation/oracle failures, four
primary verifier-construction failures, two independent-route failures, the
successful 39-check primary and 22-check independent routes, the 24-check
ten-node graph, 103 focused tests, and LOW staged impact. Representation,
arithmetic, wording, and resolution failures were repaired without widening
the scientific claim.

## Debt Ledger

The P177 ledger tracks exact source reachability, prior-evidence duplication,
operator and domain typing, background provenance, boundary and node meaning,
numerical convergence, averaged-versus-Floquet scope, consumers,
compatibility, and governed state.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| BX1's exact implementation and predicate reach are unknown | Pin every definition, check, assertion, import, solver, and runtime result | discharged |
| P054 may already own every valid conclusion | Compare exact claims, APIs, assumptions, numbers, and evidence scope | discharged |
| Radial field and transformed operator conventions may be mixed | Derive the transform, norm, domain, boundary form, and inverse map exactly | discharged |
| Background values may come from a pending or fitted source | Trace every background array and parameter to accepted or evidence-only provenance | discharged |
| Node count and eigen-index may be solver-guess artifacts | Define zero counting and independently order the finite-wall spectrum | discharged |
| Finite-wall numerics may be mistaken for a half-line theorem | Refine mesh, wall, tolerance, residual, compact norm, and soluble controls | discharged |
| Averaged evidence may be mistaken for full dynamics | Apply the C-PDE-009 defect or build a separately frozen Floquet route | discharged |
| Reverse consumers may inherit a blanket no-go or physical claim | Inventory and replay the complete affected graph | discharged |
| Legacy NumPy access may masquerade as science | Preflight and alias-replay immutable compatibility failures | discharged |
| Governed records may disagree | Synchronize disposition, queue, memory, effort, and any claim/release state | discharged |

## Review and Promotion Plan

Every BX1 predicate will receive an individual verdict. Exact transformation
or threshold algebra, numerical finite-box evidence, half-line classification,
and Floquet implications receive separate verification statuses. A distinct
claim must be reviewed from raw artifacts, extracted into a pure package API
with focused tests, replayed through all consumers, registered and released
claim-by-claim, rendered, and synchronized. If accepted claims already own the
valid content, BX1 will be qualified or marked duplicate evidence with exact
structured reasons and durable paths rather than a ceremonial release.

The final transaction edits only authoritative `migration/dispositions.yaml`
and regenerates the queue. It materializes every evidence path before registry
use, runs the targeted scientific routes, one integrated `scripts/validate.sh`,
and `git diff --check`, then validates record-only closure without repeating
the unchanged full suite. Validation and commit remain separate invocations.

## Done Gate

P177 closes only when the positive reusable spectral object, source predicate
audit, exact operator typing, numerical and boundary evidence, averaged/Floquet
scope, dependency consumers, compatibility, nonduplication, and governed
records agree with an empty campaign debt ledger. A box artifact, no bound
state, or failed Floquet route alone keeps the campaign active.

The done gate is discharged. C-PDE-012 supplies the positive reusable object;
the source, exact, numeric, mutation, dependency, consumer, compatibility,
claim, release, queue, docs, and memory records agree with no P177 debt.

## Cross-References

See C-PDE-003/004/005/006/009, C-GW-001/002/007/008, C-MOD-001/002, P052,
P054, GW3, P3D2, QB1, QB3, QB4, BX1, and the framework-migration effort.
