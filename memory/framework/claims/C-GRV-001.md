---
description: Accepted framework claim C-GRV-001
author: framework-registry
created: '2026-08-03T10:40:00Z'
updated: '2026-08-03T10:40:00Z'
tags:
- substrate-framework
- accepted-claim
- C-GRV-001
category: claims
confidence: established
status: active
---
# C-GRV-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

In M,L,T base-dimension order, for primitive columns consisting of a positive cutoff length a, speed c, and action scale hbar, the exact dimension matrix [[0,0,1],[1,1,2],[0,-1,-1]] has full rank. The unique monomial powers for Newton G are (2,3,-1), and those for 1/G are (-2,-3,1); hence dimensions permit G=q*a^2*c^3/hbar with an arbitrary dimensionless q but do not determine q or derive a cutoff mechanism. If a nonzero real coefficient s and cutoff energy E_cut=hbar*c/a are separately declared, the conditional leading inverse-coupling shift Delta(1/G)=s*hbar/(a^2*c^3)=s*E_cut^2/(hbar*c^5) is exact. Its sign, field and curvature-coupling content, regulator, cutoff identification, and coefficient remain premises. An independent baseline inverse coupling B adds before inversion, 1/G_total=B+Delta(1/G); dimensions do not set B=0, B=target-Delta realizes any supplied total, and B=-Delta cancels it. Only for B=0 and s>0 is the pure formula G=a^2*c^3/(s*hbar) available. With compatible dimensionless references, its log row on (log(a/a_ref),log(s/s_ref)) is (2,-1), whose nullspace spans (1,2); therefore one supplied G ratio identifies neither a nor s, and a=sqrt(s*hbar*G/c^3) is inverse inference after supplying G and s, not a prediction. For any separately declared source equation operator=kappa*source, [kappa]=[operator]-[source]. A direct kappa=alpha*G with dimensionless alpha is allowed only when this equals [G]; for a dimensionless scalar operator of dimension L^-2, mass-density and energy-density sources instead require alpha dimensions c^-2 and c^-4 respectively. C-OG-003 declares neither such source units nor a Newton normalization. AS3's exact power solve and cutoff substitution survive conditionally, but it leaves s free, omits the additive baseline and QFT data, imports kappa=8*pi*G from pending evidence, and does not pin a, kappa, or an over-determined physical scale. This ledger establishes no Sakharov mechanism, quantum spectrum, regulator, 3+1 Einstein dynamics, lattice ontology, medium map, observed constant, or absolute scale.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-DIM-001, C-IDN-001, C-OG-003. Assumptions: Base-dimension rows are M,L,T and primitive columns are exactly cutoff length, speed, and action scale; added primitives can change uniqueness., The cutoff energy, leading induced inverse-coupling form, nonzero real coefficient, and its QFT provenance are separately declared rather than dimensionally derived., Any baseline, logarithmic, finite, or renormalized inverse-coupling contribution is an independent same-dimension input and must not be silently set to zero., The log relation uses positive dimensionless ratios to declared compatible references; one row leaves the coefficient-cutoff null direction., Every source operator, source density, and conversion factor carries separately declared M,L,T dimensions before comparison with Newton G., No accepted claim supplies AS3's field spectrum, regulator, cutoff ontology, G5 normalization, over-determination rows, observed value, or physical lattice and medium dictionary.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.68.0` with provenance `campaigns/P074-as3-induced-gravity-scaling/adjudication.yaml`.

- `campaigns/P074-as3-induced-gravity-scaling/verify.py`
- `campaigns/P074-as3-induced-gravity-scaling/attempts/0001/result.yaml`
- `campaigns/P074-as3-induced-gravity-scaling/attempts/0002/result.yaml`
- `campaigns/P074-as3-induced-gravity-scaling/attempts/0003/result.yaml`
- `campaigns/P074-as3-induced-gravity-scaling/reviews/independent_induced_gravity_review.py`
- `campaigns/P074-as3-induced-gravity-scaling/evidence/source-reproduction.yaml`
- `campaigns/P074-as3-induced-gravity-scaling/evidence/source-audit.yaml`
- `campaigns/P074-as3-induced-gravity-scaling/evidence/literature-audit.yaml`
- `campaigns/P074-as3-induced-gravity-scaling/evidence/candidate-comparison.yaml`
- `campaigns/P074-as3-induced-gravity-scaling/evidence/primary-provenance.yaml`
- `campaigns/P074-as3-induced-gravity-scaling/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-GRV-001-review.md`
- `tests/test_induced_gravity.py`
