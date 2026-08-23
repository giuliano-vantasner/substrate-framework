---
description: Constructive review of C-M5S-004 sourced weak-field consumer and regime verdict
author: P243Reviewer
created: '2026-08-23T09:31:33+00:00'
updated: '2026-08-23T09:31:33+00:00'
tags:
- substrate-framework
- claim-review
- p243
- weak-field-consumer
category: decisions
confidence: working
status: active
---

## Claim and Positive Role

The proposed statement asked for a Poisson solve with G_total from C-M5S-003 and the clock's own time-averaged density, exterior monopole match against linearized_einstein conventions, an acceleration observable, mutation and refinement gates, and a radiative attempt at its honest role. The delivered object is that consumer, formally solved and clean, together with its decisive regime verdict: at xi=0 the induced coupling gives G_total·M/R = 213.397 ≫ 1, so the confined-clock sector is strongly coupled to its own gravity and the linearized expansion the consumer assumes is invalid for this sector — the verdict is the physics result and closes the question asked. The framework question answered: does the substrate sector consistently source the linearized Newtonian potential with its own derived coupling, and does that regime apply?

## Frozen Transaction

Base origin/main c21635f, head c2efa38; additive leaf claim. Changed implementation: none in src/ (the consumer is campaign-local, correctly so: it is an applicability probe, not reusable machinery). Evidence records: attempts/0006/{result.yaml, bvp_consumer.py, bvp-consumer.log, bvp-consumer.json}. Dependency propositions used: C-M5S-003's G_total = 46.80699908016004 under the declared B=0 reading (attempts/0003/numeric-unblinded.log); linearized_einstein.weak_field_monopole's canonical mostly-plus harmonic-gauge monopole −G M/r (src/substrate_framework/linearized_einstein.py 125-165); the committed P240 R=12 order-16 window root (proposals/P240-m5-kinetic-axis/attempts/0042/largeR-roots.json) as background, provenance re-verified by the first ledger check. Affected consumers: C-M5S-005 (consumes the verified monopole tail and the regime warning). Validation receipt: none yet at this boundary.

## Strongest Supported Positive Statement

Accept as drafted, as an applicability-bounded numeric claim carrying BOTH the solved formal object AND the strong-coupling regime verdict — the proposer's framing is correct and no shrinking is warranted: the sector's own mu-averaged static density (declared convention: the global fixed-J constraint term is not a radial source and is excluded from M), tied by a mass identity to the certified background energy M = E_static = 54.70900884959007, sources a second-order flux-form finite-difference Poisson solve on [0, 12] with regular origin and Robin exterior match to the canonical monopole slope, yielding Phi(R) = −213.396523069221 = −G_total·M/R exactly at the 1e-3 normalization gate; the weak-field expansion parameter is epsilon = G_total·M/R = 213.39704390826918 ≫ 1, so the linearized consumer is formally consistent but physically outside its validity regime for this sector at xi=0. Escape routes are registered, not asserted: xi near 1/6 (Delta → 0), a parametrically weaker sector, or nonlinear treatment. The promised radiative attempt is not present in the delivered record and is correctly absent from the drafted statement — it remains open frontier rather than a defect of the solved object.

## Evidence Map
Three evidence groups cover the consumer ledger, the mass identity bridge, and the accepted kernel convention.

| Evidence | Proposition established | Role: exact proof / corroborating subclaim / regression / applicability / provenance | Bridge to claim | Limit |
| --- | --- | --- | --- | --- |
| attempts/0006/bvp-consumer.log + bvp-consumer.json (ALL 7 CHECKS PASS) | Formal Poisson solve with provenance-verified background, mass identity, refinement ladder, Gauss-law monitors, exact monopole normalization, coupling-linearity mutation, and the recorded regime diagnostic | applicability (the claim IS an applicability probe) + corroborating_subclaim for the solve itself | The whole delivered statement | Discretization-bounded (observed FD order 1.31 documented); regime verdict robust to its error bars |
| bvp_consumer.py mass identity (GL sum, never trapezoid-over-weights) | rho integrates to the certified static energy at rel < 1e-6 | corroborating_subclaim | Ties the source to accepted energy ledger | Declared convention excludes fixed-J term from M — stated, not derived |
| linearized_einstein.weak_field_monopole | Canonical exterior kernel −G M/r with mostly-plus sign asserted internally | exact_proof (dependency) | Exterior match convention | Accepted module; not re-derived here |

