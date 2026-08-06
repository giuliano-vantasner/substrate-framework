---
description: Audit GC2's declared translated wells and multisoliton interpretation
author: vantasner
created: '2026-08-05T22:56:00Z'
updated: '2026-08-05T23:16:00Z'
tags:
- substrate-framework
- campaign-proposal
- migration-GC2
- translated-localization
- multisoliton
category: proposals
confidence: established
status: archived
---
# P209 GC2 Declared-Well Multisoliton Audit

## Question and Positive Deliverable

P209 must derive the strongest exact localization and core-tail comparison for
the separately supplied translated wells, distinguish a Hamiltonian family
from a simultaneous nonlinear field solution, determine the provenance of the
count three, and terminally adjudicate GC2. Showing that a multisoliton claim
is unsupported is not completion; the positive object is an exact translated
ground-state, centered-moment, model-provenance, count-sensitivity, and
governance ledger.

## Base Release and Provenance

The accepted base is v0.151.0 at framework commit `1fdc26e`, with 191 accepted
claims and 16 pending units. GC2 is pinned at SHA-256 `07611b1e...ac4a65`,
28,532 bytes, source blob `cda47b1`, and one predecessor commit. EM6, FG2,
FG4, GC1, MH1, MH2, WM7, WM9, and WM10 are terminal. Pending GC3, GC4, and GC5
are nonauthoritative cycle edges. GC4, GC5, and GC6 are direct reverse
consumers and grant no backward authority.

The generated queue exposes eight static check sites, two assertions, and
truncated claims about fixed well literals, quartic core attenuation,
relocated modes, and the provenance of the number three. The source body,
exact predicates, constants, tolerances, finite grids, source-text probes,
count logic, and native output remain unopened through the freeze.

## Invariants, Conventions, and Allowed Imports

C-OVL-002 owns a family of separately declared translated Pöschl--Teller
Hamiltonians. Their centers, depths, widths, and spacing are supplied;
translation changes no eigenvalue and derives no common spectrum, generation,
or multisoliton. C-QBL-005 owns the conditional quartic core deficit and no
multisoliton or hierarchy interpretation. C-OVL-001 owns normalized overlaps
with no physical Yukawa or generation identity. A finite operator family,
several levels of one operator, and several coexisting nonlinear field objects
remain distinct types.

## Candidate Preregistration

Eight candidates separate the declared operator family, a genuine
multisoliton, exact centered localization, a typed core-tail comparison, count
provenance, operator versus field typing, nonduplication, and terminal
governance.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Declared translated-well family | C-OVL-002 external wells | V0, w, R_n | Isospectral supplied family | Exact translation and provenance |
| B | Dynamical multisoliton | Common nonlinear field problem | Field and boundary data | Only with simultaneous stable solution | Equation and interaction audit |
| C | Exact localization | Normalized Pöschl ground density | s, w, R | Center R and invariant centered variance | Symmetry and characteristic integral |
| D | Core-tail comparison | C-QBL-005 core plus external V0 | kappa, R, V0 | Ratio grows but models stay distinct | Exact asymptotics and mutation |
| E | Derived count three | Independent selection theorem | Integer count | Only if list-length mutation is forbidden | Count provenance audit |
| F | Typed object alternatives | Operator and field domains explicit | Family labels | Three constructions remain inequivalent | Domain mutation |
| G | No new surface | Existing accepted claims suffice | None | Corrected object already owned | Registry and API review |
| H | Terminal governance | Accepted dependencies only | None | GC2 closes individually | Graph replay |

## Selection Criteria and Blinding

Selection prioritizes source provenance, exact unitary translation,
operator-family and field-solution typing, centered-moment covariance,
external-well versus quartic-core separation, count sensitivity, novelty,
physical ceilings, comparator exclusion, and graph closure. Source values and
detailed predicates open only after the committed freeze.

## Proposed Claim Delta

P209 proposes no new claim or API initially because C-OVL-002 already owns the
exact translated ground state, isospectrality, supplied center ladder, and
physical ceilings, while C-QBL-005 owns the quartic core deficit. C-OVL-004
remains reserved and unpromoted unless source inspection exposes a genuinely
novel positive exact object rather than a composition or negative reading.

## Implementation and Oracle Plan

