---
description: Audit GC6 neutral-scalar flavor consequence and final GC verdict
author: vantasner
created: '2026-08-06T08:39:21Z'
updated: '2026-08-06T09:20:05Z'
tags:
- substrate-framework
- campaign-proposal
- migration-GC6
- neutral-scalar-couplings
- flavor-alignment
category: proposals
confidence: established
status: archived
---
# P213 GC6 Neutral-Scalar Consequence Audit

## Question and Positive Deliverable

P213 must derive the exact mass-basis neutral-scalar coupling object behind
GC6's claimed flavor-changing consequence and determine which localization,
scalar-count, and gauge-trace conclusions follow from accepted premises. The
positive deliverable is an importable multi-scalar coupling and alignment
ledger if novel, an explicit spatial-overlap suppression ledger if it adds a
new theorem, a coherent trace/count audit, claim-level source review, and a
terminal GC6 disposition; rejecting the advertised FCNC discharge alone is not
completion.

## Base Release and Provenance

The accepted base is v0.154.0 at clean framework commit `93f7308`, with 196
accepted claims, 12 pending units, and 193 qualified units. GC6 is pinned at
source commit `6d1f4e0`, SHA-256 `e0982294...d18b17`, and 23,292 bytes. Its
candidate inputs are terminal EM6, FG2, FG4, GC1 through GC5, MH2, WM2, WM3,
and WM7 through WM10 at their registered ceilings. Later MK and MR units grant
no authority. The predecessor worktree is dirty outside the hash-pinned GC6
file, so newer prose and unrelated edits are excluded.

The generated queue exposes six static check sites, one assertion, and
truncated claims about a corrected three-doublet construction, spatial FCNC
suppression, and an exact WM7 trace effect. The source body, profiles, matrices,
grids, tolerances, numeric values, thresholds, remaining predicates, guards,
and native output remain unopened through this contract and freeze.

## Invariants, Conventions, and Allowed Imports

GC1 through GC5 are terminal without deriving a physical scalar count,
generation count, stable occupancy, Yukawa interaction, or Standard-Model
construction. C-OVL-001, C-OVL-002, C-OVL-003, and C-OVL-005 supply conditional
expectations, translated tails, finite compression algebra, and an identical-
translation singular-value limit; their profiles, amplitudes, widths, centers,
spaces, and maps remain explicit inputs. C-MIX-001 through C-MIX-003 supply
finite matrix, rephasing, and common-phase algebra but no physical mass basis or
neutral-scalar interaction.

C-RGE-004 through C-RGE-006 require supplied field tables, coefficients,
boundaries, constraints, and matching data. C-RGE-005 explicitly omits same-
order Yukawa terms, so a claimed flavor sector cannot be both omitted from the
calculation and used to complete its physical prediction. Field species,
scalar doublets, localized profiles, fermion modes, generations, Yukawa
matrices, mass bases, and neutral-scalar couplings remain distinct typed
objects. Mutable code uses `np.trapezoid` or `trapezoid_integral`; an immutable
version-only abort receives an alias-only replay and never becomes a scientific
failure.

## Candidate Preregistration

Eight candidates separate exact flavor coupling, spatial suppression, free
geometry, accepted composition, trace-count coherence, guard scope, and
terminal governance.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Multi-scalar mass-basis coupling ledger | Declared Yukawa matrices, VEVs, and biunitary mass bases | finite matrices and scalar labels | Off-diagonal neutral couplings are the exact tree-level FCNC object | Derive every transformed coupling and alignment criterion |
| B | Spatial overlap suppression theorem | Normalized localized modes and declared scalar profiles | widths, centers, amplitudes, tail rates | Suppression is conditional and rate controlled | Exact integral, asymptotic bound, and parameter mutations |
| C | Conditional hierarchy/FCNC tradeoff | One declared geometric family | spacing and tail data | Ratios move together but select no geometry | Vary spacing, widths, and amplitudes without comparator fitting |
| D | No new overlap claim | Existing C-OVL-002/003/005 hypotheses | none beyond accepted claims | Every exact survivor is accepted composition | Registry and API nonduplication audit |
| E | Exact WM7 supplied-table update | Explicit finite field table | declared scalar count | Trace changes conditionally with the table | Rebuild all row contributions exactly |
| F | Coherent count counterfactual | Representation and coefficient tables change together | explicit multiplicities | Boundary-only or symbol-only changes are inconsistent | Mutate both table and coefficients and compare |
| G | Finite anti-fit software guard | Reachable runtime value inventory | source namespaces and values | A finite predicate is not a general scientific theorem | Construct ordinary value-path evasions and lexical collisions |
| H | Terminal governance | Accepted inputs only | none | GC6 closes the GC branch independently | Dependency, reverse-consumer, release, and memory replay |

## Selection Criteria and Blinding