## Oracle Audit

The strongest practical oracle is the bvp-consumer ledger, and the numeric discipline demanded (refinement + mutation + solver status) is present as recorded. Refinement: a genuine 600/1200/2400 mesh ladder with drifts 1.15e-5 → 4.63e-6, decreasing, d2 < 5e-3 gate, and the observed order 1.31 (degraded from 2 by the near-origin row treatment) documented in the check message rather than gated away — honest reporting of a known systematic. Mutation: the coupling mutation scales G_total by 1.1 and requires the solution to track 1.1*Phi to within 1e-7 (measured 7.2e-9, the sparse-solve roundoff floor); this tests the discrete solve's linearity in the load-bearing coupling input. A second, subtler mutation is the provenance check: recomputed background energy must match the committed value to 1e-9, so a silently substituted root fails at the first gate. Solver status: spla.spsolve is a direct method that raises on singular systems rather than returning a status flag; no status is silently ignored, and any failure mode (singular matrix, NaNs) would propagate into the monopole-normalization (1e-3) and Gauss-law (5e-3 relative at r in {1,3,6,9,11}) gates, which are solution-quality assertions, not just execution receipts. The validity diagnostic is derived live (G_total * m_final / RADIUS) and its check row passes literal True as a recording device — the same recording-row pattern noted under C-M5S-002, but here the recorded quantity is the headline itself and is printed into the JSON payload. I recomputed G_total·M/R = 46.80699908016004 × 54.70900884959007 / 12 = 213.39704390826918, exactly the recorded epsilon, and Phi_R = −213.396523069221 is consistent with −G·M_enclosed/R at the mass identity's 4e-8 relative tolerance. Every check's assertion tests its labeled proposition; none tests something else under the headline's name.

## Findings
Four findings were classified once each, none blocking.

| Finding | Direct evidence | Blocking in boundary / minimum correction / follow-up | What would resolve or overturn it |
| --- | --- | --- | --- |
| validity_diagnostic_recorded is a literal-True recording row counted in "ALL 7 CHECKS PASS" | bvp_consumer.py check body (True with f-string payload) | follow-up — relabel as a record row in any replay; the diagnostic value itself is live-computed and carried in bvp-consumer.json, so nothing accepted rests on the tally | Split ledger tallies into verifying vs recording rows |
| No explicit finite/residual assertion after spla.spsolve | bvp_consumer.py solve_poisson (returns spsolve result unchecked) | follow-up — add an np.isfinite assertion or a residual-norm gate above the 1e-9 roundoff floor; direct-solve exceptions plus downstream quality gates cover the delivered run | One-line hardening; include in the promotion receipt if touched |
| Promised radiative attempt absent from the delivered record | attempts/0006/ contains no radiative artifact; drafted statement omits it | follow-up — correctly omitted from the statement; record as open frontier so the omission is deliberate, not silent | A radiative (time-dependent) consumer construction would deliver it as its own evidence record |
| Near-origin row treatment degrades observed FD order to 1.31 | mesh_refinement_stability check message; result.yaml documents it | follow-up — documented, not gated; acceptable for an applicability probe whose verdict (213 ≫ 1) tolerates order-unity error | A regular-grid treatment of the r=0 row would restore second order if the profile is ever needed at higher precision |

No blocking finding: the solve is non-circular (background provenance gated), dependencies supply what is consumed (G_total from 0003, kernel from the accepted module), and the one affected consumer (C-M5S-005) replays green. The regime finding does not shrink the claim — per the anti-weakening rules the verdict IS the result, and the statement carries both layers.

## Compatibility and Consumers

