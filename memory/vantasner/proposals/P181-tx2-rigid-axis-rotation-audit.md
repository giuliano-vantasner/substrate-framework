---
description: Audit TX2 and construct an exact rigid-axis STF rotation theorem
author: vantasner
created: '2026-08-11T07:53:00Z'
updated: '2026-08-11T08:18:00Z'
tags:
- substrate-framework
- campaign-proposal
- migration-TX2
- rigid-rotation
- quadrupole
category: proposals
confidence: established
status: archived
---
# P181 TX2 Rigid-Axis Rotation Audit

## Question and Positive Deliverable

P181 must determine exactly what follows when an axisymmetric STF moment is
orthogonally rotated about an aligned or perpendicular declared axis. The
positive deliverable is an importable convention-safe rotation construction,
an exact invariant classification, exact harmonic derivatives and conditional
TT consequences, and a predicate-level TX2 disposition. Finding that TX2's
triaxial label is false cannot complete the campaign without the corrected
positive theorem.

## Base Release and Provenance

The accepted base is v0.132.0 at clean framework commit
`b88b2576fe0490be21895b87f5b3be77cf5bbd7f`, with 170 accepted claims. Its
manifest SHA-256 is
`370471d17be24a34f909c34cfa42e8a33b8e92ce66ea1e9057ccdc72199d26bd`.
The governed predecessor baseline is
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`. TX2 is pending at
`merged-framework/bridges/phase-40/bridge_TX2_rotating_triaxial_quadrupole.py`,
SHA-256
`7dd6852af20ef060ffa2f17950219fb79d7943e50fc64235a75a10d098f7d3b7`.
The target path is clean at the governed commit and its sole history commit is
`7222eed21720c5174dd35ba8f825d8b7e0a48f3f`; unrelated later predecessor
worktree changes have no authority.

The generated queue and prior graph replay already exposed TX2's body tensor,
aligned and perpendicular rotation formulas, claimed generic triaxiality,
pure twice-frequency line, seven checks, and one assertion. P181 therefore
claims no fresh result or runtime-output blinding. Exact source definitions,
sign conventions, derivative construction, predicates, assertion target, and
conclusion dataflow remain unopened until this freeze commits.

## Invariants, Conventions, and Allowed Imports

C-MOM-001 fixes normalized `I_STF` and `Q=3*I_STF`; tensor kinematics does not
establish locally conserved source dynamics or gravity. C-GW-001/002 fix only
conditional TT projector, power, convention, and basis algebra. C-GW-007/008
distinguish tensor eigenstructure, observer coordinates, and temporal rank.
C-RMOM-001 fixes the conditional B2 normalized moment as
`diag(q,q,-2q)` with `q>0`; C-RMOM-002 supplies one dimensionless numeric
magnitude, but neither supplies a rotating field, physical scale, inertia,
stability, selected angular speed, gravity, or radiation.

Orthogonal conjugation must preserve the characteristic polynomial, repeated
eigenvalue, trace, determinant, and Frobenius norm. Cartesian diagonal entries
are not eigenvalues in the presence of off-diagonal components. A prescribed
`Omega` and rotation matrix are declared kinematics, not a solution of field
equations. Mutable quadrature uses `np.trapezoid` or `trapezoid_integral`;
immutable legacy compatibility stops receive alias-only replay and never count
as scientific candidate failures.

## Candidate Preregistration

Six candidates separate reproduction, exact kinematics, conditional TT
composition, the source's coordinate-based classification, full dynamics,
and governance.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal TX2 replay | Hash-pinned source environment | Source `q`, axis, phase, and `Omega` | Evidence only | AST, native/alias execution, tensor, derivative, spectrum, predicate, assertion, and dataflow inventory |
| B | Exact rotated-axisymmetric theorem | Orthogonal rotation and axisymmetric STF body | Amplitude, axis, phase, convention scale | Strong exact candidate | Characteristic polynomial, eigenvectors, aligned/perpendicular formulas, derivatives, zero limits, and mutations |
| C | Conditional TT composition | Candidate B plus C-GW-001/002/008 | Declared `G`, distance, observer frame | Exact but conditional | Direct TT projection, convention covariance, temporal rank, pure line, power norm, and independent basis route |
| D | Coordinate-diagonal triaxiality | Ignore off-diagonal eigenproblem | None | Conflicts with SO(3) invariants | Compare diagonal entries with exact eigenvalues and recover the rotating symmetry axis |
| E | Full rotating or tumbling field | Accepted action, inertia, charges, boundaries, and coupling | Dynamically selected parameters | Separate larger project | Full-field residual/evolution, conservation, refinement, stability, and coupling derivation |
| F | Governance closure | Claim-level review | None | Required | Dependency, consumer, disposition, queue, release, docs, memory, and debt replay |

## Selection Criteria and Blinding

Selection is ordered by accepted STF and TT convention compatibility; exact
SO(3) invariants and eigenvalue multiplicity; separation of coordinates,
principal values, and temporal rank; aligned, perpendicular, zero-speed, and
zero-amplitude limits; assumption and parameter economy; independent symbolic
derivation and mutation sensitivity; novelty; physical-scope honesty; and
downstream governance. Exposed source prose cannot select the theorem or set
a threshold. There is no fresh source-result or runtime-output blind.

## Proposed Claim Delta

P181 provisionally reserves C-GW-009 for an exact rigidly rotated
axisymmetric-STF kinematic and conditional-TT theorem. Repository-wide searches
found no collision for C-GW-009 or the rejected alternative C-MOM-004. The
claim will depend only on accepted moment and conditional TT conventions; its
TX2 application may additionally compose with C-RMOM-001/002. It will not
denote a genuinely triaxial full tensor, solved rotating field, selected
`Omega`, stability result, physical gravitational source, or observation.

Direct consumers include TX2, pending TX3, moment and TT package exports and
tests, migration records, generated docs, releases, and memory. No accepted
claim becomes retroactively dependent on P181 and no `supersedes` relation is
proposed.

## Implementation and Oracle Plan

The source audit will inventory every import, literal, rotation matrix, body
tensor, derivative, Fourier statement, triaxiality test, predicate, assertion,
output sentence, dependency, and compatibility surface. Lexical checks,
runtime checks, assertions, and headline conclusions remain separate. The
hash and prior execution evidence will be reused unless the body audit exposes
an unresolved runtime branch.

SymPy and direct matrix algebra are the strongest oracles for orthogonality,
conjugation, characteristic polynomials, eigenvalue multiplicity, symmetry-axis
recovery, trigonometric harmonics, exact derivatives, Frobenius norms, TT
readouts, convention covariance, and power. An independent derivation will use
the dyadic form `alpha*(e e^T-I/3)` and commutator differentiation rather than
the proposed component helper. Mutations change the rotation sign or order,
body eigenvalues, quadrupole scale, axis alignment, angular speed, trace, and
waveform coefficient; a fake triaxial body with three distinct eigenvalues is
the decisive counterexample to the repeated-eigenvalue result.

Any sampled time series is regression evidence only because the exact
harmonic theorem is stronger. If a spectral regression is retained, its
window is an integer number of periods with endpoint closure and the exact
twice-frequency coefficient is checked independently. The pure package API
will execute no simulation at import. Canonical integration remains
`trapezoid_integral`; mutable scripts use `np.trapezoid`, and TX2 receives an
alias-only compatibility replay only if its immutable syntax requires one.

## Attempts and Continuation

Attempt 0001 freezes v0.132.0, framework commit `b88b257`, the TX2 hash and
history, prior exposure, six candidates, selection criteria, C-GW-009, oracle
choices, impact result, compatibility policy, and open debt. Every failed
representation, implementation, source predicate, or validation route remains
append-only with a materially different next action.

## Debt Ledger

The P181 ledger tracks source reachability, tensor classification, derivative
and TT algebra, conventions, dynamics, dependencies, consumers, compatibility,
and governed state.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| TX2's exact implementation, predicates, assertion, values, and dataflow are unaudited in P181 | Pin every definition, input, check, assertion, result sentence, and source dependency | closed |
| Pairwise coordinate diagonals may be confused with eigenvalues | Derive the characteristic polynomial, eigenvectors, multiplicities, and coordinate counterexample | closed |
| Aligned, perpendicular, and generic rotation claims are unverified | Derive exact tensor and derivative formulas plus zero and wrong-axis mutations | closed |
| Convention-safe TT readouts, temporal rank, and power are open | Compose with C-GW-001/002/008 and independently rederive all factors | closed |
| Declared `Omega` and rigid rotation may be called solved dynamics | Separate kinematic path, full-field equations, conservation, stability, scale, and coupling | closed |
| C-GW-009 may duplicate accepted claims | Compare exact statements, APIs, assumptions, evidence, and consumers | closed |
| Legacy NumPy access may masquerade as science | Repair mutable code or use immutable alias-only replay without candidate rejection | closed |
| Dependencies, consumers, and governed records may disagree | Replay graph and synchronize disposition, queue, memory, claims, release, and docs | closed |

## Review and Promotion Plan

Every TX2 predicate receives an individual verdict. Rotation formulas,
aligned null, perpendicular derivatives, frequency, eigenstructure,
triaxiality, `Omega`, body-tensor provenance, quadrupole convention, TT and
power implications, full-field language, physical interpretation,
dependencies, and compatibility receive separate statuses. Any distinct
claim must be independently rederived, extracted into a pure tested API,
replayed through consumers, and promoted claim by claim. TX2 receives a
structured supported disposition with every unaccepted remainder preserved.

The promotion transaction edits only governed mutable records and generates
the queue and canonical docs. Every evidence path is materialized before
registration. Targeted routes run before one integrated `scripts/validate.sh`;
record-only closure is checked narrowly without repeating the full suite.
Validation and commit remain separate invocations.

## Done Gate

P181 closes only when a positive exact rotation theorem or an equally strong
accepted composition exists, every source predicate is adjudicated, the
eigenvalue and temporal-rank meanings are exact, kinematics and dynamics are
separate, dependencies and consumers replay, governed records agree, and the
debt ledger is empty. Refuting the word triaxial, reproducing seven checks, or
observing a clean harmonic alone keeps the campaign active.

P181 met this gate in release v0.133.0 by accepting exact C-GW-009 and
qualifying TX2 predicate by predicate. The full tensor remains axisymmetric;
the corrected positive theorem owns its prescribed rotation, derivative, tilt,
and conditional TT algebra. All eight debts are closed, and TX3 remains a
separate pending consumer.

## Cross-References

See C-MOM-001, C-GW-001/002/003/005/007/008, C-RMOM-001/002, P036-P039,
P047, P054, P055, P177, P180, BX1, E2, QB1, QB3, TX1-TX3,
`conserved_moments.py`, `tt_angular.py`, `triaxial_l2.py`, and
`conditional_triaxial_radiation.py`.
