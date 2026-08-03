---
description: Derive all-order cosine mixed coefficients and audit PN1's multi-phonon interpretation
author: vantasner
created: '2026-08-07T19:00:00Z'
updated: '2026-08-07T19:00:00Z'
tags:
- substrate-framework
- campaign-proposal
- sine-gordon
- mixed-taylor-coefficients
- migration-PN1
category: proposals
confidence: exploratory
status: archived
---
# P109 PN1 Cosine Mixed-Vertex Audit

## Question and Positive Deliverable

P109 must deliver a complete all-order mixed Taylor-coefficient theorem for a
declared cosine potential split into two normalized real coordinates. The
positive object includes coefficient-versus-derivative conventions, total
parity, alternating signs, factorials, the one-high specialization, arbitrary
background and coordinate-rescaling sensitivity, convergence and finite-
truncation ceilings, importable APIs, tests, and a terminal predicate-level
PN1 disposition.

The theorem is classical local calculus. A nonzero monomial, thirteen passing
checks, or an infinite formal series does not establish a high-frequency
quantum, low-frequency phonons, a transition matrix element, occupation
enhancement, mode overlap, resonance, energy-momentum conservation, a rate,
energy transfer, or a material mechanism.

## Base Release and Provenance

The accepted base is `v0.91.0` at parent checkpoint
`9626c2bbf4c3dd5d5d6e3f54ee60efb57cf4d44e`; the latest scientific transaction
is P108 at `3dc3703aa3b5f06523e7be1a9ebd8aee359b1882`. Source evidence remains pinned
to `substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`. The predecessor worktree's
unrelated Phase 47/48 changes and NumPy compatibility overlay are not
scientific authority.

PN1 is
`/home/dan/substrate/merged-framework/bridges/phase-30/bridge_PN1_multiphonon_vertex.py`,
11,476 bytes, SHA-256
`f2fcd58c97b9e9aa0b92e0ece9d92ff6c7ddaddec1b385b10a68a156ac3df985`,
and git blob `8ca57b5d61126c8d862a4308c0324996c6d177cc`. It matches the pinned commit.
The queue marks PN1 pending, names FS1, NC1, and NC2 as candidate dependencies,
and records thirteen checks, six literal and seven dynamic.

No source-body conclusion blinding remains. The generated queue exposes the
cosine series, odd-`n` one-high coefficient, sign alternation, unbounded formal
orders, and claimed multi-phonon meaning. P109 has not executed PN1 or
inspected its predicate implementations. Its full coefficient convention,
competing derivations, background and rescaling mutations, physical ceilings,
and selection gates are frozen first.

Authority recall read v0.91.0, C-SG-009/011/012, C-BRK-001, their canonical
modules and reviews, FS1/NC1/NC2 terminal dispositions, the generated PN1
entry, and the parent effort. Repository-wide search found no accepted,
rejected, or provisional `C-SG-019`; that identifier is reserved here. Existing
C-BRK-001 stops at a univariate sixth-order series and does not own the
all-order mixed-coordinate surface.

## Invariants, Conventions, and Allowed Imports

Let `H` and `L` be independent real formal coordinates, let `a_H` and `a_L`
be explicit real normalization factors, and first expand the normalized
classical potential
`V(H,L)=1-cos(a_H*H+a_L*L)` at the vacuum background zero. The coefficient
notation `[H^j L^k]V` means the polynomial coefficient, equal to the mixed
origin derivative divided by `j!*k!`; raw derivatives are not coefficients.

For total degree `m=j+k>0`, the expected coefficient is zero for odd `m` and
`(-1)^(m/2+1)*a_H^j*a_L^k/(j!*k!)` for even `m`. The zero-order coefficient is
zero. Thus the one-high coefficient `[H L^n]V` is zero for even `n` and is
`(-1)^((n-1)/2)*a_H*a_L^n/n!` for odd `n`. These statements must be derived by
both the entire binomial series and mixed derivatives, not accepted from the
exposed source synopsis.

