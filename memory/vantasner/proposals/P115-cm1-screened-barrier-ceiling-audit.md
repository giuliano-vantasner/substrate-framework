---
description: Derive a conditional shifted-barrier theorem and adjudicate CM1's rate-ceiling interpretation
author: vantasner
created: '2026-08-08T02:00:00Z'
updated: '2026-08-08T02:00:00Z'
tags:
- substrate-framework
- campaign-proposal
- screened-barrier
- gamow-factor
category: proposals
confidence: exploratory
status: active
---
# P115 CM1 Screened-Barrier Ceiling Audit

## Question and Positive Deliverable

This campaign must deliver a reusable, exact, dimensionally closed theorem for
the bare and energy-shifted inverse-square-root barrier factors. The positive
object includes their enhancement composition, range, monotonicity, limits,
sensitivities, stable evaluation, conditional shift ceiling, and physical
interpretation ceiling. A reproduced tiny number or rejection of a fusion-rate
narrative does not complete the campaign.

## Base Release and Provenance

The accepted base is v0.94.0 at framework checkpoint
`f5b08ef102b4dea7f7db9ef51bd9bf7e882d8816`; the scientific base is
`6c4d1c6d1e7e84a1a093c0581e9b39bf9307590b`. The predecessor baseline remains
`/home/dan/substrate` commit
`6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`.

The candidate is CM1 at
`merged-framework/bridges/phase-31/bridge_CM1_separation_boundary.py`, SHA-256
`0f6881d96469274664ed1b762ff56a88b94ecdca599c22f8bb181052bd7f3ccc`,
git blob `8cd33750623af98eaee6cd2201670b205cd71a3a`, and 11,249 bytes. Its external
candidate module is `engineering/screening/screening.py`, SHA-256
`8ed6d54c8e3626f58ee2b3da78ce6eea7f4689092103dc23ed888b985e4cb4c3`,
git blob `728fa930cb5539e701c777490e66ea51dc372ef1`, and 19,339 bytes.

Queue metadata exposes thirteen predicates, bare and shifted Gamow-form
factors, and forward dependencies CM2 through CM7. A prior repository search
also exposed formula lines and parts of the symbolic surface. This contract
does not claim pristine body blinding; it freezes every stronger gate before
execution, complete predicate inspection, or numeric comparator review.

Registry, campaign, and durable-memory searches found no accepted screening or
Gamow barrier theorem and no reserved C-SCR-001 identifier. C-GMR-001 is GMOR
parameter algebra and is unrelated. CM3, CM6, CM7, GB6, and WN7 are direct
source consumers; source cycles supply no authority.

## Invariants, Conventions, and Allowed Imports

Use positive collision energy E and barrier scale G, nonnegative energy shift
U, and one explicit common energy unit. Define the shifted dimensionless factor
as `exp(-sqrt(G/(E+U)))`. It must remain between zero and one, increase in E
and U, decrease in G, and transform covariantly under common energy rescaling.

The enhancement is the exact shifted-to-bare ratio. At positive fixed U its
separate factors become numerically singular as E approaches zero while their
composed expression has a finite nonzero limit. A supplied bound U at most
U_max yields a conditional upper barrier factor only; it neither derives the
shift nor proves a material ceiling.

No pending CM unit, external engineering prose, or comparator supplies
accepted physical inputs. Flux, cross section, S factor, attempt frequency,
density, branching, states, material realization, and observation remain
forbidden imports.

## Candidate Preregistration

The candidates distinguish reproduction, exact shifted-factor algebra,
enhancement composition, conditional bounding and countermodels, independent
rederivation, and governance closure.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal CM1 reproduction | Source conventions | Source inputs | Mixed evidence | Hash, tally, and predicate audit |
| B | Exact shifted-barrier theorem | E,G positive and U nonnegative | Three energies | Native conditional theorem | Exact range, derivatives, limits, dimensions, and scale covariance |
| C | Enhancement composition | Same domain | E,U,G | Stable exact product | Ratio identity and separate-versus-composed low-energy limit |
| D | Conditional ceiling and countermodels | Independently justified U_max | Shift family and prefactors | Exposes physical overreach | Bound direction plus zero/arbitrary prefactor and alternative-shift families |
| E | Fresh exact rederivation | Elementary calculus only | E,U,G | Independent confirmation | No import of canonical screened-barrier API |
| F | Governance and consumer audit | Complete registry and queue | None | Closed promotion scope | All inputs, cycles, consumers, and nonduplication explicit |

