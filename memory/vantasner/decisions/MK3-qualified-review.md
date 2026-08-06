---
description: Terminal qualified review of MK3 epsilon pinning
author: vantasner-review
created: '2026-08-06T10:54:05Z'
updated: '2026-08-06T10:54:05Z'
tags:
- substrate-framework
- source-disposition
- MK3
category: decisions
confidence: established
status: archived
---
# MK3 Qualified Review

## Decision

MK3 is qualified through C-BPS-001, C-SK-001, and C-VEC-002. Its exact local
scale-over-product identity and all-premise source-convention substitutions
survive only as conditional algebra; no new claim, API, or release is created.

## Convention and Dependency Corrections

C-VEC-002 requires `lambda_A=pi^2*lambda_BPS`. Therefore the source product
`N_c*m_pi/8` becomes `N_c*m_pi/(8*pi^2)` in the accepted BPS convention and
multiplies the claimed epsilon by `pi^2`. MK1 and MK2 supply no accepted
physical couplings, NY1 retains supplied mass formulas and empirical electron
energy, and `N_c=3` plus the pion mass remain inputs. The local ratio also has
no accepted map to C-BPS-003 epsilon.

## Rejected Extensions

The source's `<1` self-consistency guard reverses after the accepted convention
conversion and is not a theorem of C-BPS-003 in either convention. MK3 also
contains an unchecked factor-of-two prose contradiction, tests t-independence
only after dropping t, overstates prior dependence on `g,m_V`, and reconstructs
the nominally absent 0.929 comparator in executable guard code. A physical
epsilon value, broken KI2 family, near-BPS validation, no-import mass
prediction, paid parameter debt, and substrate mechanism are not accepted.

## Evidence and Terminal State

Twenty-nine primary, sixteen fresh independent, nine graph checks, and 61
focused tests pass. The fifteen-node graph pins 108 predicates and 16
assertions; MK3 is native with no NumPy integration surface, and inherited B1
and E3 compatibility shapes create no scientific version failure. Pending
MK4–MK6, MR2, and MR6 receive no backward authority. The record-sensitive
closeout validates 198 accepted claims, eight pending and zero partial units,
879 memory records, generated state, the physics skill, affected YAML, and
diff hygiene. It reuses P215's unchanged 1,901-test accepted-release gate.
