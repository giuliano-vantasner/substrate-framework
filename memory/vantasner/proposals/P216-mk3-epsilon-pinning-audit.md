---
description: Audit MK3 scale-product epsilon pinning and dependency closure
author: vantasner
created: '2026-08-06T10:35:36Z'
updated: '2026-08-06T10:35:36Z'
tags:
- substrate-framework
- campaign-proposal
- migration-MK3
- epsilon-identifiability
category: proposals
confidence: exploratory
status: active
---
# P216 MK3 Epsilon Pinning Audit

## Question and Positive Deliverable

P216 must determine whether MK3 derives a dependency-closed value of its
locally defined dimensionless epsilon or only a conditional quotient of a
supplied standard-sector scale and a supplied BPS coupling product. The
positive deliverable is an exact definition, convention, input-provenance,
normalization, identifiability, and physical-ontology ledger; an unsupported
pinning claim or green source tally does not complete the campaign.

## Base Release and Provenance

The accepted base is v0.156.0 at clean framework commit `1514755`, with 198
accepted claims, nine pending units, and 196 qualified units. MK3 is pinned at
source commit `6d1f4e0`, SHA-256 `64254d0f...16404`, and 19,470 bytes. The
pinned file is clean while the source checkout has unrelated newer Phase-47,
Phase-48, engineering, and memory work, all excluded from authority.

The generated queue exposes six literal check sites, one assertion, and the
identities `epsilon=(F_pi/e)/(lambda*mu)`, the claimed source product
`lambda*mu=N_c*m_pi/8`, and the conditional NY1 scale
`F_pi/e=16*pi*E_e`. It names B1, E3, E4, HE4, KI2, KI4, MK1, MK2, MK6, and
NY1 as candidate dependencies. MK6 remains pending; the other source units
confer only their governed accepted mappings. The remaining source equations,
values, predicates, guards, imports, output, comparator residuals, and consumer
details stay unopened through this contract and freeze.

## Invariants, Conventions, and Allowed Imports

C-BPS-001 declares positive `lambda_BPS` and `mu` as inputs and uses sextic
density `lambda_BPS^2*pi^4*B0^2`. KI2's local monomial is not identified with
C-BPS-003's abstract expansion coordinate, and its simultaneous coupling flow
changes rather than preserves a fixed accepted BPS theory. C-VEC-002 requires
`lambda_A=pi^2*lambda_BPS` between the MK2 source convention and the accepted
BPS convention.

MK1 supplies no accepted physical `mu`, pion, decay scale, or medium-to-BPS
map. MK2 supplies no accepted physical HLS field, omega, baryon current,
`N_c`, KSRF relation, `F_pi`, mass, coupling, or product. NY1 duplicates
C-SK-001's conditional iff between two supplied mass formulas and retains the
empirical electron rest energy. A positive scale and product determine their
quotient only conditionally. Mutable integration uses `np.trapezoid` or
`trapezoid_integral`; immutable legacy-name stops are compatibility provenance,
never scientific failure.

## Candidate Preregistration

Nine candidates separate exact definition algebra, sufficient conditional
inputs, convention conversion, Skyrme-scale composition, accepted-family
countermodels, epsilon typing, physical provenance, novelty, and governance.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Exact local quotient | Four supplied positive inputs | `F_pi,e,lambda_BPS,mu` | Identity survives as a definition | Exact reduction and exponent mutations |
| B | Scale-product reconstruction | Supplied positive `s` and `p` | `s,p` | `epsilon=s/p` is conditional, not input derivation | Forward and inverse exact algebra |
| C | Accepted BPS convention | Same normalized current across conventions | `lambda_A,lambda_BPS` | Source product gains `1/pi^2`; epsilon gains `pi^2` | Density equality and wrong-convention mutation |
| D | Conditional C-SK-001 scale | Both mass premises and their equality | `B1,E_e,F_pi,e` | Shared B1 cancels but empirical input remains | Premise removal, power, and E_e mutations |
| E | Accepted-family countermodels | C-BPS-001's positive parameter family | Free product and normalization | Every positive local ratio remains realizable | Same-scale/different-product exact families |
| F | Typed epsilon firewall | Explicit definition map required | Local normalization | No map to C-BPS-003 or a physical binding observable | Definition and registry audit |
| G | Physical dependency closure | Every field, current, mass, and coefficient map declared | `N_c,m_pi,F_pi` and vector premises | MK1/MK2 cannot supply the claimed physical value | Premise-removal graph replay |
| H | Novel reusable surface | Distinct theorem and consumers required | Minimal exact inputs | No claim if accepted ledgers own all survivors | Registry, API, and memory nonduplication audit |
| I | Terminal MK3 governance | Accepted predecessors only | None | MK3 closes without later authority | Predicate, consumer, queue, and memory replay |

## Selection Criteria and Blinding

Selection prioritizes definition-versus-derivation typing, accepted dependency
closure, exact BPS convention, parameter and normalization economy, positive
domains and dimensions, product and scale identifiability, sensitivity to
every load-bearing premise, physical field and measure maps, novelty, and
terminal consumer closure. Numerical proximity to a binding, particle, yield,
or phenomenological epsilon comparator cannot select a candidate. Remaining
source values and comparator residuals stay blinded until the committed freeze.

## Proposed Claim Delta

