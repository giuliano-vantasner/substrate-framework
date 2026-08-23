---
description: Constructive review of C-M5S-001 aligned-vacuum fluctuation census
author: P243Reviewer
created: '2026-08-23T09:31:33+00:00'
updated: '2026-08-23T09:31:33+00:00'
tags:
- substrate-framework
- claim-review
- p243
- fluctuation-spectrum
category: decisions
confidence: working
status: active
---

## Claim and Positive Role

The proposed statement asked for a "confined-clock second-variation census — bound-channel squared gaps and multiplicities about window backgrounds, separated from box-continuum classes, with refinement evidence and an independent-route agreement gate." The delivered object is the exact free-fluctuation census of the aligned spectral-Cartan vacuum M0 with mixed targets (4, 1, 3/10, 0) on the 10-dimensional symmetric basis: 3 exactly-massless propagating species (the timelike-eigenvector boost orbit, strictly positive projector-current kinetic metric 1/9, 100/1369, 1/16), 4 stiff static directions (positive stiffness 67905, 30, 361141/250000, 1 with vanishing quadratic kinetics, excluded from species counting by a named reason), and 3 inert directions. The framework question it answers is where the induced composition's multiplicity N comes from: this census supplies N=3 with all propagating z_i=0, so the accepted scale factor collapses J(0)=1 and R(0)=1 per C-IGR-004, reducing Delta(1/G) to sourcing Lambda alone.

## Frozen Transaction

Base origin/main c21635f (v0.163.0 lineage), head campaign/p243-scale-resolution c2efa38, stack 90e7a4e..c2efa38. Claim delta is additive leaf C-M5S-001; no registry entry consumes it. Changed implementation: new canonical module src/substrate_framework/m5_fluctuation_spectrum.py (391 ln, commit 90e7a4e). Evidence records: proposals/P243-clock-sourced-induced-coupling/attempts/0001/{result.yaml,vacuum_census.py,stdout.txt,manifest.yaml}. Accepted dependency propositions actually used: C-IGR-004's continuous extension at m2=0 giving J(0)=1 and spread ratio R(0)=1 on the usable set {sharp, smooth}, with the tau^-1 control class declared divergent at m2=0 (quoted as a declared boundary in attempts/0001/result.yaml consequence, matching governance/claims.yaml lines 11961-12025 assumption 4); canonical m5_covariant_action.py pinned spectrum potential and projector current. Affected consumers: C-M5S-002 (window-background soft-mode diagnostics), C-M5S-003 (N=3, z=0 inputs). Validation receipt: none yet at this boundary; fresh content-addressed receipt belongs to the promotion transaction.

## Strongest Supported Positive Statement

The strongest supported result is the aligned-vacuum census itself, exactly as delivered, plus its composition consequence: the free second variation of the conditional P239 action about M0 (targets 4, 1, 3/10, 0) decomposes on the 10-dimensional symmetric basis into exactly 3 massless propagating species with positive rational kinetic coefficients (1/9, 100/1369, 1/16), 4 stiff non-dynamical diagonal directions with exact squared stiffness gaps (67905, 30, 361141/250000, 1) excluded from species count because their quadratic kinetics vanish, and 3 inert directions; hence N=3, all z_i=0, J(0)=1, R(0)=1, and Delta(1/G) reduces to sourcing Lambda alone. This is a minimum honest repair of quantifier scope, not a narrowing without cause: the proposal prose promised window backgrounds, and no registry-grade window-background spectrum census was delivered — window-background second-variation structure appears only as family Morse-index diagnostics (lambda_1 along U/S families) inside attempts 0002/0004/0005 serving scale selection. Upgrade path: delivering an exact or refined bound-channel census about a committed window root (with nodal census and refinement evidence) restores the stronger proposed scope; nothing in this review precludes it.

## Evidence Map
Four evidence groups cover the census: the recorded verifier run, the canonical module, the accepted dependency entry, and the window-background diagnostics that stay outside this claim.

