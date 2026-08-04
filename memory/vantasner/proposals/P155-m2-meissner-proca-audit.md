---
description: Derive and audit M2's conditional source-free Proca screening theorem
author: vantasner
created: '2026-08-10T07:00:00Z'
updated: '2026-08-10T07:25:00Z'
tags:
- substrate-framework
- campaign-proposal
- migration-M2
- proca-screening
category: proposals
confidence: exploratory
status: active
---
# P155 M2 Meissner-Proca Audit

## Question and Positive Deliverable

P155 must deliver an exact importable classification of the Euler equation,
derived divergence constraint, dispersion, and unique decaying transverse
half-line solution of a separately declared source-free Proca action. It must
state the metric and action conventions together, distinguish the massive
constraint from gauge fixing, expose the growing ODE branch and the boundary
data that remove it, and keep the conditional M1 coefficient separate from
any London, Meissner, condensate, weak-boson, material, observable, or
substrate interpretation.

## Base Release and Provenance

The accepted base is v0.120.0 at framework and scientific commit `30adbe3`.
The source baseline is `/home/dan/substrate` commit
`6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`; later dirty engineering,
framework-prose, and memory files remain excluded. M2 is pinned at
`merged-framework/bridges/phase-7/bridge_M2_meissner_proca_W_mass.py`, SHA-256
`4ae3e5cb06e7c0bce6387ac7b84f555de65f12cce4be42d620405bb2b5c5b59f`.
Its dossier is `merged-framework/bridges/phase-7/dossiers/M2-dossier.md`,
SHA-256
`c2b93ee2f68f9f42fde2ad133320fd8d3fc08293850dc63d4469a55cebf8908a`.

The queue exposes six candidate dependencies, seven literal checks, one
assertion, and the broad M1 coefficient, Proca/London equation, exponential
profile, penetration length, and Meissner analogy. Those unavoidable values
are recorded and cannot select a concept. The source and dossier bodies,
exact AST data flow, action signs, component geometry, ODE branch handling,
constants, and guards remain unopened.

## Invariants, Conventions, and Allowed Imports

C-GSM-001 supplies a conditional quadratic coefficient and generalized
kinetic-metric eigenproblem, but no gauge kinetic action, stationary
condensate, spectral pole, W field, Standard Model sector, or substrate mass
mechanism. C-NAG-001 supplies covariance and curvature but no action
coefficient, equation of motion, current, mass, or physical weak sector.
C-GAU-001 supplies local Abelian covariance only. C-VTX-001 supplies a
separately declared radial Abelian-Higgs model and its conditional asymptotic
inverse lengths, while C-EFT-001 supplies algebraic stationary elimination
without a kinetic Proca PDE. C-VAC-001 and C-QBL-001 supply neither a complete
M2 gauge action nor a material dictionary.

The frozen convention is mostly-plus
`eta=diag(-1,+1,+1,+1)`,
`F_mu_nu=partial_mu A_nu-partial_nu A_mu`, and source-free density
`L=-F_mu_nu F^mu_nu/4-m^2 A_mu A^mu/2` with exact positive `m`. Variation
must give `partial_mu F^(mu nu)-m^2 A^nu=0`; its divergence must derive
`partial_mu A^mu=0`, and substitution must give
`(box-m^2)A^nu=0` with `box=-partial_t^2+nabla^2` and
`omega^2=|k|^2+m^2`. A static profile is meaningful only for a component and
geometry compatible with the divergence constraint. The frozen half-line
case is a tangential component `A_y(x)` with `A_y(0)=A0` and decay at
infinity, which selects `A0*exp(-m*x)` and inverse length `m`; the general ODE
also includes a growing branch. The massless limit has a different constraint
structure and no finite positive penetration length.

## Candidate Preregistration

