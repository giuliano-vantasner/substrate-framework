---
description: Audit W1's parity-odd chiral boundary claim
author: vantasner
created: '2026-08-09T19:35:00Z'
updated: '2026-08-09T19:55:00Z'
tags:
- substrate-framework
- campaign-proposal
- sine-gordon
- parity
- boundary-condition
- migration-W1
category: proposals
confidence: exploratory
status: active
---
# P146 W1 Parity Boundary Audit

## Question and Positive Deliverable

P146 must reproduce and adjudicate W1's claim that a signed spatial-derivative
term in a driven sine-Gordon boundary condition derives parity violation. The
positive deliverable is an exact, importable or accepted-API composition that
transforms the field, operator, boundary point, domain, outward normal, source,
coefficient, initial and boundary data, and any topological diagnostic together;
classifies internal invariance, covariant parameter families, explicit breaking,
and state asymmetry without conflating them; and closes source predicates,
dependencies, consumers, and governance. Merely observing that a derivative is
parity odd or that two numerical responses have opposite signs does not complete
the campaign.

## Base Release and Provenance

The accepted base is v0.112.0 at framework checkpoint `2cf404d`, with
scientific promotion base `069efce`. The predecessor source baseline is
`/home/dan/substrate` commit
`6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`. W1 is pinned at
`merged-framework/bridges/phase-6/bridge_W1_parity_odd_chiral_coupling.py`,
SHA-256 `bfac7d7e4ccb0cdabc6bb2703dadb650c0e09ea883ec3ff70f039231d3e62388`.
Its dossier is pinned at
`merged-framework/bridges/phase-6/dossiers/W1_dossier.md`, SHA-256
`b445fb798e2c5fab53f47eca41895ec140ae3a0d812bd14d11eee0b26c3237a1`.
Both bodies, literal predicates, output, thresholds, and further comparator
material remain unopened before this freeze. The generated queue necessarily
exposed W1's broad parity-boundary headline, candidate dependencies NC1 and NC4,
eight static and literal checks, two assertions, symbolic and numeric hints,
and zero dynamic checks. W1 remains pending adjudication. The predecessor's
uncommitted engineering and Phase 47/48 work remains excluded.

## Invariants, Conventions, and Allowed Imports

P146 preserves the accepted normalized real sine-Gordon equation and exact
scalar-parity convention. C-SG-011 proves that parity preserves that equation,
exchanges kink winding, and transforms the topological current; neither the
naive characteristic derivatives nor sector exchange are independent chiral
conservation laws or physical parity violation. C-SG-013 proves that a fixed
coordinate derivative flips under parity while a half-line outward derivative
is unchanged when the domain and normal transform together. It supplies no
boundary action, coupling, epsilon-to-phase dictionary, weak interaction, or
physical chirality.

For a real scalar field define the fixed-coordinate residual at `x=b` as
`B_(epsilon,J)[phi]=phi_t+epsilon*phi_x-J`. Under
`phi_P(t,x)=phi(t,-x)` and the scalar source pullback, exact chain rule gives
`B_(epsilon,J_P)[phi_P](t,b)=B_(-epsilon,J)[phi](t,-b)`. On the right half-line
`x>=b`, the outward derivative is `-phi_x`; on the parity-mapped left half-line
`x<=-b`, it is `+phi_x`. A coordinate coefficient and a normal coefficient are
therefore different objects, and spatial parity does not act internally on one
fixed half-line unless a separate boundary identification is supplied.

Qualified NC4 may contribute only its accepted exact surfaces and hash-pinned
finite-time evidence after freeze. Its common-phase sign reversal and pi-phase
epsilon-label exchange forbid importing phase-independent chirality, integer
charge transfer, or a physical boundary mechanism. Exact chain rule, domain
orientation, variational calculus, and symmetry definitions are permitted.
W1 becomes noncanonical evidence only after freeze. Pending W2, W3, W5, W7,
M1, and WM7 and the rejected physical readings of NC1 through NC4 are excluded
as authority.

## Candidate Preregistration

