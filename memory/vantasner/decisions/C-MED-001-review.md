---
description: Independent review of C-MED-001
author: vantasner-review
created: '2026-08-01T12:07:29Z'
updated: '2026-08-01T12:07:29Z'
tags:
- substrate-framework
- claim-review
- constitutive-scaling
category: decisions
confidence: working
status: archived
---
# Review of C-MED-001

## Claim Under Review
For positive density `rho`, thermal scale `Theta`, and reference speed `c`, the declared response laws `epsilon=rho*Theta/c^2` and `mu_inverse=rho*Theta` imply `epsilon*mu=1/c^2` and local wave speed `sqrt(mu_inverse/epsilon)=c`. Density and thermal variation cannot create an index within this co-scaling ansatz.

## Sourced Inputs
The review read `v0.7.0`, P008 and its attempt, canonical constitutive APIs/tests, S5 checks 5–8, and the source adjudication. The response laws are explicit premises. S5's separately declared continuum coupling and physical layer interpretation are not inputs.

## Independence
The main route substitutes the canonical responses. The independent route assigns arbitrary density and thermal exponents to both responses and derives logarithmic wave-speed sensitivities `(q-p)/2` and `(s-r)/2` before applying the matched-exponent case.

## Verification Status
Exact algebra, derivatives, and independent exponent analysis establish the full quantified result and earn `symbolic_verified`. The verdict is conditional on the constitutive ansatz and does not establish that a physical medium obeys it.

## Sensitivity and Counterexamples
Changing either density exponent or either thermal exponent relative to its partner restores nonzero sensitivity. These mutations show the cancellation depends on co-scaling rather than density disappearing tautologically.

## Framework Compatibility
The claim is a compatible utility with no fitted parameter or conflict with accepted optical geometry. It explicitly blocks the invalid inference from “this route produces no index” to “a desired nontrivial continuum index is realized.”

## Dependency and Consumer Replay
The claim has no accepted dependencies. Direct consumers are `constitutive.py`, exports/tests, S5's qualified disposition, and future medium proposals. No existing claim changes.

## Competing Candidate Audit
Matched-exponent analysis and conditional formula elimination were preregistered; the physical-closure narrative was rejected on dependency grounds. Previously visible comparators were excluded from every predicate.

## Four-Axis Decision

The exact conditional theorem supports a compatible accepted status.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: additive conditional theorem

## Promotion Transaction
Promotion adds the constitutive APIs/tests and `C-MED-001`, freezes P008, creates `v0.8.0`, qualifies S5/T2B with durable evidence, and regenerates canonical records.

## Continuation if Not Accepted
Failure would return to the general exponent route. A continuum coupling law could not be inserted to rescue the cancellation.

## Done Gate
The exact cancellation, domain, exponent sensitivity, independent route, and physical ceiling are complete with no claim debt.

## Cross-References
See `campaigns/P008-constitutive-qualification`, its source adjudication, S5/T2B, and the parent effort.
