---
description: Audit EM7's fractional-Laplacian force family and dimensional interpretation
author: vantasner
created: '2026-08-09T05:20:00Z'
updated: '2026-08-09T05:20:00Z'
tags: [substrate-framework, campaign-proposal, riesz-kernel, fractional-laplacian, migration-EM7]
category: proposals
confidence: exploratory
status: active
---
# P136 EM7 Fractional Force Audit

## Question and Positive Deliverable

P136 must reproduce and adjudicate EM7's claim that one fractional-Laplacian
or Riesz family constructively joins a one-dimensional linear potential, a
two-dimensional logarithm, and a three-dimensional Coulomb potential. The
positive deliverable is either a distinct importable critical-boundary and
exponent-identifiability theorem, or an exact accepted composition proving that
C-KRN-001 and C-MAX-001 already contain every supportable branch, together with
a terminal predicate-level EM7 disposition. A rejected fractal interpretation
alone cannot complete the campaign.

## Base Release and Provenance

The accepted base is v0.103.0 at scientific commit `4cea232`; the parent
migration checkpoint is `5176b6d`. EM7 is pinned to
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`, path
`merged-framework/bridges/phase-3/bridge_EM7_fractal_force_law.py`, SHA-256
`c8bf044d846d22eaa652a0f4c11cd5f5e2a51f98e49d0578536fbc4e96f63f22`.

The generated queue exposes seventeen static check calls, thirteen literal and
four dynamic calls, one assertion, symbolic and numeric oracle hints, and
dependencies D3S, EM3, and QCD5. D3S is qualified through C-LOC-001/C-KRN-001,
EM3 through C-GAU-001/C-KRN-001/C-MAX-001, and QCD5 remains pending. P134 and
P135 already executed EM7 as immutable graph evidence, exposing its body and
successful tally; P136 records that limitation and makes no fresh source or
comparator blindness claim.

## Invariants, Conventions, and Allowed Imports

C-KRN-001 supplies the exact subcritical Riesz kernel in a fixed Fourier
convention only for `r>0`, nonzero `A`, and `0<s<d/2`. C-MAX-001 separately
supplies source-normalized ordinary-Laplacian branches in positive integer
dimension, including the reference-dependent `d=2` logarithm and even `d=1`
linear branch. Neither claim selects an operator power, dimension, source,
force dictionary, physical sector, or dimensional lift.

The campaign distinguishes subcritical, critical, and supercritical domains.
The critical logarithm requires reference subtraction; the supercritical
kernel needs a distributional prescription and boundary or polynomial data.
It also distinguishes an integer Euclidean dimension from Hausdorff, spectral,
walk, and analytic-regularization parameters. A real symbol in a gamma formula
does not construct any of those spaces. A radial force additionally requires a
declared probe-energy/sign dictionary.

Allowed mathematics is exact gamma-function limiting algebra, radial
differentiation, exponent solving, ordinary radial Laplacians, Fourier or
Schwinger-parameter normalization, and explicit source, probe, coefficient,
reference, boundary, dimension, and operator inputs. C-LOC-001 supplies only
declared-kernel algebra; pending QCD5 and every physical comparator are
forbidden premises.

## Candidate Preregistration

The candidate set separates literal replay, accepted subcritical composition,
a potentially distinct critical boundary, exponent nonidentifiability,
dimension semantics, and governance closure.

| Candidate | Construction | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal EM7 replay | Source conventions | Source symbols | Some powers may survive while domain and geometry claims fail | Seventeen-predicate AST and data-flow audit |
| B | Accepted subcritical composition | C-KRN-001 plus explicit source/probe dictionaries | `d,s,A,Q,q,r` | Exact powers and Coulomb endpoint survive conditionally | Canonical kernel, derivative, normalization, and mutations |
| C | Critical reference-subtracted limit | Approach `s=d/2` from below with fixed reference radius | `d,A,r,r0` | A finite logarithmic difference survives after the divergent constant cancels | Exact gamma limit and independent radial-flux normalization |
| D | Inverse-square solution family | Supplied radial force dictionary | `d,s` | Inverse square fixes `d=2s+1`, not a unique dimension | Exact solve and endpoint mutations |
| E | Dimension-semantics ceiling | Independently defined geometric structures | dimension labels | Analytic continuation alone constructs no fractal medium | Countermodels and input inventory |
| F | Governance closure | Accepted authority order | None | Narrow claim or composition and terminal disposition | Dependencies, consumers, impact, novelty, queue, and generated state |

## Selection Criteria and Blinding

Selection is ordered by accepted closure; fixed Fourier, sign, source, probe,
boundary, and dimension conventions; honest subcritical/critical/supercritical
domains; exact gamma and radial normalization; dimension semantics; endpoint
and scaling limits; independent derivation; mutation sensitivity; parameter
economy; reusable API value; consumer compatibility; and nonduplication.

Genuine blinding is unavailable because the queue exposes EM7's formula and
Coulomb endpoint and two earlier graph replays exposed the body and tally. The
known values are quarantined from concept selection. This contract freezes the
domain split, candidates, criteria, and physical ceilings before renewed source
inspection; agreement with `1/r` or inverse square cannot select `d`, `s`, or a
space.

## Proposed Claim Delta

P136 provisionally reserves C-KRN-002 for a reference-subtracted critical Riesz
logarithm, its radial derivative, and the conditional inverse-square family
`d=2s+1`. It may depend on C-KRN-001 and compose with C-MAX-001. It will not
extend a convergent Fourier integral outside its domain, identify analytic `d`
with a fractal dimension, select `s=1` or `d=3`, or assert a physical force,
charge, electromagnetic sector, gravity sector, substrate mechanism, or
observation. If accepted claims already contain the exact surface, the
provisional identifier remains unpromoted and EM7 closes through composition.

## Implementation and Oracle Plan

The primary route will hash, parse, and execute EM7, map all seventeen executed
predicates, inventory imports and constants, and compare each formula with
C-KRN-001 and C-MAX-001. A compatibility preflight detects direct, imported,
dynamic, and eager-default legacy NumPy integration access. Mutable scripts use
exact SymPy integration or `np.trapezoid`; immutable source receives only a
recorded alias replay if required, never a scientific penalty.

SymPy exact gamma limits, differentiation, exponent solves, and radial
Laplacians are the strongest oracles. The independent route will reconstruct
the critical logarithm from a reference-subtracted Schwinger/Riesz expression
or radial flux without importing any new canonical helper. Mutating `d`, `s`,
`A`, source and probe signs, reference radius, Fourier normalization, and the
domain assumption must alter or break the relevant verdict. Any source float
or fitted slope is regression only because exact powers decide the claim. A
new API is allowed only if the novelty audit proves the critical surface is not
already canonical.

The impact audit covers the canonical kernel and all reverse consumers.
Campaign verifiers depend only on frozen evidence and accepted modules, never
on a future queue state or mutable current release.

## Attempts and Continuation

Attempt 0001 freezes this contract and records the prior-exposure limitation
before renewed EM7 inspection. Every failed domain limit, normalization,
source-replay, independent route, or governance operation will be preserved
with its mechanism and next materially different repair. Failure of literal
EM7 triggers Candidates B through F; it cannot complete the positive object.

## Debt Ledger

The ledger tracks source predicates, Fourier domain, critical subtraction,
supercritical distributional data, dimension semantics, source and force
dictionaries, endpoint selection, dependencies, consumers, novelty, and
physical scope.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| EM7 executable surface is not freshly audited | Hash, execute, AST/data-flow audit, and map all seventeen predicates | open |
| One formula may mix three domain regimes | Separate subcritical, critical, and supercritical constructions with exact hypotheses | open |
| Critical logarithm may be an unsupported limit | Derive the reference-subtracted limit and normalization independently | open |
| Fractional dimension may be only a relabeled parameter | Inventory the actual space, measure, operator, and dimension definitions or retain a no-geometry ceiling | open |
| Inverse-square endpoint may be hard-coded | Solve the full `d,s` family and mutate both inputs | open |
| Source, probe, and force signs are untyped | Declare the energy/force dictionary and test zero and sign limits | open |
| Dependencies, consumers, and novelty are unknown | Audit D3S/EM3/QCD5, reverse consumers, accepted APIs, and graph impact | open |
| Registry, release, docs, queue, and memory are unsynchronized | Promote only distinct reviewed claims or close exact composition, then regenerate governed state | open |

## Review and Promotion Plan

C-KRN-002 receives an individual review only if the critical theorem is
distinct, exact, sensitive, and independently derived. Source adjudication
separately classifies EM7. Reusable logic moves into the existing momentum-
kernel module with focused tests; literal orchestration stays in P136. A
terminal qualification or duplicate decision must name every surviving
accepted mapping and rejected physical clause. Any release, queue, generated
documentation, and memory transaction is validated once at the changed
boundary.

## Done Gate

P136 closes only with the positive critical/composition object, claim-level
review if needed, terminal EM7 disposition, sensitive exact evidence,
dependency and consumer replay, synchronized governance, and an empty campaign
ledger. A source no-go or unsupported fractal headline is attempt evidence and
does not by itself finish the campaign.

## Cross-References

See P030, P064, P134, P135, D3S, EM3, EM7, QCD5, C-LOC-001, C-KRN-001,
C-MAX-001, v0.103.0, and the parent framework-migration effort.
