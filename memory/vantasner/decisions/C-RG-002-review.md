---
description: Independent review of C-RG-002 conditional capillary constitutive map
author: vantasner-review
created: '2026-08-04T20:00:00Z'
updated: '2026-08-04T20:00:00Z'
tags:
- substrate-framework
- claim-review
- capillary-barrier
- identifiability
category: decisions
confidence: established
status: archived
---
# Review of C-RG-002

## Claim Under Review

The claim composes an explicitly declared Frank/core line tension and
quadratic loading area drive with C-RG-001. It derives the exact critical
radius, relative barrier, dimension family, conditional sensitivities, sign
domain, and parameter-identifiability ceiling while excluding material and
rate interpretations.

## Sourced Inputs

The review reads release `v0.83.0`, C-RG-001, P006, the radial-energy module
and tests, P099's frozen proposal, all append-only attempts, the pinned BD1
source, predecessor formulas, predicate ledger, dependency audit, and consumer
map. Pending rung016/rung017 physical readings and all later DBD consumers are
evidence rather than accepted authority.

## Independence

The independent review imports none of the new constitutive APIs. It integrates
the declared Frank annulus, evaluates the tilted-well difference and standing-
profile average, completes the capillary square, eliminates the radius,
constructs the general exponent balance, and computes the observation ranks
and wrong-sign domain from fresh symbols.

## Verification Status

The maximum verdict is `symbolic_verified`. The primary route passes 41 checks
through canonical APIs; the independent route passes 18 checks; the focused
radial-energy suite passes 19 tests; and P006 replays 28 checks. No empirical
comparator, float tolerance, numerical integration, simulation, or source
tally carries the accepted verdict.

## Sensitivity and Counterexamples

Mutations of the relative-barrier pi coefficient, drive factor two, amplitude
power, wavenumber power, cutoff order, and zero loading coordinates fail. A
linear-amplitude law closes with the same coupling dimension as the quadratic
law when amplitude is dimensionless. Three independent positive rescalings
change drive constituents while preserving the area drive, radius, and
barrier. Negative area drive has only a negative stationary root and is
strictly increasing on positive radius.

## Framework Compatibility

The claim is a compatible extension of C-RG-001. It preserves the positive
capillary landscape and distinguishes the relative barrier from the absolute
energy offset. The declared constitutive inputs parameterize C-RG-001 without
changing its geometry, maximum, sign convention, or accepted dependencies.

## Dependency and Consumer Replay

The only accepted dependency is C-RG-001. B1, E1, and E2 are source-queue label
collisions; BD4 is downstream. The direct accepted consumers are the radial-
energy module, package exports, focused tests, and P006. The source engineering
consumer reproduces 16 checks, but its population, temperature, material,
rate, isotope, nuclear, and power descendants remain noncanonical or pending.

## Competing Candidate Audit

Candidates A through I were frozen before source execution and body exposure.
The literal source is retained as reproduction evidence and the generic
capillary result is rejected as duplicate. Exact closure selects the
conditional composition, dimension family, sensitivity ledger,
identifiability counterfamilies, sign domains, alternative laws, and consumer
ceiling. No comparator value selects the result.

## Four-Axis Decision

The exact conditional capillary constitutive theorem is accepted with every
premise, dimension convention, free parameter, and interpretation ceiling
explicit.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: depends on C-RG-001 and challenges or supersedes no accepted claim

## Promotion Transaction

Promotion adds C-RG-002, importable radial-energy APIs and tests, immutable
P099 evidence, qualified BD1 disposition, release `v0.84.0`, and synchronized
generated docs and accepted memory. The proposal becomes an adjudicated
campaign and the parent migration advances to BD2.

## Continuation if Not Accepted

This section is not invoked because the conditional theorem is accepted. A
material or rate claim requires a separate proposal deriving the constitutive
law, amplitude convention, coupling, dispersion, inertia, noise model, and
physical parameter values without using the desired output as input.

## Done Gate

The positive composition, dependency closure, two exact derivations,
load-bearing mutations, dimension alternatives, constructive
non-identifiability, sign domains, importable APIs/tests, and consumer ceiling
close with empty claim debt. Corpus migration continues after BD1.

## Cross-References

See P099, BD1-BD5, C-RG-001, P006, P086, the radial-energy module, and the
framework-migration effort.
