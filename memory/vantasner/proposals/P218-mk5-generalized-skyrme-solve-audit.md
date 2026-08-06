---
description: Audit MK5 conditional generalized-Skyrme radial solve
author: vantasner
created: '2026-08-06T11:12:42Z'
updated: '2026-08-06T11:12:42Z'
tags:
- substrate-framework
- campaign-proposal
- migration-MK5
- generalized-skyrme
- numerical-evidence
category: proposals
confidence: exploratory
status: active
---
# P218 MK5 Generalized-Skyrme Solve Audit

## Question and Positive Deliverable

P218 must derive the exact conditional rational-map L2+L4+L6+L0 radial
functional and determine which stationary branches survive independent,
refined numerical solvers. A successful deliverable includes reusable model
and solver APIs if they are novel, plus a terminal MK5 disposition. A failed
source solve or rejected physical interpretation is attempt evidence and does
not complete the campaign.

## Base Release and Provenance

The base is v0.156.0 at clean commit `fc6a036`, with 198 accepted claims and
seven pending units. MK5 is pinned at source `6d1f4e0`, SHA-256
`a5ecb5d...246f8`, and 26,426 bytes; its file is clean while unrelated source
worktree changes are excluded. The queue exposes eight checks, one assertion,
the generalized radial density, source coefficient formulas, and the squared-
Jacobian angular-factor claim. Remaining source content stays blinded through
the committed freeze.

## Invariants, Conventions, and Allowed Imports

C-RPROF-001/002 own only the conditional L2+L4 model and its resolution-
bounded branches. C-RMAP-001/002 own angular definitions and selected inputs,
not physical baryons. C-BPS-001 uses the `lambda_BPS^2*pi^4*B0^2`
convention; C-VEC-002 maps `lambda_A=pi^2*lambda_BPS` but supplies no physical
vector or current. MK1-MK4 grant no physical potential, coupling product,
epsilon, or full-model solve. Positive `c6` and nonnegative `c0` may instead be
declared independently as dimensionless model inputs.

## Candidate Preregistration

The candidates separate the exact variational model, angular factor,
canonical and independent branches, refinement, limiting cases, convention
conversion, physical firewall, mutations, numerical fallback, and governance.

| Candidate | Description | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- |
| A | Exact extended radial functional and equation | May define a novel conditional API | Independent symbolic variation and positivity |
| B | Squared-Jacobian angular factor | Should use the declared angular functional I | Pullback-density reduction and B-squared mutation |
| C | Canonical stationary branch | Survives only with explicit endpoint data and solver status | Checked BVP or shooting residuals |
| D | Independent branch | Must use a distinct representation and quadrature | Like-for-like profile and energy agreement |
| E | Isolated refinement | Only converged quantities earn numeric evidence | Mesh/domain/cutoff/tolerance/quadrature tables |
| F | L2+L4 limit | Must reproduce C-RPROF surfaces at c6=c0=0 | Exact equation and numeric baseline replay |
| G | Lambda conventions | Conversion must be explicit before c6 evaluation | Coefficient derivation in both conventions |
| H | Physical firewall | Supplied coefficients may survive while derived physical claims fail | Premise-removal replay |
| I | Mutation suite | Load-bearing changes must alter profiles or verdicts | Coefficient, angular, tail, and degree mutations |
| J | Numerical fallback | A failed representation triggers another method | Preserved attempt plus repaired solver |
| K | Terminal governance | MK5 closes without later authority | Predicate, graph, queue, and memory replay |

## Selection Criteria and Blinding

Selection prioritizes exact variation, positivity, typed normalization,
accepted dependency closure, correct angular and lambda conventions, solver
status, endpoint/equation residuals, isolated convergence, independent method
agreement, limiting cases, mutation sensitivity, novelty, and terminal
closure. Comparator proximity cannot select a branch, coefficient, or method.
Remaining source settings and values stay blinded until the freeze commits.

## Proposed Claim Delta

P218 provisionally reserves C-GSK-001 for the exact conditional extended radial
model and C-GSK-002 for any independently converged stationary-branch evidence.
The identifiers are promoted only if they are distinct from C-RPROF-001/002,
implemented under `src/substrate_framework/`, tested, independently reviewed,
and dependency closed. Physical coupling, particle, nuclear, or binding
extensions are excluded from those proposed statements.

## Implementation and Oracle Plan

SymPy will independently vary the declared density, prove positivity, derive
the scaling identity and endpoints, and recover the L2+L4 limit. Numerical
work uses explicit double-precision equations, regular-origin and appropriate
massive or massless tail data, checked SciPy status, residual norms, and
separate mesh, output-quadrature, outer-domain, inner-cutoff, and tolerance
refinements. One route may use shared checked collocation; the other must use a
different representation such as vacuum-complement shooting or an independent
variational discretization and different quadrature. Integration compatibility
is preflight before native source execution.

## Attempts and Continuation

Attempt 0001 freezes eleven candidates, two provisional claims, the exact and
numeric obligations, coefficient and angular conventions, physical firewall,
compatibility policy, and continuation behavior before opening MK5.

## Debt Ledger

The ledger tracks equations, coefficients, angular factors, endpoint laws,
branch identity, solver status, refinements, independent methods, physical
premises, compatibility, consumers, novelty, and generated records.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| MK5 predicates settings and values remain blinded | Reproduce after committed freeze | open |
| Extended Euler-Lagrange equation may be copied or wrong | Independent symbolic variation and mutation | open |
| Sextic angular factor may conflate I and B squared | Exact angular reduction and counterexample | open |
| Source solver may hide failure or boundary artifacts | Inspect status residuals data and isolated refinements | open |
| Independent route may share the same representation | Eliminate shared intermediates and use distinct solver/quadrature | open |
| Source coefficients may mix lambda conventions | Derive lambda_A and lambda_BPS reductions explicitly | open |
| MK1-MK4 may leak rejected physical premises | Remove each premise and type surviving supplied parameters | open |
| Numeric agreement may become a physical claim | Keep claims conditional and comparator-blind | open |
| Compatibility may masquerade as science | Audit direct imported dynamic and eager integration access | open |
| Later consumers may grant backward authority | Replay terminal source graph | open |
| Novelty and governed records remain unresolved | Nonduplication review implementation release and record gate | open |

## Review and Promotion Plan

Each MK5 predicate and each provisional claim receives an individual review.
Promotion requires importable pure APIs, targeted tests, fresh independent
derivation, accepted-registry and release updates, generated docs and memory,
and a full downstream gate. If no claim survives, MK5 still needs a supported
terminal disposition and the parent effort continues to another positive
solver candidate rather than stopping at failure.

## Done Gate

P218 closes only with an exact positive generalized-model ledger, independently
verified numerical scope where claimed, mutation-sensitive evidence, every
predicate and consumer adjudicated, synchronized records, and empty campaign
debt. Source convergence or a no-go alone is insufficient.

## Cross-References

See v0.156.0, C-RMAP-001/002, C-RPROF-001/002, C-RDIFF-001/002,
C-BPS-001/002/003, C-VEC-002, P104/P105, P107, P214-P217, E1-E4, KI3-KI5,
MK1-MK6, and the framework migration effort.
