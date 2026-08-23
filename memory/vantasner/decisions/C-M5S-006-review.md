---
description: Individual claim review record for the P243 continuation batch
author: ox-alpha
created: '2026-08-23T23:20:00+00:00'
updated: '2026-08-23T23:20:00+00:00'
tags:
- substrate-framework
- decision
category: decisions
confidence: established
status: active
---

# C-M5S-006 review — window-background soft-mode adjudication

- claim: C-M5S-006 (numeric_evidence) — window-background soft-mode
  adjudication; ultra-light candidates are spectral-resolution artifacts.
- reviewer: distinct reviewer agent (RevC006), 2026-08-23, one substantive
  pass + correction check by content diff.
- transaction: continuation batch (claims C-M5S-006..009 appended as
  proposed; this claim reviewed against its evidence block).
- verification performed: all eight bottom-block stiffness values and s_b
  match census-v3.json to quoted precision; FD ladder rows[].bottom[0] =
  5.273531800250659e-07 / 4.945872382691154e-08 / 8.644979672269492e-09 at
  N_r = 48/72/96 strictly decreasing; G0 transfer 2.30e-04 vs preregistered
  5% gate (~200x margin); box trend lambda0(R) = 5.705042e-05 / 7.450258e-05
  / 1.013732e-04 rising with R; cross-order stiff_band_max_rel_drift =
  0.5189032861699523 on a genuinely converged different stationary point
  (relgrad 1.83e-14); kinetic metric psd defect 1.1e-17, all Rayleigh
  quotients positive (min 0.3707), tangent null 2.03e-26; soft omega^2
  uncertainty 9.9% declared three times in the entry. FD verdict integrity:
  GRID ARTIFACT labels fire via the pre-declared nodal-growth branch, not
  hard-coded. Dependency closure: C-M5S-001 (N=3) and C-M5S-002 (window
  root identity via largeR-roots.json R12) supply every proposition used.
- blocking findings: none.
- corrections required and applied: scope sentence precision — the FD
  ladder itself spans ~1.8 orders (61x); "four orders" holds only from the
  modal start value; statement reworded accordingly (commit 3051101/19f1049
  chain).
- non-blocking notes recorded: G0 transfer quoted 2.0e-04 vs recorded
  2.30e-04 rounding; stage-2 tally was 1/3 (G3 mutations gate also failed —
  not load-bearing for positivity/tangent-null); exclusion 1 wording nit;
  "systematically obstructed" generalizes from one direct sample plus named
  precedents, within the declared scope note.
- verdict: ACCEPTED (with applied corrections). epistemic: active,
  accepted_in v0.165.0.

## Evidence roles

- attempts/0008/fd-verdict.json + fd_route.py: exact_proof of the collapse
  trend under independent discretization.
- attempts/0008/census-v3.json + window_census.py: regression (block
  spectrum inputs).
- attempts/0008/cross-order.json: corroborating_subclaim (order-ladder
  obstruction mechanism).
- attempts/0008/kinetic-stage2.json: corroborating_subclaim (positive
  metric; tangent null; quadrature sensitivity declaration).
- box_trend_diagnostic (0008 result.yaml): applicability (domain-gift
  disfavoring).
