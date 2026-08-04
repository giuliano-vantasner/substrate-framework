---
description: Independent review of the conditional massive scalar-QED2 vacuum-polarization theorem C-VAC-001
author: vantasner-review
created: '2026-08-09T04:20:00Z'
updated: '2026-08-09T04:20:00Z'
tags: [substrate-framework, claim-review, scalar-qed, vacuum-polarization]
category: decisions
confidence: established
status: archived
---
# Review of C-VAC-001

## Claim Under Review

C-VAC-001 states the exact one-loop transverse kernel of a separately declared
massive complex scalar in Euclidean two dimensions. It fixes the scalar versus
projector form-factor convention, derives the bubble-plus-seagull Ward
cancellation, gives the real closed form and low-momentum local coefficient,
and distinguishes the infrared-divergent massless scalar limit from the finite
fermionic Schwinger result. It does not quantize the accepted classical field,
identify electric charge, generate a physical gauge sector, or establish a
propagator pole.

## Sourced Inputs

The review reads v0.102.0, C-GAU-001, the C-U1-001 and C-MAX-001 boundary
claims, the frozen P135 proposal, hash-pinned EM5 and dossier, attempts 0001
through 0010, all source/predicate/dependency/consumer/compatibility/impact/
novelty/provenance audits, the canonical module and focused tests, and both
exact derivations. Pending EM7, M1, and consumers grant no premise.

## Independence

The primary route uses the canonical real-parameter reduction and audits every
EM5 predicate. The independent route does not import
`vacuum_polarization.py`; it reconstructs the bubble contraction, seagull
cancellation, scalar Feynman numerator, real antiderivative, low-momentum
series, fixed-momentum limits, and constant-field proper-time coefficient.

## Verification Status

The maximum verdict is `symbolic_verified`. The primary verifier passes fifty
exact/source checks, the independent route passes twenty-nine exact checks,
and twenty-seven focused package tests pass. The canonical API derives its
stored limits from the closed form. The 219-predicate source graph is
regression evidence only and cannot upgrade the theorem or rescue EM5.

## Sensitivity and Counterexamples

Removing or sign-flipping the seagull breaks the Ward residual. Replacing the
scalar `(1-2*x)^2` numerator by the fermionic `4*x*(1-x)` shape changes the
massless limit from positive infinity to `e^2/pi`. Charge halving changes the
kernel quadratically; mass and species mutations change it independently.
The next low-momentum coefficient detects changes beyond the leading local
term. The zero-momentum projector domain, heavy-mass limit, field-rescaling
counterexample, missing bare kernel, and nonflat zero-action connection all
break the corresponding source interpretations.

## Framework Compatibility

The theorem is a compatible extension of C-GAU-001's connection convention.
Its quantum complex scalar, mass, charge, multiplicity, determinant, regulator,
and loop measure are declared imports rather than retrofits to C-U1-001.
C-MAX-001 supplies the boundary that a bare local kinetic coefficient remains
separate. Local counterterms, analytic continuation, gauge fixing, and field
normalization must be supplied before any propagator statement.

## Dependency and Consumer Replay

The accepted dependency is C-GAU-001. Five declared source dependencies and
fifteen direct consumers give nineteen unique hash-pinned scripts and 219
predicates; all exit cleanly with terminal tallies. M1 is both a premise and a
consumer, and EM7 returns through D3S, so those source edges are circular and
nonauthoritative. Immutable YM2 and QCD2 receive alias-only compatibility for
eager legacy `np.trapz` defaults. Mutable P135 and framework code uses current
APIs and contains no direct legacy call.

## Competing Candidate Audit

Candidate B is selected because a complete quantum action, scalar numerator,
seagull, Ward derivation, dimensions, and all limits close under the frozen
structural criteria. Candidate C retains only projector kinematics. Candidate
D provides the necessary bare-coefficient, counterterm, normalization,
statistics, and limit-order ceiling. Literal Candidate A is retained only for
individually surviving predicates, and Candidate E closes governance.
Numerical or source-coefficient closeness plays no role.

## Four-Axis Decision

The claim earns four independent accepted axes.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: new conditional quantum-field theorem depending on C-GAU-001

## Promotion Transaction

Promotion adds the pure vacuum-polarization module and exports, focused tests,
C-VAC-001, release v0.103.0, generated claim/release records, qualified EM5
disposition, and immutable P135 evidence. The editable queue is regenerated;
source files and generated documentation are not hand-edited.

## Continuation if Not Accepted

This clause is inactive for the conditional theorem. It remains active for all
excluded physical claims: a future proposal must separately derive the quantum
ontology, charge identification, bare gauge action, continuation, pole,
degrees of freedom, dimension lift, and observational dictionary.

## Done Gate

Action and tensor conventions, scalar statistics, Ward cancellation, exact
closed form, low/massless/heavy limits, dimensions, mutations, independent
proper-time derivation, dependencies, consumers, novelty, implementation, and
transactional debt are closed for C-VAC-001.

## Cross-References

See P014, P030, P134, P135, EM1, EM2, EM3, EM5, EM7, M1, C-U1-001,
C-GAU-001, C-MAX-001, `vacuum_polarization.py`,
`test_vacuum_polarization.py`, and the parent migration effort.
