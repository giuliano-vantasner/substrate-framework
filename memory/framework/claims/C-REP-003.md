---
description: Accepted framework claim C-REP-003
author: framework-registry
created: '2026-08-10T20:15:00Z'
updated: '2026-08-10T20:15:00Z'
tags:
- substrate-framework
- accepted-claim
- C-REP-003
category: claims
confidence: established
status: active
---
# C-REP-003

## Statement
The accepted statement is reproduced exactly from the claim registry.

For a separately supplied nonempty finite table of uniquely named rows, let row a have positive integer spectator multiplicity m_a, a nonempty finite sequence of exact real isospin weights t_aj, and one exact real Abelian coordinate y_a. For an exact real electric coefficient c, define q_aj=t_aj+c*y_a. The grouped spectra and state count N=sum_a m_a*n_a are exact, and flattening each component with multiplicity m_a gives precisely the C-REP-001 finite charge-trace ledger. Given separately supplied exact target charges qhat_aj of the same length and an exact provably nonzero c, one component fixes the unique candidate y_a=(qhat_a1-t_a1)/c; the row is consistent exactly when every reconstruction residual t_aj+c*y_a-qhat_aj vanishes. This uniqueness is conditional on the supplied weights, coefficient, and targets and does not select any of them. For the C-REP-002 Pauli-half doublet weights, every consistent common-coordinate spectrum has separation one. Charge conjugation maps every t_aj and y_a to its negative, retains m_a, and negates every q_aj; retaining a spectator dimension does not distinguish a representation from its conjugate. For separately supplied positive rho and positive Abelian coupling g, the simultaneous map y_a'=rho*y_a, c'=c/rho, and g'=g/rho preserves every grouped charge, every product g*y_a, the state count, and the C-REP-001 covariant trace data, while holding c fixed generally changes the spectra. These are exact supplied-data identities. They do not derive row labels, factor representations, chirality, target charges, the finite table, anomaly cancellation, Yukawa operators, generation completeness, conservation, a compact U1 period or charge lattice, a global gauge group, physical matter, an action, currents, dynamics, observation, a Standard Model identification, or a substrate mechanism.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-REP-001, C-REP-002. Assumptions: The finite table is supplied rather than derived; labels are unique provenance keys, spectator multiplicities are positive integers, each weight row is nonempty, and all generator coordinates and the electric coefficient are exact real expressions., Target inversion applies only to supplied target rows of matching nonzero length and an electric coefficient that is provably nonzero., A spectator multiplicity counts equal copies but does not name the spectator representation or distinguish conjugate representations of equal dimension., Charge conjugation negates all generator weights in the declared coordinate convention; physical right-handed fields and left-handed conjugate fields remain separately typed interpretations., Generator rescaling and inverse electric-coefficient and coupling transformations are declared coordinate changes with rho positive., The Pauli-half specialization uses C-REP-002 only for its fixed weights and scalar commuting Abelian boundary; it supplies no physical doublet identity., No anomaly equation, target selection, field completeness, Yukawa interaction, conservation law, global U1 data, matter action, observation, or substrate dictionary is imported.. Comparators: SM2 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; native execution passes all seven predicates without a NumPy compatibility event, while both hypercharges and target charges are supplied, factor dimensions do not type conjugates, the fifteen-state count is not a completeness theorem, the Yukawa sentence and conservation reading are unchecked, and coupling rescaling, global U1 data, anomaly selection, physical matter, dynamics, observation, and a substrate mechanism are absent.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.126.0` with provenance `campaigns/P164-sm2-generation-hypercharge-audit/adjudication.yaml`.

- `campaigns/P164-sm2-generation-hypercharge-audit/verify.py`
- `campaigns/P164-sm2-generation-hypercharge-audit/reviews/independent_multiplet_charge_review.py`
- `campaigns/P164-sm2-generation-hypercharge-audit/reviews/replay_source_graph.py`
- `campaigns/P164-sm2-generation-hypercharge-audit/attempts/0006/result.yaml`
- `campaigns/P164-sm2-generation-hypercharge-audit/attempts/0007/result.yaml`
- `campaigns/P164-sm2-generation-hypercharge-audit/evidence/source-reproduction.yaml`
- `campaigns/P164-sm2-generation-hypercharge-audit/evidence/source-audit.yaml`
- `campaigns/P164-sm2-generation-hypercharge-audit/evidence/check-adjudication.yaml`
- `campaigns/P164-sm2-generation-hypercharge-audit/evidence/input-provenance.yaml`
- `campaigns/P164-sm2-generation-hypercharge-audit/evidence/dependency-audit.yaml`
- `campaigns/P164-sm2-generation-hypercharge-audit/evidence/consumer-audit.yaml`
- `campaigns/P164-sm2-generation-hypercharge-audit/evidence/source-graph-inventory.yaml`
- `campaigns/P164-sm2-generation-hypercharge-audit/evidence/nonduplication-audit.yaml`
- `campaigns/P164-sm2-generation-hypercharge-audit/evidence/candidate-comparison.yaml`
- `campaigns/P164-sm2-generation-hypercharge-audit/evidence/primary-provenance.yaml`
- `campaigns/P164-sm2-generation-hypercharge-audit/reviews/source_adjudication.md`
- `campaigns/P164-sm2-generation-hypercharge-audit/reviews/impact_analysis.md`
- `memory/vantasner/decisions/C-REP-003-review.md`
- `memory/vantasner/decisions/SM2-qualified-review.md`
- `src/substrate_framework/multiplet_charges.py`
- `tests/test_multiplet_charges.py`
