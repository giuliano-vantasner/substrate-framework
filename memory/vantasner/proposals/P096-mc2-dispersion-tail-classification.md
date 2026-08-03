---
description: Derive and audit the MC2 physical dispersion and tail theorem
author: vantasner
created: '2026-08-04T15:00:00Z'
updated: '2026-08-04T15:00:00Z'
tags:
- substrate-framework
- campaign-proposal
- dimensional-sine-gordon
- migration-MC2
category: proposals
confidence: exploratory
status: archived
---
# P096 MC2 Dispersion and Tail Classification

## Question and Positive Deliverable

P096 must deliver an importable exact theorem for the linearized physical
sine-Gordon dispersion, real-frequency exterior-tail branches, and the
strongest correct whole-line linear time-harmonic no-mode result. It must keep
those results distinct from nonlinear breather existence, traveling wave
packets, finite-box standing waves, and material selection, then terminally
adjudicate every MC2 subclaim.

## Base Release and Provenance

The accepted base is `v0.81.0` at parent commit `0ea16bb`; the latest
scientific transaction is P095 at `7b4fecc`. The predecessor evidence is pinned
at `substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`. MC2 is
`/home/dan/substrate/merged-framework/bridges/phase-27/bridge_MC2_dispersion_gap_rejection.py`,
15,598 bytes, SHA-256
`b73b5a623ae645b1232b09a3f144eb6429f89fbb0cb130a3d223f42129bacef0`,
and git blob `54fe0f85f72c1bf66cc395517a69a3038fab6407`.

The generated queue marks MC2 pending and exposes its principal dispersion,
band floor, exterior exponent, and gapless and above-gap narratives. P095's
consumer audit also exposed selected MC2 excerpts. Fresh formula blinding is
therefore impossible and is not claimed. P096 has not completed the MC2 body,
executed it, inspected all twenty-one literal predicates or terminal output,
or opened additional consumer bodies and outputs.

Direct accepted sources are release `v0.81.0`, C-MED-003, C-SG-017,
C-SG-011, C-LAT-001, and C-PDE-005, together with their relevant canonical
modules and adjudicated evidence. Memory recall found the parent frontier and
tail-semantics precedents but no accepted physical 1D theorem matching the
proposed claim.

## Invariants, Conventions, and Allowed Imports

The physical root is C-MED-003's declared positive constant-coefficient
cosine density with dimensionless real field, physical `x,t`,
`c=sqrt(T/lambda)>0`, `omega_0=sqrt(mu/lambda)>0`, and
`ell=c/omega_0`. Linearization is about a cosine vacuum and must retain the
mass term. Fourier angular frequency, real spatial wavenumber, group velocity,
phase velocity, exterior decay rate, and normalized frequency remain distinct.

C-SG-017 may cross-check the exact nonlinear tail but cannot derive the linear
spectrum. C-SG-011 fixes the normalized massive limit. C-LAT-001 and C-PDE-005
are nonduplication and semantics references only. Pending MC3/MC4 and all
material or engineering consumers remain nonauthoritative.

The whole-line theorem concerns separated real-frequency fields with spatial
profile in an explicitly declared square-integrable or finite-energy class.
It does not exclude localized traveling pulses of the massless wave equation,
defect-bound modes in a different operator, forced responses, scattering
states, finite-box modes, or nonlinear breathers.

## Candidate Preregistration

The candidate set is frozen before complete MC2 body inspection, execution,
literal-check review, terminal output, or additional consumer inspection.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal MC2 reproduction | Pinned source and environment | Source symbols | Tally validates only implemented predicates | Hash, AST, process status, output, predicate ledger |
| B | Direct vacuum linearization | C-MED-003 and small real perturbation | lambda, T, mu | Physical massive Klein-Gordon equation | Taylor derivative, residual, sign and vacuum mutations |
| C | Fourier dispersion and velocities | Real `k`, positive `c,omega_0` | k | Band `[omega_0,infinity)`, subluminal group velocity | Plane-wave residual, derivatives, limits, mutations |
| D | Exterior tail classification | Real frequency and constant exterior coefficients | Omega | Evanescent below, affine at, oscillatory above threshold | ODE roots, half-line boundary branches, branch mutations |
| E | Whole-line L2 theorem | Real frequency and H1/L2 profile on `R` | Omega | No nonzero global linear time-harmonic eigenmode | Integration identity and independent branch matching |
| F | Nonlinear breather-tail cross-check | C-SG-017 only after spectrum derivation | normalized omega | Exact tail exponent equals the exterior sub-gap rate | Asymptotic log derivative and coordinate conversion |
| G | Gapless traveling-packet counterexample | Smooth compactly supported profile | packet shape | Localized finite-energy traveling solutions exist | Direct d'Alembert residual and energy support |
| H | Boundary semantics | Infinite line versus finite interval | wall position | Walls quantize standing waves but do not prove bound states | Exact boundary spectra and wall-motion dependence |
| I | Consumer audit | Hash-pinned downstream use | none | Consumers inherit theorem ceilings and free scales | Static hashes, actual imports, parameter flow |
| J | Nonduplication and canonical fit | Accepted registry and package | none | Only a distinct physical 1D API merits promotion | Registry, campaigns, package, tests, consumers |

