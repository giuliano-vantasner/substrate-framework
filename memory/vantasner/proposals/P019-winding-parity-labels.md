---
description: Separate exact winding-parity label algebra from EL2's fermion and baryonless-composite interpretation
author: vantasner
created: '2026-08-01T13:59:07Z'
updated: '2026-08-01T14:03:06Z'
tags:
- substrate-framework
- campaign-proposal
- topology-labels
- migration-EL2
category: proposals
confidence: exploratory
status: archived
---
# P019 Winding Parity Labels

## Question and Positive Deliverable
P019 must construct the exact integer-winding parity algebra actually supported
by EL2 and determine whether it licenses the source's fermion, baryon-number,
and charged-composite conclusions. The positive object is an importable
homomorphism `p(w)=(-1)^w`, its neutral-dressing invariance, and an explicit
separation between mathematical labels and physical spin-statistics. A no-go on
the physical reading alone does not complete the campaign.

## Base Release and Provenance
The accepted base is `v0.16.0` at commit `962422b`. `C-U1-001` and `C-U1-002`
supply only a conditional internal scalar charge and explicitly exclude quantum,
electric-charge, particle, and 3+1 interpretations. No accepted claim assigns
fermionic statistics, baryon number, kink winding, a physical composite, or a
contractible dressing target. The hash-pinned candidate is EL2 at
`merged-framework/bridges/phase-46/bridge_EL2_lepton_is_baryonless_fermion.py`,
SHA-256 `db90b921e0b3d6966597a39817ad48219cd94fa27ff8aa2a1de4a64c3ccf6965`.
Its listed dependencies remain pending except the narrow EM1 content already
captured by the U1 claims. Memory search surfaced historical fermion work but
it is neither project authority nor an allowed import.

## Invariants, Conventions, and Allowed Imports
Winding labels are integers under addition. The parity codomain is `{+1,-1}`
under multiplication. A label named parity is not automatically exchange
statistics, spin, fermion number, or baryon number. Internal U1 charge remains
conditional and may be continuous. No pending Lean theorem, composite mechanism,
3+1 lift, Standard Model label, or empirical particle property is admitted.

## Candidate Preregistration
The candidates are frozen before EL2's full body is read.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Promote exact winding-parity homomorphism and neutral-dressing invariance | Integer additive winding | none | Native reusable label algebra with an explicit physical ceiling | Prove homomorphism, odd/even classes, and mutations of neutrality |
| B | Preserve only source adjudication with no accepted label API | EL2 adds no useful content beyond elementary arithmetic | none | Preferred if no distinct consumer exists | Consumer and scope comparison after exact audit |
| C | Promote a forced charged baryonless fermion composite | Parity equated to statistics; baryon and charge assigned; dressing/existence imported | Multiple hidden sector premises | Conflicts with accepted U1 ceilings | Vary independent labels or remove spin-statistics map while exact parity survives |

## Selection Criteria and Blinding
Selection is ordered by exact group law, dependency closure, distinction between
labels and physical representations, assumption economy, reusable consumer
reach, and mutation sensitivity. Candidate A survives only with a real source
or later consumer and an explicit non-fermion ceiling. Candidate C must fail if
the same winding algebra admits multiple statistics, baryon, or U1 assignments.
EL2's numerical examples are excluded until the symbolic criteria freeze.

## Proposed Claim Delta
Provisional `C-TOP-001` states that `p:Z->{+1,-1}`, `p(w)=(-1)^w`, is a group
homomorphism; odd winding has label `-1`, even winding has `+1`, and adding
zero or any even winding leaves the label unchanged. The claim makes no map
from this label to fermionic exchange statistics, spin, baryon number, electric
charge, or existence of a dressed object. Its consumers are a new topology-label
API, EL2's disposition, and later governed topology proposals.

## Implementation and Oracle Plan
The package will gain pure integer winding-parity and combination APIs with
strict integer validation. Exact integer arithmetic is the right oracle. The
verifier will prove the homomorphism on symbolic integer exponents and a broad
finite counterexample grid, reject noninteger labels, mutate the dressing
winding, and show statistics/baryon/U1 labels remain independent variables.
An independent review will derive the quotient map `Z -> Z/2Z -> {+1,-1}`
without importing the API. EL2's source checks will be audited individually;
numeric reruns cannot strengthen an exact group law.

## Attempts and Continuation
Attempt `0001` will reproduce hash-pinned EL2 and test the exact label algebra
and physical ceiling. A representation failure will be repaired without
changing the candidate. If no consumer survives, the claim will be withdrawn
and the unit adjudicated without promotion. Unsupported fermion or composite
interpretations remain evidence and cannot count as the positive deliverable.

## Debt Ledger
The campaign starts with four explicit debts.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| “Parity” may be silently equated with statistics | Claim and API deny the map absent a premise | discharged |
| Neutral dressing may be assumed rather than declared | Mutation exposes nonzero/odd dressing | discharged |
| Baryon and U1 labels may be conflated with winding | Independent-label countermodels | discharged |
| Pending composite/existence sources may leak into authority | Import audit and source qualification | discharged |

## Review and Promotion Plan
Review will independently derive the quotient homomorphism, inspect integer
domains and countermodels, and map every EL2 check to exact label algebra,
declared premise, regression, or unsupported physical interpretation. Promotion
requires package APIs/tests, individual claim review, terminal EL2 disposition,
registry/release and generated-record synchronization, targeted replay, and one
full repository gate at the unchanged boundary.

## Results and Promotion
EL2's eleven source checks reproduce at the pinned hash. Attempt `0001` passes
eleven exact audit checks, the independent quotient route passes five, and
thirteen focused tests pass. `C-TOP-001` is accepted with no physical
spin-statistics mapping. EL2 is qualified because its composite map is not
constructed, its U1 charge is not fixed or electric, and its claimed Derrick
stable point has negative curvature and is a maximum.

## Done Gate
P019 is complete. The exact label object is importable and sensitive, the
statistics and charge ceilings are explicit, EL2 is terminally qualified, the
claim has individual review, consumers replay, and debt is empty.
