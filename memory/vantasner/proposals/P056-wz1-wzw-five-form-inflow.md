---
description: Derive and audit the SU(3) trace five-form and conditional extension theorem
author: vantasner
created: '2026-08-02T13:15:00Z'
updated: '2026-08-02T14:15:00Z'
tags:
- substrate-framework
- campaign-proposal
- su3-cohomology
- migration-WZ1
category: proposals
confidence: established
status: archived
---
# P056 WZ1 WZW Five-Form and Extension Audit

## Question and Positive Deliverable

P056 must produce the strongest positive, importable theorem naturally
supported for the SU(3) Maurer-Cartan trace five-form and its use in a
five-dimensional extension functional. It must prove or explicitly condition
each step from local closedness through global non-exactness and filling
dependence, and it must not call the result physical anomaly inflow without a
genuine gauge-descent calculation. A failed WZ1 subclaim is attempt evidence;
Candidates B through D must continue to the exact positive object.

## Base Release and Provenance

The accepted base is `v0.49.0` at framework commit `90c6a8c`, with scientific
transaction `a57b0e0`. The pinned source is `substrate@6d1f4e0`; WZ1 is at
`/home/dan/substrate/merged-framework/bridges/phase-17/bridge_WZ1_wzw_5d_chern_simons.py`
with verified SHA-256
`87bab354a83a6edd05ed77ed0778e1cdf11cf402f92414664f7a3196df0551b9`.
The framework inventory path resolves against that source root, not the
framework working directory. S3, S4, WZ2, and WZ3 are all pending
adjudication and are navigation evidence only. Their claimed WZW import,
vector-meson route, integer period, baryon current, and anomaly matching are
not dependencies. The accepted sources actually read are `C-LIE-001`,
`C-LIE-002`, `C-TOP-001`, their reviews, `su3.py`, `topological_labels.py`,
and focused tests. Memory contains no accepted WZW result.

## Invariants, Conventions, and Allowed Imports

The campaign preserves C-LIE-001's explicit Hermitian basis
`T_a=lambda_a/2`, `Tr(T_a T_b)=delta_ab/2`, and
`[T_a,T_b]=i f_abc T_c`. For a unitary group element, the left
Maurer-Cartan form `theta=g^{-1}dg` is anti-Hermitian, so its components in
the Hermitian basis carry an explicit factor of `i`. Every factor of `i`,
wedge-order sign, alternating-sum normalization, and orientation sign remains
visible. C-TOP-001 supplies no SU(3) homotopy, cohomology, baryon, or anomaly
map.

Allowed mathematical imports are the standard exterior derivative and graded
trace rules, the Maurer-Cartan identity, Stokes' theorem, and normalized Haar
averaging on compact SU(3). The finite-dimensional Chevalley-Eilenberg
differential must be constructed from C-LIE-001 rather than imported as an
answer. If an invariant primitive existed globally, Haar averaging would give
an invariant primitive, so exact failure of image membership in the invariant
complex is enough to establish global non-exactness without assuming the
reported `H^5(SU(3))` value. No numerical period, `pi_5` generator, WZW
level, `N_c`, baryon charge, representation rule, or anomaly coefficient is
permitted before it is independently derived or explicitly introduced as a
conditional premise.

## Candidate Preregistration

The candidate set is frozen from accepted algebra and queue metadata before
the source implementation or its reported comparator values are opened.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal WZ1 reproduction | Every source convention and imported topology statement must be traced | Source constants only | May reproduce a tally while failing topology, descent, or sensitivity obligations | Hash-pinned execution, data-flow review, normalization audit, and mutations |
| B | Direct Maurer-Cartan/graded-trace route | Standard exterior calculus | Overall symbolic scale | Proves closedness locally but cannot by itself prove non-exactness | Exact wedge algebra, cyclic-sign derivation, commuting and wrong-degree probes |
| C | Exact SU(3) invariant-cochain route | Haar averaging on compact SU(3) | No fitted parameters | Proves closed, nonzero, non-exact status if the trace cochain is a cocycle outside `im d_4` | Exact CE matrices, rank augmentation, independent construction, and structure-constant mutations |
| D | Extension, gluing, and descent route | Oriented fillings, smooth extension, Stokes; quantized periods or gauge fields only when declared | Symbolic coefficient or level | Gives a conditional filling-difference theorem; anomaly inflow requires a separate descent identity | Orientation/gluing proof, boundary variation, level mutation, and counterexample lacking a gauge connection |

