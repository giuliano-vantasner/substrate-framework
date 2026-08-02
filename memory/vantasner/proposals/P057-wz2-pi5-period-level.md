---
description: Certify an SU3 pi5 generator period and conditional WZW level theorem
author: vantasner
created: '2026-08-02T15:30:00Z'
updated: '2026-08-02T16:00:00Z'
tags:
- substrate-framework
- campaign-proposal
- su3-periods
- migration-WZ2
category: proposals
confidence: established
status: archived
---
# P057 WZ2 SU(3) Generator Period and Level Audit

## Question and Positive Deliverable

P057 must produce the strongest positive, reusable normalization theorem for
C-WZW-001's real SU(3) trace-five form. The target is a globally defined smooth
map representing a certified primitive class, its oriented trace-five period
with exact or converged normalization, and the consequent conditional
extension-phase coefficient lattice. A numerically close integer, a failed
source map, or a restatement of `pi_5(SU(3))=Z` does not complete the campaign;
another registered construction must continue.

## Base Release and Provenance

The accepted base is `v0.50.0` at framework commit `d358ed4`, whose scientific
transaction is `23484eb`. The pinned source is `substrate@6d1f4e0`; WZ2 is at
`/home/dan/substrate/merged-framework/bridges/phase-17/bridge_WZ2_level_quantization_pi5.py`
with verified SHA-256
`f991e222f038268077d3f50e759beeec95ac65f06a8369011ecc0e0ad79ce3ff`.
WZ1 is qualified and maps only to accepted C-WZW-001. S3 is pending and is
navigation evidence, so its imported WZW term, representation selection, and
integer `N_c` statements are unavailable. Memory points only to P056's explicit
period debt and the parent WZ2 next action; it contains no accepted normalized
period or generator. The first preflight shorthand `scripts/preflight.sh` was
not present; the canonical skill-local preflight then passed seven checks with
no warnings. WZ2's executable and reported values remain unopened while this
contract is frozen.

## Invariants, Conventions, and Allowed Imports

C-WZW-001 defines `Omega5=-i Alt Tr(theta^5)` in the basis `E_a=iT_a`, with
`T_a=lambda_a/2` and no hidden `1/5!`. Its exact cohomology proves that the form
is closed and globally non-exact but leaves its period lattice unspecified.
P057 must preserve the explicit factor of `-i`, every generator-scale power,
the pullback orientation, and the distinction between an unnormalized
alternating component and a differential-form coordinate density.

Allowed standard mathematics includes smooth pullback and degree theory,
oriented change of variables, Stokes, and exact sphere-volume or beta-function
integrals derived in the campaign. The principal fibration
`SU(2)->SU(3)->S^5` and its long exact sequence may enter only after their exact
statements and primary-source provenance are audited. In particular, a
projection-degree criterion must be independent of the WZW integral. No
reported unit period, Witten coefficient, `N_c`, baryon charge, anomaly
coefficient, or representation table is permitted as a derivation input.

## Candidate Preregistration

The candidate set is frozen from accepted authority and WZ2 queue metadata
before the source implementation or any reported period is inspected.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal WZ2 reproduction | Every map, topology fact, measure, cutoff, and normalization must be traced | Source constants and numerical controls | May reproduce a tally but can fail generator, coverage, or convergence obligations | Hash-pinned run, data-flow audit, map mutations, and independent topology check |
| B | Direct source-map certification | Smooth global S5 domain and explicit SU(3) map | Declared chart and quadrature controls | Succeeds only if the map has full five-dimensional pullback rank and a noncircular generator invariant | Exact unitarity/determinant/seam checks, projection degree or clutching class, density refinement, and orientation reversal |
| C | Fibration/transgression generator route | Audited SU2-SU3-S5 fibration and exact-sequence inputs | No fitted scale | Supplies an independent primitive-class criterion and may reduce the period to exact sphere integrals | Projection degree, chart gluing, exact normalization reduction, and separate numerical regression |
| D | Symbolic phase-lattice theorem | Primitive period supplied as a declared theorem | Symbolic period and coefficient | Gives exact coefficient quantization but no period or physical level by itself | Integer/noninteger phase mutations and orientation/multiple-cover limits |

## Selection Criteria and Blinding

Selection is ordered by noncircular generator certification, global map and
orientation closure, exact compatibility with C-WZW-001, absence of fitted
normalization, converged integration with explicit error, independent topology
and integration routes, sensitive degree/coverage/convention mutations, and
minimal audited imports. The source's period, convergence table, level, and
`N_c` values cannot select a map. The comparator gate opens only after the map
class, generator invariant, orientation, density, measure, error gates, and
interpretation ceiling are frozen here and in the manifest.

## Proposed Claim Delta

Provisional `C-WZW-002` may state the primitive oriented period of the exact
real form from C-WZW-001 if a generator is certified independently and the
normalization is derived without fitting. It may then state the exact
conditional coefficient lattice for filling-independent phases over integer
multiples of that primitive cycle. It cannot equate the coefficient to `N_c`,
derive a physical WZW action, select SU(3) representations, identify baryon
number, or establish anomaly matching.

