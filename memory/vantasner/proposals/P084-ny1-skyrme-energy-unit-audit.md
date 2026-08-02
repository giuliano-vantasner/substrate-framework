---
description: Audit NY1 Skyrme energy-unit cancellation, imports, corrections, and duplication
author: vantasner
created: '2026-08-04T00:00:00Z'
updated: '2026-08-04T00:18:00Z'
tags:
- substrate-framework
- campaign-proposal
- skyrme
- migration-NY1
category: proposals
confidence: exploratory
status: archived
---
# P084 NY1 Skyrme Energy-Unit Audit

## Question and Positive Deliverable

P084 must determine whether NY1 adds any dependency-closed derivation beyond
C-SK-001's already accepted conditional equivalence between two supplied mass
formulas and `F_pi/e=16*pi*E_e`. The positive deliverable is an exact
coefficient, power, premise-provenance, dimensionful-import, correction, and
nonduplication classification plus a terminal NY1 adjudication; merely finding
that the physical narrative is unsupported does not complete the campaign.

## Base Release and Provenance

The accepted base is `v0.74.0` at scientific commit `6aae8f2`; the latest
parent-effort synchronization is `81a9a3d`. The predecessor is pinned at
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`. NY1 is
`/home/dan/substrate/merged-framework/bridges/phase-24/bridge_NY1_skyrme_energy_unit.py`,
5,809 bytes, with SHA-256
`b3531d7f906fe396a1326d44d68f34d09ae34988e86a8f721c360040c4aa0921`
and git blob `f4c61dfa3c96de890503023dc3a89727d32b2a24`.

The generated queue marks NY1 pending and names B1, S2, and NY2 as candidate
dependencies. Direct inventory audit finds all three pending with empty
accepted mappings; NY2 is also later in the sequential queue and cannot serve
as a derivation dependency for NY1. Source metadata and the generated synopsis
are navigation evidence; the NY1 body and output remain unopened until the
freeze gate.

The accepted sources read directly are `governance/releases/current.yaml`,
C-SK-001, C-DIM-003, `skyrme_relations.py`, its focused tests, the P008 exact
verifier, C-SK-001 review, and P008 source adjudication. Memory search located
the parent NY1 gate and those same accepted records; every reused fact was
checked against the registry, canonical module, tests, and generated queue.

## Invariants, Conventions, and Allowed Imports

P084 preserves C-SK-001's exact conditional iff and its explicit ceiling: both
mass formulas, `B1`, electron rest energy, pion scale, and Skyrme coupling are
supplied rather than derived. Cancellation of one shared nonzero factor proves
no provenance or independence. C-DIM-003 independently confirms that a
dimensionful physical import does not become predicted through a lossless
coordinate change. B1, S2, and NY2 cannot supply accepted Skyrme dynamics,
topological mass, state identity, or a nuclear reaction map.

The allowed mathematical work is exact positive-real coefficient and monomial
algebra plus energy-dimensional bookkeeping. The electron rest energy remains
an explicit empirical input. Any classical, quantum, binding, reaction, or
matching factor remains a separate dimensionless parameter until derived.
This exact campaign uses no numerical quadrature, `np.trapz`, or
`np.trapezoid`; any future sampled integral must use the shared
`trapezoid_integral` compatibility helper.

## Candidate Preregistration

The candidates are frozen before the NY1 source body, literal checks,
executable output, MeV result, energy comparators, or correction percentage is
opened.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal NY1 promotion | Both physical mass equations and sector maps are accepted | Source premises | Fails if either equation or physical interpretation is pending or declared | Registry closure plus source equation/AST audit |
| B | C-SK-001 duplication | The two positive formulas and their equality are supplied | `B1,E_e,F_pi,e` | Exact `16*pi*E_e` iff is already accepted | Symbolic/API/claim/evidence equivalence |
| C | General coefficient/power ledger | Independent exact prefactors and powers | `a,c,p,q` | Shared coefficient cancels only when powers match; prefactor ratio remains load bearing | Exact elimination and mutations |
| D | Premise independence audit | Source citations and derivation graph are explicit | None | Shared or pending provenance blocks a two-route physical derivation | Source and queue provenance graph |
| E | Dimensionful-import audit | Electron rest energy and conversion are supplied | `E_e` | Output remains linearly dependent on imported energy | Exact derivative, units, and zero-input limit |
| F | Correction/binding family | A separate dimensionless factor multiplies the unit | `kappa` | Any positive target is reachable unless `kappa` is derived | Arbitrary-target inverse and mutation |
| G | Comparator audit | Schemes, uncertainties, and roles are declared | Opened values only | Agreement cannot select a coefficient or premise | Post-freeze residual/context audit |
| H | Nonduplication decision | Distinct theorem, API, and consumer required | None | No new claim if C-SK-001 already owns all exact content | Claim/API/consumer comparison |

## Selection Criteria and Blinding

Selection is ordered by accepted dependency closure and independent premise
provenance; exact iff, coefficient/power sensitivity, dimensions, domain, and
reverse implication; separation of cancellation, empirical input, scale,
classical matching, reaction yield, and comparator use; correction-parameter
economy; and nonduplication. Numerical closeness cannot select the coefficient
or validate either mass premise. All comparator and correction values stay
blinded until the contract hashes, freeze record, and pre-source repository
validation are recorded.

## Proposed Claim Delta

No new claim is expected because C-SK-001 already states the exact NY1
cancellation theorem, provides the importable APIs, and includes coefficient
and power sensitivity evidence. A new coefficient-provenance or energy-scale
claim may proceed only if Candidate H identifies a distinct theorem and
consumer not captured by C-SK-001 or C-DIM-003. No accepted claim is challenged
or superseded.

## Implementation and Oracle Plan

SymPy is the correct oracle for the finite exact elimination, reverse
implication, power/prefactor counterfamilies, energy dimension, imported-input
dependence, and correction inverse. The primary route will pin the source and
contracts, reproduce its tally, compare every equation and literal with
C-SK-001's canonical APIs, inspect the AST and cited dependency paths, mutate
every load-bearing prefactor and power, retain `E_e`, and open comparators only
after the structural verdict freezes. An independent route will rederive the
generic monomial result without importing the canonical Skyrme APIs or P084
verifier expressions.

Reusable code will be added only if Candidate H proves nonduplication. A
numerical solver or quadrature would be validation theater for this exact
algebra. Affected canonical tests, focused governance tests, generated queue
and memory checks, one integrated `scripts/validate.sh` boundary, and
`git diff --check` form the terminal replay.

## Attempts and Continuation

Failed routes will be recorded append-only with the failed layer and next
materially different candidate. A source pass or duplicate theorem does not
end P084 while the premise/import/correction classification and terminal NY1
disposition remain incomplete.

## Debt Ledger

The campaign tracks both mass equations, their source independence, every
prefactor and power, `B1`, electron rest energy and unit conversion, `F_pi`,
`e`, correction/binding coefficients, physical sectors and state maps,
comparators, uncertainties, and consumers. The ledger closes only when each is
derived, declared, rejected, or excluded from accepted content.

## Review and Promotion Plan

Review will compare primary and independent exact routes, source reproduction
and AST audit, registry closure, candidate comparison, mutations, impact map,
and strict nonduplication. A terminal NY1 disposition will name durable
evidence in `migration/dispositions.yaml`; the generated queue will be
regenerated. If no claim survives, the release and canonical package remain
unchanged. Parent-effort synchronization occurs only after the one unchanged
integrated gate.

## Done Gate

P084 closes only when the positive premise/import/correction and duplication
classification exists, every NY1 predicate has an individual verdict, both
exact routes and mutations pass, affected consumers replay, campaign debt is
empty, and the parent migration can continue. Comparator agreement or failure
of a physical derivation is not sufficient by itself.
