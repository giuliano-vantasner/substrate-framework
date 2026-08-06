---
description: Audit MK4 conditional compacton and failed perturbative correction
author: vantasner
created: '2026-08-06T10:58:08Z'
updated: '2026-08-06T10:58:08Z'
tags:
- substrate-framework
- campaign-proposal
- migration-MK4
- compacton
category: proposals
confidence: exploratory
status: active
---
# P217 MK4 Compacton Perturbation Audit

## Question and Positive Deliverable

P217 must derive the exact conditional compacton, classify every perturbing
energy term at its edge, and decide whether MK4 supplies a controlled
correction or only an obstruction already established by P107. The positive
deliverable includes an explicit cutoff/smoothing dependence and a viable
continuation class; divergence alone is attempt evidence, not the requested
finite correction or full-model solution.

## Base Release and Provenance

The base is v0.156.0 at clean commit `794d397`, with 198 accepted claims and
eight pending units. MK4 is pinned at source `6d1f4e0`, SHA-256
`9f2e2990...7295`, and 18,532 bytes; its file is clean while unrelated source
worktree changes are excluded. The queue exposes six checks, one assertion,
the compacton profile and radius, and a claimed logarithmic L2 obstruction.
Remaining source content stays blinded through the committed freeze.

## Invariants, Conventions, and Allowed Imports

C-BPS-001 is conditional and supplies no existence, potential, coupling, or
physical map. C-BPS-003 requires controlled expansions and remainders. P107
already independently derives the same standard-potential compacton balance,
a simple L2 edge pole of coefficient two, logarithmic cutoff growth, and a
finite L4 edge factor. MK1-MK3 supply no accepted physical closure, and pending
MK5/MK6 grant no authority. Mutable sampled integration uses `np.trapezoid` or
`trapezoid_integral`; immutable version events are compatibility provenance.

## Candidate Preregistration

The candidates distinguish the compacton, termwise edge behavior, explicit
regularization, controlled asymptotics, alternative smooth formulations,
dependency firewalls, nonduplication, and governance.

| Candidate | Description | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- |
| A | Conditional exact compacton | Survives with declared radial normalization | Exact ODE substitution and radius mutation |
| B | Edge term classification | L2 diverges while L4 stays finite | Exact limits and cutoff integral |
| C | Explicit cutoff/smoothing family | Coefficient retains logarithmic regulator dependence | Delta-asymptotics and mutation |
| D | Controlled C-BPS-003 expansion | Naive expectation fails its premise | Remainder and finiteness audit |
| E | Smooth-potential or boundary-layer alternative | Requires separate equations, not retrofit | New-problem dependency ledger |
| F | Physical dependency firewall | MK1-MK3 cannot select the model | Premise-removal replay |
| G | P107 nonduplication | Likely no new accepted surface | Claim/API/evidence comparison |
| H | Terminal governance | MK4 closes without backward authority | Predicate, graph, queue, memory replay |

## Selection Criteria and Blinding

Selection prioritizes exact density/radial conventions, accepted provenance,
edge regularity, regulator independence, controlled remainders, termwise
separation, mutation sensitivity, novelty, positive continuation, and terminal
closure. Comparator agreement cannot select a cutoff or candidate. Remaining
source predicates and values stay blinded through the freeze.

## Proposed Claim Delta

No claim identifier is proposed. P107 appears to own every exposed compacton
and obstruction result. A new claim requires a distinct positive controlled
object; otherwise MK4 receives only a terminal source disposition.

## Implementation and Oracle Plan

SymPy will substitute the exact profile into the declared BPS equation, derive
edge series, limits, and cutoff dependence, and mutate radius and edge powers.
The primary route will preflight direct/imported/dynamic/eager integration-name
access before native execution. A fresh independent route will rederive the
ODE and asymptotics without MK4 or the primary verifier. P107 evidence is
hash-reused only after exact formula and source identity checks. Numerical
quadrature is regression evidence at most because the divergence is exact.

## Attempts and Continuation

Attempt 0001 freezes eight candidates, exact compacton and edge expectations,
explicit regulator tests, the P107 nonduplication boundary, physical
firewalls, compatibility policy, and positive continuation requirement before
source inspection.

Attempt 0002 reproduces all six source checks natively in 2.46 seconds. MK4
already imports SciPy's current `trapezoid` and has no legacy NumPy integration
surface. Source inspection corrects the generated queue's `F''^2` transcription:
the executable energy density and oracle use the first radial derivative
squared.

Attempt 0003 completes nineteen primary exact checks. The compacton satisfies
the declared radial equation only at the frozen radius, the L2 edge term has
simple-pole coefficient two, and the cutoff integral grows as
`2*R*log(1/delta)`. Its finite remainder still depends on the explicit
regulator, so no cutoff-independent first-order coefficient is manufactured.

Attempt 0004 completes eight fresh independent and nine source-graph checks.
The independent route does not import MK4, the primary verifier, or a
canonical compacton API; a nonlinear degree mutation also defeats the balanced
linear cancellation. The eleven-node graph pins 70 predicates and 13
assertions, reruns MK4, and hash-reuses only unchanged expensive later
executions from P215.

Attempt 0005 completes 22 focused BPS and source-audit tests. Exact survivors
duplicate P107 and accepted conditional BPS ledgers; physical coupling closure,
a controlled correction, and a full-model solution remain outside MK4.

Attempt 0006 individually reviews MK4.1 through MK4.6 and proposes terminal
qualification through existing BPS mappings and P107 duplicate evidence. It
also corrects the generated queue's derivative transcription, conditions
degree-linear energy cancellation on attainment, and confirms that no
canonical symbol, accepted claim, package API, test, or release changes.

## Debt Ledger

The ledger tracks the radial convention, profile domain, radius, edge
derivatives, L2/L4 terms, regulator, remainder, physical inputs, compatibility,
consumers, novelty, and generated records.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| Remaining MK4 predicates are blinded | Reproduce after committed freeze | discharged by attempt 0002 |
| Compacton normalization may be wrong | Independent ODE substitution and mutations | discharged by attempts 0003 and 0004 |
| Divergent and finite terms may be conflated | Exact termwise limits and cutoff asymptotics | discharged by attempts 0003 and 0004 |
| A no-go may masquerade as a correction | Record viable continuation class and reject finite coefficient | discharged by attempts 0003 and 0004 |
| P107 duplication is unresolved | Claim/API/evidence comparison | discharged by attempts 0003 through 0005 |
| Physical and later-source authority may leak | Dependency and terminal graph replay | discharged by attempt 0004 |
| Compatibility may masquerade as science | Full executable access preflight | discharged by attempts 0002 and 0004 |
| Governed records remain open | Terminal disposition and record gate | review complete; synchronization open |

## Review and Promotion Plan

Every MK4 predicate receives an individual verdict. A new claim requires a
distinct canonical object, tests, independent review, registry/release/docs,
and full replay. Otherwise the release stays unchanged and the record-sensitive
closeout reuses the current full-suite boundary.

## Done Gate

P217 closes only with an exact positive compacton/edge/regulator ledger,
mutation-sensitive independent verification, individual predicates, terminal
consumers, synchronized records, and empty debt. The perturbative failure by
itself is insufficient.

## Cross-References

See v0.156.0, C-BPS-001 through C-BPS-003, C-RDIFF-001/002, P107, P214-P216,
E2, E4, KI3, MK1-MK6, and the framework migration effort.
