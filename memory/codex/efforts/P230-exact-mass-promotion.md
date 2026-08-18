---
description: Promote the exact constant-mass one-loop regulator theorems C-IGR-001 through C-IGR-003
author: root-agent
created: '2026-08-18T11:49:56+02:00'
updated: '2026-08-18T12:09:42+02:00'
tags:
- substrate-framework
- research-arc
- induced-gravity
- P230
category: efforts
confidence: established
status: active
---

## Positive Objective and Success
This arc promotes three narrow positive theorems from P230: exact sharp-cutoff, smooth-weight, and power-subtracted constant-mass proper-time coefficient families together with their explicitly conditional one-loop curvature and vacuum compositions. Success requires exact claim statements, accepted dependency and approved-import closure, a constant-mass scope repair, independent rederivation, mutation sensitivity, importable APIs, consumer replay, individual claim reviews, immutable campaign adjudication, registry and v0.161.0 release materialization, generated docs and accepted memory synchronization, full validation, and an empty debt ledger. Issue #76 remains open because these theorems do not select a regulator, renormalization condition, total gravitational coupling, sourced geometry, or predictions.

## Authority and Prior Work
The accepted boundary is v0.160.0 at current-main commit 0beaac3 with C-GRV-001 as the only accepted induced-coupling dependency. PR #77 contains the original P230 proposal and repair history; PR #82 contains the reviewed focused implementation at d415caf, cherry-picked unchanged as a309008. The landed scalar_induced_newton and covariant_sine_gordon_action modules promoted no claims and are implementation/provenance inputs only. Primary sources checked are Vassilevich hep-th/0306138v3 equations 1.16-1.20, 2.2, 4.27 and Visser gr-qc/0204062v1 equations 7-15. Repository memory searches for P230 and C-IGR found only the active PR records; no accepted identifier collision exists. The genuine unresolved objective is claim-level promotion of the correct constant-mass theorems, not artifact harvest.

## Definitions and Invariants
Let Lambda>0, mu>0, m^2>=0 be exact constants, N a positive integer, xi an exact real with decidable relation to 1/6, and z=m^2/Lambda^2. The determinant reading declares a positive self-adjoint boundaryless four-dimensional Euclidean D_E=-nabla_E^2+xi R_E+m^2 with constant m^2 and adequate infrared convergence or reference subtraction. Gamma_E=(1/2) ln det D_E is represented with the declared proper-time sign. I2 is the tau^-2 curvature-class integral and I3 the tau^-3 vacuum-class integral. The sharp lower limit is Lambda^-2; the smooth weight is exp(-1/(Lambda^2 tau)); the power-subtracted family is the declared cutoff finite part at scale mu. Only these local coefficient families are claimed, not an exact truncation of the full nonlocal determinant. No arbitrary x-dependent V'' background, regulator selection, cutoff ontology, additive-baseline choice, total G, or empirical comparator is part of the theorem.

## Permitted Imports and Assumptions
Permitted accepted input is C-GRV-001. Approved conditional imports are the stated real-scalar determinant/heat-kernel/EH conventions from the primary literature, exact special-function identities, and exact input validation. The scalar_induced_newton API may be reused only after independent coefficient rederivation. A sine-Gordon composition is limited to a constant vacuum whose V'' is nonnegative and constant.

## Candidate Set
The candidate set was preregistered in P230 before formula evaluation. A is the sharp tail-integral family, B the smooth essential-singularity Bessel family, and C the power-subtracted finite-part family. All three remain because the deliverable is their exact conditional comparison, not a physically selected regulator.

## Selection Criteria and Comparator Gate
Criteria in order are defining-integral/subtraction correctness, constant-mass scope, dimensions and exact limits, independent rederivation, mutation sensitivity, explicit assumption economy, API/consumer closure, and only then any later empirical test. No empirical comparator is opened in P230. Existing internal z=1 evaluations are exact formula regressions and cannot select a scheme.

## Claim Delta
C-IGR-001 states the sharp constant-mass I2/I3 and conditional shift theorem. C-IGR-002 states the smooth constant-mass Bessel I2/I3 and conditional shift theorem. C-IGR-003 states the power-subtracted constant-mass finite-part theorem and exact scheme-dependence ceiling. Each depends on C-GRV-001 only for the additive inverse-coupling ledger and uses the proposal's declared QFT conventions as explicit conditional imports. None supersedes an accepted claim.

## Claim Ladder
First prove each I2/I3 family from its defining integral or subtraction limit. Then prove dI3/dm^2=-I2, dimensions, massless and scale limits, and mutations. Then compose the independently rederived determinant and EH factors. Finally establish that scheme contrast and the independent additive baseline prevent a physical total normalization without later inputs.

