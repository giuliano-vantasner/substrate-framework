---
description: Audit YM1 and derive a properly scoped non-Abelian vacuum-polarization theorem if distinct
author: vantasner
created: '2026-08-10T11:40:00Z'
updated: '2026-08-10T11:40:00Z'
tags:
- substrate-framework
- campaign-proposal
- migration-YM1
- nonabelian-vacuum-polarization
category: proposals
confidence: exploratory
status: active
---
# P158 YM1 Yang-Mills Induction Audit

## Question and Positive Deliverable

P158 must reproduce and independently audit YM1's claimed induction of a
non-Abelian Yang--Mills kinetic term. The positive deliverable is either a
complete, distinct, conditional massive-scalar non-Abelian vacuum-polarization
theorem with importable implementation and tests, or terminal source closure
through already accepted claims if source-aware novelty fails. Group trace
algebra, transverse kinematics, a local loop term, a declared bare action, and
a physical substrate gauge sector remain separately typed.

## Base Release and Provenance

The accepted base is v0.122.0 at framework and scientific commit `bf083b8`.
The source baseline is `/home/dan/substrate` commit
`6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`; later dirty engineering,
framework-prose, and memory files remain excluded. YM1 is pinned at
`merged-framework/bridges/phase-7/bridge_YM1_yang_mills_induction.py`,
SHA-256
`bb8046bcf3a57d23bd50f9ac5ca6953cab8ffaaa2a2f852074495b48b6e83cf6`.
Its dossier is `merged-framework/bridges/phase-7/dossiers/YM1-dossier.md`,
SHA-256
`3f58232191a2b58ae507ddbc107fe0f7ed08dc4e1e41927c0ced74ea6760765d`.

The queue exposes nine literal checks, one assertion, a symbolic oracle,
dependencies EM3, EM5, EM7, GK1, M1, M2, W2, W5, W7, and YM2, plus excerpts
naming a fundamental trace factor one half, a transverse projector, and a
claimed generated kinetic term. These unavoidable values are recorded and
cannot select a candidate. The source and dossier bodies, exact AST flow,
guards, additional constants, and narrative consumers remain unopened.

## Invariants, Conventions, and Allowed Imports

C-NAG-001 already fixes `D=partial-i*g*W`, the finite connection sign,
curvature covariance, commutator, and invariant trace square, while explicitly
excluding a kinetic coefficient, equation, induction mechanism, matter sector,
and substrate map. C-VAC-001 already fixes a complete separately declared
massive complex-scalar QED2 determinant, bubble--seagull Ward cancellation,
exact kernel, low-momentum coefficient, limits, and physical ceilings. It does
not authorize a non-Abelian representation or covariant completion.

For Hermitian generators in a declared representation, the invariant index is
`tr_R(T_a T_b)=T(R) delta_ab`; a coefficient multiplying
`F_a F_a` must not be confused with one multiplying `tr_R(F F)`.
Transversality at nonzero momentum is kinematic unless the determinant,
bubble, seagull, regulator, and momentum-shift identity are supplied. A
quadratic zero-background kernel does not by itself establish the full
non-Abelian cubic and quartic curvature completion. Bare and counterterm
coefficients remain additive, and representation, mass, coupling,
multiplicity, field normalization, dimension, regulator, subtraction, and
matching scale remain explicit inputs.

## Candidate Preregistration

The candidates are frozen before source-body inspection or execution.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal YM1 audit | Hash-pinned immutable source only | Source literals | Retains only individually valid predicates | AST, data-flow, process, guard, and mutation audit |
| B | Accepted composition | C-NAG-001, C-REP-002, C-VAC-001 | Their declared inputs | No new claim if YM1 only multiplies an Abelian result by a trace | Exact claim/API nonduplication |
| C | Non-Abelian scalar loop | Euclidean 2D complex scalar in representation R, determinant, preserving regulator | m, g, multiplicity, T(R) | Distinct conditional theorem if Ward and covariant completion close | Bubble--seagull contraction, exact kernel, heat-kernel local term, limits |
| D | Classical Yang--Mills variation | Declared invariant metric, action, current, boundary variation | Bare coefficient and coupling | Distinct action theorem only if not already governed and source relevant | Matrix/action variation, Bianchi and current consistency |
| E | Algebra-only retention | Exact generators and nonzero momentum | Representation normalization | Trace and projector checks survive without loop authority | Representation and projector residuals |
| F | Representation mutations | Fundamental, adjoint, and rescaled bases | T(R), normalization coordinate | Exposes coefficient-coordinate dependence | Exact traces and coupled-generator invariance |
| G | Bare-plus-loop counterfamily | Allowed local counterterm and field rescaling | Independent baseline and scale | Rejects unique induced coupling or pole | Affine coefficient and normalization orbits |
| H | Physical mechanism | Full microscopic quantum and matching model | All material and observable inputs | Absent unless independently supplied | Premise, state, regulator, matching, and observation audit |
| I | Governance closure | Frozen DAG and consumers | None | Required for any disposition | Queue, release, docs, memory, and debt replay |

