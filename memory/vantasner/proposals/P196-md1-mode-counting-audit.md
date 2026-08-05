---
description: Derive the conditional continuum density of states while separating spatial dimension branch count and finite rank
author: vantasner
created: '2026-08-11T20:37:00Z'
updated: '2026-08-11T20:42:00Z'
tags:
- substrate-framework
- research-arc
- migration-MD1
- density-of-states
- mode-counting
category: proposals
confidence: exploratory
status: active
---
# P196 MD1 Mode Counting Audit

## Positive Objective and Success

P196 must produce the strongest exact, importable density-of-states and mode-
counting theorem that follows naturally from accepted framework claims and
explicitly declared continuum-measure inputs. Completion requires separating
spatial dimension, branch degeneracy, exact finite rank, continuum phase-space
volume, and a target-matched cutoff. A no-go against MD1's headline alone is
not completion.

## Authority and Prior Work

The accepted baseline is v0.144.0 at commit `2aa2795`, with 184 accepted
claims. The source baseline is
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`. MD1 is hash-pinned at
`e7408667dbb6644e4c88a0a1523b6eb5f9058c628b5650ff0bf72cfa3238e5ba`.
Its five candidate dependencies are qualified, but only their accepted claim
mappings have authority.

C-MED-003 and C-SG-018 supply a conditional one-dimensional scalar continuum
dispersion and explicitly leave finite-box modes, three-dimensional density of
states, and cutoff separate. C-KRN-001 demonstrates a general declared-d radial
Fourier convention but selects no dimension. D3S and QCD5 supply no accepted
three-dimensional lift of the scalar medium. WN6 rejects a mode count as the
unique missing physical bridge. Memory search found no accepted MD1 result;
all reused facts were rechecked in the registry, canonical modules, and
immutable campaigns.

## Definitions and Invariants

Freeze positive volume `V`, speed `c`, cutoff `K`, supplied positive integer
dimension `d`, independently supplied positive integer branch degeneracy `b`,
nonnegative gap `omega_0`, isotropic dispersion
`omega(k)=sqrt(omega_0^2+c^2*k^2)`, and continuum measure
`V d^d k/(2*pi)^d`. The exact continuum phase-space integral is not an exact
finite lattice-point count. A cell count additionally needs a cell complex,
cell volume, integer divisibility, degrees of freedom per cell, constraints,
and boundaries.

## Candidate Set

Five competing routes separate the continuum theorem, a discrete replacement,
the source specialization, nonduplication, and an exceptional foundation edit.

| Candidate | Construction | Natural-fit case | Expected falsifier | Status |
| --- | --- | --- | --- | --- |
| A | General-d per-branch continuum DOS and integrated ball count | Extends the accepted scalar dispersion with explicit measure inputs | Wrong Gamma, sphere, threshold, or Jacobian factor | untested |
| B | Exact finite periodic hypercubic rank theorem | Honest discrete replacement if topology and component count can be supplied | Continuum ball volume differs from lattice-point count | untested |
| C | d=3 b-branch Debye corollary | Preserves MD1 algebra conditionally | d does not determine b or cell count | untested |
| D | No new claim | Appropriate if A is duplicate of accepted APIs | C-SG-018 explicitly excludes DOS | untested |
| E | Foundational dimensional lift | Exceptional only if independently required | Accepted claims show no pre-existing inconsistency | untested |

## Selection Criteria and Comparator Gate

Selection prioritizes type separation, accepted-framework fit, explicit
measure and boundary assumptions, exact dimensions and limits, mutation
sensitivity, discrete-versus-continuum honesty, nonduplication, and downstream
usefulness. No fresh output blinding is claimed because MD1's formulas and
27-check tally were exposed before P196; the general-d formulas and criteria
are frozen before renewed execution.

## Claim Delta and Ladder

Provisional C-DOS-001 will state the conditional general-d isotropic continuum
DOS, its integrated ball count, independent branch factor, and target-matched
cutoff. It will explicitly reject an exact finite-rank or material-spectrum
reading. The ladder is sphere normalization, inverse-dispersion Jacobian,
general DOS, exact integral and gap independence, branch factor, target cutoff,
d=1/2/3 limits, then discrete counterexample and source disposition.

## Importable Implementation

If Candidate A survives, canonical pure SymPy APIs will live in a new focused
module under `src/substrate_framework/` and be exported and tested. C-SG-018's
dispersion API will be reused where its one-dimensional domain fits; the new
general-d phase-space object will declare its own dimension and measure. Exact
integrals remain symbolic, so no numerical quadrature or NumPy compatibility
surface is expected.

## Attempts

Attempt 0001 freezes v0.144.0, MD1's pinned bytes and prior exposure, five
candidates, ordered criteria, C-DOS-001's provisional formulas and explicit
nonclaims, allowed imports, compatibility rule, and debt before renewed source
execution or detailed predicate audit.

Freeze attempts 0001 and 0002 preserve memory-contract representation failures
before scientific execution; attempt 0003 corrects the schema and passes.
Attempt 0004 reproduces all 27 native MD1 checks with exit zero, 0.68 seconds
wall time, 54,860 KiB maximum resident memory, 19 static check sites, and no
NumPy compatibility surface. The per-branch continuum DOS, phase-space count,
gap independence, and target-matching algebra survive. The source does not
derive a d=3 scalar lift, three branches, exact finite rank, integer cell count,
microscopic cutoff, or participating-mode closure. Candidate A with the typed
Candidate C corollary advances to implementation; Candidate E is rejected
because no accepted foundational inconsistency exists.

## Debt Ledger

Every new assumption or unresolved distinction remains here until a concrete
artifact discharges it.

| Debt | Discharge | Status |
| --- | --- | --- |
| MD1 output and formula were previously exposed | Record exposure and claim no fresh blinding | discharged |
| Spatial dimension may be conflated with branches | Type `d` and `b` independently and mutate them | in progress |
| Continuum count may be called exact finite rank | Supply finite lattice-point counterexamples and explicit ceiling | in progress |
| `V/a^d` may be treated as derived cells | Audit cell topology divisibility and degrees of freedom | in progress |
| Debye cutoff may be called microscopic | Distinguish target matching from a Brillouin zone | in progress |
| General-d scalar lift may import pending structure | Keep dimension and isotropy as explicit claim inputs | discharged by explicit declaration |
| Candidate may duplicate existing claims | Complete claim and API nonduplication audit | open |
| Consumers and governed records may diverge | Replay graph and synchronize queue release docs and memory | open |

## Done Gate

P196 closes only when a positive exact theorem and importable implementation
survive sensitive primary and independent verification, MD1 is individually
adjudicated, dependency and consumer closure pass, generated records agree,
one integrated gate passes at promotion, and the debt ledger is empty.