SymPy is the strongest oracle for translation, exact moments, asymptotic
core-tail ratios, and count mutations. For density proportional to
`sech((x-R)/w)^(2s)`, the mean must be `R`, the centered variance must be
`w^2*polygamma(1,s)/2`, and the ground eigenvalue must be independent of `R`.
The quartic core deficit at `R` is exactly
`6*kappa^2*sech(kappa*R)^2`; comparison to fixed positive `V0` is conditional
and does not derive the external well.

The source's finite-difference run, if any, is reproduction or regression
when these exact results determine its right-hand side. Any genuinely new
numeric obligation must first record its equation, domain, boundaries, mesh,
tolerances, solver-success gate, error norm, refinement, and independent
cross-check. Mutations translate all wells, alter one center, change the list
length, replace fixed depths with core-derived depths, combine the family into
one multiwell operator, and demand one simultaneous nonlinear field equation.

Compatibility preflight scans direct, imported, dynamic, and eager legacy
NumPy access. Mutable code uses `np.trapezoid` or `trapezoid_integral`;
immutable version-name events receive alias-only provenance and never count as
scientific failures.

## Attempts and Continuation

Attempt 0001 freezes authority, eight candidates, exact translation and moment
obligations, core-tail typing, count mutations, physical ceilings, graph scope,
and compatibility policy before source access. Attempt 0002 reproduces all
eight native checks after commit `b97b48c` and opens the source model. It finds
that MH2 executes six external wells, the quantity called a centroid is
`E|x|`, only that quantity is refined, and no domain study is performed. The
source also subtracts a zero mode from FG2's already-rejected exact-sine count
and calls the remainder internal states. Exact whole-line translation and the
accepted quartic spectrum replace those weak predicates. Failures remain
append-only and change the method, representation, or candidate rather than
the objective.

## Debt Ledger

The P209 ledger tracks every well parameter, center list, operator member,
field object, localization metric, core comparison, count premise, cycle edge,
reverse consumer, compatibility event, and generated record.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| Detailed source predicates remain blinded | Reproduce once after committed freeze | discharged after freeze commit `b97b48c` |
| Fixed literals may be described as derived fields | AST and source-provenance audit | discharged; four MH2 literals and six centers recorded |
| A Hamiltonian family may be called one multisoliton | Require common field equation and simultaneous solution | discharged by rejecting the absent field construction |
| Localization metric may repeat GC1's universal inequality | Reconstruct centered mean and variance exactly | discharged by characteristic-function moments |
| The external well may be conflated with the quartic core | Compare both models without identification | discharged by exact typed depth ratio and mutation |
| Three may be inherited from a list or phase-count slot | Mutate list length and audit count authority | discharged; six and three are supplied cardinalities |
| Existing claims may already own all corrected content | Complete claim and API nonduplication audit | discharged; no new claim or API |
| Pending cycle dependencies may grant authority | Replay GC3 through GC5 without imports | discharged; no backward authority |
| Reverse consumers may be silently broken | Replay GC4 through GC6 after disposition | discharged by the terminal graph |
| Compatibility may masquerade as science | Audit every executable access shape | discharged; zero quadrature surface and failures |

## Review and Promotion Plan

Every GC2 predicate receives an individual verdict. A new claim requires a
canonical API, focused tests, independent review, registry and release update,
generated documentation, synchronized memory, and one full promotion gate. If
accepted claims already own the strongest content, P209 qualifies GC2 through
those claims, materializes all evidence first, regenerates the queue, and runs
only the record-sensitive narrow gate because v0.151.0 and canonical APIs are
unchanged.

## Done Gate

P209 closes only when the exact translated spectrum and moments, fixed versus
core-derived well typing, multisoliton definition, count provenance,
source-predicate adjudication, authority graph, compatibility audit,
disposition, generated state, and durable memory agree with an empty campaign
debt ledger. Neither an unsupported multisoliton headline nor a finite numeric
localization check can close the campaign alone.

P209 qualifies GC2 through C-QBL-001, C-QBL-003, C-OVL-001, C-OVL-002,
C-MIX-002, and C-QBL-005 with no new claim, API, or release. The exact
translated moments and fixed/core depth comparison survive; the multisoliton,
selected-three, exact-sine-count, positive-particle, mislabeled-centroid, and
reachability-guard overreads do not. The primary, independent, and terminal
graph routes pass 37, 20, and 39 checks, and 86 focused tests pass. The
14-node graph pins 107 predicates and 20 assertions with zero scientific
version failures. The campaign debt ledger is empty.
