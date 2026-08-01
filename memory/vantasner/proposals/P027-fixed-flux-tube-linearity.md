---
description: Audit CF2's fixed-flux tube linearity and tension coefficients
author: vantasner
created: '2026-08-01T15:47:05Z'
updated: '2026-08-01T15:50:39Z'
tags:
- substrate-framework
- campaign-proposal
- fixed-flux-tube
- migration-CF2
category: proposals
confidence: exploratory
status: archived
---
# P027 Fixed-Flux Tube Linearity

## Question and Positive Deliverable
P027 must derive the exact consequences of a uniform conserved flux confined
to a fixed cross-sectional area and distinguish field energy from endpoint
test-charge work. The positive deliverable is an importable coefficient-honest
linearity theorem. Calling either conditional line a quark potential or
confinement mechanism requires a separately accepted physical map.

## Base Release and Provenance
The accepted base is `v0.23.0` at commit `a02e56a`. `C-VTX-001` supplies exact
conditional vortex flux and `C-VTX-002` supplies bounded numerical energy per
length for one radial model; neither states that the tube has an ideal fixed
area or represents QCD confinement. The hash-pinned candidate is CF2 at
`merged-framework/bridges/phase-10/bridge_CF2_linear_potential.py`, SHA-256
`e9651b9d4db9f23bb54d013a419c2f050725063347e63f253a968781598bfe6a`.
Memory search found no accepted fixed-tube theorem.

## Invariants, Conventions, and Allowed Imports
Flux `Phi`, cross-sectional area `A`, endpoint charge `q`, and separation `L`
are positive. The field is uniform and longitudinal and `A` is independent of
`L`. Declared units use field-energy density `E^2/2` and endpoint force `q*E`.
These are independent constructions until work/energy conventions or a
charge-flux relation equate them. No physical quark, SU(3), or confinement
identity is imported.

## Candidate Preregistration
The candidates are frozen from migration metadata before reading CF2's full
body.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Promote separate energy and force slopes plus their exact equality condition | Uniform flux, fixed area, declared energy and force laws | `Phi,A,q,L` | Preferred if it exposes rather than hides coefficient mismatch | Derive `Phi^2/(2A)` and `qPhi/A`; solve equality and mutate the one-half |
| B | Promote only constant-field generic linearity | Same geometry, no coefficient identification | `Phi,A,L` | Preferred if endpoint work cannot be reconciled | Audit every use of “sigma” and consumer semantics |
| C | Promote physical linear quark confinement | Accepted chromoelectric/QCD tube map | Physical charges and area | Conflicts with current conditional boundaries | Dependency inventory and non-fixed-area counterexamples |

## Selection Criteria and Blinding
Selection is ordered by energy/force work consistency, premise visibility,
factor sensitivity, dimensional closure, behavior under variable area,
dependency economy, and reusable consumer reach. No empirical string tension
or quark comparator may select a candidate.

## Proposed Claim Delta
Provisional `C-FLX-001` states that `E=Phi/A`; field energy in a length `L` is
`U=Phi^2*L/(2A)` with slope `sigma_energy=Phi^2/(2A)`, while endpoint potential
from `F=qE` is `V=q*Phi*L/A` with slope `sigma_force=q*Phi/A`. The slopes are
equal exactly when `q=Phi/2`. Fixed area, uniformity, and both constitutive laws
remain premises; no physical confinement follows.

## Implementation and Oracle Plan
A pure `flux_tube.py` module will expose field, field-energy slope, endpoint
force slope, and linear energy/potential helpers without identifying the two.
SymPy exact algebra is the strongest oracle. Mutations change the energy
one-half, charge, flux, and area law. A variable area `A(L)` and spherical area
`4*pi*L^2` provide counterexamples to constant field and linearity. An
independent review will derive energy by volume integration and endpoint work
separately rather than calling package helpers.

## Attempts and Continuation
Attempt `0001` will reproduce CF2 and map all fifteen checks to the two slope
definitions. Representation or implementation failures are preserved
append-only. If coefficient equality is silently assumed, Candidate A retains
the valid positive theorem with an explicit iff; if even generic linearity
fails under the declared premises, the source is reformulated and rechecked.

## Debt Ledger
This ledger tracks geometry, coefficient, and interpretation debt.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| One symbol sigma may hide two different slopes | Derive both and solve their equality condition | discharged |
| Fixed area may be inferred rather than declared | Keep it as a load-bearing API input and add variable-area counterexamples | discharged |
| Field-energy one-half may be verifier-insensitive | Mutate it and require the energy slope to change | discharged |
| Conditional linearity may be renamed confinement | Exclude physical mapping or establish it separately | discharged |

## Review and Promotion Plan
One claim-level review will audit exact algebra, mutations, counterexamples,
consumers, and source subclaims. Promotion requires package APIs/tests,
immutable attempts, terminal CF2 disposition, registry/release/generated
synchronization, parent-effort update, targeted replay, and one full unchanged
gate. Mixed valid algebra and rejected physical interpretation gives CF2 a
qualified disposition.

## Results and Promotion
CF2 reproduces all fifteen source checks. The main audit passes 22 exact checks,
the independent route passes six, and 19 focused tests pass. `C-FLX-001`
promotes both exact slopes and their equality iff. CF2 is qualified because its
executable energy path never uses `q`, its CF1 identification is not derived,
and all physical confinement readings remain outside accepted closure.

## Done Gate
P027 is complete. Both slopes and their equality condition are exact, premises
are visible, physical overreach is excluded, consumers are recorded, CF2 is
terminally qualified, and the debt ledger is empty.
