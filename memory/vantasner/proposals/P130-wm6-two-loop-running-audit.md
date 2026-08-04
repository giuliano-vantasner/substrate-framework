---
description: Audit WM6's conditional gauge-only two-loop boundary-running solve and all-orders overread
author: vantasner
created: '2026-08-08T21:00:00Z'
updated: '2026-08-08T21:00:00Z'
tags: [substrate-framework, campaign-proposal, renormalization, numeric-running, migration-WM6]
category: proposals
confidence: exploratory
status: active
---
# P130 WM6 Two-Loop Running Audit

## Question and Positive Deliverable

P130 must deliver a reusable, status-gated numerical solver for a declared
three-factor gauge-only boundary-running inverse problem, or reject that
candidate and continue. It must distinguish conditional output from prediction
and a uniform two-loop-matrix inverse fit from an all-orders no-go.

## Base Release and Provenance

The accepted base is v0.99.0 at parent checkpoint `c1ae7f1`; the latest
scientific transaction is P129 at `f124ca6`. WM6 is pinned to
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`, path
`merged-framework/bridges/phase-33/bridge_WM6_two_loop_running.py`, SHA-256
`6d1ea4245adcf490466974d4a40b24843cd92e883c6e885936fb030cd1b31d57`.

The queue records five candidate dependencies, eleven dynamic checks, one
assertion, NumPy and SciPy use, and a numeric oracle. SM2 and SM4 are pending;
WM1 and WM3 are qualified; WM5 contributes only C-RGE-005. Later candidate
consumers include WM8 and WM10; WM4 and WM5 form earlier provenance edges.

P129's required consumer replay already executed WM6 and exposed its full
terminal output. That provenance is unavoidable and explicitly weakens
blinding; P130 does not pretend otherwise.

## Invariants, Conventions, and Allowed Imports

The accepted input is C-RGE-005's gauge-only beta polynomial, not a full
Standard-Model beta function. C-RGE-004 supplies the conditional one-loop
inverse-reconstruction semantics and no physical boundary.

For inverse couplings `a_i=4*pi/g_i^2`, P130 freezes
`da_i/dlog(mu)=-b_i/(2*pi)-sum_j B_ij/(8*pi^2*a_j)`. The supplied high boundary
has one amplitude and fixed positive factor ratios. Two supplied low linear
constraints determine amplitude and log span. Every ODE and root status,
positive-coupling domain, tolerance, method, and residual norm remains visible.

Allowed machinery is exact SymPy algebra and SciPy `solve_ivp`, `root`, and
`least_squares`, using shared numerical tolerance records where they fit. No
measured weak coordinate may enter a solve that claims to output it.

## Candidate Preregistration

The candidates separate literal replay from a canonical inverse-coupling
solver, an independent direct-coupling formulation, an exact one-loop route,
numeric refinement, data-flow mutations, a uniform-matrix scaling audit, and
governance closure.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal WM6 reproduction | Source conventions | Source unknowns | Output repeats | Predicate-level audit |
| B | Canonical inverse-coupling solve | C-RGE-005 plus supplied boundary and constraints | Boundary amplitude and log span | Stable conditional output | Status residual and refinement gates |
| C | Direct-g rederivation | Same declared problem | Same two unknowns | Agrees with B | Independent variables and method |
| D | Exact one-loop limit | Matrix set to zero | Same inputs | Recovers C-RGE-004 | Exact versus numeric equality |
| E | Refinement family | Positive domain | Tolerances and methods only | Convergent output | Tightening and cross-method errors |
| F | Mutations and data gate | None beyond input typing | Load-bearing inputs | Verdict breaks | Sign transpose boundary and input probes |
| G | Uniform-matrix inverse audit | Artificial B to kB family | Free k | Fit is nonidentifying | Higher-order and threshold countermodels |
| H | Governance closure | Accepted authority order | None | Narrow claim only | Dependency consumer nonduplication review |

## Selection Criteria and Blinding

Selection is ordered by dependency closure, inverse-problem honesty, solver
status, exact one-loop containment, method independence, refinement, mutations,
omission scope, parameter economy, and reuse. Comparator closeness is excluded.

Pristine blinding is impossible: the queue and P129 replay exposed 0.20757,
0.21064, 0.23122, 8.90 percent, and about 8.75. Candidates, equations,
tolerances, and structural gates freeze now before P130 source reinspection.
Those exposed values cannot select the formalism or make an assertion pass.

## Proposed Claim Delta

P130 reserves C-RGE-006 for the narrow conditional numeric running object if it
survives. The claim would depend on C-RGE-004 and C-RGE-005, retain every
supplied boundary and low constraint, and explicitly exclude physical field
content, Yukawa terms, matching, thresholds, a preferred boundary, observation,
all-orders closure, and substrate identity.

Registry, campaigns, and durable memory contain no C-RGE-006. A no-new-claim
outcome remains available if the exact surface is only a transient source
specialization with no reusable implementation.

## Implementation and Oracle Plan

The candidate package module will expose the inverse-coupling ODE, a pure
three-factor problem record, status-rich solve evidence, exact one-loop
specialization, and the weak-coordinate readout. Imports must not run a solve.

The primary route uses double-precision SciPy with explicit DOP853 status,
`rtol` and `atol`, positive-domain event checks, root status, and residual norm.
It tightens tolerances by at least two steps. The independent route integrates
direct `g_i` variables with Radau or another structurally distinct method and
uses a separate least-squares shooting solve. Both must reproduce the exact
`B=0` limit before the two-loop result is admitted.

Mutations transpose or sign-flip B, change a boundary ratio, change a supplied
low input, and inject the weak comparator into a residual. The last mutation
must be detected as data leakage. Absolute reference-scale covariance and the
dimensionless log span are checked exactly or by a controlled rescaling.

The uniform `B -> k*B` root may be reproduced only as comparator-dependent
inverse evidence. Independent third-loop tensors, finite thresholds, or
matching offsets provide countermodels to the all-orders reading without being
adopted as physical repairs.

The compatibility preflight scans WM6 and every replayed consumer. Mutable
scripts use `np.trapezoid`; immutable source gets an alias-only replay only if
legacy `np.trapz` is the sole abort. Such an abort is not scientific failure.

## Attempts and Continuation

Attempt 0001 freezes this contract after recorded output exposure but before
P130 body reinspection. Every later failure is appended with its mechanism and
next materially different route.

## Debt Ledger

The campaign ledger tracks solver, formula, boundary, input, comparator,
perturbative-order, dependency, consumer, and generated-state debt.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| Prior comparator and output exposure | Record it and bar values from construction selection and pass gates | frozen |
| Numeric solver and shooting sensitivity | Status domain refinement independent method and exact limit | open |
| Full-beta and all-orders wording | Primary-formula and countermodel audit | open |
| Dependency and consumer closure | Claim-level mapping and pinned replay | open |

## Review and Promotion Plan

Primary and independent verifiers review the numeric object separately. Impact,
source, predicate, input, dependency, consumer, nonduplication, primary-formula,
and candidate audits precede claim-level review. If C-RGE-006 is accepted, its
module and focused tests enter a new release; otherwise WM6 receives a terminal
qualified mapping to existing claims only. Generated docs and memory are never
hand-edited.

One integrated repository gate runs per meaningful promotion boundary. A final
attempt is created in progress before that gate and finalized afterward; only
record-sensitive checks follow.

## Done Gate

P130 closes only when the conditional positive solver or a superior surviving
candidate exists in importable form, every source predicate and overread is
adjudicated, numeric and independent oracles are sensitive, consumers replay,
governance state agrees, and debt is empty. A residual or no-go alone is not
completion.

## Cross-References

See C-RGE-004, C-RGE-005, P083, P129, SM2, SM4, WM1, WM3-WM6, WM8, WM10,
v0.99.0, and the parent framework-migration effort.
