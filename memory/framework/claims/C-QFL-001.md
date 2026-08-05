---
description: Accepted framework claim C-QFL-001
author: framework-registry
created: '2026-08-11T21:55:00Z'
updated: '2026-08-11T21:55:00Z'
tags:
- substrate-framework
- accepted-claim
- C-QFL-001
category: claims
confidence: established
status: active
---
# C-QFL-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let hbar, V, kappa, c, omega_0, and K be positive reals and let b be a separately supplied positive integer. Declare b independent scalar harmonic branches in three spatial dimensions, each with dispersion omega(k)=sqrt(omega_0^2+c^2*k^2), effective oscillator mass V*kappa/c^2 per wavevector, product ground state, and C-DOS-001's continuum measure V*d^3k/(2*pi)^3. One mode then has coordinate variance hbar*c^2/(2*V*kappa*omega(k)). Integrating every declared branch over 0<=|k|<=K gives exactly Sigma=b*hbar/(8*pi^2*kappa)*(K*sqrt(omega_0^2+c^2*K^2) -omega_0^2*asinh(c*K/omega_0)/c). With ell=c/omega_0, X=K*ell, beta^2=hbar*c/(kappa*ell^2), and J(X)=(X*sqrt(1+X^2)-asinh(X))/2, the same result is Sigma=b*beta^2*J(X)/(4*pi^2). J is the integral from zero to X of x^2/sqrt(1+x^2), is strictly increasing, and obeys J(X)<X^2/2 for X>0 with J(X)/(X^2/2)->1 as X->infinity. At fixed positive omega_0 the small-cutoff leading term is b*hbar*c^2*K^3/(12*pi^2*kappa*omega_0); the continuous zero-gap limit is b*hbar*c*K^2/(8*pi^2*kappa); and dSigma/dK is the positive cutoff shell b*hbar*c^2*K^2/(4*pi^2*kappa*sqrt(omega_0^2+c^2*K^2)). Separately, for any fixed nonempty finite sequence of nonnegative mode variances v_i, M=len(v), Sigma_set=sum_i v_i, and v_bar=Sigma_set/M obey M*v_bar=Sigma_set. This fixed-set identity does not imply that changing the admitted sequence leaves Sigma_set fixed: adding a zero term changes M alone, while adding a positive term changes both M and Sigma_set. These identities derive no quantization of the accepted classical medium, three-dimensional lift, vacuum preparation, beta value, stiffness, branch count, microscopic cutoff, granularity, material variance, participating-mode set, growth law, channel, probability, rate, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-DOS-001. Assumptions: The d3 scalar quadratic action normalization, independent oscillator decomposition, effective mass V*kappa/c^2, product ground state, and canonical ground-state variance are declared premises rather than consequences of C-DOS-001 or the accepted classical medium., C-DOS-001 supplies the continuum measure and dispersion only. Spatial dimension, scalar branch count, stiffness, action scale, gap, quantization volume, and radial UV cutoff remain independent inputs., The positive-gap closed form uses omega_0>0 and K>0. The zero-gap expression is its continuous limit at fixed hbar, kappa, c, K, and b, not a claim that the quantized vacuum state survives a physical medium limit., The continuum integral is cutoff dependent and exact only for its declared measure. It is not an exact finite periodic sum, renormalized observable, microscopic Brillouin-zone calculation, or material prediction., The branch multiplier assumes b independent identical scalar branches in the same declared product ground state; d=3 does not derive b., The beta-squared and ell coordinates are reparameterizations of supplied hbar, c, kappa, and omega_0. Their equality to the direct form is not independent overdetermination and selects no value., The finite-sequence theorem holds one explicitly fixed nonempty sequence of nonnegative variances. Mode count is discrete, and changing a mode set, cutoff, spectrum, weights, or state is outside a derivative at fixed total., No physical meaning for MD2's n<S rewrite follows without accepted n, state, cutoff, dynamics, participation, interaction, channel, and rate premises.. Comparators: MD2 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; its body and output were previously exposed, while P197 froze explicit premises, candidates, criteria, mutations, and ceilings before any P197 execution or implementation, C-DOS-001 supplies the continuum density and count but explicitly derives no state, occupation, coupling, or participating-mode set, C-OSC-002 supplies a distinct classical full-cycle peak/RMS identity, not an oscillator ground-state or spectral variance.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.146.0` with provenance `campaigns/P197-md2-phase-variance-audit/adjudication.yaml`.

- `campaigns/P197-md2-phase-variance-audit/verify.py`
- `campaigns/P197-md2-phase-variance-audit/reviews/independent_mode_variance_review.py`
- `campaigns/P197-md2-phase-variance-audit/reviews/replay_source_graph.py`
- `campaigns/P197-md2-phase-variance-audit/reviews/C-QFL-001-claim-review.md`
- `campaigns/P197-md2-phase-variance-audit/reviews/MD2-disposition-review.md`
- `campaigns/P197-md2-phase-variance-audit/reviews/source_adjudication.md`
- `campaigns/P197-md2-phase-variance-audit/reviews/impact_analysis.md`
- `campaigns/P197-md2-phase-variance-audit/attempts/0003/result.yaml`
- `campaigns/P197-md2-phase-variance-audit/attempts/0004/result.yaml`
- `campaigns/P197-md2-phase-variance-audit/attempts/0005/result.yaml`
- `campaigns/P197-md2-phase-variance-audit/attempts/0006/result.yaml`
- `campaigns/P197-md2-phase-variance-audit/attempts/0007/result.yaml`
- `campaigns/P197-md2-phase-variance-audit/attempts/0008/result.yaml`
- `campaigns/P197-md2-phase-variance-audit/attempts/0009/result.yaml`
- `campaigns/P197-md2-phase-variance-audit/attempts/0010/result.yaml`
- `campaigns/P197-md2-phase-variance-audit/attempts/0011/result.yaml`
- `campaigns/P197-md2-phase-variance-audit/evidence/formula-freeze.yaml`
- `campaigns/P197-md2-phase-variance-audit/evidence/input-provenance.yaml`
- `campaigns/P197-md2-phase-variance-audit/evidence/dependency-audit.yaml`
- `campaigns/P197-md2-phase-variance-audit/evidence/consumer-audit.yaml`
- `campaigns/P197-md2-phase-variance-audit/evidence/source-graph-inventory.yaml`
- `campaigns/P197-md2-phase-variance-audit/evidence/nonduplication-audit.yaml`
- `campaigns/P197-md2-phase-variance-audit/evidence/candidate-comparison.yaml`
- `campaigns/P197-md2-phase-variance-audit/evidence/implementation-audit.yaml`
- `campaigns/P197-md2-phase-variance-audit/evidence/gitnexus-impact.yaml`
- `campaigns/P197-md2-phase-variance-audit/evidence/primary-provenance.yaml`
- `campaigns/P197-md2-phase-variance-audit/evidence/source-reproduction.yaml`
- `campaigns/P197-md2-phase-variance-audit/evidence/consumer-reproduction.yaml`
- `campaigns/P197-md2-phase-variance-audit/evidence/compatibility-audit.yaml`
- `campaigns/P197-md2-phase-variance-audit/evidence/source-audit.yaml`
- `campaigns/P197-md2-phase-variance-audit/evidence/check-adjudication.yaml`
- `memory/vantasner/decisions/C-QFL-001-review.md`
- `memory/vantasner/decisions/MD2-qualified-review.md`
- `src/substrate_framework/quantum_mode_variance.py`
- `tests/test_quantum_mode_variance.py`
