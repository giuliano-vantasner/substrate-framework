---
description: Audit GK3D2 and derive a scalar-loop and kinetic-boundary normalization ledger
author: vantasner
created: '2026-08-11T12:13:00Z'
updated: '2026-08-11T13:05:00Z'
tags:
- substrate-framework
- campaign-proposal
- migration-GK3D2
- vacuum-polarization
- kinetic-normalization
category: proposals
confidence: established
status: archived
---
# P186 GK3D2 Induced Kinetic Normalization Audit

## Question and Positive Deliverable

P186 must determine whether GK3D2 derives both the complex-scalar
four-dimensional one-loop coefficient and a total gauge kinetic
normalization. The positive deliverable is an importable conditional scalar
bubble-plus-seagull residue and logarithmic-slope theorem together with an
exact affine kinetic-boundary ledger that preserves every bare, counterterm,
reference-scale, field-normalization, and matching coordinate. It must say
exactly what an explicitly imposed zero boundary would imply without treating
an earlier no-matter/no-kinetic premise as that boundary. A demonstration that
the source erases an integration constant is attempt evidence, not completion.

## Base Release and Provenance

The accepted base is v0.137.0 at clean framework commit
`e7b2888c8ae526ee92b5da878f92b0ebe9aa660c`, with 177 accepted claims. Its
manifest SHA-256 is
`874abae995ffc0ad883255bee7f754383b0aa183cf88aa44fa77ce9712b9a55e`.
The governed predecessor baseline is
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`. GK3D2 is pending at
`merged-framework/bridges/phase-41/bridge_GK3D2_induced_kinetic_normalization.py`,
SHA-256
`856096aba38812dc17fb07ce5cf7c0fa13eb2623665ccf871810734ac3ca0886`,
size 22,026 bytes, blob `7eb49a516a9cd5ea24bcfadfd0dde2bf5e0462b0`, and sole
history commit `7222eed`. The target path is clean at the governed source
commit; later source-worktree artifacts have no authority.

The generated queue already exposes the claimed scalar-to-Dirac factor-four
logarithmic slope, rational matter weights, the claim that rung25 removes the
additive constant, seventeen static check sites with two dynamic calls, one
assertion, and a positive normalization synopsis. P186 therefore claims no
fresh source-result blinding. Exact formulas, signs, conventions, imports,
predicate dataflow, and the executable conclusion remain unopened until this
contract passes validation.

## Invariants, Conventions, and Allowed Imports

C-GAU-001 leaves every local gauge kinetic coefficient unconstrained.
C-MAX-001 supplies a kinetic coefficient and proves that deleting the kinetic
term gives only the current constraint; it does not force the connection to be
pure gauge. C-VAC-001 is a separately declared massive complex-scalar D=2
bubble-plus-seagull theorem and supplies neither a D=4 continuation nor a
counterterm choice. C-VAC-002 supplies a conditional charged-Dirac D=4 residue
and logarithmic slope but explicitly leaves the finite counterterm, bare term,
matching condition, and total normalization free. C-DIM-009 supplies only
dimension and convention bookkeeping. C-RGE-001 requires a reference coupling
in addition to a differential beta function.

P186 may conditionally declare one or more free complex charged scalars in
four dimensions, their determinant, bubble and seagull, loop order,
gauge-preserving dimensional regulator, tensor and effective-action
conventions, subtraction scheme, and matching condition. It may import exact
Feynman parameterization, dimensionally regulated Gaussian integrals, Gamma
identities, Laurent series, and affine first-order flow integration. The loop
piece, local counterterm, bare coefficient, renormalized reference value, and
total coefficient remain separately typed.

Hash-pinned GK3D2 and its source dependencies and consumers are noncanonical
evidence only. No accepted premise identifies a no-matter theory with a
matching surface after charged matter is introduced, supplies a physical
charged scalar or Dirac spectrum, fixes a representation, multiplicity,
charge, scale ratio, bare coefficient, finite counterterm, preferred
dimension, physical gauge group, observation, or substrate mechanism.
Mutable quadrature uses `np.trapezoid` or `trapezoid_integral`; immutable
legacy-name aborts are version-only compatibility evidence and never
scientific candidate failures.

## Candidate Preregistration

Six candidates separate literal reproduction, scalar-loop derivation,
boundary identifiability, matter-weight composition, matching alternatives,
and governed closure.

| Candidate | Object | Structural gate |
| --- | --- | --- |
| A | Hash-pinned source reproduction and predicate audit | Every coefficient, dependency, boundary statement, check, assertion, and headline edge is typed |
| B | Conditional D4 complex-scalar loop | Bubble and seagull close the Ward identity and exact residue and slopes in one declared convention |
| C | Affine inverse-kinetic flow | The independent reference value survives unless a matching boundary is separately imposed |
| D | Scalar and Dirac matter weights | Statistics, multiplicity, charge, trace, generator, and coupling conventions compose without selecting matter or group |
| E | Competing boundary models | Free bare-plus-counterterm, explicit zero matching, and measured matching remain distinct before any total coefficient is selected |
| F | Governed closure | Claim, source, future consumers, release, queue, docs, memory, and debt agree |

## Selection Criteria and Blinding

Selection is ordered by declared action and statistics, bubble-seagull Ward
closure, exact scalar normalization, separation of loop slope from affine
boundary, correct scope of the earlier no-matter result, tensor and field
normalization consistency, explicit matter weights, zero-charge and heavy-mass
limits, matching and scale behavior, independent rederivation, mutation
sensitivity, assumption economy, and global closure. Numerical agreement
cannot select a coefficient or boundary. The queue synopsis already reveals
the broad source result, so the meaningful gate is frozen structural criteria
before the implementation body and detailed output open.

## Proposed Claim Delta

P186 reserves C-VAC-003 for a distinct conditional complex-scalar D4
vacuum-polarization residue and kinetic-boundary theorem, including every
action, regulator, tensor, subtraction, flow, matching, and scope condition
actually earned. Repository-wide registry, campaign, queue, and memory search
finds no identifier collision; rejected provisional identifiers remain
reserved. The proposal has no `supersedes` edge. Likely consumers are GK3D2,
GK3D3 through GK3D6, the canonical vacuum-polarization and running surfaces,
tests, registry, release, generated records, migration disposition and queue,
and later gauge-sector claims. Each may inherit only the exact conditional
coefficient and boundary ledger.

## Implementation and Oracle Plan

The source audit first pins AST and NumPy compatibility surfaces, native
execution, every imported dependency, scalar and Dirac coefficient, beta and
kinetic convention, scale, boundary premise, predicate, assertion, and
conclusion edge. Reusable equations belong in pure package APIs; imports run no
simulation or tally.

The primary symbolic route derives the regulated scalar bubble and seagull or
an equivalent gauge-preserving determinant expansion, contracts the Ward
identity, extracts the D=4 Laurent residue and declared subtraction-scale
slope, and translates it into the chosen inverse-kinetic convention. A
separate exact flow route integrates the differential coefficient while
retaining its reference value. It then evaluates, but does not infer, an
explicitly declared zero-matching condition. An independent implementation
must not import the new canonical claim module and must reconstruct the
load-bearing parameter integral, coefficient, affine family, and boundary
counterexamples.

Mutations change the scalar bubble/seagull balance, statistics factor,
charge-square or multiplicity weight, tensor sign, scale orientation, finite
counterterm, bare coefficient, and matching surface. Counterexamples compare
two theories with the same zero no-matter action but unequal permitted finite
matching after charged matter is introduced, and two total coefficients with
the same derivative. Zero charge, heavy mass at fixed subtraction, equal
scales, reference-scale changes, and explicitly imposed zero matching remain
separate limits. SymPy is the strongest practical oracle for the exact
identities; high-precision quadrature, if needed for a nonclosed integral, is
only an independently refined numeric cross-check.

Compatibility preflight inspects executable direct, imported, and dynamic
legacy trapezoidal access. Mutable code is repaired to `np.trapezoid` or the
canonical helper before scientific adjudication. Immutable source receives a
recorded alias-only replay when required, and that environment event never
rejects a candidate.

## Source Audit Result

The hash-pinned source passes all seventeen runtime checks without a NumPy
compatibility event. Its affine ODE algebra is exact once a reference value is
supplied, and its scalar-to-Dirac factor-four slope and rational matter weights
remain positive candidates pending a complete scalar loop derivation.

The load-bearing boundary inference fails at its cited source. Rung25 defines
no `Z`, cutoff, bare coefficient, counterterm, charged-matter threshold, or
matching surface. Its L3b predicate first sets `A=d chi` and then verifies
`d^2 chi=0`; this is a pure-gauge witness, not an Euler-Lagrange proof that
every connection is pure gauge. The accepted C-MAX-001 theorem is stronger and
opposite to GK3D2's use: deleting the kinetic term yields only the current
constraint and does not force `A` to be pure gauge. Introducing charged matter
and a new local loop operator also changes the theory and operator basis, so a
no-matter absence statement cannot silently become `Z(Lambda)=0` after the
matter is integrated out.

The source's scalar helper differentiates a reduced parameter integrand but
contains no declared scalar determinant, bubble, seagull, regulator dimension,
subtraction scale, Laurent pole, or counterterm. The finite slope may survive,
but P186 must derive it in a complete convention. Checks 3a, 4a, 4b, 5a, 5b,
and 6b respectively rely on a keyword, solve an imposed zero equation, repeat
that substitution, sample rather than prove an equivalence, import the scale
ordering while dropping the free boundary, and subtract a formula from itself.
They do not validate the advertised total normalization.

## Corrected Formula Freeze

P186 fixes the source tensor convention
`Pi_mn=(q^2*g_mn-q_m*q_n)*Pi2(q^2)` and spacelike `Q=-q^2>0`. For one or
more separately declared free complex charged scalars, determinant
`Tr log(-D^2+M^2)`, common gauge-preserving dimensional regulator, and both
the oriented bubble and seagull, the Ward contraction uses
`q.(2p+q)=D_(p+q)-D_p`. After the common momentum shift, the bubble contributes
`+2*q_nu*integral(1/D_p)` and the seagull contributes its negative. This earns
transversality from the loop rather than from a projector ansatz.

With `Delta=M2+x*(1-x)*Q`, integration dimension `d`, multiplicity `N`, and
charge magnitude `e`, the frozen scalar form factor is
`-N*e^2*Gamma(2-d/2)/(4*pi)^(d/2)` times the integral from zero to one of
`(1-2*x)^2*Delta^(d/2-2)`. At `d=4-2*epsilon`, with scale factor
`mu2^epsilon`, its zero-momentum bare value is
`-N*e^2/(48*pi^2)*Gamma(epsilon)*(4*pi*mu2/M2)^epsilon`. The Laurent residue
is `-N*e^2/(48*pi^2)`. Adding the MS-bar pole counterterm and arbitrary finite
local `c_fin` gives
`N*e^2/(48*pi^2)*log(M2/mu2)+c_fin`. Thus the scalar beta coefficient is one
quarter of the Dirac coefficient in the same convention.

For the connection field `B=e*A`, declare
`-Z_B*F(B)^2/4`; then `Pi2_A=e^2*Z_B`. With separately supplied invariant
complex-scalar and Dirac weights `W_s,W_f`, the matter coefficient is
`b=W_s/3+4*W_f/3` and
`mu*dZ_B/dmu=-b/(8*pi^2)`. The full exact family is
`Z_B(mu)=Z_ref+b*log(mu_ref/mu)/(8*pi^2)`, where `Z_ref` is an independent
renormalized matching coordinate. A change
`mu_ref'=kappa*mu_ref` preserves the same function only with
`Z_ref'=Z_ref-b*log(kappa)/(8*pi^2)`.

