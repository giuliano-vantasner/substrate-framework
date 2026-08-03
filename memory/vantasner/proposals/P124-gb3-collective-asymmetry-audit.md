---
description: Audit GB3's collective-emission asymmetry and wavelength gate against accepted spin and coherence theorems
author: vantasner
created: '2026-08-08T13:15:00Z'
updated: '2026-08-08T13:15:00Z'
tags:
- substrate-framework
- campaign-proposal
- symmetric-spin
- collective-emission
- migration-GB3
category: proposals
confidence: exploratory
status: active
---
# P124 GB3 Collective Asymmetry Audit

## Question and Positive Deliverable

P124 must deliver a terminal predicate-level audit of GB3 and an exact
classification of its normalized ground-edge coefficient, deterministic and
ensemble phase factors, wavelength gate, collective exponents, physical rate
premises, input provenance, dependencies, consumers, and nonduplication.

The positive object is the exact phase-aware conditional algebra and its
physical boundary. A squared ladder coefficient or wavelength comparison does
not by itself establish a soft/gamma rate asymmetry, phonon coherence, nuclear
transition, material enhancement, yield, heat, or observation.

## Base Release and Provenance

The accepted base is `v0.98.0` at parent checkpoint
`c27879644e064f48a32c4614620ef1be71f8d66a`; the latest scientific transaction
is P123 at `1ec8b1db1da2846239fc8257a145dc8ed40d8d48`. Source evidence remains
pinned to `substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`.

GB3 is `/home/dan/substrate/merged-framework/bridges/phase-32/bridge_GB3_dicke_asymmetry.py`,
9,617 bytes, SHA-256
`a168a03545312409cd41cb9b5217f54759c8564eba0e7d8ad2252faf8bcee70d`,
and git blob `ef3ea3f6e1b600842ebaa384b4f40418d652756d`. The queue marks it pending,
cites PN3, and records thirteen literal static checks with no dynamic sites.
Unrelated Phase 47/48 worktree files and the mutable engineering compatibility
overlay remain outside scientific provenance.

Queue metadata exposed the ground-edge coefficient, squared N label, 3 MeV
gamma and one-Angstrom spacing, 0.413-pm comparison, soft/gamma exponent
assignment, and rejection headline. The source body, exact predicates, and
runtime output remain unopened until the contract passes validation. Exposed
claims and values cannot select a concept or tolerance.

Authority recall read v0.98.0, C-SPN-002, its canonical symmetric-spin module
and tests, C-COH-001, PN3/P111's adjudication, the generated GB3 entry, and the
parent effort. Memory search returned those same ceilings; every reused fact
was verified in governance, campaign, or package sources.

## Invariants, Conventions, and Allowed Imports

C-SPN-002 exactly gives the normalized all-rung coefficient and arbitrary
complex site-coupling projection. At the ground edge with common coupling the
coefficient is `s*sqrt(N)` and its algebraic norm square is `s^2*N`; it remains
a vector-space quantity rather than a transition rate.

For deterministic phases, the symmetric bright norm is proportional to
`|sum_j exp(i*phi_j)|^2/N`. Equal phases maximize it, but unequal phases can
partly or fully cancel it. Wavelength alone does not fix the phases: site
positions, wavevector direction, full array extent, and phase differences
modulo `2*pi` are required.

A full-cloud diameter much smaller than wavelength is a sufficient small-sample
condition only after an approximation tolerance is declared. Comparing
wavelength with nearest-neighbor spacing is neither necessary nor sufficient:
two sites separated by half a wavelength cancel along their axis despite
`lambda>=d`, while integer-wavelength or transverse separations can align even
when a nearest spacing slogan fails.

C-COH-001 separately governs iid phasor directional intensity at fixed
per-source normalization. Its incoherent and aligned endpoints scale as N and
N-squared; changing to fixed-total normalization changes the comparison. It
does not define a rate, physical emitters, or their dynamics.

A physical rate requires declared states, state preparation, interaction,
coupling normalization, mode functions, energy conservation, final-state
measure or spectral density, linewidth, decoherence, and approximation regime.
Gamma wavelength, spacing, phonon coherence length, material, and uncertainty
are inputs rather than algebraic outputs. PN3 may be used only through
C-SPN-002 and its explicit physical ceiling.

The source has no numerical-integration hint. Canonical sampled work, if
unexpectedly required, uses `trapezoid_integral`; mutable current scripts use
`np.trapezoid`. An immutable `np.trapz`-only abort would receive an alias-only
replay and would not count as a scientific candidate failure.

## Candidate Preregistration

The candidates are frozen before source execution or predicate inspection.

