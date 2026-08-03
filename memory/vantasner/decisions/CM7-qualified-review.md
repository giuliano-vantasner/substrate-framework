---
description: Terminal review of CM7's shifted-barrier crossover and threshold-measure claims
author: vantasner-review
created: '2026-08-08T10:30:00Z'
updated: '2026-08-08T10:30:00Z'
tags:
- substrate-framework
- claim-review
- shifted-barrier
- crossover
category: decisions
confidence: established
status: archived
---
# Review of CM7 Terminal Qualification

## Claim Under Review

CM7 claims an exact screened inverse-square-root crossing, its sensitivities,
and a broad one-eV payoff over most of an admissible level window. The review
requires full real-domain, endpoint, scale, identifiability, measure,
screening-input, solver, predicate, dependency, and consumer ledgers.

## Sourced Inputs

The review reads v0.97.0; C-XOV-001, C-SCR-001, and the narrow C-CMP-001
non-rate ceiling; their accepted source modules; P121's frozen contract; all
attempts; both verifiers; and every evidence record. CM7 is pinned at SHA-256
`10344b842a47b24651c891dfa55a030dd193e3e48e0b128b93bf74f29af6cee2`.
The screening and live materials supports are separately hash pinned.

Fresh source or output blinding is not claimed because CM6 already exposed and
executed CM7. Selection criteria were frozen before renewed inspection.

## Independence

The independent route imports neither P121 implementation nor
`crossovers.py`. It derives the inverse in the positive coordinate
`k=-log(c)`, differentiates it afresh, performs independent change-of-measure
calculations, reconstructs the four screening values from pinned constants,
and implements a bracket-status bisection oracle.

Five implementation or symbolic-representation mistakes are preserved. They
concern SymPy inequality representation, Boolean conversion, an incorrect
bitwise-saturation assumption, and an independent symbolic sign coercion. None
changed the domain, tolerance, physical ceiling, or candidate decision.

## Verification Status

The exact positive result is already C-XOV-001 with dependency C-SCR-001.
Forty-four primary and thirty-four independent checks close the real response
range, inverse, endpoints, derivatives, elasticities, scale covariance,
arbitrary-target inverse, competing measures, material model, root bracket,
random interval, and mutations.

No numerical integration occurs, and CM7 triggers no `np.trapz` compatibility
event. Root comparisons are numeric regression, never exact evidence.

## Sensitivity and Counterexamples

For `c>1`, the squared-log expression returns a response `1/c`, not `c`, so
the real range is load bearing. The floor is a zero-energy endpoint rather
than an interior positive crossing. Relative sensitivities diverge there.

Every positive target can be obtained by selecting `c=P(E_T)`, while changing
relative channel normalization moves the level and crossing. Uniform log-c and
uniform-c give different threshold fractions; point-mass laws realize
probabilities zero and one. The source's 1.84 percent is therefore not a
population probability.

All four materials assign one conduction electron per atom. A declared
sixty-four-electron Ni mutation doubles the selected screening scale, exposing
model dependence. The fixed `[0,1e9] keV` bisection fails at admissible
`c=0.9999`. The five-hundred-point random interval omits endpoints and the
bottom 0.1 percent of the log window.

## Framework Compatibility

C-XOV-001 already contains the complete exact theorem and physical
nonidentifiability ceiling. C-SCR-001 contains the conditional factor and does
not derive a rate, universal material screening value, or observation. The
additional measure, provenance, and solver results belong to source auditing
and create no reusable accepted API.

## Dependency and Consumer Replay

CM1, CM3, and CM6 are direct phase-cluster cycle or comparison consumers; GB6
and WN7 are transitive scanner descendants. They replay 131 checks. Candidate
edges and cycles grant no authority, and the campaign debt ledger is empty.

## Competing Candidate Audit

Literal reproduction, accepted theorem reuse, branch mutations, elasticity and
identifiability, competing threshold measures, material provenance, numerical
regression, and independent nonduplication review were frozen before renewed
inspection. The accepted-theorem reuse and no-API decision win on dependency
closure, exactness, parameter economy, and physical honesty.

## Four-Axis Decision

The review accepts no new claim and terminally qualifies CM7 through
C-XOV-001 and C-SCR-001.

- Verification: exact for the governed theorem; bounded numeric regression for selected roots and inputs
- Review: CM7 terminal disposition `qualified`
- Compatibility: native reuse of C-XOV-001 and C-SCR-001
- Epistemic: no new claim; source evidence qualified
- Relationship: challenges and supersedes none

## Promotion Transaction

The transaction records CM7 as qualified with the two individually reviewed
accepted claims, regenerates the source queue, archives proposal memory, and
checkpoints the parent effort. The registry, v0.97.0, generated accepted
documentation, and accepted memory remain unchanged.

## Continuation if Not Accepted

If either exact route, any predicate, input, dependency, cycle, consumer,
nonduplication, or synchronization check fails, CM7 returns to P121 for
append-only repair and remains pending. Rejecting a physical overreading never
substitutes for the complete exact and source-audit ledgers.

## Done Gate

Terminal qualification requires both exact routes, all twenty-seven predicate
verdicts, measure and screening provenance, solver counterexamples, every
consumer, synchronized disposition and queue state, one integrated workflow
pass, and an empty campaign debt ledger.

## Cross-References

See P099, P115, P116, P117, P120, P121, CM1, CM2, CM3, CM6, CM7, GB6, WN7,
C-XOV-001, C-SCR-001, C-CMP-001, v0.97.0, and the framework-migration effort.
