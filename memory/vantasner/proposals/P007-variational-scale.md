---
description: Derive parameter-scale invariance and conditional optical collective dynamics
author: vantasner
created: '2026-08-01T11:49:37Z'
updated: '2026-08-01T11:55:53Z'
tags:
- substrate-framework
- campaign-proposal
- variational-scale
- migration-T1D-T2B
category: proposals
confidence: exploratory
status: archived
---
# P007 Variational Scale and Collective Dynamics

## Question and Positive Deliverable
This campaign derives three narrowly separated positive objects. `C-VAR-001` is the general Euler-Lagrange theorem that multiplication by any nonzero fixed parameter-only factor leaves the equations of motion unchanged. `C-CC-001` derives the full coordinate-time acceleration of the declared optical collective action and its slow limit, with an exact mixed-scale counterexample. `C-VIR-001` records only the conditional linear-algebra consequence of the predecessor's virial slope formulas.

The deliverable corrects two overstatements in the predecessor narrative. Uniform degree one in `E0` is sufficient but not necessary: any single nonzero uniform power or parameter-only factor cancels. And integrating an ODE twice after exact algebra has removed `E0` from its right-hand side is regression evidence, not an independent dynamic verification. Under local uniqueness, identical equations and initial data already imply identical trajectories.

## Base Release and Provenance
The accepted base is `v0.6.0` at framework commit `20e2d95`. `C-OG-001` supplies the static positive optical metric `diag(-1/n,n/c0^2)` and its conventions; no accepted Skyrmion, BEC-realizability, or full 3D PDE claim is imported.

The hash-pinned source units are T1D at `merged-framework/bridges/phase-1/bridge_T1D_Rk_E0_divides_out.py`, SHA-256 `51a62aac55097bfdb5c3db61ac5932b547881d6436d602ca04c3038a11a2c48a`, and T2B at `merged-framework/bridges/phase-2/bridge_T2B_dynamic_optionC_EP.py`, SHA-256 `c6826db8b4199977d602fc5bf92b6e432f60eea1d9805f9e42c1309ccff3c7af`. Both are pending. Their cross-references create a narrative cycle, but their exact dependency root is the generic variational theorem; the later S5 physical-realizability annotation is outside P007's allowed imports.

## Invariants, Conventions, and Allowed Imports
The scale factor is nonzero and constant with respect to the path coordinate, velocity, and evolution parameter. This restriction is load-bearing: a time- or coordinate-dependent multiplier adds Euler-Lagrange terms and is not a harmless action normalization.

For the collective action, `n(q)>0`, `c0>0`, `E0>0`, and `n(q)^2*qdot^2<c0^2`. The index is sufficiently differentiable for the exact equation and local ODE uniqueness. The one-coordinate effective action is conditional on a collective-coordinate/eikonal reduction; no full 3D field equation is inferred.

The virial formulas are explicit conditional inputs. P007 may solve their simultaneous slope condition, but it may not treat the formulas, predecessor fitted slopes, Option-C microscopic realization, or S5's later claims as derived.

## Candidate Preregistration
Three routes are frozen before implementation; there is no empirical comparator.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Factor a general fixed scale through the Euler-Lagrange operator | Scale independent of path and time | arbitrary nonzero scale | Gives the strongest exact theorem and corrects degree-one overstatement | Symbolic operator identity plus a coordinate-dependent multiplier counterexample |
| B | Reconstruct coordinate-time geodesic acceleration from the optical metric | C-OG-001 metric and timelike path | none beyond `n,c0` | Independently fixes every coefficient and sign | Christoffel route equals the action-derived acceleration |
| C | Integrate two parameterized IVPs | Solver and tolerance choices | sample profile, interval, tolerances | Redundant for the homogeneous model; potentially useful only where no exact discriminator exists | Replaced by exact local Taylor separation for the mixed-scale guard |

## Selection Criteria and Blinding
The frozen order is general exactness, correct assumptions, optical-framework composition, conditional physical scope, mutation sensitivity, then computational cost. Candidate A is selected for the scale theorem. Candidate B independently verifies the concrete optical dynamics. Candidate C is not used for the homogeneous verdict because it would integrate an already identical right-hand side; an exact difference in initial acceleration is stronger for the mixed-scale counterexample.

## Proposed Claim Delta

P007 proposes three additive claims with deliberately separate physical scope.

