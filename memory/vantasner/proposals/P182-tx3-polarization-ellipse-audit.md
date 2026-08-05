---
description: Audit TX3 and construct an exact generic-observer polarization-ellipse theorem
author: vantasner
created: '2026-08-11T08:28:00Z'
updated: '2026-08-11T08:33:00Z'
tags:
- substrate-framework
- campaign-proposal
- migration-TX3
- tt-polarization
- rotating-quadrupole
category: proposals
confidence: exploratory
status: active
---
# P182 TX3 Polarization-Ellipse Audit

## Question and Positive Deliverable

P182 must determine exactly what a generic observer reads from C-GW-009's
prescribed perpendicular rotation of an axisymmetric STF moment. The positive
deliverable is an importable, convention-safe coefficient and polarization-
ellipse classification with frame-invariant temporal rank, exact circular,
linear, and null limits, and a precisely scoped account of which common scales
cancel. Refuting TX3's wording or reproducing two nonzero coordinates cannot
complete the campaign without the corrected positive object or an exact
accepted-composition disposition.

## Base Release and Provenance

The accepted base is v0.133.0 at clean framework commit
`d0299cdfc80664e66cb9c23f0ec21278ad841cdd`, with 171 accepted claims. Its
manifest SHA-256 is
`b54f12b9dad95df4a225f980df6f74f58458ac174e312f5276c7bd1fe4ad1c8e`.
The governed predecessor baseline is
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`. TX3 is pending at
`merged-framework/bridges/phase-40/bridge_TX3_two_polarizations_omega_free.py`,
SHA-256
`ce6db5f59e61829c287e7cced5a53506838d31c77ba9e651dbceb9a241275837`.
The target path is clean at the governed commit and its sole history commit is
`7222eed21720c5174dd35ba8f825d8b7e0a48f3f`; unrelated later predecessor
worktree changes have no authority.

The generated queue and earlier reverse-consumer replay already exposed the
generic `(1,1,1)` direction, rotation-axis circular and selected perpendicular
linear classifications, two-coordinate and incommensurate-phase language,
fixed-phase ratio claim, seven checks, and one assertion. P182 therefore claims
no fresh source-result or runtime-output blind. Exact definitions, basis,
amplitudes, predicates, assertion target, and conclusion dataflow remain
unopened until this freeze commits.

## Invariants, Conventions, and Allowed Imports

C-GW-001/002 fix only conditional TT projection, normalization, and basis
algebra. C-GW-007 fixes temporal source rank and proves that two instantaneous
coordinate nonzeros are insufficient. C-GW-008 fixes the conditional real-
`m=2` waveform and quadrature-rank theorem. C-GW-009 fixes the prescribed
perpendicular rotation, pure twice-frequency tensor harmonic, derivative
norms, and rotation-axis circular readout, but it supplies no solved source
dynamics or physical radiation. C-MOM-001 and C-RMOM-001 prevent normalized
`I_STF` from being silently relabeled as triple `Q`.

Polarization coordinates depend on a declared oriented transverse frame;
temporal rank, ellipse degeneracy, and singular values are invariant under
orthogonal changes of that frame. A common factor can cancel from a ratio at
fixed dimensionless phase while the waveform at fixed physical time still
depends on `Omega` through both amplitude and phase. Mutable quadrature uses
`np.trapezoid` or `trapezoid_integral`; immutable legacy compatibility stops
receive alias-only replay and never count as scientific candidate failures.

## Candidate Preregistration

Six candidates separate reproduction, a distinct exact theorem, accepted
composition, the source's coordinate proxy, full dynamics, and governance.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal TX3 replay | Hash-pinned source environment | Source direction, frame, phase, `q`, and `Omega` | Evidence only | AST, native/alias execution, projector, coefficient, predicate, assertion, and dataflow inventory |
| B | Exact generic-observer ellipse theorem | C-GW-009 perpendicular path plus C-GW-002/008 | Direction inclination, transverse-frame angle, phase, amplitude scale | Strong exact candidate if distinct | Derive the harmonic coefficient matrix, determinant, singular values, rank, frame covariance, and circular/linear/null limits |
| C | Accepted composition or duplicate | C-GW-002/007/008/009 | No new physical parameter | Preferred if the exact statement and API already exist | Claim/API/evidence/consumer nonduplication audit |
| D | Two-coordinate proxy | Nonzero plus and cross at one phase; call their phases incommensurate | Source literals | Conflicts with accepted temporal-rank meaning | Compare full time-trace coefficient rank and common frequency with one-time coordinate tests |
| E | Full physical rotating source | Accepted action, stress, inertia, charge, stability, coupling, detector model | Dynamically selected quantities | Separate larger project | Full-field residual/evolution, conservation, stability, coupling, propagation, and detector derivation |
| F | Governance closure | Claim-level review | None | Required | Dependency, consumer, disposition, queue, release, docs, memory, and debt replay |

## Selection Criteria and Blinding

Selection is ordered by accepted STF and TT convention compatibility;
temporal-rank and ellipse invariants; exact generic-direction and limiting-view
behavior; transverse-frame covariance; separation of azimuth from time origin;
fixed-phase scale cancellation versus physical-time `Omega` dependence;
assumption and parameter economy; independent exact derivation and mutation
sensitivity; novelty; physical-scope honesty; and downstream governance.
Exposed source prose cannot select the theorem or set a threshold. There is no
fresh source-result or runtime-output blind.

## Proposed Claim Delta

P182 provisionally reserves C-GW-010 for an exact generic-observer TT
polarization-ellipse theorem for the perpendicular prescribed rotation of
C-GW-009. Repository-wide searches found no collision for C-GW-010 or P182.
The claim will depend only on accepted moment, rotation, rank, and conditional
TT conventions. It will not denote independent physical gravitons, a solved
rotating field, selected `Omega`, gravity, radiation, detector response, or an
Omega-independent physical-time signal.

Direct consumers include TX3, pending TX4/TX5 narrative edges, rotation and TT
package exports and tests, migration records, generated docs, releases, and
memory. No accepted claim becomes retroactively dependent on P182 and no
`supersedes` relation is proposed.

## Implementation and Oracle Plan

The source audit will inventory every import, tensor, derivative, line of
sight, transverse frame, TT formula, amplitude, phase, ratio, limit, predicate,
assertion, output sentence, dependency, and compatibility surface. Lexical
checks, runtime checks, assertions, and headline conclusions remain separate.
The prior hash-pinned runtime evidence will be reused unless the body audit
exposes an unresolved branch.

SymPy and direct matrix algebra are the strongest oracles for TT projection,
harmonic coefficient matrices, determinants, ranks, singular values, frame
rotations, fixed-phase scale cancellation, and exact limits. One implementation
will compose canonical rotation and TT APIs; an independent route will use the
dyadic axis path and a hand-constructed transverse basis without the proposed
readout helper. Mutations change the tensor convention, derivative order,
rotation sign, observer inclination, transverse orientation, phase origin,
`Omega`, and waveform coefficient. Proportional traces and a one-time pair of
nonzero coordinates are decisive counterexamples to an insensitive two-mode
predicate.

Sampled ranks or Fourier spectra are regression evidence only because exact
harmonic coefficients are stronger. Any retained sampled route uses a complete
integer-period window, removes DC explicitly, and compares with the exact
rank. The pure package API will execute no simulation at import. Canonical
integration remains `trapezoid_integral`; mutable scripts use `np.trapezoid`,
and TX3 receives alias-only replay only if its immutable syntax requires one.

## Attempts and Continuation

Attempt 0001 freezes v0.133.0, framework commit `d0299cd`, the TX3 hash and
history, prior exposure, six candidates, selection criteria, C-GW-010, oracle
choices, low-risk impact boundary, compatibility policy, and open debt. Every
failed representation, implementation, source predicate, or validation route
will remain append-only with a materially different next action.

## Debt Ledger

The P182 ledger tracks source reachability, projector and frame algebra,
temporal rank, ellipse classification, phase and `Omega` scope, conventions,
physical interpretation, dependencies, consumers, compatibility, and governed
state.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| TX3's exact implementation, predicates, assertion, values, and dataflow are unaudited in P182 | Pin every definition, input, check, assertion, result sentence, and source dependency | open |
| Generic-observer coefficient matrix and ellipse classification are unverified | Derive exact rank, determinant, axes, handedness information, and circular/linear/null limits | open |
| Frame covariance, direction azimuth, and time origin may be conflated | Prove the transverse-frame double-angle transformation and isolate symmetry-related phase shifts | open |
| Fixed-phase ratio cancellation may be mislabeled as physical `Omega` independence | Derive amplitude and phase dependence at fixed phase and fixed physical time, including zeros and poles | open |
| Tensor convention and conditional waveform may be promoted as physical radiation | Replay scale covariance and preserve dynamics, gravity, propagation, detector, and observation ceilings | open |
| C-GW-010 may duplicate accepted claims | Compare exact statements, APIs, assumptions, evidence, and consumers | open |
| Legacy NumPy access may masquerade as science | Repair mutable code or use immutable alias-only replay without candidate rejection | open |
| Dependencies, consumers, and governed records may disagree | Replay graph and synchronize disposition, queue, memory, claims, release, docs, and debt | open |

## Review and Promotion Plan

Every TX3 predicate receives an individual verdict. Observer directions,
transverse frames, TT amplitudes, time phases, frequency content, temporal
rank, circular/elliptical/linear/null classifications, ratio domains, `Omega`
scope, tensor convention, physical language, dependencies, and compatibility
receive separate statuses. Any distinct claim must be independently rederived,
extracted into a pure tested API, replayed through consumers, and promoted
claim by claim. TX3 receives a structured supported disposition with every
unaccepted remainder preserved.

The promotion transaction edits only governed mutable records and generates
the queue and canonical docs. Every evidence path is materialized before
registration. Targeted routes run before one integrated `scripts/validate.sh`;
record-only closure is checked narrowly without repeating the full suite.
Validation and commit remain separate invocations.

## Done Gate

P182 closes only when a positive exact generic-observer theorem or an exact
accepted-composition disposition exists, every source predicate is adjudicated,
rank and ellipse meanings are exact, phase-parametrized cancellation is not
overread as physical-time independence, dependencies and consumers replay,
governed records agree, and the debt ledger is empty. Reproducing seven checks,
finding two nonzero coordinates, or naming an ellipse alone keeps the campaign
active.

## Cross-References

See C-MOM-001, C-GW-001/002/003/005/007/008/009, C-RMOM-001/002, P038,
P039, P047, P054, P055, P180, P181, BX1, E2, GW2, GW3, QB1, QB3, QB4,
TX1-TX5, `tt_angular.py`, `triaxial_l2.py`,
`conditional_triaxial_radiation.py`, and `rigid_quadrupole_rotation.py`.
