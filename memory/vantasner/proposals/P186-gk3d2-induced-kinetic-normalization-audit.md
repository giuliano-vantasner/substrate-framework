---
description: Audit GK3D2 and derive a scalar-loop and kinetic-boundary normalization ledger
author: vantasner
created: '2026-08-11T12:13:00Z'
updated: '2026-08-11T12:13:00Z'
tags:
- substrate-framework
- campaign-proposal
- migration-GK3D2
- vacuum-polarization
- kinetic-normalization
category: proposals
confidence: exploratory
status: active
---
# P186 GK3D2 Induced Kinetic Normalization Audit

## Question and Positive Deliverable

P186 must determine whether GK3D2 derives both the complex-scalar
four-dimensional one-loop coefficient and a total gauge kinetic
normalization. The positive deliverable is an importable conditional scalar
bubble-plus-seagull residue and logarithmic-slope theorem together with an
exact affine kinetic-boundary ledger that preserves every bare, counterterm,
reference-scale, field-normalization, and matching coordinate. It must say
exactly what an explicitly imposed zero boundary would imply without treating
an earlier no-matter/no-kinetic premise as that boundary. A demonstration that
the source erases an integration constant is attempt evidence, not completion.

## Base Release and Provenance

The accepted base is v0.137.0 at clean framework commit
`e7b2888c8ae526ee92b5da878f92b0ebe9aa660c`, with 177 accepted claims. Its
manifest SHA-256 is
`874abae995ffc0ad883255bee7f754383b0aa183cf88aa44fa77ce9712b9a55e`.
The governed predecessor baseline is
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`. GK3D2 is pending at
`merged-framework/bridges/phase-41/bridge_GK3D2_induced_kinetic_normalization.py`,
SHA-256
`856096aba38812dc17fb07ce5cf7c0fa13eb2623665ccf871810734ac3ca0886`,
size 22,026 bytes, blob `7eb49a516a9cd5ea24bcfadfd0dde2bf5e0462b0`, and sole
history commit `7222eed`. The target path is clean at the governed source
commit; later source-worktree artifacts have no authority.

The generated queue already exposes the claimed scalar-to-Dirac factor-four
logarithmic slope, rational matter weights, the claim that rung25 removes the
additive constant, seventeen static check sites with two dynamic calls, one
assertion, and a positive normalization synopsis. P186 therefore claims no
fresh source-result blinding. Exact formulas, signs, conventions, imports,
predicate dataflow, and the executable conclusion remain unopened until this
contract passes validation.

## Invariants, Conventions, and Allowed Imports

C-GAU-001 leaves every local gauge kinetic coefficient unconstrained.
C-MAX-001 supplies a kinetic coefficient and proves that deleting the kinetic
term gives only the current constraint; it does not force the connection to be
pure gauge. C-VAC-001 is a separately declared massive complex-scalar D=2
bubble-plus-seagull theorem and supplies neither a D=4 continuation nor a
counterterm choice. C-VAC-002 supplies a conditional charged-Dirac D=4 residue
and logarithmic slope but explicitly leaves the finite counterterm, bare term,
matching condition, and total normalization free. C-DIM-009 supplies only
dimension and convention bookkeeping. C-RGE-001 requires a reference coupling
in addition to a differential beta function.

P186 may conditionally declare one or more free complex charged scalars in
four dimensions, their determinant, bubble and seagull, loop order,
gauge-preserving dimensional regulator, tensor and effective-action
conventions, subtraction scheme, and matching condition. It may import exact
Feynman parameterization, dimensionally regulated Gaussian integrals, Gamma
identities, Laurent series, and affine first-order flow integration. The loop
piece, local counterterm, bare coefficient, renormalized reference value, and
total coefficient remain separately typed.

Hash-pinned GK3D2 and its source dependencies and consumers are noncanonical
evidence only. No accepted premise identifies a no-matter theory with a
matching surface after charged matter is introduced, supplies a physical
charged scalar or Dirac spectrum, fixes a representation, multiplicity,
charge, scale ratio, bare coefficient, finite counterterm, preferred
dimension, physical gauge group, observation, or substrate mechanism.
Mutable quadrature uses `np.trapezoid` or `trapezoid_integral`; immutable
legacy-name aborts are version-only compatibility evidence and never
scientific candidate failures.

## Candidate Preregistration

Six candidates separate literal reproduction, scalar-loop derivation,
boundary identifiability, matter-weight composition, matching alternatives,
and governed closure.

| Candidate | Object | Structural gate |
| --- | --- | --- |
| A | Hash-pinned source reproduction and predicate audit | Every coefficient, dependency, boundary statement, check, assertion, and headline edge is typed |
| B | Conditional D4 complex-scalar loop | Bubble and seagull close the Ward identity and exact residue and slopes in one declared convention |
| C | Affine inverse-kinetic flow | The independent reference value survives unless a matching boundary is separately imposed |
| D | Scalar and Dirac matter weights | Statistics, multiplicity, charge, trace, generator, and coupling conventions compose without selecting matter or group |
| E | Competing boundary models | Free bare-plus-counterterm, explicit zero matching, and measured matching remain distinct before any total coefficient is selected |
| F | Governed closure | Claim, source, future consumers, release, queue, docs, memory, and debt agree |

## Selection Criteria and Blinding

Selection is ordered by declared action and statistics, bubble-seagull Ward
closure, exact scalar normalization, separation of loop slope from affine
boundary, correct scope of the earlier no-matter result, tensor and field
normalization consistency, explicit matter weights, zero-charge and heavy-mass
limits, matching and scale behavior, independent rederivation, mutation
sensitivity, assumption economy, and global closure. Numerical agreement
cannot select a coefficient or boundary. The queue synopsis already reveals
the broad source result, so the meaningful gate is frozen structural criteria
before the implementation body and detailed output open.

## Proposed Claim Delta

P186 reserves C-VAC-003 for a distinct conditional complex-scalar D4
vacuum-polarization residue and kinetic-boundary theorem, including every
action, regulator, tensor, subtraction, flow, matching, and scope condition
actually earned. Repository-wide registry, campaign, queue, and memory search
finds no identifier collision; rejected provisional identifiers remain
reserved. The proposal has no `supersedes` edge. Likely consumers are GK3D2,
GK3D3 through GK3D6, the canonical vacuum-polarization and running surfaces,
tests, registry, release, generated records, migration disposition and queue,
and later gauge-sector claims. Each may inherit only the exact conditional
coefficient and boundary ledger.

## Implementation and Oracle Plan

The source audit first pins AST and NumPy compatibility surfaces, native
execution, every imported dependency, scalar and Dirac coefficient, beta and
kinetic convention, scale, boundary premise, predicate, assertion, and
conclusion edge. Reusable equations belong in pure package APIs; imports run no
simulation or tally.

The primary symbolic route derives the regulated scalar bubble and seagull or
an equivalent gauge-preserving determinant expansion, contracts the Ward
identity, extracts the D=4 Laurent residue and declared subtraction-scale
slope, and translates it into the chosen inverse-kinetic convention. A
separate exact flow route integrates the differential coefficient while
retaining its reference value. It then evaluates, but does not infer, an
explicitly declared zero-matching condition. An independent implementation
must not import the new canonical claim module and must reconstruct the
load-bearing parameter integral, coefficient, affine family, and boundary
counterexamples.

Mutations change the scalar bubble/seagull balance, statistics factor,
charge-square or multiplicity weight, tensor sign, scale orientation, finite
counterterm, bare coefficient, and matching surface. Counterexamples compare
two theories with the same zero no-matter action but unequal permitted finite
matching after charged matter is introduced, and two total coefficients with
the same derivative. Zero charge, heavy mass at fixed subtraction, equal
scales, reference-scale changes, and explicitly imposed zero matching remain
separate limits. SymPy is the strongest practical oracle for the exact
identities; high-precision quadrature, if needed for a nonclosed integral, is
only an independently refined numeric cross-check.

Compatibility preflight inspects executable direct, imported, and dynamic
legacy trapezoidal access. Mutable code is repaired to `np.trapezoid` or the
canonical helper before scientific adjudication. Immutable source receives a
recorded alias-only replay when required, and that environment event never
rejects a candidate.

## Attempts and Continuation

Attempt 0001 freezes v0.137.0, framework commit `e7b2888`, the GK3D2 hash and
history, exposed synopsis, C-VAC-003, six candidates, selection criteria,
oracle hierarchy, compatibility policy, and debt before the source body opens.
Memory recall finds the accepted scalar D2, Dirac D4, Maxwell, dimensional,
and running boundaries but no governed GK3D2 result. Every later failed
implementation, representation, regulator, boundary, candidate, or verifier
route remains append-only with a materially different continuation.

## Debt Ledger

The P186 ledger tracks source reachability, scalar quantum premises,
bubble-seagull closure, D4 residue, running convention, affine boundary,
bare and counterterm freedom, compatibility, dependencies, consumers, and
governed state.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| GK3D2 formulas, predicates, assertion, and headline dataflow are unopened | Pin and audit every declared object and conclusion edge | open |
| The scalar coefficient may be copied from a numerator integral without a seagull or regulator | Derive it in a complete gauge-preserving scalar-QED convention | open |
| Dirac and scalar beta conventions may be mixed | Derive both weights in one declared kinetic and scale convention | open |
| A differential slope may be presented as a total normalization | Integrate the affine family and retain its independent reference value | open |
| The earlier no-matter result may be mislabeled a matching boundary | Compare theories, premises, and operator bases and require a separately declared matching condition | open |
| Bare and finite counterterm coordinates may be erased | Expose both and show load-bearing mutations with the same loop slope | open |
| Group and matter weights may be called physical sectors | Preserve conditional multiplicities, charge squares, traces, and generator/coupling rescaling | open |
| Legacy NumPy access may masquerade as science | Repair mutable code or use immutable alias-only replay without candidate rejection | open pending source AST preflight |
| Dependencies, future consumers, and governed records may disagree | Replay the graph and synchronize disposition, queue, claims, release, docs, memory, and debt | open |

## Review and Promotion Plan

C-VAC-003 receives a raw-artifact claim review with independent derivation and
mutation evidence. The four status axes remain separate. GK3D2 receives an
individual decision for every scalar coefficient, beta weight, running law,
boundary claim, induced normalization, group/matter composition, and physical
interpretation. Mixed surviving and rejected content yields a qualified
disposition with every remainder explicit. Evidence paths materialize before
registration. Targeted scientific routes precede one integrated workflow
boundary; record-only closure uses narrow generation and repository checks.

## Done Gate

P186 closes only when the scalar D4 loop and affine boundary objects are
importable and mutation-sensitive, the earlier no-matter premise is not
silently promoted into a matching condition, every total-normalization freedom
is explicit, candidates and source predicates are adjudicated, downstream
consumers replay, accepted state is synchronized, and the debt ledger is empty.
Any failed route queues the next materially different attempt.

## Cross-References

See C-GAU-001, C-MAX-001, C-VAC-001, C-VAC-002, C-DIM-009, C-RGE-001,
P135, P176, P185, EM3, EM5, GK1, GK3D1, GK3D2-6,
`vacuum_polarization.py`, `dirac_vacuum_polarization.py`, `maxwell.py`, and
`renormalization.py`.
