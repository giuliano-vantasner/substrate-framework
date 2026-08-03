---
description: Accepted framework claim C-FPT-001
author: framework-registry
created: '2026-08-06T12:00:00Z'
updated: '2026-08-06T12:00:00Z'
tags:
- substrate-framework
- accepted-claim
- C-FPT-001
category: claims
confidence: established
status: active
---
# C-FPT-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let a<b, x in [a,b], Theta>0, gamma>0, and let U be a declared real continuously differentiable potential on [a,b]. Conditional on the one-dimensional overdamped Ito diffusion dX=-(U'(X)/gamma)dt+sqrt(2*Theta/gamma)dW with reflection at a and absorption at b, the mean absorption time tau(x) is the unique solution of Theta*tau''-U'*tau'=-gamma on (a,b), tau'(a)=0, tau(b)=0, and is tau(x)=(gamma/Theta)*integral_x^b exp(U(y)/Theta) integral_a^y exp(-U(z)/Theta) dz dy. It is strictly positive for x<b, vanishes at b, and is invariant under an additive constant in U. For U(x)=F*(x-a), F>0, L=b-a, and a start at a, the exact result is gamma*Theta*(exp(F*L/Theta)-1-F*L/Theta)/F^2, with zero-force limit gamma*L^2/(2*Theta). A finite-horizon mean over completed paths is a conditional completed-only statistic rather than the full MFPT, and a rule returning zero below a completion threshold is an operational classifier rather than a zero physical rate. Inverse MFPT is not in general a constant hazard: free reflected diffusion started at a has squared first-passage coefficient of variation 2/3 rather than the exponential value 1. These exact conditional results derive no physical coordinate, potential, bath, friction, mobility, stochastic convention in physical units, absorbing event, material, population coupling, ignition process, attempt frequency, Kramers or Langer prefactor, or observed rate.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: none. Assumptions: The displayed reflected Ito diffusion is declared model data. U is real and continuously differentiable on the compact interval, Theta and gamma are finite and strictly positive, and the reflection and absorption conditions have the displayed meanings., The backward solution is interpreted classically where differentiable and with the standard reflecting-domain boundary condition. No discontinuous drift, state-dependent diffusion, sticky boundary, jump process, or alternative stochastic convention is inferred., The linear-potential formula assumes F>0 and a start at the reflecting endpoint; its zero-force result is the positive one-sided limit. Other initial points or boundary locations use the general integral., Completed-only, restricted, and full means require their separately stated censoring populations. A numerical estimator earns only resolution-bounded evidence and must expose horizon, timestep, boundary rule, ensemble, seed, uncertainty, and convergence., Calling inverse MFPT a physical rate or hazard requires a separately justified renewal or asymptotic model. The free reflected counterexample rules out that identification as a general theorem., Specializing U to a framework energy still requires an accepted coordinate map, friction or mobility, thermal bath and fluctuation-dissipation law, absorbing event, unit map, and observation model; dimensional consistency or a passing path tally does not supply them.. Comparators: BD5 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; its body and tally were already exposed, while P103 froze the backward equation, censoring distinctions, independent methods, mutations, and interpretation ceilings before renewed execution, The hash-pinned legacy sampled MFPT and rung091 routes; they corroborate conditional algebra but are noncanonical and do not close their physical prefactors or event narratives.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.87.0` with provenance `campaigns/P103-bd5-kramers-escape-audit/adjudication.yaml`.

- `campaigns/P103-bd5-kramers-escape-audit/verify.py`
- `campaigns/P103-bd5-kramers-escape-audit/reviews/independent_first_passage_review.py`
- `campaigns/P103-bd5-kramers-escape-audit/evidence/source-reproduction.yaml`
- `campaigns/P103-bd5-kramers-escape-audit/evidence/source-audit.yaml`
- `campaigns/P103-bd5-kramers-escape-audit/evidence/check-adjudication.yaml`
- `campaigns/P103-bd5-kramers-escape-audit/evidence/dependency-audit.yaml`
- `campaigns/P103-bd5-kramers-escape-audit/evidence/consumer-audit.yaml`
- `campaigns/P103-bd5-kramers-escape-audit/evidence/candidate-comparison.yaml`
- `campaigns/P103-bd5-kramers-escape-audit/evidence/primary-provenance.yaml`
- `campaigns/P103-bd5-kramers-escape-audit/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-FPT-001-review.md`
- `tests/test_first_passage.py`
