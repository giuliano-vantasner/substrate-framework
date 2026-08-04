---
description: Accepted framework claim C-VEC-001
author: framework-registry
created: '2026-08-09T12:30:00Z'
updated: '2026-08-09T12:30:00Z'
tags:
- substrate-framework
- accepted-claim
- C-VEC-001
category: claims
confidence: established
status: active
---
# C-VEC-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let x be a nonempty exact real matrix with three columns, define L_i=i*x_i^a*sigma_a using the Pauli convention of C-CHI-001, let G_ij=x_i dot x_j, I1=Tr(G)^2, and I2=Tr(G^2), and use ordered sums over i,j. Then sum_ij |x_i cross x_j|^2=I1-I2 and sum_ij Tr([L_i,L_j]^2)=-8*(I1-I2). Separately declare positive exact kappa and dimensionless g. The quadratic density kappa*sum_ia(v_i^a-x_i^a/2)^2 has the unique stationary point v=x/2 and positive Hessian 2*kappa*I. If L obeys Maurer-Cartan flatness, the half connection Gamma_i=L_i/2 has F_ij(Gamma)=-[L_i,L_j]/4. Substitution into the separately declared curvature density -sum_ij Tr(F_ij*F_ij)/(2*g^2) gives -sum_ij Tr([L_i,L_j]^2)/(32*g^2)=(I1-I2)/(4*g^2), so the equally normalized leading Skyrme coupling is e=g. With L=O(p), this density is order p^4; the kinetic vector equation changes the field at order p^3/M^2 and first changes the action at order p^6/M^2 under the supplied heavy-scale counting. Conditional on the separately declared relation m_V^2=a*g^2*F^2 with positive dimensionless a and equal mass dimensions for m_V and F, e=g=m_V/(sqrt(a)*F) is dimensionless. This is an exact current-algebra and conditional leading-connection theorem. It does not derive HLS field content, a physical rho or pion, the KSRF premise or a=2, B1, c4, J1, a full-vector solution, Skyrmion stabilization, a medium response, particle values, or a substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-EFT-001, C-CHI-001. Assumptions: The current components are exact real values, the Pauli generators satisfy Tr(sigma_a*sigma_b)=2*delta_ab, and all i,j sums are ordered Euclidean sums., The mass density, positive kappa, positive dimensionless g, Maurer-Cartan equation, curvature convention, and curvature-density normalization are declared action data rather than derived physical inputs., The half-connection substitution is a leading derivative expansion. The p3/M^2 field correction and p6/M^2 action ceiling require a separately supplied heavy vector scale and consistent derivative counting., The optional mass relation m_V^2=a*g^2*F^2 is a premise with positive inputs and equal mass dimensions for m_V and F; neither it nor a=2 follows from the current algebra., Changing generator, curvature, index-sum, metric, action-sign, or Skyrme-density normalization changes the displayed coefficients and requires a separately reviewed convention map., No accepted claim identifies the declared connection with a physical vector meson or the current with a physical pion, fixes B1 c4 J1 g m_V F or a, or supplies a complete soliton or substrate model.. Comparators: S4 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; its scalar series Pauli special case polynomial specialization and pole-versus-polynomial distinction survive, while its inserted rho operator assigned tensor target-fed coefficient dimensionful e result KSRF B1 medium and physical readings are corrected qualified or rejected.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.107.0` with provenance `campaigns/P140-s4-vector-meson-c4-audit/adjudication.yaml`.

- `campaigns/P140-s4-vector-meson-c4-audit/verify.py`
- `campaigns/P140-s4-vector-meson-c4-audit/reviews/independent_hls_current_review.py`
- `campaigns/P140-s4-vector-meson-c4-audit/reviews/replay_source_graph.py`
- `campaigns/P140-s4-vector-meson-c4-audit/attempts/0002/result.yaml`
- `campaigns/P140-s4-vector-meson-c4-audit/attempts/0003/result.yaml`
- `campaigns/P140-s4-vector-meson-c4-audit/attempts/0004/result.yaml`
- `campaigns/P140-s4-vector-meson-c4-audit/attempts/0005/result.yaml`
- `campaigns/P140-s4-vector-meson-c4-audit/attempts/0006/result.yaml`
- `campaigns/P140-s4-vector-meson-c4-audit/attempts/0007/result.yaml`
- `campaigns/P140-s4-vector-meson-c4-audit/attempts/0008/result.yaml`
- `campaigns/P140-s4-vector-meson-c4-audit/attempts/0009/result.yaml`
- `campaigns/P140-s4-vector-meson-c4-audit/evidence/source-reproduction.yaml`
- `campaigns/P140-s4-vector-meson-c4-audit/evidence/source-audit.yaml`
- `campaigns/P140-s4-vector-meson-c4-audit/evidence/check-adjudication.yaml`
- `campaigns/P140-s4-vector-meson-c4-audit/evidence/input-provenance.yaml`
- `campaigns/P140-s4-vector-meson-c4-audit/evidence/dependency-audit.yaml`
- `campaigns/P140-s4-vector-meson-c4-audit/evidence/consumer-audit.yaml`
- `campaigns/P140-s4-vector-meson-c4-audit/evidence/nonduplication-audit.yaml`
- `campaigns/P140-s4-vector-meson-c4-audit/evidence/candidate-comparison.yaml`
- `campaigns/P140-s4-vector-meson-c4-audit/evidence/primary-provenance.yaml`
- `campaigns/P140-s4-vector-meson-c4-audit/evidence/literature-audit.yaml`
- `campaigns/P140-s4-vector-meson-c4-audit/reviews/source_adjudication.md`
- `campaigns/P140-s4-vector-meson-c4-audit/reviews/impact_analysis.md`
- `memory/vantasner/decisions/C-VEC-001-review.md`
- `memory/vantasner/decisions/S4-qualified-review.md`
- `src/substrate_framework/hls_reduction.py`
- `tests/test_hls_reduction.py`
