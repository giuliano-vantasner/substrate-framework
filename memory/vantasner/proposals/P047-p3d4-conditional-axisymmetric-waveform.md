---
description: Derive a convention-safe axisymmetric STF radiation map and audit P3D4
author: vantasner
created: '2026-08-01T22:31:00Z'
updated: '2026-08-01T23:36:00Z'
tags:
- substrate-framework
- campaign-proposal
- axisymmetric-stf
- migration-P3D4
category: proposals
confidence: exploratory
status: archived
---
# P047 P3D4 Conditional Axisymmetric Waveform Audit

## Question and Positive Deliverable

P047 must derive an importable convention-safe TT readout and conditional
power map for an arbitrary-axis axisymmetric STF tensor. It must then determine
whether P3D4 can apply that map to the accepted regular l=2 energy-moment trace
with numerically stable second and third time derivatives. If the numerical
gates fail, the exact general tensor map remains the required positive object;
a derivative obstruction or source refutation alone does not complete P047.

## Base Release and Provenance

The accepted base is `v0.41.0` at framework commit `6196b44`, whose scientific
release was promoted in `8632e73`. `C-GW-001` supplies the exact TT angular
identity and conditional normalized/triple quadrupole conversion; `C-GW-002`
supplies the normalized polarization basis; `C-GW-004` supplies a
source-specific exact axisymmetric conditional example; and `C-PDE-003/004`
supply the exact regular l=2 equation and qualified finite-time energy-moment
trace. P3D4 is pending source evidence at `substrate@6d1f4e0`, SHA-256
`055c001288217998406b73026bf9f1402e044c5b4b26aa1929241a31402b827f`.
Memory search found the accepted dependencies and current migration effort but
no authoritative P3D4 result.

## Invariants, Conventions, and Allowed Imports

For a normalized STF moment `I`, the conditional external waveform rule is
`h_TT=(2G/R) Lambda I_ddot` and the conditional power is
`P=(G/5) I'''_ij I'''_ij`. For the triple tensor `Q=3I`, the same statements
require coefficients `2G/3` and `G/45`; using `G/5` with `Q` is a factor-nine
error. The plus/cross basis is the accepted orthonormal one, while a
conventional unnormalized plus readout differs by `sqrt(2)`. `C-PDE-004` is a
dimensionless finite-time simulation claim, not a physical scale, asymptotic
radiation zone, gravity theory, or backreaction law. A third derivative is a
new numerical observable and may not inherit the verification status of the
underlying moment trace.

## Candidate Preregistration

The alternatives are frozen from queue metadata and accepted dependencies
before reading the complete P3D4 executable or its reported values.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Exact arbitrary-axis map plus qualified derivative traces | Accepted STF conventions, conditional gravity rule, and C-PDE-004 IVP | Derivative stencil or spline order and an excluded endpoint interval | Compatible extension if derivatives converge | Exact tensor algebra plus spatial, timestep, sampling, domain, and estimator convergence |
| B | Exact arbitrary-axis map only | Accepted STF conventions and conditional gravity rule | None | Native exact extension | Exact algebra closes while derivative gates fail or add unjustified assumptions |
| C | Accept the P3D4 construction as one physical radiation mechanism | P3D4 field ansatz, moment, derivative, gravity normalization, and interpretation | Any source constants and numerical settings | Expected convention and dependency conflict | Full source reproduction, factor audit, field-consistency audit, and derivative sensitivity |

## Selection Criteria and Blinding

Selection is ordered by exact STF convention closure, exact TT inclination and
polarization geometry, accepted dependency closure, endpoint-safe derivative
stability, spatial/timestep/sampling/domain/estimator refinement, amplitude and
wrong-convention mutation sensitivity, assumption economy, and strict
conditional-versus-physical scope. Before inspecting P3D4 comparator values,
the exact parameterization and formulas will be frozen. For a trace sampled on
a uniform grid, numerical promotion requires an interior interval at least
five dimensionless time units from each endpoint; mesh successive differences
must decrease; the fine mesh, halved timestep, enlarged domain, and halved
sampling interval must change derivative RMS norms by less than five percent;
two independently implemented polynomial derivative estimators must agree in
interior RMS to ten percent; and zero/half-amplitude and factor-of-three
mutations must produce their prescribed zero/linear/factor-nine changes.
No frequency, luminosity scale, or source comparator selects a candidate.

