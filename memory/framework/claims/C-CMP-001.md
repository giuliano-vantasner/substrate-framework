---
description: Accepted framework claim C-CMP-001
author: framework-registry
created: '2026-08-08T05:30:00Z'
updated: '2026-08-08T05:30:00Z'
tags:
- substrate-framework
- accepted-claim
- C-CMP-001
category: claims
confidence: established
status: active
---
# C-CMP-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let m be a positive integer, let Delta_j be real nonzero detunings, and let c_j be real nonnegative coupling products with at least one c_j>0. For real Gamma>0 and omega>0, C-RES-001's common-loss zero-energy magnitude is K(Gamma)=Gamma*sum_(j=1)^m c_j/(Delta_j^2+Gamma^2/4). Composing it with C-DYN-001's nominal count Q_nom=omega/(2*pi*Gamma) in a declared 1/Gamma quadratic-envelope window gives exactly H_nom(Gamma)=omega/(2*pi)*sum_j c_j/(Delta_j^2+Gamma^2/4). This product is strictly positive and strictly decreasing for Gamma>0, with derivative -omega*Gamma/(4*pi)*sum_j c_j/(Delta_j^2+Gamma^2/4)^2, finite positive right limit omega/(2*pi)*sum_j c_j/Delta_j^2 at zero loss, and inverse-square large-loss coefficient (2*omega/pi)*sum_j c_j. On the source-style extension that assigns zero at Gamma=0 and at Gamma>=2*omega, the right limit at zero and left limit omega/(2*pi)*sum_j c_j/(Delta_j^2+omega^2) at 2*omega are both positive. The extension therefore has two jumps, has a nonattained supremum at zero loss, and has no positive-loss maximizer. Replacing the nominal count by the actual underdamped oscillator count Q_act=sqrt(omega^2-Gamma^2/4)/(2*pi*Gamma) gives an also strictly decreasing product on 0<Gamma<2*omega with the same zero-loss limit and zero critical left limit. Positive Gamma-independent dimensionless factors preserve these loss conclusions. For a single pair, replacing the linear opening by Gamma^p gives a stationary surface Gamma^2=4*Delta^2*(p-1)/(3-p), which is a positive finite interior point only for 1<p<3; the source linear case p=1 has none. If Delta, Gamma, and omega have one energy or inverse-time dimension and c has its square, H has one such dimension. A common rescaling including c->rho^2*c gives H->rho*H, while holding c fixed gives H->H/rho. These are conditional finite-matrix and window-count identities, not a phase-coherence, probability, transition-rate, nuclear-channel, material, magnitude, yield, heat, or observation theorem.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-RES-001, C-DYN-001. Assumptions: The family is finite and nonempty; every Delta_j is exact, real, and nonzero; every c_j is exact, real, and nonnegative; and at least one c_j is positive., The common-loss magnitude uses C-RES-001's E=0 equal-product pair convention with one real Gamma>=0. Signed or complex products, unequal member losses, unequal pair shifts, or nonzero spectral energy require separate analysis., The nominal factor omega/(2*pi*Gamma) is only C-DYN-001's natural-frequency count in a declared 1/Gamma quadratic-envelope window. It is not actual near-critical cycles, phase coherence, survival, or nonlinear breather existence., The actual-cycle specialization requires 0<Gamma<2*omega and a declared linear oscillator natural frequency omega. A finite-amplitude sub-gap breather frequency is not automatically such a frequency., The source-style zero-cutoff function is an explicit discontinuous convention. Taking a continuous composed extension at zero or using the actual-cycle critical limit defines a different boundary object., Dimension statements require Delta, Gamma, and omega in one energy or inverse-time convention and each coupling product in its square. Setting hbar=1 is a declared unit convention and does not supply kinetics., Multiplicative activation gates, count factors, thermal gates, and normalizations must be positive and Gamma independent to preserve the loss theorem. Their physical meanings and parameter maps are separate premises., A physical rate requires accepted states, interaction normalization, final-state measure or spectral density, bath dynamics, probability convention, and parameter provenance; none follows from this composition.. Comparators: CM2 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; its individual conditional factors reproduce, while its symbolic K_pos substitution, floating null, grid-defined support, positive-loss sweet spot, phase-coherence, nuclear-rate, magnitude, channel, material, yield, heat, and observation readings are qualified or rejected.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.96.0` with provenance `campaigns/P116-cm2-composite-rate-law-audit/adjudication.yaml`.

- `campaigns/P116-cm2-composite-rate-law-audit/verify.py`
- `campaigns/P116-cm2-composite-rate-law-audit/reviews/independent_composite_review.py`
- `campaigns/P116-cm2-composite-rate-law-audit/attempts/0001/result.yaml`
- `campaigns/P116-cm2-composite-rate-law-audit/attempts/0002/result.yaml`
- `campaigns/P116-cm2-composite-rate-law-audit/attempts/0003/result.yaml`
- `campaigns/P116-cm2-composite-rate-law-audit/attempts/0004/result.yaml`
- `campaigns/P116-cm2-composite-rate-law-audit/attempts/0005/result.yaml`
- `campaigns/P116-cm2-composite-rate-law-audit/attempts/0006/result.yaml`
- `campaigns/P116-cm2-composite-rate-law-audit/attempts/0007/result.yaml`
- `campaigns/P116-cm2-composite-rate-law-audit/attempts/0008/result.yaml`
- `campaigns/P116-cm2-composite-rate-law-audit/attempts/0009/result.yaml`
- `campaigns/P116-cm2-composite-rate-law-audit/evidence/source-reproduction.yaml`
- `campaigns/P116-cm2-composite-rate-law-audit/evidence/source-audit.yaml`
- `campaigns/P116-cm2-composite-rate-law-audit/evidence/check-adjudication.yaml`
- `campaigns/P116-cm2-composite-rate-law-audit/evidence/input-provenance.yaml`
- `campaigns/P116-cm2-composite-rate-law-audit/evidence/dependency-audit.yaml`
- `campaigns/P116-cm2-composite-rate-law-audit/evidence/consumer-audit.yaml`
- `campaigns/P116-cm2-composite-rate-law-audit/evidence/candidate-comparison.yaml`
- `campaigns/P116-cm2-composite-rate-law-audit/evidence/primary-provenance.yaml`
- `campaigns/P116-cm2-composite-rate-law-audit/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-CMP-001-review.md`
- `src/substrate_framework/composite_factors.py`
- `tests/test_composite_factors.py`
