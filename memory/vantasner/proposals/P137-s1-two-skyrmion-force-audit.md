---
description: Audit S1's two-Skyrmion finite-range orientation-dependent force claim
author: vantasner
created: '2026-08-09T06:20:00Z'
updated: '2026-08-09T07:30:00Z'
tags: [substrate-framework, campaign-proposal, skyrmion, interaction, migration-S1]
category: proposals
confidence: established
status: archived
---
# P137 S1 Two-Skyrmion Force Audit

## Question and Positive Deliverable

P137 must reproduce and adjudicate S1's claim that two B=1 Skyrmions produce a
finite-range orientation-dependent nucleon-nucleon force through a sourced
refractive-index profile and/or asymptotic field interaction. The positive
deliverable is a distinct importable, input-explicit two-center interaction
theorem with exact sign, range, orientation, subtraction, and force conditions,
or an exact accepted composition proving that every supportable predicate is
already governed together with a terminal predicate-level S1 disposition. A
rejected nucleon narrative or missing full-field solution alone cannot complete
the campaign.

## Base Release and Provenance

The accepted base is v0.104.0 at scientific commit `3b0b7e7`; the parent
migration checkpoint is `3eef562`. S1 is pinned to
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`, path
`merged-framework/bridges/phase-4/bridge_S1_nn_force_two_skyrmion.py`, SHA-256
`ebe1ba930be26f17671d8e82779d14fc00e7a8b988a4aada722a32d0d9328ddd`.
Its dossier is pinned separately at SHA-256
`d3536930433f3d02b86f15735a40499ac2e4e1614a27743f88431719d7ba2079`.

The generated queue exposes eleven literal check calls, two assertions,
symbolic and numeric oracle hints, and dependencies B1, G1, G2, S5, and T2B.
B1, G1, and G2 remain pending and grant no premise. S5 is qualified through
C-VIR-001, C-MED-001, and C-SK-001; T2B is qualified through C-VAR-001,
C-CC-001, and C-VIR-001. The predecessor worktree contains excluded later
Phase 47/48, engineering, and memory work; the pinned S1 and dossier hashes
match the committed baseline. The S1 body, check values, and comparators remain
unopened at this freeze.

## Invariants, Conventions, and Allowed Imports

C-CC-001 supplies the exact coordinate-time equation of a separately declared
one-coordinate optical action. Its index profile is an input; it is not a full
3D two-body reduction or a force between physical objects. C-MED-001 proves
that density-only common constitutive scaling produces no index gradient.
C-VIR-001 and C-SK-001 are conditional algebraic relations and derive no
Skyrme action, field, baryon, pion scale, or interaction.

C-RMAP-001, C-RPROF-001, and C-RPROF-002 may be used only as declared
single-map and single-profile Skyrme-model surfaces with their accepted
ceilings. They supply no full two-center field, minimizer, physical baryon,
binding energy, or nucleon map. P137 may separately declare an action,
linearized field, mass and kinetic normalization, two-center ansatz, separation
and relative orientation, source profile, boundary data, and self-energy
subtraction. Every such declaration remains visible in the claim.

A two-body force is defined only after a real interaction energy
`E_int(R,O)` is constructed by a declared isolated-self-energy subtraction;
the radial force is `-partial_R E_int` at fixed orientation. Attraction,
finite range, and most-attractive orientation are distinct predicates. The
campaign may use exact SymPy algebra and the shared numerical machinery, but
mutable sampled integration uses the canonical helper or `np.trapezoid`, never
`np.trapz`.

## Candidate Preregistration

Six candidates cover the supportable mathematical and field-theoretic routes.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal S1 reconstruction | Every source import and profile | Source-defined | Some predicates may survive individually | Claim-by-claim AST, equation, domain, and sensitivity audit |
| B | Accepted optical composition | Supplied radial index plus C-CC-001 | Profile amplitude/range, c0, coordinate map | Exact conditional acceleration but no Skyrmion ontology | Derive sign/range and arbitrary-profile counterfamilies |
| C | Linearized massive-field interaction | Declared triplet/scalar action and two far-field sources | Kinetic coefficient, mass, source/dipole tensors, R, orientation | Natural finite-range asymptotic theorem if all tensors close | Independent Green-function/cross-energy derivation and orientation mutations |
| D | Full nonlinear two-Skyrmion energy | Declared Skyrme action, topology, ansatz or solver | Couplings, grid/domain, R, orientation, subtraction | Strongest physical-model object but highest assumption/numeric cost | Refined energy/force surface with independent method and isolated limit |
| E | Accepted composition and terminal mapping | Existing claims only | None beyond accepted inputs | Likely if source only differentiates assigned profiles | Nonduplication and exact predicate mapping |
| F | Governance closure | Accepted authority order | None | Narrow claim or composition and terminal disposition | Dependencies, consumers, impact, compatibility, queue, docs, and memory |

## Selection Criteria and Blinding

Selection is ordered by accepted dependency closure; explicit action, fields,
topology, source, subtraction, separation, and orientation; natural framework
fit; correct units, signs, isolated and large-separation limits; finite-range
asymptotics; full orientation coverage; independent derivation; mutation
sensitivity; numerical refinement where genuinely needed; parameter economy;
reusable API value; consumer compatibility; and nonduplication.

The queue headline and dependency names are known, but the S1 body, check
literals, curves, and cited nuclear values remain unopened. This contract
freezes the candidate set and structural criteria before that gate. A familiar
Yukawa shape, an attractive sampled interval, or a favored orientation cannot
select the interaction concept.

## Proposed Claim Delta

P137 provisionally reserves C-SKY-001 for a distinct conditional two-center
interaction theorem, if one closes with the action, sources, normalization,
self-energy subtraction, orientation tensor, asymptotic error, and force sign
explicit. Repository-wide registry, campaign, and durable-memory searches find
no prior C-SKY-001; rejected provisional C-SK-002 remains reserved and is not
reused. C-SKY-001 may depend on accepted conditional Skyrme or optical claims
only when their exact hypotheses are genuinely used. If the exact surface is
already governed, the provisional identifier remains unpromoted and S1 closes
through composition.

Direct reverse consumers are PG4 and PN6, both qualified, plus pending WN6,
WM7, and WM8. Their passing tallies or later narratives cannot grant S1
authority. Every direct and relevant transitive consumer will be hash-pinned
and replayed before adjudication.

## Implementation and Oracle Plan

The primary route will hash, parse, and execute S1 after the freeze, map all
eleven predicates, inventory its actual action/profile/orientation objects, and
compare each formula with accepted claims. Exact radial and orientation algebra
uses SymPy. A linearized field candidate requires a fresh Green-function or
integration-by-parts derivation that does not import the canonical interaction
helper. A nonlinear field candidate requires a declared mesh, domain,
discretization, boundary data, solver status, energy norm, subtraction,
separation sampling, and mesh/domain/tolerance refinement plus an independent
method or asymptotic limit.

Mutations cover source amplitude and sign, range or mass, kinetic
normalization, separation, relative orientation, self-energy subtraction,
boundary data, and zero-source and large-separation limits. A selected channel
must be tested against the complete declared orientation family. Numeric curve
fits are regression evidence when exact differentiation fixes their slopes.
The compatibility preflight detects direct, imported, dynamic, and eager-
default legacy NumPy integration access. Mutable code uses exact integration,
the canonical helper, or `np.trapezoid`; immutable source receives only a
recorded alias-only replay if required.

GitNexus and direct search will cover any changed canonical symbol and all
reverse consumers. Campaign verifiers pin their own source and frozen proposal
hashes and do not depend on a future queue or mutable current release.

## Attempts and Continuation

Attempt 0001 freezes this contract before S1 body inspection or execution.
Every failed action derivation, field representation, orientation oracle,
source replay, numerical solver, independent route, or governance operation
will be preserved with its mechanism and next materially different repair.
Failure of literal S1 triggers Candidates B through F and cannot complete the
positive object by itself.

## Debt Ledger

The ledger tracks source predicates, action and field content, topology,
two-center construction, source profile, separation, orientation, subtraction,
force sign/range, numerics, physical scope, dependencies, consumers, and
canonicalization.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| S1 executable surface is not freshly audited | Hash, execute, AST/data-flow audit, and map all eleven predicates | closed |
| No accepted two-center interaction energy exists | Derive a distinct input-explicit theorem or prove exact accepted composition | closed |
| Index source may be assigned rather than derived | Inventory the source equation and construct amplitude/range counterfamilies | closed |
| B=1 and nucleon labels may lack an accepted map | Audit action, topology, state, and ontology; retain explicit ceilings | closed |
| Orientation ordering may compare only selected channels | Define the full orientation variable and prove or bound its extrema | closed |
| Force sign and range may be fitted | Derive them from E_int with exact limits and load-bearing mutations | closed |
| Numerical evidence may lack refinement or subtraction control | State solver and errors; refine mesh/domain/tolerance and cross-check a soluble limit or second method | closed |
| Dependencies, consumers, and novelty are incomplete | Audit B1/G1/G2/S5/T2B, accepted nearby claims, reverse consumers, and graph impact | closed |
| Registry, disposition, docs, queue, and memory are unsynchronized | Promote only reviewed distinct claims or close composition, then regenerate governed state | closed |

## Adjudication Result

P137 accepts C-SKY-001 in v0.105.0 as an exact conditional interaction theorem
for a separately declared massive triplet field with two dipole sources. The
self-subtracted cross energy, complete SO(3) extrema, attractive-channel force,
massless limit, and exponential large-separation behavior were derived by the
canonical implementation and a fresh Cartesian-Hessian review. The theorem
does not construct the nonlinear Skyrme model, B=1 states, nucleons, binding,
an absolute scale, or a substrate sector.

S1 is terminally qualified through C-CC-001, C-VIR-001, C-RPROF-001, and
C-SKY-001. Its numerical force omits a load-bearing factor of `1/R`, its
orientation comparison samples only two assigned channels, and its declared
index and source profile do not derive a two-Skyrmion energy or nucleon force.
The primary verifier passes 26 checks, the independent route passes 13, the
focused package boundary passes 28 tests, and the pinned 11-node source graph
replays 157 predicates. Immutable G1 and B1 receive isolated aliases backed by
`np.trapezoid`; every mutable P137 surface uses current APIs or exact algebra.
All campaign debt is closed.

## Review and Promotion Plan

C-SKY-001 receives an individual claim review only if it is distinct, exact or
properly resolution-bounded, sensitive, and independently derived. Source
adjudication separately decides every S1 predicate. Reusable interaction,
orientation, or solver logic moves under `src/substrate_framework/` with
focused tests; literal orchestration stays in P137. A terminal qualification
must name every surviving accepted mapping and rejected physical clause with
durable evidence. Any release, disposition, queue, generated documentation,
and accepted-memory transaction is validated once at the changed boundary.

## Done Gate

P137 closes only with the complete positive interaction or composition object,
claim-level review if needed, terminal S1 disposition, sensitive primary and
independent evidence, dependency and consumer replay, synchronized governance,
and an empty campaign ledger. A no-go for the nucleon interpretation or a
failed full-field route is attempt evidence and does not by itself finish the
campaign.

## Cross-References

See P007, P008, P063, P084, P104, P105, B1, G1, G2, S1, S5, T2B,
C-VAR-001, C-CC-001, C-MED-001, C-VIR-001, C-SK-001, C-RMAP-001,
C-RPROF-001, C-RPROF-002, v0.104.0, and the parent migration effort.