| Candidate | Construction | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal GB3 reproduction | Pinned source environment | Source inputs | Evidence only | Every predicate is classified |
| B | C-SPN-002 mapping | Normalized symmetric state and common operator scale | N and s | Exact existing theorem | Any coefficient or normalization mismatch |
| C | Deterministic finite-array factor | Declared sites and wavevector | Positions and phases | Exact phase-dependent projection | Spacing alone fixes the factor |
| D | C-COH-001 ensemble comparison | Iid phases and fixed normalization | N and visibility | Directional expectation only | Deterministic and ensemble quantities are conflated |
| E | Phase-diameter and matching audit | Declared geometry and tolerance | Array extent and wavelength | Spacing slogan rejected | It is necessary and sufficient |
| F | Input-provenance audit | Declared units and sources | Gamma energy, spacing, coherence length | Conditional numerics only | Values are derived from accepted claims |
| G | Physical rate countermodels | Accepted algebra unchanged | Coupling, density, detuning, linewidth | Rate headline rejected | Algebra forces a nonzero asymmetry |
| H | Terminal nonduplication | Existing claims and consumers | None | No new claim if fully subsumed | A distinct governed consumer survives |

## Selection Criteria and Blinding

Selection is ordered by accepted dependency closure; normalized state,
operator, and observable conventions; exact phase structure, array extent,
direction, wavelength, and limits; complete rate premises; input provenance;
mutation sensitivity; parameter economy; nonduplication; and predicate and
consumer closure. Numerical proximity to 0.413 pm or a declared spacing cannot
select a candidate.

Queue formulas and advertised values are already exposed. Source predicate
details and runtime output remain blinded until the frozen commit.

## Proposed Claim Delta

No claim identifier is reserved. C-SPN-002 already includes arbitrary complex
site couplings, and C-COH-001 governs the complementary iid directional
intensity theorem. Candidate H must find a distinct exact theorem, package API,
and governed consumer before any claim delta is proposed. No accepted claim is
challenged or superseded.

## Implementation and Oracle Plan

The primary route reuses canonical C-SPN-002 APIs, exact complex sums, SymPy
trigonometry, and finite arrays. It checks the normalized ground edge, arbitrary
phase projections, two-site cancellation and alignment, regular-array
structure factors, phase-diameter bounds, direction dependence, normalization
changes, wavelength units, and load-bearing physical-rate mutations.

The independent route constructs explicit one-excitation vectors and geometric
sums without importing the primary verifier. Countermodels include
half-wavelength cancellation despite the source gate, integer-wavelength and
transverse alignment outside it, random-phase ensemble versus deterministic
arrays, zero coupling, zero spectral density, off resonance, and complete
dephasing. Source, predicate, input, dependency, consumer, nonduplication, and
impact audits close the remaining surface.

No ODE, PDE, quadrature, FFT, or fitted comparator is appropriate. A canonical
module is added only if a distinct accepted theorem and consumer survive the
nonduplication gate.

## Attempts and Continuation

Every provenance, source reproduction, phase, normalization, input, dependency,
consumer, or verifier failure is preserved append-only with its mechanism and
next materially different route. Attempt 0001 already preserves a manually
expanded commit-hash error caught before source access.

## Debt Ledger

P124 tracks source and freeze hashes, all thirteen predicates, normalized
states, operator scale, ground versus middle rungs, algebraic norm versus rate,
site phases, array extent, direction, wavelength, spacing, gamma energy,
phonon coherence length, material and uncertainty, small-sample tolerance,
phase matching, deterministic versus ensemble normalization, interaction,
final states, spectral density, linewidth, decoherence, PN3, dependencies,
consumers, nonduplication, disposition, generated state, and parent
continuation. Every item must be derived, declared, rejected, or excluded.

## Review and Promotion Plan

The primary canonical-algebra route, fresh explicit-vector review, source and
predicate audit, phase and normalization mutations, input provenance, physical
countermodels, dependency and consumer replay, nonduplication, and impact
analysis must agree. If accepted claims already subsume the exact surface, GB3
receives a terminal qualified disposition with no release or package change.
The final gate is recorded in progress and finalized only after one integrated
workflow; later edits receive record-sensitive checks only.

## Done Gate

P124 closes only when normalized algebra, deterministic and ensemble phase
structure, wavelength and geometry conditions, input provenance, every GB3
predicate, physical rate ceilings, dependencies, consumers, nonduplication,
terminal disposition, and an empty debt ledger agree. A square-root
coefficient, wavelength comparison, channel label, or pass tally is not
sufficient alone.

## Cross-References

See GB3, PN3/P111, C-SPN-002, C-COH-001, P124, the migration queue, and the
parent framework-migration effort.
