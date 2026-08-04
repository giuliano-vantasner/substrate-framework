---
description: Audit S4's vector-meson Skyrme-quartic closure claim
author: vantasner
created: '2026-08-09T11:20:00Z'
updated: '2026-08-09T11:20:00Z'
tags:
- substrate-framework
- campaign-proposal
- vector-elimination
- skyrme-quartic
- migration-S4
category: proposals
confidence: exploratory
status: active
---
# P140 S4 Vector-Meson c4 Audit

## Question and Positive Deliverable

P140 must reproduce and adjudicate S4's claim that integrating out a rho
vector closes the Skyrme quartic tensor and coefficient. The positive
deliverable is an importable, convention-explicit theorem deriving the full
quartic tensor, sign, coefficient ledger, and controlled derivative-order
status from a complete declared action. If the physical rho route does not
close, P140 must still construct the strongest distinct conditional vector or
current-wedge object rather than treating a no-go as success.

## Base Release and Provenance

The accepted base is v0.106.0 at scientific commit `9ccd333`; the parent S3
checkpoint is `aa6327b`. S4 is pinned to
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`, path
`merged-framework/bridges/phase-4/bridge_S4_c4_vector_meson_closure.py`, and
SHA-256
`49c7b2392bbe23d2824f4f73030ccd30f245e1750e0c7736dc420d3f64d7a780`.
Its dossier is separately pinned at
`merged-framework/bridges/phase-4/dossiers/S4-dossier.md`, SHA-256
`1680127b0678d8969f7f08da0463ddab10f34e75554d3a842813275868030ed9`.

The generated queue exposes eleven literal checks, one assertion, a symbolic
oracle hint, and declared dependency B1. B1 remains pending and supplies no
authority. Reverse source consumers are S3, WZ1, WZ4, PN6, KI1, KI2, MK2,
MR3, MR4, MR5, and MR6. S3, WZ1, WZ4, and PN6 are already qualified through
accepted surfaces that do not import S4; the remaining consumers are pending.
Queue excerpts have necessarily exposed the claimed tensor ratio, target
coefficient, approximate comparator, propagator sign, KSRF step, and positive
headline. S4's body, check literals, output, and dossier body remain unopened
before freeze.

## Invariants, Conventions, and Allowed Imports

The accepted framework keeps generic elimination, group algebra, and physical
identification separate. C-EFT-001 derives the exact Schur complement only
for a fully declared symmetric invertible kernel and source, and explicitly
withholds HLS fields, vector mesons, KSRF, masses, couplings, operator bases,
and coefficients. C-CHI-001 and C-CHI-002 fix only conditional Pauli trace and
chiral-coordinate conventions. C-LIE-001 fixes an explicit trace convention
without a physical vector sector. C-SK-001 keeps B1 as a positive free
premise; pending B1 grants no value or profile.

The campaign distinguishes four signs: the inverse propagator or propagator,
the stationary reduced action, the induced local operator, and the static
energy. These signs are compared only after fixing metric signature, action
versus energy, field reality, index raising, source coupling, and trace
normalization. A purely algebraic auxiliary field is exact; a kinetic massive
vector generally gives a derivative expansion with a remainder.

Allowed mathematics is exact finite-dimensional variation, Euclidean Gram
and cross-product identities, SU(2) Lie brackets, and formal inverse
expansions. A massive-vector or HLS action may be declared only with every
field, coefficient, sign, generator, and derivative order visible. Primary
literature can check conventions after freeze but cannot import the desired
coefficient as framework authority.

## Candidate Preregistration

Six candidates cover the literal source, auxiliary, kinetic, Lie-algebra,
identifiability, and governance routes.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal S4 reconstruction | Every claimed derivation must be present and exercised | Source symbols only | Algebraic fragments may survive while action or physical closure fails | Hash-pinned execution, AST/data-flow, and eleven-predicate audit |
| B | Exact auxiliary vector/current-wedge reduction | A complete positive or sign-declared quadratic kernel and current-wedge source | Kernel, source coupling, current normalization | Produces an exact Schur complement proportional to the full wedge norm | Stationary equation, direct substitution, completion of square, and sign mutations |
| C | Kinetic massive-vector derivative expansion | A complete kinetic and mass action with declared gauge or connection variables | Mass, kinetic coupling, current coupling, expansion scale | Produces a leading local operator plus controlled higher derivatives, not an exact finite propagator identity | Exact inverse residual, low-momentum limit, next-order term, and independent action substitution |
| D | SU(2) tensor identity | Accepted Pauli trace and one current convention | Current components only | The commutator square is proportional to I1-I2 with convention-dependent trace/sign factors | Pauli-matrix derivation versus independent vector Gram identity and wrong-normalization probes |
| E | KSRF/B1 identifiability ledger | Separately supplied physical dictionary and relations | Mass, coupling, F, B1, field scale | Coefficient agreement remains conditional and changes under omitted normalization inputs | Rescaling, target-as-input, zero-coupling, free-B1, and alternate-KSRF countermodels |
| F | Governance closure | Accepted authority order | None | A distinct reviewed theorem or exact composition terminally qualifies S4 | Novelty, dependency, cycle, consumer, compatibility, release, queue, docs, and memory replay |

## Selection Criteria and Blinding

Selection is ordered by a complete action and metric; accepted trace and
current normalization; actual stationarity and on-shell substitution; exact
auxiliary versus derivative-expansion typing; full I1-I2 tensor derivation;
explicit coefficient and remainder ledger; correct static-energy conversion;
limits and mutation sensitivity; assumption economy; reusable API value;
consumer compatibility; and nonduplication.

The queue has exposed the claimed `beta/alpha=-1`, `c4=8/B1^2`, approximate
5.27 value, propagator sign, KSRF pinning, and conclusion. Those are visible
comparators and may not choose the action, convention, candidate, coefficient,
or thresholds. The complete candidate set and structural tests freeze before
opening S4 or its dossier.

## Proposed Claim Delta

P140 provisionally reserves C-VEC-001 for a distinct exact conditional theorem
only if Candidates B through D close beyond C-EFT-001. Its possible surface is
the stationary reduction of a fully declared vector or antisymmetric
auxiliary multiplet coupled to a supplied SU(2) current wedge, together with
the exact wedge/Gram and commutator-square identities and every normalization
factor. A kinetic-vector statement must retain its derivative-expansion
remainder.

Direct searches find no accepted, proposed, rejected, or reserved C-VEC
identifier and no canonical vector-saturation or current-wedge quartic API.
C-EFT-001 remains the generic elimination dependency rather than being
re-promoted. C-VEC-001 cannot claim HLS, a physical rho, KSRF, B1, a numerical
c4, a unique ultraviolet completion, physical Skyrme stabilization, or a
substrate mechanism unless those separate premises close.

## Implementation and Oracle Plan

The source gate begins with an AST compatibility audit. Mutable scripts use
`np.trapezoid` when sampled integration is required, canonical integration
uses `trapezoid_integral`, and immutable source with legacy access receives an
explicit alias-only replay backed by `np.trapezoid`; a version abort is not a
scientific rejection. Exact algebra is expected, so sampled quadrature should
not enter the new theorem.

SymPy is the primary oracle for stationary equations, on-shell substitution,
matrix traces, cross products, coefficient transformations, formal inverse
residuals, and limits. A fresh independent reviewer derives the wedge norm and
completion of square without the canonical helper. Mutations flip the source
sign and metric, remove the coupling, change the one-half convention, rescale
generators or vector fields, alter KSRF, free B1, exchange I1 and I2, omit a
commutator term, and keep the next inverse-mass order. Static positivity is
tested on the derived energy object rather than inferred from a propagator
denominator.

The primary verifier pins source, dossier, frozen proposal, accepted claim
surfaces, every source predicate, data flow, and any new API. Graph replay
uses a frozen manifest so later valid queue changes do not invalidate P140.
Only a genuinely changed promotion boundary receives the integrated workflow
gate; focused scientific checks run during development.

## Attempts and Continuation

Attempt 0001 freezes this contract before source execution or body inspection.
Later failures are appended with the failed representation, scientific or
technical mechanism, and a materially different next route. Failure of S4's
physical headline advances Candidates B through F and does not close the
positive conditional object by itself.

## Debt Ledger

The campaign ledger tracks every source predicate and each missing action,
convention, coefficient, import, compatibility event, dependency, consumer,
and generated record.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| S4 executable and checks are unopened | Hash, compatibility preflight, native or alias replay, AST/data-flow audit, and all eleven predicates | open |
| The claimed vector action may be incomplete | Inventory every kinetic, mass, interaction, gauge, source, boundary, and sign term | open |
| Tensor structure may be inserted | Independent full I1-I2 and commutator-square derivations with mutations | open |
| Propagator sign may be confused with action or energy sign | One convention-closed stationary and static-energy ledger | open |
| A finite low-momentum series may be called exact | Explicit inverse residual, next-order term, domain, and limit | open |
| KSRF B1 and c4 may be imported or fitted | Provenance, free-parameter, rescaling, and target-as-input countermodels | open |
| Dependencies consumers and novelty are incomplete | B1, accepted claims, eleven reverse consumers, cycles, and graph impact audit | open |
| Registry disposition release docs queue and memory are unsynchronized | Individual review and one terminal governed-state transaction | open |

## Review and Promotion Plan

Any C-VEC-001 candidate receives a fresh independent symbolic derivation and
an individual claim review. Reusable algebra moves under
`src/substrate_framework/`; source orchestration and physical-ceiling evidence
remain in P140. The review separately assigns verification, review,
compatibility, and epistemic axes and audits every dependency and mutation.

S4 receives a terminal predicate-level disposition whether or not a new claim
is promoted. A mixed source maps only exact accepted surfaces and records the
rejected KSRF, coefficient, rho, physical, or substrate readings. The release,
disposition queue, generated docs, accepted memory, proposal memory, and parent
effort update only at their actual changed boundaries.

## Done Gate

P140 closes only with a complete positive exact or controlled-expansion object,
sensitive primary and independent evidence, individual review for any new
claim, terminal S4 disposition, closed dependencies and consumers,
synchronized governed state, and an empty campaign ledger. A clean eleven-
check tally, favorable sign, numeric c4 match, imported KSRF relation, or rho
label does not complete the campaign.

## Cross-References

The governing references are P008, P024, P059, P060, P061, P137, P138, P139,
B1, S4, WZ4, C-EFT-001, C-CHI-001, C-CHI-002, C-LIE-001, C-SK-001,
v0.106.0, and the parent migration effort.
