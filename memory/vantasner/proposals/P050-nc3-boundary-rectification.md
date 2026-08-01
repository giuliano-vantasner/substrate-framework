---
description: Derive periodic boundary rectification and audit NC3 parity claims
author: vantasner
created: '2026-08-02T00:48:00Z'
updated: '2026-08-02T01:25:00Z'
tags:
- substrate-framework
- campaign-proposal
- sine-gordon
- migration-NC3
category: proposals
confidence: exploratory
status: archived
---
# P050 NC3 Boundary Rectification Audit

## Question and Positive Deliverable

P050 must construct an importable exact full-field boundary functional over a
declared period, derive its transformation under scalar spatial parity and time
translation, and give a phase-convention-safe closed form for sinusoidal time
and spatial derivatives. It must distinguish a coordinate derivative at a
parity center from an oriented physical boundary normal and determine exactly
what, if anything, follows about physical parity violation. A critique of NC3
without the positive functional and correlation theorem would not complete the
campaign.

## Base Release and Provenance

The accepted base is `v0.44.0`; the working baseline is framework commit
`476e8a4`, whose scientific release transaction is `5fcbda5`. `C-SG-001`
fixes the normalized real field and breather period, while `C-SG-011` and
`C-SG-012` fix scalar parity covariance and prohibit importing a physical
handed-sector conclusion. NC3 is pending source evidence at
`substrate@6d1f4e0`, SHA-256
`dceed4b3d8f59daa75bbd6b31e9a726de99f180e252accb19f7d0ae625c5c9bd`.
Its dossiers and upstream rungs are supporting evidence rather than additional
claim units. Memory search found only the P049 handoff and no accepted NC3
result. The predecessor executable remains unopened until this contract is
frozen.

## Invariants, Conventions, and Allowed Imports

For a sufficiently regular scalar field define the coordinate-boundary
functional at point `b` over a declared period `T` by
`R_b[phi]=integral_0^T sign(phi_t(t,b))*phi_x(t,b) dt`; values at isolated
zeros of `phi_t` do not change the integral. Under scalar parity
`phi_P(t,x)=phi(t,-x)`, coordinate differentiation implies
`R_b[phi_P]=-R_-b[phi]`, and only at the parity center does this reduce to an
odd same-point observable. An outward-normal derivative on a half-line is a
different object because the domain and normal orientation transform too.
Odd observable transformation, a nonzero value in one state, noninvariant
boundary data, spontaneous selection of a parity pair, and explicit
parity-breaking dynamics are not interchangeable. Pending G1, G2, NC4, W1,
and W3 content is excluded from the dependency closure.

## Candidate Preregistration

The alternatives are frozen from queue metadata and accepted invariants before
the full NC3 executable is read.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Coordinate-boundary sign correlation with exact pullback and harmonic evaluation | Periodic boundary traces, scalar parity, coordinate derivative | Boundary point, period, two amplitudes, frequency, relative phase | Native minimal exact theorem with an interpretation ceiling | Piecewise integral, parity pullback, phase and sign mutations, centered breather and parity-pair limits |
| B | Oriented-normal boundary functional on a declared half-line | Candidate A plus domain and outward-normal orientation | Domain side and normal sign | Compatible but describes additional boundary geometry, not NC3's bare coordinate formula | Transform the domain and normal explicitly and compare with the fixed-coordinate result |
| C | Nonzero odd functional is itself physical nonlinear V-A parity violation | Pending weak-sector dynamics and a selected boundary/state | Coupling, boundary law, sector dictionary | Dependency and symmetry conflict expected | Exhibit the parity-paired state and parity-invariant dynamics or boundary data |

## Selection Criteria and Blinding

Selection is ordered by exact scalar-parity compatibility, explicit boundary
and orientation data, phase and sign normalization, periodic and centered-
breather limits, dependency closure, assumption economy, and reusable API
scope. The campaign has no empirical comparator. NC3's detailed formula and
checks remain unopened until the functional, candidates, interpretation
ceiling, exact tests, and load-bearing mutations are frozen here.

