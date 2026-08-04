---
description: Audit G5's medium-density and effective-Newton relation
author: vantasner
created: '2026-08-09T18:10:00Z'
updated: '2026-08-09T18:10:00Z'
tags:
- substrate-framework
- campaign-proposal
- medium-density
- dimensional-analysis
- identifiability
- migration-G5
category: proposals
confidence: exploratory
status: active
---
# P145 G5 Medium-Density and Effective-Newton Audit

## Question and Positive Deliverable

P145 must reproduce and adjudicate G5's claim that vacuum permittivity,
permeability, and a gravitational coupling determine a mechanical medium
density, strain-energy density, and linked relation for the effective Newton
constant. The positive deliverable is an exact, importable or accepted-API
composition that types every quantity in SI units, separates constitutive
premises from consequences, distinguishes linked outputs from parameter-free
predictions, preserves every conversion scale and free coupling, and closes all
dependencies and consumers. A dimensional objection, failed source claim, or
honest non-identifiability result alone does not complete the campaign.

## Base Release and Provenance

The accepted base is v0.111.0 at framework checkpoint `73ecbba`, with
scientific promotion base `e86930c`. The source baseline is
`/home/dan/substrate` commit
`6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`. G5 is pinned at
`merged-framework/bridges/phase-5/bridge_G5_Geff_medium_density.py`, SHA-256
`38a28bb452b055e7aa7894e1c31e3fcc98bfc5c6a8cbee2040aa003c62a4071a`.
Its dossier is pinned at
`merged-framework/bridges/phase-5/dossiers/G5-dossier.md`, SHA-256
`972605f48b9941c6a8d054c4bd7ca173d7cf6d05d370d92ac59db18d2a61e427`.
Both bodies, literal predicates, full output, and further comparator material
remain unopened before this freeze. The generated queue necessarily exposed
G5's headline, four displayed relations, rounded values, fifteen static and
literal checks, one assertion, symbolic-only hints, and dependencies G1, G2,
G3, and G4. G5 remains pending adjudication. The predecessor worktree's
uncommitted Phase 47/48 and engineering files remain excluded.

## Invariants, Conventions, and Allowed Imports

P145 preserves the conditional status of every medium dictionary and the
source-typed status of every gravitational coupling. C-MED-001 and C-MED-002
derive exact consequences only after response laws, primitive scales, and a
density dictionary are declared; they do not identify SI vacuum constants with
a material. C-DIM-002 fixes powers only within one primitive basis, and
C-IDN-001 says rank cannot establish row provenance or physical independence.
C-GRV-001 requires the field operator and source dimensions before mapping
Newton G to a coupling. C-STG-001 uses natural units and an energy-stress source
and selects no physical kappa. C-RAD-001, C-GOR-001, and C-RR-001 supply no
material or Newton normalization. Qualified G1 through G4 contribute evidence,
not their rejected gravity or substrate narratives.

The exact SI base-dimension order is mass M, length L, time T, and electric
current I. The frozen columns are
`[epsilon_0]=(-1,-3,4,2)`, `[mu_0]=(1,1,-2,-2)`,
`[rho]=(1,-3,0,0)`, `[K]=[u]=(1,-1,-2,0)`,
`[c]=(0,1,-1,0)`, `[G]=(-1,3,-2,0)`, and
`[G/c^2]=(-1,1,0,0)`. A mechanical dictionary
`rho=lambda*epsilon_0`, `K=lambda/mu_0` needs a common dimensioned
conversion `[lambda]=(2,0,-4,-2)`; its ratio cancels from
`K/rho=1/(epsilon_0*mu_0)`. A dimensionless factor one-half cannot replace
that conversion, and `1/mu_0` alone is not an energy density. The current
BIPM SI Brochure is permitted after freeze for definition and unit provenance.
Official BIPM or NIST numerical constants remain behind the comparator gate.

## Candidate Preregistration

