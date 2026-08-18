---
description: Accepted framework claim C-VIR-002
author: framework-registry
created: '2026-08-18T22:40:00+02:00'
updated: '2026-08-18T22:40:00+02:00'
tags:
- substrate-framework
- accepted-claim
- C-VIR-002
category: claims
confidence: established
status: active
---
# C-VIR-002

## Statement
The accepted statement is reproduced exactly from the claim registry.

For positive real wave speed c and positive period T, if a total nonnegative density magnitude M satisfies the period-integrated virial relation 6*c^2*M*T=0, then M=0: a positive-period, positive-speed configuration with vanishing period-integrated virial forces the total density to vanish. The supporting finite certificates hold exactly: a sum of four real squares a^2+b^2+d^2+e^2 equals zero only termwise; a real affine function nonnegative on all of the real line has zero slope; and the single-crossing identity R0^2+3*c^2*(R0/c)^2=4*R0^2. These are the finite algebraic implications of the Comparsi exact-breather virial nonexistence route; the PDE differentiation and integration-by-parts identities that produce the virial relation are declared inputs verified symbolically in the source workspace, not here. This is a conditional finite-implication theorem. It does not prove the virial identity for any PDE, establish nonexistence of periodic solutions by itself, or treat any physical breather.

## Status Axes
The four governance axes remain independent.

Verification is `formal_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: none. Assumptions: The virial relation 6*c^2*M*T=0 and its PDE derivation are declared inputs; the claim machine-checks the finite implications and certificates., The nonexistence reading requires the separately verified symbolic structure identities; this claim supplies only their finite algebraic consequences.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.163.0` with provenance `campaigns/P233-lean-discrete-facts/adjudication.yaml`.

- `formal/SubstrateFramework/Ingested/ComparsiVirial.lean`
- `campaigns/P233-lean-discrete-facts/attempts/0001/result.yaml`
- `campaigns/P232-lean-corpus-census/census.yaml`
