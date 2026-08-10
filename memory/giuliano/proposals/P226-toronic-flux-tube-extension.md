---
description: 'P226: structural flat-connection obstruction, validated minimal flux background, and Minkowski flux-tube ensemble analysis (issue #28)'
author: giuliano
created: '2026-08-10T18:05:00+00:00'
updated: '2026-08-10T18:05:00+00:00'
tags:
- substrate-framework
- campaign-proposal
- toronic-casimir
category: proposals
confidence: working
status: active
---

## Question and Positive Deliverable
Once fundamental (doublet) matter is included on the toronic-condensate
preprint's Sec. 10 bundle, does a flat connection exist, what is the minimal
background's classical energy, and can the single-tube structure extend to a
Lorentz-invariant static tube ensemble in Minkowski space? The deliverables
are the modules `toron_bundle` and `flux_tube_ensemble` with structural
oracles, split from PR #27 per the 2026-08-10 harvest review.

## Base Release and Provenance
Accepted release v0.159.0; stacked on the issue #26 audit branch head
bf68ee1f (PR #27, narrowed core). Preprint PDF: durable attachment on issue
#26 (comment 5243581613); bundle construction is Eqs. (106)-(120).

## Invariants, Conventions, and Allowed Imports
No edits to accepted claims or to the #27 core beyond reuse. Structural gate
from the review: no hard-coded booleans; construction claims need
construction-level checks; measure statements need derived measures.
Conventions: T_a = sigma_a/2; U(1)_Y coupling g' with Y = 1/2 for doublets.

## Candidate Preregistration
Two flux carriers are preregistered so the energy estimate does not depend
on an unexamined case split.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Exact cocycle + kernel membership for the obstruction; su(2) minimal flux representative | Sec. 10 transition functions as declared | g, g', L | no flat connection; positive classical energy | wrong-kernel and no-quotient mutations; plaquette/winding checks |
| B | u(1)_Y-carried flux representative | same bundle, hypercharge flux | g', L | higher classical energy at SM couplings | energy comparison; cocycle phase = +1 permits either carrier |

## Selection Criteria and Blinding
Exact symbolic results first; lattice evidence corroborates and must pass
construction-level checks (plaquette uniformity, winding, gauge covariance,
refinement). The two flux carriers are both enumerated so the energy
estimate is not case-split dependent.

## Proposed Claim Delta
None. All symbols conditional, unpromoted, linked to issue #28.

## Implementation and Oracle Plan
The campaign ships two modules with the following importable APIs.

`toron_bundle`: `transition_function_cocycle`, `cover_holonomy_commutator`,
`quotient_kernel`, `flat_toron_connection_exists`,
`flux_background_candidates`, `minimal_flux_classical_energy_density`,
`uniform_flux_links`, `plaquette_holonomies`, `cycle_two_holonomy`,
`spectrum_from_links`, `landau_ground_dimensionless`,
`best_constant_twist_residual` (continuous differential-evolution
falsifier). `flux_tube_ensemble`: tube pressures, isotropic w,
orientation average, `timelike_axis_induced_metric`,
`timelike_axis_orbit_volume`, `self_dual_split_norms_constant`,
`oriented_grassmannian_2_4_volume`, `modulus_stationary_point_exists`.
Replay: targeted pytest plus one full `scripts/validate.sh` at the boundary.

## Verdicts (verified results)
1. No flat connection with fundamentals: cocycle (-I,+1) not in the diagonal
   Z2 kernel; mutation controls behave as required.
2. Minimal classical flux energy 2 pi^2/(g^2 L^4) (su(2) carrier), >10x the
   one-loop gauge term at SM couplings; positive and unavoidable.
3. The lattice constant-curvature representative passes plaquette/winding/
   gauge-covariance/refinement checks; ground converges to 1/(4 pi); no
   constant-twist fit under continuous optimization.
4. Ensemble: w = +1/3 exact; derived H^3 orbit volume infinite; derived
   Gr~(2,4) volume 16 pi^2 finite (Euclidean, not a static vacuum); no
   modulus stationary point under either sign.

## Attempts and Continuation
Append-only attempt record; all first-pass routes were refuted by the
harvest review and repaired as listed.

| Attempt | Route | Verdict | Mechanism | Next |
| --- | --- | --- | --- | --- |
| 0001 | boolean obstruction (PR #27 v1) | refuted by review | no structural content | exact cocycle (landed) |
| 0002 | U(1) "uniform-flux" links (PR #27 v1) | refuted by plaquette check | zero net U(1) flux | su(2) Landau links (landed) |
| 0003 | grid no-twist scan | refuted by review | not continuous | differential evolution (landed) |
| 0004 | stand-in orbit integrals | refuted by review | measures not derived | induced-metric derivation (landed) |

## Debt Ledger
Campaign debt tracked here; both rows are recorded frontiers, not
merged-scope debt.

| Debt | Introduced by | Why it is real | Discharge artifact | Status |
| --- | --- | --- | --- | --- |
| one-loop on the flux background uncomputed | scope | needs a renormalization condition on the magnetic spectrum | issue #28 frontier | open frontier |
| magnetic tower shape beyond the ground state unidentified analytically | lattice evidence | not needed for the obstruction or no-twist verdict | frontier: analytic magnetic spectrum on the Z2-quotient bundle | open frontier |

## Review and Promotion Plan
No claim promotion. Reviewer focus: the mutation sensitivity of the
obstruction, the construction-level lattice checks, and the derived
measures. Stacked PR base: research/toronic-casimir-verification; retarget
to main when PR #27 merges.

## Done Gate
Complete when the stacked PR is open with targeted tests green and one clean
full-suite validation recorded. Frontiers above stay on issue #28.
