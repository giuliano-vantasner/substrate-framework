---
description: Accepted framework claim C-PRC-001
author: framework-registry
created: '2026-08-10T08:20:00Z'
updated: '2026-08-10T08:20:00Z'
tags:
- substrate-framework
- accepted-claim
- C-PRC-001
category: claims
confidence: established
status: active
---
# C-PRC-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let A^mu be a real twice-differentiable vector field on 3+1 Minkowski space with eta=diag(-1,+1,+1,+1), define F_mu_nu=partial_mu*A_nu-partial_nu*A_mu, and separately declare the source-free density L=-F_mu_nu*F^mu_nu/4-m^2*A_mu*A^mu/2 with exact m>0 and boundary behavior licensing integration by parts. Exact variation gives partial_mu*F^(mu nu)-m^2*A^nu=0. Commuting derivatives and antisymmetry then derive partial_nu*A^nu=0 as a massive constraint rather than a gauge choice, and hence (box-m^2)*A^nu=0 for box=-partial_t^2+nabla^2. A plane wave proportional to exp(-i*omega*t+i*k dot x) has omega^2=|k|^2+m^2. For a static tangential component A_y(x) on x>=0 with A_y(0)=A0 and A_y tending to zero as x tends to infinity, the unique solution is A0*exp(-m*x); the general ODE also has a growing branch, and a longitudinal A_x(x) generally violates the derived divergence constraint. The inverse length is m and the penetration length is 1/m. More generally, a separately declared positive one-mode kinetic coefficient kappa and positive quadratic coefficient q give m^2=q/kappa. Conditional on C-GSM-001's lower-doublet coefficient q=g^2*v^2/4, exact positive g and v, and an independently declared canonical free kinetic action, m=g*v/2 and the length is 2/(g*v). At m=0 the divergence constraint is not derived and no finite positive penetration length follows. These are exact conditional action and boundary-value identities. They supply no London current, Maxwell-material response, Meissner magnetic observation, stationary condensate, physical W boson, Standard Model selection, or substrate mass mechanism.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-GSM-001. Assumptions: The vector field is real and twice differentiable on flat 3+1 Minkowski space, coordinate derivatives commute, and variations or boundary data license every integration by parts., The metric, field-strength definition, mostly-plus action signs, source-free condition, and exact positive mass are declared together; formulas from another signature require a reviewed convention map., The divergence condition is derived only for nonzero mass. The massless theory has gauge redundancy and cannot inherit this algebraic constraint or a finite penetration length silently., The half-line theorem concerns a static tangential component A_y depending on x, a supplied real boundary amplitude, and decay at positive infinity. A longitudinal profile answers a different constrained vector problem., The q over kappa statement requires exact positive coefficients in the same one-mode field coordinate and a complete free quadratic action; a quadratic mass form alone is insufficient., The g*v/2 specialization additionally imports only C-GSM-001's conditional lower-doublet coefficient and independently declares canonical kinetic normalization; it does not turn the mode into a physical W., No London constitutive relation, material current, Maxwell medium, stationary condensate, observed screening field, weak sector, Standard Model, or substrate dictionary is imported.. Comparators: M2 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; native execution passes all seven predicates without a NumPy compatibility event, while the source varies a scalar proxy, calls the massive constraint gauge fixing, uses an OR branch guard, assumes its on-shell relation, and does not derive its London Meissner W or substrate identification.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.121.0` with provenance `campaigns/P155-m2-meissner-proca-audit/adjudication.yaml`.

- `campaigns/P155-m2-meissner-proca-audit/verify.py`
- `campaigns/P155-m2-meissner-proca-audit/reviews/independent_proca_review.py`
- `campaigns/P155-m2-meissner-proca-audit/reviews/replay_source_graph.py`
- `campaigns/P155-m2-meissner-proca-audit/attempts/0004/result.yaml`
- `campaigns/P155-m2-meissner-proca-audit/attempts/0008/result.yaml`
- `campaigns/P155-m2-meissner-proca-audit/attempts/0010/result.yaml`
- `campaigns/P155-m2-meissner-proca-audit/attempts/0012/result.yaml`
- `campaigns/P155-m2-meissner-proca-audit/evidence/source-reproduction.yaml`
- `campaigns/P155-m2-meissner-proca-audit/evidence/source-audit.yaml`
- `campaigns/P155-m2-meissner-proca-audit/evidence/check-adjudication.yaml`
- `campaigns/P155-m2-meissner-proca-audit/evidence/input-provenance.yaml`
- `campaigns/P155-m2-meissner-proca-audit/evidence/dependency-audit.yaml`
- `campaigns/P155-m2-meissner-proca-audit/evidence/consumer-audit.yaml`
- `campaigns/P155-m2-meissner-proca-audit/evidence/nonduplication-audit.yaml`
- `campaigns/P155-m2-meissner-proca-audit/evidence/candidate-comparison.yaml`
- `campaigns/P155-m2-meissner-proca-audit/evidence/primary-provenance.yaml`
- `campaigns/P155-m2-meissner-proca-audit/evidence/literature-audit.yaml`
- `campaigns/P155-m2-meissner-proca-audit/reviews/source_adjudication.md`
- `campaigns/P155-m2-meissner-proca-audit/reviews/impact_analysis.md`
- `memory/vantasner/decisions/C-PRC-001-review.md`
- `memory/vantasner/decisions/M2-qualified-review.md`
- `src/substrate_framework/proca.py`
- `tests/test_proca.py`