Seven candidates separate literal reproduction, coordinate and normal
conventions, action provenance, symmetry classification, numeric data flow, and
governance closure.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal W1 predicate audit | Hash-pinned source after freeze | Source inputs | Narrow transformation statements may pass without proving the headline | Native replay plus AST, dependency, and data-flow audit of all eight checks and two assertions |
| B | Fixed-coordinate boundary-operator pullback | Smooth real scalar, point `b`, scalar source | General `epsilon`, `J`, and `b` | Parity maps `epsilon` to `-epsilon` and `b` to `-b` | Direct chain rule, inverse transform, and sign/source mutations |
| C | Oriented half-line boundary map | Right and left half-lines with declared outward normals | Normal coefficient and source | Domain-plus-normal parity may preserve the normal coefficient | Exact domain orientation ledger and wrong-normal counterexample |
| D | Boundary-action realizability | Local real-scalar boundary calculus, with auxiliaries only if declared | Boundary potentials or extra degrees | A first-order law needs explicit dynamical provenance; a total derivative cannot supply it alone | Endpoint-fixed variation and auxiliary-field comparison |
| E | Symmetry-breaking classifier | Complete transformation of theory and data | Spurion choice or fixed parameter | Family covariance, one-theory invariance, explicit breaking, and state asymmetry separate | Orbit/stabilizer and same-data versus transformed-data countermodels |
| F | Numerical and topological provenance audit | Only source and qualified NC4 evidence after freeze | Phase, drive, width, duration, boundary data | Regression signs need not be parity or integer charge | Data-flow reconstruction, phase mutation, and vacuum-endpoint audit |
| G | Governance closure | Framework contract | None | Required transaction | Novelty, graph, consumer, compatibility, disposition, generated-state, and debt checks |

## Selection Criteria and Blinding

Selection is ordered by exact transformation of field, operator, point, domain,
normal, source, parameter, and data; correct classification of symmetry versus
state response; compatibility with accepted sine-Gordon topology and boundary
semantics; assumption and parameter economy; correct zero-coupling,
parity-center, full-line, half-line, and reflected-domain limits; sensitivity to
sign, side, source, phase, and normal mutations; explicit variational or other
dynamical provenance; reusable value, nonduplication, and consumer closure.
Source outputs and any external values are excluded from concept selection and
thresholds. The source body, checks, output, dossier, and further comparators
remain blinded until this contract, manifest, hashes, conventions, candidates,
criteria, compatibility policy, and done gate are committed.

## Proposed Claim Delta

P146 provisionally reserves C-BND-001 under revision 0001. C-SG-011 already
governs scalar parity, topological current, winding exchange, and the absence of
an inferred weak mechanism; C-SG-013 already governs fixed-coordinate and
oriented-normal boundary correlations without defining a boundary condition.
Repository registry, campaign, package, and durable-memory searches found no
prior use of C-BND-001 and no accepted theorem carrying the general boundary
residual, even/odd decomposition, internal-invariance versus parameter-family
classification, oriented-normal coefficient map, and trace underdetermination
together. C-SG-013 is the direct dependency rather than a duplicate.

The nine anticipated reverse consumers are pending W2, W3, W5, W7, M1, and
WM7 plus qualified NC1, NC2, and NC3. Circular source references grant no
authority; each qualified unit retains only its accepted independent closure.

## Proposal Revision

Revision 0001 activates preregistered Candidates B, C, and E after immutable
source reproduction and source-aware nonduplication. W1 computes a valid
coefficient sign exchange but calls the entire mixed residual parity odd,
equates family covariance with intrinsic violation, and infers charge selection
from separately constructed traces. C-SG-013 already warns about the domain and
normal but does not provide the boundary-residual classification consumers need.
The revision therefore reserves collision-free C-BND-001 before implementation.
The initial proposal, candidate ordering, transformation conventions, selection
criteria, compatibility policy, and source-value exclusion remain unchanged.

C-BND-001 will state the exact scalar boundary-residual theorem. For
`R=a*u+beta*v-J`, scalar parity gives the reflected-point residual with
`beta` replaced by `-beta`. This is covariance of a parameter pair. At a parity
center, fixed-parameter invariance for arbitrary traces requires `beta=0`; a
mixed residual contains an even part `a*u-J` and an odd part `beta*v` and is not
a parity eigenobject. Mapping a right half-line and its outward normal to the
left leaves the normal coefficient unchanged. One residual equation also leaves
the two traces underdetermined and therefore supplies neither the sign
correlation nor the separately defined topological charge transfer. The theorem
adds no boundary action, state selection, weak interaction, particle map,
observation, or substrate mechanism.

## Implementation and Oracle Plan

