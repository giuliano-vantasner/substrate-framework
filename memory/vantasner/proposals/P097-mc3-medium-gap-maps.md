---
description: Derive and audit the MC3 lattice and gas medium-gap maps
author: vantasner
created: '2026-08-04T16:00:00Z'
updated: '2026-08-04T16:00:00Z'
tags:
- substrate-framework
- campaign-proposal
- medium-gap
- migration-MC3
category: proposals
confidence: exploratory
status: active
---
# P097 MC3 Medium Gap Maps

## Question and Positive Deliverable

P097 must deliver importable exact conditional theorems for a physical
dimensionless-phase Frenkel-Kontorova chain and for the scale content of a
mixed-coordinate sine-Gordon equation. It must state exactly when an isotope
gap ratio reduces to a mass ratio, determine whether the self-induced-
transparency equation supplies a laboratory spectral gap, separate both from
host and nonlinear-breather selection, and terminally adjudicate MC3.

## Base Release and Provenance

The accepted base is `v0.82.0` at parent commit `f8290a0`; the latest
scientific transaction is P096 at `b0113d5`. The predecessor evidence is
pinned at `substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64` while later
dirty Phase 47/48 files remain excluded. MC3 is
`/home/dan/substrate/merged-framework/bridges/phase-27/bridge_MC3_per_medium_omega0.py`,
28,562 bytes, SHA-256
`74fbddc086781a0d61d5dd22effabf48d7ff37f47c6d97ebde0b2fb6186464a5`,
and git blob `8a6dc1e87bc2f46fe1ef6d56c2eb90afd2f363e4`.

MC3's complete source body was already inspected during P096's required
consumer audit. Fresh body or formula blinding is therefore impossible and is
not claimed. MC3 has not been executed under P097, its imported predecessor
self-tests have not been trusted, its primary literature has not been opened,
and additional consumer outputs have not been inspected.

Direct accepted sources are release `v0.82.0`, C-LAT-001, C-MED-003,
C-SG-017, C-SG-018, and C-DIM-002 with their canonical modules and adjudicated
evidence. Memory recall found only the parent frontier and older conditional
unit-basis records, not an accepted material or mixed-coordinate theorem that
would settle MC3.

## Invariants, Conventions, and Allowed Imports

The lattice field is a dimensionless real phase. Its site kinetic coefficient
is an inertia `I` with dimensions energy times time squared, the bond and
on-site coefficients `K,V0` have energy dimensions, and the site spacing `a`
has length. If a physical displacement is `q=b*u`, then and only then does a
bare particle mass enter as `I=m*b^2`. The general gap ratio must retain
potential, phase-scale, and effective-inertia differences until independently
fixed.

The gas equation `theta_z_tau=g*sin(theta)` uses one length coordinate and one
time coordinate unless a different map is explicitly declared. Therefore
`g` has inverse-length-inverse-time dimensions, whereas an angular-frequency
squared has inverse-time-squared dimensions. A light-cone or laboratory map,
including its scale and sign, must precede any gap interpretation.

C-LAT-001 supplies normalized structure, C-MED-003 supplies continuum units,
C-SG-018 supplies the conditional linear gap, and C-SG-017 supplies one exact
nonlinear solution only inside its model. Hash-pinned MC3, ME3, rung165, and
rung176 are evidence after the freeze. Primary McCall-Hahn literature may be
opened after the freeze to audit the cited regime and equations, not imported
as accepted framework truth. MC4 and all material and engineering consumers
remain nonauthoritative.

## Candidate Preregistration

The competing constructions are frozen before MC3 execution, imported
self-test execution, primary-literature inspection, or additional consumer
output inspection.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal MC3 reproduction | Pinned source environment | Source symbols and imports | Tally validates only implemented predicates | Hash, AST, process, imports, output, predicate ledger |
| B | General FK phase chain | Declared dimensionless phase action | I,K,V0,a | Gap is sqrt(V0/I), with exact lattice band | Variation, Fourier symbol, units, mutations |
| C | Physical displacement lift | q=b*u and mass kinetic energy | m,b | I=m*b^2 and gap=sqrt(V0/(m*b^2)) | Coordinate substitution and dimension matrix |
| D | General isotope ledger | Two supplied host parameter sets | I_H,I_D,V_H,V_D,b_H,b_D | Ratio retains every parameter; sqrt2 is conditional | Exact quotient and counterfamilies |
| E | Effective-parameter alternatives | Isotope-dependent potential or phase scale allowed | parameter ratios | Same isotope labels realize non-sqrt2 ratios | Constructive arbitrary-ratio families |
| F | Mixed z-tau SG | Declared length and time coordinates | g | Plane waves obey k*Omega=g and have no finite band floor | Dimensions, Fourier substitution, limits |
| G | Explicit hyperbolic map | Declared light-cone scale and orientation | L0,T0 or velocity | Standard SG coefficient needs a map and retains scale freedom | Chain rule, rank/nullspace, sign mutations |
| H | Primary SIT audit | Exact cited paper regime | published coefficients | Citation may support a conditional area equation, not extra claims | Primary equations, units, assumptions, terminology |
| I | Gap/existence separation | Accepted linear and nonlinear ceilings | none | Positive curvature is not sufficient for a breather | Free-field and alternative-potential countermodels |
| J | Consumer/nonduplication audit | Hash-pinned downstream use | none | Consumers cannot backfill material or scale premises | Hashes, dependency flow, registry and API comparison |