| Claim | Exact statement | Dependencies | Oracle | Consumers |
| --- | --- | --- | --- | --- |
| C-VAR-001 | A nonzero parameter-only multiplier factors through the Euler-Lagrange operator, so it preserves the solution set; no special degree-one restriction is required | none | exact general SymPy differentiation plus dependent-multiplier counterexample | all effective-action and scale-invariance campaigns |
| C-CC-001 | The declared optical collective action gives the exact profile-dependent, `E0`-free acceleration and slow drift; its IVP is scale-independent where locally unique, while a specified mixed-scale action has exact `E0`-dependent initial acceleration | C-VAR-001, C-OG-001 | exact EL solve, independent Christoffel derivation, local Taylor counterexample | optical drift and collective-coordinate campaigns |
| C-VIR-001 | Conditional on the declared slope formulas, both slopes equal `-1/2` if and only if `(a,b)=(0,1)` | none; formulas are assumptions | exact linear solve and wrong-option probes | future governed Option-C proposals |

## Implementation and Oracle Plan
A pure `src/substrate_framework/variational.py` module will expose the Euler-Lagrange operator and unique acceleration solver. A pure `src/substrate_framework/collective_dynamics.py` module will expose the optical collective action, exact acceleration, slow limit, and conditional virial exponents. Tests will cover formulas, domain guards, factorization, and wrong multipliers.

The main verifier will use a general symbolic Lagrangian to factor an arbitrary fixed scale, show a uniform square also cancels, and reject a coordinate-dependent multiplier. It will solve the concrete action rather than insert the acceleration, prove full and slow forms, and derive exact `E0` sensitivity for the source's mixed-scale action on `n=1+alpha*q`. The independent review will compute Christoffels directly and convert affine geodesics to coordinate time. Another exact route will solve the virial linear system and reject Options A/B.

No SciPy integration is planned for the homogeneous action: exact parameter elimination plus local uniqueness already proves same-data trajectory identity. This directly removes the T2B validation ceremony. Numerical integration becomes appropriate only for behavior not fixed analytically.

## Attempts and Continuation
Attempt `0001` implements Candidate A and the exact concrete consequences. If SymPy cannot solve the general functional EL equation, the theorem will be verified structurally by explicit product differentiation without weakening its quantifiers. If the metric route disagrees, conventions are audited before either formula is accepted.

## Debt Ledger

P007 begins with four explicit debts that must all be discharged.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| Predecessor claims degree one is the precise cancellation condition | Prove arbitrary nonzero fixed uniform factors cancel and update workflow language | discharged |
| T2B calls duplicate integrations new dynamic evidence | Codify the exact-uniqueness shortcut in AGENTS, skill, templates, and review | discharged |
| Collective-coordinate action could be narrated as a full 3D derivation | Claim and review keep the action and physical lift conditional | discharged |
| T2B contains a later S5 physical-realizability annotation | Preserve it as explicit remaining source scope rather than importing it | discharged |

## Review and Promotion Plan
Three claim-level reviews will separately audit the generic theorem, optical equation, and conditional virial selection. Promotion will freeze P007, add importable APIs/tests, create a pinned release, regenerate docs and accepted memory, mark T1D migrated if all of its exact predicates are represented, and mark T2B partially migrated with the S5 annotation as exact remaining scope. Full validation runs once at the unchanged promotion boundary.

## Results and Promotion
Attempt `0001` passed 22 exact checks. The independent first-variation, Christoffel, slow-expansion, and inverse-virial routes passed seven checks. The exact theorem corrects the predecessor's degree-one necessity language: every nonzero path- and time-independent multiplier preserves the Euler-Lagrange solution set, while dependent multipliers do not in general.

`C-VAR-001`, `C-CC-001`, and `C-VIR-001` were accepted as symbolically verified in `v0.7.0`. T1D is fully migrated. T2B is partially migrated because its exact collective-coordinate predicates are represented more strongly, but its later S5 physical-realizability annotation remains unadjudicated. Duplicate `E0` trajectory integrations were deliberately not repeated; exact vector-field independence plus local uniqueness decides that statement, and exact initial acceleration separates the mixed-scale counterexample.

## Done Gate
P007 is complete. All three positive claims pass exact and independent checks, the workflow improvement is consolidated, affected consumers replay, both source dispositions preserve their exact scope, and the campaign debt ledger is empty.