Direct consumers are WZ2 and later WZ3/WZ4 units that cite its generator,
period, level, or `N_c` language. C-WZW-001 remains unchanged and supplies
only the closed non-exact form and conditional gluing algebra. S3 remains
pending regardless of whether the mathematical period theorem succeeds.

## Implementation and Oracle Plan

A canonical pure module may add a globally explicit generator map or audited
chart representation, its exact SU(3) membership and differential, pullback
density, topological-class witness, and normalized period/phase helpers. It
must perform no integration or printing at import. Exact SymPy algebra fits
unitarity, determinant, seam, Jacobian, orientation, and any tractable
symmetry-reduced integral. A numerical integral earns only numeric evidence
and must specify the domain/atlas, coordinate singularities, measure,
precision, deterministic cubature or quasi-Monte-Carlo method, mesh or sample
sequence, stopping status, scale-relative error, and independent method.

The topology oracle cannot be the trace-five integral under review. Preferred
independent evidence is the degree of the last-column projection under the
audited `SU(2)->SU(3)->S^5` exact sequence or equivalent clutching data. A
piecewise map must prove seam compatibility and account for null or singular
sets. Load-bearing mutations reverse orientation, compose with degree zero or
multiple covers, rescale generators, remove `-i`, truncate a chart, perturb
unitarity or determinant, and replace an integer-compatible coefficient by a
half-integer. Each relevant verdict must fail.

## Attempts and Continuation

Three append-only attempts complete P057. Attempt 0001 reproduces WZ2's clean
eight-check tally but rejects Candidate A: its map has determinant `exp(iF)`,
its suspension of `CP2` is not `S5`, its generator witness is circular, and its
doubling is literal multiplication. Attempt 0002 selects Candidate C and
passes exact SU(3) membership, two-preimage degree `+2`, tangent density
`-480`, primitive period `-480*pi^3`, and coefficient step
`1/(240*pi^2)`. Attempt 0003 independently reimplements the map, demonstrates
second-order finite-difference refinement, and converges a five-dimensional
Gauss-Legendre cubature to the exact period with final relative error
`0.0005120`. Candidate D supplies the exact conditional phase algebra after C
closes the period; no physical identification is added.

## Debt Ledger

This ledger tracks source provenance, map topology, global smoothness,
orientation, pullback normalization, numerical integration, phase algebra,
physical interpretation, independent evidence, consumers, and canonical
synchronization.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| WZ2's literal implementation, dependencies, map, environment behavior, and tally are unaudited | Hash-check, execute, trace every input and preserve output or failure | discharged by attempt 0001 and source reproduction |
| The proposed map may fail SU(3) membership, global smoothness, seam closure, or full five-dimensional rank | Exact membership and derivative checks on every chart plus singular/seam analysis | discharged by rejecting WZ2's U(3) map and replacing it with the global Puttmann-Rigas embedding |
| A near-unit WZW integral may circularly label its own cycle a generator | Establish degree or clutching class independently of the trace-five integral | discharged by the two-preimage degree +2 calculation and audited generator theorem |
| The anti-Hermitian, alternating, orientation, and action conventions may hide factors of i, factorials, pi, or covering number | Derive conversions exactly and pass rescaling, orientation, and multiple-cover mutations | discharged by exact density/period algebra and load-bearing mutations |
| Numerical integration may omit a measure, chart, singular region, error model, or convergence dimension | Record the complete method and demonstrate refinement plus an independent route | discharged by attempt 0003's five-coordinate finite-difference cubature and exact symmetry route |
| `pi_5(SU(3))=Z` or fibration facts may be imported without precise provenance | Audit exact primary-source statements and isolate them as declared mathematical imports | discharged by topology-provenance.yaml and independent degree reproduction |
| Integer phase algebra may be mislabeled a derived physical WZW level or N_c | Keep the coefficient symbolic and exclude physical identifications absent separate evidence | discharged by the mathematical sphere-filling ceiling in C-WZW-002 |
| Independent evidence and downstream replay are absent | Complete distinct topology/integration evidence, focused tests, impact analysis, and consumer replay | discharged by attempts 0002/0003, LOW API impact, and focused replay |
| Registry, release, generated docs, migration queue, and durable memory are unsynchronized | Review claim by claim, adjudicate WZ2, regenerate canonical consumers, and empty this ledger | discharged by v0.51.0 and generated synchronization |

## Review and Promotion Plan

Each map, topology, period, phase, and interpretation subclaim receives
separate verification, review, compatibility, and epistemic axes. An
independent reviewer must inspect the global map, generator criterion,
normalization, convergence, and mutations without inheriting the source's
reported period. Accepted reusable logic moves under `src/substrate_framework/`
with tests. WZ2 receives a terminal structured disposition in
`migration/dispositions.yaml`, with every unproved topology or physical
subclaim retained. Promotion requires a pinned release if a claim is accepted,
rendered docs/memory, affected-consumer replay, one final
`scripts/validate.sh`, explicit required pytest, and `git diff --check`.

## Done Gate

P057 is accepted in v0.51.0. The explicit primitive map, independent degree
witness, exact oriented period, conditional coefficient lattice, numerical
refinement, sensitive mutations, qualified WZ2 disposition, generated
records, focused consumers, and empty debt ledger pass. The result remains
strictly mathematical and sphere-filling scoped. The parent migration remains
active and advances to WZ3.
