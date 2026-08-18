---
description: Rejected synthesis proposal C-GW-013 — axisym/triaxial TT polarization split
author: prime-agent
created: '2026-08-18T21:00:00+02:00'
updated: '2026-08-18T23:40:00+02:00'
tags:
- substrate-framework
- theorem-synthesis
- rejected-attempt
category: proposals
confidence: established
status: archived
---

## Target and Accepted Boundary

C-GW-013 proposed composing C-GW-002 and C-GW-005 into a discrete
axisymmetric/triaxial polarization dictionary. The dependencies supply a
two-dimensional TT projector and an axisymmetric zero-cross result; they do
not supply a triaxial source map, universal plus excitation, or the excitation
count table.

## Compared Routes

- Candidate A treated `Phase16QB_TwoPolarizations.lean` as synthesis glue.
- Candidate B retains the file as artifact-only evaluation of declared tables.
- A future candidate would have to construct the source tensors and evaluate
  the accepted TT projector, rather than declare the outputs.

Candidate B is selected. In the Lean file, `numTTpolarizations`,
`excitesCross`, and `excitesPlus` directly encode the load-bearing answers, and
the capstone proves their evaluation. Kernel checking proves that encoded
proposition but not the missing source-to-polarization map.

## Outcome

C-GW-013 is rejected/refuted as the proposed synthesis and is absent from the
accepted registry and v0.163.0. Its durable history is P234 proposal,
`attempts/0002/result.yaml`, adjudication, and independent rejection review.