Seven candidates separate literal replay, SI typing, a repaired constitutive
dictionary, gravitational convention restoration, prediction rank,
countermodels, and governance closure.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal G5 reproduction and predicate audit | Hash-pinned source only after freeze | Source inputs | Narrow algebra may pass while units or independence fail | Native replay plus AST and data-flow audit of all fifteen predicates |
| B | Exact four-base-dimension SI ledger | SI quantity definitions | No fitted values | Native and decisive for every proposed equality | Dimension residuals under M,L,T,I and wrong-unit mutations |
| C | Common-conversion mechanical dictionary | Positive `epsilon`, `mu`, and dimensioned `lambda` | One free conversion scale | Wave speed closes while density and stiffness scales remain free | Exact substitution, rescaling orbit, and C-MED nonduplication |
| D | Source-typed gravitational coupling ledger | Declared Einstein operator and either energy- or mass-density source | Convention-specific c and hbar factors | Natural only when source type is explicit | Dimension solve and cross-convention mutation |
| E | Dependency and prediction-rank ledger | Exact positive inputs and provenance-bearing equations | All genuinely independent inputs | Algebraic outputs need not be parameter-free predictions | Log-Jacobian rank, left-null constraints, and arbitrary-target families |
| F | Alternate valid dictionaries and couplings | Same wave-speed product with varied common scale or free kappa | Conversion and coupling families | Same c with arbitrary rho, K, or G ratio | Constructive rescaling and free-parameter countermodels |
| G | Claim, dependency, consumer, compatibility, and release closure | Governance contract | None | Required transaction | Frozen graph replay and empty debt |

## Selection Criteria and Blinding

Selection is ordered by exact SI dimensional homogeneity, explicit premise and
source typing, genuine constraint or prediction rank, preservation of free
conversion scales and couplings, correct common-rescaling and convention
limits, mutation sensitivity, assumption economy, accepted-framework fit,
reusable value, consumer closure, and nonduplication. Numerical closeness and
the queue's already exposed rounded values are excluded from concept selection
and thresholds. The source body, check literals, full output, dossier body, and
official numerical constant values remain blinded until the proposal, hashes,
unit columns, coupling conventions, candidate set, criteria, compatibility
policy, and done gate are committed.

## Proposed Claim Delta

P145 reserves no claim identifier at freeze. C-MED-001 and C-MED-002 already
govern conditional response cancellation and the separately declared density
dictionary; C-DIM-002, C-IDN-001, and C-GRV-001 already govern dimension
powers, provenance-bearing rank, Newton dimensions, free coefficients, and
source normalization. Repository registry, campaign, module, and durable-memory
search found no reason yet to duplicate them. A new identifier may be proposed
only after source-aware nonduplication finds a distinct exact theorem with an
importable consumer; that requires an explicit proposal revision and renewed
freeze before implementation. G5 may map multiple accepted claims while its
unsupported subclaims receive a terminal qualified disposition.

The anticipated reverse consumers are W5, QCD1, SM1, OD, AS1, AS2, AS3, AS4,
and OD3. The first three remain pending; OD, AS1, AS2, and AS3 are qualified;
AS4 and OD3 are duplicate evidence. None gains authority merely by citing G5.

## Implementation and Oracle Plan

SymPy and exact integer dimension vectors are the strongest oracles for unit
residuals, constitutive substitutions, dependency matrices, ranks, nullspaces,
limits, and arbitrary-target families. The primary route may compose accepted
`constitutive`, `dimensional_analysis`, `scale_constraints`, and
`induced_gravity` APIs. A fresh independent route must rebuild the SI columns
and eliminate the common conversion without importing any new P145 helper.
A distinct exact theorem, if found, must become a pure package API with focused
tests; otherwise the campaign must reuse existing accepted APIs and avoid a
duplicate module or claim.

