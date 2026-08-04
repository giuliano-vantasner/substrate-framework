---
description: Accepted framework claim C-GOR-001
author: framework-registry
created: '2026-08-09T15:25:00Z'
updated: '2026-08-09T15:25:00Z'
tags:
- substrate-framework
- accepted-claim
- C-GOR-001
category: claims
confidence: established
status: active
---
# C-GOR-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let eta_ab=diag(-1,1,1,1), let u^a be an exact real unit timelike four-velocity with eta_ab*u^a*u^b=-1, and let n be an exact positive refractive index. The signature-consistent mostly-plus Gordon effective inverse metric and metric are g^ab=eta^ab+(1-n^2)*u^a*u^b and g_ab=eta_ab+(1-1/n^2)*u_a*u_b. They are exact mutual inverses with determinants -n^2 and -1/n^2, so no positive-index sqrt(2) pole occurs; in the medium rest frame g_ab=diag(-1/n^2,1,1,1) and its null phase speed is 1/n. If the medium has constant z velocity v with |v|<1 and gamma^2=1/(1-v^2), while n=n(x) depends only on the transverse coordinate, define K=(n*n_xx-2*n_x^2)/n^2. In coordinates (t,x,y,z), the only nonzero covariant Einstein components are G_tt=-gamma^2*v^2*K, G_tz=G_zt=gamma^2*v*K, G_yy=-K, and G_zz=-gamma^2*K; G_xx=0 and the Ricci scalar is 2*K. Direct Christoffel reconstruction satisfies the contracted Bianchi identity componentwise. A constant index is flat. At v=1/2 and the local profile data n=2, n_x=1, n_xx=0, G_tt=1/6, G_tz=-2*G_tt, G_yy=3*G_tt, and G_zz=4*G_tt. This is an exact conditional effective-wave-geometry theorem. It does not supply a dielectric or matter action, conserved material stress, Einstein-source match, coupling, boundary-value solution, dynamical or physical gravity, observation, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: none. Assumptions: The metric signature is mostly plus, the four-velocity is exact and normalized to minus one, and the refractive index is exact and positive; floating inputs are outside the exact API., The Gordon rank-one relation is an approved effective-medium input translated consistently from the mostly-minus convention; it is not derived from an accepted substrate or material action., The transverse-profile tensor additionally assumes a spatially constant z velocity with absolute value below one and a twice differentiable positive n depending only on x., The displayed Einstein tensor uses the framework's stated Riemann and Ricci sign convention. Changing that convention requires a separately reviewed map, while the metric inverse determinant signature and null cone are convention-independent., A Gordon metric is an effective propagation geometry. Nonzero curvature and the contracted Bianchi identity do not identify a material stress or make the metric a solution of physical Einstein dynamics., Any Einstein-source interpretation requires a separately declared medium and matter action, componentwise conserved stress, coupling, field equations, and boundary data., No accepted claim identifies n or u with a sine-Gordon breather, fixes a physical refractive profile, coupling, or medium flow, or supplies physical gravity, observation, or substrate ontology.. Comparators: G2 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; native execution passes all six checks with no NumPy compatibility event, while its copied-sign convention, spurious sqrt-two pole, positive-definite n=2 witness, five-sixths value, absent stress match, free-coupling argument, dynamical-gravity, and substrate readings are corrected qualified or rejected.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.109.0` with provenance `campaigns/P142-g2-gordon-metric-audit/adjudication.yaml`.

- `campaigns/P142-g2-gordon-metric-audit/verify.py`
- `campaigns/P142-g2-gordon-metric-audit/reviews/independent_gordon_review.py`
- `campaigns/P142-g2-gordon-metric-audit/reviews/replay_source_graph.py`
- `campaigns/P142-g2-gordon-metric-audit/attempts/0002/result.yaml`
- `campaigns/P142-g2-gordon-metric-audit/attempts/0003/result.yaml`
- `campaigns/P142-g2-gordon-metric-audit/attempts/0004/result.yaml`
- `campaigns/P142-g2-gordon-metric-audit/attempts/0005/result.yaml`
- `campaigns/P142-g2-gordon-metric-audit/attempts/0006/result.yaml`
- `campaigns/P142-g2-gordon-metric-audit/attempts/0007/result.yaml`
- `campaigns/P142-g2-gordon-metric-audit/attempts/0008/result.yaml`
- `campaigns/P142-g2-gordon-metric-audit/attempts/0009/result.yaml`
- `campaigns/P142-g2-gordon-metric-audit/attempts/0010/result.yaml`
- `campaigns/P142-g2-gordon-metric-audit/attempts/0011/result.yaml`
- `campaigns/P142-g2-gordon-metric-audit/attempts/0012/result.yaml`
- `campaigns/P142-g2-gordon-metric-audit/attempts/0013/result.yaml`
- `campaigns/P142-g2-gordon-metric-audit/evidence/source-reproduction.yaml`
- `campaigns/P142-g2-gordon-metric-audit/evidence/source-audit.yaml`
- `campaigns/P142-g2-gordon-metric-audit/evidence/check-adjudication.yaml`
- `campaigns/P142-g2-gordon-metric-audit/evidence/input-provenance.yaml`
- `campaigns/P142-g2-gordon-metric-audit/evidence/dependency-audit.yaml`
- `campaigns/P142-g2-gordon-metric-audit/evidence/consumer-audit.yaml`
- `campaigns/P142-g2-gordon-metric-audit/evidence/nonduplication-audit.yaml`
- `campaigns/P142-g2-gordon-metric-audit/evidence/candidate-comparison.yaml`
- `campaigns/P142-g2-gordon-metric-audit/evidence/primary-provenance.yaml`
- `campaigns/P142-g2-gordon-metric-audit/evidence/literature-audit.yaml`
- `campaigns/P142-g2-gordon-metric-audit/reviews/source_adjudication.md`
- `campaigns/P142-g2-gordon-metric-audit/reviews/impact_analysis.md`
- `memory/vantasner/decisions/C-GOR-001-review.md`
- `memory/vantasner/decisions/G2-qualified-review.md`
- `src/substrate_framework/gordon_metric.py`
- `tests/test_gordon_metric.py`
