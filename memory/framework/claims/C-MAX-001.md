---
description: Accepted framework claim C-MAX-001
author: framework-registry
created: '2026-08-09T02:50:00Z'
updated: '2026-08-09T02:50:00Z'
tags:
- substrate-framework
- accepted-claim
- C-MAX-001
category: claims
confidence: established
status: active
---
# C-MAX-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Conditional on C-GAU-001's real connection and field-strength convention, a positive integer spatial dimension d, flat (d+1)-dimensional signature (+,-,...,-), a positive supplied kinetic coefficient kappa, and a smooth supplied contravariant current j^mu, the declared action density L=-kappa*F_mu_nu*F^mu_nu/4-j^mu*A_mu has, under compactly supported variations, the exact Euler equation kappa*partial_mu F^mu_nu=j^nu. The Bianchi identity follows from F=dA; the double divergence vanishes identically, so a solution requires partial_nu j^nu=0, which is also the bulk condition for gauge invariance of the source action after its boundary term is removed. Deleting the kinetic term gives only j^nu=0 and does not force A to be pure gauge. In the static convention A_0=phi, A_i=0, j^0=rho, the equation is -kappa*Delta(phi)=rho and E=-grad(phi). Let S_(d-1)=2*pi^(d/2)/Gamma(d/2), let r>0, and separately supply a point source Q with normalized flux kappa*S_(d-1)*r^(d-1)*E_r=Q. For integer d>2 and phi tending to zero at infinity, phi=Q/[kappa*(d-2)*S_(d-1)*r^(d-2)] and E_r=Q/[kappa*S_(d-1)*r^(d-1)]. For d=2, fixing phi=phi0 at positive r0 gives phi=phi0-Q*log(r/r0)/(2*pi*kappa); for the even d=1 full-line branch with phi(0)=phi0, phi=phi0-Q*r/(2*kappa). These branches are harmonic away from the source and have the same normalized radial flux. The potential decays at infinity for every d>2; within this integer family the radial force is inverse-square only for d=3. If a separate test-charge dictionary declares U=q*phi and F=q*E, then like source and test charges repel and opposite signs attract. This theorem imports the action, kappa, current, dimension, point source, boundary data, and force dictionary. It derives no kinetic coefficient, charged matter, electric ontology, preferred dimension, photon, physical electromagnetic or material sector, gravity coupling, observed force, or substrate mechanism.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-GAU-001, C-KRN-001. Assumptions: The connection, flat coordinates, explicit metric diagonal, positive kinetic coefficient, source-coupling sign, current, and compactly supported variation class are declared rather than derived by local covariance., The current is smooth and conserved on the field-equation domain. C-U1-001 supplies one conditional current theorem but no physical electric identification or universal source for this action., The static branch additionally declares A_0=phi, vanishing spatial potential, time independence, point-source distribution and normalization, integer spatial dimension, regularity away from the source, and the displayed boundary or reference data., C-KRN-001 supplies the d>2 Riesz normalization. The d=2 logarithmic and d=1 linear branches require their stated reference data and admit separately governed homogeneous additions under other boundaries., The radial coordinate describes the positive branch; signs of real Q and q determine field and force orientation. U=q*phi and F=q*E are separately declared test-charge relations., Decay of the potential selects only d>2, not d=3. Inverse-square force selects d=3 only after the ordinary two-derivative kernel, integer dimension family, source normalization, and test-charge dictionary are already supplied., No accepted claim derives the kinetic coefficient, source ontology, dimension, physical unit convention, medium identifications, CODATA values, radiation, or observational map.. Comparators: EM3 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; its imported-action variation Bianchi identity source-normalized Coulomb endpoint and conditional force survive, while its A_0 sign unique-decay numeric-independence neutral-source pure-gauge-EOM medium-map physical-sector and no-data readings are corrected qualified or rejected.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.102.0` with provenance `campaigns/P134-em3-maxwell-coulomb-audit/adjudication.yaml`.

- `campaigns/P134-em3-maxwell-coulomb-audit/verify.py`
- `campaigns/P134-em3-maxwell-coulomb-audit/reviews/independent_maxwell_review.py`
- `campaigns/P134-em3-maxwell-coulomb-audit/reviews/replay_source_graph.py`
- `campaigns/P134-em3-maxwell-coulomb-audit/attempts/0002/result.yaml`
- `campaigns/P134-em3-maxwell-coulomb-audit/attempts/0003/result.yaml`
- `campaigns/P134-em3-maxwell-coulomb-audit/attempts/0004/result.yaml`
- `campaigns/P134-em3-maxwell-coulomb-audit/attempts/0005/result.yaml`
- `campaigns/P134-em3-maxwell-coulomb-audit/attempts/0006/result.yaml`
- `campaigns/P134-em3-maxwell-coulomb-audit/attempts/0007/result.yaml`
- `campaigns/P134-em3-maxwell-coulomb-audit/attempts/0008/result.yaml`
- `campaigns/P134-em3-maxwell-coulomb-audit/attempts/0009/result.yaml`
- `campaigns/P134-em3-maxwell-coulomb-audit/attempts/0010/result.yaml`
- `campaigns/P134-em3-maxwell-coulomb-audit/evidence/source-reproduction.yaml`
- `campaigns/P134-em3-maxwell-coulomb-audit/evidence/source-audit.yaml`
- `campaigns/P134-em3-maxwell-coulomb-audit/evidence/check-adjudication.yaml`
- `campaigns/P134-em3-maxwell-coulomb-audit/evidence/input-provenance.yaml`
- `campaigns/P134-em3-maxwell-coulomb-audit/evidence/dependency-audit.yaml`
- `campaigns/P134-em3-maxwell-coulomb-audit/evidence/consumer-audit.yaml`
- `campaigns/P134-em3-maxwell-coulomb-audit/evidence/nonduplication-audit.yaml`
- `campaigns/P134-em3-maxwell-coulomb-audit/evidence/candidate-comparison.yaml`
- `campaigns/P134-em3-maxwell-coulomb-audit/evidence/primary-provenance.yaml`
- `campaigns/P134-em3-maxwell-coulomb-audit/reviews/source_adjudication.md`
- `campaigns/P134-em3-maxwell-coulomb-audit/reviews/impact_analysis.md`
- `memory/vantasner/decisions/C-MAX-001-review.md`
- `memory/vantasner/decisions/EM3-qualified-review.md`
- `src/substrate_framework/maxwell.py`
- `src/substrate_framework/source_audit.py`
- `tests/test_maxwell.py`
- `tests/test_source_audit.py`
