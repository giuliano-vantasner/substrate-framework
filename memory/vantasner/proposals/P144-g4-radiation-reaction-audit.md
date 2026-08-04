---
description: Audit G4's radiation-reaction and internal-mode backreaction claim
author: vantasner
created: '2026-08-09T17:00:00Z'
updated: '2026-08-09T17:00:00Z'
tags:
- substrate-framework
- campaign-proposal
- radiation-reaction
- self-force
- migration-G4
category: proposals
confidence: exploratory
status: active
---
# P144 G4 Radiation-Reaction Audit

## Question and Positive Deliverable

P144 must reproduce and adjudicate G4's claim that a supplied radiated power
determines both a reaction force and internal-mode backreaction. The positive
deliverable is an importable exact field-plus-source or explicitly conditional
effective balance theorem that closes every declared energy reservoir,
generalized force, allocation, sign, dimension, causal-history, regularization,
initial, boundary, and limiting premise. A power identity, damping sign, failed
candidate, or honest statement of nonuniqueness does not complete the campaign.

## Base Release and Provenance

The accepted base is v0.110.0 at framework checkpoint `5e56737`, with scientific
promotion base `d5e840f`. The source baseline is `/home/dan/substrate` commit
`6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`. G4 is pinned at
`merged-framework/bridges/phase-5/bridge_G4_radiation_reaction_self_force.py`,
SHA-256 `308c8d82aff062fb0f0254498fb2bdb19fe6bdc207036cb0fa73643d3608c799`.
Its dossier SHA-256 is
`e88a3bdc12599f72c4092f374fa73ebf3c7632c6ae7e70f5b6c238c38337a39b`.
The source and dossier bodies, literal predicates, output, and numeric values
remain unopened before this freeze. The queue exposes ten static checks, one
assertion, symbolic and numeric hints, dependencies G1, G2, G3, T2A, and T2C,
and no result excerpt. G4 remains pending adjudication.

## Invariants, Conventions, and Allowed Imports

P144 preserves the separation between radiated field flux and source dynamics.
C-RAD-001 supplies exact retarded flux and source work for a prescribed
one-dimensional point-source amplitude but no self-force. C-SG-002, C-SG-008,
and C-SG-012 supply normalized rest energy, constant boosts, and stress only;
promoting velocity or internal frequency to time-dependent coordinates requires
an explicit adiabatic action. C-GOR-001 is effective geometry, C-STG-001 is a
homogeneous cosmology, and C-OG-004 is profile averaging. Exact generalized
energy balance and declared Rayleigh calculus are permitted. Primary literature
may be read after freeze for regularization, causality, near-field energy, and
effective-equation scope only.

## Candidate Preregistration

Six candidates separate literal replay, balance classification, a genuine
field-plus-source derivation, a conditional effective model, countermodels, and
governance.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal G4 reproduction and predicate audit | Hash-pinned source only after freeze | Source values | Mixed narrow identities and overclaim likely | Native or alias replay plus AST and data-flow audit |
| B | Exact generalized energy-balance and allocation family | Differentiable declared energy and all work reservoirs | Allocation coordinates | Native and parameter-economical | Derive the complete affine force family and rank |
| C | Retarded field-plus-source self-force | Explicit source degrees of freedom, causal Green function, coincidence prescription | Action and regulator data | Strongest physical closure but highest assumption cost | Variation, finite regularized limit, conservation, and counterterms |
| D | Declared Rayleigh effective dynamics | Local Markovian dissipation as a premise | Nonnegative damping matrix | Compatible conditional extension | Energy identity, existence, limits, and coefficient mutations |
| E | Turning-point, near-field, external-work, and alternate-allocation countermodels | Same total radiated power under changed hidden structure | No fitted comparator | Exposes nonuniqueness and singular divisions | Same P with distinct forces or internal rates |
| F | Claim, dependency, consumer, compatibility, and release closure | Governance contract | None | Required transaction | Full downstream replay and empty debt |

## Selection Criteria and Blinding

Selection is ordered by a complete action or explicitly conditional effective
law, causal and regularization closure, all-reservoir energy bookkeeping,
generalized-force rank, signs and dimensions, nonsingular domains, initial and
boundary data, known limits, mutation sensitivity, parameter economy,
reusability, dependency closure, and nonduplication. G4 output and numeric
comparators remain blinded until this proposal, source and dossier hashes,
candidate set, force conventions, thresholds, compatibility plan, and done gate
are committed.

