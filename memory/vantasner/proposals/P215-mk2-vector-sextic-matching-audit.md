---
description: Audit MK2 vector-current elimination and BPS sextic-coupling closure
author: vantasner
created: '2026-08-06T10:01:44Z'
updated: '2026-08-06T10:25:00Z'
tags:
- substrate-framework
- campaign-proposal
- migration-MK2
- vector-elimination
- bps-sextic
category: proposals
confidence: exploratory
status: active
---
# P215 MK2 Vector Sextic Matching Audit

## Question and Positive Deliverable

P215 must derive the exact squared-current coefficient obtained by eliminating
a declared massive isoscalar vector, convert it into the accepted BPS-Skyrme
convention, and decide whether accepted framework claims independently supply
the vector mass, coupling, current, HLS metric, and physical field map. The
positive deliverable is a convention-complete elimination and identifiability
ledger, a claim-level adjudication of every MK2 predicate, and a terminal MK2
disposition. Finding an unsupported physical closure does not itself complete
the campaign.

## Base Release and Provenance

The accepted base is v0.155.0 at clean framework commit `ecee9d5`, with 197
accepted claims, 10 pending units, and 195 qualified units. MK2 is pinned at
source commit `6d1f4e0`, SHA-256 `351136bc...eb07`, and 22,413 bytes. Its
candidate dependencies are KI1, KI2, MK1, S4, WZ2, WZ3, and WZ4 at their
registered dispositions. KI1 is refuted, MK1 is qualified without its physical
medium map, and later MK/MR units grant no authority. The source checkout is
dirty outside the hash-pinned MK2 file, so unrelated newer prose and edits are
excluded.

The generated queue exposes seven literal check sites, one assertion, and
truncated claims about a low-momentum vector elimination, a fundamental U(2)
trace metric, and omega-rho mass equality. Earlier governed inventory evidence
also exposes the proposed `lambda_A=N_c/(4*F_pi)`. The source body, remaining
equations, parameter values, predicates, guards, imports, output, and consumer
details stay unopened through this contract and freeze.

## Invariants, Conventions, and Allowed Imports

C-EFT-001 already owns exact stationary elimination of a declared quadratic
kernel and explicitly distinguishes a finite derivative expansion from an
exact inverse. C-BPS-001 uses sextic density
`lambda_BPS^2*pi^4*B0^2`, takes `lambda_BPS` and `B0` as supplied, and derives
no physical baryon or vector sector. C-VEC-001 owns a conditional leading SU(2)
HLS connection result but no singlet omega, physical rho, KSRF theorem, baryon
current, `N_c`, or substrate map. C-WZW-001 and C-WZW-002 are mathematical
five-form and level theorems without those physical identifications.

The source convention `-lambda_A^2*B_mu*B^mu` equals C-BPS-001's convention
only when `lambda_A=pi^2*lambda_BPS`. A chosen fundamental trace metric is
declared action data, not a consequence of writing `U(2)`: the reductive
algebra admits the additional invariant `Tr(X)*Tr(Y)`, which changes the
singlet coefficient without breaking U(2) invariance. Mutable integration uses
`np.trapezoid` or `trapezoid_integral`; an immutable version-only abort receives
an alias-only replay and never becomes a scientific failure.

## Candidate Preregistration