## Selection Criteria and Blinding

Selection is ordered by logical separation of the seven distinct obligations,
dependency closure, convention safety, assumption economy, exact image tests,
correct dimension and commuting limits, independent rederivation, and a strict
physical-interpretation ceiling. A reported period, level, baryon number,
anomaly coefficient, representation, or familiar WZW normalization cannot
select a candidate. The comparator gate opens only after the Maurer-Cartan
convention, alternating basis, CE image test, orientation and gluing laws,
mutation set, and interpretation ceiling are frozen here and in the manifest.

## Proposed Claim Delta

Provisional `C-WZW-001` may state that, in C-LIE-001's convention, the
alternating trace five-cochain associated with the left Maurer-Cartan form is
closed and nonzero and, if exact CE rank evidence succeeds, is not the
differential of an invariant four-cochain. Haar averaging would then promote
that last fact to global de Rham non-exactness on compact SU(3). The claim may
also give the conditional extension theorem: for two compatible oriented
fillings, the difference of extension integrals is the integral over their
glued closed five-cycle. It may state phase independence only conditional on a
declared period lattice and coefficient. It cannot assert the generator
period, `pi_5(SU(3))=Z`, a physical WZW level, `N_c`, baryon current,
representation selection, or anomaly inflow unless those receive separate
load-bearing evidence.

Direct consumers are WZ1 and later WZ units that cite its five-form,
closed-not-exact claim, extension, or inflow language. C-LIE-001 remains the
sole expected accepted scientific dependency; C-LIE-002 and C-TOP-001 remain
unchanged interpretation ceilings unless the audit finds an exact need.

## Implementation and Oracle Plan

A canonical pure module may expose exterior-cochain bases, the CE differential
from exact structure constants, the alternating fundamental-trace
five-cochain, exact closedness and image-membership witnesses, and a symbolic
extension-difference rule. Imports must not run a simulation or print a tally.
SymPy fits the core obligations because all matrices, structure constants,
cochains, ranks, and residuals are finite and exact. Numerical quadrature can
reproduce a source result but is neither independent evidence nor a substitute
for exact cohomology. Any genuinely new period integral would require a
declared smooth cycle, atlas or parameterization, measure, orientation,
precision, singular-boundary handling, convergence norm, and an independent
method; that work is not silently inherited from pending WZ2.

The primary exact route will build `d:C^k->C^(k+1)` from the bracket and test
`d_5 omega=0`, `omega!=0`, and
`rank([d_4|omega])=rank(d_4)+1`. An independent route will reconstruct the
relevant matrices without the proposed reducers or will exhibit a dual cycle
or annihilator separating `omega` from `im d_4`. Load-bearing mutations alter
one structure constant, remove graded signs, rescale or complex-conjugate the
generator convention, reduce to a group of dimension below five, replace
generators by commuting matrices, reverse orientation, alter alternating
normalization, and replace an integer-compatible phase coefficient by a
noninteger one. A mutation counts only when the relevant verdict fails.

## Attempts and Continuation

