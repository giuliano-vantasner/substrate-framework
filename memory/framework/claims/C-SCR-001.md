---
description: Accepted framework claim C-SCR-001
author: framework-registry
created: '2026-08-08T02:30:00Z'
updated: '2026-08-08T02:30:00Z'
tags:
- substrate-framework
- accepted-claim
- C-SCR-001
category: claims
confidence: established
status: active
---
# C-SCR-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let E and G be positive real energies and U a nonnegative real energy in the same unit. Define the dimensionless bare inverse-square-root barrier factor B(E,G)=exp(-sqrt(G/E)), the shifted factor P(E,U,G)=exp(-sqrt(G/(E+U))), and the enhancement F=P/B. Then exactly F=exp(sqrt(G/E)-sqrt(G/(E+U))), with 0<B<=P<1 and equality B=P iff U=0. The logarithmic derivatives of P are partial_E log(P)=partial_U log(P)=sqrt(G)/(2*(E+U)^(3/2))>0 and partial_G log(P)=-1/(2*sqrt(G)*sqrt(E+U))<0. For U>0, F>1 and decreases strictly with E. As E tends to zero from above, B tends to zero, P tends to the finite positive value exp(-sqrt(G/U)), and F tends to infinity; for U=0, P=B and both tend to zero. As E tends to infinity, P and F tend to one. Common positive rescaling (E,U,G)->rho*(E,U,G) leaves all three factors invariant. Consequently, if an independent premise establishes 0<=U<=U_max, then P(E,U,G)<=P(E,U_max,G); the theorem neither derives U_max nor establishes a material screening model. Direct evaluation of P avoids the separate numerical zero-times-infinity form B*F at very small E. These are exact conditional dimensionless identities. They do not derive a Coulomb or Gamow approximation, physical screening energy, universal material ceiling, cross section, astrophysical S factor, collision flux, attempt frequency, density, branching, transition rate, reaction yield, heat, coherent channel, material realization, or observation.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: none. Assumptions: E and G are positive real quantities, U is nonnegative real, and all three use one common energy dimension and unit before any ratio or sum is formed., The displayed inverse-square-root exponential is a declared conditional factor. The theorem does not derive it from a potential, scattering equation, WKB regime, or nuclear model., Strict B<P, F>1, the finite positive low-energy shifted floor, divergent low-energy enhancement, and decreasing-in-E enhancement require U>0. At U=0 the shifted and bare factors agree., The U_max inequality requires a separately justified bound in the same convention. A selected maximum over finitely many assigned material models is not such a universal premise., The factors are dimensionless. A physical cross section, rate, or yield requires separately accepted dimensionful prefactors, states, dynamics, normalization, and parameter provenance., Direct composed evaluation is a numerical representation rule for the exact identity, not evidence for a physical model or magnitude.. Comparators: CM1 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; its exact factor identity and limits survive, while its one-point shape proof, selected four-model ceiling, low-input-null wording, physical rate, maximum-yield, material, channel, and observation readings are qualified or rejected.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.95.0` with provenance `campaigns/P115-cm1-screened-barrier-ceiling-audit/adjudication.yaml`.

- `campaigns/P115-cm1-screened-barrier-ceiling-audit/verify.py`
- `campaigns/P115-cm1-screened-barrier-ceiling-audit/reviews/independent_screened_barrier_review.py`
- `campaigns/P115-cm1-screened-barrier-ceiling-audit/attempts/0001/result.yaml`
- `campaigns/P115-cm1-screened-barrier-ceiling-audit/attempts/0002/result.yaml`
- `campaigns/P115-cm1-screened-barrier-ceiling-audit/attempts/0003/result.yaml`
- `campaigns/P115-cm1-screened-barrier-ceiling-audit/attempts/0004/result.yaml`
- `campaigns/P115-cm1-screened-barrier-ceiling-audit/attempts/0006/result.yaml`
- `campaigns/P115-cm1-screened-barrier-ceiling-audit/evidence/source-reproduction.yaml`
- `campaigns/P115-cm1-screened-barrier-ceiling-audit/evidence/source-audit.yaml`
- `campaigns/P115-cm1-screened-barrier-ceiling-audit/evidence/check-adjudication.yaml`
- `campaigns/P115-cm1-screened-barrier-ceiling-audit/evidence/input-provenance.yaml`
- `campaigns/P115-cm1-screened-barrier-ceiling-audit/evidence/dependency-audit.yaml`
- `campaigns/P115-cm1-screened-barrier-ceiling-audit/evidence/consumer-audit.yaml`
- `campaigns/P115-cm1-screened-barrier-ceiling-audit/evidence/candidate-comparison.yaml`
- `campaigns/P115-cm1-screened-barrier-ceiling-audit/evidence/primary-provenance.yaml`
- `campaigns/P115-cm1-screened-barrier-ceiling-audit/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-SCR-001-review.md`
- `src/substrate_framework/screened_barrier.py`
- `tests/test_screened_barrier.py`