No claim identifier is proposed at freeze. C-BPS-001, C-SK-001, C-VEC-002,
and P172's governed KI2 adjudication appear to own every preexposed exact
survivor. A new claim or API may proceed only if post-source nonduplication
finds a distinct dependency-closed theorem and consumer; otherwise MK3 will
receive a terminal source disposition without changing the accepted release.

## Implementation and Oracle Plan

SymPy is the strongest oracle for the finite monomial reduction, product
substitution, pi-squared convention conversion, arbitrary-target families,
premise removal, and normalization mutations. The primary route will inventory
all six MK3 predicates and its assertion, reproduce native execution after a
direct/imported/dynamic/eager compatibility scan, and classify every formula
against accepted claims. A fresh independent route will derive the quotient,
convention map, and counterfamilies without importing MK3 or the primary
verifier.

The source graph will type accepted mappings separately from source narrative
edges and later consumers. Exact predecessor results will be hash-reused where
the inputs and claims are unchanged; only source-sensitive consumers will be
replayed. Numerical substitution is regression evidence because exact algebra
already fixes its output. No quadrature or solver is justified for this claim.

## Attempts and Continuation

Attempt 0001 freezes the authority boundary, nine candidates, exact quotient,
product sufficiency, BPS convention conversion, C-SK premise ledger,
accepted-family and normalization countermodels, physical firewalls,
compatibility policy, and no expected claim delta before source-body
inspection. Its first record preflight correctly stops on a schema-invalid
manifest status and an unquoted YAML flow scalar. Attempt 0002 repairs only
those record shapes and the verified full base hash; no formula, candidate,
premise, selection criterion, or scientific state changes. If the source's physical closure fails, P216 continues through the
positive exact ledger and terminal adjudication rather than treating the
failure as completion.

Attempt 0003 reproduces all six source checks natively in 0.47 seconds with no
NumPy integration surface. It exposes the load-bearing lambda-convention
error, an unchecked 64-versus-128 prose contradiction, incomplete dependence
and flow guards, and executable reconstruction of the nominally absent 0.929
comparator.

Attempt 0004 preserves a primary-verifier stop after eleven passes on a
misspelled SymPy API before the scientific predicate was evaluated. Attempt
0005 preserves the repaired route reaching twenty passes before a brittle
governed-record wording probe. Requiring the structured dispositions and their
actual convention and physical-ceiling terms changes no scientific result.

Attempt 0006 completes twenty-nine primary exact checks. Even under all source
premises, the accepted BPS convention multiplies the source epsilon by
`pi^2`, moving the exact rational substitution from below one to above one.
No accepted map supplies the product or identifies the quotient with
C-BPS-003 epsilon.

Attempt 0007 completes sixteen fresh independent and nine graph checks plus 61
focused tests. The fifteen-node graph pins 108 predicates and 16 assertions;
MK3 replays freshly, while unchanged expensive later consumers reuse P215's
hash-guarded executions. MK3 has no integration surface, and inherited B1/E3
version shapes remain compatibility provenance only.

## Debt Ledger

The P216 ledger tracks the local definition and normalization, BPS convention,
standard scale, coupling product, every physical input and map, source
predicates, compatibility, consumers, novelty, and generated state.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| MK3 predicates and remaining values remain blinded | Reproduce once after committed freeze | discharged by attempt 0003 |
| Definition may be presented as derived observable | Type every input, normalization, and map | discharged by attempts 0006 and 0007 |
| Source and accepted BPS lambdas may be conflated | Replay the pi-squared conversion through every product and consumer | discharged by attempts 0006 and 0007 |
| MK1/MK2/NY1 rejected readings may grant authority | Remove each physical premise and audit the accepted graph | discharged by attempts 0006 and 0007 |
| Product pinning may be mistaken for individual coupling derivation | Construct exact same-product and different-product families | discharged by attempts 0006 and 0007 |
| KI2 and C-BPS-003 epsilons may be silently identified | Require an explicit definition map or reject the identification | discharged by attempts 0006 and 0007 |
| Later consumers may grant backward authority | Replay the terminal graph without later imports | discharged by attempt 0007 |
| Compatibility may masquerade as science | Audit every executable integration-name access before native replay | discharged by attempts 0003 and 0007 |
| Novelty and governed records remain unresolved | Complete nonduplication, disposition, generation, and closeout | open |

## Review and Promotion Plan

Every MK3 predicate receives an individual verdict. Any novel claim requires
canonical code, tests, primary and independent exact routes, claim-level
review, impact analysis, registry/release updates, generated documentation,
and synchronized memory. If no claim survives, MK3 still requires materialized
evidence, a terminal disposition, consumer replay, and record-sensitive
validation without repeating the unchanged full suite.

## Done Gate

P216 closes only when the positive definition, convention, provenance,
normalization, and identifiability ledger exists; primary and independent
mutation-sensitive verification passes; every MK3 predicate is adjudicated;
downstream and compatibility replay agree; governed records are synchronized;
and the campaign debt ledger is empty.

## Cross-References

This contract links v0.156.0, C-SK-001, C-BPS-001 through C-BPS-003,
C-VEC-002, C-BRK-001, C-CHI-002, C-IDN-002, C-XOV-001, P084, P107, P172,
P174, P214, P215, B1, E3, E4, HE4, KI2, KI4, MK1 through MK6, NY1, the
proposal manifest, formula freeze, provenance record, migration registry, and
durable framework-migration effort memory.