Setting `Z_ref=0` is a separately declared compositeness or zero-matching
condition. Only on that branch, with positive `b`, is positivity equivalent to
`mu_ref>mu`. The general branch depends on `Z_ref`; two unequal reference
values have the same one-loop slope. Rung25 supplies neither branch selection
nor a matching coordinate.

Two nonauthoritative primary comparators are pinned. The scalar-QED
renormalization paper arXiv:hep-ph/9806451 declares the action, bubble and
seagull, transverse sum, and beta `e^3/(48*pi^2)`. ArXiv:1611.00446v2 writes
the ordinary scalar bubble and seagull subgraphs in dimensional regularization
and reproduces the same commutative coefficient; its additional
noncommutative sector is not imported.

## Attempts and Continuation

Attempt 0001 freezes v0.137.0, framework commit `e7b2888`, the GK3D2 hash and
history, exposed synopsis, C-VAC-003, six candidates, selection criteria,
oracle hierarchy, compatibility policy, and debt before the source body opens.
Memory recall finds the accepted scalar D2, Dirac D4, Maxwell, dimensional,
and running boundaries but no governed GK3D2 result. Every later failed
implementation, representation, regulator, boundary, candidate, or verifier
route remains append-only with a materially different continuation.

Attempt 0004 extracts pure scalar Ward, general-dimensional master, D4
Laurent/MS-bar, and affine kinetic-boundary APIs into the package. Eighty
focused tests pass across the new scalar surface and the accepted Dirac,
generic beta, and affine-running ledgers. The wrong-seagull, finite-boundary,
scale-ordering, and hidden-float mutations change or reject the relevant
verdict, while a paired reference-coordinate change preserves the same
running function. This discharges implementation debt but not independent
rederivation, source-graph replay, or governed promotion.

