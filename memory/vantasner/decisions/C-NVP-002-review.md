---
description: Accepted review of generic finite-Lie scalar vacuum polarization claim C-NVP-002
author: vantasner-review
created: '2026-08-10T17:05:00Z'
updated: '2026-08-10T17:05:00Z'
tags: [substrate-framework, claim-review, C-NVP-002, nonabelian-vacuum-polarization]
category: decisions
confidence: established
status: archived
---
# C-NVP-002 Claim Review

## Claim Under Review

C-NVP-002 states a conditional exact one-loop theorem for massive complex
scalar multiplets in a supplied finite exact Hermitian Lie representation on
Euclidean two-space. It validates the structure constants and trace metric,
then covers the color-indexed scalar kernel, bubble--seagull Ward cancellation,
exact limits, typed local coefficients, and full leading curvature completion.

## Sourced Inputs

The review read v0.123.0, C-VAC-001, C-NAG-001, the compatibility surface of
C-NVP-001, both frozen P160 proposals, QCD1 and its dossier, all exact and
independent evidence, primary-source provenance, impact analysis, and source
consumers. No QCD1 action, statistics, massless coefficient, bare term,
physical color dictionary, or dimensional lift is imported.

## Independence

The canonical route validates arbitrary supplied generators and structure
constants, then composes the accepted Abelian ledger and reconstructs the
proper-time coefficient. The independent route rebuilds SU3 locally and
rederives the scalar parameter integral, bubble--seagull contraction, trace
index, proper-time mass integral, and noncommuting-background curvature without
importing the new generic function.

## Verification Status

Exact evaluated SymPy expressions support symbolic verification. The primary
and independent routes pass 38 and 27 checks. Fundamental SU3, direct-sum SU3,
and SU2 specializations exercise representation dependence. The scalar limits,
Ward residuals, and covariant-completion residuals evaluate exactly.

## Sensitivity and Counterexamples

Wrong-sign structure constants and nonorthogonal rescaling are rejected.
Direct-sum generators double T(R). Deleting or sign-flipping the seagull breaks
the Ward contraction. The QCD1 numerator differs from the scalar numerator and
has the wrong massless behavior. A curl-only background misses noncommuting
curvature. Bare and counterterm families defeat unique induction.

## Framework Compatibility

The implementation is a compatible additive generalization. C-VAC-001 fixes
the declared complex-scalar determinant and exact Abelian kernel; C-NAG-001
fixes the connection and curvature convention. The existing C-NVP-001 class,
function signature, return type, and field meanings are preserved through an
exact SU2 specialization rather than rewritten in consumers.

## Dependency and Consumer Replay

Direct dependencies are C-VAC-001 and C-NAG-001; C-NVP-001 is a compatibility
consumer, not a hidden scientific premise. GitNexus reports LOW risk, one
direct caller from the preserved wrapper, and no affected process. P158 and
P159 pass 32 and 31 checks. The 17-node graph passes 28 checks over 170 source
predicates; pending physical-sector sources receive no authority. Immutable
QCD2's version-only `np.trapz` access is replayed solely through `np.trapezoid`.

## Competing Candidate Audit

Candidates were frozen before source-body inspection. Accepted composition
alone lacked generic representation validation and a reusable API; an SU3-only
wrapper duplicated the SU2 theorem; a physical QCD candidate lacked its action
and matching premises. The generic theorem wins by dependency closure,
parameter economy, and reusable framework fit rather than numerical agreement.

## Four-Axis Decision

The four status axes support conditional additive promotion.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: generic finite-representation extension preserving C-NVP-001

## Promotion Transaction

Promotion adds the generic pure API and tests, C-NVP-002, P160 evidence,
release v0.124.0, qualified QCD1 disposition, generated records, and accepted
memory. The SU2 API remains stable and all accepted consumers replay.

## Continuation if Not Accepted

Nonacceptance would retain the implementation as proposal evidence and return
to a direct diagrammatic or background-field derivation. Physical QCD would
still require a separate declared action, matter content, regulator,
renormalization, matching, dimension, state, and observable proposal.

## Done Gate

The registry, release, disposition, generated documentation, memory,
compatibility policy, downstream replay, and debt ledger must agree. The claim
remains conditional and cannot promote QCD1's unique physical induction.

## Cross-References

See P160, QCD1, C-VAC-001, C-NAG-001, C-NVP-001,
`nonabelian_vacuum_polarization.py`, its focused tests, and P160's evidence.
