---
description: Audit GB5's peak identity against exact subdivision arithmetic and the requirements for a spectrum
author: vantasner
created: '2026-08-08T15:15:00Z'
updated: '2026-08-08T15:45:00Z'
tags:
- substrate-framework
- campaign-proposal
- spectral-peak
- quotient-remainder
- migration-GB5
category: proposals
confidence: exploratory
status: archived
---
# P126 GB5 Spectral Peak Audit

## Question and Positive Deliverable

P126 must deliver a terminal predicate-level audit of GB5 and an exact
classification of its peak-equals-unit identity, derivative, monotonicity,
weight-regime independence, data gate, quotient-remainder dependencies,
consumers, and nonduplication.

The positive object is the declared identity and the complete list of premises
needed to turn an energy unit into a spectral mode. Euclidean division or a
unit derivative does not by itself establish emitted quanta, a phonon line,
material spectrum, yield, heat, or observation.

## Base Release and Provenance

The accepted base is `v0.98.0` at parent checkpoint
`b22e667a81eeffb93d2d371cf7ac65673ce1e607`; the latest scientific transaction
is P125 at `bbc6b6dc9815ee45a9e4dd9b3fd987e3db90b5ae`. Source evidence remains
pinned to `substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`.

GB5 is `/home/dan/substrate/merged-framework/bridges/phase-32/bridge_GB5_spectral_peak.py`,
8,028 bytes, SHA-256
`0f7f1a4a1ba4ab548b27de1924c84af984971eb84f50de3544045a3150dbec3e`,
and git blob `1655a6a60a3d3adbba89998948de4269e136cd26`. The queue marks it pending,
cites GB2 and PN2, and records eleven static checks, ten literal and one
dynamic. GB2 also cites GB5, exposing a candidate cycle. Unrelated Phase 47/48
worktree files and the mutable engineering compatibility overlay remain outside
scientific provenance.

Queue metadata exposed the identity, derivative, monotonicity, weight absence,
data-gate statement, and qualitative comparator names. The source body, exact
predicates, and runtime output remain unopened until the contract passes
validation. Exposed formulas and comparator names cannot select a concept.

Authority recall read v0.98.0, the qualified PN2 and GB2 dispositions, P110 and
P123's exact arithmetic ceilings, the generated GB5 entry, and the parent
effort. Memory search returned those same ceilings and the GB2-GB5 cycle; every
reused fact was verified at governance or campaign sources.

## Invariants, Conventions, and Allowed Imports

For exact nonnegative total energy and positive same-unit divisor, Euclidean
division uniquely gives the floor quotient and half-open remainder. P110 and
P123 close quotient zero, plateaus, one-sided jumps, scaling, and representation
limits. Neither campaign assigns physical constituent energies or a spectrum.

Defining `peak(omega)=omega` makes the derivative one and gives strict
monotonicity by identity. To interpret that function as a spectral peak, a
spectral measure, support, weights or occupations, resolution, and a tie rule
must first be supplied. Conservation alone admits exact partitions with
different modal energies.

The equal-quanta construction of n entries at omega plus a remainder is an
additional ansatz. If n is zero it supplies no omega entries; if n is one and a
nonzero remainder is included, equal counting weights create a tie. Intensities
and detector response can move the observed mode even when support is fixed.

At fixed total energy, changing omega changes the floor quotient by plateaus
and jumps and changes the remainder. The derivative of the identity ignores
those changes. Absence of a subdivision weight from that identity establishes
only syntactic independence. Common energy scaling preserves the quotient but
moves the asserted peak, so the absolute scale remains free.

A physical spectrum requires states, interactions, matrix elements, phase
space or density of states, occupations, linewidth, broadening, detector
response, material provenance, and a measurement map. GB2 and PN2 may be used
only as qualified arithmetic.

No numerical integration is expected. Canonical sampled work, if unexpectedly
required, uses `trapezoid_integral`; mutable current scripts use
`np.trapezoid`. An immutable `np.trapz`-only abort would receive an alias-only
recorded replay and would not count as a scientific candidate failure.

## Candidate Preregistration

The candidates are frozen before source execution or predicate inspection.

| Candidate | Construction | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal GB5 reproduction | Pinned source environment | Source symbols | Evidence only | Every predicate is classified |
| B | Declared identity | Positive energy coordinate | Omega and omega | Exact but definitional | Identity is presented as dynamics |
| C | Equal-quanta spectrum | n copies at omega and a remainder convention | n, r, weights | Peak conditional for n>1 | Arithmetic alone forces the ansatz |
| D | Alternative spectra | Same total-energy bookkeeping | Supports and multiplicities | Peak nonunique | Every admissible spectrum peaks at omega |
| E | Varying-divisor ledger | Fixed Omega and exact floor | Omega and omega | n and r change stairwise | Identity derivative captures full response |
| F | Data and scale audit | Declared units and finite scanner | Scale and comparator syntax | No validation from absence | Closed gate validates a spectrum |
| G | Physical countermodels | Arithmetic unchanged | Coupling, occupation, linewidth, detector | Physical headline rejected | Arithmetic forces an observed line |
| H | Terminal nonduplication | Existing qualified evidence and consumers | None | No new claim if no theorem survives | A distinct governed spectrum survives |