Attempts 0005 and 0006 preserve two primary-verifier representation failures:
structural comparison of expanded and factored SymPy expressions, and phrase
comparison across docstring line wrapping. Neither changed a scientific
formula or threshold. Attempt 0007 passes all 31 hash-pinned, exact, and
mutation-sensitive primary checks after simplifying algebraic differences and
normalizing documentation whitespace. Independent rederivation remains open.

Attempt 0008 preserves a self-referential independence predicate that matched
its own forbidden substring after 27 scientific checks had passed. Attempt
0009 replaces that predicate with an AST import-module inventory and passes 28
raw-SymPy checks without importing the canonical scientific claim, Dirac,
generic-beta, or renormalization modules. It independently rebuilds the
vertex weight, pole, finite family, slopes, factor four, affine solution, and
boundary counterexamples. Source-graph and governance closure remain open.

Attempt 0010 refreshes the code graph and records LOW additive implementation
risk, zero affected indexed processes, and the indexer's explicit failure to
materialize the new factory functions as function nodes. The result-dataclass
and transaction routes still expose the expected file consumers; temporary
GitNexus host artifacts were removed. Attempt 0011 passes 20 source-graph and
governance checks across eight hash-pinned nodes. It keeps the GK3D1 prose
cycle harmless, GK3D3 through GK3D6 individually pending, and GK3D5's current-
first lazy quadrature fallback classified as compatibility rather than science.

