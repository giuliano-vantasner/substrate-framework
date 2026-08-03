---
description: Independent review of the exact conditional rational-map sphere theorem and axial family
author: vantasner-review
created: '2026-08-07T12:20:00Z'
updated: '2026-08-07T12:20:00Z'
tags:
- substrate-framework
- claim-review
- rational-map
- sphere-geometry
category: decisions
confidence: established
status: archived
---
# Review of C-RMAP-001

## Claim Under Review

C-RMAP-001 conditions on the oriented unit Riemann sphere with its normalized
round measure and on a declared coprime holomorphic rational map `R=p/q` of
exact degree `B>=1`. Its conformal Jacobian has normalized area `B`; the angular
functional `I=<J^2>` obeys `I>=B^2`, with deficit equal to the normalized
integral of `(J-B)^2`. For the axial family `R=z^B`, explicit beta integration
gives `I_B=B^3(1+Gamma(2-1/B)Gamma(2+1/B))/3`, including `I_1=1` and
`I_2=pi+8/3`. The claim also requires exact common-factor reduction before
assigning rational degree. It challenges and supersedes no accepted claim.
For `u=cos(theta)`, the review uses
`sin(theta)dtheta=-du` and reverses the transformed bounds, so the implemented
positive measure is `du*dphi` on `u` from `-1` to `1`.

## Sourced Inputs

The review reads base release `v0.87.0`, accepted C-MOD-001, C-MOD-002,
C-SK-001, C-TOP-002, and C-DIM-002, their relevant canonical modules and
reviews, P104's frozen proposal, all append-only attempts, both verifiers,
focused tests, source/check/dependency/consumer ledgers, and hash-pinned E1.
The accepted claims are interpretation ceilings, not scientific dependencies.

## Independence

The independent route imports no canonical rational-map implementation. It
freshly computes polynomial gcds, performs the degree-two radial area and
angular integrals directly, evaluates a separate Euler-beta decomposition for
the generic axial family, and uses direct/reciprocal-chart adaptive integration
only as implementation corroboration. The source decimals are not its oracle.

## Verification Status

The maximum status is `symbolic_verified`. Exact polynomial algebra, the
pullback degree theorem, the normalized-square identity, explicit radial
substitution, Euler beta/gamma evaluation, reflection formula, and exact
identity/degree-two controls establish the promoted surface. The primary route
passes thirty-five checks and the independent route eighteen. Numerical sphere
integration is regression and specialization evidence only; it does not
upgrade or replace the exact theorem.

One earlier primary pass contained self-comparing beta and variance assertions.
Attempt 0005 rejects that oracle despite its successful tally. Attempt 0006
replaces it with three explicit beta kernels and the derived nonnegative-square
deficit. The failed-oracle record is preserved rather than rewritten.

## Sensitivity and Counterexamples

Common polynomial factors alter apparent degree while leaving the reduced map
unchanged. Derivative, sphere-measure, and normalization mutations break the
area identity. A flat theta-phi weight breaks identity normalization. Exact
identity and degree-two controls expose E1's endpoint-loss bias. Axial maps of
degrees two through eight are strictly above the lower bound, while the
identity saturates it. None of these facts converts a single shifted-map
comparison into a global minimization proof.

## Framework Compatibility

The claim is a native dependency-root mathematical extension. It changes no
accepted invariant and introduces no physical Skyrme action, radial ansatz,
state map, or scale. C-MOD-001 supplies only a compatibility check at `B=1`;
C-TOP-002 concerns a distinct SU(3) current and cannot identify rational degree
with physical baryon number. All model and physical interpretations remain
explicitly excluded.

## Dependency and Consumer Replay

Direct governed consumers are the pure module, additive exports, focused tests,
P104 verifiers, governance, generated documentation, and memory. No accepted
canonical path imports the module. Pinned E2 and later sources duplicate the
formula and add unaccepted premises; they are sequential migration targets,
not accepted consumers. GitNexus reports LOW additive impact and no affected
pre-existing symbol or process. Canonical work uses no version-specific NumPy
trapezoidal alias.

## Competing Candidate Audit

Candidates A through H and structural criteria froze before source inspection.
Exact degree/area/bound and axial derivation, stable tensor cubature, independent
adaptive integration, declared-map evaluation, rejected minimization, and
consumer ceilings were compared on exactness, dependency closure, mutation
sensitivity, and assumption cost. The exposed E1 decimals neither select the
theorem nor set its tolerances.

## Four-Axis Decision

The integrated promotion gate closes the review decision as acceptance.

- Verification: `symbolic_verified`
- Review: `accepted`
- Compatibility: `native`
- Epistemic: `active`
- Relationship: dependency root; challenges and supersedes none

## Promotion Transaction

Promotion adds C-RMAP-001, the importable rational-map module and tests,
immutable P104 evidence, qualified E1 disposition, release `v0.88.0`, generated
documentation, and accepted-state memory. E1's exact identity survives; its
broader numerical and interpretive headlines remain qualified or rejected.

## Continuation if Not Accepted

If the gate fails, the append-only attempt remains and the campaign repairs the
exact derivation, verifier, evidence closure, or consumer replay without
weakening the theorem. Global minimization, radial energy, or a physical-state
map requires a separately preregistered claim with its own oracle.

## Done Gate

Acceptance requires the positive exact theorem, competing concepts, actual
beta and lower-bound derivations, independent rederivation, mutation-sensitive
controls, importable APIs/tests, complete source classification, synchronized
promotion surfaces, and no claim-level debt. The corpus migration continues
after P104 because later units remain pending.

## Cross-References

See P104, E1, C-RMAP-002, C-MOD-001, C-MOD-002, C-SK-001, C-TOP-002,
C-DIM-002, the rational-map module, proposed release `v0.88.0`, and the
framework-migration effort.