## Selection Criteria and Blinding

Selection is ordered by accepted dependency closure; exact quotient-remainder
domains; explicit spectral measure, support, weights, tie convention, and
units; correct varying-parameter behavior; assumption and parameter economy;
scale covariance; physical-premise completeness; counterexamples; mutation
sensitivity; data-gate specificity; nonduplication; and predicate and consumer
closure. Comparator proximity is excluded from selection.

Queue formulas, comparator names, and the data-gate headline are already
exposed. Source predicate details and runtime output remain blinded until the
frozen commit.

## Proposed Claim Delta

No claim identifier is reserved. P110 and P123 already govern every surviving
quotient-remainder fact, while `peak(omega)=omega` is a declared identity rather
than a derived spectral theorem. Candidate H must find a distinct positive
spectral object, package API, and governed consumer before any claim delta is
proposed. No accepted claim is challenged or superseded.

## Implementation and Oracle Plan

The primary route uses exact integer and rational arithmetic, SymPy calculus,
finite weighted measures, and explicit unit scaling. It checks quotient zero,
remainder, plateaus, the identity derivative, equal-quanta edge cases,
alternative spectra with identical bookkeeping, common-scale covariance,
weight absence, data-gate mutations, and zero-coupling, zero-occupation,
broadening, and detector countermodels.

The independent route constructs spectra as finite support-weight mappings and
derives their modes without importing the primary verifier. It compares exact
partitions of the same total energy, tracks quotient and remainder across
divisor jumps, and tests ties and detector reweighting. Source, predicate,
dependency-cycle, consumer, nonduplication, and impact audits close the
remaining surface.

No ODE, PDE, quadrature, FFT, fitted comparator, or numerical rerun is
appropriate. A canonical module is added only if a distinct accepted theorem
and consumer survive the nonduplication gate.

## Attempts and Continuation

Every provenance, freeze, source reproduction, arithmetic, spectrum,
derivative, unit, data-gate, dependency, consumer, or verifier failure is
preserved append-only with its mechanism and next materially different route.

## Debt Ledger

P126 tracks source and freeze hashes, all runtime predicates, quotient-zero and
positive-quotient domains, remainder, plateaus, varying omega, identity versus
response derivative, spectral measure, support, weights, occupation, tie and
resolution conventions, equal and unequal partitions, weight independence,
free scale, units, common scaling, data-gate syntax and semantics, physical
states, interaction, matrix element, density, linewidth, broadening, detector,
material, GB2, PN2, cycles, consumers, nonduplication, disposition, generated
state, and parent continuation. Every item must be derived, declared, rejected,
or excluded.

## Review and Promotion Plan

The primary exact-measure route, fresh finite-spectrum review, source and
predicate audit, arithmetic and mode mutations, physical countermodels,
dependency-cycle and consumer replay, nonduplication, and impact analysis must
agree. If no positive spectral theorem survives, GB5 receives a terminal
qualified disposition with no accepted-claim mapping, release, or package
change. The final gate is recorded in progress and finalized only after one
integrated workflow; later edits receive record-sensitive checks only.

## Done Gate

P126 closes only when quotient-remainder arithmetic, identity and response
derivatives, spectral-measure premises, alternative partitions, edge cases,
units, scale, data gate, every GB5 predicate, physical spectrum ceilings,
dependencies, cycles, consumers, nonduplication, terminal disposition, and an
empty debt ledger agree. A unit identity, derivative one, comparator absence,
or pass tally is not sufficient alone.

## Adjudicated Outcome

P126 terminally qualifies GB5 without changing v0.98.0. Forty-two primary and
fifteen independent checks close exact arithmetic, the declared identity,
finite spectral measures, alternative partitions, quotient-zero and tie cases,
scale, data flow, physical countermodels, dependencies, consumers, and
nonduplication. Three equal-total spectra peak at different energies; the
source sweep copies its inputs and its final no-fit guard is literal `True`.
The pinned empirical values are unused comparator provenance, not validation.
No positive spectral theorem, claim, API, release, or NumPy compatibility event
survives.

## Cross-References

See GB5, GB2/P123, PN2/P110, GB6, WN7, v0.98.0, and the parent framework-
migration effort.