The candidates are frozen independently of the queue-exposed formulas.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal M2 audit | Hash-pinned source and dossier | Source declarations | Retains only convention-consistent conditional consequences | AST, data-flow, process, guard, and mutation audit |
| B | Free Proca theorem | Declared mostly-plus source-free action | `A_mu,m` | Euler equation, derived divergence constraint, massive dispersion | Exact variation, divergence, and plane-wave derivation |
| C | Transverse half-line BVP | Tangential component, boundary value, decay | `A0,m` | Unique decaying exponential and inverse length | General ODE solution, branch exclusion, and longitudinal counterexample |
| D | C-GSM composition | Accepted quadratic coefficient plus declared kinetic action | `M2,K` | Physical quadratic parameter uses the kinetic metric | Canonical and noncanonical mode calculation |
| E | London and vortex comparison | Separately declared actions and dictionaries | Model-specific | Shared equation shape does not identify physical systems | Premise and observable map comparison |
| F | Accepted composition only | Existing accepted claims | No new parameter | No new claim if definition-level | Registry, source, and API nonduplication |
| G | Physical countermodels | Same profile with distinct dictionaries | External interpretation | Exponential shape alone identifies no Meissner or weak sector | Same-equation countermodels |
| H | Governance closure | Frozen graph and registry | None | Pending or green sources grant no authority | Dependency, consumer, queue, release, docs, and memory replay |

## Selection Criteria and Blinding

Selection is ordered by explicit metric, action, field-strength, mass and
variation conventions; positive massive dispersion; derivation of the
constraint rather than gauge-fixing language; correct massive and massless
limits; component geometry and boundary data; growing-branch exclusion;
separation of mass coefficient, kinetic normalization, pole, material
response, and observable dictionary; accepted-framework compatibility;
mutation sensitivity; alternative dictionaries; assumption economy;
reusability; nonduplication; and complete semantic-consumer closure.
Queue-exposed `M_W`, `lambda_W`, and Meissner values do not select a theorem or
threshold. The remaining body and dossier stay closed until this contract and
matching manifest are committed.

## Proposed Claim Delta

Source-aware nonduplication reserves `C-PRC-001` through frozen revision 0001.
It depends on C-GSM-001 only for the final conditional lower-doublet
composition. The claim starts from a separately declared source-free Proca
action in the frozen mostly-plus convention, derives its full vector Euler
equation, nonzero-mass divergence constraint, transverse massive wave and
plane-wave dispersion, and the unique decaying tangential half-line profile.
For positive one-mode kinetic coefficient `kappa` and quadratic coefficient
`q`, it uses `m^2=q/kappa`; only with a separately declared canonical free
action may C-GSM-001's `q=g^2v^2/4` give `m=gv/2` and inverse length
`2/(gv)`. It establishes no London current, Meissner material response,
stationary condensate, physical W boson, Standard Model sector, observation,
or substrate realization.

## Source-Aware Classification

The unchanged source exits zero and prints all seven passes, but its headline
does not survive. CHECK1 repeats C-GSM-001's conditional coefficient after
declaring the lower-doublet inputs. CHECK2 varies a scalar Klein-Gordon proxy,
not the displayed vector action, and incorrectly describes the massive
divergence constraint as a Lorenz-gauge choice. CHECK3 is the static equation
only for a compatible transverse component. CHECK4 directly verifies one
decaying exponential, but its branch predicate uses `has(decaying) OR
has(growing)`, imposes neither boundary nor decay data, and would pass a
general solution containing only the growing branch.

CHECK5 does not test a physical Meissner identification. Its declared
superconductor mass-squared is unused, its two inverse-length checks are
definitions, and the `e -> g/2` substitution is a relabeling without a London
current, Maxwell/material action, field dictionary, or observable. CHECK6
solves a separately asserted on-shell relation rather than deriving it from
the full vector equation. CHECK7 correctly evaluates the conditional
`v -> 0+` algebra, but it does not prove a physical unbroken substrate phase;
at zero mass the Proca divergence constraint is no longer derived.

The original Proca paper supports deriving the divergence constraint from the
nonzero-mass vector equations. London 1935 supplies material-specific
electromagnetic equations tied to the Meissner observation, while Anderson
1963 discusses a solid-state analogy through current response. None supplies
the source's exact W/substrate identification. Accepted EM5 instead supplies
a massive scalar-QED2 vacuum-polarization theorem whose fixed-mass low-Q term
is kinetic and whose fixed-Q massless limit diverges; it is not the source's
claimed finite Schwinger mass template for this scalar field.

