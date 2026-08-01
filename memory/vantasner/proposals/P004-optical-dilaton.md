---
description: Derive and promote the exact 1+1 optical curvature-dilaton and conditional weak-field maps
author: vantasner
created: '2026-08-01T11:23:59Z'
updated: '2026-08-01T11:30:13Z'
tags:
- substrate-framework
- campaign-proposal
- optical-geometry
- dilaton
- migration-T1B
category: proposals
confidence: exploratory
status: archived
---
# P004 Optical Metric and Dilaton

## Question and Positive Deliverable
This campaign derives the exact geometry of the declared static 1+1 optical metric `g=diag(-1/n,n/c0^2)` for positive `n(x)`. It asks which scalar compositions `f(n)` obey `Box_g f(n)=R[g]` for every static profile, then derives the conditional weak-field potential and geodesic-drift map under the explicit constitutive relation `n=(1+2 Phi/c0^2)^-1`.

The positive deliverables are two narrow claims. `C-OG-001` states the exact curvature formula, `Box_g log(n)=R[g]`, and uniqueness `f(n)=log(n)+C` among twice-differentiable compositions. `C-OG-002` states conditionally that `log(n)=-log(1+2 Phi/c0^2)` has leading term `-2 Phi/c0^2`, while the metric's slow geodesic acceleration is exactly `-(1+2 Phi/c0^2) Phi_x` and tends to `-Phi_x` in the weak-field scaling limit.

No sourced matter equation, Poisson normalization, 3+1 gravity claim, or empirical comparison is proposed.

## Base Release and Provenance
The accepted base is `v0.3.0` at framework commit `5709eab`. Its four accepted sine-Gordon claims are invariants but not dependencies of the optical root.

The hash-pinned predecessor unit is `T1B`, path `merged-framework/bridges/phase-1/bridge_T1B_phi_ln_n_potential.py`, SHA-256 `d23749be7385706cad0e7b3441298c30d085d4ce3992fa558cd0283d847d7947`. It is pending in `migration/source-claims.yaml`. Its bridge is candidate evidence; its pass tally is not authority.

## Invariants, Conventions, and Allowed Imports
The index is a positive twice-differentiable static function, `c0>0`, coordinates are `(t,x)`, and the signature is `(-,+)`. The metric form is a declared model premise. The TF relation between `n` and `Phi` is an explicitly approved conditional import for `C-OG-002`, not a framework-derived constitutive law.

Additive constants in the dilaton must remain a symmetry because `Box_g C=0`. The result stays strictly 1+1 dimensional. The predecessor's assertion that a matter-sourced dilaton equation yields a particular Poisson coefficient is excluded because T1B does not state or derive the required sourced action and sign normalization.

## Candidate Preregistration
Three approaches are frozen before implementation; there is no empirical comparator.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Write `Box_g f(n)` for arbitrary profile derivatives and match independent `n''` and `(n')^2` coefficients to curvature | Declared metric and exact calculus | additive constant only | Proves the true uniqueness class, stronger and more honest than rejecting one alternative | Coefficient equations force `f'=1/n`, `f''=-1/n^2`, while constants remain invisible |
| B | Compute curvature from Christoffels/Riemann and `Box` independently from the volume-form divergence | Declared metric and tensor definitions | none | Supplies construction independence for the master identity | Both routes reproduce canonical closed forms for arbitrary symbolic `n(x)` |
| C | Use `n=1+alpha*x` to accept `log(n)` and reject `n`, then expand the TF relation | Declared metric and one concrete profile | profile slope `alpha` | Useful sensitivity check but cannot establish uniqueness | General coefficient route must strictly dominate the single-profile guard |

## Selection Criteria and Blinding
The frozen order is arbitrary-profile exactness, uniqueness modulo a named symmetry, construction independence, assumption economy, strict dimensional scope, mutation sensitivity, then API clarity. Candidate A is selected because it proves the load-bearing uniqueness statement rather than inferring it from a single rejected alternative. Candidate B is the independent review route. Candidate C remains a counterexample and weak-field sensitivity route.

