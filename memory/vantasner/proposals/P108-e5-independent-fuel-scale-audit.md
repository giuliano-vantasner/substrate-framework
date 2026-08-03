---
description: Audit E5's finite multi-reaction ratios, scale selection, and physical state map
author: vantasner
created: '2026-08-07T18:20:00Z'
updated: '2026-08-07T18:20:00Z'
tags:
- substrate-framework
- campaign-proposal
- reaction-scale
- finite-sample
- migration-E5
category: proposals
confidence: exploratory
status: active
---
# P108 E5 Independent Fuel Scale Audit

## Question and Positive Deliverable

P108 must determine exactly what follows when four supplied nuclear-reaction
release values are divided by the supplied 25.686 MeV coordinate. The positive
deliverable is an exact, mutation-sensitive ledger for reaction arithmetic,
units and provenance, dimensionless ratios, common-scale covariance,
finite-sample spread, selection effects, reaction bookkeeping, and physical
state-map closure, followed by a terminal predicate-level E5 disposition.

A table of positive ratios, a factor-three range, an `O(1)` label, or a shared
integer four does not complete this campaign. Any robust or universal scale
statement must survive predeclared scale and sample mutations and must have an
independent rule selecting its scale; any physical alpha/degree-four statement
must have an accepted state map.

## Base Release and Provenance

