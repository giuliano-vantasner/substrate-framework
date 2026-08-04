---
description: Accepted framework claim C-RAD-001
author: framework-registry
created: '2026-08-09T14:10:00Z'
updated: '2026-08-09T14:10:00Z'
tags:
- substrate-framework
- accepted-claim
- C-RAD-001
category: claims
confidence: established
status: active
---
# C-RAD-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let A and c be exact positive real quantities, B an exact real source coupling, and q(t) an exact real point-source amplitude, and separately declare the one-dimensional scalar Lagrangian density A*(phi_t^2-c^2*phi_x^2)/2+B*phi*q(t)*delta(x). Its Euler equation is phi_tt-c^2*phi_xx=(B/A)*q(t)*delta(x). Under no-incoming retarded boundary data and a source primitive I with I'=q and vanishing past boundary term, the distributional solution is phi(t,x)=B*I(t-|x|/c)/(2*A*c). Its one-sided derivatives obey the outgoing characteristic relations, and their jump is -B*q/(A*c^2), exactly reproducing the delta source. From the same action, the canonical energy density is A*(phi_t^2+c^2*phi_x^2)/2 and the right-directed flux is -A*c^2*phi_t*phi_x. Each outgoing side carries B^2*q^2/(4*A*c), total outward power is B^2*q^2/(2*A*c), and that total equals the local source-work rate B*q*phi_t(t,0). The field rescaling phi'=s*phi, A'=A/s^2, B'=B/s preserves B^2/A and the power. For constant q, the static field -B*q*abs(x)/(2*A*c^2) obeys the same local equation and jump but has zero flux, so the retarded radiation conclusion requires the stated boundary and history data and does not follow from the sourced equation alone. This is an exact conditional scalar-action theorem. It does not derive a dilaton or gravitational action, propagating graviton, optical metric, sine-Gordon or breather source, accelerated solution, multipole expansion, coupling value, radiation reaction, physical gravity, observation, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: none. Assumptions: A and c are exact positive real quantities, while B and the evaluated source amplitude q are exact real quantities; floating inputs are outside the exact API., The displayed scalar action, source sign, metric convention, point support, and canonical energy definition are declared inputs, not consequences of a dilaton or optical theory., The retarded branch assumes no incoming field and a source primitive whose past boundary term vanishes. Other initial or boundary data can add homogeneous fields and change the flux., The point-source field is distributional at x=0. The derivative jump, one-sided fluxes, and local work are the governed observables; no finite self-energy or self-force is claimed., The static absolute-value solution has nonzero asymptotic slope and infinite full-line energy for nonzero q. It is a same-equation boundary/history countermodel, not an alternative finite-past radiative solution., A source history and source dynamics are distinct. The theorem does not determine q(t), energy loss, backreaction, or a radiation-reaction equation., No accepted claim identifies phi with a dilaton, metric perturbation, gravitational wave, sine-Gordon breather, medium excitation, or substrate field.. Comparators: G1 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; alias-only replay backed by np.trapezoid passes all ten checks, while its extra source derivative, factor-four flux error, gamma trace boost, same-RHS numeric oracle, target-selected coupling, accelerated-breather, dilaton-gravity, multipole, reaction, and substrate readings are corrected qualified or rejected.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.108.0` with provenance `campaigns/P141-g1-radiating-dilaton-audit/adjudication.yaml`.

- `campaigns/P141-g1-radiating-dilaton-audit/verify.py`
- `campaigns/P141-g1-radiating-dilaton-audit/reviews/independent_retarded_wave_review.py`
- `campaigns/P141-g1-radiating-dilaton-audit/reviews/replay_source_graph.py`
- `campaigns/P141-g1-radiating-dilaton-audit/attempts/0002/result.yaml`
- `campaigns/P141-g1-radiating-dilaton-audit/attempts/0003/result.yaml`
- `campaigns/P141-g1-radiating-dilaton-audit/attempts/0004/result.yaml`
- `campaigns/P141-g1-radiating-dilaton-audit/attempts/0005/result.yaml`
- `campaigns/P141-g1-radiating-dilaton-audit/attempts/0006/result.yaml`
- `campaigns/P141-g1-radiating-dilaton-audit/attempts/0007/result.yaml`
- `campaigns/P141-g1-radiating-dilaton-audit/attempts/0008/result.yaml`
- `campaigns/P141-g1-radiating-dilaton-audit/attempts/0009/result.yaml`
- `campaigns/P141-g1-radiating-dilaton-audit/attempts/0010/result.yaml`
- `campaigns/P141-g1-radiating-dilaton-audit/evidence/source-reproduction.yaml`
- `campaigns/P141-g1-radiating-dilaton-audit/evidence/source-audit.yaml`
- `campaigns/P141-g1-radiating-dilaton-audit/evidence/check-adjudication.yaml`
- `campaigns/P141-g1-radiating-dilaton-audit/evidence/input-provenance.yaml`
- `campaigns/P141-g1-radiating-dilaton-audit/evidence/dependency-audit.yaml`
- `campaigns/P141-g1-radiating-dilaton-audit/evidence/consumer-audit.yaml`
- `campaigns/P141-g1-radiating-dilaton-audit/evidence/nonduplication-audit.yaml`
- `campaigns/P141-g1-radiating-dilaton-audit/evidence/candidate-comparison.yaml`
- `campaigns/P141-g1-radiating-dilaton-audit/evidence/primary-provenance.yaml`
- `campaigns/P141-g1-radiating-dilaton-audit/evidence/literature-audit.yaml`
- `campaigns/P141-g1-radiating-dilaton-audit/reviews/source_adjudication.md`
- `campaigns/P141-g1-radiating-dilaton-audit/reviews/impact_analysis.md`
- `memory/vantasner/decisions/C-RAD-001-review.md`
- `memory/vantasner/decisions/G1-qualified-review.md`
- `src/substrate_framework/retarded_wave.py`
- `tests/test_retarded_wave.py`
