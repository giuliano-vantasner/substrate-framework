---
description: Accepted framework claim C-HOL-001
author: framework-registry
created: '2026-08-10T10:00:00Z'
updated: '2026-08-10T10:00:00Z'
tags:
- substrate-framework
- accepted-claim
- C-HOL-001
category: claims
confidence: established
status: active
---
# C-HOL-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let H be a nonzero finite-dimensional complex inner-product carrier and let B_1 through B_n be a nonempty chronological sequence of exact Hermitian integrated connection matrices. In the convention inherited from D=partial-i*g*W, define V(B_1,...,B_n)=exp(i*B_n)*...*exp(i*B_1), with later segments on the left. V is unitary and det(V)=exp(i*sum_j trace(B_j)); concatenation is ordered multiplication. The reversed path has chronological segments -B_n through -B_1 and transporter V_reverse=V_dagger=V_inverse. Pairwise commuting B_j collapse to exp(i*sum_j B_j). If supplied exact unitary node gauges U_0 through U_n transform segment transporters as E_j'=U_j*E_j*U_(j-1)_dagger, their product transforms as V'=U_n*V*U_0_dagger. For a declared closed path with U_n=U_0, V changes by conjugation, so its characteristic polynomial, spectrum, determinant, raw trace, and dimension-normalized trace are invariant; V itself is not a scalar invariant. A cyclic basepoint move conjugates the ordered product. In the Pauli-half fundamental carrier, exp(2*pi*i*T3)=-I_2 and exp(4*pi*i*T3)=I_2. For chronological segments a*T1 then a*T2, the ordered product minus exp(i*a*(T1+T2)) is not the zero matrix function and has leading term i*a^2*T3/2, while commuting axes collapse. The same 2*pi SU2 center element acts as -I_2 in the fundamental and +I_3 in the adjoint, with raw traces -2 and +3 and normalized traces -1 and +1. These are exact conditional finite-matrix transport identities. They supply no base-space defect, flux, curvature localization, gauge action, weak matter carrier, physical W sector, Aharonov-Bohm observation, detector response, or substrate map.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-NAG-001, C-REP-002. Assumptions: The carrier is finite-dimensional and nonzero with its standard positive inner product, and all matrix and scalar inputs are exact; floating inputs are outside the exact API., The chronological integrated connections are same-size Hermitian matrices and already include the oriented path integral and coupling; no path geometry is inferred from the matrices alone., The transport sign is paired specifically with D=partial-i*g*W, and the sequence convention places later chronological segments on the left., Endpoint covariance requires same-size exact unitary node gauges. Closed-loop conjugacy additionally requires a separately declared closed path and equal endpoint gauge matrices., The spectrum statement is finite-dimensional characteristic-polynomial data, and every raw or normalized trace remains typed by its declared carrier representation., The SU2 examples use the exact Pauli-half fundamental generators and the exact spin-one adjoint T3 generator; their equal group source does not make their matrices or raw traces equal., No base-space loop, excluded region, localized curvature or flux, gauge action, matter field, weak coupling dictionary, detector, interference observable, or substrate realization is imported.. Comparators: NA1 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; native execution passes all five predicates without a NumPy compatibility event, while its constant T3 example is commuting, its su2_z orientation is hidden at center values, its noncommuting result lacks endpoint and representation structure, and its set equality does not establish a common object or physical weak Aharonov-Bohm sector.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.122.0` with provenance `campaigns/P156-na1-nonabelian-holonomy-audit/adjudication.yaml`.

- `campaigns/P156-na1-nonabelian-holonomy-audit/verify.py`
- `campaigns/P156-na1-nonabelian-holonomy-audit/reviews/independent_holonomy_review.py`
- `campaigns/P156-na1-nonabelian-holonomy-audit/reviews/replay_source_graph.py`
- `campaigns/P156-na1-nonabelian-holonomy-audit/attempts/0012/result.yaml`
- `campaigns/P156-na1-nonabelian-holonomy-audit/attempts/0013/result.yaml`
- `campaigns/P156-na1-nonabelian-holonomy-audit/attempts/0014/result.yaml`
- `campaigns/P156-na1-nonabelian-holonomy-audit/attempts/0016/result.yaml`
- `campaigns/P156-na1-nonabelian-holonomy-audit/evidence/source-reproduction.yaml`
- `campaigns/P156-na1-nonabelian-holonomy-audit/evidence/source-audit.yaml`
- `campaigns/P156-na1-nonabelian-holonomy-audit/evidence/check-adjudication.yaml`
- `campaigns/P156-na1-nonabelian-holonomy-audit/evidence/input-provenance.yaml`
- `campaigns/P156-na1-nonabelian-holonomy-audit/evidence/dependency-audit.yaml`
- `campaigns/P156-na1-nonabelian-holonomy-audit/evidence/consumer-audit.yaml`
- `campaigns/P156-na1-nonabelian-holonomy-audit/evidence/nonduplication-audit.yaml`
- `campaigns/P156-na1-nonabelian-holonomy-audit/evidence/candidate-comparison.yaml`
- `campaigns/P156-na1-nonabelian-holonomy-audit/evidence/primary-provenance.yaml`
- `campaigns/P156-na1-nonabelian-holonomy-audit/evidence/literature-audit.yaml`
- `campaigns/P156-na1-nonabelian-holonomy-audit/reviews/source_adjudication.md`
- `campaigns/P156-na1-nonabelian-holonomy-audit/reviews/impact_analysis.md`
- `memory/vantasner/decisions/C-HOL-001-review.md`
- `memory/vantasner/decisions/NA1-qualified-review.md`
- `src/substrate_framework/nonabelian_holonomy.py`
- `tests/test_nonabelian_holonomy.py`
