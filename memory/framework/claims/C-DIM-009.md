---
description: Accepted framework claim C-DIM-009
author: framework-registry
created: '2026-08-11T05:02:00Z'
updated: '2026-08-11T05:02:00Z'
tags:
- substrate-framework
- accepted-claim
- C-DIM-009
category: claims
confidence: established
status: active
---
# C-DIM-009

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let D be a separately supplied exact positive real spacetime-dimension bookkeeping parameter in natural units, with [d^D x]=-D and [partial]=1. In the canonical gauge-potential convention with dimensionless action, density kappa_A F(A)^2/4, dimensionless positive kappa_A, and covariant derivative partial-i*g*A, the exact mass exponents are [A]=(D-2)/2, [g]=(4-D)/2, [F(A)]=D/2, and [F(A)^2]=D. In a quadratic momentum action whose transverse projector is dimensionless, its scalar coefficient Pi_hat has exponent two. The special scale-free ansatz Pi_hat=g^2*c with nonzero dimensionless c is homogeneous exactly when D=2. This implication is not a universal polarization no-go: with a separately supplied positive mass scale M, g^2*M^(D-2)*c has exponent two for every D. In D=4, for momentum-square Q and positive M, every expression Q*f(Q/M^2) has exponent two for a dimensionless f; constant, Q/(Q+M^2), and log(1+Q/M^2) are exact distinct examples, so dimensional analysis alone selects neither a logarithm nor any form factor or coefficient. In the connection-field convention B=g*A and F(B)=g*F(A), [B]=1, [F(B)]=2, and the identical density is kappa_B F(B)^2/4 with kappa_B=kappa_A/g^2 and [kappa_B]=D-4. For a dimensionless fixed generator basis, the convention change T_a'=rho*T_a, g'=g/rho with supplied positive rho gives T(R)'=rho^2*T(R) and preserves g^2*T(R); a trace factor alone carries no spacetime dimension and is not a convention-preserving Abelian limit. These exact identities perform dimensional and normalization bookkeeping only. They do not derive a loop determinant, numerator, regulator, subtraction, counterterm, matching scale, kinetic coefficient value, total coupling, preferred dimension, logarithmic running, dimensional lift, propagating gauge particle, physical gauge group, observable, or substrate mechanism.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-GAU-001, C-NAG-001. Assumptions: D is an exact positive real bookkeeping parameter; statements about an integer number of field components are outside this claim., Natural units, a dimensionless action, a dimensionless transverse projector, and the canonical density normalization are separately declared rather than derived., The pure-coupling implication assumes a nonzero dimensionless multiplier and no independently supplied scale; the mass and form-factor examples are counterfamilies, not quantum loop derivations., Couplings, kinetic coefficients, masses, trace indices, and generator scales supplied to the package API are exact, explicitly real, and positive., The generator basis is dimensionless and its rescaling is accompanied by the inverse coupling rescaling; changing a trace normalization alone changes the convention., C-GAU-001 and C-NAG-001 supply only connection and curvature algebra; no kinetic action, quantum matter content, regulator, matching prescription, or physical interpretation is imported from them.. Comparators: GK1 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; native execution passes all eleven predicates and its trace, component-count, and narrow pure-coupling D=2 identities survive, while its complex-scalar numerator conflicts with the accepted bubble-seagull kernel and exact scale and form-factor counterfamilies refute the universal two-dimensional and logarithm-selection readings; it supplies no total kinetic normalization, physical gauge sector, dimensional lift, or substrate mechanism.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.128.0` with provenance `campaigns/P176-gk1-gauge-kinetic-dimensionality-audit/adjudication.yaml`.

- `campaigns/P176-gk1-gauge-kinetic-dimensionality-audit/verify.py`
- `campaigns/P176-gk1-gauge-kinetic-dimensionality-audit/reviews/independent_dimension_review.py`
- `campaigns/P176-gk1-gauge-kinetic-dimensionality-audit/reviews/replay_source_graph.py`
- `campaigns/P176-gk1-gauge-kinetic-dimensionality-audit/attempts/0005/result.yaml`
- `campaigns/P176-gk1-gauge-kinetic-dimensionality-audit/attempts/0006/result.yaml`
- `campaigns/P176-gk1-gauge-kinetic-dimensionality-audit/attempts/0007/result.yaml`
- `campaigns/P176-gk1-gauge-kinetic-dimensionality-audit/attempts/0009/result.yaml`
- `campaigns/P176-gk1-gauge-kinetic-dimensionality-audit/attempts/0010/result.yaml`
- `campaigns/P176-gk1-gauge-kinetic-dimensionality-audit/attempts/0012/result.yaml`
- `campaigns/P176-gk1-gauge-kinetic-dimensionality-audit/evidence/source-reproduction.yaml`
- `campaigns/P176-gk1-gauge-kinetic-dimensionality-audit/evidence/source-audit.yaml`
- `campaigns/P176-gk1-gauge-kinetic-dimensionality-audit/evidence/check-adjudication.yaml`
- `campaigns/P176-gk1-gauge-kinetic-dimensionality-audit/evidence/input-provenance.yaml`
- `campaigns/P176-gk1-gauge-kinetic-dimensionality-audit/evidence/dependency-audit.yaml`
- `campaigns/P176-gk1-gauge-kinetic-dimensionality-audit/evidence/consumer-audit.yaml`
- `campaigns/P176-gk1-gauge-kinetic-dimensionality-audit/evidence/source-graph-inventory.yaml`
- `campaigns/P176-gk1-gauge-kinetic-dimensionality-audit/evidence/nonduplication-audit.yaml`
- `campaigns/P176-gk1-gauge-kinetic-dimensionality-audit/evidence/candidate-comparison.yaml`
- `campaigns/P176-gk1-gauge-kinetic-dimensionality-audit/evidence/accepted-evidence-reuse.yaml`
- `campaigns/P176-gk1-gauge-kinetic-dimensionality-audit/evidence/primary-provenance.yaml`
- `campaigns/P176-gk1-gauge-kinetic-dimensionality-audit/evidence/literature-audit.yaml`
- `campaigns/P176-gk1-gauge-kinetic-dimensionality-audit/reviews/source_adjudication.md`
- `campaigns/P176-gk1-gauge-kinetic-dimensionality-audit/reviews/impact_analysis.md`
- `memory/vantasner/decisions/C-DIM-009-review.md`
- `memory/vantasner/decisions/GK1-qualified-review.md`
- `src/substrate_framework/gauge_dimensions.py`
- `tests/test_gauge_dimensions.py`