## Proposed Claim Delta
P004 proposes two additive root-sector claims and no challenge or supersession.

| Claim | Exact statement | Dependencies | Oracle | Consumers |
| --- | --- | --- | --- | --- |
| C-OG-001 | The declared 1+1 metric has `R=c0^2(n n''-2n'^2)/n^3`; `Box log n=R`; all composition solutions are `log n+C` | none; conditional on the declared metric | exact SymPy coefficient matching plus independent tensor reconstruction | optical geodesics, 1+1 dilaton, later gravity bridge candidates |
| C-OG-002 | Conditional on `n=(1+2Phi/c0^2)^-1`, the dilaton has leading term `-2Phi/c0^2` and slow geodesic acceleration tends to `-Phi_x` | C-OG-001 plus the named constitutive import | exact SymPy substitution, series, limits, and independent Christoffel route | weak-field drift consumers only |

## Implementation and Oracle Plan
A pure `src/substrate_framework/optical_geometry.py` module will expose the metric, scalar curvature, static scalar wave operator, dilaton, TF index map, and slow geodesic acceleration. No simulation or print occurs on import.

The main verifier will derive the determinant, divergence-form wave operator, arbitrary-profile curvature identity, general-composition coefficient equations, additive-constant symmetry, TF expansion, exact drift substitution, and weak-field limit. It will reject scale, linear-in-index, sign, and factor mutations. The independent review will reconstruct Christoffels and Ricci from definitions without importing the canonical closed curvature or box APIs, compare nontrivial profiles, and exhibit a 3+1 counterexample as a scope guard rather than a promoted no-go.

## Attempts and Continuation
Attempt `0001` implements Candidate A. Tensor simplification failures trigger explicit derivative-basis coefficient collection, not a weaker pointwise claim. If coefficient matching admits another nonconstant branch, the uniqueness statement is corrected before review while the user's positive identity objective remains. Failure of the conditional drift map activates a direct geodesic expansion before reconsidering the constitutive import.

## Debt Ledger
P004 starts with four dischargeable debts.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| T1B overstates uniqueness by rejecting only `f(n)=n` | General profile-jet matching proves exactly `f(n)=log(n)+C`, and the additive constant passes as a symmetry | discharged |
| The TF index-potential relation is imported | C-OG-002, its APIs, review, and T1B disposition all state the conditional import | discharged |
| The Poisson coefficient lacks a fully specified sourced dilaton equation | The registry excludes it and T1B's partial remainder preserves it | discharged |
| A 1+1 identity could be narrated as 3+1 gravity | The independent tensor review rejects the identity on an explicit 3+1 radial metric and every claim quantifier remains 1+1 | discharged |

## Review and Promotion Plan
Each claim receives a separate review entry. Review will inspect the metric convention, independent tensor construction, uniqueness quantifiers, additive symmetry, conditional import, exact and weak limits, mutations, dimensional scope, and consumer map.

Promotion will freeze P004, add only accepted claim statements, create a pinned release, regenerate docs and accepted memory, update T1B to `partially_migrated` with its sourced-Poisson and 3+1 remainder explicit, regenerate the migration queue, replay affected consumers, and run one full workflow validation.

## Results and Promotion
Attempt `0001` passed 21 exact checks. The independent tensor construction passed six checks, reconstructing curvature, the scalar wave operator, and the connection from definitions and rejecting a 3+1 overextension. The general coefficient proof corrected T1B's uniqueness statement to `log(n)+C`; no constant was incorrectly treated as a failed mutation.

`C-OG-001` and conditional `C-OG-002` were individually accepted as `symbolic_verified`, `compatible_extension`, and `active` in `v0.4.0`. T1B is now partially migrated, with its matter-sourced Poisson normalization and lack of a positive 3+1 construction preserved as explicit remaining scope.

## Done Gate
P004 is complete. Both positive conditional objects are importable and independently verified, each claim is reviewed on four axes, T1B's accepted and remaining subclaims are separated, all affected paths replay, and the campaign debt ledger is empty.
