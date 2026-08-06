---
description: Terminal qualified disposition review for MK1
author: vantasner
created: '2026-08-06T09:45:00Z'
updated: '2026-08-06T09:58:25Z'
tags:
- substrate-framework
- migration-decision
- MK1
category: decisions
confidence: established
status: archived
---
# MK1 Qualified Review

## Decision

MK1 is qualified at unchanged release v0.155.0 through C-BRK-001, C-CHI-002,
and C-BPS-001. It promotes no new claim or API.

## Retained Scope

The exact positive coefficient match is
`mu_BPS=m*F*sqrt(K)/q`; MK1's `m*F/2` is its declared `q=2,K=1`
specialization. The matching SU(2) trace pair is coordinate covariant, and the
supplied one-cosine potential has exact round-S3 average
`32*sqrt(2)/(15*pi)`.

## Rejected Scope

No accepted claim identifies the dimensional 1+1 medium field, action measure,
onsite coefficient, or gap with the SU(2) BPS potential and physical pion
data. The tail expression simplifies to `2*mu_BPS/F`, so it restates rather
than independently confirms the coefficient relation. The medium-supplied
coupling, physical pion map, selected potential, broken KI2 family, paid
parameter debt, and downstream physical closure are not accepted.

## Evidence and Continuation

Twenty-nine primary, eleven fresh independent, seven aggregate source-graph
checks, and 57 focused tests pass. The graph pins 17 nodes, 129 predicate
sites, and 18 assertions. E1 through E3 use current-first lazy
`numpy.trapezoid` compatibility; no alias or scientific version failure occurs.
MK2 through MK6, MR2, and MR6 remain pending nonauthoritative consumers.
The record-only closeout validates all 872 memory files, repository and skill
contracts, generated-claim no-drift, campaign YAML, and diff hygiene without
repeating the unchanged v0.155.0 full release suite.