| Evidence | Proposition established | Role: exact proof / corroborating subclaim / regression / applicability / provenance | Bridge to claim | Limit |
| --- | --- | --- | --- | --- |
| attempts/0001/stdout.txt + vacuum_census.py (ALL 10 CHECKS PASS) | Census counts 3/4/3, exact kinetic coefficients, exact stiff gaps, certification nullities all zero, three mutations fail as required | exact_proof | The whole positive statement for M0 | Aligned vacuum only; not window backgrounds |
| src/substrate_framework/m5_fluctuation_spectrum.py (classify_census, certify_projector_variation) | Reusable exact construction: stiffness via epsilon^2 series coefficient, kinetic metric from certified dP, classification with joint-nonzero guard | exact_proof | Makes the census importable and replayable | No committed unit test at c2efa38 |
| C-IGR-004 registry entry (governance/claims.yaml 11961-12025) | J(0)=1, R(z)=1 only at z=0, usable set {sharp, smooth}, tau^-1 divergence at m2=0 | exact_proof (dependency) | Bridges census to the composition consequence N=3, all z=0 | Declared conditional composition, not physics selection |
| attempts/0002..0005 lambda_1(U/S) family diagnostics | Window-background soft-mode structure along two stationary families | provenance_only (for THIS claim) | Feeds C-M5S-002's selection record, not a spectrum census | Not a registry-grade census; carries solver-order systematics |

## Oracle Audit

The strongest practical oracle is vacuum_census.py under PYTHONPATH=src, and mutation evidence is actually present, satisfying the exact-symbolic discipline. It computes both matrices as exact rationals (sympy series coefficient extraction and polarization identity for off-diagonals), certifies the analytic first variation dP by affine uniqueness against the linearized defining system (right/left eigen-relations, idempotence, eta self-adjointness): satisfaction exact, symbolic consistency matrix_a * analytic_vector == rhs, and trivial homogeneous kernel in all 10 directions (projector_variation_certified_unique). Mutations present and meaningful: degenerate timelike target raises (degenerate_target_rejected); kappa rescale 7 moves every kinetic coefficient (kinetic_rescaling_moves_coefficients); dropping a potential weight moves the stiff gaps (weight_mutation_moves_stiff_gaps). No refinement axis exists — every value is exact, so refinement discipline is not applicable rather than absent. Positivity of the massless kinetic restriction is pinned by the exact diagonal values themselves (each equals kappa/(lambda_t - lambda_a)^2 for distinct spatial targets) plus kinetic_rank == 3 in the printed record. I cross-checked internal consistency of the recorded stdout against the module source and found no check whose assertion fails to test its labeled proposition; each check maps onto a clause of the claim.

## Findings
Three findings were classified once each, none blocking.

| Finding | Direct evidence | Blocking in boundary / minimum correction / follow-up | What would resolve or overturn it |
| --- | --- | --- | --- |
| Delivered scope is the aligned vacuum, not window backgrounds as proposed | attempts/0001/result.yaml frozen_question vs proposal.yaml claims_proposed C-M5S-001 prose; no window-root census artifact exists | minimum correction — adopt the proposer's restatement (aligned-vacuum census + derived N=3/z=0 collapse); window-background soft-mode structure stays evidence under C-M5S-002's selection record | An exact or refined bound-channel census about a committed window root (nodal census + refinement ladder) restores the original scope |
| Canonical module has no committed unit test at the boundary | git ls-tree c2efa38 tests/ lists no test_m5_fluctuation_spectrum.py; untracked tests/test_m5_fluctuation_spectrum.py exists in working tree outside the frozen transaction | follow-up — gate-8 promotion work; the attempt script is the operative oracle meanwhile | Commit the prepared test file with independent closed-form expectations and include it in the promotion validation receipt |
| First-execution stderr is empty but uncaptioned in the record | attempts/0001/stderr.txt is 0 bytes (clean run) | follow-up — none needed beyond noting it here | n/a |

No blocking finding: there is no counterexample, no circular or absent load-bearing step, no dependency shortfall (C-IGR-004 supplies exactly J(0)=1 and R(0)=1 as used), and no affected consumer failure. No prior review narrowed this claim; this is the first scope adjustment and it carries contrary evidence (the delivered artifact genuinely covers only M0).

## Compatibility and Consumers

