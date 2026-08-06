---
description: Audit MK1 medium-to-BPS potential matching and coefficient closure
author: vantasner
created: '2026-08-06T09:26:17Z'
updated: '2026-08-06T09:26:17Z'
tags:
- substrate-framework
- campaign-proposal
- migration-MK1
- bps-potential
- normalization
category: proposals
confidence: exploratory
status: active
---
# P214 MK1 Medium Potential Matching Audit

## Question and Positive Deliverable

P214 must derive the exact coefficient relation obtained when a declared
BPS-Skyrme potential is matched to a normalized periodic mass term and decide
whether accepted framework claims independently supply the required
medium-to-BPS map. The positive deliverable is a convention-complete matching
ledger, a claim-level adjudication of every MK1 predicate, and a terminal MK1
disposition. Finding that a physical medium or pion interpretation is missing
does not by itself complete the campaign.

## Base Release and Provenance

The accepted base is v0.155.0 at clean framework commit `388a6ad`, with 197
accepted claims, 11 pending units, and 194 qualified units. MK1 is pinned at
source commit `6d1f4e0`, SHA-256 `98ff5459...3222`, and 19,743 bytes. Its
candidate dependencies are E1 through E4, KI2, MC1, MK2, NY1, PG2, and S3 at
their registered dispositions. MK2 is pending and grants no authority. The
source checkout is dirty outside the hash-pinned MK1 file, so unrelated newer
prose and edits are excluded.

The generated queue exposes seven literal check sites, one assertion, and
truncated claims about `V=1-cos(F)`, `F=2*pi/F_pi`,
`mu_BPS=m_pi*F_pi/2`, and a downstream tail check. The source body, remaining
equations, imports, predicate bodies, guard, output, and consumer details stay
unopened through this contract and freeze.

## Invariants, Conventions, and Allowed Imports

C-BRK-001 says that `A*(1-cos(q*pi/F))` with scalar kinetic coefficient `K`
has generalized mass squared `A*q^2/(K*F^2)`. C-CHI-002 fixes the matching
SU(2) trace and kinetic convention but derives no chiral action, physical pion,
decay scale, coefficient, or substrate map. C-BPS-001 takes `lambda_BPS`,
`mu_BPS`, and `V(U)` as supplied. C-MED-003 uses a dimensionless 1+1 field and
an onsite energy-per-length coefficient `mu_medium`, retains a common action
scale, and does not identify that coefficient with the BPS square-root
potential coupling.

Symbols with the same spelling remain different typed objects until their
field coordinate, dimensions, action measure, and normalization are mapped.
Local Hessian equality remains weaker than equality of global periodic
potentials. A tail obtained from the same kinetic and potential coefficients
is a dependent consequence, not an independent coefficient oracle. Mutable
integration uses `np.trapezoid` or `trapezoid_integral`; an immutable
version-only abort receives an alias-only replay and never becomes a
scientific failure.

## Candidate Preregistration

Eight candidates separate local matching, global equality, accepted
composition, cross-sector typing, tail evidence, identifiability, possible API
novelty, and terminal governance.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Convention-covariant local match | Declared periodic amplitude and scalar kinetic metric | positive `mu_BPS,m,F,K,q` | `mu_BPS=m*F*sqrt(K)/q` | Derive the Hessian ratio and mutate `q` and `K` |
| B | Full-potential match | Same periodic angle, amplitude, action measure, and field map | both model coefficients | Stronger than a local mass match only when the global functions coincide | Compare period, amplitude, derivatives, and measure |
| C | Accepted conditional specialization | C-BRK-001 and C-CHI-002 with `q=2,K=1,A=mu_BPS^2` | supplied `m,F` | `mu_BPS=m*F/2` is exact but not a new derivation | Nonduplication audit against claims and APIs |
| D | Explicit medium-to-BPS map | Field, dimension, measure, and coefficient conversion | mapping data | No cross-sector inference without all map components | Remove each component and require identification to fail |
| E | Tail as dependent consequence | Independently fixed kinetic and potential pair | tail frequency or exponent | Reusing the same coefficient does not confirm it independently | Dependency graph and symbolic substitution audit |
| F | Residual coefficient family | Shape or gap ratios without absolute action normalization | one or more scale parameters | Kinematics can remain fixed while energy/action scale varies | Exact common-rescaling counterexample |
| G | Novel reusable BPS matching API | An exact survivor not already exposed | only necessary symbolic inputs | Extraction is warranted only for a distinct theorem | Registry and package nonduplication audit |
| H | Terminal MK1 governance | Accepted predecessors only | none | MK1 closes without MK2 authority | Graph, consumer, registry, release, and memory replay |