## Proposed Claim Delta

P144 provisionally reserves C-RR-001 for a distinct exact conditional radiation-
reaction balance or effective-dissipation theorem if complete closure,
sensitivity, nonduplication, and individual review pass. Registry, campaign,
and memory search found no prior use of C-RR-001 or C-RAD-002. No G4 headline,
physical self-force, or internal-mode law is imported. The accepted dependency
set will be the smallest exact closure selected after audit; pending source
units never become dependencies by citation.

## Implementation and Oracle Plan

The selected reusable surface will live under `src/substrate_framework/` with
pure exact APIs for the complete balance and allocation or Rayleigh ledger.
SymPy is the strongest oracle for exact chain rules, force-power contractions,
rank, domains, solutions, dimensions, and limits. A fresh independent route
will derive the same identity without importing the canonical module. If G4
contains SciPy evolution, it must state the equations, domain, data, method,
tolerances, solver success, mesh or timestep policy, stopping rule, error norm,
refinement, independent soluble limit, and load-bearing mutations; otherwise it
earns regression coverage only.

Compatibility preflight uses the shared AST auditor. Mutable code uses exact
algebra, `trapezoid_integral`, or `np.trapezoid`. G4's immutable direct
`np.trapz` shape receives only an alias backed by `np.trapezoid` if native
execution requires it, and no compatibility abort may select or reject a
scientific candidate. Primary, independent, focused, dependency, consumer,
generated, and mutation routes must all pass at the promotion boundary.

## Attempts and Continuation

Attempts remain append-only. A technical source, symbolic, integration,
regularization, solver, refinement, or representation failure is preserved and
repaired without weakening the scientific claim. A balance law that proves
only nonuniqueness triggers another positive effective or field-plus-source
candidate rather than closing the campaign as a no-go.

## Debt Ledger

P144 tracks source predicates, field and source actions, self-field
regularization, causal and boundary history, near-field energy, external work,
translation and internal reservoirs, allocation, signs, dimensions, source
dynamics, numerical controls, dependencies, consumers, compatibility, and
generated state.

| Debt | Discharge artifact | Status |
| --- | --- | --- |
| G4 executable and literal predicates are unopened | Hash, compatibility preflight, replay, AST/data-flow audit, and all ten predicates | open |
| Radiated power may be relabeled as a unique force | Complete generalized-force allocation and rank classification | open |
| Field self-force may omit action or regularization | Explicit source variation, causal prescription, coincidence treatment, and conservation | open |
| Internal energy may be double counted or assigned | All reservoirs, external work, near-field term, and allocation rule | open |
| Numeric evidence may be same-equation regression | Solver status, refinement, independent limit, and mutations | open |
| Dependencies consumers and novelty are incomplete | G1 G2 G3 T2A T2C, five reverse consumers, graph, cycles, and nonduplication audit | open |
| Registry disposition release docs queue and memory are unsynchronized | Individual review and one governed terminal transaction | open |

## Review and Promotion Plan

Any C-RR-001 candidate receives a fresh independent derivation and individual
claim review. G4 receives a terminal predicate-level disposition whether or not
a claim is promoted. A mixed source maps only accepted surfaces and records
every rejected force, internal-mode, gravity, material, physical, or substrate
clause. Release, queue, docs, accepted memory, proposal memory, and parent
effort change only at actual boundaries. The final attempt is prepared in
progress before one integrated gate and finalized afterward with record-
sensitive checks only.

## Done Gate

P144 closes only with a complete positive field-plus-source or explicitly
conditional effective radiation-reaction object, sensitive primary and
independent evidence, individual claim review, terminal G4 disposition, closed
dependencies and consumers, synchronized governed state, and an empty ledger.
A clean tally, supplied radiated power, energy-loss sign, damping ODE, or no-go
label does not complete the campaign.

## Cross-References

The governing references are P132, P133, P141, P142, P143, G1, G2, G3, G4,
T2A, T2C, C-RAD-001, C-SG-002, C-SG-008, C-SG-012, C-OG-004, C-GOR-001,
C-STG-001, provisional C-RR-001, v0.110.0, and the parent migration effort.
