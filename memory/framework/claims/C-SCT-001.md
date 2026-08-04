---
description: Accepted framework claim C-SCT-001
author: framework-registry
created: '2026-08-10T02:48:00Z'
updated: '2026-08-10T02:48:00Z'
tags:
- substrate-framework
- accepted-claim
- C-SCT-001
category: claims
confidence: established
status: active
---
# C-SCT-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let c and zeta be exact positive speeds and z=zeta/c. On the right half-line x>=0, let a real massless scalar obey phi_tt-c^2*phi_xx=0, with incoming harmonic proportional to exp(-i*omega*(t+x/c)), reflected harmonic proportional to exp(-i*omega*(t-x/c)), and passive boundary condition phi_t-zeta*phi_x=0. Exact substitution gives amplitude reflection r=(z-1)/(z+1), reflected power R=r^2, and, for a steady harmonic ledger with no other boundary storage or flux channel, absorbed fraction T=1-R=4*z/(z+1)^2. The half-line bulk energy rate contributed by the boundary is -c^2*zeta*phi_x(0,t)^2<=0. Under z->1/z, r changes sign while R and T are invariant, so power data alone do not identify which reciprocal impedance applies. If a separate reference channel is declared perfectly reflected, C-BRN-001 gives contrast A=(1-R)/(1+R)=2*z/(z^2+1)=T/(2-T); A is a deterministic transform, not an independent prediction, and is also reciprocal-invariant. This theorem derives no boundary law from a piston action, lambda or mu coefficient, physical chirality, parity violation, current, charge, detector, weak interaction, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-BRN-001. Assumptions: Inputs are exact and explicitly positive; floating and unsigned symbolic values are outside the exact API., Coordinates use the right half-line x>=0, signature (+,-), and the stated incoming and reflected phase convention., The bulk energy is the canonical scalar energy and the passive sign is phi_t-zeta*phi_x=0., Calling 1-R absorbed assumes steady harmonic balance with no other boundary storage, work, radiation, or flux channel., The reference contrast additionally assumes a separately declared channel with unit reflected power and imports only C-BRN-001 normalization., Boundary action, material realization, physical states, parity action, current, charge, interaction, and detector data are not inferred.. Comparators: W5 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; native execution passes all twenty-seven predicates without a NumPy compatibility event, while its reversed wave roles and active sign cancel in amplitude algebra and its piston derivation, independent-observable, physical chirality, parity-violation, weak, detector, and substrate readings are corrected qualified or rejected.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.116.0` with provenance `campaigns/P150-w5-chiral-asymmetry-audit/adjudication.yaml`.

- `campaigns/P150-w5-chiral-asymmetry-audit/verify.py`
- `campaigns/P150-w5-chiral-asymmetry-audit/reviews/independent_scattering_review.py`
- `campaigns/P150-w5-chiral-asymmetry-audit/reviews/replay_source_graph.py`
- `campaigns/P150-w5-chiral-asymmetry-audit/attempts/0008/result.yaml`
- `campaigns/P150-w5-chiral-asymmetry-audit/attempts/0009/result.yaml`
- `campaigns/P150-w5-chiral-asymmetry-audit/evidence/source-reproduction.yaml`
- `campaigns/P150-w5-chiral-asymmetry-audit/evidence/source-audit.yaml`
- `campaigns/P150-w5-chiral-asymmetry-audit/evidence/check-adjudication.yaml`
- `campaigns/P150-w5-chiral-asymmetry-audit/evidence/input-provenance.yaml`
- `campaigns/P150-w5-chiral-asymmetry-audit/evidence/dependency-audit.yaml`
- `campaigns/P150-w5-chiral-asymmetry-audit/evidence/consumer-audit.yaml`
- `campaigns/P150-w5-chiral-asymmetry-audit/evidence/nonduplication-audit.yaml`
- `campaigns/P150-w5-chiral-asymmetry-audit/evidence/candidate-comparison.yaml`
- `campaigns/P150-w5-chiral-asymmetry-audit/evidence/primary-provenance.yaml`
- `campaigns/P150-w5-chiral-asymmetry-audit/evidence/literature-audit.yaml`
- `campaigns/P150-w5-chiral-asymmetry-audit/reviews/source_adjudication.md`
- `campaigns/P150-w5-chiral-asymmetry-audit/reviews/impact_analysis.md`
- `memory/vantasner/decisions/C-SCT-001-review.md`
- `memory/vantasner/decisions/W5-qualified-review.md`
- `src/substrate_framework/boundary_scattering.py`
- `tests/test_boundary_scattering.py`
