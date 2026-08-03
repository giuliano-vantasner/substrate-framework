---
description: Derive rational-map sphere integrals and audit E1 map evaluation and minimality claims
author: vantasner
created: '2026-08-07T12:00:00Z'
updated: '2026-08-07T12:00:00Z'
tags:
- substrate-framework
- campaign-proposal
- rational-map
- migration-E1
category: proposals
confidence: exploratory
status: active
---
# P104 E1 Rational-Map Angular Audit

## Question and Positive Deliverable

P104 must deliver an importable, mutation-sensitive mathematical account of
the rational-map conformal Jacobian on the Riemann sphere, its degree-area
identity, the angular functional and lower bound, and the exact axial family
`R(z)=z^B`. It must also implement a chart-stable refined numerical evaluator
and independently evaluate any nonaxial map that survives source audit.

The campaign is not complete merely because a grid returns the three exposed
decimals or the source prints six passes. It must distinguish exact identities
from quadrature evidence, handle both stereographic poles, establish map degree
and coprimality, mutate load-bearing coefficients and charts, and separate the
value of one supplied map from a proof that it is the global degree-fixed
minimum. It must close E1 without importing a physical Skyrme action,
multi-Skyrmion radial solution, baryon state, reaction, yield, or material.

## Base Release and Provenance

The accepted base is `v0.87.0` at parent commit
`37be46c04133b49212f006ec985a748740faede5`; the latest scientific transaction
is P103 at `bcf5bfddfba2ec95d7c2bd07a6c6eea687d131a6`. Source evidence is pinned
to `substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`; unrelated dirty Phase
47/48 work and the explicit NumPy compatibility overlay remain outside
scientific authority.

E1 is
`/home/dan/substrate/merged-framework/bridges/phase-29/bridge_E1_rational_map_integrals.py`,
11,655 bytes, SHA-256
`1afa9ba8ade88912e7361bbbd6f59a9fce5cc114c75ddf604a6439bc066ae2d1`,
and git blob `ca226759fef9ea3276e8e7069867ef881910c6e1`. It is clean relative to the
pinned commit. The generated queue marks it pending, records six literal
checks, and lists E2, E4, NY2, PG3, and S2 as candidate dependencies. E2, E4,
and S2 are pending; NY2 is duplicate evidence; PG3 is qualified through
C-MOD-001, C-MOD-002, and C-SCL-001. None may enter as authority for E1.

No source body or terminal output has been inspected or executed under P104.
The generated queue and parent effort already expose the angular functional,
the identity, axial degree-two and cubic degree-four map descriptions, the
advertised values `1`, `5.79`, and `20.63`, the convergence headline, and the
six-check count. P104 therefore claims no comparator blinding. It freezes
structural alternatives and error gates before opening the file.

Direct accepted sources read before freeze are release `v0.87.0`, C-DIM-002,
C-SK-001, C-TOP-002, C-MOD-001, and C-MOD-002, plus the canonical conditional
Skyrme relation and radial-model implementation. Durable memory was searched
and re-sourced at those authority surfaces. Repository-wide collision search
found no accepted rational-map angular claim and no reserved `C-RMAP-001` or
`C-RMAP-002` identifier.

## Invariants, Conventions, and Allowed Imports

Use the unit Riemann sphere with stereographic coordinate
`z=tan(theta/2)*exp(i*phi)` and area form
`dOmega=4*r*dr*dphi/(1+r^2)^2=dphi*d(cos(theta))` with the corresponding
orientation declared explicitly. A rational map is `R(z)=p(z)/q(z)` for
coprime complex polynomials, with algebraic degree `B=max(deg p,deg q)` after
cancellation and with its value at infinity handled in the reciprocal chart.

Define the nonnegative conformal Jacobian
`J_R=((1+|z|^2)/(1+|R|^2)*|dR/dz|)^2`. For an orientation-preserving
holomorphic degree-B map, the pullback-area theorem must give
`integral J_R dOmega=4*pi*B`. The angular functional is
`I[R]=(1/(4*pi))*integral J_R^2 dOmega`; Cauchy-Schwarz therefore gives
`I>=B^2`. Domain and target sphere rotations may change coordinates but not
the degree or integral. None of these mathematical labels identifies a
physical baryon or a minimizer of a declared energy without additional data.

