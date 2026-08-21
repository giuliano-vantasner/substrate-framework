---
description: 'P240 attempt 0043: pair oracle on boxed separately-relaxed defects is
  structurally unable to measure the Newton channel (issue 151 item 4)'
author: giuliano
created: '2026-08-21T15:58:48.241434+00:00'
updated: '2026-08-21T15:58:48.241434+00:00'
tags:
- substrate-framework
- campaign
- m5
- issue-151
- pair-oracle
- newton
category: efforts
confidence: working
status: active
---

## Question and Positive Deliverable

Issue 151 Phase 2 item 4 asked whether separately relaxed two-defect hedgehog fields at fixed individual typed momenta produce a positive cross inertia with a 1/r tail, which would turn the conditional Newton formula into a prediction.

## Method

Derivation first: the exact two-clock algebra of attempt 0034 fixes the observable; the composition rule was taken from committed P236 prior art (additive shared-field form, product ansatz historically rejected); the evaluator was built in the certified cpu_energy chart and gated on machine-precision one-body certification before any pair number was inspected. Two protocol amendments (ball mask; summed-angle frame) were documented before corrected results were interpreted.

## Result

The pair oracle resolves negatively for the boxed realization, structurally rather than numerically: (1) deviation supports are disjoint by ansatz because profiles vanish at each wall, so no overlap channel exists; (2) in the summed-angle chart both clock phases enter only through their sum, the counter-rotating combination costs exactly zero, det I = 0, and the fixed-J Legendre transform is ill-posed; (3) naive per-center generators give |C| of order 100-200 against I0 = 0.677, dominated by misaligned-generator probing of the far defect. The only well-defined interaction channel is a repulsive static frame coupling E_int = +457 * d^-1.70 (fit residual 3.5 percent).

## Reusable Mechanisms

- The hedgehog clock is soft only for its own radial generator: matched-generator ball integrals run at the certified scale while misaligned probes inflate by three orders of magnitude. Any multi-defect kinetic measurement must localize each clock's generator on its own defect.
- Gate discipline paid off twice: the G2 self-recovery gate caught an ambient-filling artifact and then a frame-chart mismatch, each of which would have produced confident garbage C(d) values.
- Ball-mask restriction plus single-defect recovery against a certified oracle is a reusable certification pattern for any composite configuration measurement.

## Continuation State

Attempt 0043 records the negative structural result; no claim promotion. The Newton mechanism question transfers to de-boxed profiles or jointly relaxed pairs: issue 151 Phase 3 (natural/Robin or soliton-tail boundaries) is now on the critical path of the mechanism itself. The Coulomb sector item 5 remains defined-blocked (no in-repo charge density for the certified chart).
