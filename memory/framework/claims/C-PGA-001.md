---
description: Accepted framework claim C-PGA-001
author: framework-registry
created: '2026-08-10T19:18:00Z'
updated: '2026-08-10T19:18:00Z'
tags:
- substrate-framework
- accepted-claim
- C-PGA-001
category: claims
confidence: established
status: active
---
# C-PGA-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

On C^3 tensor C^2, let T_a be the eight standard fundamental SU3 generators of C-LIE-001 and let t_i=sigma_i/2 be the three standard Pauli-half SU2 generators of C-REP-002. For an exact explicitly real nonzero supplied scalar y, define C_a=T_a tensor I_2, L_i=I_3 tensor t_i, and Y=y*I_6. Then every C_a and L_i is Hermitian, each factor obeys its accepted Lie bracket, all 35 cross-factor commutators among C_a, L_i, and Y vanish, and the twelve matrices are linearly independent. They therefore give a faithful finite-dimensional representation of the local Lie algebra su3 direct-sum su2 direct-sum u1. The full joint commutant of the C_a and L_i in Mat_6(C) is exactly the scalar span of I_6, so every Hermitian Abelian generator commuting with both non-Abelian factors has the form y*I_6. For separately supplied exact positive factor couplings and exact connection components, the algebra-valued connection component is their unique displayed linear sum in this fixed basis. If a compact U1 parameter is separately assigned period 2*pi, its full-turn action is exp(2*pi*i*y)*I_6 and descent to that compact parameterization additionally requires exp(2*pi*i*y)=1. These exact local matrix facts do not select a global direct product rather than a finite central quotient, a compact hypercharge normalization, physical matter representations, fields, a gauge transformation law, kinetic terms, an action, currents, couplings matched to observation, gauge bosons, a Standard Model identification, or a substrate mechanism.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-LIE-001, C-REP-002. Assumptions: The tensor carrier uses the exact standard positive-definite inner products and the fixed generator normalizations of C-LIE-001 and C-REP-002., The Abelian weight is supplied exact, explicitly real, and provably nonzero; a zero or unresolved weight is outside the faithful-rank API., The displayed connection component uses separately supplied exact components and positive exact couplings in the fixed generator basis; it is algebra data rather than a derived gauge field., Compact period theta equivalent to theta plus 2*pi is an additional declared global convention and is not inferred from the local Lie algebra., No global quotient, physical matter carrier, hypercharge table, coordinate-dependent transformation, derivative, action, kinetic coefficient, current, field equation, observation, or substrate dictionary is imported.. Comparators: SM1 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; native execution passes all six predicates without a NumPy compatibility event, while it checks only selected factor pairs, hides the nonzero U1 weight inside a rank substitution, does not compute the full joint commutant or global kernel, and constructs no compact normalization, local transformation law, physical matter table, kinetic term, action, dynamical gauge boson, or substrate mechanism.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.125.0` with provenance `campaigns/P163-sm1-combined-gauge-group-audit/adjudication.yaml`.

- `campaigns/P163-sm1-combined-gauge-group-audit/verify.py`
- `campaigns/P163-sm1-combined-gauge-group-audit/reviews/independent_product_algebra_review.py`
- `campaigns/P163-sm1-combined-gauge-group-audit/reviews/replay_source_graph.py`
- `campaigns/P163-sm1-combined-gauge-group-audit/attempts/0007/result.yaml`
- `campaigns/P163-sm1-combined-gauge-group-audit/attempts/0008/result.yaml`
- `campaigns/P163-sm1-combined-gauge-group-audit/evidence/source-reproduction.yaml`
- `campaigns/P163-sm1-combined-gauge-group-audit/evidence/source-audit.yaml`
- `campaigns/P163-sm1-combined-gauge-group-audit/evidence/check-adjudication.yaml`
- `campaigns/P163-sm1-combined-gauge-group-audit/evidence/input-provenance.yaml`
- `campaigns/P163-sm1-combined-gauge-group-audit/evidence/dependency-audit.yaml`
- `campaigns/P163-sm1-combined-gauge-group-audit/evidence/consumer-audit.yaml`
- `campaigns/P163-sm1-combined-gauge-group-audit/evidence/source-graph-inventory.yaml`
- `campaigns/P163-sm1-combined-gauge-group-audit/evidence/nonduplication-audit.yaml`
- `campaigns/P163-sm1-combined-gauge-group-audit/evidence/candidate-comparison.yaml`
- `campaigns/P163-sm1-combined-gauge-group-audit/evidence/primary-provenance.yaml`
- `campaigns/P163-sm1-combined-gauge-group-audit/reviews/source_adjudication.md`
- `campaigns/P163-sm1-combined-gauge-group-audit/reviews/impact_analysis.md`
- `memory/vantasner/decisions/C-PGA-001-review.md`
- `memory/vantasner/decisions/SM1-qualified-review.md`
- `src/substrate_framework/product_gauge.py`
- `tests/test_product_gauge.py`
