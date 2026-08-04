---
description: Audit S3's SU(3) WZW collective representation-selection claim
author: vantasner
created: '2026-08-09T10:00:00Z'
updated: '2026-08-09T11:00:00Z'
tags:
- substrate-framework
- campaign-proposal
- su3-representations
- wzw
- migration-S3
category: proposals
confidence: established
status: archived
---
# P139 S3 SU(3) WZW Baryon-Representation Audit

## Question and Positive Deliverable

P139 must reproduce and adjudicate S3's claim that exact SU(3) representation
formulas and a WZW-induced right-hypercharge condition select the physical
baryon octet and decuplet. The positive deliverable is an importable,
convention-explicit SU(3) irrep object that derives dimension, quadratic
Casimir, center triality, complete weights and multiplicities, isospin and
hypercharge from nonnegative Dynkin labels. If a collective constraint closes,
it must separately expose the action, WZW level, winding, left/right generator
conventions, state filter, and every physical import. A no-go for the physical
label, a finite table, or source reproduction alone does not complete P139.

## Base Release and Provenance

The accepted base is v0.105.0 at scientific commit `bb1016e`; the S2 terminal
adjudication is `69321eb` and the parent migration checkpoint is `46a375e`.
S3 is pinned to `substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`,
path `merged-framework/bridges/phase-4/bridge_S3_su3_wzw_baryon_reps.py`,
and SHA-256
`44d8cd1f3a3b3d0a316d0984db92d5e47e13cac9dcf3d476e2d996bf09f13b9a`.
Its dossier is separately pinned at
`merged-framework/bridges/phase-4/dossiers/S3-dossier.md`, SHA-256
`4467a11ac07ac9ffe97826722f28887a28f729f275ca81bbae9ea237346181b2`.

The generated queue exposes ten literal checks, two assertions, symbolic
oracles, and dependencies S2, S4, S5, WZ1, and WZ4. S2 is qualified only
through C-MOD-001, C-MOD-002, C-SCL-001, C-SG-002, and C-SK-001. S5 is
qualified through C-VIR-001, C-MED-001, and C-SK-001. WZ1 is qualified through
C-WZW-001 and WZ4 through C-EFT-001. S4 remains pending. The predecessor
worktree contains excluded Phase 47/48, engineering, synthesis, and memory
changes; the pinned S3 and dossier hashes match the committed baseline.

Durable memory points to P056 through P059. Rechecking their accepted registry
and adjudications fixes the exact distinction: C-WZW-001 supplies no period or
representation selection, C-WZW-002 supplies a mathematical sphere-filling
integer level but no `k=N_c` or baryon map, C-TOP-002 supplies mathematical
winding but no physical baryon current, and C-EFT-001 supplies only conditional
stationary elimination. The S3 queue necessarily exposes its headline Weyl,
Casimir, right-hypercharge, octet, and decuplet claims. S3's source body, exact
checks, finite table, named comparisons, outputs, and dossier body remain
unopened before freeze; the exposure is recorded rather than called full
blinding.

## Invariants, Conventions, and Allowed Imports

C-LIE-001 fixes Hermitian fundamental generators `T_a=lambda_a/2`, trace
normalization one half, C_F=4/3, C_A=3, and no physical sector. C-LIE-002 fixes
the exact center and abstract triality character. C-WZW-001 uses the
anti-Hermitian basis and real trace-five form with unnormalized alternating
sum. C-WZW-002 fixes the primitive oriented S5 period and an integer
sphere-filling coefficient. C-TOP-002 fixes the mathematical SU(3) winding
current and endpoint charge. None grants `N_c`, a collective action, physical
baryons, representation selection, a mass formula, or anomaly dynamics.

Dynkin labels p and q are nonnegative integers. The candidate irrep convention
uses highest U(3) Gelfand-Tsetlin row `(p+q,q,0)`. Interlacing patterns determine
all basis states. In the standard fundamental hypercharge convention
`Y=2*T8/sqrt(3)`, each pattern has
`I=(m12-m22)/2`, `I3=m11-(m12+m22)/2`, and
`Y=m12+m22-2*(p+2q)/3`. The quadratic Casimir must reduce to 4/3 for `(1,0)`
and 3 for `(1,1)`, matching C-LIE-001. Center triality is `p+2q mod 3` in
C-LIE-002's convention. These formulas are frozen as candidates and must be
independently derived before acceptance.