For the axial family `R=z^B`, P104 preregisters the exact radial reduction
`I_B=2*B^4*integral_0^infinity
r^(4*B-3)*(1+r^2)^2/(1+r^(2*B))^4 dr` and the candidate closed form
`I_B=(B^3/3)*(1+Gamma(2-1/B)*Gamma(2+1/B))`, with the continuous equivalent
reflection-form simplification audited at `B=1`. The identity result and
degree-two specialization are exact controls rather than numerical targets.

Allowed external mathematics is limited to standard stereographic sphere
geometry, holomorphic rational-map degree and pullback area, Cauchy-Schwarz,
beta/gamma identities, polynomial coprimality, and Riemann-Hurwitz. SymPy may
verify exact algebra. NumPy Gauss-Legendre cubature and SciPy or mpmath adaptive
integration may supply only resolution-bounded evidence. Accepted framework
claims enter only as interpretation and nonduplication ceilings.

## Candidate Preregistration

The candidate set is frozen before E1's body or output is opened.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal source reproduction | Pinned source environment | Source grids and literals | Tally proves only implemented predicates | Hash, AST, process, output, and predicate ledger |
| B | Exact general degree theorem | Coprime holomorphic rational map on the unit sphere | Polynomial coefficients and degree | Area identity, positivity, and `I>=B^2` hold independently of E1 values | Pullback derivation, exact controls, Cauchy equality conditions, measure/orientation mutations |
| C | Exact axial family | `R=z^B`, integer `B>=1` | B | Beta/gamma reduction fixes the whole family | Symbolic substitution, identity and B=2 cases, endpoint limits, exponent/factor mutations |
| D | Canonical sphere cubature | Regular chart transitions and finite declared map | Gauss-Legendre orders | Degree and I converge without sampling either pole | At least four tensor orders, chart overlap, exact axial comparators, relative error |
| E | Independent adaptive route | Same declared map, separately coded coordinates | Precision and tolerances | Independent values converge to the same integrals | High-precision/adaptive status, tolerance refinement, method agreement |
| F | Degree-four supplied-map audit | Coprime declared numerator/denominator | Complex map coefficient | Degree, symmetry, pole regularity, and one numeric I can survive without minimality | GCD/resultant, coefficient and rotation mutations, chart and method refinements |
| G | Degree-fixed minimization | Explicit admissible family and objective | Family coefficients | A supplied value proves minimality only after an actual variational comparison | Stationarity/Hessian or preregistered family search and competing maps |
| H | Consumer and interpretation audit | Accepted dependencies only | None | No radial solution, physical state, or nuclear yield follows from I alone | Registry, source, consumer, and parameter ledger |

## Selection Criteria and Blinding

Selection is ordered by accepted dependency closure and nonduplication; exact
sphere normalization, degree, positivity, lower bound, axial formula, limits,
and mutation sensitivity; chart-stable independent numerical convergence;
honest separation of evaluation and minimization; assumption and parameter
economy; canonical extraction; and complete consumer closure. The exposed
decimals and source tally cannot select a candidate or set a tolerance.

No numeric comparator blinding remains. Before source inspection, P104 freezes
the exact general and axial routes, compact sphere measure, reciprocal-chart
checks, coprimality and degree tests, four-level quadrature refinements,
independent method, coefficient and chart mutations, global-minimality ceiling,
and no-yield interpretation boundary.

## Proposed Claim Delta

P104 reserves `C-RMAP-001` for the exact conditional rational-map theorem and
axial-family formula. It reserves `C-RMAP-002` for resolution-bounded evidence
about a specifically declared nonaxial map only if two independent refined
methods, exact degree/regularity checks, and mutation gates survive. The second
claim will not call the map globally minimal unless a separately preregistered
variational oracle establishes that statement.

Both proposed claims are dependency-root mathematical objects. C-MOD-001 is a
compatibility surface for the B=1 radial specialization, not a derivation
input. C-MOD-002, C-SK-001, C-TOP-002, and C-DIM-002 supply ceilings only. No
accepted claim is challenged or superseded. If the numeric candidate fails,
its attempt is preserved while the exact positive object and terminal E1 audit
continue.

## Implementation and Oracle Plan

If Candidates B through F survive, a pure `rational_maps.py` module will expose
polynomial/coprimality validation, stereographic conformal Jacobians, exact
axial integrals, domain/target rotation helpers as needed, and a sphere
cubature evidence object. Every coefficient, chart convention, quadrature
order, tolerance, and precision is explicit; import runs no integration or
printing.

