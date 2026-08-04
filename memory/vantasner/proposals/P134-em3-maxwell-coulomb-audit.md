---
description: Audit EM3's imported Maxwell action, Coulomb tail, and two-charge force
author: vantasner
created: '2026-08-09T01:30:00Z'
updated: '2026-08-09T01:30:00Z'
tags: [substrate-framework, campaign-proposal, maxwell, coulomb, migration-EM3]
category: proposals
confidence: working
status: active
---
# P134 EM3 Maxwell and Coulomb Audit

## Question and Positive Deliverable

P134 must reproduce and adjudicate EM3's claim that an imported Maxwell kinetic
term extends the accepted conditional local-U1 connection to a sourced field
equation, static point-charge tail, and two-charge force. The positive
deliverable is a reusable, convention-closed conditional action theorem with
its general-dimensional static consequence, or an exact terminal mapping to
accepted Green-kernel and force algebra if no distinct claim survives.

## Base Release and Provenance

The accepted base is v0.101.0 at parent checkpoint `ce9fca6`; the latest
scientific adjudication is P133 at `1babed5`. EM3 is pinned to
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`, path
`merged-framework/bridges/phase-3/bridge_EM3_maxwell_coulomb_tail.py`, SHA-256
`1c674bae211322b24a4504ff5aafc04424eb6a4bfe7813f63e5ec4337f783fc9`.

The generated queue exposes eleven literal checks, one assertion, symbolic and
numeric oracle hints, the named Maxwell/Coulomb/inverse-square targets, and
dependencies EM2, G1, G2, and G3. EM2 is qualified through C-GAU-001; G1, G2,
and G3 remain pending and supply no authority. EM3's body and result have not
been opened or executed during this freeze.

## Invariants, Conventions, and Allowed Imports

C-GAU-001 fixes the conditional connection, field-strength sign, and local-U1
transformation, while explicitly supplying no kinetic coefficient, gauge-field
equation, photon, force, physical charge, or electromagnetic sector. The new
independent model premise is flat signature `(+,-,...,-)` and
`L=-kappa*F_mu_nu*F^mu_nu/4-j^mu*A_mu`, with positive `kappa`, a smooth supplied
conserved current, and compactly supported variations. Its candidate equation
is `kappa*partial_mu F^mu_nu=j^nu`.

For static `A_0=phi`, `A_i=0`, and `j^0=rho`, the frozen convention gives
`-kappa*Laplacian(phi)=rho` and `E=-gradient(phi)`. Point-source normalization,
dimension, regularity away from the source, boundary data, and the force
dictionary are independent premises. For `d>2`, decaying boundary data give
`phi=Q/[kappa*(d-2)*S_(d-1)*r^(d-2)]` and
`E_r=Q/[kappa*S_(d-1)*r^(d-1)]`, with
`S_(d-1)=2*pi^(d/2)/Gamma(d/2)`. The `d=2` solution is logarithmic with a
reference scale; the `d=1` solution is linear up to homogeneous data.

C-KRN-001 already owns the exact general Riesz kernel and its conditional
`d=3,s=1,A=1` endpoint `1/(4*pi*r)` without selecting dimension, source,
boundary, charge, or force. C-FLX-001 separately owns conditional `F=qE`
algebra. C-U1-001 supplies current conservation only under its declared
complex-field premises and does not identify that current as physical electric
charge. These ceilings and the nonauthority of pending G1/G2/G3 are invariant.

## Candidate Preregistration

The candidate set separates literal replay, action variation, static Green
geometry, force construction, accepted composition, countermodels, and
governance closure.

| Candidate | Construction | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal EM3 replay | Source conventions | Source values | Narrow equations may repeat while dimensions and ontology remain imported | Eleven-predicate, AST, and data-flow audit |
| B | Maxwell action variation | Declared action/current/boundary | `kappa,j,A` | Field equation and continuity close exactly | Euler derivative, gauge variation, and sign mutations |
| C | General static point source | Supplied dimension/source/boundary | `d,Q,kappa` | Power, logarithmic, and linear cases separate | Radial flux, Laplacian, and dimension probes |
| D | Two-charge force | Supplied test charge and force dictionary | `q,Q` | Force sign and radial power follow conditionally | Energy gradient and charge-sign mutations |
| E | Accepted composition | C-KRN-001/C-FLX-001 | None new | Three-dimensional endpoint is duplicate | Claim/API nonduplication audit |
| F | Countermodels | Frozen conventions | Alternate `d`, signs, homogeneous data | Physical and uniqueness overreads fail | `d=4`, `d=2`, source-sign, and boundary countermodels |
| G | Governance closure | Accepted authority order | None | Narrow terminal disposition | Dependencies, consumers, impact, queue, and generated-state replay |

## Selection Criteria and Blinding

Selection is ordered by accepted dependency closure, complete action and source
premises, fixed metric/index/sign conventions, exact variation and continuity,
correct sphere and delta normalization, all dimension cases, dimensional
consistency, independent Green-function agreement, mutation sensitivity, known
limits, parameter economy, reusable API value, physical-scope honesty, and
nonduplication. The queue exposes the favored named endpoint but no empirical
comparator; matching `1/(4*pi*r)` cannot select its dimension or ontology.

## Proposed Claim Delta

Provisional C-MAX-001 may state the exact conditional Maxwell Euler-Lagrange
equation, necessary conserved-current condition, and source-normalized static
point-charge family with its separately conditional test-charge force. It must
depend on C-GAU-001 and reuse rather than duplicate C-KRN-001. It may not assert
that local covariance derives the kinetic coefficient, that the accepted
complex scalar supplies electric charge, that three dimensions are uniquely
selected by decay, or that the framework contains a photon, physical
electromagnetism, gravity coupling, observed force, or substrate mechanism.

## Implementation and Oracle Plan

After the freeze commit, the primary route will hash, parse, and execute EM3,
map all eleven predicates, inventory imports and constants, and rebuild its
variation, antisymmetry, static equation, radial tail, dimension claim,
two-charge energy, force, units, signs, and limits. SymPy exact tensor and
radial algebra is the primary oracle; numerical regression cannot upgrade an
exact claim.

A fresh route will vary the action without calling a future canonical helper,
derive continuity by swapping dummy indices, normalize the point source with a
small-sphere flux, and recover the potential from the field and from
C-KRN-001 independently. Kinetic-coefficient, source-sign, field-strength-sign,
sphere-area, dimension, charge-sign, and boundary mutations must break their
load-bearing verdicts. Zero source, zero test charge, large radius, near source,
like/opposite charge, `d=4`, `d=2`, and `d=1` probes remain explicit.

No numerical quadrature is needed for the exact candidate. If immutable source
reproduction uses a legacy NumPy integration name, it receives an alias-only
replay and is classified as a version event rather than scientific failure.
Every mutable script uses `np.trapezoid` or the canonical
`trapezoid_integral`; exact work uses neither.

## Attempts and Continuation

Attempt 0001 freezes the contract before source-body inspection. After that
commit, attempt 0002 will preserve the exact native reproduction or failure and
continue through Candidates B through G. A source sign or normalization failure
narrows the source surface; it does not cancel the positive action and
general-dimensional derivation. A duplicate endpoint is mapped rather than
re-promoted.

## Debt Ledger

The ledger tracks source, action, current, Green-function, dimension, force,
physical-scope, dependency, consumer, and novelty debt until each item has
evidence-level closure.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| EM3 executable surface unaudited | Hash, execute, AST audit, and map all eleven predicates | open |
| Maxwell action and signs unverified | Derive the Euler equation and gauge boundary term in the frozen convention | open |
| Current compatibility unverified | Derive the continuity condition from antisymmetry and audit the supplied current | open |
| Static source normalization unclosed | Derive Poisson sign, sphere flux, homogeneous data, and point-source coefficient | open |
| Dimension and tail claim unclosed | Derive `d>2`, `d=2`, and `d=1` cases and test uniqueness language | open |
| Two-charge force premise untyped | Separate field equation, source charge, test charge, energy, and force dictionary | open |
| Physical language ungoverned | Separate conditional U1 dynamics from photon, electromagnetism, gravity, material, and observation | open |
| Dependencies, consumers, and novelty unknown | Audit EM2/G1/G2/G3, reverse consumers, accepted APIs, and generated state | open |

## Review and Promotion Plan

C-MAX-001 receives an individual review only if its action-level content is
distinct from C-GAU-001 and C-KRN-001 and every coefficient and premise closes.
Source adjudication separately decides EM3's disposition. Accepted reusable
logic moves to a pure package module with focused tests; proposal scripts call
it. Impact, dependency, consumer, generated-state, memory, queue, and one
integrated promotion replay close any promotion.

## Done Gate

P134 closes only when the positive conditional action/static-force object or
its exact accepted composition exists, every source predicate is adjudicated,
the strongest exact and independent oracles are mutation-sensitive, dimensions,
signs, sources, boundaries, and limits close, consumers replay, generated state
agrees, and the campaign debt ledger is empty. Rejecting a source overclaim
alone is not completion.

## Cross-References

See P014, P027, P030, P064, P133, EM2, EM3, G1, G2, G3, C-U1-001,
C-GAU-001, C-FLX-001, C-KRN-001, v0.101.0, and the parent
framework-migration effort.
