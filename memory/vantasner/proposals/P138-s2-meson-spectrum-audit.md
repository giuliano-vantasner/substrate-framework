---
description: Audit S2's hedgehog-fluctuation and meson-spectrum identification
author: vantasner
created: '2026-08-09T08:00:00Z'
updated: '2026-08-09T09:00:00Z'
tags:
- substrate-framework
- campaign-proposal
- hedgehog
- fluctuation-spectrum
- migration-S2
category: proposals
confidence: established
status: archived
---
# P138 S2 Hedgehog Fluctuation and Meson-Spectrum Audit

## Question and Positive Deliverable

P138 must reproduce and adjudicate S2's claim that fluctuation or breather
modes of a hedgehog Skyrmion constitute a meson spectrum. The positive
deliverable is an importable, input-explicit spectral object that states the
time-dependent action, stationary background, perturbation variables, kinetic
inner product, self-adjoint domain, channel decomposition, continuum and
resonance definitions, and scale ledger. It must distinguish vacuum small-field
masses, localized-soliton modes, wall-quantized continuum levels, resonances,
and physical particles. If the exact supportable surface is already accepted,
an exact composition plus predicate-level terminal S2 disposition satisfies
the positive object. Rejecting a meson label or exposing bad eigenvalues alone
does not complete the campaign.

## Base Release and Provenance