The accepted base is `v0.91.0` at parent checkpoint
`f328b04bc96e4dd50a594bc58673c9514645e34d`; the latest scientific transaction
is P107 at `2297324`. Source evidence remains pinned to
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`. The predecessor worktree's
unrelated Phase 47/48 changes and explicit NumPy compatibility overlay are not
scientific authority.

E5 is
`/home/dan/substrate/merged-framework/bridges/phase-29/bridge_E5_independent_fuel_test.py`,
9,956 bytes, SHA-256
`f1754902fb112f63c9c9052b60cdeca5455023560680e4e31889669cddf764af`,
and git blob `9824f55b14c21d0d678ce12f68ea38da91be86c9`. It matches the pinned commit.
The queue marks E5 pending, names E2, NY1, NY2, and O1 as candidate
dependencies, and records five checks, four literal and one dynamic.

No comparator blinding remains. The generated queue exposes the denominator,
four reaction-release values and ratios, the reported interval, factor-three
and `O(1)` language, and the claimed alpha/degree-four identification. P085
already exposed the D+D comparator and conditional scale. P108 has not
executed E5 or inspected its predicate implementations. Its data ceilings,
competing analyses, mutations, structural criteria, and nonduplication gate
are frozen first.

Authority recall read `v0.91.0`, the accepted C-DIM, C-SK, C-RDIFF, and
C-RPROF ceilings, P084 and P085's immutable audits, the generated E5 and O1
queue entries, and the parent effort. NY1 and NY2 are duplicate evidence for
C-SK-001. O1 remains pending and concerns spin-1 polar order-parameter
topology, not a nuclear state or reaction scale.

## Invariants, Conventions, and Allowed Imports

For separately supplied reaction releases `Q_i` in one declared energy unit
and a separately supplied positive scale `U` in the same unit, define only the
dimensionless coordinates `r_i=Q_i/U`. Under `U -> a*U` for `a>0`, every ratio
changes as `r_i -> r_i/a`; ratio-to-ratio quotients remain unchanged. For any
positive target coordinate `t_i`, the scale `U=Q_i/t_i` realizes it. Therefore
a finite interval of ratios cannot independently select a freely supplied
denominator.

A finite sample supports exact extrema, arithmetic or geometric means for its
declared positive entries, and spread measures such as `max/min`. It does not
support population typicality, a universal bracket, robustness to unobserved
reactions, or a physical law without a declared sampling frame and selection
rule. The phrase `O(1)` has no falsifiable content here unless a numerical
interval, asymptotic parameter, and quantifier are declared before comparison.

C-SK-001 remains only a conditional coordinate iff. C-RDIFF-001 may organize
a declared signed difference but does not derive its inputs. C-RPROF-001/002
describe conditional rational-map fields and stationary branches, not nuclei.
Map degree, baryon number, isotope mass number, a physical alpha particle, and
a product multiplicity remain distinct. P084/P085 are historical audit
evidence; O1 is pending and not an allowed authority.

Exact P108 work requires no sampled quadrature. If immutable E5 aborts only
because `np.trapz` is absent, the campaign records an alias-only compatibility
replay before scientific adjudication. Mutable current-environment scripts use
`np.trapezoid`; canonical sampled integration would use
`trapezoid_integral`. Such a compatibility event is not a scientific failure.

## Candidate Preregistration

The candidate set is frozen before E5 execution or predicate inspection.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal E5 promotion | All data, scale, reaction, sampling, and state premises are authoritative | Source literals | Fails if imports or interpretation links are missing | Source, registry, predicate, and dependency audit |
| B | Reaction ledger | Reactant and product quantities are separately supplied with units and stoichiometry | Imported entries | Exact signed arithmetic only | Independent recomputation, unit and multiplicity mutations |
| C | Scale-coordinate family | Positive `U` and declared `Q_i` | `U,Q_i` | Common inverse rescaling; no selected `U` | Exact inverse, rescaling, and arbitrary-target tests |
| D | Finite-sample description | A declared selected set of positive ratios | Sample membership | Descriptive extrema and spread only | Add/remove samples and compare predeclared statistics |
| E | Selection countermodels | The scale and sample are not independently fixed | Alternative `U` and entries | Positive and factor-three ranges are easy to manufacture or destroy | Rescale, zero/negative, and added-outlier mutations |
| F | Reaction interpretation | Physical branch, rate, products, multiplicity, and deposition are declared | Channel data | Energy arithmetic alone is insufficient | Branch and consumer dependency closure |
| G | State-map audit | A governed map connects mathematical and nuclear states | Map plus corrections | Shared integer labels alone fail | Degree/isotope/product mutation and registry search |
| H | Nonduplication | A distinct theorem, API, and accepted consumer exist | None | No new claim for elementary composition of existing ceilings | Registry, package, campaign, and consumer collision search |

## Selection Criteria and Blinding

Selection is ordered by accepted dependency closure; exact stoichiometry,
units, signs, multiplicities, inverse maps, and scale covariance; a
predeclared quantitative spread statistic; robustness to denominator and
sample mutations; separation of description from prediction, causation,
rate, or model selection; absence of label conflation; assumption economy;
nonduplication; and downstream closure.

No comparator gate remains blinded because the queue and prior audits expose
the table and narrative. The exposed values cannot determine the criteria,
scale, sample, expected verifier outputs, or tolerances. P108 freezes those
gates before opening E5's implementation.

## Proposed Claim Delta

P108 proposes no new claim. Exact ratio formation, inverse rescaling, and
arbitrary-target coordinates compose accepted dimensional ceilings with
elementary algebra; finite-set extrema and spread are descriptive arithmetic.
C-SK-001, C-DIM-002/003, C-RDIFF-001, and C-RPROF-001/002 are reused but not
challenged or superseded.

A proposal revision is required before any claim identifier, canonical API,
or release delta is introduced. Candidate H must first demonstrate a distinct
reusable theorem with accepted consumers and a verification surface beyond
the existing ceilings. Imported nuclear values, selected reactions, an `O(1)`
label, or an alpha/degree-four analogy cannot enter the accepted registry.

## Implementation and Oracle Plan

Exact rational or SymPy algebra is the strongest oracle for signed reaction
bookkeeping, ratios, common-scale covariance, inverse maps, finite extrema,
spread, and load-bearing mutations. A second implementation will recompute the
ledger without importing the primary verifier's expressions. No numeric PDE,
BVP, sampled quadrature, or fitted statistic is appropriate because E5
supplies neither such an equation nor an inference model.

The primary route will reproduce the pinned source, inventory imports and
checks, classify every predicate, and freeze a source-data provenance ledger.
It will mutate the denominator, one release, sample membership, sign, product
multiplicity, state label, and comparator availability. Alternative-scale and
arbitrary-target families must change any range-based conclusion while
leaving scale-free pairwise ratios identifiable. Zero, negative, and distant
positive additions will test whether the claimed bracket is a selected-sample
property rather than a universal result.

P085's pinned literature audit is sufficient to classify the D+D quantity as
an external comparator and a channel-specific mass difference. New web data
will be consulted only if E5 introduces a distinct datum whose provenance is
needed for the terminal classification. No canonical package code will be
added unless Candidate H survives. Targeted campaign checks, repository and
memory validation, generated queue replay, impact analysis, and one full
unchanged-boundary workflow close the terminal no-release transaction.

## Attempts and Continuation

Every reproduction, representation, data-provenance, ratio, scale, sample,
state-map, nonduplication, or verifier failure is preserved append-only with
its command, environment, mechanism, and next materially different route.
Failure of the universal-scale or physical-state interpretation does not end
the exact ledger, predicate adjudication, terminal disposition, or corpus
continuation.

## Debt Ledger

P108 tracks the source hash and execution, all five predicates, every reaction
label and datum, reactant/product sign and multiplicity, unit and uncertainty
provenance, denominator provenance, ratio and scale covariance, quantitative
spread definition, sampling frame, selection effects, alternative scales and
samples, branch/rate/deposition distinctions, physical state maps, NY1/NY2/O1
ceilings, consumers, nonduplication, disposition, generated state, and parent
continuation. Every entry must be derived, declared, rejected, or excluded.

## Review and Promotion Plan

The primary and independent exact ledgers, source and predicate audit,
alternative-scale and sample countermodels, data and reaction bookkeeping,
dependency and state-map audit, candidate comparison, and impact analysis must
agree. E5 then receives a terminal disposition with durable evidence. With no
surviving claim, the registry, release, and canonical package remain unchanged;
the generated queue and proposal/attempt memory still synchronize.

One full workflow runs at the terminal adjudication boundary. A final attempt
begins in progress, is finalized only after that gate, and triggers only
record-sensitive repository and generation checks afterward. The parent effort
is then checkpointed separately and advances to the next pending source unit.

## Done Gate

P108 closes only when the exact reaction and ratio ledger, scale covariance,
finite-sample ceiling, alternative-scale and sample sensitivity, provenance,
reaction and physical-state maps, all five source predicates, nonduplication,
canonical records, generated consumers, and empty debt ledger agree. Four
positive ratios, a factor-three span, an `O(1)` label, or a source pass tally is
not sufficient by itself.
