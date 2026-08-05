---
description: Audit WN3 and derive an exact bosonic Fock ladder and parity-complete composition ledger
author: vantasner
created: '2026-08-11T16:52:00Z'
updated: '2026-08-11T17:53:00Z'
tags:
- substrate-framework
- campaign-proposal
- migration-WN3
- bosonic-fock-ladder
- factorial-multiplicity
category: proposals
confidence: exploratory
status: active
---
# P191 WN3 Bosonic Multiplicity Audit

## Question and Positive Deliverable

P191 must determine whether WN3 adds a distinct reusable exact theorem for a
one-mode bosonic Fock ladder and its conditional composition with the accepted
parity-sensitive cosine coefficient. The positive deliverable is an importable
domain-, normalization-, parity-, and sample-space-complete ledger. Rejecting
an unsupported physical rate or a defective finite representation is evidence,
not a substitute for constructing the exact mathematical object.

## Base Release and Provenance

The accepted base is v0.141.0 at clean commit
`5666c2978f066b24e37bae8823dfff62c1c1f53c`, with 181 accepted claims and
current-manifest SHA-256
`d871dcd50df14cf7acf3d8def8a4d9e7b1f59e99ab6b6ba57ee060dd686e89cb`.
The registry SHA-256 is
`777700d977db2eb04040f29fbd9727d3a6335a50a2acfd177772ef949f76bc33`.
The predecessor baseline is
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`.

WN3 is pending at
`merged-framework/bridges/phase-37/bridge_WN3_amplitude_scale_and_multiplicity.py`,
SHA-256
`8a13c8b2af4d89297a11b3ef7460cc1f35fe274dc4affb2b9a7d3649bc237e88`,
size 14,375 bytes, blob `7a525a7a29aa71c7daeb83b559fb8cfc62d8f391`,
and sole history commit `7222eed`. Its declared dependencies GB4, PN1, PN3,
WN1, and WN2 are individually governed: PN1 maps C-SG-019, PN3 maps
C-SPN-002, WN1 maps C-SG-019 and C-CMB-001, WN2 maps C-SG-019, C-CMB-001,
C-CMB-002, and C-BRN-001, while GB4 maps C-BRN-001. Those mappings do not
blanket-promote WN3's compositions.

No fresh blinding is possible. WN3 was executed during P189 and P190's
preregistered reverse-consumer replays, its result excerpt is in the generated
migration inventory, and part of its body was displayed during WN2 review.
This exposure is preserved. Structural criteria freeze before any new WN3
execution, complete body inspection, implementation, normalization, candidate
selection, or new predicate adjudication. A repository-local memory search for
`WN3|Fock|bosonic multiplicity|creation operator` found no matching durable
entry; every reused predecessor fact above was re-sourced from canonical
governance and accepted modules.

## Invariants, Conventions, and Allowed Imports

C-SG-019 owns the exact classical cosine coefficient with background,
activity, and coordinate scales explicit. It supplies no oscillator
quantization, interaction Hamiltonian, matrix element, or rate. C-CMB-001 and
C-CMB-002 own the inverse-square factorial sequence and its normalized
positive-odd mass, not a bosonic ladder or factorial-one composition.

C-SPN-002 is a finite permutation-symmetric two-state SU(2) ladder. It must
not be renamed as a one-mode bosonic CCR representation. Exact bosonic ladder
identities may instead be defined on the algebraic finite-support domain of an
infinite orthonormal Fock basis. A finite D-level truncation necessarily obeys
`[a,a_dagger]=I-D|D-1><D-1|`; trace cyclicity forbids a full finite identity
commutator. An interior-block equality is useful regression evidence but not a
global theorem.

Multiplication by `sqrt(n!)` retains all zeros and parity restrictions of the
cosine coefficient. Positive odd orders, positive integers, and all
nonnegative occupations are different sample spaces with different
normalizers. Squared algebraic amplitudes are not transition rates without
accepted states, interaction normalization, final-state measure or spectral
density, dynamics, and units. WN4 and later units remain pending. Mutable
quadrature uses `np.trapezoid` or `trapezoid_integral`; an immutable legacy
compatibility stop cannot reject a scientific candidate.

## Candidate Preregistration

The candidate set separates literal reproduction, accepted composition, the
infinite-domain ladder, a parity-complete conditional composition, distinct
factorial-one sample spaces, exact modes, physical countermodels, and governed
closure.

| Candidate | Description | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- |
| A | Reproduce and adjudicate WN3 | Mixed exact and interpretive evidence | AST, runtime, assertion, dataflow, and conclusion audit |
| B | Accepted composition only | No new claim if every exact result is already governed | Claim, API, test, and consumer nonduplication |
| C | Exact one-mode Fock ladder | Distinct theorem only on an explicit infinite algebraic domain | Ladder induction, CCR, trace obstruction, truncation defect |
| D | Conditional cosine-to-Fock composition | Exact matrix-element identity only if parity and scales survive | Independent coefficient and ladder derivations |
| E | Factorial-one mass families | Different normalizers for all, positive, and odd supports | Exact exponential and hyperbolic series |
| F | Exact mode criteria | Activity-sensitive crossovers without WN4 | Adjacent-order ratios and boundary cases |
| G | Rate and admissibility countermodels | Squared coefficients underdetermine physical rates | Zero coupling, zero spectral density, state, and parity probes |
| H | Governed closure | Terminal only after every affected record agrees | Consumer, queue, release, docs, memory, and debt replay |

## Selection Criteria and Blinding

Selection is ordered by exact domain and operator normalization; finite trace
obstruction and top-state defect; C-SG-019 background, scale, and parity
compatibility; nonconflation with C-SPN-002; sample-space provenance;
interaction and rate typing; correct vacuum, top-state, even-order,
small-activity, and large-order limits; exact mode crossovers and adverse
mutations; assumption and API economy; and independent consumer closure.
Agreement with WN3's exposed sample peak is not a selection criterion.

## Proposed Claim Delta

P191 provisionally reserves C-OSC-001 for an exact single-mode bosonic Fock
ladder theorem and finite-truncation defect, with an optional conditional
parity-complete composition only if it remains one coherent reusable claim.
Registry, campaign, package, test, and memory searches found no `C-OSC-*`
collision or existing bosonic Fock API. The identifier remains reserved but
unpromoted if novelty, coherence, or consumer gates fail. No challenge or
supersedes edge is proposed.

## Implementation and Oracle Plan

The source audit will pin imports, compatibility, runtime predicates,
finite-matrix conventions, commutator slice, factorial-norm construction,
coefficient composition, parity handling, mode calculations, admissibility
guard, and every headline edge. Static lexical check sites, runtime check
executions, and assertion nodes remain separate inventories.

Exact operator action and induction are the primary oracle. SymPy exact
matrices, factorial identities, exponential and hyperbolic sums, rational
inequalities, and symbolic ratios fit the remaining obligations. A finite
NumPy matrix is regression coverage for the explicitly truncated object, not
independent proof of the infinite CCR. An independent review will derive the
ladder action and series from raw basis coefficients without importing the new
candidate API.

Mutations change ladder normalization, operator orientation, vacuum, top-state
defect coefficient, Fock inner product, factorial power, activity, parity,
order domain, normalizer, and a load-bearing interaction or spectral factor.
Counterexamples include every finite-dimensional trace obstruction, an even
cosine order that remains zero after bosonic multiplication, zero coupling,
zero final-state spectral density, and alternate prepared states. Compatibility
preflight covers direct, imported, dynamic, and eager-default legacy NumPy
access before scientific execution.

## Attempts and Continuation

Attempt 0001 passes repository, workflow, memory, YAML, and diff validation
and freezes the base release, source identity, unavoidable exposure, eight
candidates, ordered criteria, provisional C-OSC-001, exact oracle hierarchy,
compatibility rule, and debt before new WN3 execution or complete inspection.
Every later failure will be appended with an implementation,
representation, candidate, target, or foundation diagnosis and a materially
different continuation.

Attempt 0002 reproduces the hash-pinned source with exit zero and all forty-
eight runtime checks. Static inventory finds nineteen check call sites, no
assertions, and no NumPy compatibility surface. The exact activity scaling,
finite interior commutator, below-edge factorial norms, positive-odd
matrix-element algebra, and one-factorial cancellation survive. The headline
does not: the exact finite commutator has a top-state defect; nine instances do
not prove the infinite theorem; a repeated-creation norm is not a density of
distinct single-mode states; and an algebraic square lacks the interaction,
energy, spectral, and dimensional premises of a rate. Most decisively, the
source's composition is positive-odd-only but its guard substitutes an
all-positive-order family and calls even orders reopened. The next attempt
therefore freezes the infinite algebraic domain, exact truncation defect,
parity-complete sample spaces, and countermodel obligations.

Attempt 0003 freezes the distinct candidate before implementation. On the
algebraic finite-support span of an orthonormal occupation basis, the exact
ladder has `[a,a_dagger]=I` and
`(a_dagger)^n|0>=sqrt(n!)|n>`. Its D-level matrix truncation instead has the
exact defect `I-D|D-1><D-1|`, consistent with the finite trace obstruction.
Conditional composition with C-SG-019 retains positive-odd support and gives
the algebraic square proportional to `S^n/n!`; its normalized total is
`sinh(S)`. The distinct all-nonnegative and positive-integer families have
totals `exp(S)` and `exp(S)-1`. Exact adjacent-order ratios freeze all mode
and tie predicates. Candidates C through F are selected as one coherent claim
surface; A and G remain source and countermodel evidence, H remains the open
governance route, and accepted-composition-only candidate B cannot deliver the
new Fock object.

Attempt 0004 adds the standalone exact module, package exports, and canonical
tests, then stops with two failures after ninety-one passes. Both failures are
test representation defects: SymPy's immutable dense matrix exposes no
`is_Immutable` flag, and its independently summed positive exponential tail
is algebraically but not structurally equal to `exp(S)-1` before
simplification. The repair uses an explicit immutable-class predicate and
exact symbolic simplification. No formula, domain, mutation, or threshold is
changed; the repaired focused run and serious verifiers remain open.

The repaired focused run passes all ninety-three tests. Attempt 0005 then
passes ninety primary exact and adverse-mutation checks before stopping at the
last documentation ceiling. The required sentence is present, but a source
line break defeats a raw contiguous substring probe. Normalizing whitespace
repairs the oracle without changing any scientific formula, mutation, domain,
or threshold. A clean primary terminal tally and the independent raw route
remain required.

Attempt 0006 repeats the same compound documentation gate and identifies a
second wrapped public sentence that the first repair did not normalize. The
single-mode and algebraic-element clauses now pass; only the mathematical-mass
ceiling is split across a source newline. The complete repair normalizes all
three docstrings. This repeated stop changes no scientific or mutation
predicate and still requires a terminal primary tally rather than being
waived.

Attempt 0007 passes the repaired boundary: ninety-one primary exact and
mutation-sensitive checks, forty-four independent raw-SymPy checks, and all
ninety-three focused tests. The additive module exposes two dataclasses and
eight pure functions through ten package-root exports, changes no existing
signature, imports no NumPy, and adds no fitted parameter. The primary route
pins WN3, v0.141.0, and the formula freeze; the independent route imports no
candidate or accepted scientific API. GitNexus reports low code risk and only
the intended new caller edges, while its missing test and governance semantics
remain explicitly overridden by direct inventories. Exact claim review and
the complete WN3 consumer replay remain open.

Attempt 0008 pauses review readiness because the field-to-mode convention is
underdeclared even though the formula is correct. The repaired statement
declares `Q=low_scale*(a+a_dagger)` and verifies directly that
`<n|Q^n|0>=low_scale^n*sqrt(n!)`: in exactly `n` ladder actions, only the
all-creation word can reach level `n` from the vacuum. The API is explicitly a
low-sector element of the formal H-linear coefficient; a high-sector operator
and state element remain missing from any complete transition amplitude. The
formula-freeze revision changes no coefficient, parity, factorial,
normalizer, mode, mutation threshold, or physical verdict.

Attempt 0009 passes the repaired review-readiness boundary with 101 primary
checks, 57 independent raw checks, and 94 focused tests. Both routes now
construct the full coordinate power rather than assuming its selected term.
The exact values are unchanged, but the claim surface no longer hides a
high-sector matrix element or equate a low-sector coefficient element with a
complete transition. Individual review and the sixteen-node source replay
remain the next gates.

Attempt 0010 completes individual claim, source, dependency, candidate, impact,
and consumer review. The sixteen-node graph executes 637 native checks, and
the replay oracle passes 56 checks with no compatibility alias or version
failure. Review recommends symbolic acceptance of C-OSC-001 with dependency
C-SG-019 and qualification of WN3 through C-SG-019, C-CMB-001, and
C-OSC-001. Ten reverse consumers remain pending. The registry, disposition,
release, generated records, and integrated gate are still open.

## Debt Ledger

The P191 ledger tracks source predicates, Fock domain, truncation, parity,
sample space, normalization, interaction and rate typing, forward cycles,
compatibility, dependencies, consumers, and governed state.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| WN3 was exposed before P191 | Record exposure and claim no fresh blinding | discharged |
| Source predicates and conclusions are not P191-adjudicated | Pin and classify every executable and narrative edge | discharged |
| Finite matrices may masquerade as exact CCR | Prove the trace obstruction and explicit top-state defect | discharged |
| The bosonic Fock domain and inner product may be hidden | Declare basis, algebraic domain, operator actions, and norm | discharged |
| Bosonic multiplication may silently drop cosine parity | Preserve zero even orders through the full composition | discharged |
| All-order and odd-order masses may be conflated | Declare each sample space, total mass, and normalizer | discharged |
| Squared coefficients may be called rates | Supply full rate premises or retain mathematical-only scope | discharged |
| WN4 may be imported through a forward cycle | Exclude it until individually accepted | discharged |
| C-OSC-001 may duplicate or sprawl accepted mathematics | Complete claim and API nonduplication and cohesion review | discharged |
| Compatibility may masquerade as science | Repair mutable access or alias-replay immutable access without candidate rejection | discharged |
| Governed records may disagree | Replay and synchronize every affected path with empty debt | open |

## Review and Promotion Plan

C-OSC-001 receives an individual four-axis review only if its exact novelty,
domain, mutation, independent-rederivation, and consumer gates pass. WN3
receives predicate-level decisions for activity scaling, truncation, factorial
norms, parity, sample spaces, modes, admissibility, and physical rates. A mixed
result yields a qualified disposition with explicit accepted mappings and
rejected remainders. Evidence paths materialize before registration; the
migration queue and documentation are generated rather than hand-edited.

## Done Gate

P191 closes only when the positive bosonic ladder and conditional-composition
ledger exists, all domains and physical ceilings are explicit, candidates and
mutations are adjudicated, dependencies and consumers replay, governed state
agrees, and the debt ledger is empty. A no-rate result or finite-truncation
obstruction alone cannot complete the campaign.

## Cross-References

See C-SG-019, C-SPN-002, C-CMB-001, C-CMB-002, P110, P122, P189, P190, GB4,
PN1, PN3, WN1 through WN4, `cosine_vertices.py`,
`factorial_suppression.py`, `symmetric_spin.py`, and the framework-migration
effort.
