---
description: Review and harvest every correct reusable unit from the FlatIrrationalTorus v13.0 model
author: codex
created: '2026-08-19T15:18:24+02:00'
updated: '2026-08-19T15:36:35+02:00'
tags:
- substrate-framework
- research-arc
- flat-torus
- source-audit
category: efforts
confidence: exploratory
status: active
---

## Positive Objective and Success
This effort audits the full model advertised by Viktar-Pi/FlatIrrationalTorus
at immutable commit `ba487f6361f1f8740a4fe518bf86584847ab518b` and imports
every scientifically correct, novel, maintainable unit into Substrate. Success
requires a reproducible source audit, pure tested package APIs for every
surviving unit, unit-level non-import rationales for the rest, an empty
in-boundary debt ledger, and the impact-selected validation receipt. The
upstream headline is neither accepted nor rejected as a bundle: each bridge is
judged at its actual evidential strength.

## Authority and Prior Work
The accepted baseline is release `v0.163.0` at framework commit
`56f10e18848331f1ab57e97c4ec4a358f5124cc7`. The registry and source search
found no accepted rectangular compact-three-torus, reciprocal spectrum, or
matched-circle API. `C-STG-001` explicitly leaves compact spatial
identifications as separately declared data, while `C-DOS-001` treats an
isotropic continuum count and explicitly excludes exact periodic
lattice-point counts. They are scope cross-checks rather than dependencies.
The existing `twisted_casimir` module concerns a shifted square-lattice
Epstein zeta on `T2 x R2` and is not duplicated here.

Repository-local memory searches for "flat irrational torus" and "matched
circles reciprocal lattice compact topology" found no prior compact-torus
implementation. The canonical goal is issue #105. The active P236 worktree
and its user-owned `AGENTS.md` change are outside this effort and remain
untouched.

## Definitions and Invariants
The exact core candidate is a rectangular flat torus
`R^d / (L_1 Z x ... x L_d Z)` with positive side lengths in one consistent
length unit. Integer mode `n` has reciprocal wavevector components
`k_i = 2*pi*n_i/L_i` and scalar-Laplacian eigenvalue `|k|^2`. A lattice
translation indexed by integer vector `m` has length
`sqrt(sum_i (m_i L_i)^2)`. Two radius-`chi` Euclidean spheres separated by a
nonzero translation length `d` intersect in a nondegenerate circle iff
`0 < d < 2 chi`, with angular radius `acos(d/(2 chi))` as seen from either
center. Equality is a tangent point, not a circle.

No `Z2` quotient, spin structure, Dirac operator, cosmological dynamics,
observer position, transfer function, likelihood, or physical scale map is
implicit. Those objects require separate definitions.

## Permitted Imports and Assumptions
Permitted imports are the accepted release for convention checks, elementary
flat-torus Fourier and Euclidean sphere geometry, Python/NumPy, and the MIT
upstream repository solely as a pinned source object. Paper 4 is accessible at
Zenodo record 19599505; the in-hand PDF has SHA-256
`5624a9978b1be2405e58ad119fdedbbe6bd9fa7836fd365dbee7a7f53b5663c6`.
Its three pages and Eqs. (1)-(11) were extracted. The source commit and PDF are
evidence, not authority.

## Candidate Set
The review compares three import layers because the upstream headline bundles
mathematically distinct mechanisms.

| Candidate | Construction | New objects/parameters | Natural-fit case | Expected falsifier | Status |
| --- | --- | --- | --- | --- | --- |
| A | Exact flat rectangular-torus modes, translations, and sphere intersections | Side lengths, integer indices, observation radius | Pure conditional geometry with no comparator | Wrong exact spectrum, limit, or translation enumeration | selected for implementation |
| B | Observational estimators and model predictions from `scripts/` | Maps, masks, transfer functions, estimator definitions | Only if an IT3 prediction is computed independently of the observed map | Observed data reused as the prediction, missing normalization, or no convergence | not selected: no valid model observable |
| C | Constants, gravity, inflation, gauge-RG, dark energy, and CMB physical mappings | Every typed bridge stated in Paper 4 and the engine | Only with derived dependencies and unit-consistent scale maps | Hard-coded output, sector-specific fitted input, dimensional inconsistency, or missing dynamics | not selected: dependency closure absent |