## Selection Criteria and Blinding

Selection prioritizes accepted dependency closure; exact domain, boundary,
norm, sign, Fourier, and unit consistency; separation of the five distinct
solution concepts; mutation sensitivity; correct limiting behavior; parameter
economy; framework fit; consumer closure; and nonduplication. Source check
count, status prose, or later engineering agreement cannot select the theorem.
Main formulas were pre-exposed by the generated queue and P095 snippets, so
the contract freezes the unexposed norm, boundary, theorem, counterexample,
and consumer criteria before the remaining source and output gate.

## Proposed Claim Delta

P096 reserves `C-SG-018`; repository-wide registry, campaign, proposal, memory,
source, and test search found no collision. The proposed dependency set is
C-MED-003 and C-SG-011, with C-SG-017 as the nonlinear cross-check. The claim
will state exact linearization, dispersion and velocities, exterior-tail
branches, the whole-line L2 time-harmonic theorem, and the gapless traveling-
packet ceiling. It challenges and supersedes nothing.

Anticipated consumers are a pure physical-spectrum module or an extension of
the dimensional sine-Gordon module, package exports, focused tests, campaign
verifiers, governance, release, generated docs and memory, and later audited
MC/MD/engineering units. Pending consumers cannot broaden the claim.

## Implementation and Oracle Plan

Reusable exact dataclasses and APIs will live under `src/substrate_framework/`
and expose the linearized residual, dispersion, velocities, exterior branch
classification, and exact profile identities without executing work on
import. SymPy is the strongest oracle for Taylor linearization, plane-wave
substitution, ODE characteristic roots, limits, branch matching, integration
identities, and d'Alembert counterexamples. No numerical solver or quadrature
is needed; specifically no NumPy trapezoidal alias is permitted.

The primary route will call canonical APIs. An independent route will derive
the quadratic form and exterior branches without importing the new API.
Mutations will change mass and gradient signs, omit `c`, confuse `omega` with
`omega^2`, swap evanescent/radiative branches, delete one whole-line boundary,
and treat a traveling packet as time harmonic. Focused replay covers P095,
normalized sine-Gordon, lattice dispersion, and radial tail classification.

## Attempts and Continuation

Every execution or oracle failure is appended under the proposal. A symbolic
branch failure triggers explicit assumptions or a different exact
representation; an overbroad no-go is narrowed to the strongest quantified
positive theorem while the requested classification remains active.

## Debt Ledger

The P096 ledger is empty. Source reproduction, linearization, Fourier
convention, dimensions, branches, norms, half-line and whole-line boundaries,
threshold, counterexamples, nonlinear cross-check, material ceiling,
consumers, nonduplication, independent review, generated state, and queue
disposition all have durable closing artifacts.

## Review and Promotion Plan

The completed review accepted C-SG-018 as a symbolic-verified compatible
extension. Importable logic and tests, all twenty-one source-predicate
decisions, consumer ceilings, qualified MC2 disposition, release v0.82.0,
generated state, and parent continuation are synchronized. The single
integrated workflow gate passed 870 tests; later record edits receive only
record-sensitive validation.

## Results

P096 derives the exact physical vacuum spectrum, phase and group velocities,
and the evanescent/threshold/oscillatory exterior trichotomy. Full-rank
sub-gap matching, affine threshold behavior, and positive norm per
oscillatory period prove that the homogeneous whole-line equation has no
nonzero L2 real-frequency separated mode. The accepted nonlinear breather's
tail rate agrees without being used as an existence proof. Exact flux and
d'Alembert counterexamples prevent radiation and gapless-dynamics overreach.
MC2 is qualified and exact P096 work uses no NumPy quadrature alias.

## Done Gate

P096 is closed: the positive theorem exists, dependencies and consumers replay,
the 45-check primary and 24-check independent exact oracles are sensitive,
every MC2 subclaim is terminally adjudicated, generated state agrees, and the
campaign debt ledger is empty. The parent corpus effort continues to MC3.