SymPy is the strongest oracle for the identity map, algebraic degree, axial
radial reduction, beta/gamma formula, `B=1` limit, `B=2` specialization,
pullback-area controls, and coefficient mutations. The general area identity
and Cauchy bound will be derived rather than tested by copied literals.
Riemann-Hurwitz or an explicit critical-point count will separate equality
conditions and branch points from a numeric closeness claim.

The canonical numerical route will use tensor Gauss-Legendre integration in
`u=cos(theta)` and `phi`, never sampling endpoints. Orders will include at
least `(16,32)`, `(24,48)`, `(32,64)`, and `(48,96)` or a stricter sequence
chosen before viewing results. It will record binary64 precision, both sphere
intervals, nodes, chart switching, degree-area error, I values, successive
relative differences, and finite-status gates. Identity and axial maps must
agree with exact values to a scale-relative threshold established from
refinement, initially `2e-10` for the final exact controls.

The independent route will not import the canonical evaluator. It will use
mpmath high precision or nested SciPy adaptive quadrature with a separately
implemented stereographic/reciprocal-chart formula at tolerances no weaker
than `1e-8`, `1e-10`, and `1e-12`, report convergence and status, and agree
with the final canonical nonaxial value within `2e-8` relative unless a
preserved convergence study justifies a stricter gate. Any singular-looking
coordinate point must be resolved analytically or by a tested reciprocal
chart, not masked or clipped.

Load-bearing mutations change the sphere area factor, Jacobian square,
derivative power, map degree, numerator/denominator coprimality, degree-four
coefficient, target or domain rotation normalization, reciprocal chart, and
pole handling; each relevant verdict must fail. Counterexamples include a
common polynomial factor that changes apparent but not reduced degree, a
nonholomorphic map outside the theorem, a perturbed same-degree map with a
different I, and multiple maps whose evaluation does not establish global
minimality.

Compatibility preflight is frozen now: canonical sampled integration will use
the declared Gauss-Legendre weights or `trapezoid_integral`, never a direct
NumPy trapezoidal alias. Mutable current-environment scripts must use
`np.trapezoid`. If immutable E1 aborts only because it calls removed
`np.trapz`, P104 will preserve the native hash and diagnostic and run an
alias-only compatibility replay before scientific adjudication; that abort is
not candidate rejection.

Focused replay will cover the new module and relevant radial, Skyrme relation,
topological, dimension, and numerics tests. Every E1 predicate and affected
consumer receives an individual verdict. One full workflow runs only at a
meaningful promotion or terminal-adjudication boundary.

## Attempts and Continuation

Every source, chart, pole, degree, algebra, representation, quadrature,
precision, symmetry, minimization, dependency, consumer, or verifier failure
is append-only with command, environment, output, diagnosis, and next route.
A failed cubic-map number or minimality claim does not complete P104; the
exact theorem, repaired numerical route, competing maps, and terminal source
audit continue.

## Debt Ledger

P104 tracks source hash and prior exposure; sphere radius, measure,
orientation, stereographic and reciprocal charts, complex derivative, map
coprimality and degree, pole and infinity limits, Jacobian normalization,
area identity, angular functional, lower bound, beta/gamma formula, numeric
precision, orders, tolerances, error norms, method independence, map
coefficients and symmetries, global-minimality evidence, every source check,
dependencies, consumers, disposition, generated state, and parent
continuation. Every item must be derived, declared, rejected, or excluded.

## Review and Promotion Plan

Each surviving proposed claim receives a separate claim-level review. P104
will add primary and independent verifiers, source predicate adjudication,
impact analysis, and affected-consumer replay. Acceptance requires canonical
package extraction, sensitive tests, governance and release updates,
generated documentation, accepted-memory synchronization, a terminal E1
disposition, and one full workflow. A final record-only update reruns only
record-sensitive repository, generation, memory, and diff checks.

## Done Gate

P104 closes only when the exact rational-map object exists, every promoted
numeric value has independent refined evidence, evaluation and minimization
are separated, chart and pole semantics are explicit, every E1 predicate and
consumer is adjudicated, claim and release surfaces agree, campaign debt is
empty, and the parent migration advances. Six passing checks or three exposed
decimals are not completion.

## Cross-References

This campaign cross-references E1, E2, E4, NY2, PG3, S2, C-DIM-002,
C-SK-001, C-TOP-002, C-MOD-001, C-MOD-002, P058, P062, P084, P085, and the
canonical radial-model, Skyrme-relation, topology, and numerics modules.