## Proposed Claim Delta

Provisional `C-SG-013` will state, if verified, the coordinate-boundary
functional, its parity-center oddness and general boundary-point pullback, its
time-origin invariance for complete periods, its homogeneity and sign behavior,
and the exact sinusoidal correlation formula with an explicit relative-phase
convention. It will record that the centered rest breather has zero spatial
derivative at its symmetry center. It will explicitly withhold physical
parity-breaking dynamics, a selected boundary condition or state, topological
quantization, conserved charge, chiral anomaly, V-A interaction, weak force,
particle identity, and substrate ontology.

## Implementation and Oracle Plan

A small pure module will expose the boundary rectification density and exact
sinusoidal-period result; campaign code will derive rather than copy the
piecewise integral. SymPy is the strongest oracle for the parity pullback,
elementary half-period integrals, phase laws, amplitude scaling, and exact
breather-center limit. Mutations will flip or omit the parity derivative sign,
replace the period, interchange sine and cosine conventions without converting
the phase, remove the frequency denominator, change the factor four, flip the
temporal amplitude orientation, and substitute an oriented normal for the
coordinate derivative. An independent route will use the square-wave Fourier
series or direct positive/negative half-cycle decomposition without calling the
new exact helper. Targeted replay includes sine-Gordon and P048/P049 consumers;
the full repository gate runs once at the final promotion boundary.

## Attempts and Continuation

Attempt 0001 reproduced the hash-pinned NC3 executable at status zero with all
18 source checks, then audited its equations and interpretations. Candidate A
closed directly: the primary verifier passed 37 checks and the independent
Fourier, chain-rule, fundamental-theorem, and breather route passed eight.
The audit found the preregistered sine/cosine mismatch and preserved both exact
phase conventions. Candidate B was retained as an orientation guard, while
Candidate C was rejected by covariance, functional-independence
counterexamples, and missing dynamics rather than by numerical mismatch.

## Debt Ledger

This ledger tracks zero-set regularity, boundary point and orientation, period
closure, phase convention, amplitude sign, actual-breather specialization,
parity semantics, source mapping, and affected consumers.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| NC3's executable and phase convention have not been audited | Reproduce the hash-pinned source and review every checked conclusion | discharged: reproduction, source adjudication, and phase-convention mutation pass |
| No canonical periodic rectification API exists | Implement and independently verify the minimal exact functional | discharged: importable density, harmonic, and half-line charge APIs pass exact tests |
| Coordinate and outward-normal derivatives may be conflated | Derive both transformations and state which object NC3 defines | discharged: coordinate pullback and transformed-domain normal law are separately proved |
| Odd transformation may be conflated with physical parity violation | Exhibit the symmetry map, state/boundary alternatives, and dependency ceiling | discharged: parity pairs, missing dynamics, and interpretation ceiling are explicit |
| Direct and downstream consumers are not inventoried | Run graph impact and targeted/global replay | discharged: low graph impact, 61 targeted tests, P001/P048/P049, and the 357-test repository gate pass |

## Review and Promotion Plan

The proposed exact claim receives an individual review from raw verifier and
independent derivation artifacts. Promotion requires importable implementation,
tests, append-only attempts, source reproduction, sentence-level adjudication,
consumer replay, a structured NC3 disposition in `migration/dispositions.yaml`,
registry and pinned-release updates, generated docs and memory, status-zero
full validation, and `git diff --check`. Mixed source content will remain
qualified with every rejected remainder recorded explicitly.

## Done Gate

P050 is closed. The positive boundary functional, exact phase and parity laws,
independent derivation, sensitivity, boundary-orientation distinction,
individual claim review, qualified NC3 disposition, targeted replay,
canonical v0.45.0 state, and empty campaign debt ledger pass. The single full
promotion gate validated 62 accepted claims, 218 migration units with 170
pending, all 224 memory records, the repo-local skill, and 357 tests; `git diff
--check` also passes. The parent corpus-migration effort continues to NC4.
