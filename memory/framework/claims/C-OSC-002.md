---
description: Accepted framework claim C-OSC-002
author: framework-registry
created: '2026-08-11T20:00:00Z'
updated: '2026-08-11T20:00:00Z'
tags:
- substrate-framework
- accepted-claim
- C-OSC-002
category: claims
confidence: established
status: active
---
# C-OSC-002

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let x be real, V(x)=1-cos(x), Q(x)=x^2/2, and E(x)=Q(x)-V(x). Then 0<=E(x)<=x^4/24 for every real x. For x!=0 the error relative to the quadratic approximation obeys 0<=E(x)/Q(x)<=x^2/12, so for every declared epsilon>0 the symmetric domain |x|<=sqrt(12*epsilon) is sufficient to guarantee E(x)/Q(x)<=epsilon. At the cosine barrier x=pi this relative error is exactly 1-4/pi^2>0.59, so the barrier is not a universal small-oscillation accuracy boundary. Separately, let P and delta be real, let omega be real and nonzero, and define phi(t)=P*cos(omega*t+delta). Its mean square over any full period T=2*pi/|omega| is P^2/2 and its RMS amplitude is |P|/sqrt(2). Hence if A_RMS>=0 denotes RMS amplitude then the mean square is A_RMS^2 and the harmonic peak is sqrt(2)*A_RMS, whereas if A_peak>=0 denotes peak amplitude then the mean square is A_peak^2/2. These conventions are distinct from C-OSC-001's separately declared one-mode Fock-coordinate intensity S=q_0^2 unless an explicit map is supplied. These exact approximation and cycle-average identities derive no material amplitude, quantum state, multimode composition, density of states, topological winding, transition probability, rate, reaction, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-SG-019, C-OSC-001. Assumptions: The phase coordinate x is real and uses C-SG-019's normalized exact cosine potential; the inequalities compare that exact potential with Q=x^2/2 and do not truncate the cosine itself., The relative error is measured against Q and is stated for x!=0. Its continuous origin limit is zero, and sqrt(12*epsilon) is a sufficient domain rather than a claimed maximal domain., The tolerance epsilon is a separately declared exact positive accuracy requirement. It is not fitted to WN6, PN2, a material, or an empirical comparator., The harmonic mean square averages over one complete period with real nonzero omega. A partial cycle, stochastic process, anharmonic motion, multimode field, or alternate measure is a different problem., Peak amplitude, RMS amplitude, variance about a nonzero mean, and C-OSC-001's Fock coordinate q_0 are distinct conventions unless a caller supplies and justifies a map., A pointwise barrier or basin condition does not by itself specify an approximation tolerance. Calling a coordinate excursion a winding additionally requires spatial boundary or topological data absent here., WN6's PN2 band, multi-mode sum, material mode count, spectral density, channel, and rate narratives supply no premise to this claim. WN7 and MD1 through MD6 remain separately governed.. Comparators: WN6 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; its S=A^2, RMS, PN2-band, single-vacuum, winding, and multi-mode conclusions were exposed by the generated queue and prior consumer audits before P194 froze conventions, exact error criteria, mutations, and physical ceilings, C-SG-019 supplies the entire cosine coefficient theorem and explicitly leaves finite-approximation remainder control open, C-OSC-001 supplies the distinct one-mode Fock-coordinate intensity S=q_0^2 but no classical peak or RMS phase map.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.144.0` with provenance `campaigns/P194-wn6-scale-verdict-audit/adjudication.yaml`.

- `campaigns/P194-wn6-scale-verdict-audit/verify.py`
- `campaigns/P194-wn6-scale-verdict-audit/reviews/independent_phase_scale_review.py`
- `campaigns/P194-wn6-scale-verdict-audit/reviews/replay_source_graph.py`
- `campaigns/P194-wn6-scale-verdict-audit/reviews/C-OSC-002-claim-review.md`
- `campaigns/P194-wn6-scale-verdict-audit/reviews/WN6-disposition-review.md`
- `campaigns/P194-wn6-scale-verdict-audit/reviews/source_adjudication.md`
- `campaigns/P194-wn6-scale-verdict-audit/reviews/impact_analysis.md`
- `campaigns/P194-wn6-scale-verdict-audit/attempts/0002/result.yaml`
- `campaigns/P194-wn6-scale-verdict-audit/attempts/0003/result.yaml`
- `campaigns/P194-wn6-scale-verdict-audit/attempts/0004/result.yaml`
- `campaigns/P194-wn6-scale-verdict-audit/attempts/0005/result.yaml`
- `campaigns/P194-wn6-scale-verdict-audit/attempts/0006/result.yaml`
- `campaigns/P194-wn6-scale-verdict-audit/evidence/formula-freeze.yaml`
- `campaigns/P194-wn6-scale-verdict-audit/evidence/input-provenance.yaml`
- `campaigns/P194-wn6-scale-verdict-audit/evidence/dependency-audit.yaml`
- `campaigns/P194-wn6-scale-verdict-audit/evidence/consumer-audit.yaml`
- `campaigns/P194-wn6-scale-verdict-audit/evidence/source-graph-inventory.yaml`
- `campaigns/P194-wn6-scale-verdict-audit/evidence/nonduplication-audit.yaml`
- `campaigns/P194-wn6-scale-verdict-audit/evidence/candidate-comparison.yaml`
- `campaigns/P194-wn6-scale-verdict-audit/evidence/implementation-audit.yaml`
- `campaigns/P194-wn6-scale-verdict-audit/evidence/gitnexus-impact.yaml`
- `campaigns/P194-wn6-scale-verdict-audit/evidence/primary-provenance.yaml`
- `campaigns/P194-wn6-scale-verdict-audit/evidence/independent-provenance.yaml`
- `memory/vantasner/decisions/C-OSC-002-review.md`
- `memory/vantasner/decisions/WN6-qualified-review.md`
- `src/substrate_framework/cosine_vertices.py`
- `tests/test_cosine_vertices.py`
