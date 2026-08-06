---
description: Accepted framework claim C-PHS-001
author: framework-registry
created: '2026-08-06T07:46:24Z'
updated: '2026-08-06T07:46:24Z'
tags:
- substrate-framework
- accepted-claim
- C-PHS-001
category: claims
confidence: established
status: active
---
# C-PHS-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let N>=2 scalar phases theta_1,...,theta_N be points on one circle and let W=max_{i<j} cos(theta_i-theta_j) over the complete pair graph. Sorting the phases gives a nearest circular gap at most 2*pi/N, and a regular N-gon attains the bound, so the sharp optimum is inf_{theta_1,...,theta_N} W=cos(2*pi/N). Therefore a complete scalar phase graph can have every pairwise cosine strictly negative exactly when N<=3, while every pairwise cosine can be nonpositive exactly when N<=4. The strict capacity is achieved at N=3 by phases (0,2*pi/3,4*pi/3), whose pairwise cosines are -1/2; the weak capacity is achieved at N=4 by quadrature phases and includes zero cosines. These are upper capacities, not occupancy selectors: N=2 also satisfies the strict condition. Sparse interaction graphs can admit more scalar phases, and higher-dimensional internal orientations can admit four pairwise negative products, as the regular tetrahedral vectors show. The theorem establishes no interaction kernel, force sign, common field solution, equilibrium, merger or persistence dynamics, stability, physical CP operation or violation, condensate or generation identity, selected count three, Standard-Model map, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: none. Assumptions: The phases are scalar points modulo 2*pi and every unordered pair belongs to the complete interaction graph., Pairwise comparison uses cosine of the shortest circular separation; no kernel weight sign or dynamics is imported., Strict negativity and weak nonpositivity are different predicates with capacities three and four respectively., The optimal-worst-cosine theorem is a geometric capacity result and supplies neither required occupancy nor a physical meaning for N.. Comparators: GC4's exact ordered-gap argument and regular Z3 witness survive while its merger stability and exact-count readings are rejected, A four-cycle with alternating phases is a sparse-graph countermodel to complete-graph universality, Four regular-tetrahedral vectors are a higher-internal-dimension countermodel to scalar-circle universality.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.153.0` with provenance `campaigns/P211-gc4-phase-packing-stability-audit/adjudication.yaml`.

- `campaigns/P211-gc4-phase-packing-stability-audit/verify.py`
- `campaigns/P211-gc4-phase-packing-stability-audit/reviews/independent_phase_interaction_review.py`
- `campaigns/P211-gc4-phase-packing-stability-audit/reviews/C-PHS-001-claim-review.md`
- `campaigns/P211-gc4-phase-packing-stability-audit/reviews/source_adjudication.md`
- `campaigns/P211-gc4-phase-packing-stability-audit/evidence/formula-freeze.yaml`
- `campaigns/P211-gc4-phase-packing-stability-audit/evidence/nonduplication-audit.yaml`
- `campaigns/P211-gc4-phase-packing-stability-audit/evidence/primary-provenance.yaml`
- `campaigns/P211-gc4-phase-packing-stability-audit/evidence/independent-provenance.yaml`
- `campaigns/P211-gc4-phase-packing-stability-audit/evidence/compatibility-audit.yaml`
- `campaigns/P211-gc4-phase-packing-stability-audit/evidence/impact-analysis.yaml`
- `src/substrate_framework/phase_interactions.py`
- `tests/test_phase_interactions.py`