## Selection Criteria and Blinding

Selection is ordered by accepted dependency closure, exact dimensional and
domain closure, composition, derivative signs, sharp range and limits,
ceiling direction, sensitivity, stable evaluation, physical-semantic honesty,
assumption economy, reusable API fit, and complete consumer replay.

The formula family is already exposed. Numeric material values, reported tiny
floors, and consumer comparisons remain blinded until the contract, claim
scope, implementation tests, and structural verdicts are frozen. Numerical
closeness cannot select a theorem or physical interpretation.

## Proposed Claim Delta

P115 provisionally reserves C-SCR-001 for the exact conditional shifted-barrier
factor, enhancement ratio, monotonicities, endpoint limits, range, scale
covariance, conditional U_max ceiling, and explicit non-rate ceiling. It has no
accepted scientific dependency because the formula and inputs are conditional.

The proposed implementation is `src/substrate_framework/screened_barrier.py`.
The five direct source consumers remain pending and receive no authority from
CM1. No challenge or supersession relationship is proposed.

## Implementation and Oracle Plan

The canonical module will expose pure exact APIs for bare factor, shifted
factor, enhancement, and an exact sensitivity/limit ledger. SymPy will verify
identities, derivative signs, exact limits, series, dimensions, common-scale
covariance, and mutations of exponent sign, square-root power, shift sign, and
barrier normalization. Exact bounds will use declared positive assumptions,
not finite samples.

An independent verifier will rebuild the exponent and common-denominator
calculus without importing the canonical module. Countermodels will multiply
the factor by zero and arbitrary dimensionful prefactors, vary the shift law,
and propagate an energy interval to show why a penetrability alone is neither
a rate nor an absolute negligible-yield theorem.

CM1 numeric evaluation is regression only after exact formulas close. Stable
evaluation will use the composed exponent rather than a numerical zero times
an overflowing enhancement. No solver or quadrature is required. If sampled
integration appears in immutable source, a missing `np.trapz` receives an
alias-only replay; mutable canonical work would use `trapezoid_integral` or
`np.trapezoid`. Compatibility is not scientific rejection.

The consumer audit pins CM3, CM6, CM7, GB6, and WN7, excluding CM1 when a
cycle returns to the root. Targeted package, campaign, registry, generated
state, and consumer replays precede one full terminal workflow gate.

## Attempts and Continuation

Every source abort, compatibility event, dimensional mismatch, singular
evaluation, false monotonicity, failed ceiling direction, physical-prefactor
counterexample, or oracle defect is preserved before repair. If C-SCR-001 is
not distinct, the campaign must map the exact positive object to existing
governance rather than promoting a duplicate.

## Debt Ledger

The ledger tracks energy units and domains, shift and barrier provenance,
enhancement composition, low-energy evaluation, conditional ceiling direction,
input uncertainty, physical prefactors, material and reaction interpretations,
source cycles, five direct consumers, and nonduplication. It begins empty
because each item is an explicit frozen gate.

## Review and Promotion Plan

Every CM1 predicate receives an individual verdict. Exact primary and
independent reviewers, source and input audits, consumer replay, mutation
sensitivity, physical-semantic countermodels, and nonduplication determine
whether C-SCR-001 is accepted. Promotion requires an importable module, focused
tests, claim-level registry entry, release manifest, generated docs and memory,
and an empty debt ledger. CM1 is expected to be qualified if exact factor
algebra survives while its rate, yield, material, or channel narrative does
not.

## Done Gate

P115 closes only when the exact shifted-barrier object, enhancement,
monotonicity, limits, range, dimensions, scale covariance, conditional ceiling,
stable evaluation, countermodels, all thirteen predicates, source inputs,
consumer closure, governance records, and downstream replay pass with no debt.

## Cross-References

See CM1, CM2 through CM7, GB6, WN7, P115, provisional C-SCR-001, v0.94.0, and
the framework-migration effort.