At a general background `phi0`, odd total degrees generally reappear through
derivatives of `1-cos(phi)` at `phi0`; the vacuum rule is not background
independent. Coordinate rescaling changes every coefficient by the displayed
powers. For unit normalizations the nonzero one-high magnitudes are `1/n!` and
tend factorially to zero. Entire convergence does not make a finite truncation
exact and does not supply physical accessibility.

C-SG-012 provides only the classical normalized potential. C-BRK-001 provides
univariate local data and its physical ceiling. FS1, NC1, and NC2 supply no
mode split or quantization. Any quantum-process reading requires separately
declared canonical mode functions, normalization, operator expansion, initial
and final states, occupation factors, spacetime overlap, kinematics,
resonance/linewidth, perturbative domain, and rate rule.

Exact P109 work requires no sampled quadrature. If immutable PN1 aborts only
because `np.trapz` is absent, the campaign records an alias-only replay before
scientific adjudication. Mutable current-environment scripts use
`np.trapezoid`; canonical sampled integration would use
`trapezoid_integral`. A compatibility event is not a scientific failure.

## Candidate Preregistration

The candidate set is frozen before PN1 execution or predicate inspection.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal PN1 promotion | Every high/low, quantum, phonon, and process label is accepted | Source symbols | Fails if only a classical polynomial is checked | Source, AST, dependency, and predicate audit |
| B | Entire binomial theorem | Declared cosine and two formal coordinates | `j,k,a_H,a_L` | Full even-total coefficient formula | Exact series extraction and sign/factorial mutations |
| C | Mixed-derivative theorem | Sufficient differentiability at the origin | Same | Agrees with B after division by factorials | Direct arbitrary-order derivative pattern and finite controls |
| D | Background expansion | A separately declared real `phi0` | `phi0` | Odd-total terms appear away from vacuum | General derivative formula and `phi0=pi/2` counterexample |
| E | Normalization covariance | Independent coordinate rescalings | `a_H,a_L` | Coefficients carry explicit powers | Rescaling, swap, and raw-derivative probes |
| F | Convergence and suppression | Entire cosine series | truncation order | Unbounded nonzero formal orders but factorial decay | Ratio, limit, remainder, and finite-polynomial counterexample |
| G | Quantum-process ceiling | A physical transition needs extra declared structure | modes and states | Classical coefficient alone is insufficient | Missing-object and same-coefficient countermodels |
| H | Nonduplication | A distinct theorem/API/consumer surface exists | None | Only all-order mixed calculus survives | Registry, package, campaign, and consumer collision search |

## Selection Criteria and Blinding

Selection is ordered by accepted dependency closure; explicit potential sign,
field split, background, normalization, derivative, and coefficient
conventions; agreement of entire-series and mixed-derivative routes; correct
zero order, total parity, signs, factorials, one-high formula, background and
rescaling behavior; convergence and truncation honesty; separation of
classical coefficients from quantum dynamics; assumption economy;
nonduplication; and downstream closure.

No comparator gate remains blinded because the queue exposes PN1's formula and
narrative. The exposed coefficients cannot become expected booleans. P109
freezes stronger general formulas and mutations before opening the source
implementation.

## Proposed Claim Delta

P109 reserves `C-SG-019` for the exact all-order mixed-coordinate theorem. The
claim may state the full `[H^j L^k]` coefficient at zero background, the
one-high specialization, equivalence with factorial-normalized mixed
derivatives, explicit normalization powers, the background counterexample,
and entire-series/factorial-decay ceiling. It depends on C-SG-012 only for the
declared normalized classical potential and may cite C-BRK-001 as a
nonduplication boundary.

The claim must explicitly exclude a preferred high/low split, quantum field,
phonon, creation or annihilation operator, matrix element, transition, energy
exchange, resonance, rate, material, or nuclear mechanism. Candidate H must
reject or narrow it if existing APIs already own the exact surface or no
governed consumer exists. No existing claim is challenged or superseded.

## Implementation and Oracle Plan

