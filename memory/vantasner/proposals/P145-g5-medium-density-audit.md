---
description: Audit G5's medium-density and effective-Newton relation
author: vantasner
created: '2026-08-09T18:10:00Z'
updated: '2026-08-09T19:24:00Z'
tags:
- substrate-framework
- campaign-proposal
- medium-density
- dimensional-analysis
- identifiability
- migration-G5
category: proposals
confidence: established
status: archived
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
G3, and G4. G5 was pending adjudication at freeze and is now qualified by
P145. The predecessor worktree's
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

## Proposal Revision

Revision 0001 activates preregistered Candidate C after native reproduction and
source-aware nonduplication. The source's central defect is not merely C-MED-001's
already accepted common-response cancellation: it substitutes the actual SI
vacuum coefficients into an untyped mechanical dictionary, and no accepted API
currently states the required dimensioned calibration or its rescaling orbit.
The revision therefore reserves collision-free C-MED-005 before implementation.
The initial frozen proposal, candidate ordering, SI columns, selection criteria,
and source-value exclusion remain unchanged.

C-MED-005 will state the exact SI mechanical-conversion theorem. With SI base
rows M,L,T,I, a multiplicative dictionary


`rho=a*epsilon` and `K=b*mu_inverse` requires both `a` and `b` to have dimension
`(2,0,-4,-2)`. It gives `c_m^2=(b/a)/(epsilon*mu)` and hence the electromagnetic
speed exactly iff `a=b` for positive factors. The common factor then remains a
free calibration that rescales density, stiffness, and energy while leaving the
speed fixed. For dimensionless strain `xi`, `u=K*xi^2/2`; under a common factor,
`u/c^2=a*epsilon*xi^2/2`, which is not the inertial density `a*epsilon` at unit
strain. Bare `epsilon/2` is not an SI mass density and bare `1/(2*mu)` is not an
SI energy density. The theorem derives no material, field amplitude, calibration,
gravity coupling, observation, or substrate mechanism.

## Proposed Claim Delta

P145 reserved and promoted C-MED-005 under revision 0001. Repository registry,
campaign, module, and durable-memory searches found no prior use of that
identifier before promotion or an accepted theorem carrying the SI conversion-factor dimension,
two-factor speed ratio, common-scale orbit, and strain-energy ceiling together.
C-MED-001 and C-MED-002 remain dependencies or neighboring ceilings rather than
duplicates: their response variables already have declared mechanical dimensions
and their density map is explicitly a premise. C-DIM-002, C-IDN-001, and
C-GRV-001 continue to govern dimension powers, provenance-bearing rank, Newton
dimensions, free coefficients, and source normalization. G5 may map C-MED-005
and older accepted claims while its unsupported subclaims receive a terminal
qualified disposition.

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
| G5 executable and literal predicates are unopened | Hash, compatibility preflight, replay, AST/data-flow audit, and all fifteen predicates | discharged |
| SI electric dimensions may be suppressed | Exact M,L,T,I ledger and dimension-residual mutations | discharged |
| Mechanical density or energy may be named without conversion | General dimensioned dictionary, scale orbit, and energy-density typing | discharged |
| Kappa conventions may mix natural and SI units | Source-typed coupling ledger with c and hbar restoration | discharged |
| Linked consequences may be called independent predictions | Dependency graph, log-rank, left-null, and arbitrary-target audit | discharged |
| Existing medium and gravity claims may be duplicated | Registry/module/campaign/memory nonduplication decision | discharged |
| Dependencies and reverse consumers are incomplete | G1 G2 G3 G4 plus nine reverse consumers and frozen graph replay | discharged |
| Queue disposition docs release and memory may diverge | Individual review and one governed terminal transaction | discharged |

## Review and Promotion Plan

C-MED-005 received a fresh independent derivation and individual claim review.
G5 received its predicate-level qualified disposition. The disposition maps
only exact accepted surfaces and names every invalid unit, free-parameter,
independence, material, gravitational, empirical, and substrate clause. Release
v0.112.0, the queue, docs, accepted memory, proposal memory, and parent effort
advance only at their proper governance boundaries. Final attempt 0007 began in
progress before the single integrated repository gate, finalized afterward,
and receives only record-sensitive checks.

## Adjudicated Outcome

P145 promotes C-MED-005 as a symbolic-verified compatible extension depending
on C-MED-001 and qualifies G5 through C-MED-001, C-MED-005, C-IDN-001, and
C-GRV-001. The canonical and independent routes pass 36 and 20 checks, 17
focused package tests pass, and the fourteen-node graph passes 34 checks over
145 predicates. The integrated repository boundary passes 1,275 tests with
147 accepted claims, 593 valid memory records, and 75 pending queue units.
Native G5 passes all fifteen checks without a NumPy integration event; inherited
immutable G1 and G4 remain alias-only through `np.trapezoid`.

## Done Gate

P145 is closed. The exact unit-aware constitutive ledger exists as an accepted
reviewed addition; all fifteen source predicates are sensitively adjudicated;
G5 has a terminal disposition; nine reverse consumers close; generated state
agrees; and the campaign debt ledger is empty. The source's tally and familiar
constants remain evidence rather than the basis of the accepted theorem.

## Cross-References

The governing references are P008, P016, P065, P074, P141 through P145, G1
through G5, C-MED-001, C-MED-002, C-MED-005, C-DIM-002, C-IDN-001,
C-GRV-001, C-RAD-001, C-GOR-001, C-STG-001, C-RR-001, v0.112.0, and the parent
migration effort.