Attempt 0012 records that the two new decision files used semantically natural
but schema-invalid frontmatter enums. Attempt 0013 repairs only those record
coordinates and validates all 761 memory files. No equation, threshold, claim
scope, or scientific verdict changed.

Attempt 0014 is the single integrated promotion boundary. It validates 178
accepted claims, 38 pending migration units, all 761 memory files, generated
documentation and accepted memory, the physics skill, compilation, and 1,619
repository tests. The gate exits cleanly in 171.65 seconds. P186 is therefore
archived with C-VAC-003 active, GK3D2 qualified, and every debt below closed.

## Debt Ledger

The P186 ledger tracks source reachability, scalar quantum premises,
bubble-seagull closure, D4 residue, running convention, affine boundary,
bare and counterterm freedom, compatibility, dependencies, consumers, and
governed state.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| GK3D2 formulas, predicates, assertion, and headline dataflow are unopened | Pin and audit every declared object and conclusion edge | discharged by source audit and attempt 0002 |
| The scalar coefficient may be copied from a numerator integral without a seagull or regulator | Derive it in a complete gauge-preserving scalar-QED convention | discharged by canonical, primary, and independent bubble-seagull and D4 derivations |
| Dirac and scalar beta conventions may be mixed | Derive both weights in one declared kinetic and scale convention | discharged by exact factor-four, generic-ledger, and independent cross-checks |
| A differential slope may be presented as a total normalization | Integrate the affine family and retain its independent reference value | discharged by canonical and independent affine families and same-slope unequal-boundary mutations |
| The earlier no-matter result may be mislabeled a matching boundary | Compare theories, premises, and operator bases and require a separately declared matching condition | discharged by C-MAX-001 comparison, source adjudication, and conditional zero-matching countermodels |
| Bare and finite counterterm coordinates may be erased | Expose both and show load-bearing mutations with the same loop slope | discharged by finite-counterterm, boundary, and reference-coordinate mutations |
| Group and matter weights may be called physical sectors | Preserve conditional multiplicities, charge squares, traces, and generator/coupling rescaling | discharged by conditional exact-weight APIs, claim scope, and consumer audit |
| Legacy NumPy access may masquerade as science | Repair mutable code or use immutable alias-only replay without candidate rejection | discharged: GK3D2 has no NumPy surface |
| Dependencies, future consumers, and governed records may disagree | Replay the graph and synchronize disposition, queue, claims, release, docs, memory, and debt | discharged by the 20-check graph replay, v0.138.0 records, and integrated gate |

## Review and Promotion Plan

C-VAC-003 receives a raw-artifact claim review with independent derivation and
mutation evidence. The four status axes remain separate. GK3D2 receives an
individual decision for every scalar coefficient, beta weight, running law,
boundary claim, induced normalization, group/matter composition, and physical
interpretation. Mixed surviving and rejected content yields a qualified
disposition with every remainder explicit. Evidence paths materialize before
registration. Targeted scientific routes precede one integrated workflow
boundary; record-only closure uses narrow generation and repository checks.

## Done Gate

P186 closes only when the scalar D4 loop and affine boundary objects are
importable and mutation-sensitive, the earlier no-matter premise is not
silently promoted into a matching condition, every total-normalization freedom
is explicit, candidates and source predicates are adjudicated, downstream
consumers replay, accepted state is synchronized, and the debt ledger is empty.
Any failed route queues the next materially different attempt.

## Cross-References

See C-GAU-001, C-MAX-001, C-VAC-001, C-VAC-002, C-DIM-009, C-RGE-001,
P135, P176, P185, EM3, EM5, GK1, GK3D1, GK3D2-6,
`vacuum_polarization.py`, `dirac_vacuum_polarization.py`, `maxwell.py`, and
`renormalization.py`.
