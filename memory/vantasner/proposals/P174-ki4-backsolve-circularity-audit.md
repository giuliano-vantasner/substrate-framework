---
description: Audit KI4's inverse-reconstruction circularity and zero-information claims
author: vantasner
created: '2026-08-11T03:32:00Z'
updated: '2026-08-11T03:35:00Z'
tags:
- substrate-framework
- campaign-proposal
- migration-KI4
- inverse-reconstruction
category: proposals
confidence: exploratory
status: active
---
# P174 KI4 Backsolve Circularity Audit

## Question and Positive Deliverable

P174 must determine exactly what KI4 proves about back-solving a parameter from
the same coefficient later called a prediction. The positive deliverable must
separate inverse identity, same-datum reconstruction, parameter identification,
a union over hypothetical observations, and independent predictive testing.

## Base Release and Provenance

The accepted base is v0.127.0 at clean framework commit `5034940`, with 163
accepted claims. The source baseline is
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`. KI4 is pinned at
`merged-framework/bridges/phase-34/bridge_KI4_backsolve_circularity.py`, SHA-256
`138f204c2bf7e7278a1a4aadad4bed1680e11b6b6de7189a02640a81652f00cd`.
The shared dossier and Lean capstone remain pinned at SHA-256
`e01fbee40d81ebae1fc6f9452c321e2914cb185cdf257ae226d849ea6392702b`
and `269c2b6b023fb1bfacb7dede2e708f09d3e08cad00bcc933e5149357ef5870f5`.
All three paths are clean at the governed source baseline and KI4's sole source
history commit is `7222eed21720c5174dd35ba8f825d8b7e0a48f3f`.

Generated inventory, P173 graph execution, earlier dossier excerpts, and memory
already expose KI4's identity, zero-information headline, four illustrative
maps, and comparator. P174 claims no fresh blinding and freezes its criteria
before a whole-body KI4 audit.

## Invariants, Conventions, and Allowed Imports

For a declared bijection `f` and target `y` in its range,
`f(f_inverse(y))=y` is an exact inverse identity. The resulting zero residual
on `y` is inverse reconstruction, not an independent validation of the same
equation. C-IDN-002 already makes this distinction for one accepted system.

Back-solving is not categorically invalid. Conditional on a fixed known
injective map and exact observed target, the inverse can identify a parameter.
Calibration becomes predictively testable only through held-out data, a
distinct observable, or an overidentifying row that was not used to solve the
parameter. A union across every hypothetical target must not be confused with
conditioning on the one target actually observed.

P173 retains KI3's four formulas only as explicit open-range examples and
rejects the universal physical bracket and common interpolation. C-XOV-001
owns exact conditional monotone inverse classification and preserves free-map,
scale, normalization, and physical-identification ceilings. No accepted claim
maps KI2's ratio or a KI3 witness to C-BPS-003's physical epsilon.

Comparator 0.929 may be a supplied target but cannot validate its own inverse
reconstruction or select the map. Mutable integration uses `np.trapezoid` or
the canonical helper; immutable legacy-name stops are version-only evidence.

## Candidate Preregistration

The candidates distinguish execution, inverse identity, same-datum
reconstruction, parameter information, hypothetical-output union, inverse
failures, held-out prediction, accepted composition, comparator isolation,
formal scope, and governance closure.

| Candidate | Description | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- |
| A | Literal KI4 replay | Execution evidence only | AST and native replay |
| B | Exact inverse composition | Valid under injectivity and range premises | Symbolic residual and domain mutations |
| C | Same-datum zero residual | Valid inverse-reconstruction classification | Mark the datum used in the solve and deny independence |
| D | Zero information about epsilon after exact observation | Expected false for fixed injective map | Compare prior and target-conditioned parameter sets |
| E | Union over hypothetical reconstructed outputs | Plausible but different quantifier | Separate union-before-observation from posterior-after-observation |
| F | Noninjective, partial, or unknown map | Exposes missing inverse premises | Multi-root, no-root, and shape-family counterexamples |
| G | Calibration plus held-out prediction | Legitimate noncircular route | Add an independent observable or overidentifying row |
| H | Accepted IDN/XOV composition | Likely nonpromotion ceiling | Match exact accepted statement scope |
| I | Comparator firewall | Required | Mutate/remove 0.929 without changing structural theorem |
| J | Lean capstone | Exact encoding only | Audit set definitions and quantifiers before trusting prose |
| K | Governance closure | Required | Predicate, consumer, queue, memory, and release replay |

## Selection Criteria and Blinding

Selection is ordered by conditioning and quantifier accuracy, inverse domain and
injectivity, map provenance, same-datum versus held-out use, parameter versus
output information, comparator separation, assumption economy, accepted
dependency fit, consumer reach, and nonduplication. Prior exposure is explicit;
the known result and 0.929 cannot select a candidate.

## Proposed Claim Delta

No claim identifier is proposed at freeze. The inverse identity is elementary,
C-IDN-002 already governs inverse reconstruction, and C-XOV-001 already governs
conditional monotone inverses. A new claim would require distinct reusable
content, an importable API, accepted consumers, and individual four-axis review.

## Implementation and Oracle Plan

The primary route will inventory KI4's five checks, definitions, asserted map
domains, inverse formulas, set constructions, comparator dataflow, imports,
assertions, and compatibility. SymPy is the strongest oracle for inverse
residuals, roots, exact sets, and countermodels.

The quantifier probe will compare a fixed target-conditioned parameter set with
the union over every hypothetical target. Noninjective and partial maps will
test whether the inverse premise is load bearing. A separate two-observable
example will distinguish same-datum reconstruction from a real held-out
prediction or overidentifying test.

The independent route will reconstruct the strongest valid statement without
importing KI4 or the primary verifier. The Lean theorem will be inspected at
its exact hash-identical scope; its P172 clean execution will be reused unless
the bytes or formal obligation change. Accepted derivation matrices will not be
rerun merely for ceremony.

## Attempts and Continuation

Attempt 0001 freezes release, commits, hashes, prior exposure, allowed imports,
eleven candidates, selection criteria, claim delta, and oracle before P174
opens the KI4 body or shared dossier body.

## Debt Ledger

The P174 ledger tracks inverse premises, conditioning, comparator use, formal
scope, consumer propagation, and governed record agreement.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| KI4's exact definitions and predicate reachability are unknown | Pin every definition, check, assertion, import, and runtime result | open |
| Identity and circularity language may have different scope | Separate exact algebra from methodological interpretation | open |
| The zero-information claim may confuse output unions with observed-target conditioning | Compute both set constructions explicitly | open |
| A global inverse may be absent | Supply noninjective, partial, and unknown-map countermodels | open |
| Comparator input may masquerade as validation | Trace and mutate every path from 0.929 | open |
| Lean prose may exceed its theorem | Inspect exact definitions, sets, quantifiers, and prior execution | open |
| Reverse consumers may inherit KI3/KI4 overclaims | Type and replay affected pending nodes without promotion | open |
| Governed records may disagree | Synchronize disposition, queue, memory, effort, and release state | open |

## Review and Promotion Plan

Every KI4 predicate receives an individual verdict. Exact inverse identities may
survive while zero-information, physical, empirical, and universal readings are
qualified or rejected. A source tally or formal theorem over one declared map
cannot promote a stronger information-theoretic or physical claim.

## Done Gate

P174 closes only when inverse domains, injectivity, target conditioning,
hypothetical unions, same-datum residuals, held-out predictions, comparator
dataflow, all predicates and assertions, formal scope, dependencies, consumers,
compatibility, nonduplication, and governed records agree with empty debt.

## Cross-References

See C-IDN-001/002, C-XOV-001, C-BPS-003, C-RDIFF-002, P065, P078, P117, P172,
P173, KI2-KI5, relevant MK/MR consumers, `linear_systems.py`,
`gravity_scale_confrontation.py`, `crossovers.py`, and the migration effort.
