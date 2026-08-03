---
description: Derive conditional rational-map radial branches and audit E2 profile and binding claims
author: vantasner
created: '2026-08-07T13:00:00Z'
updated: '2026-08-07T15:45:00Z'
tags:
- substrate-framework
- campaign-proposal
- rational-map
- radial-bvp
- migration-E2
category: proposals
confidence: established
status: archived
---
# P105 E2 Rational-Map Radial Profiles

## Question and Positive Deliverable

P105 must deliver an importable exact definition of the declared generalized
rational-map radial functional, its Euler-Lagrange equation, scaling split, and
endpoint exponents. It must then construct resolution-bounded stationary
branches for the accepted degree-one, degree-two, and declared degree-four
angular inputs using two independent asymptotic-boundary numerical methods.

Completion requires actual profile and energy evidence with solver status,
residuals, domain/cutoff/tolerance refinement, tail control, mutations, and
consumer closure. Reproducing E2's six checks or its exposed energy decimals is
not completion. The campaign must distinguish a stationary branch of a
declared one-profile reduction from a global reduced minimizer, a full
three-dimensional solution, a physical baryon or nucleus, binding, reaction,
or yield.

## Base Release and Provenance

The accepted base is release `v0.88.0` at parent checkpoint
`d09de1dc36239c407e9be34413638254952065af`; the scientific transaction is
P104 at `42337ce`. Source evidence remains pinned to
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`. Unrelated dirty Phase
47/48 work and the explicit external NumPy compatibility overlay remain
outside scientific authority.

E2 is
`/home/dan/substrate/merged-framework/bridges/phase-29/bridge_E2_multi_skyrmion_solutions.py`,
12,692 bytes, SHA-256
`fdde30878eaf1f8dff7fce9c2d9d4234d1d6e14566be6d2ee56dd1926481c46f`,
and git blob `6a2ec5e0cca1255605d3644a5e421ac655734835`. It is clean relative to the
pinned commit. The generated queue marks E2 pending, lists B1, E1, E3, PG3,
and S2 as candidate dependencies, and records six literal checks. E1 is now
qualified through C-RMAP-001/002; B1, E3, and S2 remain pending, while PG3 is
qualified through C-MOD-001/002 and C-SCL-001. Only the accepted claims may
enter as authority.

P104 already inspected E2's header and lines through the energy helper during
its consumer audit. Exposed content includes the functional and ODE, source
angular integration defect, hard finite-cutoff Dirichlet boundary data,
solve_bvp settings and initial guess, sampled energy quadrature, advertised
per-degree values, and snippets of the I=B-squared guard. P105 therefore claims
neither source-body nor comparator blinding. It has not executed E2 or inspected
the remaining predicate bodies and terminal output.

Authority and memory recall read release `v0.88.0`, C-RMAP-001, C-RMAP-002,
C-MOD-001, C-MOD-002, C-SCL-001, the canonical rational-map, radial-mode, and
numerics modules, P104's consumer ledger, and the parent effort. Registry,
campaign, source, and memory collision search found no accepted or reserved
`C-RPROF-001` or `C-RPROF-002` identifier.

## Invariants, Conventions, and Allowed Imports

For exact positive `B` and `I`, declare the dimensionless density on `r>0`

`L=r^2 f'^2+2 B sin(f)^2(1+f'^2)+I sin(f)^4/r^2`

and `E=4 pi integral_0^infinity L dr`. Direct variation must give

`(r^2+2 B sin(f)^2)f''+2 r f'+B sin(2f)(f'^2-1)
-I sin(2f)sin(f)^2/r^2=0`.

At `B=I=1` these must reduce exactly to C-MOD-001. Split the density into
`E2=4 pi integral(r^2 f'^2+2 B sin(f)^2)dr` and
`E4=4 pi integral(2 B sin(f)^2 f'^2+I sin(f)^4/r^2)dr`.
Under `f_s(r)=f(exp(s)r)`, the energy is
`exp(-s)E2+exp(s)E4`; a stationary finite-energy branch must satisfy `E2=E4`,
but that identity alone proves neither uniqueness nor global minimality.

For `f=pi-A r^sigma+...` at the regular origin and `B>1`, dominant balance
gives `sigma^2+sigma-2B=0`, hence
`sigma=(sqrt(1+8B)-1)/2`. The `B=1` case has `sigma=1` with a nonlinear leading
coefficient and is checked separately against C-MOD-002. For the massless tail
`f=C r^-p+...`, the indicial equation is `p^2-p-2B=0`, hence
`p=(sqrt(1+8B)+1)/2`. The canonical finite-domain conditions therefore use
`r f'+sigma(pi-f)=0` at the inner cutoff and `r f'+p f=0` at the outer wall,
not exact vacuum values at finite coordinates.

The accepted angular inputs are `(B,I)=(1,1)`,
`(2,pi+8/3)`, and `(4,20.6496264884189)` with the final value retaining
C-RMAP-002's numeric status. C-MOD-001/002 may validate only the B=1
specialization. Standard variational calculus, endpoint asymptotics, ODE
shooting/collocation, SymPy, NumPy/SciPy, and the shared numerics APIs are
allowed. No physical Skyrme action, rational-map minimization, state map,
absolute scale, empirical binding energy, or later source claim is allowed.

## Candidate Preregistration

The candidate set is frozen before the unexposed E2 body or output is opened.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal E2 reproduction | Pinned source environment | Source grids, walls, tolerances, and literals | Tally proves only implemented predicates | Hash, AST, process, output, and six-predicate ledger |
| B | Exact generalized functional | Declared positive B and I | B and I | Variation, B=1 reduction, scaling, and virial identity close exactly | Independent SymPy variation, substitutions, scaling, signs, and factor mutations |
| C | Endpoint-asymptotic branch | Regular origin and massless tail | Inner amplitude and two exponents | Correct Robin data reduce cutoff and wall artifacts | Dominant balance, B=1 limit, cutoff/domain refinement, hard-wall countercomparison |
| D | Canonical shooting | One monotone branch bracket per declared input | DOP853 tolerances, cutoffs, domains, samples | Solver succeeds and profiles/energies converge with explicit tail control | Root bracket, solver evidence, EOM residual, virial balance, and refinements |
| E | Independent collocation | Same exact ODE and asymptotic data, fresh initialization | Initial mesh, tolerance, max nodes | solve_bvp agrees without importing the shooting profile | Status, collocation residuals, common-grid profile and energy comparisons |
| F | Angular-input sensitivity | Same branch family under changed I | accepted I, source I, and B-squared mutation | Corrected values cause measurable but controlled shifts; I is load bearing | Profile/energy differences and ordering under preregistered mutations |
| G | Minimization audit | Explicit admissible variation would be required | None unless registered later | Stationarity and virial balance do not by themselves prove global minimum | Negative-mode or competing-profile search if a minimum claim is attempted |
| H | Consumer ceiling | Accepted dependencies only | None | No state, binding, or yield follows from conditional b values | Registry and hash-pinned downstream consumer ledger |

## Selection Criteria and Blinding

Candidates are selected by accepted dependency closure, exact variational and
endpoint correctness, solver status, residual and refinement evidence,
independent-method agreement, tail and virial control, assumption economy,
mutation sensitivity, and separation of mathematical and physical claims.
Numerical closeness to E2's exposed `1.2317`, `1.208`, and `1.136` values cannot
select a method, boundary condition, mesh, tolerance, or claim.

No comparator blinding remains. P105 freezes the corrected accepted inputs,
endpoint exponents, two numerical routes, residuals, refinements, mutations,
and interpretation ceilings before further source inspection or execution.

## Proposed Claim Delta

P105 reserves C-RPROF-001 for the exact conditional generalized radial
functional, Euler-Lagrange equation, B=1 reduction, endpoint exponents, Derrick
scaling, and virial identity. It reserves C-RPROF-002 for separately reviewed
resolution-bounded stationary branch and energy evidence for the three exact
declared input pairs if both numerical methods meet the frozen gates.

C-RPROF-001 depends on C-RMAP-001 only for the meaning of declared positive
degree and angular input; the functional itself remains a conditional model.
C-RPROF-002 depends on C-RPROF-001, C-RMAP-001, and C-RMAP-002. C-MOD-001/002
are B=1 compatibility anchors rather than hidden derivation inputs. No accepted
claim is challenged or superseded.

## Implementation and Oracle Plan

A pure `rational_map_radial.py` module will expose the symbolic density and
residual, endpoint exponents and boundary residuals, an evidence dataclass,
energy components, and a canonical shooting solver. Imports execute no solve
or print. Sampled energy integration must use `trapezoid_integral`; no direct
NumPy trapezoidal alias is permitted.

SymPy is the strongest oracle for variation, B=1 reduction, dominant-balance
equations, scaling, and normalization. The exact checks will derive expressions
rather than compare copied formulas. Mutations change the B coefficient, I
sign/factor, radial measure, scaling direction, origin exponent, and tail
exponent.

Canonical shooting uses DOP853 through `solve_ivp_evidence`, a bracketing root
for the origin amplitude, binary64 precision, inner cutoffs including at least
`1e-3`, `3e-4`, and `1e-4`, outer domains including at least `16`, `24`, `32`,
and `48` where stable, tolerances no weaker than `rtol=1e-9`, `atol=1e-11`,
and at least three sample resolutions. It records function evaluations,
boundary residuals, pointwise ODE residual on an independently differentiated
profile, `E2`, `E4`, normalized `b=E/(12 pi^2)`, omitted-origin and tail
estimates, and monotonicity without assuming it.

Independent collocation uses `solve_bvp_evidence`, a fresh analytic monotone
guess rather than the shooting result, asymptotic Robin residuals at both
walls, initial meshes at least 300, 600, and 1200, tolerances including
`1e-5`, `1e-7`, and `1e-9`, and sufficient `max_nodes`. It records success,
iterations, RMS residuals, common-grid profile differences, energy differences,
and boundary residuals. Final method agreement targets `2e-4` relative in
energy and a scale-normalized profile sup norm below `2e-3`, tightened if the
refinement data justify it.

For a tail `C r^-p`, the leading omitted two-derivative energy is evaluated
from `(p^2+2B)C^2 r^-2p`; origin and four-derivative omissions are also bounded
or shown negligible by domain/cutoff refinement. A hard finite-wall Dirichlet
solve, source-biased I values, `I=B^2`, wrong ODE signs, and missing solver
status are countermodels. Any attempted global-minimum statement additionally
requires a separately registered second-variation or competing-profile oracle;
otherwise it is rejected without weakening the stationary result.

Focused replay covers the new module, C-MOD-001/002 radial tests, C-RMAP-001/002
tests, and shared numerics tests. Each E2 predicate and direct/indirect consumer
receives an individual verdict. One full workflow runs only at a promotion or
terminal adjudication boundary.

## Attempts and Continuation

Every source, variation, endpoint, branch, bracket, stiffness, solver, mesh,
domain, cutoff, tolerance, quadrature, residual, tail, normalization, mutation,
consumer, or verifier failure is append-only with its exact command, output,
diagnosis, and next route. A failed B=4 shooting bracket or source hierarchy
does not finish P105; the method is repaired or changed while the positive
exact object and terminal E2 audit continue.

## Debt Ledger

P105 tracks source hash and exposure, exact B and I, density and normalization,
variation, signs, B=1 reduction, endpoint exponents and amplitudes, inner and
outer boundary semantics, solver status, precision, cutoff, domain, mesh,
tolerances, residual norms, energy components, origin/tail omissions, virial
balance, independent method, angular sensitivity, stationarity versus
minimality, every source check, dependencies, consumers, disposition,
generated state, and parent continuation. Every item must be derived,
declared, rejected, or excluded.

## Review and Promotion Plan

Each surviving proposed claim receives a separate claim-level review. P105
will add primary and independent verifiers, source predicate adjudication,
impact analysis, and affected-consumer replay. Acceptance requires canonical
package extraction, sensitive tests, governance and release updates, generated
documentation, accepted-memory synchronization, a terminal E2 disposition,
and one full workflow. A final record-only update reruns only record-sensitive
repository, generation, memory, and diff checks.

## Done Gate

P105 closes only when the exact generalized radial object exists, every
promoted branch has two-method refined evidence with endpoint and tail control,
the corrected angular inputs are used, stationarity and minimization are
separated, every E2 predicate and consumer is adjudicated, claim/release state
agrees, campaign debt is empty, and the parent migration advances. Six source
checks or three exposed energy decimals are not completion.

## Cross-References

This campaign cross-references E1 through E5, B1, PG3, S2, C-RMAP-001,
C-RMAP-002, C-MOD-001, C-MOD-002, C-SCL-001, P062, P084, P104, the canonical
rational-map, radial-mode, and numerics modules, and the framework-migration
effort.

## Terminal Adjudication

P105 promotes C-RPROF-001 as the exact conditional generalized radial
functional, equation, energy split, scale identity, and endpoint theorem, and
C-RPROF-002 as two-method resolution-bounded evidence for the three declared
stationary branches. Canonical 2401-sample per-degree coefficients are
`1.2314456867`, `1.2081352135`, and `1.1365144999`; fresh collocation agrees
within its declared residual and integration bounds.

Attempts 0002 and 0003 preserve the loss of the tiny degree-four origin signal
when evolving `f` near `pi` and the failure of root tightening to repair it.
The equivalent vacuum-complement variable closes that representation defect.
Attempt 0004 corrects a comparison between endpoint-corrected and uncorrected
finite-domain energies, and 0006 preserves a 1201-versus-2401 sample-count
record correction. `I=B` and `I=B^2` change energies but preserve the selected
ordering, so neither validates a physical binding narrative.

E2 is qualified. No physical action, angular or radial global minimum, full
field, baryon or nucleus map, fission threshold, binding hierarchy, reaction,
or yield is promoted. Claim debt is empty; the corpus migration continues
with E3.
