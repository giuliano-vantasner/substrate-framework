---
description: Qualified review of W1 parity-odd chiral boundary coupling
author: vantasner-review
created: '2026-08-09T20:35:00Z'
updated: '2026-08-09T20:35:00Z'
tags: [substrate-framework, source-review, migration-W1, boundary-parity]
category: decisions
confidence: established
status: archived
---
# W1 Qualified Review

## Decision

W1 is qualified through C-BND-001, C-SG-011, and C-SG-013. Its linear
massless characteristic identity and exact coefficient-family parity pullback
survive under those ceilings. No intrinsic parity violation, epsilon-to-charge
selection, correlation-as-topological-transfer, vector or chiral dynamics,
fermion parity, weak interaction, boundary action, or nonlinear chiral split
is promoted.

## Corrected Positive Object

For `R=a*u+beta*v-J`, scalar fixed-coordinate parity maps the beta member to
the minus-beta member. The mixed residual has even `a*u-J` and odd `beta*v`
parts and is not itself odd. A domain-and-normal parity map preserves the
normal coefficient. One residual leaves one trace free. These exact facts
supply a reusable positive boundary theorem without turning an orientation or
parameter exchange into a physical interaction.

## Retained and Rejected Content

W1.1 is retained only as a linear massless projector identity. W1.2 is retained
as family covariance, not fixed-theory invariance. W1.3 hard-codes its charge
map. W1.4 inserts zero spatial trace, while W1.4b violates its displayed
epsilon-plus residual. W1.5 and W1.6 test inserted integer arithmetic. W1.7
detects a nonzero odd component but not pure oddness. The relabelled correlation
contains no vacuum-boundary evidence for topological transfer.

## Compatibility and Closure

Native W1 stops only at two removed `np.trapz` calls after its first three
checks. Alias-only `np.trapezoid` replay passes all eight checks; the event is
version compatibility, not scientific evidence against the source. Primary,
independent, graph, and focused routes pass 39, 23, 45, and 21 checks. The
eleven-node graph pins 129 predicates and ten assertions. Mutable P146 and
canonical code have no legacy integration access. GitNexus rates the additive
API change LOW risk with no affected execution process.

## Cross-References

See P146, C-BND-001, C-SG-001, C-SG-011, C-SG-013, the predicate,
dependency, consumer, source, and nonduplication audits, the independent
derivation, and the frozen graph.
