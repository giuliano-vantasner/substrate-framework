---
description: Derive and audit the MC1 dimensional sine-Gordon reduction
author: vantasner
created: '2026-08-04T13:00:00Z'
updated: '2026-08-04T13:00:00Z'
tags:
- substrate-framework
- campaign-proposal
- dimensional-sine-gordon
- migration-MC1
category: proposals
confidence: exploratory
status: archived
---
# P095 MC1 Dimensional Sine-Gordon Reduction

## Question and Positive Deliverable

P095 must derive the exact conditional field equation, dimensions, coordinate
normalization, parameter-identifiability class, and physical-coordinate
breather consequences of a declared positive-coefficient cosine-medium
Lagrangian. The positive deliverable is an importable, claim-level separation
of ratio-fixed dynamics from the free overall energy/action scale, exact
frequency and width conversions, transformed energy and canonical action,
material and consumer ceilings, and a terminal MC1 disposition.

## Base Release and Provenance

The accepted base is `v0.80.0` at parent commit `433c25c`; the latest
scientific transaction is P094 at `1553412`. The predecessor evidence is pinned
at `substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`. MC1 is
`/home/dan/substrate/merged-framework/bridges/phase-27/bridge_MC1_constitutive_reduction.py`,
18,553 bytes, SHA-256
`32ed770bb753a9d1f0e67620a66fa29355e84c430c150694ffdfdb3003a8d3f3`,
and git blob `f5bb79a30d764627225dee11c23f558a968a2f9f`.

The generated queue marks MC1 pending, records twenty-four literal check calls
and no assert statement, and exposes its principal dimensional Lagrangian,
Euler-Lagrange equation, speed, gap, length, coordinate normalization, and
physical-coordinate breather claim. Fresh formula blinding is therefore
impossible and is not claimed. P095 has not opened or executed MC1 and has not
opened additional MC2/MC3 or engineering consumer bodies or outputs.

Direct accepted sources are release `v0.80.0`, C-SG-001 through C-SG-003,
C-VAR-001, C-DIM-002, the complete canonical sine-Gordon, variational, and
dimensional-analysis modules, and the relevant P001 and P016 accepted campaign
evidence. Memory search found normalized sine-Gordon and dimension-basis
pointers but no accepted dimensional cosine-medium reduction. Every reused
fact is re-sourced at the registry, module, or immutable campaign.

## Invariants, Conventions, and Allowed Imports

The normalized root remains the real dimensionless `1+1` equation
`phi_tau_tau-phi_XX+sin(phi)=0`, with `0<omega<1`,
`eta=sqrt(1-omega^2)`, normalized energy `16*eta`, and canonical action
`16*acos(omega)`. A physical lift must not silently reuse normalized
coordinates, frequencies, integration measures, or energy/action units.

P095 may declare the density
`L=lambda*u_t^2/2-Tcoef*u_x^2/2-mu*(1-cos(u))` with dimensionless real `u`,
physical `x` and `t`, and positive exact `lambda`, `Tcoef`, and `mu`. Its field
Euler-Lagrange equation, Noether energy, and chain-rule normalization must be
derived directly. With density dimension energy per length, the coefficient
dimensions are `[lambda]=E*time^2/length`, `[Tcoef]=E*length`, and
`[mu]=E/length`; equivalent base-dimension ledgers must state the density
convention explicitly.

The candidate ratios are `c^2=Tcoef/lambda`,
`omega_0^2=mu/lambda`, and `ell^2=Tcoef/mu`, so `ell=c/omega_0` only for
positive coefficients and a fixed positive-root convention. These ratios have
only two independent degrees because `ell^2*omega_0^2=c^2`. Multiplying all
three coefficients by one positive factor preserves the equation and ratios
while scaling the integrated Lagrangian, energy, and canonical action. This
free direction must remain visible rather than being renamed a material
prediction.

Pending MC2 may later analyze linear dispersion and tail rejection, and MC3
may later propose per-medium parameters. Neither is an allowed premise here.
A periodic, bistable, Josephson, mechanical, or substrate label does not derive
the exact cosine potential, coefficient values, dimensionality, continuum
validity, or a material realization.

## Candidate Preregistration

The candidate set is frozen before MC1 body inspection, execution, literal
check inspection, terminal output, or additional consumer inspection.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal MC1 reproduction | Pinned source and environment | All source values | Tally classifies only implemented predicates | Hash, AST, process status, output, predicate ledger |
| B | Direct field variation | Declared cosine density and endpoint-fixed variations | lambda, Tcoef, mu | Exact dimensional equation with all signs and factors | Variation by integration by parts, residual, sign mutations |
| C | Ratio map and inverse family | Positive coefficients and positive roots | c, omega_0, ell, one scale | Ratios obey one identity and leave a common multiplier free | Exact forward/inverse map, rank/nullspace, multiplier mutation |
| D | Breather pullback | C-SG-001 plus the exact coordinate map | omega and the three coefficient ratios | omega_b=omega*omega_0 and inverse width eta/ell | Direct dimensional PDE residual, normalized limit, factor mutations |
| E | Energy/action transform | C-SG-002/C-SG-003 and transformed measures | common coefficient scale | E_phys=sqrt(Tcoef*mu)*E_norm and J_phys=sqrt(lambda*Tcoef)*J_norm | Hamiltonian Jacobian, phase-space integral, independent slices |
| F | Dimension audit | Dimensionless field and energy-per-length density | base-dimension convention | Every ratio and scale has the claimed dimension | Dimension matrix, simultaneous rescaling, wrong-unit probes |
| G | Potential-family comparison | Alternative differentiable on-site potentials | potential function | Exact sine-Gordon requires the cosine derivative, not periodicity alone | Generic residual and explicit noncosine counterexample |
| H | Gap-scope separation | Only MC1's exact nonlinear equation | none | Linear band/tail claims remain for MC2 | Claim-delta and source-predicate audit |
| I | Consumer audit | Hash-pinned downstream use | none | Consumers inherit any free scale and material premise | Static hashes, actual imports, parameter flow |
| J | Nonduplication and canonical fit | Accepted registry and package | none | Only genuinely new dimensional APIs merit claims | Registry, campaigns, memory, package, tests |

