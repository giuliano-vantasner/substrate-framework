---
description: Qualified review of SM1 combined Standard Model gauge-group bridge
author: vantasner-review
created: '2026-08-10T19:18:00Z'
updated: '2026-08-10T19:18:00Z'
tags: [substrate-framework, source-review, migration-SM1, product-gauge-algebra]
category: decisions
confidence: established
status: archived
---
# SM1 Qualified Review

## Decision

SM1 is qualified through C-PGA-001 and the accepted C-LIE-001 and C-REP-002
factor claims. Its complete exact local tensor-factor algebra survives; its
global Standard Model group and simultaneous physical gauge-sector headline do
not.

## Corrected Positive Object

On `C^3 tensor C^2`, the standard SU3 and Pauli-half SU2 tensor embeddings
close their factor brackets and commute across factors. A supplied exact real
nonzero scalar U1 weight produces twelve independent matrices and a faithful
local `su3 direct-sum su2 direct-sum u1` representation. The joint commutant of
the non-Abelian factors is exactly the scalar span, and a supplied algebra-valued
connection component is the exact three-factor linear sum.

## Retained and Rejected Content

SM1's six predicates reproduce, but its rank test silently substitutes U1
weight one. Local brackets do not select compact normalization or distinguish
a direct product from a finite central quotient. No faithful physical matter
table, local product transformation, action, kinetic term, current, field
equation, dynamical boson, coupling match, observation, or substrate mechanism
is constructed.

## Compatibility and Closure

Primary and independent exact routes pass 31 and 13 checks; 62 affected
accepted-API tests pass; the nine-node graph passes 22 checks while separating
80 lexical sites, 80 runtime executions, and nine assertions. Every node is
native and has no NumPy integration surface. SM2, SM3, SM4, and GK1 receive no
new physical authority. SM1 is terminally qualified in v0.125.0.

## Cross-References

See P163, C-LIE-001, C-REP-002, C-PGA-001, the source and predicate audits,
independent derivation, source graph, primary provenance, and impact analysis.
