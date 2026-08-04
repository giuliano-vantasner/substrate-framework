---
description: Audit O1 spin-one polar topology and Berry holonomy against accepted framework claims
author: vantasner
created: '2026-08-10T10:20:00Z'
updated: '2026-08-10T11:25:00Z'
tags:
- substrate-framework
- campaign-proposal
- migration-O1
- spin1-polar-topology
category: proposals
confidence: established
status: archived
---
# P157 O1 Spin-One Polar Topology Audit

## Question and Positive Deliverable

P157 must reproduce and independently audit O1's spin-one polar-state,
projective-director, and Berry-holonomy construction. It must determine whether
any reusable theorem remains beyond accepted C-SPN-001, C-DEF-001,
C-BER-001, and C-HOL-001. The result must keep the polar ray orbit `RP2`, the
phase-retaining full polar manifold `(S2 x U1)/Z2`, and a physical spinor-BEC
model as three separately typed objects.

## Base Release and Provenance

The accepted base is v0.122.0 at framework and scientific commit `5a19786`.
The source baseline is `/home/dan/substrate` commit
`6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`; later dirty engineering,
framework-prose, and memory files remain excluded. O1 is pinned at
`merged-framework/bridges/phase-7/bridge_O1_spin1_bec_rp2.py`, SHA-256
`270877b5ae3507ba5000643333a06269dce2c6a2ec7dbd9ae86f8e2b6e77ef64`.
Its dossier is `merged-framework/bridges/phase-7/dossiers/O1-dossier.md`,
SHA-256
`968e5df0e64739cbf61c7a34091269b99f8602d15450118eae2fd241c47f9aea`.

The queue exposes seven literal checks, one assertion, a symbolic oracle,
dependencies B1, ME1, NA1, and S2, and excerpts naming a rotated reference
polar state, zero spin, an antipodal director phase, local connection one
half, integral pi, and a minus-one value. These unavoidable values are
recorded and cannot select a concept. The source and dossier bodies, exact AST
flow, guards, further constants, and narrative consumers remain unopened.

## Invariants, Conventions, and Allowed Imports

C-SPN-001 already governs the standard pure spin-one carrier, its exact
invariant, the zero-spin polar ray orbit `RP2`, and conditional positive-c2
selection. C-DEF-001 already separates `pi1(RP2)=Z2` from the full polar
manifold's integer deck group. C-BER-001 requires the endpoint transition in
closed-ray holonomy. C-HOL-001 requires representation-typed center data: an
integer-spin `2*pi` rotation is `+I3`, so a projective minus sign must come
from the endpoint or phase quotient rather than a fundamental spinor sign.

Under the accepted Cartesian convention, a real unit director maps to a
normalized polar spinor and director reversal negates the representative but
not its ray. Retaining a physical condensate phase instead gives the diagonal
identification `(d,theta)~(-d,theta+pi)`. The polar ray stabilizer must be
derived, including both rotations about the director and its disconnected
ray-preserving component. A nontrivial projective loop must have the same
transition-corrected Berry holonomy in a real lift and a periodic phase gauge;
a fixed-ray phase is a counterexample, not another proof of the topology.

## Candidate Preregistration

The candidates are frozen independently of the queue-exposed values.

| Candidate | Description | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- |
| A | Literal O1 audit | Retains only exact, correctly typed predicates | AST, data-flow, process, guard, and mutation audit |
| B | Accepted composition | O1 is terminally duplicate or qualified if it contains only accepted orbit, topology, and Berry content | Claim, API, and exact-statement nonduplication |
| C | Explicit polar section and stabilizer | A new claim is possible only if this reusable theorem is absent | Exact spin-one rotations, ray stabilizer, and quotient map |
| D | Embedded Berry gauges | Real and periodic sections agree only after endpoint correction | Direct one-form, transition, and fixed-ray controls |
| E | Typed quotient comparison | Ray `RP2` and full polar order have distinct loop composition | Cover and deck-transformation audit |
| F | Complete physical BEC model | Requires an independently declared action, couplings, trap, boundary data, and ground state | Premise and stationary-field audit |
| G | Physical countermodels | Equal ray or holonomy values leave material and substrate dictionaries free | Alternative carrier, phase, and material maps |
| H | Governance closure | Pending or green sources grant no authority | Dependency, consumer, queue, release, docs, and memory replay |

## Selection Criteria and Blinding

Selection is ordered by basis and rotation agreement; normalization; explicit
global phase and director quotient; ray stabilizer; typed base loop and
endpoint transition; integer-spin representation behavior; real-versus-
periodic gauge agreement; separation of projective and full polar topology;
conditional versus physical BEC premises; mutation sensitivity; assumption
economy; reusability; nonduplication; and semantic-consumer closure. The
queue-exposed `RP2`, one-half, pi, and minus-one values cannot select a theorem
or threshold.

## Proposed Claim Delta

The default delta is empty. C-SPN-001, C-DEF-001, and C-BER-001 already govern
the advertised positive objects, while C-HOL-001 supplies the representation
boundary. A source-aware revision may reserve one exact additive identifier
only if an explicit spin-one director section or ray-stabilizer theorem is
both absent from the accepted closure and useful outside O1.

