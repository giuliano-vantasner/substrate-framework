---
description: Derive exact monotone level-crossing theorems and adjudicate CM3's channel-dominance interpretation
author: vantasner
created: '2026-08-08T06:00:00Z'
updated: '2026-08-08T06:00:00Z'
tags:
- substrate-framework
- campaign-proposal
- monotone-crossover
- identifiability
category: proposals
confidence: exploratory
status: active
---
# P117 CM3 Monotone Crossover Audit

## Question and Positive Deliverable

This campaign must deliver a reusable exact theorem for a horizontal level
crossing a continuous strictly increasing response, with explicit range and
endpoint conditions. The positive object includes the exponential-saturation
inverse used by CM3, the actual C-SCR-001 shifted-factor inverse, sensitivities,
limits, convexity, common-scale covariance, strictness and continuity
counterexamples, identifiability, and a physical interpretation ceiling. A
reproduced `log(2)` value or rejection of channel dominance is not completion.

## Base Release and Provenance

The accepted base is v0.96.0 at framework checkpoint
`d9cc3ae1ffe62fc08e5640671a6d677cb158a641`; its scientific base is
`3a56c1553e977b4aed15253924b591a3bcc672b7`. The predecessor baseline remains
`/home/dan/substrate` commit
`6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`.

The candidate is CM3 at
`merged-framework/bridges/phase-31/bridge_CM3_crossover.py`, SHA-256
`d62d8deadbba30c4d240ed57c204149ffe0d6b2ec49ed0e200206a4b4a8eccdb`, git
blob `21d09380d7f83f84312dc13e845ea12d657d30df`, and 9,364 bytes. The hash
matches the source inventory. Unrelated Phase 47/48 work and the deliberate
current-NumPy compatibility overlay remain outside P117.

CM3 has already executed as a hash-pinned consumer during P115 and P116, so
its ten-check tally, c=0.5 example, and `log(2)` output are exposed. Queue
metadata also exposes its formula and channel-ordering prose. This contract
does not claim source-execution blinding; it freezes every stronger gate before
renewed execution, whole-body inspection, or additional comparator review.

The accepted authority read for this freeze is v0.96.0, C-SCR-001,
C-CMP-001, and the canonical screened-barrier and composite-factor modules.
Registry, campaign, and durable-memory searches found no C-XOV-001 identifier
or accepted general monotone level-crossing theorem. Existing isolated
crossings occur in other parameter systems and do not govern this response
range or physical ceiling.

## Invariants, Conventions, and Allowed Imports

A continuous strictly increasing map crosses a horizontal level at most once,
but existence requires the level to lie in its actual range. Finite endpoints,
limits approached only at infinity, and an open positive-energy domain must
not be conflated.

For E>=0 and E0>0, declare `S(E)=1-exp(-E/E0)`. It is dimensionless and has
range [0,1). The unique finite solution of S(E)=c is
`E=-E0*log(1-c)` for 0<=c<1, with a positive solution only for 0<c<1.
Neither S nor c is a physical rate without independent typing.

C-SCR-001's shifted factor is not S. At positive shift it has a finite positive
zero-energy floor. Its admissible c interval and exact inverse must be derived
independently from the accepted factor. C-CMP-001 supplies no flat physical
CM2 rate, and pending CM7 cannot be used as authority.

## Candidate Preregistration

The candidates separate reproduction, the general theorem, the source
specialization, the accepted screened specialization, countermodels, and
independent governance closure.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal CM3 reproduction | Source conventions | E0 and free c | Mixed evidence | Hash, tally, and ten-predicate audit |
| B | General monotone range theorem | Continuity, strict increase, declared endpoints | Function and level | Native mathematical theorem | Existence iff level is in range and at-most-one proof |
| C | Exponential saturation inverse | E>=0, E0>0, 0<=c<1 | E0 and c | Exact source algebra | Inverse, residual, derivatives, convexity, limits, and scaling |
| D | Actual shifted-barrier inverse | C-SCR-001 domains | E,G,U,c | Natural accepted specialization with positive floor | Exact admissible interval, inverse, sensitivities, and U=0 limit |
| E | Structural and physical countermodels | Alternative lawful maps and prefactors | Plateaus, jumps, oscillations, levels, normalizations | Exposes missing premises and nonidentifiability | Multiple/no crossing and zero/arbitrary-rate families |
| F | Fresh derivation and governance audit | Complete registry and queue | None | Closed adjudication scope | Independent proof, cycles, consumers, predicates, and nonduplication |