## Importable Implementation
Canonical APIs are scalar_one_loop_mass.curvature_proper_time_integral, vacuum_proper_time_integral, exact_mass_inverse_newton_shift, exact_mass_vacuum_density_shift, and regulator_scheme_ledger. The implementation must declare constant mass, must not call an unpromoted scientific result as authority, and must expose exclusions in its documentation. Campaign verifiers import the API; the independent rederivation imports no scalar_one_loop_mass symbol.

## Harvest Checkpoints
PR #82 is the reviewed implementation checkpoint and PR #77 is the proposal/attempt provenance. Both are superseded only after the promotion PR lands. Canonical issue #76 predates both PRs. The promotion successor uses Advances #76 because the parent emergent-gravity objective remains open.

## Attempts
Attempt 0001 produced the original exact atoms but contained a vacuum double count. Attempt 0002 repaired that defect and zeta sign semantics but left false authority language in the broad proposal boundary. Attempt 0003 is this promotion repair: narrow to constant mass, restate the claims exactly, independently rederive, and complete governance materialization.

## Framework-Fit Audit
The claims are conditional extensions compatible with C-GRV-001 because they preserve its independent baseline and premise ledger. They neither identify the scalar with substrate matter nor choose regulator, scale, cutoff, total coupling, sign of the total inverse coupling, or a physical background. A varying mass endomorphism is explicitly excluded rather than retrofitted into a factorized formula.

## Verifier Audit
The primary verifier exited zero with all 27 checks passing. The independent reviewer imports no `scalar_one_loop_mass` scientific symbol and exited zero with all 21 checks passing, using raw SymPy derivations plus 60-digit quadrature only as corroboration. Exact oracles cover defining integrals, subtraction limits, `dI3/dm^2=-I2`, massless and large-mass limits, scale derivatives, dimensions, signs, and the independently reconstructed determinant-to-Einstein-Hilbert factor. Mutations cover branch, Bessel order, prefactor, determinant sign, vacuum double counting, and varying-background scope; each load-bearing mutation breaks its relevant verdict. The executable compatibility scan found no direct, imported, or dynamic legacy `np.trapz` access.

## Global Dependency Replay
The affected scalar tests and the `scalar_induced_newton` regression passed 42 tests. Direct package import passed. Repository validation closed 210 accepted claims and the v0.161.0 release with no migration queue debt; canonical docs and accepted memory were regenerated. GitNexus classified the change as low risk with zero affected execution flows and no external runtime caller of the new composed APIs. The final full workflow gate passed all fixed checks and 2,263 tests in 288.80 seconds. The campaign verifier and independent rederivation passed separately at 27 and 21 checks. Final record-sensitive repository, memory, docs, and accepted-memory checks passed, and `git diff --check` was clean.

## Foundational Revision Gate
No foundational revision is opened. The constant-mass narrowing resolves the candidate scope defect without changing accepted canon.

## Debt Ledger
No debt remains inside the three-claim promotion scope. The original arbitrary-background language was narrowed to constant nonnegative mass; exact statements, independent rederivation, immutable campaign and individual reviews, registry and release entries, and generated consumers are all materialized. Regulator selection, a renormalization condition, total coupling, sourced geometry, and higher-curvature terms are explicitly outside these claims and remain frontier of issue #76 rather than hidden promotion debt.

## Independent Claim Review
Separate reviews for C-IGR-001, C-IGR-002, and C-IGR-003 accept each exact conditional theorem against the frozen criteria and reject every broader reading listed in the adjudication.

## Results and Continuation
The promotion package establishes three positive, exact constant-mass theorems: the sharp-cutoff family, the smooth Bessel family, and the declared power-subtracted finite-part family, including their conditional curvature and vacuum compositions and exact scheme ceiling. After this package lands, issue #76 continues at the tau^-1/higher-curvature and renormalization-condition frontier rather than treating these claims as a total gravity derivation.

## Promotion and Materialization
Campaign P230, three claim reviews, governance entries, the v0.161.0 release, generated docs, accepted claim/release memory, and validation evidence are materialized on `research/p230-exact-mass-promotion`. PRs #77 and #82 remain provenance inputs and must stay open until the corrected successor lands; repository acceptance still requires the distinct merger mandated by AGENTS.md.

## Done Gate
All scientific, verification, review, dependency, consumer, materialization, and debt gates for C-IGR-001..003 pass. The package is ready for a distinct merger. Completion of this arc promotes those three claims but does not close issue #76.

## Cross-References
Canonical issue #76; PRs #77 and #82; proposal P230; C-GRV-001; source module scalar_one_loop_mass.py.