## Selection Criteria and Blinding

Selection is ordered by convention agreement; complete quantum inputs;
bubble--seagull Ward derivation; coefficient and trace typing; non-Abelian
covariant completion; exact limits; baseline, counterterm, normalization, and
representation sensitivity; physical-interpretation separation; framework fit
and nonduplication; then graph and governance closure. The queue-preexposed
one-half, projector, and generated-term labels are excluded from selection and
all thresholds until the committed freeze.

## Proposed Claim Delta

The proposed delta reserves one identifier only if every theorem gate closes.

`C-NVP-001` is reserved only for a complete conditional non-Abelian scalar
vacuum-polarization theorem that remains distinct from C-NAG-001 and C-VAC-001
after source inspection. It would depend on those claims without superseding
them and would explicitly retain the separately declared quantum action,
representation, regulator, bare coefficient, counterterm, normalization,
dimension, and physical ceilings. If completeness or novelty fails, the
identifier remains unpromoted and the campaign closes YM1 through existing
accepted claims.

## Implementation and Oracle Plan

The primary route will use exact SymPy representation and loop algebra, the
canonical C-NAG-001 and C-VAC-001 APIs, source hashes and AST, and a
background-field or heat-kernel derivation if Candidate C survives. A fresh
review will independently reconstruct generator traces, bubble--seagull Ward
cancellation, the scalar parameter integral, the local curvature coefficient,
and Abelian, heavy-mass, massless, zero-momentum, representation, and
counterterm limits without importing a new canonical module.

Load-bearing mutations include deleting or sign-flipping the seagull, replacing
the scalar numerator by a fermion numerator, omitting T(R), changing
representation normalization without the coupled-g change, replacing a
moving curvature background by projector algebra, dropping the bare
coefficient, changing mass or species count, and identifying equal
coefficients across distinct physical dictionaries. Source and graph replay
will pin hashes and predicate inventories without granting pending consumers
authority.

Compatibility preflight audits direct, imported, dynamic, and eager legacy
NumPy integration access. Mutable and canonical code must use exact algebra,
`trapezoid_integral`, or `np.trapezoid`; executable `np.trapz` is
forbidden. An immutable spelling-only failure receives an isolated alias backed
by `np.trapezoid` before scientific replay and never counts as candidate
failure. Exact algebra is preferred because all currently frozen obligations
are analytic; any genuinely numerical route must separately preregister its
equation, solver, tolerances, refinement, error norm, and independent method.

## Attempts and Continuation

Every action, representation, regulator, Ward, coefficient, limit,
normalization, compatibility, source, consumer, or verifier failure is
preserved append-only with a diagnosed layer and materially different next
attempt. A source failure cannot lower the theorem's bar; it selects a better
candidate or terminal source mapping while the parent migration continues.

## Debt Ledger

The ledger tracks source and dossier hashes, all nine predicates and one
assertion, generator and trace normalization, connection and curvature
conventions, quantum field and determinant, bubble and seagull, regulator,
dimension, exact kernel, local expansion, background completion, bare and
counterterm coefficients, field normalization, limits, physical dictionaries,
dependencies, consumers, compatibility, nonduplication, disposition,
generated state, and parent continuation.

## Review and Promotion Plan

Every proposed or affected claim receives individual review. A surviving
C-NVP-001 is extracted to a pure package module with focused tests, exact and
independent oracles, impact analysis, registry entry, release, generated docs,
and accepted memory. Otherwise YM1 receives a terminal qualified, refuted, or
duplicate disposition with exact retained and rejected content. Both routes
require dependency, semantic-consumer, compatibility, novelty, queue,
documentation, memory, and empty-debt closure, followed by one integrated
terminal gate.

## Done Gate

P158 closes only when the representation convention, Ward derivation, kernel,
local invariant, full versus quadratic scope, all nine predicates, coefficient
freedom, exact limits, physical ceiling, compatibility, semantic consumers,
canonical or nonduplication state, and debt ledger close. A physical
Yang--Mills or substrate sector additionally requires a complete governed
quantum action, matter representation, regulator, counterterms, matching,
dimension, state, and observable evidence.

## Cross-References

See YM1, YM1-dossier, W7, EM5, YM2, C-NAG-001, C-REP-002, C-VAC-001,
C-GAU-001, C-MAX-001, `nonabelian_gauge.py`,
`vacuum_polarization.py`, P151, P135, and the parent migration effort.