Selection prioritizes exact interaction and basis typing, accepted-invariant
fit, assumption economy, basis covariance, dimensions, signs, limiting
behavior, sensitivity to widths, spacings, amplitudes, scalar counts, and
textures, and novelty beyond accepted overlap and gauge-running surfaces.
Exact alignment, asymptotic suppression, a small sampled ratio, and a physical
experimental bound remain distinct. Source values cannot select a candidate.
Only generated queue metadata is exposed before the manifest, provenance,
memory, repository validation, and freeze commit exist.

## Proposed Claim Delta

P213 provisionally reserves C-MIX-004 for an exact finite multi-scalar
mass-basis neutral-coupling and alignment theorem if C-OVL-003 and C-MIX-001 do
not already own it. The identifier is absent from the registry, campaigns,
proposals, package code, tests, generated documentation, migration records, and
durable memory. Any new geometric overlap identifier will be proposed only
after a post-source nonduplication audit; count underdetermination and a
software guard do not receive scientific identifiers merely for being useful
counterevidence.

Opened inspection confirms C-MIX-004 as the minimum novel surface. For a
declared family `Y_a`, weights `v_a`, mass matrix `M=sum_a v_a*Y_a`, and
biunitary mass basis `D=U_L^dagger*M*U_R`, the individual mass-basis couplings
are `Gamma_a=U_L^dagger*Y_a*U_R` and reconstruct `D=sum_a v_a*Gamma_a`.
Off-diagonal cancellation in the sum does not make each coupling diagonal.
For complex symmetric `M`, a Takagi basis uses `U_R=conjugate(U_L)`; GC6's
`U_L^dagger*I_a*U_L` transform is not the mass-basis coupling. C-OVL-002 already
owns the source geometry's conditional tail dependence, so no new overlap
identifier is proposed.

The alignment corollary retains one necessary edge condition. If
`Y_a=c_a*Y` and `C=sum_a v_a*c_a` is nonzero, then
`Gamma_a=c_a*D/C` is diagonal. If `C=0`, the mass matrix vanishes and an
arbitrary degenerate mass basis need not diagonalize the individual aligned
couplings. This condition is part of C-MIX-004 rather than hidden in a basis
choice.

## Implementation and Oracle Plan

SymPy will derive mass matrices, biunitary transformations, mass-basis neutral
couplings, simultaneous diagonality conditions, exact small-matrix
countermodels, and tractable localized overlaps. General finite-matrix claims
will use exact algebra and operator-norm or singular-value bounds where
required. Numerical source runs are reproduction only when exact objects fix
their output; genuinely unresolved spectral or quadrature evidence must record
the equation, Cartesian measure, domain, normalization, precision, grid,
solver, tolerances, stopping status, scale-relative error norm, refinement, and
independent method.

Mutations change individual Yukawa textures, scalar VEVs, amplitudes, widths,
centers, separation, count, representation rows, coefficients, boundaries, and
matching inputs. Countermodels separate exact alignment from small overlaps and
small overlaps from physical experimental safety. Compatibility preflight scans
direct, imported, dynamic, eager-default, and local-import legacy NumPy access
before native execution. Every source predicate receives an individual verdict,
and the terminal graph imports no later unit.

## Attempts and Continuation

Attempt 0001 freezes the authority boundary, eight candidates, exact and
numeric obligations, object types, countermodels, graph scope, and quadrature
policy before source inspection or execution. If a claimed three-doublet or
FCNC mechanism fails, the campaign continues with the exact multi-scalar
coupling object, a different localization formalism, or accepted composition
rather than ending on the failed headline.

Attempt 0002 finds zero quadrature compatibility surface across GC6, its WM7
dynamic import, and WM7's WM1, SM2, and SM4 transitive imports. Native GC6
reproduces all six checks in 0.90 seconds with exit zero. This establishes
source provenance, not the physical headline.

Attempt 0003 corrects the source's left-basis-on-both-sides transform to the
biunitary mass-basis transform. The corrected ratios at spacings 3, 4, 5, and 6
remain small in the declared model, but a denser 0.25 spacing scan shows rises
from 4.75 through 5.25, refuting the source's sampled monotonic reading. An
exact two-by-two Takagi countermodel has diagonal correct couplings while the
source transform manufactures off-diagonal entries. The WM7 trace reduces
exactly to `3*(8*n_gen+n_h)/(2*(32*n_gen+3*n_h))`, conditional on the supplied
field table.

Attempt 0004 freezes C-MIX-004 and candidates A, C, E, F, G, and H before
implementation. Candidate B remains conditional numeric campaign evidence
already bounded by C-OVL-002, while candidate D is rejected because the general
biunitary multi-scalar reconstruction is not owned by C-OVL-003.

Attempt 0005 preserves the primary verifier stopping after four provenance
checks because YAML loaded the unquoted revision token `0002` as integer `2`.
The type-aware comparison repairs the oracle before any scientific check ran;
no claim, tolerance, or candidate changed.

