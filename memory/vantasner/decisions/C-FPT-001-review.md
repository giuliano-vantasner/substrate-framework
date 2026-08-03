---
description: Independent review of C-FPT-001 reflected first-passage theorem and interpretation ceilings
author: vantasner-review
created: '2026-08-03T14:08:59Z'
updated: '2026-08-03T14:08:59Z'
tags:
- substrate-framework
- claim-review
- first-passage
- stochastic-process
category: decisions
confidence: established
status: archived
---
# Review of C-FPT-001

## Claim Under Review

C-FPT-001 conditions on a one-dimensional overdamped Itô diffusion on a
compact interval `[a,b]`, with drift `-U'/gamma`, diffusion scale
`sqrt(2*Theta/gamma)`, reflection at `a`, absorption at `b`, and an initial
point `x`. For positive `Theta` and `gamma` and a sufficiently regular declared
potential, the mean absorption time is the unique positive solution of
`Theta*tau''-U'*tau'=-gamma`, `tau'(a)=0`, `tau(b)=0`, with the exact positive
double-integral representation. Additive potential constants cancel. The
linear-potential specialization and its zero-force limit are exact. The claim
also states that completed-only finite-horizon means and thresholded zeros are
not the full MFPT, and inverse MFPT is not generally a constant hazard. It
challenges and supersedes no accepted claim.

## Sourced Inputs

The review reads base release `v0.86.0`, C-RG-001, C-RG-002, C-COL-001,
C-TH-001, C-TH-002, C-COH-001, C-PRB-001, their relevant canonical modules and
reviews, P103's frozen proposal, all append-only attempts, primary and
independent verifiers, focused tests, source and literal-check ledgers,
dependency and consumer maps, and hash-pinned BD5. BD5's constant-Kramers-rate,
temperature-independent-prefactor, optimum, convergence, population ignition,
physical inertia, material, and event readings remain outside the claim delta.

## Independence

The independent route imports no canonical first-passage implementation. It
freshly differentiates the integrating-factor solution, evaluates the linear
control, derives the free-diffusion moment counterexample, evaluates nested
quadrature at 45 decimal digits, and solves the backward boundary-value problem
by direct collocation over three tolerances. Source predicates, expected values,
and the primary API are not its oracle.

## Verification Status

The maximum status is `symbolic_verified`. The promoted theorem,
boundary data, additive-offset cancellation, linear formula, zero-force limit,
and free-diffusion counterexample are exact symbolic results. The primary route
passes thirty-seven checks and the independent route twenty-one. Adaptive
quadrature, collocation, and Euler-Maruyama studies validate implementations
and the BD5 specialization but do not upgrade numerical evidence into an exact
proof. No unevaluated symbolic object is treated as a terminal result.

## Sensitivity and Counterexamples

Mutations change the backward diffusion, drift, source coefficient, drift sign,
potential sign, absorbing location, barrier depth, completion threshold, and
censored-path treatment; every load-bearing verdict changes or fails. Zero and
linear forces provide soluble controls. Free reflected diffusion has squared
coefficient of variation `2/3`, not the exponential value one, so inverse MFPT
does not imply a constant hazard. At barrier ratio twenty the exact inverse
MFPT stays positive while the source returns its operational zero. Quadrature
tolerance, collocation tolerance/mesh, stochastic timestep, and ensemble size
are refined with solver status, residual, relative error, seed, horizon, and
uncertainty exposed.

## Framework Compatibility

The claim is a compatible dependency-root mathematical extension. It changes
no accepted invariant and makes the process, potential, friction, thermal
scale, interval, initial state, and boundary semantics explicit. Accepted
radial, collective, thermal, and coherence claims are interpretation ceilings,
not hidden dependencies. A physical coordinate, bath, mobility, material,
event, and observation map remain unresolved premises for any broader use.

## Dependency and Consumer Replay

Direct governed consumers are the pure module, additive exports, focused tests,
P103 verifiers, governance, generated documentation, and memory. The legacy
sampled MFPT converges to the adaptive result and uses `np.trapezoid`; rung091
passes its algebraic checks but does not close the physical prefactor. Other
legacy consumers are static narrative evidence. GitNexus reports LOW additive
risk, no pre-existing affected symbols or execution flows, and no relevant
repository process. The claim creates no debt in accepted consumers.

## Competing Candidate Audit

Candidates A through I and structural criteria froze before renewed source
execution. Literal reproduction remains evidence only. The exact backward
route, independent numerical route, explicit stochastic regression, censoring
audit, boundary asymptotic, load-bearing boundary mutations, and interpretation
ceilings are selected by exactness, assumption economy, convergence, and
framework fit—not by the source tally or its fitted slope near minus one.

## Four-Axis Decision

The integrated promotion gate closes the review decision as acceptance.

- Verification: `symbolic_verified`
- Review: `accepted`
- Compatibility: `compatible_extension`
- Epistemic: `active`
- Relationship: dependency root; challenges and supersedes none

## Promotion Transaction

Promotion adds C-FPT-001, the importable first-passage module and tests,
immutable P103 evidence, qualified BD5 disposition, release `v0.87.0`, generated
documentation, and accepted-state memory. The source queue is regenerated from
the editable disposition record. The active proposal becomes an adjudicated
campaign after all referenced evidence exists and the integrated gate passes.

## Continuation if Not Accepted

If the gate fails, the failed attempt remains append-only and the campaign
repairs the exact implementation, numerical method, record closure, or consumer
surface without weakening the theorem. A physical Kramers, Langer, population,
material, ignition, or event claim requires a separate proposal that derives
the missing stochastic and observational premises.

## Done Gate

Acceptance requires the exact positive object, frozen competing concepts,
independent rederivation, mutation-sensitive numerical evidence, importable
APIs/tests, complete source classification, synchronized promotion surfaces,
and an empty claim-level debt ledger. The parent corpus migration remains
active after P103 because later source units are pending.

## Cross-References

See P103, BD5, legacy rung091, C-RG-001, C-RG-002, C-COL-001, C-TH-002,
C-COH-001, C-PRB-001, the first-passage module, proposed release `v0.87.0`, and
the framework-migration effort.
