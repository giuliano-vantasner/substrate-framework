---
description: Qualified review of W3 V-A charged-current bridge
author: vantasner-review
created: '2026-08-10T00:45:00Z'
updated: '2026-08-10T00:45:00Z'
tags: [substrate-framework, source-review, migration-W3, currents]
category: decisions
confidence: established
status: archived
---
# W3 Qualified Review

## Decision

W3 is qualified through C-SG-011, C-SG-012, C-SG-013, C-BND-001,
C-REP-002, and C-U1-001 with no new claim or release. Its corrected scalar
derivative identities, epsilon-dual conservation, parity exchange, conditional
boundary trace, and field-type distinction survive under those ceilings. No
physical V-A current, charged vertex, intrinsic parity violation, charge event,
real-scalar U1 current, anomaly, gauge interaction, weak sector, or substrate
mechanism is promoted.

## Corrected Classification

For `phi=L(t+x)+R(t-x)`, direct chain rule gives
`phi_x=L'-R'`, hence the plus and minus characteristics are `2L'` and `2R'`.
W3 uses the negative sign and later imports the opposite channel label. With
signature `(+,−)` and `epsilon^(01)=+1`, the gradient derivative has divergence
`Box phi=-sin(phi)` on shell, while its epsilon dual is conserved off shell and
is exactly the accepted topological-current object up to normalization.

## Retained and Rejected Content

Scalar parity transforms the gradient as a vector, its dual as an axial vector,
and exchanges the null combinations. This is covariance, not a selected
parity-breaking interaction. W3 normalizes its Gaussian to the desired area,
assigns the compared charge and axial integers, imports a current belonging to
a distinct complex field, and equates one chosen zero correlation with zero
topological transfer. It supplies no boundary evolution, spinor, action,
connection, vertex, anomaly calculation, or dynamics.

## Compatibility and Closure

Native W3 passes its first three predicates and stops only at NumPy's removed
`trapz` name. Alias-only replay through `np.trapezoid` passes all seven. Primary,
independent, and frozen-graph routes pass 47, 25, and 61 checks. The seventeen-
node graph inventories 184 predicates and sixteen assertions. Mutable P148 code
has no executable legacy integration access; immutable compatibility shapes are
version-only evidence, not scientific failures.

## Cross-References

See P148, C-SG-011, C-SG-012, C-SG-013, C-BND-001, C-REP-002, C-U1-001,
the source, predicate, dependency, consumer, and nonduplication audits, fresh
independent derivation, impact analysis, and frozen source graph.
