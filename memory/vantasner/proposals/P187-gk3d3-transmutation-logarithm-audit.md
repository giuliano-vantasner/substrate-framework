---
description: Audit GK3D3 and derive a provenance-complete scale-matched kinetic ledger
author: vantasner
created: '2026-08-11T13:08:00Z'
updated: '2026-08-11T13:08:00Z'
tags:
- substrate-framework
- campaign-proposal
- migration-GK3D3
- dimensional-transmutation
- kinetic-matching
category: proposals
confidence: exploratory
status: active
---
# P187 GK3D3 Transmutation Logarithm Audit

## Question and Positive Deliverable

P187 must determine whether GK3D3 derives the physical scale identifications
needed to close the matter-induced kinetic logarithm. The positive deliverable
is an importable exact ledger composing arbitrary positive lengths, explicit
inverse-length energy conversions, C-RGE-003's formal one-loop hierarchy, and
C-VAC-003's affine kinetic family without losing the independent matching
coordinate. It must characterize the separately imposed zero-matching branch
and any resulting conditional effective coupling without calling supplied
labels or inputs predictions. Showing that the source imports an identification
or erases a boundary value is attempt evidence, not completion.

## Base Release and Provenance

The accepted base is v0.138.0 at clean framework commit
`ba1cbaf3dfcdd34d36fc22c1c6105c27cbac2d36`, with 178 accepted claims. Its
manifest SHA-256 is
`55916c2f626ebcd2afdb6461de485d35c850e22fbf439c78d9cbccea08004591`.
The governed predecessor baseline is
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`. GK3D3 is pending at
`merged-framework/bridges/phase-41/bridge_GK3D3_transmutation_closes_the_log.py`,
SHA-256
`1c3f81d15ace3ec2c6326c89659596f5b9ff84ac23ef7f0143a53ad92b23b211`,
size 21,995 bytes, blob `d4efb0d8d96d4368272902683c54df6bf3af7b80`, and sole
history commit `7222eed`. The target path is clean at the governed source
commit; unrelated later source-worktree artifacts have no authority.

The generated queue already exposes the proposed maps
`Lambda_UV=hbar*c0/a` and `m=hbar*c0/xi`, their cancellation to
`log(xi/a)`, substitution of a one-loop exponent, the claimed
`g_eff^2=b0*beta^2/b`, fourteen static and literal check sites, no dynamic
checks, one assertion, and a positive closure synopsis. P187 therefore claims
no fresh source-result blinding. Exact imports, formulas, conventions,
predicates, assertion dataflow, and conclusion edges remain unopened until the
freeze validates and is committed.

## Invariants, Conventions, and Allowed Imports

C-RGE-003 owns the exact two-length dimension kernel and the formal one-loop
energy/length map. It leaves the length labels, conversion factors, beta
coefficient, coupling squared, reference energy, absolute scale, and physical
interpretation supplied. C-IDN-002 proves that the later gravity-plus-length
system retains a one-dimensional nullspace and that backsubstitution into a
defining row is inverse reconstruction. C-DIM-007 leaves its one-scale tension
coefficient free. C-DIM-009 supplies bookkeeping only. C-VAC-003 owns
`Z(mu)=Z_ref+b*log(mu_ref/mu)/(8*pi^2)` and keeps `Z_ref`, matching scales,
matter weights, group data, and physical labels independent.

P187 may use exact positive-scale, inverse-length conversion, logarithm,
affine-flow, and rank-identifiability algebra. A map from a length to an energy
has the declared form `E=K/ell` with its own positive `K`. Identifying the
short length with a UV matching scale and the long length with a charged
excitation mass is separate model data. Setting both conversion factors to
`hbar*c`, assigning unit soliton mass coefficient, identifying the affine
reference scale with the UV scale, or imposing `Z_ref=0` are distinct premises.
Hash-pinned GK3D3 and its source dependencies and consumers are noncanonical
evidence only after this freeze. Mutable quadrature uses `np.trapezoid` or
`trapezoid_integral`; immutable legacy-name aborts are version-only
compatibility evidence and never scientific candidate failures.

## Candidate Preregistration

Six candidates separate literal reproduction, general conversion algebra,
consistent transmutation composition, matching alternatives, physical-label
countermodels, and governed closure.

| Candidate | Object | Structural gate |
| --- | --- | --- |
| A | Hash-pinned source reproduction and predicate audit | Every import, scale map, cancellation, check, assertion, and conclusion edge is typed |
| B | Arbitrary two-length energy map | Independent conversion factors remain visible in `log[(K_uv/K_ir)*(ell_ir/ell_uv)]` |
| C | Consistent one-loop length/energy composition | Paired C-RGE-003 conversions cancel exactly while all one-loop inputs and `Z_ref` survive |
| D | Competing affine boundary models | Free, explicitly zero, and measured matching remain distinct before any effective coupling is defined |
| E | Physical-identification countermodels | Unequal conversions, soliton coefficient, reversed labels, and common rescaling expose imported premises |
| F | Governed closure | Claim, source, consumers, release, queue, docs, memory, and debt agree |

## Selection Criteria and Blinding

Selection is ordered by accepted scale orientation and physical-label
provenance, exact conversion and dimensional consistency, preservation of the
affine reference coordinate, separation of supplied one-loop inputs from
outputs, rescaling and conversion covariance, correct limiting behavior,
assumption and parameter economy, independent exact rederivation, mutation
sensitivity, novelty beyond accepted claims, and global closure. Numerical
closeness cannot select a scale map or boundary. The queue already reveals the
broad source result, so the meaningful gate is frozen structural criteria
before the implementation body and detailed output open.

## Proposed Claim Delta

P187 provisionally reserves C-VAC-004 for the distinct exact composition of
C-RGE-003 and C-VAC-003: two independently converted lengths determine a
conditional scale-ratio logarithm; when those lengths are consistently the
inverse-energy images of the declared one-loop reference and transmuted
energies, the conversion factors cancel; the affine `Z_ref` remains; and only
an explicitly imposed zero-matching branch yields a conditional inverse
kinetic coupling. Repository-wide registry, campaign, source, package, test,
and durable-memory searches find no identifier collision or existing
scale-matched kinetic API. If the source audit or nonduplication review shows
that the composition adds no claim-level content, the identifier remains
reserved and the implementation is governed as a consumer theorem rather
than promoted by ceremony. The proposal has no `supersedes` edge. Likely
consumers are GK3D3 through GK3D6, EL2, HE5, scale-transmutation and vacuum-
polarization APIs, tests, registry, release, generated records, migration
disposition and queue, and later gauge-sector claims.

## Implementation and Oracle Plan

The source audit first pins AST and NumPy compatibility surfaces, native
execution, every imported dependency, scale label, energy conversion,
logarithm orientation, transmutation substitution, affine boundary,
effective-coupling definition, predicate, assertion, and conclusion edge.
Reusable equations belong in a pure package API; imports run no simulation or
tally.

The primary symbolic route derives `E_uv/E_ir=(K_uv/K_ir)*(ell_ir/ell_uv)`
from the two declared inverse-length maps and composes that exact ratio with
the affine kinetic family. A second route substitutes C-RGE-003's paired
length ratio `(K_ir/K_uv)*exp(X)` and proves the conversion factors cancel to
`X`, without assuming they are equal. It retains `Z_ref` and then evaluates,
but does not infer, the explicit zero-matching specialization. An independent
implementation must not import the new claim module and must reconstruct the
ratio, cancellation, affine family, conditional inverse, and identifiability
counterexamples from raw SymPy algebra.

Mutations exchange the length orientation, perturb either conversion factor,
insert a soliton mass coefficient, change `Z_ref`, alter the matter weight or
beta coefficient, break the matching-scale identification, and treat a
backsubstitution as a fresh row. Counterexamples compare identical lengths
with unequal conversions, identical scale logarithms with unequal affine
boundaries, and common-rescaled lengths with unchanged ratios but different
absolute scales. Equal lengths, equal conversions, zero matter weight,
zero-matching, common rescaling, and positive-kinetic domains remain separate
limits. SymPy is the strongest practical oracle because every obligation is
exact algebra; numeric reruns would be regression coverage, not independent
evidence.

Compatibility preflight inspects executable direct, imported, and dynamic
legacy trapezoidal access, including eager nested `getattr` defaults. Mutable
code is repaired to `np.trapezoid` or the canonical helper before scientific
adjudication. Immutable source receives a recorded alias-only replay when
required, and that environment event never rejects a candidate.

## Source Audit Result

The hash-pinned source passes all fourteen runtime checks without a NumPy
compatibility event. Its exact cancellation of a shared inverse-length energy
conversion, conditional `log(exp(X))=X` reduction, zero-matching algebra, and
common length-rescaling identity survive as candidates after their premises
are restored.

The load-bearing physical and boundary claims do not survive their cited
sources. C-RGE-003 leaves both length labels, both conversions, `b0`, the
coupling, the reference scale, and physical interpretation supplied.
C-IDN-002 proves that AS7's gravity-plus-length system has a one-dimensional
nullspace, so its reported coupling is inverse reconstruction after a third
coefficient is supplied, not an upstream over-determination. C-VAC-003 retains
`Z_ref`; neither rung25 nor GK3D2 sets it to zero after charged matter is
introduced.

The source predicates do not repair those gaps. Check 0b searches mutable live
file prose. Check 0c defines the desired exponential before taking its log.
Checks 1a and 1b set both conversion factors and the soliton coefficient to one
before testing cancellation and symbol count. Check 2a overwrites its first
scale-ratio expression. Checks 2b and 2c inherit the rejected zero boundary and
then invert it. Check 2d partly subtracts an expression from itself. Check 3c
multiplies a defined reciprocal back to its input. Check 4b never inspects the
data surface.

The power-law argument is also false at claim scope. Dimensional exponent zero
gives a constant, not a logarithm, and C-DIM-009 already shows that dimensions
do not select a loop form factor. A logarithm is not the unique function whose
composition with `exp(X)` is rational: constants, powers and rational
functions of `log(y)`, and `1/log(y)` are immediate counterfamilies. The
source's perturbativity check inserts `b0=7` and `beta^2=0.245` despite calling
them derived free inputs, samples two matter weights, and does not establish a
general loop-validity domain.

## Corrected Formula Freeze

Let `ell0`, `ell1`, `K0`, and `K1` be independently supplied positive exact
quantities and define `E0=K0/ell0` and `E1=K1/ell1`. The exact relative
coordinates are `R_ell=ell1/ell0`, `R_K=K1/K0`, and
`E0/E1=R_ell/R_K`, so the affine kinetic logarithm is
`L=log(R_ell/R_K)`. Unequal conversion factors remain load-bearing when the
lengths are held fixed.

With `b=W_s/3+4*W_f/3`, C-VAC-003 composes exactly as
`Z(E1)=Z_ref+b*L/(8*pi^2)`. C-RGE-003's consistently paired one-loop branch
has `E1=E0*exp(-X)`, `X=8*pi^2/(b0*g^2)`,
`ell0=K0/E0`, and `ell1=K1/E1`. Therefore
`R_ell=R_K*exp(X)` and `L=X`: the two conversion factors cancel even when
they are unequal because each belongs to the length it defines. This earns
`Z(E1)=Z_ref+b/(b0*g^2)`, not the source's zero-boundary expression.

Only after separately imposing `Z_ref=0`, and only for positive `b`, `b0`, and
`g^2`, does the positive zero-branch inverse coordinate exist as
`g_kin^2=b0*g^2/b`. It is a conditional inverse kinetic coordinate, not a
selected physical gauge coupling. The scale maps, one-loop inputs, matter and
group weights, field convention, matching boundary, and physical labels all
remain premises.

A common positive rescaling of both lengths preserves the ratio, logarithm,
and kinetic coefficient but shifts both absolute energies, so it proves only
relative-scale invariance. Changing a conversion at fixed lengths changes the
answer; changing a conversion together with its paired inverse-energy length
at fixed energy does not. Changing `Z_ref` changes the total without changing
the logarithm or slope. These distinctions are the load-bearing mutation
tests for the canonical implementation.

## Attempts and Continuation

Attempt 0001 freezes v0.138.0, framework commit `ba1cbaf`, the GK3D3 hash and
history, exposed synopsis, provisional C-VAC-004, six candidates, selection
criteria, oracle hierarchy, compatibility policy, and debt before the source
body opens. Memory recall finds the accepted two-length, affine kinetic, and
rank-underdetermination ceilings but no governed GK3D3 result. Every later
failed implementation, representation, scale map, boundary, candidate, or
verifier route remains append-only with a materially different continuation.

Attempt 0002 runs the immutable source natively in 0.41 seconds and records all
fourteen executed checks, fourteen lexical and literal sites, one helper
assertion, and no NumPy surface. It retains the exact conditional ratio,
logarithm, zero-branch, and rescaling algebra while rejecting the source's
physical scale derivation, erased affine boundary, uniqueness argument,
parameter-free headline, and sampled perturbativity conclusion. The next route
generalizes the conversions and composes the accepted claims directly.

Attempt 0003 freezes the corrected generic scale map, affine composition,
consistent one-loop conversion cancellation, explicit zero branch, covariance
tests, and non-uniqueness counterfamilies. Registry and implementation search
finds no prior claim or API composing C-RGE-003 with C-VAC-003, so C-VAC-004
remains provisionally distinct pending primary, independent, and consumer
review.

## Debt Ledger

The P187 ledger tracks source reachability, scale labels, inverse-length
conversions, transmutation inputs, affine boundary, effective-coupling domain,
physical identification, compatibility, dependencies, consumers, and
governed state.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| GK3D3 formulas, predicates, assertion, and headline dataflow are unopened | Pin and audit every declared object and conclusion edge | discharged by source reproduction, check adjudication, and attempt 0002 |
| The two source lengths may be relabeled as cutoff and Compton scales | Type every physical identification as a separately supplied map | open |
| Equal `hbar*c` conversions may hide a soliton or threshold coefficient | Derive the arbitrary-conversion formula and mutate each factor | open |
| The transmutation relation may be presented as prediction of its supplied coupling | Preserve the beta coefficient, coupling, reference scale, conversion data, and formal-domain ceiling | open |
| The affine `Z_ref` may be erased by inheritance from GK3D2 | Compose the general family first and test unequal-boundary counterexamples | open |
| A conditional inverse kinetic coefficient may be called a physical coupling | State positivity, convention, matter, group, matching, and identification premises | open |
| Legacy NumPy access may masquerade as science | Repair mutable code or use immutable alias-only replay without candidate rejection | discharged: GK3D3 has no NumPy surface |
| Dependencies, future consumers, and governed records may disagree | Replay the graph and synchronize disposition, queue, claims, release, docs, memory, and debt | open |

## Review and Promotion Plan

C-VAC-004 receives a claim-level review only if exact nonduplication and
positive composition gates pass; otherwise the reserved identifier is not
promoted. The four status axes remain separate. GK3D3 receives an individual
decision for every scale map, cancellation, transmutation equation, affine
boundary, total normalization, effective coupling, physical label, and
interpretation. Mixed surviving and rejected content yields a qualified
disposition with every remainder explicit. Evidence paths materialize before
registration. Targeted exact routes precede one integrated workflow boundary;
record-only closure uses narrow generation and repository checks.

## Done Gate

P187 closes only when the scale-matched affine kinetic object is importable and
mutation-sensitive, every scale and boundary premise is explicit, candidates
and source predicates are adjudicated, downstream consumers replay, accepted
state is synchronized, and the debt ledger is empty. Any failed route queues
the next materially different attempt.

## Cross-References

See C-RGE-001, C-RGE-003, C-IDN-002, C-DIM-007, C-DIM-009, C-GAU-001,
C-MAX-001, C-VAC-002, C-VAC-003, P073, P078, P176, P185, P186, AS1, AS3,
AS5, AS7, CF4, GK1, GK3D1-6, QCD3, `scale_transmutation.py`, and
`vacuum_polarization.py`.
