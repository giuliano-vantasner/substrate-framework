---
description: Derive and audit the exact current content of W3's proposed V-A charged-current bridge
author: vantasner
created: '2026-08-09T23:40:00Z'
updated: '2026-08-10T01:00:00Z'
tags:
- substrate-framework
- campaign-proposal
- migration-W3
- current
category: proposals
confidence: exploratory
status: archived
---
# P148 W3 V-A Current Audit

## Question and Positive Deliverable

P148 must deliver an exact importable classification of W3's scalar derivative,
vector, axial, characteristic, boundary, and current statements. The positive
object must distinguish kinematic identities from conservation laws and
boundary balances, and distinguish all of those from an internal charged
current or interaction vertex. If every exact object is already accepted, a
complete qualified disposition rather than a duplicate claim is still a
positive framework result.

## Base Release and Provenance

The accepted base is v0.114.0 at framework checkpoint `49277be`, with
scientific promotion `0d623a5`. The source baseline is
`/home/dan/substrate` commit
`6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`; later dirty Phase 47/48 and
engineering files remain excluded. W3 is pinned at
`merged-framework/bridges/phase-6/bridge_W3_VA_charged_current.py`, SHA-256
`b49a0bd1075b16b5906719b6ed51454ed04adab5168be7ec98178599313b3f17`.
Its dossier is pinned at
`merged-framework/bridges/phase-6/dossiers/W3_dossier.md`, SHA-256
`c9b327bba0fa227083017173cae475728f061e7b82da0f1810dbfb9f74e00b5b`.
The queue exposes eight dependencies, seven literal checks, one assertion,
symbolic and numeric hints, two immutable legacy trapezoid calls, and no result
excerpt. Neither source body has been opened or executed before this freeze.

## Invariants, Conventions, and Allowed Imports

P148 preserves the normalized real sine-Gordon equation and C-SG-011's sourced
characteristic balances and topological-current ceiling, C-SG-012's (+,-)
metric and one-half light-cone conventions, C-SG-013's separation of correlation
from charge transfer, C-BND-001's W1 qualification, and C-REP-002's independent
carrier-factor correction to W2. C-U1-001 and C-GAU-001 may be used only as
distinct examples of the matter, current, equation, connection, and coupling
premises missing from a real scalar derivative identity. Pending source units
and rejected readings grant no authority.

The default tensor convention uses coordinates (t,x), signature (+,-), scalar
spatial parity `phi_P(t,x)=phi(t,-x)`, and orientation fixed consistently with
C-SG-011. Covariant, contravariant, vector, axial, topological, Noether, and
boundary objects must remain separately typed. Integrated statements require
explicit domains and flux conditions.

## Candidate Preregistration

The candidates and their discriminating tests are frozen before source-body inspection.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal W3 predicate audit | Hash-pinned source | Source formulas and samples | Retains only what each predicate evaluates | AST, process, data-flow, compatibility, and mutation audit |
| B | Existing characteristic and stress identities | Accepted real sine-Gordon field | None beyond accepted conventions | Most scalar formulas are duplicate C-SG-011/C-SG-012 surfaces | Match exact expressions and ceilings without physical relabelling |
| C | Vector and Hodge-dual axial derivative ledger | Smooth real scalar, fixed metric and orientation | Overall normalization | Gives exact divergences, parity laws, duality, and null combinations but no internal charge | Independent tensor and differential-form derivations |
| D | Boundary flux and trace classification | Declared domain, boundary traces, and flux hypotheses | Boundary coefficients and data | Separates local balance, integrated flux, sign correlation, and topological transfer | General trace families and counterexamples |
| E | Internal current and gauge completion | Separate complex or spinor matter and declared connection/action | Charges and couplings | Shows which premises a physical vertex needs and their nonuniqueness | Construct distinct models sharing the same scalar derivative identity |
| F | Governance and graph closure | Frozen dependencies and consumers | None | No circular or pending source authority enters acceptance | Hash, disposition, compatibility, and downstream replay |

## Selection Criteria and Blinding

Selection is ordered by tensor and field-type correctness, separation of
identity from conservation and interaction, nonlinear sine-Gordon compatibility,
parity semantics, dimensional and boundary closure, known limits, mutation
sensitivity, assumption economy, reusability, nonduplication, and consumer
closure. Queue-visible hints do not select a candidate. Exact predicates,
formulas, numerical samples, output, thresholds, and further comparator
material remain blinded until this contract and matching manifest are committed.