SymPy and exact symbolic calculus are the strongest oracles for chain-rule
pullbacks, residual equality, coefficient transformations, domain-normal maps,
group action, and endpoint-fixed boundary variation. A primary route may reuse
accepted sine-Gordon and boundary APIs; a fresh independent route must rebuild
the transformations without importing any new P146 helper. If source execution
contains numerical response checks, those are regression evidence only unless
their actual IBVP, data, solver status, error norm, refinement, and independent
route satisfy the simulation contract. Exact algebra will not be ceremonially
rechecked by duplicate numerics.

Every source predicate will be mapped to its evaluated object, inputs, domain,
dependencies, sensitivity, and maximum verdict. Mutations change the derivative
sign, coefficient, boundary side, normal orientation, source parity, field
parity assignment, phase, drive, and vacuum endpoints. Countermodels compare a
parity-covariant `+epsilon/-epsilon` family with a fixed-parameter theory, a
right half-line with its mapped left half-line, and parity-symmetric dynamics
with asymmetric data or solutions.

Compatibility preflight uses the shared AST auditor. Mutable code uses exact
algebra, `trapezoid_integral`, or `np.trapezoid`, never `np.trapz`. Immutable
source receives an explicit alias-only replay backed by `np.trapezoid` only if
native execution reveals a legacy access; that version-only abort cannot select
or reject a scientific candidate. Primary, independent, focused, graph,
consumer, generated, mutation, and source-exit/tally routes must close at the
terminal boundary.

## Attempts and Continuation

Attempts remain append-only. A compatibility, source-replay, symbolic-normal-
form, boundary-orientation, variational, data-flow, or verifier failure is
preserved with its mechanism and repaired without weakening the positive
object. If W1's literal physical concept conflicts with accepted parity
semantics, P146 continues through the exact coordinate/normal boundary theorem,
action-provenance classification, or accepted-API composition. If every exact
surface is already accepted, the campaign completes source mapping and
adjudication without a duplicate claim.

## Debt Ledger

P146 tracks every field and source transformation, coefficient, boundary point,
domain, outward normal, initial and boundary datum, action premise, symmetry
classification, topological hypothesis, numeric input, predicate, dependency,
consumer, compatibility event, and generated record.

| Debt | Discharge artifact | Status |
| --- | --- | --- |
| W1 executable, dossier, predicates, and assertions are unopened | Hash, compatibility preflight, native or alias replay, and predicate-level audit | open |
| Fixed-coordinate and normal coefficients may be conflated | Exact point, domain, and outward-normal transformation ledger | open |
| Family covariance may be called intrinsic symmetry breaking | Single-theory, spurion-family, and state-asymmetry classifier with countermodels | open |
| The boundary law may lack dynamical provenance | Variational audit or explicit independent-law premise | open |
| Numeric signs may be tuned or non-topological | Data-flow, phase/data mutation, and vacuum-endpoint audit | open |
| Existing parity and boundary claims may be duplicated | Registry, package, campaign, and memory nonduplication decision | open |
| Dependencies and nine reverse consumers are incomplete | NC1/NC4 authority audit and frozen graph replay | open |
| Queue, disposition, docs, release, and memory may diverge | Individual review or no-new-claim adjudication and governed terminal transaction | open |

## Review and Promotion Plan

Any new claim receives a fresh independent derivation and individual four-axis
review; no identifier is reserved at freeze. W1 receives a predicate-level
terminal disposition regardless of claim novelty. A qualified decision maps
only exact accepted surfaces and explicitly names every rejected orientation,
symmetry, action, topology, numerical, weak-physics, and substrate clause. A
no-new-claim boundary leaves v0.112.0 unchanged. A final attempt begins in
progress before one integrated repository gate, finalizes after it, and receives
only record-sensitive validation afterward.

## Done Gate

P146 closes only when an exact positive boundary-parity classification exists
through accepted APIs or a distinct reviewed addition, all eight checks and two
assertions are sensitively adjudicated, W1 receives a terminal disposition,
NC1 and NC4 authority and nine reverse consumers close, generated state agrees,
and the campaign debt ledger is empty. A passing source tally, coefficient sign
flip, parity-covariant family, or opposite numerical response alone does not
complete the campaign.

## Cross-References

The governing references are P048 through P051, NC1 through NC4, W1,
C-SG-001, C-SG-011, C-SG-013, provisional C-BND-001, the canonical sine-Gordon
and boundary modules, v0.112.0, and the parent migration effort.
