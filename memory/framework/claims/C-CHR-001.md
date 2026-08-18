---
description: Accepted framework claim C-CHR-001
author: framework-registry
created: '2026-08-03T02:00:00Z'
updated: '2026-08-03T02:00:00Z'
tags:
- substrate-framework
- accepted-claim
- C-CHR-001
category: claims
confidence: established
status: active
---
# C-CHR-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

For a positive integer n, let C_n be the additive cyclic group and let S={+1,-1} under multiplication. Every homomorphism C_n->S is fixed by the generator image epsilon subject to epsilon^n=1. If n is odd only epsilon=+1 is allowed; if n is even there are exactly two characters, the trivial one and chi_n([k])=(-1)^k. The nontrivial even-order character has the even-residue kernel of size n/2, quotient order two, and is faithful exactly when n=2. Thus chi(1)=-1 and chi(2)=+1 alone establish at most a supplied sign quotient, not that the source group is C_2. For every positive r, all characters of C_2^r are chi_a(x)=(-1)^(a dot x), indexed by a in C_2^r, so there are 2^r; every nontrivial character has a kernel of size 2^(r-1), and a faithful sign character exists exactly when r=1. Distinct characters can agree at -1 on a selected element while differing elsewhere and having different kernels. Separately supplied quotient maps into C_2 may pull back the same codomain sign character, but this does not identify their source domains, maps, generators, orientations, representations, operators, topologies, physical statistics, or substrate mechanisms.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `native`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-TOP-001. Assumptions: C_n uses its additive generator presentation, C_2^r uses componentwise addition modulo two, and the codomain signs compose by multiplication., Group orders and binary ranks are positive concrete integers; elements and selectors use exact integer or binary coordinates., Function identity requires a common typed domain and agreement on every element; equal values at selected inputs are insufficient., Any common pullback requires separately supplied quotient maps, and no pending OM1 dependency or physical interpretation is imported.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.60.0` with provenance `campaigns/P066-om1-cyclic-sign-characters/adjudication.yaml`.

- `campaigns/P066-om1-cyclic-sign-characters/verify.py`
- `campaigns/P066-om1-cyclic-sign-characters/attempts/0001/result.yaml`
- `campaigns/P066-om1-cyclic-sign-characters/attempts/0002/result.yaml`
- `campaigns/P066-om1-cyclic-sign-characters/attempts/0003/result.yaml`
- `campaigns/P066-om1-cyclic-sign-characters/reviews/independent_character_review.py`
- `campaigns/P066-om1-cyclic-sign-characters/evidence/primary-provenance.yaml`
- `campaigns/P066-om1-cyclic-sign-characters/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-CHR-001-review.md`
- `tests/test_topological_labels.py`