## Selection Criteria and Blinding

Selection prioritizes exact object and coordinate typing, accepted dependency
closure, assumption economy, coordinate covariance, dimensions, signs,
positivity, limits, sensitivity to `q`, `K`, trace prefactors and map removal,
the distinction between local and global matching, and novelty beyond existing
claims. A numerical value cannot select a candidate. Only generated queue
metadata is exposed before proposal, formula, provenance, repository, memory,
and commit gates freeze.

## Proposed Claim Delta

P214 provisionally reserves C-BPS-004 for a BPS-specific coefficient-matching
theorem if a nonduplication audit finds a novel exact surface. The identifier
has no pre-P214 hit in the registry, campaigns, proposals, durable memory,
package, tests, generated documentation, or migration records. Candidate C is
preferred if C-BRK-001 and C-CHI-002 already own all exact algebra; in that
case C-BPS-004 remains reserved and unpromoted, and MK1 maps existing claims
rather than manufacturing novelty.

## Implementation and Oracle Plan

SymPy will differentiate the declared periodic potential, divide by the
declared kinetic metric, solve the positive coefficient relation, compare
global functions, and derive tail equations only after their dependency graph
is explicit. Exact mutations change the angle multiplier, kinetic metric,
trace prefactor, field map, and common medium coefficient scale. A quadratic
potential with the same Hessian is the global-equivalence counterexample.

The compatibility preflight scans MK1 and every direct, imported, dynamic, and
eagerly accessed executable dependency for legacy NumPy integration names
before native execution. Mutable consumers are repaired to `np.trapezoid` or
the canonical `trapezoid_integral`; immutable source receives an alias-only
recorded replay if needed. Native numeric or symbolic checks reproduce source
provenance only when exact accepted algebra already fixes the result.

## Attempts and Continuation

Attempt 0001 freezes the authority boundary, eight candidates, exact
coefficient formulas, map requirements, mutation set, tail-independence rule,
compatibility policy, and provisional claim identifier before source-body
inspection. If the medium-to-BPS interpretation fails, P214 continues through
the exact conditional matching object and terminal adjudication instead of
ending on the obstruction.

## Debt Ledger

The P214 ledger tracks BPS and medium coefficient types, dimensions, action
measures, field maps, angle multiplier, coordinate scale, kinetic metric,
trace prefactor, local curvature, global potential, physical ontology, tail
dependency, pending authority, compatibility, consumers, and generated state.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| MK1 predicates remain blinded | Reproduce once after committed freeze | open |
| The same symbol may hide different coefficient types | Build a typed dimensional and measure ledger | open |
| A local Hessian may be presented as a global model identity | Compare full functions and periods | open |
| A tail may circularly reuse the coefficient match | Trace every tail premise and construct a dependent-evidence audit | open |
| PG2's rejected normalization may leak into MK1 | Replay exact q, K, Z, and C conventions | open |
| Pending MK2 may grant backward authority | Replay the terminal graph without later imports | open |
| Compatibility may masquerade as science | Audit all executable integration-name access before native replay | open |
| Claim novelty and generated state remain unresolved | Complete nonduplication, review, disposition, generation, and the proper promotion or record-only gate | open |

## Review and Promotion Plan

Every MK1 predicate receives an individual verdict. A novel theorem requires
canonical code and tests, primary and independent exact routes, claim review,
impact analysis, registry and release updates, generated documentation,
synchronized memory, and one integrated promotion gate. If no claim changes,
MK1 still requires materialized evidence, terminal disposition, consumer
replay, and record-sensitive validation without rerunning an unchanged full
suite.

## Done Gate

The campaign closes only when the exact positive matching ledger, dependency
typing, source reproduction, mutation-sensitive verification, individual
claim review, terminal source disposition, downstream replay, canonical
records, and debt ledger all agree. A version-only NumPy event, failed physical
interpretation, or passing source tally is not completion.

## Cross-References

This contract links v0.155.0, C-BRK-001, C-CHI-002, C-BPS-001 through
C-BPS-003, C-MED-003, C-SG-017, P061, P095, P107, P172, E1 through E4, KI2,
MC1, MK1, pending MK2, NY1, PG2, S3, the proposal manifest, formula freeze,
provenance record, future verifier and review, migration registry, generated
documentation, and durable framework-migration effort memory.