## Selection Criteria and Blinding

Selection prioritizes accepted dependency closure, action and coordinate-map
derivation, dimensional and Fourier consistency, explicit effective-parameter
assumptions, honest treatment of isotope approximations, scale identifiability,
mutation sensitivity, counterfamilies, correct limits, parameter economy,
natural framework fit, and consumer closure. Source tallies, imported self-test
counts, the numerical closeness of real isotope masses to two, and later
engineering agreement cannot select a theorem.

MC3's body and formulas are already exposed. P097 freezes the still-load-
bearing unit, coordinate, exactness, literature, existence, consumer, and
claim criteria before source execution or comparator inspection.

## Proposed Claim Delta

P097 reserves `C-LAT-002` for the conditional physical phase-chain and isotope
ledger and `C-MED-004` for the mixed-coordinate sine-Gordon scale theorem.
Repository-wide registry, campaign, proposal, memory, source, and test search
found no collision. Proposed dependencies are C-LAT-001 and C-DIM-002 for the
lattice claim, and C-MED-003 plus C-SG-018 for the coordinate claim. Neither
claim challenges or supersedes accepted work.

Anticipated consumers are a pure medium-gap module, package exports, focused
tests, P097 verifiers, governance, release, generated docs and memory, and
later audited MC4/MD/engineering units. Pending consumers cannot broaden the
claims.

## Implementation and Oracle Plan

Reusable exact dataclasses and functions will live under
`src/substrate_framework/` and expose phase-chain coefficients, displacement
conversion, dispersion, isotope ratios, mixed-coordinate dimensions,
plane-wave relation, and coordinate normalization without import-time work.
SymPy is the strongest oracle for variation, dimension matrices, Fourier
substitution, ratios, nullspaces, limits, and counterfamilies. Literature
inspection can validate citation scope only; it cannot replace the exact
oracle or accepted imports. No numerical solver or quadrature is needed, and
no version-specific NumPy integration alias is permitted.

The primary route calls canonical APIs. An independent route derives the
action and coordinate map without importing them. Mutations change kinetic
inertia, drop `b^2`, swap isotope ratios, vary host potential, confuse
inverse-length-inverse-time with inverse-time-squared, and change light-cone
signs. Focused replay covers lattice scalar, dimensional sine-Gordon,
dimensional analysis, and accepted spectrum tests.

## Attempts and Continuation

Every source, literature, representation, or verifier failure is appended. A
dimensionally incomplete material map is repaired to the strongest exact
conditional theorem and its broader source reading is qualified; failure of
one channel does not terminate the positive two-ledger objective.

## Debt Ledger

The ledger tracks source reproduction, imported self-tests, action and field
units, lattice variation and dispersion, displacement scale, isotope
assumptions and counterfamilies, mixed-coordinate dimensions and transforms,
primary-literature scope, nonlinear-existence ceiling, consumers,
nonduplication, independent review, generated state, and source disposition.
It must be empty before promotion.

## Review and Promotion Plan

Each proposed claim receives its own independent claim review. Accepted logic
must be importable and tested; every MC3 predicate and named import and
consumer receives a durable verdict. Promotion, if earned, updates the
registry, a pinned release, qualified MC3 disposition, generated queue, docs,
accepted memory, and parent effort. A single integrated workflow gate is
followed only by record-sensitive validation.

## Done Gate

P097 closes only when both positive conditional ledgers exist, dependencies
and consumers replay, primary and independent exact oracles are sensitive,
every MC3 subclaim and external import is terminally adjudicated, generated
state agrees, and the campaign debt ledger is empty. Otherwise the next
materially distinct attempt remains active.