Nine candidates separate algebraic elimination, the full kinetic inverse,
BPS conventions, invariant metrics, conditional physical relations,
identifiability, possible API novelty, accepted composition, and governance.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Algebraic Proca-current elimination | Declared mass term, source sign, and supplied current | positive `m_omega`, real `g_omega` | `lambda_A=abs(g_omega)/(sqrt(2)*m_omega)` | Exact variation, substitution, sign and normalization mutations |
| B | Full kinetic-vector inverse | Declared differential kernel and low-q counting | `m_omega` plus derivative operator | Local `B^2` is leading order, not the exact full inverse | Exact finite inverse residual and a nonzero-derivative counterexample |
| C | BPS convention conversion | Same normalized topological current | `lambda_A`, `lambda_BPS` | `lambda_A=pi^2*lambda_BPS` | Equate the two sextic densities and mutate the pi factor |
| D | General U(2) invariant metric | Adjoint-invariant real quadratic forms | independent triplet and singlet coefficients | U(2) alone does not force mass degeneracy | Add `b*Tr(X)*Tr(Y)` and verify unequal positive coefficients |
| E | Conditional HLS/KSRF/anomaly composition | Every action, current, representation, and coefficient premise declared | `g,m,F,a,N_c` as applicable | No physical relation survives premise removal unless accepted dependencies supply it | Dependency audit plus generator and coupling mutations |
| F | Positive identifiability families | Fixed accepted SU(2) data | free singlet mass and coupling | The ratio and the pair remain underdetermined absent a new singlet theorem | Construct same-data/different-ratio and same-ratio/different-pair families |
| G | Novel reusable API | Exact survivor beyond accepted generic elimination | minimal exact inputs | Extraction only for a distinct theorem | Registry, module, and memory nonduplication audit |
| H | Accepted composition | Existing exact claims and explicit convention map | none beyond declared symbols | Add no claim if every survivor is already owned | Claim-by-claim overlap comparison |
| I | Terminal MK2 governance | Accepted predecessors only | none | MK2 closes without later authority | Graph, consumer, registry, release, and memory replay |

## Selection Criteria and Blinding

Selection prioritizes exact field, source, metric, sign, generator, current, and
BPS convention typing; accepted dependency closure; assumption economy; local
versus nonlocal scope; the complete U(2)-invariant quadratic-form family;
dimensions, positivity, symmetries, limits, and identifiability; sensitivity to
source, current, singlet-metric, coupling, mass, and pi-squared mutations;
novelty; and terminal consumer closure. Numerical agreement with particle or
decay-scale comparators cannot select a candidate.

## Proposed Claim Delta

P215 provisionally reserves C-VEC-002 for a massive-vector current-matching
theorem if a nonduplication audit finds a novel exact surface. The identifier
has no pre-P215 registry, campaign, proposal, memory, package, test, generated
documentation, or migration hit. Candidate H is preferred if C-EFT-001 and
existing convention claims already own every exact survivor; in that case
C-VEC-002 remains reserved and unpromoted.

## Implementation and Oracle Plan

SymPy will vary and substitute the algebraic vector model, compare it with a
nonzero derivative kernel, solve both sextic-coupling conventions, and test the
full U(2)-invariant quadratic-form family. Exact countermodels vary the singlet
metric, mass, coupling, current normalization, source sign, and BPS pi factor.
The identifiability oracle constructs both fixed-ratio/different-pair and
fixed-SU2-data/different-singlet-ratio families.

The compatibility preflight scans MK2 and every direct, imported, dynamic, and
eagerly accessed executable dependency for legacy NumPy integration names
before native execution. Mutable consumers are repaired to `np.trapezoid` or
the canonical `trapezoid_integral`; immutable source receives an alias-only
recorded replay if needed. Exact accepted algebra remains the scientific
oracle; native output is reproduction evidence.

## Attempts and Continuation

Attempt 0001 freezes the authority boundary, nine candidates, algebraic and
full-inverse distinction, BPS convention conversion, U(2) invariant-form
countermodel, identifiability families, dependency firewalls, mutations,
compatibility policy, and provisional identifier before source-body
inspection. Any failed physical closure redirects the campaign to the exact
conditional object and terminal adjudication rather than ending the effort.

Attempt 0002 preserves the freeze commit stopping on four trailing YAML EOF
blank lines. The repair removes only those blank lines and reruns diff hygiene;
it changes no formula, candidate, premise, threshold, or scientific state.

Attempt 0003 finds no direct NumPy integration surface and reproduces all
seven MK2 checks natively in 0.49 seconds. The exact algebraic match and
single-trace specialization survive, while the full kinetic inverse, general
U(2) metric, accepted BPS convention, and dependency audit expose the
headline's missing premises.