A filter asking whether an irrep contains one supplied exact hypercharge is
kinematic. It does not choose a state within a multiplet or distinguish all
same-dimension and conjugate irreps. A physical collective-state claim needs a
declared SU(3) configuration space, left/right action, Hilbert-space measure,
WZW linear velocity term, canonical generators, spin/isospin and statistics
conditions, Hamiltonian, symmetry breaking, and state/observable map.

Allowed machinery is exact SymPy and finite integer combinatorics in a new pure
module if selected, plus accepted `su3.py`, `wzw.py`, `source_audit.py`, and
`verification.py`. Primary literature may be read after freeze for exact
conventions and scope, not for importing a desired octet/decuplet answer.

## Candidate Preregistration

Six candidates cover literal, general irrep, conditional-filter, collective,
compositional, and governance routes.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal S3 reconstruction | Every formula, table, constraint, and label is actually derived | Source-defined | Some group arithmetic may survive while selection or physics fails | Hash-pinned execution, AST/data-flow, and ten-predicate audit |
| B | Complete SU(3) irrep theorem | Nonnegative Dynkin labels and accepted generator convention | p and q | Dimension, Casimir, triality, and complete weights close without physical imports | Weyl formula versus independent Gelfand-Tsetlin enumeration and fundamental/adjoint/conjugation mutations |
| C | Conditional right-hypercharge filter | Candidate B and supplied exact Y_R | Y_R and a finite label search domain | Minimal dimension can be derived but ties and exotic irreps remain visible | Complete enumeration, minimality certificate, conjugate and omitted-table counterexamples |
| D | Declared collective-WZW constraint | Explicit SU(3) collective action, level, winding, generator signs, and canonical quantization | level k, winding B, inertias | A conditional right-generator constraint may close without identifying k with N_c or states | Independent canonical momentum derivation, orientation/level mutations, zero-level and zero-winding limits |
| E | Accepted composition and typing | Existing C-LIE/WZW/TOP surfaces only | None | S3 may close through exact composition if no distinct representation theorem remains | Exact nonduplication and predicate mapping with physical ceilings |
| F | Governance closure | Accepted authority order | None | Individual claim or terminal source composition closes | Dependency, cycle, consumer, novelty, impact, compatibility, queue, docs, and memory replay |

## Selection Criteria and Blinding

Selection is ordered by accepted dependency closure; complete representation
carrier and normalization; exact integer multiplicities; consistent Casimir,
triality, isospin, and hypercharge; complete finite-table and tie handling;
correct fundamental, adjoint, conjugate, zero-level, zero-winding, and
orientation limits; assumption and parameter economy; mutation sensitivity;
independent derivation; reusable API value; downstream compatibility; and
nonduplication.

The queue has exposed the claimed formulas and named octet/decuplet outcome, so
those values are treated as visible comparators, not hidden inputs. Equations,
candidate conventions, structural criteria, and tests are frozen without
opening the exact S3 table or check bodies. Named baryons, masses, and empirical
assignments cannot choose the candidate, formula, normalization, or threshold.

## Proposed Claim Delta

P139 provisionally reserves C-IRR-001 for a complete exact SU(3) Dynkin-label
irrep theorem and conditional supplied-hypercharge filter if it closes beyond
C-LIE-001 and C-LIE-002. Direct searches find no C-IRR-001 and no canonical
Gelfand-Tsetlin, Weyl-dimension, full-weight, or right-hypercharge-selection API
in the registry, campaigns, proposals, memory, package, or tests. The identifier
is not promoted merely because it is reserved. A separate physical collective
claim is not preregistered unless Candidate D closes with a genuinely distinct,
dependency-complete statement.

Reverse source consumers are W2, QCD1, WZ1, WZ2, WZ3, WZ4, AS8, WM2, PN6,
WM7, WM8, MK1, and MR2. Their chronology and tallies grant no S3 authority.
P139 will hash-pin the actual graph, preserve accepted consumer closures, and
keep pending units pending. Any new claim receives individual review.

## Implementation and Oracle Plan

The source preflight first audits executable NumPy syntax after freeze. Any
immutable compatibility abort is preserved and replayed through an isolated
alias backed by `np.trapezoid`; mutable P139 scripts use current APIs or exact
algebra. No sampled integration is expected for the representation theorem.

Candidate B uses exact integer validation and a pure API returning Gelfand-
Tsetlin patterns and aggregated weights. The canonical route derives the Weyl
dimension and Casimir, enumerates interlacing patterns, and checks the pattern
count. A fresh independent route will use a Weyl-character or root/string
construction without importing the candidate helper. Tests cover singlet,
fundamental, antifundamental, sextets, adjoint, decuplet, antidecuplet, larger
labels, p/q conjugation, center triality, exact multiplicity sums, and wrong
normalizations.

