---
description: Audit CF3's SU(3) center and declared Wilson area law
author: vantasner
created: '2026-08-01T15:54:28Z'
updated: '2026-08-01T16:01:23Z'
tags:
- substrate-framework
- campaign-proposal
- su3-center
- wilson-area-law
- migration-CF3
category: proposals
confidence: exploratory
status: archived
---
# P028 SU(3) Center and Wilson Law

## Question and Positive Deliverable
P028 must derive the center of the accepted explicit SU(3) representation and
its action on fundamental and adjoint objects, then audit CF3's Wilson-loop
logic without treating an assumed area law as its own derivation. The positive
deliverable is importable center/triality algebra and, if distinct, a narrowly
conditional theorem translating a declared rectangular loop law into a static
potential.

## Base Release and Provenance
The accepted base is `v0.24.0` at commit `8ef57bf`. `C-LIE-001` supplies the
standard eight generators and invariants but no center theorem or physical
gauge-sector map. `C-FLX-001` is an ideal fixed-flux geometry and supplies no
Wilson expectation. The hash-pinned candidate is CF3 at
`merged-framework/bridges/phase-10/bridge_CF3_wilson_area_law.py`, SHA-256
`8655579ef3173730c315d60aa821f7085cc131920ae49cb93c60b075d884889d`.
Memory search found no accepted center or Wilson claim.

## Invariants, Conventions, and Allowed Imports
The representation convention is exactly `C-LIE-001`. Center elements must be
unitary determinant-one matrices commuting with all generators, and closure
must be checked independently of labels. Fundamental and adjoint actions must
be separated. A rectangular Wilson expectation may be declared as
`W(R,T)=exp(-sigma*R*T)` only as a premise; it cannot establish why the theory
obeys that law. No physical substrate, quark, gluon, or confinement identity is
allowed.

## Candidate Preregistration
The candidates are frozen from migration metadata before the full CF3 body is
read.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Promote exact center/triality and a separate premise-explicit area-law consequence | C-LIE-001; declared rectangular exponential law for the second claim | Center power, positive `sigma,R,T` | Compatible if the Wilson claim says nothing about law selection | Exhaustive center closure/action plus area/perimeter mutation |
| B | Promote center/triality only | C-LIE-001 | Center power | Preferred if Wilson checks merely substitute the advertised answer | Inventory every Wilson check's independent inputs and outputs |
| C | Promote physical area law and confinement | Nonperturbative gauge measure and sector map | Physical loop and tension | Conflicts absent an independent Wilson oracle | Dependency closure and same-algebra perimeter-law counterexample |

## Selection Criteria and Blinding
Selection is ordered by premise/conclusion separation, exact group closure,
representation consistency, area/perimeter sensitivity, assumption economy,
and distinct consumer reach. Numerical or phenomenological confinement values
cannot select a candidate.

## Proposed Claim Delta
Provisional `C-LIE-002` records that the explicit SU(3) center is
`{omega^k I_3 | k=0,1,2}`, isomorphic to `Z_3`, with fundamental center phase
`omega^k` and adjoint conjugation trivial. Provisional `C-WIL-001` states only
that an independently declared positive rectangular area law
`W=exp(-sigma*R*T)` gives `-lim(log W)/T=sigma*R`, whereas a declared perimeter
law gives an R-independent large-T contribution. It does not derive either law.

## Implementation and Oracle Plan
Extend `su3.py` with exact center elements and representation actions if the
audit passes; put Wilson algebra in a separate pure module. SymPy matrices and
finite exhaustive multiplication are the exact oracles. Mutations change the
root order, determinant phase, representation action, exponent sign, area
`R*T` to perimeter `2*(R+T)`, and string coefficient. Independent review will
classify scalar matrices commuting with the fundamental generators and derive
the large-T limits without package helpers.

## Attempts and Continuation
Attempt `0001` reproduced CF3 and passed twenty-three exact checks. Candidate A
was selected: the complete center theorem and both premise-explicit loop limits
are distinct reusable results. Candidate C fails against the perimeter-law
countermodel without changing any center algebra.

## Debt Ledger
This ledger tracks center completeness, Wilson premise, and interpretation debt.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| Three exhibited scalar matrices may not prove the full center | Solve the commutant and determinant/unitarity constraints | discharged |
| Triality labels may be asserted rather than represented | Apply center matrices to fundamental and adjoint objects | discharged |
| Area law may be the borrowed answer | Mark it as premise and add a perimeter-law counterexample | discharged |
| Conditional loop algebra may be renamed physical confinement | Exclude the map or prove it independently | discharged |

## Review and Promotion Plan
Each proposed claim receives an individual review. Promotion requires package
APIs/tests, immutable attempts, source reproduction/adjudication, terminal CF3
disposition, registry/release/generated synchronization, parent update,
targeted replay, and one full unchanged gate. Mixed exact algebra and rejected
physical interpretation gives CF3 a qualified disposition.

## Done Gate
P028 closes with exact center completeness and representation action, explicit
mutation-sensitive Wilson premises, independent rederivation, qualified CF3
disposition, replayed consumers, and an empty campaign debt ledger.
