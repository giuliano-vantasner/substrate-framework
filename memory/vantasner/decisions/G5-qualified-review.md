---
description: Qualified review of G5 medium density and effective-Newton relation
author: vantasner-review
created: '2026-08-09T18:55:00Z'
updated: '2026-08-09T18:55:00Z'
tags: [substrate-framework, source-review, migration-G5, medium-density]
category: decisions
confidence: established
status: archived
---
# G5 Qualified Review

## Decision

G5 is qualified through C-MED-001, C-MED-005, C-IDN-001, and C-GRV-001. Its
SI wave-product identity, selected wrong-form dimension guards, free-kappa
derivative, and conditional L4 substitution survive under those ceilings. No
SI mass density, strain-energy density, independent-prediction count, physical
medium, absolute gravity, observation, or substrate mechanism is promoted.

## Corrected Positive Object

A valid mechanical dictionary is rho=a*epsilon_0 and K=b/mu_0, where both
factors have dimension M^2*T^-4*I^-2. Its speed squared is
(b/a)/(epsilon_0*mu_0), so exact speed matching selects a=b but leaves that
common calibration free. Quadratic energy also requires dimensionless strain:
u=K*xi^2/2. This supplies a reusable positive theorem without pretending that
SI electromagnetic constants alone determine a material scale.

## Retained and Rejected Content

Current SI retains epsilon0*mu0=1/c^2 exactly, but epsilon0 and mu0 are
correlated rather than independent inputs. Bare epsilon0/2 is not mass density,
and bare 1/(2*mu0) is not energy density. L3 is algebraically dependent on L1
and L2. Repeated symbol membership is not an independence oracle. L4 follows
only after free kappa is assigned Newton-G units; energy- and mass-density
Einstein sources require distinct c restorations. G5's numeric Newton example
is a rounded imported comparator.

## Compatibility and Closure

Native G5 passes all fifteen predicates and has no NumPy compatibility event.
Primary, independent, graph, and focused routes pass 36, 20, 34, and 17 checks.
The fourteen-node graph pins 145 predicates. Immutable G1 and G4 keep only their
previous alias-backed compatibility shapes; mutable P145 code uses exact
algebra and contains no legacy integration access. GitNexus rates the additive
API change LOW risk with no affected execution process.

## Cross-References

See P145, C-MED-005, C-MED-001, C-IDN-001, C-GRV-001, the predicate,
dependency, consumer, source, literature, and nonduplication audits, the
independent derivation, and the frozen graph.