## Selection Criteria and Comparator Gate
Selection is ordered by explicit object and domain, absence of hidden
comparators, dimensions/signs/symmetries/limits, mutation sensitivity or
convergence, framework novelty, maintenance cost, and only then empirical
reach. Comparator blinding was impossible because the supplied public source
already prints its target values. No observed value may select or repair a
candidate.

## Claim Delta
No accepted claim changes in this harvest. The intended output is unpromoted,
conditional infrastructure plus a source audit. Any later theorem promotion
requires a separately frozen claim delta and individual review.

## Frozen Review Transaction
The transaction contains the pinned external source audit, one additive
flat-torus geometry module, its focused tests, proposal and effort records,
and provenance/disposition evidence under P237. Accepted registry entries,
releases, generated docs, P236, and unrelated consumers are excluded. The
base is `56f10e18848331f1ab57e97c4ec4a358f5124cc7`; the head/tree and validation
receipt will be recorded after implementation.

## Claim Ladder
The exact conditional geometry is checked before any observational or physical
interpretation.

| Step | Claim | Oracle | Sensitivity/counterexample | Prerequisites | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | Reciprocal wavevectors and scalar-Laplacian eigenvalues on a rectangular torus | Exact formula and analytic known modes | Change one side length and require only its component/eigenvalue to change | Positive side lengths | complete |
| 2 | Finite enumeration of all nonzero translations shorter than a supplied bound | Direct integer-bound proof plus brute-force boundary tests | Include/exclude translations across the strict cutoff | Step 1 definitions | complete |
| 3 | Nondegenerate matched-circle condition and angular radius | Exact Euclidean sphere-intersection derivation | Tangency, zero separation, and containment counterexamples | Step 2 | complete |
| 4 | Upstream module-by-module dispositions | Source audit plus native/compatibility replay | Hard-coded output and load-bearing mutation probes | Pinned sources | complete |

## Importable Implementation
The planned package surface is `substrate_framework.flat_torus`: validated
side lengths, reciprocal wavevectors, scalar-Laplacian eigenvalues, lattice
translation enumeration, and matched-circle angular radii. It remains pure and
does not import `healpy`, execute simulations, or embed the upstream physical
scale. SymPy carries exact geometry and mpmath evaluates explicitly finite
Epstein partial sums at declared precision. No sampled integration is used.

## Harvest Checkpoints
The canonical goal is issue #105. PR #107 uses `Fixes #105` because the full
source-audit and reusable-import gate is met; only the distinct-merger
operation remains. Source PR closure is not applicable because the source is
an external repository rather than a contributed Substrate PR. The compact
issue handoff is posted at issue comment 5342914592.

| Unit | Local claim | Independent of headline? | Evidence | Commit/PR | Disposition |
| --- | --- | --- | --- | --- | --- |
| Rectangular-torus geometry | Exact conditional Fourier/translation identities | yes | 21 focused tests and P237 source audit | PR #107, frozen tree `ee288685993e573f79972dca6c387a7a614a9ec7` | ready for distinct merge |
| Matched-circle geometry | Exact conditional sphere-intersection result | yes | exact limits and translation enumeration tests | PR #107, frozen tree `ee288685993e573f79972dca6c387a7a614a9ec7` | ready for distinct merge |
| Rectangular Epstein partial sums | Convergent finite positive lattice sums with visible refinement increments | yes | scale mutation, 1D oracle, and cutoff ladder | PR #107, frozen tree `ee288685993e573f79972dca6c387a7a614a9ec7` | ready for distinct merge |

## Attempts
The attempt ledger distinguishes compatibility and evidential defects from
mathematical failures.