The accepted base is v0.105.0 at scientific commit `bb1016e`; the parent
migration checkpoint is `7bb60fe`. S2 is pinned to
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`, path
`merged-framework/bridges/phase-4/bridge_S2_meson_hedgehog_spectrum.py`, and
SHA-256 `48a9eadf6fbc1e3ebe7fcd6b98c2d60cc10a3f5282404c84e4626910f296eaf7`.
Its dossier is separately pinned at
`merged-framework/bridges/phase-4/dossiers/S2-dossier.md`, SHA-256
`74e77d5130c9f2f96132572bd9720d90b8da0902130dfb0866b4b4035de783ed`.

The generated queue exposes ten literal check calls, one assertion, symbolic
and numeric oracle hints, and dependencies B1, PG1, PG2, and PG3. B1 remains
pending and grants no premise. PG1 is qualified through C-SYM-001 and
C-CHI-001, PG2 through C-BRK-001, C-CHI-002, and C-GMR-001, and PG3 through
C-MOD-001, C-MOD-002, and C-SCL-001. The predecessor worktree contains
excluded later Phase 47/48, engineering, and memory work; the S2 and dossier
hashes match the pinned committed baseline.

The queue headline and question necessarily expose the claimed identification.
A prior P131 lexical audit recorded three direct legacy NumPy trapezoid calls
inside immutable S2 but did not execute S2 or import it as science. The P062
audit exposes the nearby positive-eigenvalue and particle-label failure
mechanism through PG3. P138 has not opened S2's scientific body, check literals,
numeric outputs, or dossier comparators before this freeze. That partial prior
exposure is recorded rather than described as full blinding.

## Invariants, Conventions, and Allowed Imports

C-MOD-001 is the exact mixed-term-complete self-adjoint radial Hessian theorem
for one separately declared massless Option-C reduced energy. Its positive
weight, Green form, Derrick tangent, and exact zero continuum edge are fixed;
a positive finite-box level is not a bound mode. C-MOD-002 supplies qualified
float64 evidence for one stationary branch and an inverse-wall-squared box
ladder, but no half-line bound state or resonance. C-SCL-001 proves that an
inverse-time scale, action scale, energy normalization, and quantization rule
remain independent of a dimensionless squared classical eigenvalue.

C-SYM-001 and C-CHI-001 provide exact conditional stationary-symmetry Hessian
and coordinate-metric statements. C-BRK-001, C-CHI-002, and C-GMR-001 provide
conditional local-curvature and parameter ledgers. None derives a physical
chiral action, pion, sigma, meson, Skyrmion, nucleon, quantization rule, or
absolute scale. C-RMAP-001, C-RPROF-001, and C-RPROF-002 may be used only as
declared reduced angular/profile surfaces with their accepted ceilings.

A fluctuation spectrum requires the second variation of a declared
time-dependent action about an actually stationary background, a positive
kinetic form, self-adjoint boundary data, and a declared channel decomposition.
The spectral parameter is a squared classical frequency only after the time
kinetic normalization closes. A bound state lies below the relevant continuum
edge with admissible norm and boundaries. A box level, threshold state,
resonance pole or phase-shift feature, and vacuum particle mass are different
objects. Pending B1 supplies no collective quantization, state, baryon,
spin-statistics, or physical-particle map.

Allowed machinery is exact variational and Sturm-Liouville analysis through
the accepted modules `radial_modes.py`, `rational_map_radial.py`,
`symmetry_breaking.py`, and `explicit_breaking.py`, plus shared numerical,
source-audit, and verification APIs. A newly declared full action or channel
operator must expose every coefficient and remains conditional. Primary
literature may be consulted after freeze for convention and scope checks, not
for importing the desired answer.

## Candidate Preregistration

Six candidates cover literal, compositional, full-field, vacuum, typing, and
governance routes.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal S2 reconstruction | Every source action, operator, mode, and label is actually constructed | Source-defined | Some algebra may survive while the spectrum or particle map fails | Hash-pinned AST, data-flow, execution, and predicate audit |
| B | Accepted radial composition | S2 uses only the massless Option-C radial problem | C-MOD inputs only | C-MOD-001/002/SCL-001 already decide its box and scale claims | Exact formula and numerical-surface mapping without a new claim |
| C | Full hedgehog small fluctuations | A declared time-dependent field action and stationary hedgehog | Couplings, background, channel, domain, boundaries | A conditional channel spectrum may close if the complete quadratic operator is supplied | Independent variation, Green form, sparse spectrum or scattering classification, and refinement |
| D | Vacuum generalized masses | A separately declared chiral vacuum action | Kinetic metric and potential Hessian | Vacuum masses can be exact while remaining distinct from soliton modes | Derive K-inverse-H and construct same-mass/different-soliton countermodels |
| E | Spectral-typing and scale theorem | Only well-typed classical spectral data | Threshold, norm, time/action/energy scales, state dictionary | Equal selected numbers do not identify operators, spectra, or particles | Direct-sum and rescaling counterfamilies with exact type checks |
| F | Governance closure | Accepted authority order | None | Individual claim or exact composition plus terminal S2 disposition | Dependency, cycle, consumer, novelty, impact, compatibility, queue, docs, and memory replay |

## Selection Criteria and Blinding

Selection is ordered by accepted dependency closure; explicit time-dependent
action, background stationarity, kinetic metric, domain, and channel data;
self-adjointness; dimensions and origin/asymptotic regularity; correct vacuum,
zero-source, threshold, and large-domain limits; exact separation of bound,
box, resonant, continuum, and particle objects; assumption and parameter
economy; mutation sensitivity; numerical refinement; independent assembly;
reusable API value; downstream compatibility; and nonduplication.

Named mesons, fitted masses, source eigenvalues, and numerical proximity to any
particle comparator are excluded from concept selection, tolerance choice, and
operator construction. The compatibility tokens and PG3 failure mechanism are
already exposed, but S2's body, check values, and comparator values remain
closed until this contract and its byte-identical manifest are validated and
committed.

## Proposed Claim Delta

P138 provisionally reserves C-MES-001 for a distinct spectral-typing or
complete conditional hedgehog-fluctuation theorem if one closes beyond
C-MOD-001, C-MOD-002, C-SCL-001, and the accepted symmetry/breaking ledgers.
Repository-wide searches find no C-MES-001 in the registry, campaigns,
proposals, durable memory, package, or tests. The identifier is not promoted
merely because it is reserved. If the exact surface is already governed,
C-MES-001 remains unpromoted and S2 closes through composition.

Reverse source consumers are T1Z2, S3, O1, FG2, FG4, P3D2, WZ3, PG1, PG2,
PG3, PG4, WM2, NY1, E1, E2, PN6, WM7, and WM8. Their prior passing tallies or
later narratives grant no S2 authority. P138 will hash-pin the direct graph,
separate already qualified consumers from pending ones, and replay the actual
affected closure. A new claim receives individual review rather than blanket
campaign promotion.

## Implementation and Oracle Plan

The source preflight first audits executable NumPy syntax. Native S2 execution
is preserved as compatibility provenance if its three legacy calls fail under
current NumPy; an isolated wrapper then aliases the immutable name to
`np.trapezoid` and reruns the unchanged science. Mutable P138 scripts use
`np.trapezoid`, the canonical helper, or exact algebra and never use the
removed name or an eager nested fallback.

The primary verifier will pin the source, dossier, and frozen-manifest hashes,
inventory all ten checks and executable imports, and map every predicate to its
actual object. SymPy is the strongest oracle for exact variation, quadratic
forms, coordinate conventions, dimensions, and analytic limits. A genuinely
new spectrum uses float64 SciPy sparse generalized eigenproblems, BVP or
scattering machinery with equations, inner product, domain, boundary
implementation, mesh, wall, tolerance, solver status, residual norm, node or
phase classification, and independent mesh/domain/method refinement. The
independent route must derive the load-bearing quadratic operator or spectral
typing without calling the candidate helper.

Mutations cover the omitted mixed Hessian term, kinetic weight, background
stationarity, mass or breaking term, origin condition, outer wall, channel
label, continuum threshold, scale, action normalization, and particle
dictionary. Soluble free and vacuum limits, equal-eigenvalue distinct-operator
countermodels, and domain growth must break overstrong verdicts. A numerical
rerun of an exactly identical operator is regression coverage, not independent
evidence. Campaign verifiers pin durable evidence and never assert unrelated
future queue states remain fixed.

## Attempts and Continuation

Attempt 0001 freezes the matching prose and YAML contracts before S2 body or
comparator inspection. The prior compatibility-token exposure is recorded and
does not consume a scientific candidate. Later action-derivation, operator,
boundary, spectral, solver, independent-route, consumer, and governance
failures are appended with their mechanism and next materially different
repair. Failure of the literal meson identification triggers Candidates B
through F and cannot close the positive spectral object by itself.

## Debt Ledger

The ledger tracks source predicates, compatibility, action and background,
stationarity, perturbation and channel domains, kinetic and Hessian forms,
self-adjoint boundaries, continuum and resonance definitions, numerics,
scale and particle maps, dependencies, consumers, novelty, and
canonicalization.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| S2 executable surface is not freshly audited | Hash, compatibility preflight, native/alias replay, AST/data-flow audit, and map all ten predicates | closed |
| The action and stationary hedgehog may be declared or incomplete | Inventory the full time-dependent action and prove stationarity before linearization | closed |
| The perturbation operator may omit channels or mixed terms | Derive the full claimed quadratic form, weight, Green form, domain, and channel decomposition | closed |
| Box levels may be called bound or resonant modes | Establish continuum edges, normalizability or scattering criterion, and domain refinement | closed |
| Vacuum masses may be conflated with soliton frequencies | Type both spectral problems and construct countermodels or an explicit valid map | closed |
| A squared eigenvalue may be treated as a particle energy | Close inverse-time, action, energy, quantization, and state dictionaries | closed |
| Numerical evidence may lack status, residual, or refinement | Record solver details and run mesh, wall, tolerance, and independent-method checks | closed |
| Dependencies, consumers, and novelty are incomplete | Audit B1/PG1/PG2/PG3, accepted nearby claims, cycles, reverse consumers, and graph impact | closed |
| Registry, disposition, docs, queue, and memory are unsynchronized | Promote only reviewed distinct claims or close composition, then regenerate governed state | closed |

## Review and Promotion Plan

C-MES-001 receives a separate claim review only if it is distinct,
dependency-closed, sensitive, and independently derived. S2 receives its own
predicate-level source adjudication regardless. Reusable spectral definitions,
operators, or solvers move under `src/substrate_framework/` with focused tests;
literal orchestration remains in the campaign. A terminal qualification names
every accepted mapping and rejected particle clause with durable evidence.
Any release, disposition, queue, generated documentation, and accepted-memory
transaction is validated once at its changed boundary.

## Resolution

P138 closes by exact composition rather than by claim promotion. S2's native
NumPy 2.5.1 abort is a version-only event; an isolated alias backed by
`np.trapezoid` reproduces all ten predicates without changing the pinned source.
The primary 27-check and independent 18-check routes recover the omitted mixed
Hessian correction and the exact zero continuum edge. Corrected finite-box
levels collapse as R^-2 and establish no bound mode. The 293 MeV check bypasses
the solved inertia and round-trips a fitted input. C-MOD-001, C-MOD-002,
C-SCL-001, C-SG-002, and C-SK-001 govern the surviving surfaces; C-MES-001
remains unpromoted. The 20-node graph and 90 focused tests close affected
consumers with no canonical code or release change.


## Done Gate

P138 closes only with the complete positive spectral or exact-composition
object, sensitive primary and independent evidence, individual claim review if
needed, terminal S2 disposition, closed dependencies and consumers,
synchronized governed state, and an empty campaign ledger. A compatibility
abort, rejected meson label, positive finite-box level, or no-go is attempt
evidence and does not finish the campaign.

## Cross-References

See P033, P060, P061, P062, P131, B1, PG1, PG2, PG3, S2, C-SYM-001,
C-CHI-001, C-BRK-001, C-CHI-002, C-GMR-001, C-MOD-001, C-MOD-002,
C-SCL-001, C-RMAP-001, C-RPROF-001, C-RPROF-002, v0.105.0, and the parent
migration effort.
