---
description: Audit EM5's one-loop induced or emergent gauge-sector claim
author: vantasner
created: '2026-08-09T03:30:00Z'
updated: '2026-08-09T03:30:00Z'
tags: [substrate-framework, campaign-proposal, scalar-qed, vacuum-polarization, migration-EM5]
category: proposals
confidence: exploratory
status: active
---
# P135 EM5 Induced Gauge Audit

## Question and Positive Deliverable

P135 must reproduce and adjudicate EM5's claim that integrating out an assumed
charged complex scalar in 1+1 dimensions generates a transverse gauge
quadratic action. The positive deliverable is an importable, input-explicit
one-loop vacuum-polarization ledger that distinguishes a local kinetic term, a
nonlocal transverse kernel, and any pole statement, or an exact terminal
mapping of the surviving tensor algebra if no distinct quantum claim closes.

## Base Release and Provenance

The accepted base is v0.102.0 at scientific commit `f20f7ad`; the parent
migration checkpoint is `1091175`. EM5 is pinned to
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`, path
`merged-framework/bridges/phase-3/bridge_EM5_induced_gauge_sector.py`, SHA-256
`bcf2c49e1e98eefea98be0076afd29341ce80fd71a7b141618978139982e4ec0`.

The queue exposes eleven literal checks, one assertion, a symbolic oracle hint,
and dependencies EM1, EM2, EM3, EM7, and M1. EM1 is qualified through
C-U1-001/C-U1-002, EM2 through C-GAU-001, and EM3 through C-MAX-001. EM7 and M1
remain pending. P134 already executed EM5 as a reverse consumer and exposed its
body, successful tally, and claimed result; P135 records that limitation and
does not claim source or comparator blindness.

## Invariants, Conventions, and Allowed Imports

C-U1-001 supplies a conditional classical current for an independently
declared complex scalar. C-GAU-001 supplies conditional local covariance and
curvature but no quantum field, loop measure, kinetic coefficient, photon,
force, or physical charge. C-MAX-001 supplies a Maxwell equation only after the
kinetic coefficient, current, dimension, source, and boundary data are supplied.
Pending EM7 and M1 are evidence rather than authority.

The independent quantum candidate is a declared Euclidean complex scalar with
operator `-D^2+m^2`, `D_mu=partial_mu-i*e*A_mu`, and a separately supplied bare
gauge quadratic term. Bubble and seagull diagrams, determinant sign and
multiplicity, a gauge-preserving regulator or restoring counterterms,
renormalization conditions, and analytic continuation remain explicit inputs.

For nonzero Euclidean `q^2`, the projector
`P_mu_nu=delta_mu_nu-q_mu*q_nu/q^2` is transverse and idempotent by definition
but undefined at zero momentum. `P_mu_nu*Pi_hat(q^2)` differs by a factor of
`q^2` from `(q^2*delta_mu_nu-q_mu*q_nu)*Pi_scalar(q^2)`. A constant multiplying
the projector is a nonlocal `F*(1/box)*F` kernel, whereas a local Maxwell term
is the analytic coefficient of the second form. The `q^2 -> 0` and `m -> 0`
limits, counterterm freedom, field normalization, species multiplicity,
statistics, and charge normalization cannot be hidden.

## Candidate Preregistration

The candidate set separates literal replay, a complete scalar-loop derivation,
kinematic tensor algebra, renormalized-family freedom, and governance closure.

| Candidate | Construction | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal EM5 replay | Source conventions | Source values | Some tensor identities may pass while loop inputs remain declared | Eleven-predicate AST and data-flow audit |
| B | Full scalar-QED loop ledger | Complete complex-scalar quantum action and gauge-preserving prescription | `e,m,q^2`, multiplicity, subtraction | Transverse kernel and limits close conditionally | Bubble-plus-seagull reduction, Ward identity, and independent parameter integral |
| C | Tensor-only qualification | Supplied transverse scalar kernel | `Pi_hat` or `Pi_scalar` | Projector algebra survives without a loop theorem | Zero-momentum domain and constructed-kernel countermodels |
| D | Renormalized conditional family | Local counterterms and field normalization explicit | subtraction point and bare coefficient | No universal induced coupling or mass | Counterterm, rescaling, statistics, and limit-order mutations |
| E | Governance closure | Accepted authority order | None | Narrow terminal disposition | Dependency, consumer, impact, novelty, queue, and generated-state replay |

## Selection Criteria and Blinding

Selection is ordered by accepted dependency closure, complete quantum action
and measure, fixed metric/Fourier/tensor/determinant conventions, derivation of
bubble plus seagull terms before imposing transversality, a regulator-valid Ward
identity, exact distinction between the two transverse scalar conventions,
dimensions and known limits, noncommuting limit order, counterterm and field-
rescaling honesty, independent derivation, mutation sensitivity, parameter
economy, reusable API value, consumer compatibility, and nonduplication.

Genuine blinding is unavailable because P134 exposed EM5's formulas, result,
and tally. The source's known coefficient and pole language are quarantined
from selection; this contract freezes the independent action, candidates,
criteria, and physical ceilings before fresh body inspection.

## Proposed Claim Delta

P135 reserves C-VAC-001 for a possible exact conditional complex-scalar
vacuum-polarization ledger. It may depend on C-GAU-001 and C-MAX-001 only if the
complete loop action, regulator, renormalization, tensor normalization, and
limit domains close. It will not assert that the accepted classical complex
field is quantized, that local covariance generates a loop, that a coefficient
is universal, or that the framework contains a physical photon, electric
charge, material gauge sector, substrate mechanism, or observation.

## Implementation and Oracle Plan

After the freeze commit, the primary route will hash, parse, and execute EM5,
map all eleven predicates, inventory imports and constants, and reconstruct its
projector, Ward identity, parameter integral, massless and massive limits,
effective action, and pole equation. The compatibility preflight uses the
canonical AST audit: mutable scripts use `np.trapezoid`, direct/imported/dynamic
legacy names and eager nested defaults are detected, and immutable source gets
only an alias replay when necessary.

SymPy exact tensor, rational-integral, series, and limit algebra is the primary
oracle. A fresh route will derive the bubble-plus-seagull tensor and Feynman-
parameter scalar without importing any new canonical helper. If a closed form
is impractical, high-precision mpmath quadrature with declared endpoint,
precision, subdivision, and convergence is regression evidence only, not an
independent proof. Removing or flipping the seagull, changing statistics,
charge, mass, multiplicity, subtraction, tensor convention, or field
normalization must move or break the relevant verdict. Zero charge, zero
species, heavy mass, zero momentum, massless-first, momentum-first, and bare-
coefficient limits remain explicit.

The impact audit covers any proposed API and all reverse consumers. Campaign
verifiers depend only on frozen evidence and accepted modules, never on a
future queue state or mutable current release.

## Attempts and Continuation

Attempt 0001 freezes this contract and records the compromised-blinding fact
before any fresh EM5 body inspection. Every failed implementation, tensor
reduction, limit, oracle, or source-replay route will be appended with its
mechanism and next repair; no failed route can complete the positive object.

## Debt Ledger

The ledger tracks source, quantum-action, regulator, renormalization, tensor,
limit, pole, dependency, consumer, novelty, and physical-scope debt.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| EM5 executable surface freshly unaudited | Hash, execute, AST/data-flow audit, and map all eleven predicates | open |
| Quantum action and loop measure incomplete | State field, statistics, multiplicity, determinant, vertices, and bare gauge term | open |
| Ward identity may be imposed by ansatz | Derive bubble plus seagull under a declared regulator and mutate a load-bearing term | open |
| Polarization normalization untyped | Separate `Pi_hat*P` from `Pi_scalar*(q^2 delta-qq)` with dimensions | open |
| Renormalization and local term unresolved | State subtraction/counterterm freedom and derive any local coefficient | open |
| Massive/massless and zero-momentum limits unresolved | Derive domains and both limit orders with infrared behavior | open |
| Pole or mass statement unclosed | Derive it from the full supplied bare-plus-loop kernel and test field rescaling | open |
| Physical language ungoverned | Separate conditional scalar QED from photon, material, substrate, and observation claims | open |
| Dependencies, consumers, and novelty unknown | Audit EM1/EM2/EM3/EM7/M1, reverse consumers, accepted APIs, and generated state | open |

## Review and Promotion Plan

C-VAC-001 receives an individual review only if the complete conditional loop
theorem survives both derivations and mutations. Source adjudication separately
classifies EM5. Reusable logic moves into a pure package module with focused
tests; literal source orchestration stays in the campaign. Dependency, impact,
consumer, novelty, generated-state, queue, release, documentation, and memory
replay close any promotion. A terminal qualification or refutation names its
reason and durable evidence even if no claim is accepted.

## Done Gate

P135 closes only with the positive, convention-complete loop object or an exact
accepted composition that already supplies every supportable part, plus
claim-level review, terminal EM5 disposition, sensitive oracle evidence,
downstream replay, synchronized governance, and an empty campaign ledger. A
source no-go or unsupported headline is evidence and triggers the next
candidate; it is not success by itself.

## Cross-References

See P014, P030, P064, P134, EM1, EM2, EM3, EM5, EM7, M1, C-U1-001,
C-GAU-001, C-MAX-001, v0.102.0, and the parent framework-migration effort.
