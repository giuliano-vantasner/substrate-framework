---
description: Audit WM3 one-loop running and derive an affine intersection and inverse-fit ledger
author: vantasner
created: '2026-08-03T22:30:00Z'
updated: '2026-08-03T23:30:00Z'
tags:
- substrate-framework
- campaign-proposal
- renormalization
- migration-WM3
category: proposals
confidence: exploratory
status: archived
---
# P083 WM3 One-Loop Running Audit

## Question and Positive Deliverable

P083 must determine whether WM3 independently tests a three-coupling one-loop
intersection or instead solves an exactly determined inverse construction for
a weak-angle coordinate, logarithmic scale, and common inverse coupling from
two supplied low-energy observations and imported slopes. The positive
deliverable is an exact signed-affine consistency, crossing, degeneracy,
convention, and identifiability classification plus a terminal WM3
adjudication; a near miss, nonintersection, or failed physical narrative alone
is not the deliverable.

## Base Release and Provenance

The accepted base is `v0.73.0` at scientific commit `0ec7d20`; the latest
parent-effort synchronization is `f391c54`. The predecessor is pinned at
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`. WM3 is
`/home/dan/substrate/merged-framework/bridges/phase-23/bridge_WM3_sin2thetaw_rg_running.py`,
22,183 bytes, with SHA-256
`2328ae4d6e66e1caa14a39042c362e57258406383f14ecaa5f5f6c468105e298`
and git blob `1ab71b9b34723ce2f1ea048c973e6fff33500ff7`.

The generated queue marks WM3 pending and names QCD3, SM4, WM1, and WM2 as
candidate dependencies. Direct inventory audit finds QCD3 qualified only
through C-LIE-001, C-RGE-001, and C-RGE-002; SM4 remains pending; WM1 is
qualified through the conditional C-REP-001 ledger; and WM2 is duplicate
evidence with its physical common-induction interpretation unaccepted. Source
metadata and the generated synopsis are navigation evidence; the WM3 body and
output remain unopened until the freeze gate.

The accepted sources read directly are `governance/releases/current.yaml`,
C-RGE-001, C-RGE-002, C-LIN-001, C-IDN-001, C-REP-001,
`renormalization.py`, `linear_systems.py`, and `charge_traces.py`. Memory
search located the parent effort's WM3 gate, P024's conditional SU(3)
coefficient audit, C-RGE-001's convention ceiling, and the P081/P082
normalization decisions; every reused fact was checked against the accepted
registry and generated source queue.

## Invariants, Conventions, and Allowed Imports

P083 preserves C-LIN-001's exact rank/consistency semantics and C-IDN-001's
left-null and coordinate-identifiability semantics. C-RGE-001 uses a positive
`b0` convention for one coupling, while WM3's generated synopsis advertises a
signed inverse-alpha coefficient triple; those conventions may not be mixed
without an explicit sign and normalization map. C-RGE-002 supplies only the
conditional SU(3) `b0` specialization. C-REP-001 supplies no accepted physical
weak-angle boundary, common induction mechanism, unification scale, or running
law. Pending SM4 and rejected WM1/WM2 physical semantics are evidence only.

The allowed mathematical object is a separately supplied exact affine family
`a_i(t)=a_i0+s_i*t`, with positive physical inverse-coupling inputs only where
the source separately supplies them. `t=log(mu/mu0)` is dimensionless and
reference changes must be covariant. Supplied `alpha_em` and `alpha_s` remain
observations or inverse-fit inputs. Sector thresholds and matching offsets
remain explicit unless independently derived to zero. Positive U(1) generator
rescaling must be paired with inverse coupling and beta-coordinate changes.
This exact campaign uses no numerical quadrature, `np.trapz`, or
`np.trapezoid`; any future genuinely sampled integral must use the shared
`trapezoid_integral` compatibility helper.

## Candidate Preregistration

The candidates are frozen before the WM3 source body, literal equations,
executable output, reported result, or measured weak-angle comparator is
opened.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal WM3 promotion | Accepted boundary, all slopes, sectors, observations, and exact matching | Source inputs | Fails if decisive physical imports are pending or declared | Registry closure plus source equation/AST audit |
| B | Generic affine-line ledger | Exact separately supplied intercepts and slopes | `a_i0,s_i,t` | Pairwise crossings and common intersection have exact consistency and degeneracy conditions | Symbolic elimination, rank, and reference-covariance checks |
| C | Inverse construction | Weak coordinate, log scale, and common inverse coupling are adjustable | Three fit coordinates | Three independent equations can identify all three without testing fixed-data unification | Exact rank, solve, and input-provenance classification |
| D | Fixed-data unification test | All low-energy coupling coordinates fixed independently | No fitted weak coordinate | Three pairwise crossing scales must agree | Pairwise equality and left-null residual |
| E | Threshold/matching family | Sector offsets are independently allowed | `delta_i` | Offsets reopen free directions and can realize otherwise excluded targets | Exact nullity and arbitrary-target construction |
| F | Coefficient convention covariance | Paired U(1) generator/coupling/beta conversion | Positive normalization `rho` | Physical running is invariant only under the full paired map | Exact conjugation and wrong-convention counterexample |
| G | Nonunification and degeneracies | Exact affine data | Mutated inputs or slopes | Parallel unequal, coincident, equation-removal, and slope mutations change the relevant verdict | Counterexample and mutation suite |
| H | Nonduplication decision | Distinct API and consumer required | None | No new claim if generic accepted linear/identifiability algebra already owns the result | Claim/API/consumer comparison |

## Selection Criteria and Blinding

Selection is ordered by accepted dependency closure; exact signed-affine
consistency, rank, degeneracy, units, and reference covariance; separation of
forward prediction, inverse construction, comparator use, and fixed-data
testing; normalization covariance; parameter economy; mutation sensitivity;
and nonduplication. Numerical closeness cannot select a running or matching
concept. The body, output, reported values, measured weak angle, and later
interpretations stay blinded until the prose/YAML contract hashes, immutable
freeze record, and pre-source repository validation are recorded.

## Proposed Claim Delta

Provisional C-RGE-004 may state an exact multi-line affine inverse-coupling
intersection, degeneracy, and inverse-fit ledger only if it is not merely a
specialization of C-LIN-001, C-IDN-001, C-RGE-001, C-RGE-002, and elementary
affine algebra and if a distinct reusable consumer exists. Otherwise P083 will
add no claim and will terminally classify WM3 with its inverse inputs and
physical interpretation explicit. No accepted claim is challenged or
superseded.

## Implementation and Oracle Plan

SymPy is the correct primary oracle because every planned obligation is exact
linear or rational algebra: affine evolution, pairwise crossings, common
intersection, inverse solve, rank, threshold nullity, convention transforms,
and counterexamples. The primary route will pin the contracts and source,
reproduce the source tally, map its equations into one declared sign
convention, inspect its AST and dependency imports, distinguish fixed inputs
from solved coordinates, and mutate every load-bearing intercept, slope,
normalization, and equation. The measured weak angle opens only after this
structural record is fixed. An independent route will rederive the solution
and compatibility conditions without importing any new P083 API or verifier
expressions.

Reusable code will be added only if Candidate H proves a distinct general
object. Numerical solvers and quadrature would be validation theater for this
tractable exact system. Affected canonical tests, focused governance tests,
generated queue/docs/memory checks, one integrated `scripts/validate.sh`
boundary, and `git diff --check` form the promotion replay.

## Attempts and Continuation

Failed routes will be recorded append-only with the failed layer, unchanged
scientific state, and next materially different candidate. A literal source
pass, an exact inverse solution, or a comparator residual does not end the
campaign while the positive affine/identifiability classification is
incomplete.

## Debt Ledger

The campaign tracks every sector identity, beta coefficient, sign convention,
hypercharge normalization, observation, fit coordinate, boundary, reference
scale, threshold, matching premise, perturbative-domain claim, comparator, and
consumer. The ledger closes only when each is derived, declared, rejected, or
excluded from the accepted claim.

## Review and Promotion Plan

Claim-level review will compare the primary and independent exact routes,
source reproduction and AST audit, registry closure, candidate comparison,
mutations, impact map, and nonduplication analysis. If a new claim survives,
its pure API and focused tests must precede registry promotion. A terminal WM3
disposition will name durable evidence in `migration/dispositions.yaml`; the
generated queue will be regenerated, never hand edited. Release, docs,
accepted memory, and the parent effort will be synchronized only after the one
unchanged integrated gate.

## Done Gate

P083 closes only when the positive signed-affine intersection and inverse-fit
classification exists, every WM3 predicate has a claim-level verdict, both
exact routes and mutations pass, affected consumers replay, campaign debt is
empty, and the parent migration can continue to the next pending unit. A
physical near miss or nonunification result is attempt evidence, not completion
by itself.
