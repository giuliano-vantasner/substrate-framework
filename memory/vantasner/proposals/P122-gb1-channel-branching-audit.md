---
description: Exact two-channel branching, normalization, dependency, and GB1 audit
author: vantasner
created: '2026-08-08T11:00:00Z'
updated: '2026-08-08T11:30:00Z'
tags:
- substrate-framework
- campaign-proposal
- branching-fraction
- rate-ceiling
category: proposals
confidence: exploratory
status: archived
---
# P122 GB1 Channel Branching Audit

## Question and Positive Deliverable

This campaign must reproduce and independently audit GB1's two declared
rate-valued objects, branching fractions, odds, relative enhancement,
dimensions, domains, endpoints, normalizations, weight and count assumptions,
dependency closure, selected-symbol scan, and every predicate. It must decide
whether a reusable two-channel allocation theorem survives or whether all
useful content is source-specific algebra. A rejected physical channel reading
does not replace the positive exact ledger and terminal disposition.

## Base Release and Provenance

The accepted base is v0.97.0 at parent checkpoint
`c8d0fbdf907a502ff4884b701bd09a8a10696300`, whose latest scientific
adjudication is `59e1e9e3293ef396115aa3d5fad6f279e74a8c9a`. GB1 is the next
pending unit at `merged-framework/bridges/phase-32/bridge_GB1_channel_definitions.py`
in source commit `6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`, pinned by SHA-256
`ace0515d7ea362ef45a55db22308aecffdad9a003d03f2b1209c0a11874b489b`,
git blob `145bfcaeed8353efcc3b81bcd87a596fa7bea4da`, and size 9,360 bytes.

The body and runtime output remain unopened in P122 at freeze. Generated queue
metadata already exposes the two displayed rates, branching reductions,
relative enhancement, source dependencies, and advertised free-symbol result,
so only body, predicate-detail, selected-value, and output blinding remains.

The direct accepted authority read is v0.97.0, C-CMP-001 and
`composite_factors.py`, and C-SPN-002 and `symmetric_spin.py`. P110 and PN2
supply qualified arithmetic only and no accepted claim. Memory search located
those exact reviews and the parent done gate; every reused fact was rechecked
in the registry and modules. Unrelated dirty Phase 47/48 work and the source
compatibility overlay remain excluded from authority.

## Invariants, Conventions, and Allowed Imports

For nonnegative rates `A` and `B` not both zero, the shares `A/(A+B)` and
`B/(A+B)` lie in the closed unit interval and sum to one. They preserve zero
and unit endpoints, depend only on relative normalization, and are undefined
at the double-zero point. Calling the inputs rates is a premise: algebra can
propagate inverse-time units but does not construct physical states,
interactions, final-state measures, or kinetics.

For `A=r_s*w*N` and `B=r_gamma`, `w` and `N` must be dimensionless for the
rates to share units. The reduction `rho=r_gamma/r_s` requires `r_s>0`.
Odds and a ratio-of-ratios enhancement require nonzero rates and a nonzero
baseline weight. Common scaling cancels; independent scaling changes the
fractions. Free normalizations, weight, and count make the result
nonpredictive until independently fixed.

C-SPN-002 supplies exact normalized ladder algebra and explicitly no rate.
C-CMP-001 supplies a conditional matrix-element-dimensional composition and
explicitly no rate or physical channel. PN2 supplies arithmetic only. Exact
real algebra, dimensions, limits, inequalities, source hashes, and SymPy are
allowed. Candidate dependency edges and symbol-name absence supply no
authority or semantic completeness.

## Candidate Preregistration

The candidate set separates literal reproduction, a general allocation
theorem, the GB1 specialization, enhancement premises, countermodels,
dependency closure, symbol-scan semantics, and a no-new-claim outcome.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Reproduce every GB1 predicate | Pinned source conventions | Source symbols | Regression evidence only | Clean exit, AST and predicate ledger |
| B | General two-channel allocation theorem | Nonnegative rates not both zero | A and B | Exact reusable simplex and odds object | Endpoints, bounds, derivatives, limits and common scaling |
| C | GB1 rate specialization | Dimensionless positive weight and finite count | r_s, r_gamma, w, N | Conditional reduction through rho | Units, substitutions, domain mutations |
| D | Relative enhancement ledger | Positive comparison rate and nonzero baseline | N, n, w | Normalizations cancel conditionally | Exact ratio, zero-baseline and arbitrary-weight probes |
| E | Countermodel family | Minimal algebraic premises | zeros, signs, units and prefactors | Physical conclusions remain unclosed | Zero coupling, independent scaling, negative weight and dimension mismatch |
| F | Accepted dependency audit | C-CMP-001 and C-SPN-002 only | none | No inherited physical rate | Registry and source-module closure |
| G | Selected-symbol absence audit | Exact source matcher after freeze | names and aliases | Finite syntax only | Collision, alias, import and equivalent-semantic probes |
| H | Independent review and no-new alternative | No P122 implementation reuse | none | Promote only if reusable novelty survives | Fresh derivation, impact, consumers and nonduplication |