Every source predicate will be mapped to its evaluated object, inputs, units,
dependencies, sensitivity, and maximum verdict. Load-bearing mutations change
the density coefficient, common conversion, one permeability exponent, a c
power, kappa convention, input provenance, and free-scale orbit. Exact
countermodels preserve `epsilon*mu` while changing density or stiffness, and
preserve the displayed gravity ratio while changing free kappa. Numerical
constant evaluation is regression only and cannot establish the exact claim or
physical medium.

Compatibility preflight uses the shared AST auditor. Mutable code uses exact
algebra, `trapezoid_integral`, or `np.trapezoid`; it never uses
`np.trapz`. Immutable source receives an alias-only replay backed by
`np.trapezoid` only if native execution reveals a legacy integration access,
and such a version-only abort cannot select or reject a scientific candidate.
Primary, independent, focused, dependency, consumer, generated, and mutation
routes must close at the terminal boundary.

## Attempts and Continuation

Attempts remain append-only. A compatibility, symbolic-representation,
dimension-basis, convention, provenance, source-replay, or verifier failure is
preserved with its mechanism and repaired without weakening the intended
positive object. If the literal medium concept fails, P145 continues with the
dimension-valid common-conversion theorem or accepted-API composition. If that
surface is already accepted, P145 completes the exact mapping and source
adjudication without manufacturing a duplicate claim.

## Debt Ledger

P145 tracks every unit column, conversion factor, independent input, definition,
algebraic consequence, prediction-rank statement, coupling convention, source
predicate, comparator, dependency, consumer, compatibility event, and generated
record.

| Debt | Discharge artifact | Status |
| --- | --- | --- |
| G5 executable and literal predicates are unopened | Hash, compatibility preflight, replay, AST/data-flow audit, and all fifteen predicates | open |
| SI electric dimensions may be suppressed | Exact M,L,T,I ledger and dimension-residual mutations | open |
| Mechanical density or energy may be named without conversion | General dimensioned dictionary, scale orbit, and energy-density typing | open |
| Kappa conventions may mix natural and SI units | Source-typed coupling ledger with c and hbar restoration | open |
| Linked consequences may be called independent predictions | Dependency graph, log-rank, left-null, and arbitrary-target audit | open |
| Existing medium and gravity claims may be duplicated | Registry/module/campaign/memory nonduplication decision | open |
| Dependencies and reverse consumers are incomplete | G1 G2 G3 G4 plus nine reverse consumers and frozen graph replay | open |
| Queue disposition docs release and memory may diverge | Individual review or no-new-claim adjudication and one governed terminal transaction | open |

## Review and Promotion Plan

Any newly proposed claim receives a fresh independent derivation and individual
claim review; no identifier is currently reserved. G5 receives a
predicate-level terminal disposition whether or not a new claim is promoted.
A mixed unit maps only exact accepted surfaces and names every invalid unit,
free-parameter, independence, material, gravitational, empirical, and substrate
clause. A no-new-claim boundary leaves v0.111.0 unchanged. The queue, docs,
accepted memory, proposal memory, and parent effort change only at their proper
governance boundaries. A final attempt starts in progress before the single
integrated repository gate, is finalized afterward, and receives only
record-sensitive checks.

## Done Gate

P145 closes only when an exact positive unit-aware constitutive and coupling
ledger exists through accepted APIs or a distinct reviewed addition, all
fifteen predicates are sensitively adjudicated, G5 receives a terminal
disposition, dependencies and nine reverse consumers close, generated state
agrees, and the campaign ledger is empty. A passing source tally, correct
wave-speed product, numerically familiar vacuum constants, dimensional
criticism, free kappa, or no-new-claim decision alone does not complete the
campaign.

## Cross-References

The governing references are P008, P016, P065, P074, P141 through P144, G1
through G5, C-MED-001, C-MED-002, C-DIM-002, C-IDN-001, C-GRV-001, C-RAD-001,
C-GOR-001, C-STG-001, C-RR-001, v0.111.0, and the parent migration effort.