## Selection Criteria and Blinding

Selection is ordered by accepted dependency closure; explicit domains, ranges,
endpoints, units, and normalization; exact existence and uniqueness; sensitivity
to continuity and strictness; faithful C-SCR-001 specialization; scale
covariance; identifiability; physical-semantic honesty; assumption economy;
reusable API fit; and complete consumer replay.

The source formula and c=0.5 output are already exposed. Any other selected
numeric values and consumer comparisons remain excluded from selection until
the contract and structural verdicts validate. Numerical agreement cannot
select a theorem, response model, or channel interpretation.

## Proposed Claim Delta

P117 provisionally reserves C-XOV-001 for the general monotone level-crossing
range theorem, the exact exponential-saturation inverse and sensitivity
ledger, the independently derived C-SCR-001 shifted-factor crossing, common-
scale covariance, counterexamples, and an explicit non-rate and non-prediction
ceiling. Its only proposed accepted scientific dependency is C-SCR-001; the
general and exponential statements are elementary conditional mathematics.

The proposed implementation is `src/substrate_framework/crossovers.py`. No
challenge or supersession relationship is proposed. If the whole theorem is
already governed, P117 must qualify CM3 without promoting a duplicate.

## Implementation and Oracle Plan

The canonical module will expose pure exact APIs for exponential saturation,
its finite crossover, a sensitivity ledger, and the shifted-barrier crossover
using the canonical C-SCR-001 factor. A small range-classification API will
keep finite endpoints and open limiting values explicit.

SymPy is the strongest oracle for exact inversion, residuals, derivatives,
convexity, limits, scale covariance, and mutations. The general theorem will
be checked through its injectivity consequence and intermediate-value premises,
not by a copied root. Mutations alter the exponential sign, scale, level
complement, response floor, logarithm branch, and shifted-factor exponent.

An independent verifier will rederive both inverses without importing the new
module. Counterexamples include a plateau for lost strictness, a step for lost
continuity, a nonmonotone polynomial with multiple crossings, out-of-range
levels, the positive screened floor, arbitrary E0/c target families, and zero
or arbitrary physical-rate prefactors.

CM3 bisection is regression only after exact formulas close. No solver or
quadrature is needed for the accepted theorem. Canonical sampled integration
would use `trapezoid_integral`, mutable current-environment scripts would use
`np.trapezoid`, and an immutable source aborting only on `np.trapz` would
receive an alias-only replay before adjudication. Compatibility is not
scientific rejection.

The consumer audit will pin every direct and transitive source edge, exclude
cycle returns from authority, and replay only paths affected by CM3. Targeted
module, campaign, registry, generated-state, and consumer checks precede one
full terminal workflow gate.

## Attempts and Continuation

Every source abort, compatibility event, range error, false endpoint,
nonunique counterexample, surrogate mismatch, branch or sign defect,
identifiability failure, physical-prefactor counterexample, dependency leak,
and oracle defect will be preserved before repair. Failure of channel
dominance changes the next candidate and does not finish P117.

## Debt Ledger

The ledger tracks domains and ranges, finite versus limiting endpoints,
continuity and strictness, energy units, source versus screened response,
level and scale provenance, derivative and limit signs, identifiability,
physical normalization, CM1/CM2 ceilings, CM7 cycles, all ten predicates,
consumers, and nonduplication. It begins empty because every item is a frozen
gate.

## Review and Promotion Plan

Every CM3 predicate receives an individual verdict. Exact primary and
independent reviewers, source/input/dependency/cycle/consumer audits, mutations,
countermodels, and nonduplication determine whether C-XOV-001 is accepted.
Promotion requires an importable module, focused tests, claim-level registry
entry, release manifest, generated docs and memory, and an empty debt ledger.
CM3 is expected to be qualified if the mathematical crossover survives while
the CM2-rate, screened-surrogate, physical dominance, and prediction readings
do not.

## Done Gate

P117 closes only when the general theorem, both exact specializations, domains,
ranges, endpoints, sensitivities, scaling, counterexamples, identifiability,
all ten predicates, dependency and consumer closure, governance records, and
downstream replay pass with no debt.

## Cross-References

See CM3, CM1, CM2, CM7, C-SCR-001, C-CMP-001, provisional C-XOV-001,
v0.96.0, and the framework-migration effort.
