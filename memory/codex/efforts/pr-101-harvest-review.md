---
description: Corrective review and landing record for PR 101's P236 two-clock GEM Newton-limit campaign
author: codex
created: '2026-08-19T07:54:53+02:00'
updated: '2026-08-19T18:30:00+02:00'
tags:
- substrate-framework
- continuation-pr
- pr-101
category: efforts
confidence: established
status: active
---

## Goal and Success Contract

Review, correct, and merge PR #101 without reducing issue #96 or editing an
accepted claim. The required positive object is a genuinely relaxed shared
M5.8 GEM field whose directly differenced force is attractive and inverse
square on both a growing-box ladder and separate fixed-domain grid refinement,
with mandatory controls and a typed accepted-#89 coefficient bridge.

## Accepted Frontier

Pinned accepted release `v0.163.0`. Accepted inputs C-IGR-004 and C-GRV-002
remain unchanged. C-IGR-004 is conditional and supplies neither a cutoff value
nor a unique numeric normalization; C-GRV-002 supplies the exact attractive
sign map.

## Review Findings and Correction

The source head `5ba1fe63a0c4e37acb0f3ce2e796f12e64c82ea4` was not mergeable as
scientific evidence: its active frame was non-orthogonal, its two tails doubled
the ambient field, the headline rows were not the relaxed state, subtraction
mixed masks, the exponent oracle was circular, the verifier trusted stored
summaries, grid and box effects were confounded, and the #89 numeric dictionary
was unsupported. The campaign preserves that source as attempt 0001.

Attempt 0002 repairs every blocker with the orthogonal M5.17 frame, one guarded
M5.21.8 shared rapidity minimized at every row, common-mask local subtraction,
direct raw-force fits, composite source-aligned quadrature, a separate fixed-D
refinement, independent cylindrical reconstruction, and symbolic Lambda.

## Verified Result

The corrected production and independent pipelines agree on the following
bounded result.

- Growing box 24^3/32^3/48^3: force exponents
  `-2.03198/-2.04361/-2.06018`; coefficients
  `-123.07961/-124.99928/-123.90481`.
- Fixed D=120 refinement: exponents
  `-2.04403/-2.04661/-2.06018`; coefficients
  `-118.31856/-123.82310/-123.90481`.
- Independent cylinder: exponent `-2.02037`, coefficient `-118.32911`, 4.50%
  magnitude difference.
- Zero boost is exact zero. Deleting clock 2's texture collapses peak force
  16.52 times and changes the exponent to `-3.08670`.
- The raw Green kernel is normalized by the explicitly measured `Z_GEM`; the
  accepted conditional `G_total` multiplies the unit-source kernel. No numeric
  cutoff, physical-unit prediction, or accepted-claim change is asserted.

## Validation Ledger

The exact correction boundary has the following validation state.

| Gate | Result |
| --- | --- |
| Corrected campaign verifier | 29/29 pass |
| Independent REFUTE pipeline | 5/5 pass |
| N-3/frame/single-limit | pass |
| Growing-box and fixed-domain convergence | pass |
| Source deletion and zero boost | pass |
| P231 consumer tests | pass |
| Final repository validation and tree receipt | pending landing check |

## Debt Ledger

Empty inside issue #96. The issue explicitly excludes editing OpenWave
MODELS.md and opening the OpenWave PR; those are the user's separate follow-on
discussion, not an obligation of this transaction.

## Promotion and Merge Record

No claim promotion is proposed. The user explicitly authorized the reviewer
to correct and self-merge named PR #101 after the bounded correction check.
Merge/issue/branch cleanup receipts remain pending until landing.

## Cross-References

Issue #96; PR #101; P236 attempt 0002; C-IGR-004; C-GRV-002; v0.163.0.