SymPy and exact combinatorics are the strongest practical oracles. A minimal
pure module may expose a mixed cosine coefficient, a one-high specialization,
a background coefficient, and a finite Taylor polynomial. It must validate
nonnegative integer orders, keep normalization and background explicit, and
must not name physical phonons or transition rates. Tests will mutate total
parity, alternating sign, each factorial, coefficient-versus-derivative
normalization, field-split weights, background, order, and truncation.

The primary derivation expands the entire cosine series, applies the binomial
coefficient, and compares finite arbitrary orders with direct symbolic
derivatives. The independent route uses the complex-exponential representation
or derivative cycle without importing the primary API. It will check the
univariate reconstruction under `H+L=phi`, the C-BRK-001 local coefficients,
the `phi0=pi/2` odd-total counterexample, factorial ratios and limits, and a
nonzero-coefficient countermodel with no declared dynamics.

Post-freeze work executes the pinned PN1 source, inventories its imports and
thirteen checks, and audits every predicate. Consumer tracing includes PN2 and
later WN/MD units only as hash-pinned noncanonical evidence; none may authorize
the present claim. Focused tests, generated records, one full workflow at a
promotion boundary, GitNexus impact/detect checks, and `git diff --check` close
the campaign.

## Attempts and Continuation

Every source reproduction, representation, coefficient, factorial,
background, normalization, convergence, dependency, consumer,
nonduplication, or verifier failure is preserved append-only with command,
environment, mechanism, and next materially different route. Failure of the
quantum-process interpretation does not end the exact theorem, source
adjudication, or corpus continuation.

## Debt Ledger

P109 tracks the source hash and execution, all thirteen predicates, potential
and Lagrangian sign, field split, coordinate and mode normalization,
background, coefficient and derivative conventions, parity, signs,
factorials, convergence and truncation, perturbative domain, quantum operator
map, state normalization, occupations, overlap, energy-momentum, resonance,
rate, material and nuclear maps, FS1/NC1/NC2 ceilings, consumers,
nonduplication, disposition, claim review, release, generated state, and parent
continuation. Every item must be derived, declared, rejected, or excluded.

## Review and Promotion Plan

The primary series route, independent derivative or exponential derivation,
source and predicate audit, background and rescaling countermodels,
convergence and quantum-interpretation ceiling, dependency and consumer
audits, candidate comparison, and impact analysis must agree. Each surviving
claim receives its own four-axis review, importable implementation, and focused
tests. PN1 then receives a terminal disposition with durable evidence.

If C-SG-019 is accepted, the registry, new release, current manifest, generated
documentation, accepted memory, package exports, and downstream consumers are
synchronized. One full workflow runs at that promotion boundary. A final
attempt begins in progress, is finalized only after the gate, and triggers only
record-sensitive checks afterward.

## Done Gate

P109 closes only when the all-order mixed coefficient, independent derivation,
background and normalization sensitivity, convergence and truncation ceiling,
all thirteen PN1 predicates, physical interpretation boundary, dependencies,
consumers, claim review, canonical records, and empty debt ledger agree. A
nonzero formal coefficient, infinite series, or source tally is not sufficient
by itself.

## Adjudicated Outcome

P109 accepted C-SG-019 in release v0.92.0. Exact derivative, entire-series,
complex-exponential, and binomial routes agree on the arbitrary-order mixed
coefficient with amplitude, background, coordinate scales, and both factorials
explicit. Positive-order vacuum parity, the one-high odd subsequence,
factorial decay, and the first omitted finite-truncation term are mutation
sensitive. The package API is additive and pure.

PN1 is qualified. Its 32 runtime checks reproduce, but its high/low, quantum,
phonon, nuclear, mode, multiplicity, and energy-transfer labels never enter an
equation or oracle. No frequency-mode normalization, operator, state, overlap,
kinematic channel, resonance, or transition-rate premise is accepted. Attempts
0002 through 0004 preserve one wrong expected sign and two independent-oracle
defects; the scientific formula did not change. Exact P109 work uses no NumPy
or sampled quadrature and has no `np.trapz` compatibility event.
