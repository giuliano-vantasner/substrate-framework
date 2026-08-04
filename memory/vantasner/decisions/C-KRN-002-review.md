---
description: Independent review of the critical Riesz logarithm and conditional force-family theorem C-KRN-002
author: vantasner-review
created: '2026-08-09T05:40:00Z'
updated: '2026-08-09T05:40:00Z'
tags: [substrate-framework, claim-review, riesz, fractional-laplacian]
category: decisions
confidence: established
status: archived
---
# Review of C-KRN-002

## Claim Under Review

C-KRN-002 derives the reference-subtracted critical limit of C-KRN-001 and an
explicit conditional source-probe radial-force ledger. It distinguishes the
subcritical, critical, and supercritical regimes and proves that inverse-square
behavior selects `d=2s+1`, not either parameter separately. It does not
construct a geometry, select a dimension, or establish a physical force.

## Sourced Inputs

The review reads v0.103.0, C-KRN-001, C-MAX-001, the frozen P136 proposal,
hash-pinned EM7 and dossier, attempts 0001 through 0008, all source/predicate/
dependency/consumer/compatibility/impact/novelty/provenance audits, the
canonical module and focused tests, and both exact derivations. Circular D3S
and QCD5 source edges grant no premise.

## Independence

The primary route takes the exact accepted subcritical normalization through a
reference-subtracted one-sided gamma limit. The independent route does not
import `momentum_kernels.py`; it reconstructs the Riesz coefficient from the
Schwinger parameter and Gaussian Fourier kernel, derives the critical limit,
normalizes the d=2 logarithm by radial flux, checks the d=1 distributional
ordinary inverse, and solves the force exponent afresh.

## Verification Status

The maximum verdict is `symbolic_verified`. The primary verifier passes
twenty-nine exact/source checks, the independent route passes fifteen exact
checks, and twenty-two focused package tests pass. The 140-predicate source
graph is regression evidence only and cannot widen the theorem or rescue EM7.

## Sensitivity and Counterexamples

Omitting the critical subtraction produces a divergent limit. Changing the
reference changes the potential but not its derivative. Source zero removes
potential and force; probe zero retains potential but removes force; changing
either sign changes the corresponding response; doubling A halves the kernel.
The valid `(s,d)=(9/10,14/5)` inverse-square pair defeats endpoint uniqueness.
The d=1 ordinary branch and the source's d=1,s=3/4 residual expose the domain
error in silently extending the subcritical integral.

## Framework Compatibility

The theorem is a compatible extension of C-KRN-001 and agrees with C-MAX-001
at the independently normalized d=2 and d=1 boundaries. It does not modify the
accepted subcritical API or infer a geometry from analytic d. Every source,
probe, boundary, convention, and force relation remains explicit.

## Dependency and Consumer Replay

The accepted dependencies are C-KRN-001 and C-MAX-001. Three declared source
dependencies and eleven direct consumers give thirteen unique hash-pinned
scripts and 140 predicates; all exit cleanly with terminal tallies. D3S and
QCD5 are both dependencies and consumers, hence circular and nonauthoritative.
Immutable YM2 and QCD2 receive alias-only compatibility for eager legacy
`np.trapz` defaults. Mutable P136 and framework code uses current APIs.

## Competing Candidate Audit

Candidate B reuses the accepted subcritical theorem. Candidate C is selected
for the exact critical subtraction. Candidate D is selected for the explicit
force dictionary and nonidentifiability result. Candidate E supplies the
necessary analytic-versus-geometric dimension boundary. Literal Candidate A
is retained only per predicate, and Candidate F closes governance.

## Four-Axis Decision

The four independent axes are:

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: exact critical and force extension of C-KRN-001 with C-MAX-001 boundary agreement

## Promotion Transaction

Promotion extends the pure momentum-kernel module and exports, adds focused
tests, C-KRN-002, release v0.104.0, generated claim/release records, qualified
EM7 disposition, and immutable P136 evidence. The queue and generated outputs
are rebuilt; source files and generated documentation are not hand-edited.

## Continuation if Not Accepted

This clause is inactive for the conditional theorem. It remains active for
the excluded geometric and physical objectives: a future proposal must
construct the space/operator, derive endpoint selection and dimensional lift,
and supply a gauge, source, force, and observational dictionary independently.

## Done Gate

Fourier convention, gamma normalization, domain split, subtraction, reference,
d=2 flux, d=1 distribution, source/probe sign, coefficient scaling,
inverse-square family, dimension semantics, dependencies, consumers, novelty,
implementation, and transactional debt are closed for C-KRN-002.

## Cross-References

See P064, P134, P136, EM3, EM7, D3S, QCD5, C-KRN-001, C-MAX-001,
`momentum_kernels.py`, `test_momentum_kernels.py`, and the parent migration
effort.
