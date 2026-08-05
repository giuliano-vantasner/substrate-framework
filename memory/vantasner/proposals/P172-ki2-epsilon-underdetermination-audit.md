---
description: Audit KI2's structural epsilon underdetermination argument
author: vantasner
created: '2026-08-11T02:00:00Z'
updated: '2026-08-11T02:40:00Z'
tags:
- substrate-framework
- campaign-proposal
- migration-KI2
- parameter-underdetermination
category: proposals
confidence: established
status: archived
---
# P172 KI2 Epsilon Underdetermination Audit

## Question and Positive Deliverable

P172 must determine whether KI2 proves an exact underdetermination theorem for
an explicitly defined near-BPS `epsilon` after refuted KI1 is removed. The
positive deliverable must distinguish: dimensions from values; a family of
accepted parameter choices from a symmetry of one fixed theory; absence of an
accepted selection relation from physical non-identifiability; and KI2's
declared epsilon from C-BPS-003's abstract controlled expansion coordinate.

## Base Release and Provenance

The accepted base is v0.127.0 at clean framework commit `49276b4`, with 163
accepted claims. The source baseline is
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`. KI2 is pinned at
`merged-framework/bridges/phase-34/bridge_KI2_epsilon_underdetermination.py`,
SHA-256
`9e16fc6fafa940f43d559ea0f6a9c2730940d1247f36f655375c2f75f6fd1e81`.
The shared Phase-34 dossier remains pinned at SHA-256
`e01fbee40d81ebae1fc6f9452c321e2914cb185cdf257ae226d849ea6392702b`.
Both paths are clean at the pinned source baseline; unrelated predecessor dirt
is excluded.

Generated inventory and P171 already expose KI2's question, result, dependency
labels, six-check shape, claimed simultaneous `lambda,mu` scaling, and clean
local graph tally. P172 claims no fresh result blinding. It has not opened the
KI2 or dossier body after this campaign began.

Authority recall read v0.127.0, C-BPS-001/002/003, the canonical BPS module,
P171's KI1 refutation, and reviewed E3/E4/S4/NY1/NY2 mappings. Memory search
found P171's warning, P107 BPS reviews, and downstream narrative references but
no prior KI2 adjudication. An initial unsupported `memory search --root`
invocation is preserved; corrected `--base` searches succeeded.

## Invariants, Conventions, and Allowed Imports

C-BPS-001 declares a family of energies indexed by positive `lambda` and `mu`.
For fixed parameters its density contains `lambda^2` and `mu^2`, while its
bound coefficient contains `lambda*mu`. A transformation between allowed
parameter choices is not automatically a symmetry of one fixed energy or its
accepted consumers.

With natural-unit spatial coordinates, the accepted convention gives
`[B0]=E^3`, `[lambda]=E^-1`, `[mu]=E^2`, and `[lambda*mu]=E`. A standard-sector
scale such as `F_pi/e` has energy dimension only under an explicitly accepted
convention. Dimensional consistency does not select values, normalization, or
a physical connection between sectors.

Any epsilon formula must state positivity, normalization, scale inputs, and
whether it is a definition or a derived observable. C-BPS-003 accepts an
abstract positive dimensionless expansion coordinate tending to zero; it does
not identify that coordinate with KI2's ratio or make it numerically small.

Refuted KI1 supplies no premise. KI3, KI4, MK1, MK2, and MK3 remain pending and
may be used only as counterevidence. No baryon, nucleus, reaction, yield,
empirical fit, or substrate premise is allowed. Mutable integration uses
`np.trapezoid` or the canonical helper; immutable legacy-name stops are version
provenance only.

## Candidate Preregistration

The candidates separate literal replay, exact dimension algebra, valid family
underdetermination, the stronger fixed-theory symmetry, invalid dependencies,
pending counterevidence, accepted duplication, possible API work, and record
closure.

| Candidate | Description | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- |
| A | Literal KI2 replay | Execution evidence only | AST and native replay |
| B | Exact dimension solve and monomial basis | Plausible exact algebra | Rank, nullspace, and mutation audit |
| C | Underdetermination across allowed parameterized theories | Plausible qualified ceiling | Construct distinct allowed choices and compare accepted objects |
| D | Epsilon-changing symmetry of one fixed BPS theory | Expected conflict | Transform density, bound, and canonical APIs |
| E | Argument requiring refuted KI1 | Expected rejection | Remove KI1 and replay every premise |
| F | Pending MK relations select epsilon | Noncanonical counterevidence only | Status and dependency audit |
| G | Duplicate accepted free-parameter ceiling | Likely scientific closure | C-BPS object-level nonduplication |
| H | New reusable parameter-orbit API | Only if distinct consumers survive | Package and impact analysis |
| I | Governance closure | Required | Predicate, consumer, queue, memory, and release replay |

## Selection Criteria and Blinding

Selection is ordered by fixed-theory versus parameter-family typing, exact
dimension and normalization closure, accepted dependency fit without KI1,
invariant-observable and counterexample sensitivity, assumption and API
economy, consumers, nonduplication, and governance. The source result and local
tally are exposed; no fresh result or comparator blinding is claimed.

## Proposed Claim Delta

No claim identifier is proposed at freeze. A dimension solution or explicit
free-parameter family may be exact yet already contained in C-BPS-001's
arbitrary positive inputs. A new claim requires a distinct theorem, accepted
dependency closure, reusable API, tests, consumers, and individual four-axis
review. A false fixed-theory symmetry earns no qualified promotion.

## Implementation and Oracle Plan

The primary route will inventory KI2's imports, six predicates, one assertion,
definitions, dimensions, monomial construction, scaling maps, positivity
domains, dependencies, and compatibility surface. SymPy is the strongest
oracle for exponent systems, exact transformations, and counterexamples.

The fixed-theory probe will apply every claimed flow to the accepted
C-BPS-001 density, saturation residual, and bound coefficient. The family
probe will instead construct distinct positive parameter choices admitted by
the same theorem schema and identify exactly which accepted quantities change.
Load-bearing exponent, one-parameter, normalization, and definition mutations
must change the relevant verdict.

A fresh independent route will derive the dimensionless monomial lattice and
parameter orbits without importing KI2 or the primary verifier. P107 evidence
will be hash-reused, with only source-sensitive canonical consumers replayed.
The affected narrative graph will type clean local tallies separately from
accepted authority and scientific premise closure.

## Attempts and Continuation

Attempt 0001 freezes this contract before P172 opens KI2 or the shared dossier
body. It records the exact releases, hashes, clean paths, prior exposure,
authority classes, nine candidates, selection criteria, and the distinction
between a fixed theory and an allowed parameter family. It also preserves and
corrects the pre-freeze memory CLI option error.

Attempts 0002 through 0004 preserve the memory-template preflight failure,
native six-check reproduction, and one command-option error. Attempt 0005
closes 45 primary checks. Attempt 0006 preserves an independent-review function
typo; attempt 0007 closes 21 fresh checks. Attempt 0008 closes 59 typed graph
checks over 81 predicates and ten assertions, and attempt 0009 records a clean
Lean exit with the exact weak theorem encoding. Attempts 0010 through 0012
preserve two record-patch boundary failures and one patch-context failure before
the governed records were synchronized. Attempts 0013 and 0014 preserve an
effort-context and memory-base invocation failure. Attempt 0015 closes 27
focused consumers, and attempt 0016 records two clean 1,478-test executions
with 694 valid memory files.

## Debt Ledger

The P172 ledger tracks the exact source objects, transformation semantics,
dimension/value separation, authority boundaries, and downstream records.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| KI2's exact definitions and predicate reachability are unknown | Pin every definition, check, assertion, import, and runtime result | closed: six predicates, one assertion, SymPy only, native tally exact |
| The claimed flow may change the accepted BPS theory | Transform density, residual, bound, and canonical consumers exactly | closed: density, square, and bound scale by t squared; residual scales by t |
| Dimensionless monomials may be mistaken for values | Derive rank and basis independently and supply value countermodels | closed: exact kernel plus normalization and product-relation counterfamilies |
| KI2 may inherit refuted KI1 | Remove KI1 and classify every remaining premise | closed: family statement survives; every-quantity premise does not |
| Pending MK relations may be treated as authority | Audit status and reverse-consumer effects separately | closed: MK1-MK3 remain pending counterevidence |
| C-BPS-003 epsilon may be silently identified with KI2's ratio | Audit definitions, normalization, and composition requirements | closed: no source or registry map exists |
| Consumers and governed records may disagree | Replay graph and synchronize disposition, queue, memory, and effort | closed: qualified transaction synchronized |

## Review and Promotion Plan

Every KI2 predicate receives an individual verdict. A qualified source may
retain exact dimensional or parameter-family content while rejecting its
fixed-theory symmetry and physical reading. Duplicate evidence applies if all
surviving scientific content is already explicit in accepted claims. Refuted
applies if the load-bearing headline itself is false with no distinct positive
object. No accepted claim, API, release, or generated documentation changes
without a genuinely new closed theorem.

## Done Gate

P172 closes with every listed debt discharged. KI2 is qualified through the
unchanged C-BPS-001 parameter family and C-SK-001 conditional scale. Its
fixed-theory symmetry, all-future impossibility, physical epsilon, and silent
C-BPS-003 identification are rejected. No claim, API, release, or generated
accepted documentation changes.

## Cross-References

See C-BPS-001/002/003, C-RDIFF-001/002, C-SK-001, C-VEC-001, C-EFT-001,
C-CHI-001, P105, P107, P140, P171, E3, E4, KI1-KI4, NY1, NY2, S4, MK1-MK3,
`bps_energy.py`, and the parent migration effort.
