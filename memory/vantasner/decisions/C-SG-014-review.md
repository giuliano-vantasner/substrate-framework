---
description: Review of proposed NC4 amplitude-robust discrimination claim C-SG-014
author: vantasner-review
created: '2026-08-02T02:18:00Z'
updated: '2026-08-02T02:30:00Z'
tags:
- substrate-framework
- claim-review
- sine-gordon
- migration-NC4
category: decisions
confidence: working
status: archived
---
# Review of Proposed C-SG-014

## Claim Under Review

The proposal asked whether NC4 establishes amplitude-robust topological-charge
discrimination and a physical boundary-correlation sign flip on the full
nonlinear sine-Gordon PDE, and whether a distinct accepted simulation claim is
warranted.

## Sourced Inputs

The review read `v0.45.0`, `C-SG-001`, `C-SG-005`, `C-SG-011`, `C-SG-012`,
and `C-SG-013`; P051's frozen contract and append-only attempts; hash-pinned
NC4, its dossier, imported `study.py`, and the predecessor half-line charge
discussion; the canonical solver and focused tests; the 36-check primary
verifier; the nine-check independent Fourier/direct-solve_ivp review; and the
numerical audit record. G1, G2, G3, W1, W3, weak dynamics, particle labels, and
the calibrated chirality dictionary remain unaccepted imports.

## Independence

The primary route uses package leapfrog and DOP853 surfaces, exact symbolic
mutations, and corrected finite-interval diagnostics. The independent route
rewrites the moving breather, Fourier spatial operator, Neumann ghost point,
Sommerfeld boundary, drive, solve_ivp system, endpoint coordinate, and sampled
correlation without calling any new evolution or diagnostic API. It reproduces
the selected response and the common-phase counterexample.

## Verification Status

The exact equation and parity/topological semantics remain symbolically
verified existing claims. The selected, calibrated `w=0.6` IBVP earns only
finite-grid finite-time simulation evidence. The proposed four-frequency
amplitude-robust headline is refuted by a common-phase counterexample and
therefore remains unverified as stated; no new registry claim is promoted.

## Sensitivity and Counterexamples

Changing the spatial-operator sign or sine coefficient breaks the exact
breather residual. Mesh, timestep, domain, adaptive tolerance, energy flux,
and independent-method checks bound the selected numerical response. Holding
phase 5.50 fixed changes `dQ` from about `-1.033` at `w=0.6` to about `+1.947`
at `w=0.8`. Adding pi to the phase exactly swaps the two epsilon-labelled
drives. The source's scale-zero guard supplies identical inputs and a zero
correlation factor, so it cannot detect those load-bearing mutations.

## Framework Compatibility

The reusable numerical surface is a compatible extension of the normalized
1+1 PDE and uses accepted energy, boundary, parity, and topological
conventions. The proposed physical headline conflicts with framework
semantics: a finite-interval endpoint coordinate is not integer topological
charge without vacuum endpoints, boundary correlation does not imply winding,
and a forcing-sign label is not spatial parity or chirality absent the complete
transformation and a derived boundary law.

## Dependency and Consumer Replay

The source's supportable exact content maps to `C-SG-001`, `C-SG-005`,
`C-SG-011`, and `C-SG-013`. The package export change has low graph impact and
no affected indexed process. Targeted consumers are the new 1D solver tests,
shared numerics and existing sine-Gordon/boundary tests, and the P001,
P048, P049, and P050 verifiers. The NC4 disposition and later W1/W3 audits are
the only new narrative consumers.

## Competing Candidate Audit

Literal source audit, exact nonlinear reference, and a separately explicit
boundary model were registered before NC4 values were opened. Candidate A is
retained only as a corrected, setup-specific numerical audit. Candidate B
validates the solver with no new physics import. Candidate C is not opened:
the Neumann IBVP is mathematically explicit, while inventing a new boundary
action would broaden rather than repair NC4's source claim.

## Four-Axis Decision

The decision applies to proposed C-SG-014, not to the already accepted claims
used by the solver.

- Verification: unverified for the headline; simulation evidence only for the tuned subcase
- Review: rejected
- Compatibility: conflict for the physical/topological reading
- Epistemic: refuted as an amplitude-robust, phase-independent statement
- Relationship: qualified source evidence mapping to C-SG-001, C-SG-005, C-SG-011, and C-SG-013; supersedes none

## Promotion Transaction

No registry or release change is made. P051 freezes the reusable numerical
surface and all attempts, terminally qualifies NC4, regenerates the migration
queue, and synchronizes proposal, decision, and effort memory. The provisional
claim identifier remains a rejected proposal record and is not inserted into
`governance/claims.yaml`.

## Continuation if Not Accepted

The migration continues to the next pending source unit. A future physical
boundary claim would require an independently specified boundary action,
phase/chirality map, well-posed coupled dynamics, charge-vacuum endpoints,
predeclared untuned predictions, and the same numerical gates.

## Done Gate

The rejection is closed. The positive solver surface, tuned-subcase audit,
common-phase and phase-relabel counterexamples, terminal source qualification,
targeted replay, regenerated queue, and empty campaign debt ledger pass. The
repository-wide gate passed with 62 accepted claims, 218 migration units, 169
pending units, 226 valid memory files, a valid skill, and 365 passing tests.
`C-SG-014` remains outside the accepted registry and supersedes nothing.

## Cross-References

See P051, NC4, `C-SG-001`, `C-SG-005`, `C-SG-011`, `C-SG-013`, the 1D solver
module, P051 source adjudication, and the active corpus-migration effort.
