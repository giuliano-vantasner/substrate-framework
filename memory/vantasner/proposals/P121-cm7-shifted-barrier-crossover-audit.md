---
description: Exact shifted-barrier inverse, threshold-measure, material-input, and CM7 audit
author: vantasner
created: '2026-08-08T10:00:00Z'
updated: '2026-08-08T10:30:00Z'
tags:
- substrate-framework
- campaign-proposal
- shifted-barrier
- crossover
category: proposals
confidence: exploratory
status: archived
---
# P121 CM7 Shifted Barrier Crossover Audit

## Question and Positive Deliverable

This campaign must reproduce and independently audit CM7's exact shifted
inverse-square-root level crossing, its complete domain and endpoint cases,
sensitivities, dimensions, scale behavior, free-level identifiability,
threshold-window measure, selected material inputs, numerical regressions, and
all twenty-seven predicates. It must decide novelty against C-XOV-001 and
C-SCR-001 and terminally adjudicate CM7; a green exact solve or rejection of a
physical narrative does not replace the positive ledger and disposition.

## Base Release and Provenance

The accepted base is v0.97.0 at parent checkpoint
`0ebb6762117cf593cc76f0b4842855843938a7ca`, whose latest scientific
adjudication is `c8c323ed23015f636700bbd743a4cc025f752ea0`. CM7 is the next
pending unit at
`merged-framework/bridges/phase-31/bridge_CM7_gamow_crossover.py` in source
commit `6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`, pinned by SHA-256
`10344b842a47b24651c891dfa55a030dd193e3e48e0b128b93bf74f29af6cee2`, git
blob `5cfd67d2301cfe5b72154bd39b50218d136f599c`, and size 19,709 bytes.

Fresh source and output blinding is impossible. CM6's audit exposed extensive
CM7 line content and ran all twenty-seven predicates, while the generated queue
exposes the inverse, domain, derivative, screening-input, and threshold
headlines. P121 records that exposure and freezes stronger gates before renewed
line-by-line inspection and execution.

The direct accepted authority read for the freeze is v0.97.0, C-XOV-001 and
`crossovers.py`, and C-SCR-001 and `screened_barrier.py`. C-CMP-001 supplies
only the accepted reason that CM2 is not a physical flat rate or common
observable. Memory search located the accepted reviews and parent done gate;
each reused fact was rechecked in the registry and modules. The selected source
screening module is pinned at SHA-256
`8ed6d54c8e3626f58ee2b3da78ce6eea7f4689092103dc23ed888b985e4cb4c3`
and becomes noncanonical evidence only after freeze. Unrelated dirty Phase
47/48 work and the compatibility overlay remain excluded from authority.

## Invariants, Conventions, and Allowed Imports

For real `E>=0`, `G>0`, and `U>0` in one energy unit, the declared factor
`P(E)=exp(-sqrt(G/(E+U)))` is continuous and strictly increasing from the
attained floor `p0=exp(-sqrt(G/U))` to the unattained limit one. A unique
positive crossing exists exactly for `p0<c<1` and is
`E_x=G/log(c)^2-U`. The floor itself crosses at zero; one occurs only at
infinite input; other levels do not cross. The `U=0` limiting case has floor
zero and inverse `G/log(c)^2` for `0<c<1`.

The logarithm is the real natural logarithm of a positive dimensionless level.
Its branch and the open interval are load bearing even though the inverse uses
the square of the logarithm. Exact sensitivities on the interior are
`partial_c E_x=-2G/(c log(c)^3)>0`,
`partial_G E_x=1/log(c)^2>0`, and `partial_U E_x=-1`. Elasticities inherit the
zero-crossing singularity. Common positive scaling of every energy rescales
the inverse and an energy threshold; partial rescalings do not.

Every positive target can be fitted by choosing `c=P(E_T)`, so a free level is
nonidentifying. The threshold level is
`c_T=exp(-sqrt(G/(U+E_T)))`. Only under an explicitly uniform log-c measure is
the below-threshold fraction `1-sqrt(U/(U+E_T))`; uniform-c and arbitrary
probability laws differ. No probability distribution over c is imported.

C-XOV-001 already owns the complete exact theorem and its physical ceiling.
C-SCR-001 owns the conditional factor and explicitly supplies no physical
screening energy, universal material maximum, cross section, rate, coherent
channel, yield, heat, or observation. A maximum over four assigned source
models is a selected input, not universal. Exact calculus, dimensions,
measure countermodels, SymPy, the accepted modules, and hash-pinned source
bytes are allowed. Numerical root solves are regression only.

## Candidate Preregistration

The candidate set separates literal reproduction, accepted theorem reuse,
endpoint and branch auditing, sensitivity and identifiability, measure choice,
material provenance, numerical regression, and independent governance closure.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Reproduce all twenty-seven CM7 predicates | Pinned source conventions only | Source inputs | Regression evidence only | Clean exit, AST and predicate ledger |
| B | Accepted exact shifted inverse ledger | C-XOV-001 and C-SCR-001 premises | E, G, U, c | Full positive math is already governed | API match, exact residual, range and derivative tests |
| C | Endpoint, branch and mutation audit | Real declared factor | c and U boundary cases | Squared log alone cannot relax the domain | Floor, one, outside-range, wrong-sign and unscreened probes |
| D | Elasticity and identifiability ledger | Interior positive crossing | free level and scales | Any target fits; elasticities expose floor sensitivity | Exact inverse target and limit calculations |
| E | Threshold-measure comparison | Explicit measure over admissible levels | E_T and distribution | Few-percent wording is measure-dependent | Log-uniform, uniform-c and concentrated-law results |
| F | Material-input provenance audit | Pinned source screening module | models, constants and units | Selected maximum is not universal | Exact import inventory, conversions, uncertainty and alternatives |
| G | Numerical regression audit | Declared bracket and exact monotone factor | tolerance, iterations and samples | Bisection repeats the exact inverse | Status, residual, refinement and mutated-root rejection |
| H | Independent rederivation and governance closure | No P121 implementation reuse | none | No new claim or API if exact surface matches | Fresh formulas plus complete predicate and consumer review |

