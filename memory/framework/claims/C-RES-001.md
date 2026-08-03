---
description: Accepted framework claim C-RES-001
author: framework-registry
created: '2026-08-07T23:30:00Z'
updated: '2026-08-07T23:30:00Z'
tags:
- substrate-framework
- accepted-claim
- C-RES-001
category: claims
confidence: established
status: active
---
# C-RES-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let H_PP be a finite square complex endpoint block, H_QQ a finite square complex intermediate block, and H_PQ and H_QP compatible complex blocks. At a declared real spectral energy E for which E*I-H_QQ is invertible, define the exact finite effective block H_eff(E)=H_PP+H_PQ*(E*I-H_QQ)^-1*H_QP. For a two-state intermediate block with diagonal energies +Delta-i*Gamma/2 and -Delta-i*Gamma/2, real nonzero Delta, real Gamma>=0, and declared off-diagonal coupling products c_plus and c_minus, its paired endpoint contribution is exactly R(E)=c_plus/(E-Delta+i*Gamma/2)+c_minus/(E+Delta+i*Gamma/2). When both products equal c, this becomes 2*c*(E+i*Gamma/2)/((E+i*Gamma/2)^2-Delta^2), and at E=0 it is -i*c*Gamma/(Delta^2+Gamma^2/4). At zero loss and E=0 the contribution cancels exactly if and only if c_plus=c_minus; away from E=0 the equal- product zero-loss expression is 2*c*E/(E^2-Delta^2) where defined. For nonzero c, the magnitude of the equal-product E=0 contribution on Gamma>0 vanishes as Gamma tends to zero and infinity, has small-loss coefficient -i*c/Delta^2 and large-loss coefficient -4*i*c/Gamma, and has its unique positive maximum |c|/|Delta| at Gamma=2*|Delta|. A sum of L identical pairs grows by L when each pair product is fixed and is invariant when the total product weight is held fixed by using c/L per pair; changing L is model enlargement, not a numerical refinement. These are exact finite complex-matrix identities. A common imaginary shift is a declared phenomenological input and the theorem establishes no microscopic bath, complete open-system or Lindblad dynamics, physical loss mechanism, normalized probability, transition rate, nuclear or phonon channel, material realization, magnitude, or observation.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: none. Assumptions: Every displayed block is finite-dimensional over the complex numbers, all shapes are compatible, and E*I-H_QQ is invertible at the declared spectral energy., The effective-block convention is exactly H_PP+H_PQ*(E*I-H_QQ)^-1*H_QP; reversing the resolvent sign or silently replacing a supplied coupling orientation by an adjoint changes the result., The paired specialization uses real nonzero Delta, real Gamma>=0, diagonal intermediate energies plus and minus Delta minus i*Gamma/2, and explicitly declared complex coupling products c_plus and c_minus., The if-and-only-if cancellation statement is restricted to E=0 and Gamma=0; off-shell energy, unequal detunings, or unequal complex products need not cancel., Peak and asymptotic magnitude statements require equal nonzero product c and vary positive Gamma at fixed Delta and c. They do not assert monotone growth., Pair-count statements compare explicitly declared coupling normalizations. Adding intermediate pairs changes the model and is not mesh, domain, timestep, or tolerance refinement., The imaginary shift is input rather than a derived self-energy. A physical interpretation requires separately accepted states, bath dynamics, normalization, measurement or spectral rule, and parameter map.. Comparators: PN4 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; its exact E=0 equal-product formula reproduces after freeze, while its zero-loss transfer, refinement, open-channel, probability, rate, nuclear, phonon, material, magnitude, and literature readings are rejected or qualified.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.94.0` with provenance `campaigns/P112-pn4-lossy-paired-resolvent-audit/adjudication.yaml`.

- `campaigns/P112-pn4-lossy-paired-resolvent-audit/verify.py`
- `campaigns/P112-pn4-lossy-paired-resolvent-audit/reviews/independent_resolvent_review.py`
- `campaigns/P112-pn4-lossy-paired-resolvent-audit/attempts/0001/result.yaml`
- `campaigns/P112-pn4-lossy-paired-resolvent-audit/attempts/0003/result.yaml`
- `campaigns/P112-pn4-lossy-paired-resolvent-audit/attempts/0004/result.yaml`
- `campaigns/P112-pn4-lossy-paired-resolvent-audit/attempts/0005/result.yaml`
- `campaigns/P112-pn4-lossy-paired-resolvent-audit/attempts/0006/result.yaml`
- `campaigns/P112-pn4-lossy-paired-resolvent-audit/evidence/source-reproduction.yaml`
- `campaigns/P112-pn4-lossy-paired-resolvent-audit/evidence/source-audit.yaml`
- `campaigns/P112-pn4-lossy-paired-resolvent-audit/evidence/check-adjudication.yaml`
- `campaigns/P112-pn4-lossy-paired-resolvent-audit/evidence/dependency-audit.yaml`
- `campaigns/P112-pn4-lossy-paired-resolvent-audit/evidence/consumer-audit.yaml`
- `campaigns/P112-pn4-lossy-paired-resolvent-audit/evidence/candidate-comparison.yaml`
- `campaigns/P112-pn4-lossy-paired-resolvent-audit/evidence/primary-provenance.yaml`
- `campaigns/P112-pn4-lossy-paired-resolvent-audit/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-RES-001-review.md`
- `tests/test_paired_resolvent.py`
