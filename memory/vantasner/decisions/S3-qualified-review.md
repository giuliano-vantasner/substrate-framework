---
description: Qualified review of S3's SU(3) WZW baryon-representation source claim
author: vantasner-review
created: '2026-08-09T11:00:00Z'
updated: '2026-08-09T11:00:00Z'
tags: [substrate-framework, source-review, migration-S3, su3, wzw]
category: decisions
confidence: established
status: archived
---
# S3 Qualified Review

## Decision

S3 is qualified through C-IRR-001, C-LIE-001, C-LIE-002, C-WZW-002, and
C-TOP-002. C-IRR-001 is promoted for the distinct exact representation
surface. No physical collective-WZW or baryon claim is promoted.

## Corrected Positive Object

The exact SU(3) object derives arbitrary-label dimension, Casimir, triality,
complete basis states, weight multiplicities, and SU(2)xU(1) rows. At `Y=1`,
the octet is the unique minimum. Dimension ten is a tie between the
antidecuplet with `I=1/2` and decuplet with `I=3/2`; a weight filter alone
does not choose the latter.

## Retained and Rejected Content

S3's Weyl and Casimir formulas survive. Its sextet hypercharge table is wrong,
its enumeration is finite and incomplete, and its two-color prose is
inconsistent. It inserts `Y_R=N_c*B/3`, `N_c=3`, baryon number, statistics,
state labels, and physical names. Under its displayed rotor Hamiltonian the
decuplet-octet gap is `3/(2I1)`, not `3/(2I2)`. Literal periods and finite
exponential samples do not replace the narrower accepted WZW theorems.

## Compatibility and Closure

S3 has no NumPy compatibility event. Primary, independent, graph, and focused
routes pass 28, 16, 39, and 31 checks. The 17-node graph pins 195 predicates.
S2 and WZ3 retain prior alias-only paths backed by `np.trapezoid`; no mutable
legacy quadrature access is introduced. GitNexus risk is LOW.

## Cross-References

See P139, C-IRR-001, its predicate adjudication, source audit, literature
audit, impact analysis, and frozen dependency/consumer graph.