Attempt 0006 preserves the repaired primary route passing 36 checks before a
brittle registry prose pin searched for wording not present in C-OVL-005. The
check now pins the accepted statement's actual `physical mass or hierarchy`
ceiling; all prior exact, mutation, numeric, and refinement results remain
unchanged.

Attempt 0007 preserves the fresh independent route passing nine exact checks
before structurally comparing factored and expanded versions of the same trace
family. Their simplified difference is exactly zero, so only that independent
oracle is repaired and rerun; the already closed 38-check primary route is not
repeated.

Attempt 0008 tightens the alignment corollary before commit. The aligned family
`(Y,-Y)` with weights `(1,1)` has zero mass matrix while a declared identity
mass basis leaves nondiagonal individual couplings. C-MIX-004 therefore requires
nonzero `sum_a v_a*c_a` for alignment alone to imply diagonality; the candidate,
identifier, and selection remain unchanged.

Attempt 0009 completes the additive implementation. Forty primary checks cover
the canonical exact theorem, mutations, source finite-box reproduction,
corrected biunitary ratios, grid refinement, trace family, authority ceilings,
and spacing counterexample. Eighteen fresh checks rederive the matrix theorem
without the new API and replace the finite-box eigensolver with exact whole-line
Pöschl modes plus adaptive quadrature. All 192 focused package and accepted-
consumer tests pass, and the new canonical module has no NumPy or quadrature
surface.

Attempt 0010 refreshes the GitNexus index at implementation commit `8f5c8fb`
and falls back to its project-local CLI after the MCP transport closes. Both
new functions are low risk with no affected execution process. The exported
dataclass receives a medium graph label only because its package-root export
fans out conservatively to unrelated importers; static symbol search narrows
the actual consumers to the new module, package export, P213 verifier, and
focused tests. The 16-node terminal source graph pins 133 predicates and 22
assertions, passes 39 checks, imports no later unit, and has zero quadrature
surface.

Attempt 0011 preserves three procedural validator-invocation errors: a missing
skill-directory argument, a missing memory path, and a repository-relative
memory path without an explicit base. Corrected invocations validate the
physics skill and all 516 Vantasner memory files without altering a scientific
claim, threshold, or candidate.

Attempt 0012 completes the v0.155.0 promotion boundary. The one full integrated
gate validates 870 memory files and passes all 1,887 tests in 180.23 pytest
seconds and 194.13 seconds wall time with 219,912 KiB peak RSS and exit zero.
No second full gate is run for record-only finalization.

## Debt Ledger

The P213 ledger tracks field species, scalar profiles, doublet labels, fermion
modes, generations, Yukawa matrices, VEVs, mass matrices, left and right bases,
neutral-scalar couplings, overlap domain and measure, amplitudes, widths,
centers, tail rates, spacings, ratios, physical bounds, scalar-count tables,
gauge coefficients, boundaries, omitted terms, compatibility, consumers, and
generated state.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| Source predicates remain blinded | Reproduce once after committed freeze | discharged by attempts 0002 and 0003 |
| Small off-diagonal entries may be mistaken for no FCNC | Derive the exact mass-basis coupling criterion | discharged by C-MIX-004 and attempts 0008-0009 |
| Free geometry may manufacture suppression | Enumerate and mutate every load-bearing overlap input | discharged as conditional model evidence by attempts 0003 and 0009 |
| Three scalar doublets and generations may be imported from rejected GC claims | Audit every field and count map against accepted authority | discharged by individual source review |
| A gauge trace may change incoherently with count | Rebuild representation rows and coefficients together | discharged by coherent trace counterfactual |
| Gauge-only running may be presented as flavor-complete | Preserve C-RGE-005's Yukawa and matching omissions | discharged by source and claim reviews |
| A finite anti-fit guard may masquerade as science | Audit reachable value paths and counterexamples | discharged as finite lexical evidence only |
| Later units may grant backward authority | Replay the terminal graph without MK or MR imports | discharged by attempt 0010 |
| Compatibility may masquerade as science | Audit every executable legacy access shape | discharged with zero surface and zero scientific version failures |
| Promotion and generated state remain open | Complete reviews, disposition, generation, and integrated gate if required | discharged by attempt 0012 |

## Review and Promotion Plan

Every GC6 predicate receives an individual verdict. A novel coupling theorem
requires canonical code and tests, primary and fresh independent exact routes,
claim-level review, impact analysis, registry and release update, generated
documentation, synchronized memory, and one full promotion gate. If no claim
changes, GC6 still requires a structured terminal disposition with materialized
evidence and a record-sensitive closeout. The final disposition must preserve
each rejected physical conclusion explicitly.

## Done Gate

The done gate passes. The neutral-scalar coupling object, alignment and
suppression conditions, count and trace coherence, physical-interpretation
ceilings, countermodels, source-predicate adjudication, authority graph,
compatibility audit, source disposition, generated state, and durable memory
agree with an empty debt ledger. A small sampled coupling ratio or restated
phase verdict is not treated as the positive derivation.