## Proposed Claim Delta

No identifier was reserved at the initial freeze. Source-aware nonduplication
now selects Candidate B and parts of C through E as an exact classification
already governed by C-SG-011 through C-SG-013, C-BND-001, C-REP-002, and
C-U1-001. Revision 0001 freezes a zero-claim, zero-release, zero-module delta.
The canonical characteristic, topological-current, boundary, U1, and SU2 APIs
already provide the positive object; P148 adds source-specific verification and
a qualified W3 disposition without duplicating them.

## Proposal Revision

Revision 0001 records the exact convention-explicit result before verifier
implementation. For a smooth real scalar, the raised derivative
`D=(phi_t,-phi_x)` has divergence `Box(phi)`, while the epsilon-dual
`T=(phi_x,-phi_t)` is exactly off-shell conserved. Their sums and differences
are the accepted null derivative combinations, and parity exchanges them. For
`phi=L(t+x)+R(t-x)`, direct chain rule gives
`phi_x=L_prime-R_prime`, so the plus characteristic is `2L_prime` and the
minus characteristic is `2R_prime`. This corrects W3's internal sign and
channel mismatch without creating an internal charged current or interaction.

## Implementation and Oracle Plan

SymPy exact tensor and differential identities are the primary oracle for
tractable current, parity, and balance statements. Numerical integration can
only reproduce a source sample or exercise a genuinely sampled boundary
observable; it cannot strengthen an exact identity and may not select a
candidate. A fresh route will derive load-bearing signs and one-half factors
without importing any new canonical helper.

Mutations change a metric sign, orientation, derivative sign, light-cone
factor, parity pullback, boundary normal, source term, or flux hypothesis.
Countermodels separate nonzero characteristic combinations from conservation,
nonzero sign correlation from topological transfer, and identical scalar
kinematics from inequivalent matter or gauge dynamics.

The compatibility preflight uses the shared AST auditor. Mutable code must use
exact algebra, `trapezoid_integral`, or `np.trapezoid` and contain no
executable legacy access. W3's immutable two-call `np.trapz` shape will be
preserved as native compatibility provenance, then replayed through an explicit
alias-only binding to `np.trapezoid` before scientific adjudication. The
native abort does not reject a candidate.

## Attempts and Continuation

Every failed reproduction, convention, current, parity, compatibility, or graph
route is append-only with a diagnosed mechanism and materially different next
attempt. Technical failures are repaired and source overclaims yield to the
next preregistered candidate. Neither a version-only abort nor a scientific
no-go stops the parent migration.

## Debt Ledger

The ledger tracks field and carrier types, metric and orientation, raised and
lowered indices, current normalization and dimensions, equation and conservation
status, boundary flux, parity semantics, source and coupling provenance,
compatibility shapes, dependency cycles, broken consumers, and generated
state. The terminal disposition resolves or excludes every listed item. The
campaign is archived with no new claim, no release change, and no remaining
debt.

## Review and Promotion Plan

Every affected claim receives individual review. W3 receives a terminal
disposition that retains exact mathematical content while naming supplied or
unsupported physical readings. Any distinct claim is extracted into pure APIs
and focused tests only after a frozen revision. Dependencies, consumers,
compatibility, nonduplication, queue, generated docs, release state, and memory
are replayed. One integrated repository gate runs at the final transaction
boundary.

## Done Gate

P148 closed when a positive current-classification object existed through
accepted APIs or a separately reviewed exact addition, all seven predicates are
adjudicated, the native compatibility event and alias-only replay are preserved,
dependencies and reverse consumers close, generated state agrees, and the debt
ledger is empty. A physical charged-current or V-A interaction additionally
requires independently sourced matter, transformation, connection, action,
coupling, current, and dynamics; scalar derivative names cannot substitute.

The accepted route uses the already governed exact objects and qualifies W3.
Primary, fresh independent, and frozen-graph checks pass 47, 25, and 61 gates;
the integrated repository workflow passes all 1,289 tests. See adjudication
commit `feb8191` and the archived W3 decision record.

## Cross-References

See W3, C-SG-011, C-SG-012, C-SG-013, C-BND-001, C-REP-002, C-U1-001,
C-GAU-001, P048 through P050, P146, P147, the canonical sine-Gordon, boundary,
current, gauge, and SU2 carrier modules, and the parent migration effort.