Conventions: mostly-plus harmonic-gauge monopole from the accepted module; declared density convention (fixed-J term excluded from M) is stated in the script docstring and result.yaml — an explicit hypothesis, not hidden debt. Units are the action's own; epsilon is dimensionless. The two-step trapezoid fallback follows the repository numpy compatibility rule (getattr(np, "trapezoid", None) with np.trapz fallback, evaluated safely). Consumer replay inside the transaction: force_pairing.py builds on the 0006-verified monopole tail and carries the regime warning verbatim; its ledger replays green (attempts/0007/force-pairing.log). The strong-coupling verdict constrains all future weak-field use of this sector and is correctly registered as an escape-route fork, not as a framework conflict. Defects introduced inside this transaction: the two follow-ups above only.

## Four-Axis Decision

Verification: numeric evidence (discretization-bounded solve with refinement and mutation gates) + applicability verdict derived from it.
Review: accepted as drafted (applicability-bounded numeric claim carrying the formal solution and the strong-coupling regime verdict).
Compatibility: native (campaign-local consumer; no canonical contract changed).
Epistemic: active.
Relationship: depends on C-M5S-003, linearized_einstein conventions, P240 committed background; challenges and supersedes none.
Strongest accepted or proposed statement: the registry text below.

Registry-ready final statement (verbatim):

> C-M5S-004 (numeric + applicability): The confined-clock sector's own gravity consumer is solved and regime-diagnosed. With G_total = 46.80699908016004 from the purely-induced composition (C-M5S-003, declared B=0 reading) and the mu-averaged static density of the committed P240 R=12 order-16 window root as source (declared convention: the global fixed-J constraint term is excluded from M; the density ties to the certified static energy M = 54.70900884959007 by a Gauss-Legendre mass identity at relative tolerance < 1e-6), the radially symmetric Poisson problem on [0, 12] — second-order flux-form finite differences, regular origin, Robin exterior match to the canonical linearized_einstein monopole slope — is solved with all recorded gates passing: background provenance re-verified to 1e-9, mesh refinement drifts 1.15e-5 → 4.63e-6 (observed order 1.31, degraded by the documented near-origin row treatment), local Gauss-law residuals < 5e-3 at r in {1, 3, 6, 9, 11}, boundary normalization Phi(R) = −213.396523069221 = −G_total·M/R at 1e-3, and a coupling mutation (1.1x G_total) tracked to 7.2e-9 (sparse-solve roundoff floor). Headline and regime verdict: the weak-field expansion parameter is epsilon = G_total·M/R = 213.39704390826918 ≫ 1, so at xi=0 the sector is strongly coupled to its own gravity and the linearized expansion this consumer assumes is invalid for this sector — the formal solution is clean and recorded, and the decisive result is the regime closure. Consequences registered: weak-field statements about this sector at xi=0 require xi near 1/6 (Delta → 0), a parametrically weaker sector, or nonlinear treatment. The numeric solution is discretization-bounded evidence; the regime verdict is robust to its error bars.

## Promotion Transaction

No registry implementation beyond the claim entry: add C-M5S-004 to governance/claims.yaml with the verbatim statement above, dependencies [C-M5S-003], evidence [attempts/0006/result.yaml, attempts/0006/bvp_consumer.py, attempts/0006/bvp-consumer.log, attempts/0006/bvp-consumer.json, proposals/P240-m5-kinetic-axis/attempts/0042/largeR-roots.json, src/substrate_framework/linearized_einstein.py], verification numeric, accepted_in v0.164.0. No new canonical module or test is required (applicability probe stays campaign-local per the architecture rule). Pin v0.164.0, regenerate docs, synchronize memory, fold into the single promotion validation receipt.

## Correction Check

Not needed — first substantive review; no corrections requested.

## Result and Frontier

The positive result retained is twofold and neither half may be dropped: a formally clean, gate-verified sourced consumer, and the strong-coupling regime verdict that closes the asked question at xi=0 with escape routes registered. Frontier: the radiative attempt (promised, undelivered, correctly unstated) and any of the three escape routes are open campaign work.

## Cross-References

Proposal proposals/P243-clock-sourced-induced-coupling/proposal.yaml; campaign contract memory/vantasner/proposals/P243-clock-sourced-induced-coupling.md; frozen txn local://p243-review-txn.md; evidence attempts/0006/*; dependencies C-M5S-003 review, linearized_einstein.py, P240 0042 largeR-roots.json; consumer C-M5S-005 review; sibling reviews C-M5S-001..003, 005; commit c2efa38.
