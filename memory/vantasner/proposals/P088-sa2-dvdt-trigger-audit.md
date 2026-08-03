---
description: Audit SA2's dV/dt-not-V displacement-current and trigger claim
author: vantasner
created: '2026-08-04T03:10:00Z'
updated: '2026-08-04T03:45:00Z'
tags:
- substrate-framework
- campaign-proposal
- voltage-slew
- migration-SA2
category: proposals
confidence: exploratory
status: archived
---
# P088 SA2 dV/dt Trigger Audit

## Question and Positive Deliverable

P088 must determine whether SA2 derives a dependency-closed physical trigger
whose output is independent of standing voltage and controlled by voltage
slew, or only conditional Fourier and displacement-current identities applied
to an inserted waveform and the rejected SA1 transfer interpretation. The
positive deliverable is an exact DC-shift, transform, waveform, constitutive,
interaction, response, seeding, saturation, breakdown, consumer, and
nonduplication classification, individual promotion of any distinct theorem
that survives, and a terminal SA2 disposition.

## Base Release and Provenance

The accepted base is `v0.76.0`; the latest scientific adjudication is P087 at
commit `c77cae6`, and the parent effort synchronization is `650120c`. The
predecessor is pinned at
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`. SA2 is
`/home/dan/substrate/merged-framework/bridges/phase-25/bridge_SA2_dvdt_not_v_emerges.py`,
9,672 bytes, with SHA-256
`4772f0e52f08e68197662383efe2ee91426769b1281dc2db1d20aa40c8a8398e`
and git blob `5f980f33c1dbb94af07428e709a8d2c4e0878304`.

The generated queue marks SA2 pending and names SA1 and SA4 as candidate
dependencies. Its synopsis exposes the alleged zero-DC intrinsic-kernel route,
a displacement-current `omega^2` route, flat-in-voltage language, and a
rising-and-saturating-in-slew result. Source metadata and the synopsis are
navigation evidence; the SA2 body, literal waveform, equations, checks,
output, thresholds, saturation values, and consumer implementation remain
unopened until the freeze gate.

The accepted sources read directly are the current release, C-SG-015,
C-MED-001, C-DIM-002, C-DIM-003, the canonical sine-Gordon and conditional
constitutive APIs, and P087's terminal SA1 evidence. Memory search found only
the parent continuation and P087 ceiling records; every reused fact is checked
at the registry, campaign, or pinned source.

## Invariants, Conventions, and Allowed Imports

C-SG-015 is an undriven field-trace theorem and explicitly supplies no
susceptibility or seeding map. SA1's Gaussian, overlap-as-population, and
engine readings are rejected dependencies, while SA4 is pending. A positive
SA2 mechanism cannot inherit them through chronology.

For an infinite-time transform, adding a constant can add a distribution
supported at zero frequency; pairing that distribution with a well-defined
kernel that vanishes at zero gives a conditional invariant. A finite window,
sample grid, or nonperiodic record requires its own leakage and boundary-term
ledger. In either case, offset invariance compares `V(t)` with `V(t)+c`; it
does not prove equality across pulses whose amplitude, width, spectrum,
breakdown state, or deposited energy changes with the voltage control.

The conditional continuum identity is `J_D=partial_t D`. Replacing it by
`epsilon*partial_t E` requires a declared linear time-independent
permittivity, and replacing `E` by `V/d` requires geometry and quasi-static
boundary conditions. Fourier multiplication by `i*omega` then establishes a
derivative spectrum, not a coupling, response, absorption, formation, count,
or saturation law. Exact P088 work uses no numerical quadrature or direct
NumPy integration alias; any sampled work must use `trapezoid_integral`.

## Candidate Preregistration

The candidates are frozen before the SA2 source body, checks, literal
waveform, executable output, thresholds, saturation values, or consumer code
are opened.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal SA2 promotion | All named dependencies and consumer objects are accepted | Source premises | Fails if SA1/SA4 or any trigger object is missing | Registry, source, and consumer closure |
| B | Conditional DC-shift theorem | Explicit infinite-domain distribution convention and kernel pairing | Waveform, offset, kernel | Narrow exact invariance only | Distributional support and wrong-DC mutation |
| C | Voltage/waveform distinction | Declared finite or infinite waveform family | Amplitude, offset, duration, shape | Offset invariance is weaker than voltage independence | Same-offset and same-slew counterfamilies |
| D | Displacement-current identity | Declared D(E), geometry, transform, and boundary terms | Permittivity, gap, waveform | Exact derivative identity only | Product rule, units, boundary and transform probes |
| E | Physical seeding response | Driven field interaction, observables, causality, and formation law | Couplings and state | Absent unless explicitly constructed | Dependency and Green-function audit |
| F | Slew and saturation | Frozen one-parameter waveform and positive overlap | Shape, width, normalization | Not universal in scalar slew | Spectral counterfamilies and scale mutations |
| G | Breakdown and consumers | Plasma/boundary dynamics and actual import path | Gap and material inputs | Separate from DC and derivative algebra | Consumer graph and threshold audit |
| H | Source-oracle audit | Every predicate represents its headline | None | Literal samples cannot validate mechanism | AST and load-bearing mutations |
| I | Nonduplication | A distinct theorem, API, and governed consumer exist | None | No new claim if accepted utilities own it | Claim, API, and consumer comparison |

## Selection Criteria and Blinding

Selection is ordered by accepted closure of geometry, constitutive response,
voltage-to-field map, interaction, causal response, absorption, formation,
breakdown, saturation, and consumer; exact transform convention, distribution
pairing, boundary terms, waveform family, dimensions, support, limits, and
mutation sensitivity; separation of offset, amplitude, slew, bandwidth,
current, deposition, and count; parameter economy; and nonduplication. Source
values and output cannot select a concept.

## Proposed Claim Delta

No new claim identifier is assigned. The registry, campaigns, and durable
memory were searched for identifier collisions, and rejected provisional
identifiers remain reserved. C-SG-015 already owns the exact breather field
trace and its response ceiling; C-MED-001 owns only a declared conditional
constitutive ansatz. A new claim proceeds only if Candidate I identifies a
distinct reusable waveform or Fourier-derivative theorem with complete
assumptions, mutation-sensitive verification, an importable API, and a
governed consumer. No accepted claim is challenged or superseded.

## Implementation and Oracle Plan

SymPy is the primary oracle for derivative transforms, distributional support
bookkeeping, finite-window integrals, waveform rescaling, product-rule terms,
units, signs, limits, and counterfamilies. The primary route will pin and
reproduce SA2, audit every source equation and literal, trace SA1/SA4 and the
named consumers, mutate DC support, waveform shape, amplitude, duration,
permittivity, gap, interaction, kernel, threshold, and saturation inputs, and
inspect numerical values only after structural selection freezes. An
independent route will reconstruct the transform and waveform ledgers without
importing P088 expressions.

Reusable package code and tests will be added only for distinct content. A
finite-window or sampled claim must state its window, grid, endpoint
conditions, normalization, leakage metric, and convergence policy. A physical
response requires a driven equation rather than multiplying a supplied
spectrum by `omega^2`. Focused canonical and governance tests, generated queue
and memory checks, one integrated unchanged-boundary gate, and `git
diff --check` close the task.

## Attempts and Continuation

Failed routes are append-only. A missing susceptibility, interaction,
breakdown, saturation, or consumer mechanism is preserved as evidence while
the exact conditional identities, terminal disposition, and corpus
continuation proceed.

## Debt Ledger

P088 tracks transform convention, distribution pairing, finite window,
endpoint and leakage conditions, waveform family, offset, amplitude, slew,
duration, bandwidth, electric field, displacement, permittivity, gap geometry,
voltage-to-field map, current, interaction, input/output observables, retarded
condition, causality, absorption, formation, seeded count, threshold,
saturation, breakdown, consumer, and every accepted or pending dependency.
Every item must be derived, declared, rejected, or excluded.

## Review and Promotion Plan

Review compares primary and independent exact routes, source reproduction and
AST audit, registry and source dependency closure, mutations, candidate
comparison, impact map, consumer inspection, and nonduplication. A terminal
SA2 disposition will name durable evidence and regenerate the source queue.
Any accepted claim receives its own collision-free registry decision, package
tests, release, generated documentation, and memory synchronization; otherwise
v0.76.0 and the package remain unchanged.

## Done Gate

P088 closes only when the positive transform/waveform/current/response/
seeding/saturation/breakdown classification exists, every source predicate has
an individual verdict, both exact routes and mutations pass, affected
consumers replay, campaign debt is empty, and the parent migration can
continue. DC-offset invariance, an `omega^2` factor, a monotone sample, a
source tally, or absence of a physical mechanism is not sufficient alone.

## Cross-References

See SA2, SA1, SA4, P087, C-SG-015, C-MED-001, C-DIM-002, C-DIM-003, the
conditional constitutive and sine-Gordon APIs, and the parent migration
effort.