## Implementation and Oracle Plan

SymPy exact tensor-component algebra and variational identities are the
primary oracle because the requested theorem is algebraic and linear. The
campaign must independently derive the Euler expression by differentiating
the declared density, verify antisymmetry makes the double divergence vanish,
derive the wave equation only after the massive constraint, and check the
plane-wave dispersion. Exact constant-coefficient ODE algebra must derive both
branches before boundary and decay data select the half-line solution. A
fresh route must reconstruct these objects without importing the canonical
helper; numerical sampling is only regression coverage and cannot count as an
independent proof.

The importable boundary will use pure APIs
`mostly_plus_proca_momentum_evidence`,
`transverse_half_line_proca_evidence`, and
`normalized_proca_mode_evidence`. Mutations change the mass sign, metric sign,
mass to zero, field-strength sign pairing, kinetic normalization, component
orientation, boundary data, and decay condition.
Countermodels retain the same exponential equation under different physical
dictionaries. The compatibility preflight is explicit: canonical integration
uses `trapezoid_integral`, mutable current-environment scripts use
`np.trapezoid`, and executable direct, imported, or dynamic `np.trapz` access
is forbidden. If immutable M2 aborts only because of legacy NumPy spelling,
an alias backed by `np.trapezoid` may reproduce it and the compatibility event
is recorded rather than treated as scientific failure. This exact campaign
should require no quadrature.

## Attempts and Continuation

Every action-sign, metric, constraint, component, branch, boundary,
kinetic-normalization, compatibility, dependency, consumer, or verifier
failure is preserved append-only with its mechanism and a materially
different next attempt. Technical invocation failures are repaired without
changing the science; source overclaims yield to another registered
candidate.

## Debt Ledger

The ledger tracks source, dossier, proposal, and preexposure hashes; all seven
predicates and one assertion; metric, action, mass sign, field strength,
variation, divergence constraint, wave operator, dispersion, component
geometry, general ODE branches, boundary and decay data, massless limit,
kinetic metric, C-GSM composition, London and Meissner premises, physical
ceilings, six candidate dependencies, semantic and lexical consumers,
compatibility, nonduplication, disposition, generated state, and parent
continuation. Every item must be derived, declared, rejected, or excluded.

## Review and Promotion Plan

Every affected claim receives individual review. M2 receives a terminal
disposition retaining exact conditional mathematics while naming action,
geometry, boundary, normalization, and physical ceilings. Any distinct
theorem is extracted into pure APIs and focused tests only after a frozen
source-aware revision. Primary, independent, graph, compatibility,
dependency, consumer, nonduplication, release, queue, documentation, and
memory paths are replayed. One integrated gate runs at the final promotion
boundary; after it, only record-sensitive checks are repeated.

## Done Gate

P155 closes only when the action and metric conventions, Euler variation,
derived divergence constraint, wave and dispersion signs, transverse
component geometry, both static ODE branches, boundary and decay selection,
massless and noncanonical-kinetic limits, all seven source predicates,
physical content, compatibility, semantic consumers, generated state, and
debt ledger close through accepted APIs or a reviewed addition. A physical
Meissner medium, London current, W pole, condensate, weak sector, or substrate
mechanism additionally requires a governed gauge-scalar or material action,
stationary state, field normalization, current and observable dictionary, and
evidence; equation shape cannot replace them.

## Cross-References

See M2, M2-dossier, C1, EM5, EM6, M1, W2, W7, C-GSM-001, C-NAG-001,
C-GAU-001, C-VTX-001, C-EFT-001, C-VAC-001, C-QBL-001, P026, P059, P135,
P147, P151, P153, P154, `gauge_scalar_mass.py`, `nonabelian_gauge.py`,
`abelian_higgs_vortex.py`, and the parent migration effort.
