---
description: Accepted framework claim C-LIE-001
author: framework-registry
created: '2026-08-01T15:07:43Z'
updated: '2026-08-01T15:07:43Z'
tags:
- substrate-framework
- accepted-claim
- C-LIE-001
category: claims
confidence: established
status: active
---
# C-LIE-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

For the eight explicit standard fundamental SU(3) generators T_a=lambda_a/2, each generator is Hermitian and traceless and Tr(T_a*T_b)=(1/2)*delta_ab. With [T_a,T_b]=i*f_abc*T_c and f_abc=-2*i*Tr([T_a,T_b]*T_c), the structure constants are totally antisymmetric. The exact representation invariants are T_F=1/2, C_F=4/3 from sum_a T_a^2=(4/3)I_3, and C_A=3 from both sum_a F_a^2=3I_8 for (F_a)_bc=-i*f_abc and sum_cd f_acd*f_bcd=3*delta_ab. These are convention-specific algebraic facts and establish no physical gauge-sector identification.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `native`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: none. Assumptions: The explicit matrices use the standard Gell-Mann ordering and T_a=lambda_a/2 normalization., Generator and structure-constant indices run from zero through seven in the package API., The commutator convention is [T_a,T_b]=i*f_abc*T_c., No loop coefficient, matter content, or physical substrate interpretation is part of the claim.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.21.0` with provenance `campaigns/P024-su3-one-loop-coefficient/adjudication.yaml`.

- `campaigns/P024-su3-one-loop-coefficient/verify.py`
- `campaigns/P024-su3-one-loop-coefficient/attempts/0001/result.yaml`
- `campaigns/P024-su3-one-loop-coefficient/reviews/independent_completeness_review.py`
- `campaigns/P024-su3-one-loop-coefficient/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-LIE-001-review.md`
- `tests/test_su3.py`
- `formal/SubstrateFramework/Ingested/Phase8QCD_SU3GaugeFacts.lean`
