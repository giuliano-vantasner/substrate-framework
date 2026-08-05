---
description: Audit SC1 and construct an exact Gordon scalar-source compatibility locus
author: vantasner
created: '2026-08-11T06:15:00Z'
updated: '2026-08-11T06:51:00Z'
tags:
- substrate-framework
- campaign-proposal
- migration-SC1
- gordon-metric
- source-compatibility
category: proposals
confidence: established
status: archived
---
# P178 SC1 Gordon Source-Compatibility Audit

## Question and Positive Deliverable

P178 must determine whether hash-pinned SC1 correctly closes the Gordon
sourcing channel it tests. The positive deliverable is an exact, reusable
compatibility-locus theorem or classifier that decides when the accepted
transverse Gordon Einstein tensor and a declared scalar stress obey one
componentwise Einstein coupling, including zero-component support, coupling
uniqueness, conservation, matter equations, domains, and countermodels. A
stress mismatch or no-go by itself is attempt evidence, not completion.

## Base Release and Provenance

The accepted base is v0.129.0 at clean framework commit `36a9e39`, with 165
accepted claims. The governed source baseline is
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`. SC1 is pending at
`merged-framework/bridges/phase-36/bridge_SC1_gordon_coupled_overdetermined.py`,
SHA-256
`70799bff934f1f6986545a0bde0cb94fe016dd4b468b36614ac3e5d9bb74aec0`.
The target path is clean at the governed baseline and its sole history commit
is `7222eed21720c5174dd35ba8f825d8b7e0a48f3f`. Unrelated newer source-tree
changes have no authority and are excluded.

The generated queue already exposes SC1's broad rank-one-ray conclusion,
selected component ratios, stress-mismatch conclusion, five-check tally, and
part of its result synopsis. P178 therefore claims no fresh conclusion or
comparator blinding. The exact source body, check literals, intermediate
expressions, and runtime output remain unopened until this contract validates
and is committed.

## Invariants, Conventions, and Allowed Imports

C-GOR-001 fixes the exact mostly-plus Gordon metric and, for uniform z flow
with transverse index `n(x)`, the full covariant Einstein tensor. It explicitly
supplies no material action, stress match, coupling, boundary-value solution,
physical gravity, observation, or substrate realization. C-STG-001 fixes the
canonical four-dimensional scalar stress, Einstein-scalar equations, on-shell
conservation identity, and one homogeneous FLRW solution, but no scalar-to-
index or breather-to-Gordon map.

C-SG-012 governs normalized one-plus-one sine-Gordon stress only. A four-
dimensional source requires an explicit transverse embedding, units, support,
and boundary data. C-LIN-001 already owns exact finite linear-system rank,
consistency, nullity, duplicate-row, and equation-count distinctions. P178
must not rename generic proportionality as new physics. C-GRV-001 may be used
only for coupling-dimension and free-normalization ceilings.

All tensors use explicit signature, coordinate order, index placement, and
domains. `G_ab=kappa*T_ab` requires every independent component, including
zeros, to agree with one declared coupling; it also requires a compatible
conserved stress, matter equation, coupling sign and dimension, and boundary
data. Neither a nonzero `G_ab` nor one fitted ratio closes the system.

Mutable numerical code uses `np.trapezoid` or `trapezoid_integral`. The
preflight checks direct, imported, dynamic, and eager-default legacy access.
Immutable hash-pinned source receives an isolated alias backed by
`np.trapezoid` only if needed; a version-only abort cannot reject a scientific
candidate.

## Candidate Preregistration

Seven candidates separate literal reproduction, accepted coverage, generic
linear algebra, the domain-specific Gordon-scalar locus, the source's
one-plus-one embedding, a constructive matter alternative, and governance.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal SC1 replay | Hash-pinned source environment | Source literals | Evidence only until audited | AST, native/compatibility execution, predicate and dataflow inventory |
| B | Accepted composition | C-GOR-001, C-STG-001, C-SG-012, C-LIN-001 | None new | May own all valid SC1 content | Exact statement, API, evidence, and consumer comparison |
| C | Generic tensor proportionality certificate | Exact symmetric tensors | One scalar multiplier | Likely duplicate of C-LIN-001 unless a distinct API surface survives | Rank, support, minors, zero and inconsistent controls |
| D | Exact Gordon-canonical-scalar compatibility locus | Accepted Gordon metric and declared four-dimensional scalar action | Gradient, potential, coupling, index profile and boost | Strongest domain-specific positive object | Solve every component plus scalar and conservation conditions exactly |
| E | One-plus-one sine-Gordon embedding audit | Explicit transverse embedding and units | Profile, support, normalization | Expected to expose missing premises | Component, conservation, transverse-energy, rest and flat limits |
| F | Constructive anisotropic matter source | Separately declared action and conserved stress | Only action-owned parameters | Admissible only without defining stress backward from geometry | Variation, conservation, full component match, boundary solution |
| G | Governance closure | Claim-level review | None | Required | Dependency, consumer, disposition, release, docs, memory, debt replay |

## Selection Criteria and Blinding

Selection is ordered by accepted metric, stress, signature, component, and
index compatibility; exact closure of every component and zero-support case;
declared matter action, scalar equation, conservation, domain, and boundary
data; separation of one-plus-one per-area from localized four-dimensional
sources; coupling sign, dimensions, assumptions, and parameter economy; known
flat, rest, constant-index, on-shell, and wrong-convention limits; novelty
beyond C-LIN-001; mutation sensitivity; consumer reach; and physical-scope
honesty. Exposed source conclusions cannot select a concept or tolerance.

## Proposed Claim Delta

The source-aware revision provisionally reserves C-GOR-002 after direct
registry, campaign, and durable-memory searches found no collision. C-LIN-001
already imposes a strong generic-rank novelty ceiling, so the proposed delta is
not a generic proportionality result. It is the domain-specific exact
compatibility locus for the accepted C-GOR-001 tensor and C-STG-001 stress.

For a positive `n(x)`, uniform subluminal z boost, real canonical scalar
`U(t,x)`, real potential value `V`, and positive coupling, the proposed theorem
states that the componentwise Einstein equations hold exactly only when
`U_t=U_x=V=K=0`, where
`K=(n*n_xx-2*n_x^2)/n^2`. Conversely those conditions make both tensors zero.
For nonzero boost, a source-derived 3-by-3 component minor is
`8*n^2*v^2*(v^2-1)^5`, hence nonzero on the declared domain. At rest, the zero
`tt` and `xx` equations give `n^2*U_t^2+U_x^2+2V=0` and
`n^2*U_t^2+U_x^2-2V=0`; real-square nonnegativity closes the remaining branch.
Finally `K=0` is equivalent to `(1/n)_xx=0`, so the positive reciprocal index
is affine on each connected interval. A normalized `1-cos(U)` specialization
is an on-shell vacuum, not a four-dimensional breather derivation.

SC1's disposition is the immediate consumer. G2 and G3 remain qualified only
through C-GOR-001 and C-STG-001, and cannot gain blanket authority. Every
reverse consumer found after freeze must retain its current claim ceiling
unless independently replayed and reviewed.

## Implementation and Oracle Plan

The source audit will inventory every SC1 definition, import, literal,
predicate, assertion, tensor component, stress construction, coupling solve,
dependency, result sentence, and NumPy compatibility surface. SymPy is the
strongest practical oracle for exact tensor support, component minors,
coupling consistency, gradient and potential elimination, special limits, and
mutations. Numerical reruns of exact algebra count only as regression.

Candidate D will live in a pure package API and consume the
accepted Gordon and scalar-stress constructors rather than copying them. It
must distinguish a compatible nonzero locus, a trivial flat locus, an
inconsistent locus with an explicit component certificate, and cases where a
coupling is free because both tensors vanish. It must not divide by a component
before proving it nonzero. The scalar Euler equation and stress conservation
are separate from algebraic proportionality.

Load-bearing mutations change metric signature, covariant versus
contravariant Gordon convention, boost sign, curvature kernel, zero `G_xx`,
stress index placement, scalar gradient direction, potential sign, coupling
sign, fitted single component, transverse embedding, and on-shell condition.
Independent review will reconstruct the relevant tensor equations without
importing a proposed compatibility helper. Flat index, rest boost, constant
index, zero stress, proportional synthetic stress, inconsistent zero support,
wrong sign, and off-shell scalar data are required controls.

The source-aware revision also permits one narrow repair to the accepted
Gordon constructor: simplify `1-v^2` before asking SymPy whether the margin is
positive. This preserves every rejected numeric and superluminal input while
admitting exact symbolic subluminal parameterizations such as
`v=r/sqrt(1+r^2)`. GitNexus rates the indexed blast radius LOW with no callers
or processes; direct inspection adds the focused Gordon tests and P142
verifier as the actual regression surface.

The dependency graph will start with G2, G3, SC1, their accepted canonical
modules, and every direct import and reverse consumer discovered after freeze.
Lexical check sites, runtime checks, and assertions remain separate counts.
Immutable NumPy compatibility is replayed only by an explicit alias backed by
`np.trapezoid` and cannot become a scientific verdict.

## Attempts and Continuation

Attempt 0001 freezes v0.129.0, commit `36a9e39`, source hash and history,
prior result exposure, accepted ceilings, seven competing candidates,
selection criteria, empty initial claim delta, exact oracle, mutation plan,
and compatibility policy before opening SC1's body. Attempts 0002 through
0004 repair a source-audit path invocation and establish native five-check
reproduction with authority gaps. Attempt 0005 derives the provisional exact
locus. Attempt 0006 preserves a symbolic-domain guard failure; attempt 0007
records the source-aware proposal revision and LOW impact result. Attempts
0008 and 0009 preserve then repair three test-representation and domain
failures. Attempts 0010 through 0012 preserve progressively narrower primary-
oracle representation failures before attempt 0013 passes all 35 checks.
Attempts 0014 and 0015 pass the 14-check independent derivation and 21-check
source graph. Attempt 0016 records the impact analysis; attempt 0017 passes 53
focused tests, the 29-check historical verifier, both exact P178 routes,
compilation, and diff hygiene. Attempts 0018 and 0019 make the graph oracle
replay-safe and pass it before and after the exact SC1 qualification without
granting SC2 authority. No failed route was converted into a scientific
verdict, and no unchanged full suite was repeated.

## Debt Ledger

The P178 ledger tracks source reachability, convention fidelity, stress
embedding, algebraic and dynamical closure, novelty, dependencies, consumers,
compatibility, and governed state.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| SC1's exact implementation and predicate reach are unknown | Pin every definition, check, assertion, import, tensor, and runtime result | discharged: five predicates, one assertion, all objects, outputs, and prose inventoried |
| The source stress may mix one-plus-one and four-dimensional conventions | Trace dimensions, embedding, support, index placement, and conservation | discharged: wrong potential sign and missing four-dimensional premises isolated |
| One fitted coupling may hide inconsistent zero or nonzero components | Solve all independent component equations without unsafe division | discharged: nonzero and rest branches close every covariant component |
| Algebraic proportionality may be mistaken for a sourced solution | Check matter equation, conservation, action, domain, and boundary data separately | discharged: accepted claim is explicitly local and algebraic with dynamical ceiling |
| A generic classifier may duplicate C-LIN-001 | Compare exact statements, APIs, assumptions, evidence, and consumers | discharged: generic candidate rejected; domain-specific iff locus is novel |
| A backward-defined effective stress may masquerade as matter | Require a separately declared action or reject the route | discharged: no effective stress was defined backward from geometry |
| Dependencies and reverse consumers may inherit blanket authority | Inventory and replay the complete affected graph | discharged: exact SC1 qualification passes while SC2 stays pending and unmapped |
| Legacy NumPy access may masquerade as science | Preflight and alias-replay immutable compatibility failures | discharged: all four nodes are native with no integration-name event |
| Governed records may disagree | Synchronize disposition, queue, memory, effort, claim and release state | discharged: v0.130.0, 166 claims, SC1 qualification, docs and memory agree |

## Review and Promotion Record

Every SC1 predicate received an individual verdict. Gordon geometry, scalar
stress, tensor proportionality, scalar dynamics, conservation, physical
interpretation, and result prose received separate statuses. The exact theorem
was independently rederived from raw artifacts, extracted into a pure tested
API, replayed through consumers, and accepted claim-by-claim as C-GOR-002.
SC1 is qualified through C-GOR-001, C-STG-001, and C-GOR-002; SC2 remains
pending.

The transaction edited `migration/dispositions.yaml` and regenerated the
queue, generated docs, and accepted memory. Every registered evidence path was
materialized first. Targeted scientific routes ran before the one integrated
`scripts/validate.sh`; record-only closure is checked narrowly without
repeating the full suite. Validation and commit remain separate invocations.

## Done Gate

The positive exact compatibility locus exists as C-GOR-002, every source
predicate and component is adjudicated, matter and conservation ceilings are
explicit, dependencies and consumers replay, compatibility is classified,
governed records agree, and the debt ledger is empty. The campaign closes on
the positive iff object and synchronized authority—not on SC1's mismatch. The
single integrated boundary validates 715 memory records and passes all 1,514
repository tests.

## Cross-References

See C-GOR-001, C-STG-001, C-SG-012, C-LIN-001, C-GRV-001, P142, P143, G2,
G3, SC1, `gordon_metric.py`, `einstein_scalar.py`, `sine_gordon.py`, and the
framework-migration effort.
