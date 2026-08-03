---
description: Independent review of the declared cubic degree-four rational-map sphere evaluation
author: vantasner-review
created: '2026-08-07T12:22:00Z'
updated: '2026-08-07T12:22:00Z'
tags:
- substrate-framework
- claim-review
- rational-map
- numerical-cubature
category: decisions
confidence: established
status: archived
---
# Review of C-RMAP-002

## Claim Under Review

C-RMAP-002 evaluates the fully declared rational map
`(z^4+2*i*sqrt(3)*z^2+1)/(z^4-2*i*sqrt(3)*z^2+1)`. Exact polynomial algebra
makes the pair coprime and degree four. Separately refined homogeneous-Wronskian
tensor cubature and independent adaptive two-chart integration give normalized
pullback area four and angular functional `20.6496264884189` at the stated
binary64 resolution and tolerances. This is evaluation evidence only: the claim
does not assert cubic symmetry, global degree-four minimality, a radial solution,
physical baryon or nuclear identity, energy, binding, reaction, or yield.

## Sourced Inputs

The review uses C-RMAP-001 as its sole accepted scientific dependency, the
exact supplied polynomial coefficients, P104's frozen contract and attempts,
both numerical routes, source and consumer audits, and focused tests. E1's
advertised `20.63`, literature language, map label, and later consumer values
are comparators or noncanonical context, never derivation inputs.

## Independence

The independent reviewer imports no canonical rational-map code. It reverses
the coefficient arrays in the reciprocal chart, directly evaluates the
homogeneous Wronskian, and performs nested SciPy adaptive integration at
tolerances `1e-7`, `1e-9`, and `1e-11`. Exact gcd/degree is recomputed with a
fresh polynomial representation. Agreement with the tensor route is checked
only after both methods return finite area and angular values.

## Verification Status

The maximum status is `numeric_evidence`. Coprimality and degree are exact, but
the load-bearing angular value is numerical. Tensor orders from `16x32` through
`64x128` converge to `20.6496264884189`; the area converges to four. The
independent adaptive route agrees within the frozen relative gate and reports
finite error estimates and evaluation counts. Tight tolerances do not turn the
decimal into an exact theorem.

## Sensitivity and Counterexamples

Changing the imaginary quadratic coefficient from `2*sqrt(3)` to `3.2`
preserves degree area but raises the angular value by more than `0.1`, so the
coefficient is load bearing. Independent domain and target axial rotations
preserve both integrals. The exact degree-two control and identity normalization
reject E1's endpoint-excluding quadrature. A shifted degree-two map evaluates
higher but is retained only as a counterexample to the source's minimization
logic, not as evidence for this degree-four value.

## Framework Compatibility

The claim is a compatible specialization of C-RMAP-001. It changes no accepted
invariant. Every polynomial coefficient, chart, precision, quadrature order,
tolerance, and error gate is explicit. It supplies no mechanism for selecting
this map from all degree-four maps and imports no physical action or state map.

## Dependency and Consumer Replay

The only canonical consumers are additive exports, focused tests, and P104's
two verifiers. No accepted execution path depends on the number. Pinned E2,
E3, KI5, TX1, TX4, MK5, and MR5 duplicate a biased predecessor value and add
unaccepted radial or physical premises; their own campaigns must replay the
corrected canonical input. GitNexus reports LOW additive risk with no affected
pre-existing process. Canonical cubature uses neither `np.trapz` nor direct
sampled trapezoidal reduction.

## Competing Candidate Audit

The tensor, adaptive two-chart, exact-control, coefficient-mutation, rotation,
and minimization-ceiling routes were frozen before source execution. The
declared-map evaluation is selected because two structurally different methods
meet the area, refinement, and mutation criteria. The exposed `20.63`
comparator did not select the method or tolerance.

## Four-Axis Decision

The integrated promotion gate closes the review decision as acceptance.

- Verification: `numeric_evidence`
- Review: `accepted`
- Compatibility: `compatible_extension`
- Epistemic: `active`
- Relationship: specializes C-RMAP-001; challenges and supersedes none

## Promotion Transaction

Promotion adds C-RMAP-002 alongside C-RMAP-001 in release `v0.88.0`, with the
pure evaluator, tests, independent review, corrected E1 disposition, generated
state, and no accepted consumer debt. The numeric and exact claims remain
separate records.

## Continuation if Not Accepted

If the gate fails, P104 preserves the failed route and repairs cubature,
precision, chart regularity, evidence closure, or consumer replay. It does not
widen tolerances, borrow the source decimal, or promote global minimality.

## Done Gate

Acceptance requires exact map identity and degree, two independent numerical
methods, explicit refinement and errors, coefficient and rotation sensitivity,
source-bias detection, complete consumer classification, synchronized records,
and an empty claim-level debt ledger. The sequential E2 campaign remains the
next place to test downstream radial sensitivity.

## Cross-References

See P104, E1, C-RMAP-001, the rational-map module, proposed release `v0.88.0`,
and the framework-migration effort.
