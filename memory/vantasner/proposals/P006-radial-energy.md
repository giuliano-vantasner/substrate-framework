---
description: Derive and promote the exact radial-energy classification used by T1A
author: vantasner
created: '2026-08-01T11:39:13Z'
updated: '2026-08-01T11:43:25Z'
tags:
- substrate-framework
- campaign-proposal
- radial-energy
- migration-T1A
category: proposals
confidence: exploratory
status: archived
---
# P006 Exact Radial-Energy Classification

## Question and Positive Deliverable
This campaign derives an importable radial-energy classification rather than an object-identification slogan. The positive claim `C-RG-001` will state the exact homogeneity, derivatives, and stationary structure of positive line, spherical-shell, and capillary energies. It will then instantiate the line class conditionally with an independent tension `T` and with the accepted breather energy `E_b(omega)` from `C-SG-002`.

The intended ceiling is exact: two circumference-weighted line energies have the same function of radius, while equality for every positive radius holds if and only if their density coefficients agree. No accepted premise equates `T` with `E_b`, derives a common physical object, fixes the radius, or forces ring quantization.

## Base Release and Provenance
The accepted base is `v0.5.0` at framework commit `a4d0dc4`. The only accepted dependency is `C-SG-002` for `E_b(omega)=16 sqrt(1-omega^2)` on `0<omega<1`.

The hash-pinned source unit is T1A at `merged-framework/bridges/phase-1/bridge_T1A_ring_equals_ring.py`, SHA-256 `2960ca43cb2f3a30939548853de0aa464c11e0d779d4f74522f48c19c2864976`. It is pending adjudication. Its linked Frank-action, shadow-ring, and quantization materials are evidence, not accepted dependencies. In particular, T1A itself says the full capillary energy is `2*pi*R*T-pi*R^2*P+E_core`, that the breather ring is a declared lift, and that no source equates `T` to `E_b`.

## Invariants, Conventions, and Allowed Imports
The radius `R`, line density, shell density, and where used pressure are positive real quantities. Core energy is an arbitrary additive constant. Homogeneity is tested by `E(aR)=a^k E(R)` for every positive scale `a`; an additive core or mixed radial powers therefore make the full capillary energy nonhomogeneous even though it contains a line component.

The geometric factors `2*pi*R` and `4*pi*R^2` are declared circumference and spherical-area constructions. `C-SG-002` supplies only the breather coefficient. The Frank tension remains an independent positive input; its microscopic formula is not imported or rederived here.

## Candidate Preregistration
Three exact routes are registered before implementation. There is no empirical comparator.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Euler/homogeneity classification under radius rescaling | Positive radius and coefficients | none beyond API inputs | Directly captures the source's shared-form ceiling | Exact scaling residuals vanish only at the correct degree |
| B | Marginal derivative classification | Differentiability | none | Independently separates constant line marginal cost from radius-dependent shell cost | Derivatives and second derivatives have the claimed dependence |
| C | Logarithmic slope and stationary structure | Positive energy for log slope | none | Useful cross-check and exposes the capillary barrier | Recover degrees one/two and the unique capillary maximum |

## Selection Criteria and Blinding
The frozen order is full-domain exact scaling, independent-coefficient honesty, discrimination among line/shell/capillary forms, stationary-radius behavior, mutation sensitivity, then API simplicity. Candidate A is primary because it states the structural equivalence without relying on a sample point. Candidate B independently checks the line hallmark. Candidate C supplies an additional classification and the capillary maximum. No comparison values exist to inspect.

## Proposed Claim Delta
P006 proposes one compatible-extension claim depending on `C-SG-002`.

| Claim | Exact statement | Dependencies | Oracle | Consumers |
| --- | --- | --- | --- | --- |
| C-RG-001 | Positive circumference line energy is degree one with constant positive derivative and no stationary radius; positive spherical-shell energy is degree two with radius-dependent derivative; the full positive-pressure capillary form has a unique strict maximum. Conditional pulson and breather line lifts share only the line class, and equality is equivalent to coefficient equality. | C-SG-002 | exact SymPy algebra/calculus and independent scaling derivation | future ring-lift, capillary, and dimensional-classification campaigns |

## Implementation and Oracle Plan
A pure `src/substrate_framework/radial_energy.py` module will expose line, spherical-shell, and capillary energies plus the positive-pressure critical radius. APIs will accept exact SymPy objects and ordinary real scalars without hidden units or global state.

The main verifier will prove exact scaling, derivatives, Euler identities, absence or presence of stationary radii, the strict capillary maximum, breather positivity and limits, and the coefficient-equality condition. It will reject radius powers zero/two for the line predicate, the shell measure as a line, coefficient equality without an explicit premise, and a minimum interpretation of the capillary critical radius. An independent review will derive scaling exponents from ratios and derivatives without importing the new module.

## Attempts and Continuation
Attempt `0001` implements Candidate A and uses Candidates B/C as independent guards. If the generic homogeneity predicate accepts a mixed capillary form, it is repaired or rejected before promotion. If coefficient equality cannot be established from accepted dependencies, object identity remains excluded rather than being fitted or narrated into the claim.

## Debt Ledger
P006 starts with four debts.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| Shared radial degree could be misreported as object identity | Claim and review state the exact coefficient-equality iff condition and exclude object identity | discharged |
| The isolated line term could be confused with the full capillary energy | Full form is implemented and its nonhomogeneity and strict maximum are checked | discharged |
| A declared ring radius could be presented as predicted | Exact derivative proves a positive line term has no stationary positive radius | discharged |
| The source's shell guard could be a copied power count | Independent scaling and derivative routes reject it as a line | discharged |

## Review and Promotion Plan
One claim-level review will inspect exact domains, the dependency on `C-SG-002`, coefficient independence, all T1A subclaims, mutations, and consumers. Promotion will freeze P006, add the importable module/tests, update the registry and release, regenerate documentation and migration memory, and mark T1A migrated only if its shared-form result, shell guards, free-radius ceiling, and coefficient non-identity are all represented. The source's unproved microscopic Frank-tension derivation and optional quantization will remain explicit nonclaims rather than pending bridge subclaims.

## Results and Promotion
Attempt `0001` passed 28 exact checks. The independent route passed eight checks using transverse-measure ratios, logarithmic derivatives, completion of the square, and a separate coefficient-equality solution. The capillary critical point is a global maximum, the isolated line term has no stationary radius, and coefficient equality is neither assumed nor inferred.

`C-RG-001` was accepted as `symbolic_verified`, `compatible_extension`, and `active` in `v0.6.0`. T1A is fully migrated because all eight executable source predicates are represented, while the physical Frank-action attribution, declared breather lift, and optional quantization remain explicit conditional inputs rather than promoted conclusions.

## Done Gate
P006 is complete. The positive radial-energy classification exists, exact and independent routes agree, load-bearing mutations fail, T1A has a reviewed migrated disposition, affected consumers replay, and the campaign debt ledger is empty.