## Selection Criteria and Blinding

Candidates are ranked first by accepted dependency closure and direct field
variation; then by dimension, sign, coordinate, frequency, energy, and action
consistency; multiplier and inverse-map honesty; structural nonduplication;
correct limits; mutation sensitivity; parameter economy; and governed consumer
closure. A passing source tally, material name, or later numerical value cannot
select or normalize a candidate.

The generated queue already exposed the principal formulas, so P095 records
partial prior exposure. Source implementation details, literal predicates,
terminal output, any literal parameter examples, additional citations, and
consumer bodies and outputs remain closed until this contract and its matching
manifest validate and freeze.

## Proposed Claim Delta

P095 provisionally reserves two collision-free identifiers. `C-MED-003` would
cover the declared dimensional cosine density, exact field equation, positive
ratio map, inverse coefficient family, common-multiplier free direction, and
unit ledger. `C-SG-017` would cover the exact pullback of C-SG-001 with physical
frequency, period, width, energy, and canonical action scalings. Repository-
wide searches of governance, campaigns, proposals, memory, source, and tests
found neither identifier; both remain reserved even if later rejected.

The provisional dependencies are C-VAR-001 and C-DIM-002 for C-MED-003, and
C-SG-001 through C-SG-003 plus C-MED-003 for C-SG-017. No existing claim is
challenged or superseded. Linear dispersion, tail classification, per-medium
values, material identity, lifetime, thermal noise, coherence survival,
population, and discharge claims are excluded from the delta.

## Implementation and Oracle Plan

The smallest canonical surface is a pure
`substrate_framework.dimensional_sine_gordon` module for coefficient ratios,
the dimensional field residual, coordinate maps, inverse coefficient family,
breather pullback, and energy/action scaling. It will reuse normalized
sine-Gordon APIs rather than duplicate their constants or field definitions.
Imports execute no calculation or printing.

SymPy and direct exact algebra are the strongest practical oracles. The primary
route must derive the field equation from independent partial derivatives of
the density, substitute the rescaling and pulled-back breather into the
dimensional residual, transform the Hamiltonian and canonical phase-space
integrals including both Jacobians, compute the coefficient-map rank and
nullspace, and evaluate dimensions and all limits. An independent route will
vary the action by integration by parts, derive coefficient ratios from plane-
wave units or chain rules, and reconstruct energy/action scales without calling
the new helpers.

Mutations change the kinetic or gradient sign, omit a factor or Jacobian,
invert one coordinate scale, use `omega/omega_0` instead of
`omega*omega_0`, use `ell/eta` as inverse width, replace the cosine derivative,
drop the common multiplier, or conflate energy and action scale. Each must fail
a relevant check. Exact work needs no numerical quadrature or NumPy integration
alias; numerical reproduction of exact source expressions is regression only.

Consumer replay includes focused new tests, accepted sine-Gordon and
variational/dimension tests, P001's exact verifier, P016's exact dimension
verifier, generated governance consumers, and every actual downstream module
named by the final claim delta. MC2/MC3 may be audited as pending consumers but
cannot broaden P095.

## Attempts and Continuation

Source, representation, variation, coordinate, branch, dimension, energy,
action, implementation, and consumer failures remain append-only. If the
source formulas duplicate accepted normalized algebra, P095 continues through
the inverse-map and scaling classification. If either provisional claim is too
broad, it is narrowed claim by claim without turning a qualification into the
campaign's positive result.

## Debt Ledger

P095 tracks source hash and blob, all twenty-four predicates, field and
coordinate dimensions, density versus integrated-action convention, coefficient
positivity, endpoint assumptions, field variation, EOM sign, speed, gap,
length, root branches, ratio identity, inverse coefficient family, common
multiplier, coordinate Jacobians, normalized and physical frequencies, period,
width, field amplitude, Hamiltonian density, energy scale, canonical momentum,
action scale, limiting cases, alternative potentials, material claims,
downstream consumers, claim collisions, canonical APIs, generated consumers,
and validation. Every item must be derived, declared, rejected, or excluded
before closure.

## Review and Promotion Plan

Claim-level review compares literal source reproduction, direct variation,
primary and independent exact routes, load-bearing mutations, dimension and
parameter-rank audits, alternative-potential countermodels, consumer and impact
maps, and nonduplication. Surviving claims receive pure APIs, focused tests,
separate four-axis reviews, registry and release transactions, generated docs,
accepted memory, and a qualified or migrated MC1 disposition with durable
evidence. The integrated workflow runs once at the actual promotion or terminal
disposition boundary; record-only additions do not repeat it.

## Done Gate

P095 closes only when the positive dimensional field, coefficient-map,
breather, energy, action, unit, material, consumer, and nonduplication
classification exists; every source predicate is individually adjudicated;
the primary and independent mutation-sensitive routes pass; affected consumers
replay; campaign debt is empty; and the parent migration can continue. A
correct rescaling alone, a 24-check tally, or a named material is not
completion.