## Proposed Claim Delta

Provisional `C-GW-005` would state the exact arbitrary-axis result for
`S(t)=alpha(t)*(e e^T-I/3)`: Frobenius norm
`S_ij S_ij=2 alpha^2/3`, zero cross polarization in the natural meridian
basis, conventional plus readout `alpha*sin(i)^2/2`, and the corresponding
conditional normalized/triple waveform and power conversions. Provisional
`C-GW-006` would separately record only endpoint-qualified finite-time
second/third derivative and conditional waveform/power coefficient traces if
all frozen numerical gates close. It would depend on `C-PDE-004` and
`C-GW-005`, remain simulation evidence and epistemically qualified, and make
no physical-radiation assertion.

## Implementation and Oracle Plan

A pure package API will construct and validate arbitrary-axis axisymmetric STF
tensors, return normalized and conventional TT polarization readouts, and map
normalized or triple conventions to conditional waveform and power
coefficients. SymPy is the primary oracle for trace, norm, projector,
inclination, and factor-of-three identities; rotated Cartesian evaluation is
an independent exact/numeric route. Mutations will delete trace subtraction,
replace the triple power coefficient by `G/5`, and perturb the symmetry axis.
If numerical promotion is attempted, the C-PDE-004 velocity-Verlet system will
be rerun at its declared domain and IVP with three spatial meshes, timestep
halving, domain enlargement, and two aligned sample intervals. Derivatives
will be evaluated only on the frozen interior interval using a local
least-squares polynomial differentiator and an independent quintic spline or
Savitzky-Golay route. RMS relative differences use a symmetric denominator
with an explicit near-zero guard. Solver success and finite values precede
all derivative use; zero and half amplitude test linear scaling. Campaign code
imports package APIs and replays the exact GW consumers plus P046.

## Attempts and Continuation

Six attempts are preserved. Attempt 0001 closes the bounded derivative study;
attempt 0002 exposes and removes a self-referential source-string ceremony;
attempt 0003 closes the full primary verifier but leaves formal `epsilon`
implicit in two result labels; attempt 0004 repairs that scope notation;
attempt 0005 catches stale independent-review artifact keys; and attempt 0006
combines the unchanged status-zero primary result with the repaired
independent review. Candidate A is selected. Candidate B remains the exact-only
fallback, while Candidate C is rejected by field, convention, and derivative
evidence.

## Debt Ledger

This ledger tracks STF normalization, polarization conventions, derivative
stability, conditional gravity scope, source mapping, and affected consumers.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| The existing source-specific axisymmetric result is not a general arbitrary-axis API | Derive, test, and independently rotate a pure implementation | discharged by C-GW-005 and the direct-projector review |
| Second and third derivatives of the finite-time l=2 trace are unverified | Close every frozen numerical gate or omit C-GW-006 | discharged by attempts 0004/0006 and the seven-point review |
| P3D4 may mix normalized and triple quadrupoles | Reproduce the source and audit every coefficient | discharged by the exact factor-nine audit |
| Conditional formulas may be narrated as physical radiation | Review every source sentence and preserve the gravity boundary | discharged by separate exact/numeric claims and qualified disposition |
| Direct and downstream consumers are not inventoried or replayed | Run impact analysis and targeted/global replay before promotion | discharged by graph inventory, 60 tests, and P042/P043/P046 replay |

## Review and Promotion Plan

Exact and numerical statements received separate accepted reviews and evidence
axes. The importable APIs, tests, immutable attempts, source reproduction,
sentence-level adjudication, impact inventory, qualified P3D4 mapping,
registry and v0.42 release transaction, targeted replay, and full repository
gate constitute promotion. P3D4 remains qualified rather than blanket
accepted.

## Done Gate

P047 closes with `C-GW-005/006`, independently verified exact and numerical
objects, qualified P3D4 disposition, status-zero consumer replay, synchronized
generated and durable state, and an empty campaign debt ledger. The parent
corpus-migration effort remains active and continues to the next pending unit.
