---
description: Accepted framework claim C-IRR-001
author: framework-registry
created: '2026-08-09T11:00:00Z'
updated: '2026-08-09T11:00:00Z'
tags:
- substrate-framework
- accepted-claim
- C-IRR-001
category: claims
confidence: established
status: active
---
# C-IRR-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

In the standard fundamental SU(3) convention of C-LIE-001 with Y=2*T_8/sqrt(3), let p and q be arbitrary nonnegative integer Dynkin labels and use the U(3) Gelfand-Tsetlin top row (p+q,q,0). The exact Weyl dimension is (p+1)(q+1)(p+q+2)/2, the quadratic Casimir is (p^2+p*q+q^2+3*p+3*q)/3, and the C-LIE-002 center triality is p+2*q modulo three. Every interlacing pattern p+q>=m12>=q>=m22>=0 and m12>=m11>=m22 gives one basis state with I=(m12-m22)/2, I3=m11-(m12+m22)/2, and Y=m12+m22-2*(p+2*q)/3; these patterns are complete, their count equals the Weyl dimension, and aggregation gives the exact weight multiplicities and multiplicity-free SU(2)xU(1) branching rows. Conditional on an exact rational target hypercharge and explicitly supplied finite nonnegative bounds max_p and max_q, enumerating all labels in the rectangular domain returns every irrep containing that hypercharge and preserves all minimum-dimension ties. At target Y=1 the unique global minimum is (1,1) of dimension eight with I=1/2; the next distinct dimension is ten and contains both (0,3) with I=1/2 and (3,0) with I=3/2. This is a mathematical representation and kinematic-filter theorem only. It does not supply a collective-coordinate action, right generator constraint, WZW level or response, N_c, baryon number, statistics, Hamiltonian, symmetry breaking, particle dictionary, mass spectrum, physical octet/decuplet selection, or substrate mechanism.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-LIE-001, C-LIE-002. Assumptions: The fundamental generators, trace normalization, isospin embedding, and hypercharge Y=2*T_8/sqrt(3) are exactly those of C-LIE-001., Dynkin labels p and q and finite search bounds max_p and max_q are nonnegative integers; floating or symbolic bounds are outside the API., The Gelfand-Tsetlin top row is (p+q,q,0), the displayed interlacing is exact, and each pattern labels one mathematical basis state., A filter target is an exact rational hypercharge. Completeness is certified only inside the explicitly supplied finite rectangular label domain., Calling a weight right hypercharge requires a separately supplied right-action convention. Matching a mathematical Y value alone does not select a physical state or distinguish every conjugate or equal-dimension irrep., The global low-dimension Y=1 statement uses the Weyl formula to exhaust all irreps of dimension at most ten; larger labels have dimension greater than ten., No accepted claim identifies an SU(3) irrep here with flavor, QCD color, a collective soliton, baryon number, spin statistics, an observed particle, or a substrate sector.. Comparators: S3 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; its Weyl and Casimir formulas survive, while its finite table, sextet convention, physical decuplet selection, inserted collective constraint, rotor gap, spin derivation, WZW identifications, and substrate reading are corrected qualified or rejected.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.106.0` with provenance `campaigns/P139-s3-su3-baryon-representation-audit/adjudication.yaml`.

- `campaigns/P139-s3-su3-baryon-representation-audit/verify.py`
- `campaigns/P139-s3-su3-baryon-representation-audit/reviews/independent_su3_tableau_review.py`
- `campaigns/P139-s3-su3-baryon-representation-audit/reviews/replay_source_graph.py`
- `campaigns/P139-s3-su3-baryon-representation-audit/attempts/0003/result.yaml`
- `campaigns/P139-s3-su3-baryon-representation-audit/attempts/0004/result.yaml`
- `campaigns/P139-s3-su3-baryon-representation-audit/attempts/0005/result.yaml`
- `campaigns/P139-s3-su3-baryon-representation-audit/attempts/0006/result.yaml`
- `campaigns/P139-s3-su3-baryon-representation-audit/attempts/0007/result.yaml`
- `campaigns/P139-s3-su3-baryon-representation-audit/evidence/source-reproduction.yaml`
- `campaigns/P139-s3-su3-baryon-representation-audit/evidence/source-audit.yaml`
- `campaigns/P139-s3-su3-baryon-representation-audit/evidence/check-adjudication.yaml`
- `campaigns/P139-s3-su3-baryon-representation-audit/evidence/input-provenance.yaml`
- `campaigns/P139-s3-su3-baryon-representation-audit/evidence/dependency-audit.yaml`
- `campaigns/P139-s3-su3-baryon-representation-audit/evidence/consumer-audit.yaml`
- `campaigns/P139-s3-su3-baryon-representation-audit/evidence/nonduplication-audit.yaml`
- `campaigns/P139-s3-su3-baryon-representation-audit/evidence/candidate-comparison.yaml`
- `campaigns/P139-s3-su3-baryon-representation-audit/evidence/primary-provenance.yaml`
- `campaigns/P139-s3-su3-baryon-representation-audit/evidence/literature-audit.yaml`
- `campaigns/P139-s3-su3-baryon-representation-audit/reviews/source_adjudication.md`
- `campaigns/P139-s3-su3-baryon-representation-audit/reviews/impact_analysis.md`
- `memory/vantasner/decisions/C-IRR-001-review.md`
- `memory/vantasner/decisions/S3-qualified-review.md`
- `src/substrate_framework/su3_representations.py`
- `tests/test_su3_representations.py`