| Attempt | Candidate/method | Artifact | Verdict | Diagnosed layer | Next materially different route |
| --- | --- | --- | --- | --- | --- |
| 0001 | README, master engine, scripts, stored report, and Paper 4 source audit | pinned clone and PDF text | exact geometric atoms survive; full-model verification not established | upstream verification architecture | inspect analysis package and execute native paths |
| 0002 | Native advertised entrypoints | `evidence/source-reproduction.yaml` | 12/12 text reproduces; full pipeline and several scripts abort; spectral helper contradicts itself | compatibility plus implementation and claim-oracle defects | exact clean-room extraction |
| 0003 | Canonical exact geometry extraction | `flat_torus.py`, 21 focused tests | passed | conditional mathematical core | bounded source/implementation review and scoped replay |

## Framework-Fit Audit
Candidate A is additive and naturally conditional. It neither changes
`C-STG-001` nor conflates the exact lattice spectrum with `C-DOS-001`'s
continuum measure. Candidates B and C require their own model observable,
typed physical maps, declared units, and genuine predictions; proximity to a
printed comparator is not a bridge.

## Verifier Audit
The strongest oracle for the harvested core is exact construction plus
boundary counterexamples. The 21 focused tests catch a missing `2*pi`,
side-index mutation, mixed twist grid, nonstrict tangency, zero-translation
inclusion, cutoff-bound errors, Epstein scaling, and hidden tail increments.
They pass at frozen tree `ee288685993e573f79972dca6c387a7a614a9ec7`.

## Impact-Bounded Dependency Replay
The new leaf module has no prior package consumers. GitNexus reports low risk,
zero affected symbols, and zero affected processes. The single scoped receipt
runs the new tests plus `test_mode_counting.py` and `test_twisted_casimir.py`;
all 60 pass with every fixed repository check. No accepted physics consumer
changes.

## Foundational Revision Gate
No independent inconsistency in accepted canon has been found. The upstream
model's unsupported bridges do not require a foundational revision.

## Debt Ledger
No in-boundary debt is accepted. The external model's unestablished physical
bridges are source dispositions and continuing scientific frontier, not hidden
premises inside the imported conditional API.

| Debt | Source | Effect | Discharge | Status |
| --- | --- | --- | --- | --- |

## Independent Claim Review
No accepted claim is proposed or changed. The code/source harvest receives one
bounded implementation review through the PR lifecycle; a later claim proposal
would require its own claim review.

## Results and Continuation
The strongest positive result is a complete clean exact compact-torus geometry
layer separated from the unsupported physical bundle. It provides cell volume,
fixed-twist reciprocal modes, exact finite eigenspaces, deck translations,
matched-circle geometry, and honest Epstein partial-sum refinement. The
module-by-module audit gives terminal non-import reasons for every other
current advertised v13 unit. The source and implementation boundary is
complete; only PR landing remains operational.

## Promotion and Materialization
This harvest materializes package code, public exports, tests, proposal
evidence, and durable effort memory. Accepted claims, releases, and generated
docs stay unchanged. The validation receipt is
`proposals/P237-flat-irrational-torus-import-audit/evidence/validation-receipt.yaml`.

## Done Gate
The source inventory has unit-level dispositions, every reusable atom is in
the frozen PR tree or explicitly excluded for a technical reason, the debt
ledger is empty, affected validation passes, and the canonical issue handoff
is posted. The record remains active only until PR #107 lands; no scientific
or implementation obligation remains inside the harvest boundary.

## Cross-References
Canonical issue: https://github.com/vantasnerdan/substrate-framework/issues/105

Pull request: https://github.com/vantasnerdan/substrate-framework/pull/107

Issue handoff: https://github.com/vantasnerdan/substrate-framework/issues/105#issuecomment-5342914592

Upstream source: https://github.com/Viktar-Pi/FlatIrrationalTorus

Paper 4: https://zenodo.org/records/19599505/files/Paper_4.pdf?download=1