## Source Inspection Gate

The O1 and dossier bodies remain unopened until this memory contract and the
matching YAML manifest are byte-frozen, validated, and committed. After that
boundary, native reproduction classifies evidence only; a clean exit or green
tally cannot decide novelty or physical meaning.

## Implementation and Oracle Plan

SymPy exact matrices, orbit-stabilizer algebra, and endpoint-corrected Berry
calculus are the primary oracles. A fresh route must avoid any new helper and
derive the director section and Berry result directly. Mutations change the
spin basis, global phase, director sign, endpoint transition, winding,
periodic gauge, representation, quotient, and interaction-sign premise.

Compatibility preflight is explicit: canonical integration uses
`trapezoid_integral`, mutable numeric scripts use `np.trapezoid`, and
executable direct, imported, or dynamic `np.trapz` access is forbidden. If
immutable O1 fails only because of a legacy NumPy spelling, an alias backed by
`np.trapezoid` may reproduce it and the event is version-only rather than a
scientific rejection. The expected exact campaign should need no quadrature.

## Source-Aware Classification

The unchanged O1 source exits zero and prints all seven passes with no NumPy
surface. O1.1 and O1.2 are exact representative regressions for C-SPN-001,
not global orbit or physical ground-state proofs. O1.3 is load-bearingly wrong:
`R_z(chi)|m=0>` is constant, so the declared section is only
`exp(i*chi/2)|0>` with a constant projector. Its local connection is minus one
half and its bare phase is minus one, but its endpoint transition is also
minus one. C-BER-001 therefore gives corrected closed-ray holonomy plus one.

O1.4's two-pi minus sign comes from that inserted U1 half phase; the spin-one
representation itself gives plus identity at two pi. O1.5 retains the
antipodal involution but conflates projective `RP2` with the full polar
manifold and assigns a fundamental SU2 matrix to an RP2 deck label without a
map. O1.6 compares values rather than typed objects. O1.7 is only the narrow
fact that a deliberately chi-independent one-component internal state has
zero spin-frame derivative. Ho 1998, Ohmi--Machida 1998, and
Ruostekoski--Anglin 2003 support complete conditional spinor-condensate models,
not these missing endpoint and typing steps.

Source-aware nonduplication selects Candidate B with A, D, E, G, and H as
audit or ceiling machinery. Candidate C is unnecessary because the accepted
global orbit is stronger than O1's witnesses, and Candidate F's complete
physical premises are absent. Revision 0001 freezes an empty claim delta and
no canonical implementation or release change.

## Attempts and Continuation

Every basis, rotation, stabilizer, quotient, endpoint, representation,
material-premise, compatibility, dependency, consumer, or verifier failure is
preserved append-only with a materially different next attempt. Technical
invocation failures change no scientific candidate; duplicate content leads
to terminal qualification rather than a ceremonial new claim.

## Debt Ledger

The ledger tracks source, dossier, contract, and preexposure hashes; all seven
predicates and one assertion; the spin-one carrier and reference state;
director section, ray, phase, stabilizer, and quotients; Berry section,
endpoint, and gauge; integer-spin center behavior; projective and full loop
groups; physical BEC action, interaction, ground-state, defect, and observable
ceilings; four candidate dependencies; semantic consumers; compatibility;
nonduplication; disposition; generated state; and parent continuation.

All P157 debt is closed. The campaign adds no assumption, parameter, residual,
canonical consumer, or unresolved compatibility surface.

## Review and Promotion Plan

Every affected claim receives individual review. O1 receives a terminal
disposition naming exact retained, duplicate, corrected, and rejected content.
Any distinct theorem is extracted into a pure API and focused tests only after
a frozen source-aware revision. Primary, independent, graph, compatibility,
dependency, consumer, nonduplication, release, queue, documentation, and
memory paths are replayed. One integrated gate runs only if a promotion or
terminal disposition transaction changes governed state.

The terminal review qualifies O1 through unchanged accepted claims and makes
no release or API change. The disposition, generated queue, generated docs,
durable decision record, and integrated gate are the completed transaction.

## Done Gate

P157 closes only when the spin-one convention, polar representative, director
quotient, ray stabilizer, full phase manifold, projective and full loop groups,
Berry endpoint law, all seven source predicates, physical content,
compatibility, semantic consumers, generated state, and debt ledger close
through accepted claims or a reviewed addition. A physical BEC or half-quantum
defect additionally requires a governed action, material parameters, spatial
state, boundary data, stability, and observable evidence.

P157 satisfies this gate by accepted composition and terminal qualification:
the corrected mathematical object exists in accepted modules, every source
predicate has an individual verdict, the semantic graph closes, no new
physical BEC claim is asserted, and the campaign debt ledger is empty.

## Cross-References

See O1, O1-dossier, B1, ME1, ME2, NA1, S2, C-SPN-001, C-DEF-001,
C-BER-001, C-HOL-001, `spin1_mean_field.py`, `angular_defects.py`,
`berry_holonomy.py`, and the parent migration effort.