## Selection Criteria and Blinding

Candidates are ranked first by accepted dependency closure and exact response
domain, range, endpoints, logarithm branch, inverse, dimensions, and
sensitivities. Next come common-scale behavior, free-level identifiability,
measure declaration, source-parameter provenance, boundary and mutation
sensitivity, novelty, parameter economy, reusable API value, and complete
solver and consumer review. Numerical agreement or the prior tally cannot
select a concept.

No fresh body or output blinding is claimed. Domain, endpoint, logarithm,
inverse, derivative, elasticity, scale, identifiability, threshold-measure,
material-provenance, solver, mutation, predicate, dependency, cycle, import,
and consumer gates are frozen before renewed inspection or execution.

## Proposed Claim Delta

No claim identifier is proposed at freeze. Candidate B predicts that
C-XOV-001 already contains CM7's complete mathematical surface with dependency
C-SCR-001. A new identifier will be reserved only if a distinct exact theorem
survives with a reusable consumer and assumptions not manufactured from the
selected source inputs.

The mandatory source delta is a terminal CM7 disposition with every predicate,
import, dependency, cycle, selected parameter, and direct and transitive
consumer reviewed. Existing claims are considered individually and are not
blanket-promoted through the source tally.

## Implementation and Oracle Plan

The primary route will call the accepted exact crossover and screened-factor
APIs, derive all endpoint cases, residuals, sensitivities, elasticities, scale
laws, arbitrary-target inverse, and threshold fractions, and compare them with
the pinned CM7 AST. Load-bearing mutations change the response sign,
logarithmic power, shift sign, factor floor, c domain, energy units, scale
convention, threshold measure, selected maximum, solver bracket, and exact
root.

The source screening module will be audited for the pair, material list,
constants, units, model assumptions, maximum operation, and missing uncertainty
or universality premise. Uniform log-c, uniform-c, and concentrated probability
laws will demonstrate that a window-length fraction is not a population
probability. Zero normalization and arbitrary common-observable maps preserve
the formal inverse while changing physical channel conclusions.

An independent verifier will derive the inverse through the positive coordinate
`k=-log(c)` and fresh monotonicity and change-of-variable arguments without
importing P121 or `crossovers.py`. Exact results are the oracle; bisection and
random samples are only regression and mutation coverage. If all positive
content duplicates accepted APIs, orchestration stays inside P121 and no
redundant package module or tests are added.

Compatibility preflight searches CM7 and executed consumers. Canonical sampled
integration uses `trapezoid_integral`; mutable scripts use `np.trapezoid`; an
immutable source that aborts solely on removed `np.trapz` receives an alias-only
replay and no scientific rejection. CM7's exact and root work is expected to
require no quadrature.

The primary and independent verifiers, focused accepted tests, hash-pinned
direct and transitive consumers, governance validator, regenerated queue and
memory checks, one final `scripts/validate.sh`, and `git diff --check` form the
terminal boundary. The full suite runs once, not after each attempt.

## Attempts and Continuation

Every failed route is appended under P121 with its command, diagnosis,
scientific effect, and next candidate. Implementation, representation, solver,
or oracle defects are repaired without weakening the exact domain or physical
ceiling; duplicated content is retained as audit evidence rather than promoted.

## Debt Ledger

The ledger tracks energy and level domains, logarithm branches, endpoint cases,
dimensions, derivatives, elasticities, scale conventions, free-level
identifiability, threshold measure, probability distribution, screening models,
constants, units, material list, uncertainty, maximum selection, solver bracket,
tolerance, residual, convergence, mutations, imports, cycles, consumers, and
physical normalization. It is empty at freeze and must be empty at adjudication.

## Review and Promotion Plan

Claim-level review will compare both exact routes with C-XOV-001 and C-SCR-001
before any registry edit. The source audit will classify all twenty-seven
symbolic, domain, derivative, numerical, fake, import, and physical-payoff
predicates separately. Direct and transitive consumers replay from pinned
hashes, while source cycles remain provenance only.

If a distinct claim survives, promotion requires an importable module and
tests, immutable P121, a release, generated docs and accepted memory, CM7's
disposition, regenerated queue, and complete validation. If C-XOV-001 governs
everything exact, P121 closes as an immutable no-release campaign with CM7
qualified through C-XOV-001 and C-SCR-001. A final gate attempt starts in
progress and is finalized only after clean exit; later record edits receive
only targeted checks.

## Done Gate

P121 closes only when the exact range, inverse, endpoint, sensitivity,
elasticity, scale, identifiability, threshold-measure, source-input, and solver
ledgers exist; novelty is decided; all predicates, imports, dependencies,
cycles, and consumers are audited; every physical ceiling is explicit;
canonical state agrees; validation is mutation-sensitive; and the debt ledger
is empty. A passing source solve, a free parameter, or a selected one-eV window
does not complete the campaign alone.