Six append-only attempts complete P056. Attempt 0001 reproduces the source's
`ALL 12 CHECKS PASS` and identifies its hard-coded period, ceremonial
predicates, false even-power guard, and unsupported inflow language. Attempt
0002 passes the exact package construction with ranks 35 and 20, a
one-dimensional invariant fifth cohomology, and exact rejection of the source
guard. Attempt 0003 independently passes 26 checks using locally reconstructed
generators, trace-projected brackets, graded cochains, and a dual separator.
Attempt 0004 preserves the assembled verifier's YAML scalar-type failure; the
categorical label was quoted without changing any scientific predicate.
Attempt 0005 passes the 27-check pre-promotion scientific verifier, and the
promoted version passes 31 checks after registry, queue, and release closure.
Attempt 0006 passes the complete repository workflow with 70 accepted claims,
164 pending units, 252 valid memory files, the updated skill, and all 413
tests.

## Debt Ledger

This ledger tracks source provenance, exact form conventions, cohomology,
period and extension assumptions, descent, physical interpretation,
independent evidence, consumers, and canonical synchronization.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| WZ1's literal implementation, dependencies, environment behavior, and tally are unaudited | Hash-check, execute, trace every asserted result, and preserve output or failure | discharged by attempt 0001 and source reproduction |
| Local closedness may be inferred from copied antisymmetry or a zero expression | Derive the exterior identity, prove a nonzero evaluation, and mutate graded signs or structure constants | discharged by exact cochains and attempts 0002/0003/0005 |
| Pointwise nonzero may be mislabeled global non-exactness | Build exact CE differentials, prove non-image membership, and justify the Haar-averaging lift | discharged by rank augmentation, dual separation, and audited Haar averaging |
| The reported WZW normalization or integer period may be imported from pending WZ2 | Keep normalization symbolic or independently derive a genuine closed-cycle period with convergence and orientation evidence | discharged by excluding the period and qualifying WZ1; WZ2 remains separately pending |
| A five-dimensional extension density may be mislabeled Chern-Simons anomaly inflow | Prove the gluing theorem and require an explicit gauge connection plus descent/boundary-variation identity for inflow language | discharged by the conditional gluing theorem and explicit rejection of physical inflow |
| Hermitian, anti-Hermitian, wedge-factorial, trace, and orientation conventions may be mixed | Encode each convention once and pass rescaling, conjugation, and orientation mutations | discharged by the canonical module and both exact verifiers |
| `N_c`, baryon number, level quantization, or SU(3) representation claims may enter without authority | Exclude them or open separately governed claims with exact dependencies and evidence | discharged by the C-WZW-001 ceiling and qualified source disposition |
| Independent exact evidence and downstream replay are absent | Complete a separately implemented oracle, focused tests, impact analysis, and affected-consumer replay | discharged by attempts 0003/0005/0006 and LOW graph impact |
| Registry, release, generated docs, migration queue, and durable memory are unsynchronized | Adjudicate claim by claim, regenerate canonical consumers, and empty this ledger | discharged by v0.50.0 and attempt 0006 |

## Review and Promotion Plan

Each mathematical and interpretive subclaim receives separate verification,
review, compatibility, and epistemic axes. Accepted reusable definitions move
under `src/substrate_framework/` with exact focused tests. An independent
review must inspect the CE differential signs, trace normalization,
Haar-averaging argument, extension gluing, mutations, and language ceiling.
WZ1 receives a terminal structured disposition in
`migration/dispositions.yaml`; a mixed unit is `qualified` and names every
remaining subclaim. Promotion requires a pinned release if claims change,
generated documentation and accepted memory, affected-consumer replay, one
final `scripts/validate.sh`, `.venv/bin/python -m pytest`, and
`git diff --check`.

## Done Gate

P056 is accepted in v0.50.0. The positive real SU(3) trace-five cocycle,
invariant and global non-exactness proof, conditional filling theorem,
ungauged boundary identity, false-guard counterexample, independent dual
separator, sensitive mutations, qualified WZ1 disposition, consumer replay,
canonical synchronization, and empty campaign debt all pass. The parent
migration remains active and advances to WZ2.