Conventions are declared and consistent: mostly-plus eta, mixed targets as eigenvalues, symmetric basis in canonical order, action's own dimensionless units. The module imports only sympy and canonical primitives (m5_covariant_action), executes nothing at import, and rejects degenerate targets. Consumer replay inside this transaction: C-M5S-002's family diagnostics and C-M5S-003's N=3/z=0 ledger both consume the census as recorded and replay green in their own artifacts (attempts/0003/stdout.txt ALL 10 CHECKS PASS uses massless_count=3). The tau^-1 divergence at m2=0 is quoted as a declared boundary inherited from C-IGR-004, not hidden debt. Defects introduced inside this transaction: none found.

## Four-Axis Decision

Verification: symbolic_verified (exact rationals, uniqueness certification, mutations; no numeric component).
Review: accepted with minimum correction (statement restated to the aligned vacuum; registry text below).
Compatibility: native (new additive module and leaf claim; no existing contract touched).
Epistemic: active.
Relationship: depends on C-IGR-004 and canonical m5_covariant_action.py; challenges and supersedes none.
Strongest accepted or proposed statement: the restated registry text below.

Registry-ready final statement (verbatim):

> C-M5S-001 (symbolic_verified): The exact free-fluctuation census of the aligned spectral-Cartan vacuum M0 with mixed targets (4, 1, 3/10, 0), computed as exact rational matrices on the 10-dimensional symmetric basis of the conditional P239 action's pinned spectrum potential and projector-current kinetic metric, decomposes into exactly 3 massless propagating species (timelike-eigenvector boost orbit; kinetic coefficients exactly 1/9, 100/1369, 1/16, positive), 4 stiff static directions (exact squared stiffness gaps 67905, 30, 361141/250000, 1; vanishing quadratic kinetics, excluded from species counting by this named reason), and 3 inert directions. The first variation of the timelike spectral projector is certified by exact affine uniqueness against its linearized defining system (satisfaction, consistency, trivial kernel in all 10 directions), and preregistered mutations (degenerate target, kinetic rescaling, weight drop) each break the corresponding record. Consequence consumed downstream: the induced composition multiplicity is N=3 with every propagating species exactly massless, so z_i=0, the accepted continuous extension gives J_sharp(0)=J_smooth(0)=1, the scheme spread R(0)=1 exactly per C-IGR-004, and Delta(1/G)=(1-6*xi)*Lambda^2/(4*pi) reduces to sourcing Lambda alone; the tau^-1 higher-curvature control class remains logarithmically divergent at m2=0 as C-IGR-004's declared boundary. Scope note: this census is about the aligned vacuum M0; window-background second-variation structure is carried as family Morse-index evidence under C-M5S-002's selection record, not by this claim.

## Promotion Transaction

Add C-M5S-001 to governance/claims.yaml with the verbatim statement above, dependencies [C-IGR-004], evidence [attempts/0001/result.yaml, attempts/0001/stdout.txt, attempts/0001/vacuum_census.py, src/substrate_framework/m5_fluctuation_spectrum.py], verification symbolic_verified, accepted_in v0.164.0. Land the prepared untracked tests/test_m5_fluctuation_spectrum.py (independent expectations) in the same promotion, pin release v0.164.0, regenerate docs via scripts/render_docs.py, synchronize accepted-claim memory, move the adjudicated campaign record into campaigns/, and record one content-addressed validation receipt (scripts/validate_changed.py scope selection incl. the new test files) at the final boundary.

## Correction Check

Not needed — no correction was requested of a prior pass; this is the first substantive review.

## Result and Frontier

The positive result retained is the exact aligned-vacuum census with its derived N=3, z=0 collapse feeding the whole downstream campaign — the strongest oracle-backed form the delivered evidence supports. Frontier: a window-background bound-channel spectrum census (the original proposed scope) remains open campaign work and would extend this claim; it is not required by any consumer of the current statement.

## Cross-References

Proposal proposals/P243-clock-sourced-induced-coupling/proposal.yaml; campaign contract memory/vantasner/proposals/P243-clock-sourced-induced-coupling.md; frozen txn local://p243-review-txn.md; evidence attempts/0001/{result.yaml,vacuum_census.py,stdout.txt}; module src/substrate_framework/m5_fluctuation_spectrum.py; dependencies C-IGR-004 (governance/claims.yaml 11961-12025), m5_covariant_action.py; consumers C-M5S-002/003 reviews; sibling reviews C-M5S-002..005; precedent memory/vantasner/decisions/C-IGR-004-review.md; base c21635f, head c2efa38.