Attempt 0004 preserves the independent verifier stopping immediately because
its eliminated vector had been declared positive, excluding the negative
stationary solution. Restricting positivity to mass and coupling repairs the
symbol domain without changing the frozen action.

Attempt 0005 preserves the repaired independent route reaching fourteen
checks before a brittle registry check searched the claim statement for a
KSRF ceiling stored in its assumptions. The corrected oracle requires both
authoritative locations and changes no scientific result.

Attempt 0006 completes twenty-nine primary and fifteen fresh independent exact
checks. The fifteen-node source graph pins 107 predicates and 17 assertions;
fourteen nonrefuted nodes replay cleanly, KI1 alone stops at its governed
refutation, and immutable WZ3 receives an alias-only `np.trapezoid` replay.
C-VEC-002 is selected for the novel invariant-metric and convention surface.

Attempt 0007 preserves two predecessor CLI usage stops caused by omitted
required evidence arguments. After re-sourcing their adjudication commands,
eighty focused tests, twenty-five P059 primary, twenty-three P059 independent,
thirty-six P140 primary, twenty-five P140 independent, twenty-nine P215
primary, and fifteen P215 independent checks pass.

## Debt Ledger

The P215 ledger tracks vector and current field types, kernel and source signs,
low-q scope, generator and trace conventions, singlet versus triplet metrics,
mass and coupling identifiability, BPS convention conversion, HLS/KSRF/anomaly
premises, physical ontology, pending authority, compatibility, consumers, and
generated state.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| MK2 predicates remain blinded | Reproduce once after committed freeze | discharged by attempt 0003 |
| Algebraic and kinetic elimination may be conflated | Compare exact kernels and finite inverse residuals | discharged by attempts 0006 and 0007 |
| U(2) may be mistaken for a unique trace metric | Classify invariant forms and test a positive unequal-mass countermodel | discharged by attempts 0006 and 0007 |
| Source and accepted BPS lambdas differ by convention | Verify `lambda_A=pi^2*lambda_BPS` through every consumer | discharged by attempts 0006 and 0007 |
| A ratio may be presented as two derived parameters | Construct exact identifiability families | discharged by attempt 0006 |
| Inserted HLS, KSRF, `N_c`, baryon, or physical maps may propagate circularly | Audit every dependency and premise-removal mutation | discharged by attempts 0006 and 0007 |
| Later units may grant backward authority | Replay the terminal graph without later imports | discharged by attempt 0006 |
| Compatibility may masquerade as science | Audit every executable integration-name access before native replay | discharged by attempts 0003 and 0006 |
| Claim novelty and generated state remain unresolved | Complete nonduplication, review, disposition, generation, and proper closeout gate | open |

## Review and Promotion Plan

Every MK2 predicate receives an individual verdict. A novel theorem requires
canonical code and tests, primary and independent exact routes, claim review,
impact analysis, registry and release updates, generated documentation,
synchronized memory, and one integrated promotion gate. If no claim changes,
MK2 still requires materialized evidence, terminal disposition, consumer
replay, and record-sensitive validation without repeating an unchanged full
suite.

## Done Gate

P215 closes only when the exact positive elimination and convention ledger,
mutation-sensitive primary and independent verification, every MK2 predicate,
terminal disposition, downstream replay, compatibility audit, canonical
records, and generated state agree with an empty campaign debt ledger.

## Cross-References

This contract links v0.155.0, C-EFT-001, C-BPS-001 through C-BPS-003,
C-VEC-001, C-CHI-001, C-CHI-002, C-WZW-001, C-WZW-002, C-TOP-002,
C-ANO-001, P059, P107, P140, P171, P214, KI1, KI2, MK1, MK2, S4, WZ2,
WZ3, WZ4, the proposal manifest, formula freeze, provenance record, future
verifiers and review, migration registry, generated documentation, and durable
framework-migration effort memory.