Candidate C enumerates every irrep in a declared finite label domain, proves
the returned minimal dimension within that domain, reports all ties, and
constructs omitted-conjugate and same-filter counterexamples. It never calls a
finite favored source table complete. Candidate D is exact symbolic mechanics:
derive canonical momentum from the declared velocity-linear term and mutate
its sign, coefficient, level, winding, and generator normalization. An exact
identity copied as an input is regression evidence, not an independent route.

The primary verifier pins source, dossier, frozen manifest, accepted claim
surfaces, every source check, data flow, and all new APIs. Mutations cover p/q
interchange, noninteger/negative labels, missing GT patterns, Casimir factors,
hypercharge scaling, triality, representation truncation, WZW orientation,
level, winding, k=N_c, state labels, and mass assignments. Source consumers
and generated state replay only after candidate selection.

## Attempts and Continuation

Attempt 0001 freezes the matching prose and YAML contracts before S3 source or
dossier inspection. Later source, representation, collective-action,
normalization, mutation, consumer, or governance failures are appended with
their mechanism and materially different next route. Failure of the physical
baryon headline triggers Candidates B through F and cannot close the positive
representation object by itself.

## Debt Ledger

The ledger tracks source predicates, compatibility, irrep completeness,
normalizations, collective action, WZW and topology links, state and physical
maps, dependencies, consumers, novelty, and canonicalization.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| S3 executable and check surfaces are unopened | Hash, compatibility preflight, native or alias replay, AST/data-flow audit, and all ten predicates | closed |
| General irrep formulas and multiplicities may be incomplete | Independent Weyl and Gelfand-Tsetlin derivations across exact domains and mutations | closed |
| Hypercharge filtering may omit ties or conjugates | Complete declared-domain enumeration, minimality certificate, and omitted-table counterexamples | closed |
| The right-hypercharge constraint may be assumed | Derive it from an explicit collective action or retain it as a declared conditional input | closed |
| Mathematical WZW level may be identified with N_c or baryon number | Audit level, winding, orientation, topology, and every physical bridge separately | closed |
| A weight filter may be called a physical state selection | Inventory Hilbert, generator, spin, statistics, Hamiltonian, breaking, and observable premises | closed |
| Dependencies, consumers, and novelty are incomplete | Audit S2/S4/S5/WZ1/WZ4, accepted nearby claims, cycles, reverse consumers, and graph impact | closed |
| Registry, release, disposition, docs, queue, and memory are unsynchronized | Promote only reviewed distinct claims or close composition, then regenerate governed state | closed |

## Review and Promotion Plan

C-IRR-001 receives an individual claim review only if its complete exact
surface is distinct, dependency-closed, sensitive, independently derived, and
reusable. Reusable representation logic moves under `src/substrate_framework/`
with focused tests; orchestration remains in P139. S3 receives predicate-level
adjudication regardless. A terminal qualification names every accepted mapping
and rejected physical clause with durable evidence. Release, disposition,
queue, docs, accepted memory, and parent-effort state update once at their real
changed boundaries.

## Resolution

P139 promotes C-IRR-001 in v0.106.0. Exact Gelfand--Tsetlin and independent
semistandard-tableau routes close arbitrary-label dimensions, Casimirs,
triality, complete weights, and SU(2)xU(1) rows. The bounded hypercharge filter
shows a unique minimum octet at Y=1 and a dimension-ten
antidecuplet/decuplet tie. S3's sextet convention, completeness claim,
collective and WZW imports, decuplet mass formula, and physical baryon reading
are corrected or rejected. Primary, independent, graph, and focused routes
pass 28, 16, 39, and 31 checks; LOW impact and an empty ledger close the
campaign.

## Done Gate

P139 closes only with the complete positive irrep or exact-composition object,
sensitive primary and independent evidence, individual review for any new
claim, terminal S3 disposition, closed dependencies and consumers,
synchronized governed state, and an empty campaign ledger. A reproduced table,
WZW slogan, rejected baryon label, or no-go does not finish the campaign.

## Cross-References

See P024, P028, P056, P057, P058, P059, P138, S2, S3, S4, S5, WZ1, WZ2,
WZ3, WZ4, C-LIE-001, C-LIE-002, C-WZW-001, C-WZW-002, C-TOP-002,
C-EFT-001, v0.105.0, v0.106.0, and the parent migration effort.