## Selection Criteria and Blinding

Candidates are ranked first by accepted dependency closure, denominator and
endpoint domains, dimensions, bounds, partition, ratio invariance, and limits.
Next come free-parameter identifiability, physical-rate separation, mutation
sensitivity, scan specificity, novelty, parameter economy, reusable API value,
and complete predicate and consumer review. Numerical agreement and source
confidence words cannot select a theorem.

The queue-exposed algebra is acknowledged. The source body, exact predicate
wording, selected values, and runtime output remain blinded until the matching
manifest and immutable copy pass repository validation.

## Proposed Claim Delta

P122 reserves provisional C-BRN-001 for the exact general two-nonnegative-rate
allocation theorem, including the excluded double-zero point, endpoints,
partition, odds, derivatives, monotone limits, and common-scale invariance. Its
GB1 specialization and ratio-of-ratios result may remain corollaries. The
identifier will not be accepted if registry search, impact analysis, or source
review shows duplication, no reusable consumer, or assumption-heavy novelty.

C-CMP-001 and C-SPN-002 are reviewed individually and remain unchanged. The
mandatory source delta is a terminal GB1 disposition with every predicate,
dependency, cycle, scan premise, and direct and transitive consumer reviewed.

## Implementation and Oracle Plan

Candidate B may produce a pure `src/substrate_framework/branching.py` API with
exact SymPy validation and focused tests. The primary route will derive the
simplex, odds, derivatives, Hessian or elasticity behavior where meaningful,
endpoints, common-scale invariance, and the GB1 substitutions. Mutations cover
the double-zero denominator, negative rates or weights, non-dimensionless
factors, zero comparison normalization, zero baseline, independently rescaled
channels, arbitrary weight laws, and fake asserted fractions.

The source AST will recover every check and the actual absence rule after
freeze. Alias, imported-value, constant, function, comment, and benign-name
probes will distinguish selected free-symbol evidence from semantic or
data-flow closure. Exact algebra is the oracle; any source numeric examples are
regression only.

An independent verifier will derive the shares from the positive total and an
odds coordinate without importing P122 implementation. It will independently
check the specialization, normalization covariance, endpoint countermodels,
and physical-rate premises. Direct consumers GB4, GB6, WN2, and WN5 and the
ten generated transitive consumers will be hash pinned and replayed without
granting their pending claims authority.

Compatibility preflight searches GB1 and executed consumers. Canonical sampled
integration uses `trapezoid_integral`; mutable scripts use `np.trapezoid`; an
immutable source that aborts solely on `np.trapz` receives an alias-only replay
and no scientific rejection. Exact branching algebra should require no
quadrature.

The primary and independent routes, focused package tests if an API survives,
source predicates, consumers, governance validator, regenerated queue, memory,
one final `scripts/validate.sh`, and `git diff --check` form the terminal
boundary. The full suite runs once at the unchanged promotion boundary.

## Attempts and Continuation

Every failure is appended with its command, diagnosis, scientific effect, and
next candidate. The first preserved failure is a prefreeze template-path guess;
the correct campaign-proposal contract was then read in full. Algebra,
representation, implementation, dependency, or oracle failures are repaired
without weakening the denominator domain or physical ceiling.

## Debt Ledger

The ledger tracks rate and factor dimensions, signs, zero denominators,
endpoints, counts, weight domains, rho and odds definitions, baseline
normalization, arbitrary prefactors, physical states and interactions,
selected-symbol scope, imports, aliases, dependencies, cycles, consumers,
claim novelty, generated records, and compatibility. It is empty at freeze and
must remain empty at adjudication.

## Review and Promotion Plan

Every source predicate receives an individual verdict. Exact primary and fresh
routes must agree before C-BRN-001 is considered. Impact and nonduplication
reviews decide whether the generic object belongs in the package; an accepted
claim requires focused tests, registry and release updates, generated docs and
memory, and downstream replay.

If the result is already governed or too source-specific, P122 closes as an
immutable no-release campaign and GB1 receives a disposition with only its
individually justified accepted mappings. The final gate attempt begins in
progress and is finalized only after clean exit; later record-only edits
receive targeted validation rather than another full suite.

## Done Gate

P122 closes only when the exact branching and specialization objects exist,
all domains and endpoints are explicit, dimensions and physical ceilings are
closed, novelty is decided, every predicate, import, dependency, cycle, scan,
and consumer is audited, mutation-sensitive verification passes, canonical
records agree, and the debt ledger is empty. A partition-to-one identity,
declared rate unit, or green source tally does not complete the campaign alone.
