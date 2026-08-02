---
description: Derive and audit periodic explicit breaking and conditional GMOR algebra
author: vantasner
created: '2026-08-02T12:52:59Z'
updated: '2026-08-02T20:00:00Z'
tags:
- substrate-framework
- campaign-proposal
- explicit-breaking
- migration-PG2
category: proposals
confidence: established
status: archived
---
# P061 PG2 Explicit-Breaking and GMOR Audit

## Question and Positive Deliverable

P061 must deliver an importable exact account of a declared periodic
explicit-breaking potential: its Taylor coefficients, stationary curvature,
generalized quadratic mass relative to a supplied kinetic metric, and exact
SU(2) trace representations in fixed Pauli conventions. It must also expose
the sign, scaling, residual, and free-input ledger of a separately declared
GMOR relation. It must independently decide whether PG2 predicts a physical
pion mass or merely names and reparameterizes supplied coefficients. A source
normalization error, an imported physical dictionary, or a no-go for PG2's
headline cannot complete the campaign; the exact conditional potential and
parameter-identifiability object remains the positive deliverable.

## Base Release and Provenance

The accepted base is `v0.54.0` at framework commit `e637c81`, whose scientific
transaction is `d053f92`. The pinned predecessor is
`substrate@6d1f4e0`; PG2 is
`/home/dan/substrate/merged-framework/bridges/phase-18/bridge_PG2_gmor_pion_mass.py`
with verified SHA-256
`0502a53f65d3bd11a3f17d26d55ed7d67a1e0f61d194b38cd41728873c4a06ad`.
PG2 is pending in the generated queue and names PG1 and S2 as dependencies.
PG1 maps only accepted C-SYM-001 and C-CHI-001 with strict classical,
coordinate-model, and nonphysical ceilings; S2 remains pending and supplies
no premise. The fresh skill preflight passes seven checks without warnings,
the framework tree was clean before this contract was instantiated, and git
history separates the current release transaction from its effort sync.
Memory supplies only the accepted frontier, the PG2 pointer, and the warning
to distinguish supplied coefficients from predictions. The queue synopsis
necessarily exposes a claimed cosine expansion, a trace equality, and GMOR
scaling; PG2's executable equations, conventions, checks, and output remain
unopened at this contract boundary.

## Invariants, Conventions, and Allowed Imports

The accepted C-SG-001 potential is the dimensionless normalized function
`1-cos(phi)` and contains no physical pion coordinate, `F_pi`, condensate,
quark mass, or absolute mass coefficient. C-SYM-001 and C-CHI-001 are
conditional finite-dimensional classical results. In particular, C-CHI-001
does not accept a chiral action or physical breaking mechanism, and its SU(2)
coordinate scale `F` is declared rather than identified with a measured decay
constant. Those ceilings remain invariant.

Allowed mathematics is exact calculus and Taylor expansion, real
finite-dimensional quadratic forms, explicit Pauli matrices and traces,
positive kinetic metrics supplied in the same coordinates, exact dimensions,
and algebraic parameter-identifiability analysis. C-SG-001, C-SYM-001, and
C-CHI-001 may be composed only within their accepted assumptions. Primary
GMOR literature may establish the external relation's actual hypotheses and
sign conventions, but citation cannot make it a framework derivation.
Pending S2, phenomenological pion or quark masses, a fitted condensate,
physical `F_pi`, QCD dynamics, and a substrate-to-pion map are forbidden
inputs.

## Candidate Preregistration

The candidate set is frozen before opening PG2's executable internals.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal PG2 reproduction | Every headline noun resolves to computed action, coordinate, kinetic metric, coefficient provenance, and physical map | Source symbols only | Exact algebra may survive while prediction and identity claims enter through names or declarations | Hash-pinned execution, data-flow audit, and coefficient/name mutations |
| B | General periodic potential | Declared `V=A*(1-cos(phi/F))`, real coordinate, nonzero scale, and optional positive scalar kinetic coefficient | `A`, `F`, `K` | Vacuum curvature is `A/F^2`, quartic coefficient is `-A/(24*F^4)`, and generalized quadratic mass is `A/(K*F^2)`; writing `A=m^2*F^2` makes `m` an input unless `A` and `F` are independently fixed | Direct derivatives and series plus amplitude, scale, sign, kinetic, and coordinate-rescaling mutations |
| C | Explicit SU(2) trace forms | `U=exp(i*tau_3*phi/F)`, standard Pauli trace, and declared identity matrix | Trace prefactor, sign, additive constant | `Tr(U-I)` and `Tr(U+U^dagger-2I)` have different fixed numerical factors; only the corresponding derived prefactor represents a chosen cosine potential | Exact matrix exponential/characteristic-polynomial route and independent eigenvalue trace route |
| D | Locally matched breaking competitors | Periodic potential, accepted conditional O(4) linear tilt, and a quadratic local model, each in explicit coordinates | Their independent amplitudes and vacuum data | Distinct global potentials can share one positive vacuum curvature, so a local mass term cannot select the breaking mechanism | Match Hessians, then distinguish periodicity, higher derivatives, stationary branches, and large-field behavior |
| E | Conditional GMOR ledger | Separately declared relation, positive squared scale, stated signs, and no empirical values | Quark-mass sum, condensate, scale, mass squared | The relation solves one coordinate from three independent inputs and has exact scaling and sign consequences but predicts no number or physical map without those inputs | Symbolic residual, dimensional check, zero-mass and sign limits, and independent rescaling family |

## Selection Criteria and Blinding

Selection is ordered by compatibility with accepted claim ceilings, exact
coefficient/sign/trace/kinetic consistency, explicit dimensions and field
coordinates, assumption and parameter economy, correct limiting behavior,
mutation sensitivity, and independent rederivation. Numerical agreement with
a physical pion mass or another comparator is forbidden as a selector. The
inventory-exposed formulas cannot fix a prefactor, sign, kinetic convention,
condensate, decay scale, or field dictionary. Candidate equations, mutations,
and ceilings are frozen in this contract before PG2's executable is opened.

## Proposed Claim Delta

Provisional C-BRK-001 may state the exact periodic-potential series,
stationary curvature, generalized mass relative to a supplied positive
kinetic coefficient, coordinate-rescaling covariance, and the theorem that a
matched local curvature does not uniquely identify a global breaking
potential. It may compose with C-SG-001 only as a declared rescaling of its
normalized cosine, never as a derived physical map.

Provisional C-CHI-002 may state convention-explicit SU(2) trace, kinetic,
curvature, and generalized-mass identities. Provisional C-GMR-001 may state
only the algebraic sign, scaling, dimensions, and free-parameter content of a
separately declared GMOR-form relation. Neither may claim that the framework
derives a chiral sector or GMOR, select a condensate or `F_pi`, identify the
coordinate as a physical pion, predict a mass, or import pending S2. Claims
will be reviewed individually; any provisional claim may be narrowed or
rejected without blanket promotion.

## Implementation and Oracle Plan

A pure additive module under `src/substrate_framework/` will expose the
periodic potential, its exact derivative/Hessian/series evidence, scalar
generalized quadratic mass, explicit Pauli trace evidence for alternative
trace forms, locally matched competing potentials, and a conditional-GMOR
residual/parameter ledger. Imports will print nothing and run no simulations.
The existing C-CHI-001 kinetic-metric API will be reused rather than copied.

SymPy exact algebra is the strongest oracle because the obligations are
finite derivatives, Taylor coefficients, matrix exponentials/traces,
substitutions, dimensions, and scaling identities. The primary route will
derive objects from supplied parameters rather than expected constants. An
independent review will obtain the trace from the eigenvalues of the Pauli
generator and obtain Taylor coefficients from derivatives at the vacuum,
without importing the canonical evidence helper. Load-bearing mutations will
change amplitude, sign, scale, kinetic coefficient, trace prefactor, generator
normalization, condensate sign, and one GMOR input; wrong-convention probes
must fail the relevant verdict. Matched-curvature counterexamples will have
equal Hessians but different fourth derivatives or periodicity. GitNexus
impact analysis will precede canonical edits. Focused tests, primary and
independent verifiers, affected consumers, one full `scripts/validate.sh`
promotion gate, and `git diff --check` will close validation. No numerical
quadrature, simulation, or `np.trapz` compatibility path is planned because
exact algebra decides the claim; if later numeric integration is genuinely
needed, current code will use `numpy.trapezoid` with an explicit convergence
oracle.

## Attempts and Continuation

The append-only ledger contains three completed attempts. Attempt 0001
reproduces PG2's four-check tally and preserves its exact Taylor, trace-shape,
and conditional-scaling subclaims while rejecting the physical route. It
exposes the missing kinetic metric, factor-four trace switch, inconsistent
decay-constant conversion, and free-input GMOR premise. Attempt 0002
implements Candidates B through E canonically and passes ten focused tests;
its initial composite-factor derivative failure is preserved and repaired by
deriving monomial sensitivities from independent internal slots. Attempt 0003
independently derives the Taylor coefficients, Pauli-eigenvalue trace,
kinetic/curvature ratio, factor-four mismatch, potential counterexample, and
conditional GMOR ledger without importing the canonical module. It passes 30
checks. Candidates B through E are selected; A remains rejected as the
advertised physical mechanism.

## Debt Ledger

This ledger tracks source provenance, potential and field conventions,
kinetic normalization, trace prefactors, Taylor coefficients, parameter
identifiability, GMOR imports and signs, physical-interpretation ceilings,
independent evidence, consumers, and canonical synchronization.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| PG2's literal equations, checks, imports, and output are unaudited | Hash-check, execute, trace every subclaim to its defining object, and preserve output or failure | discharged by source reproduction, audit, and attempt 0001 |
| The positive periodic-potential object is not implemented | Derive potential, derivatives, series, curvature, kinetic normalization, limits, and coordinate-rescaling behavior in a tested importable API | discharged by `explicit_breaking.py`, focused tests, and attempts 0002/0003 |
| Trace normalization and sign may be copied from the source target | Derive every candidate trace from explicit matrices and independently from generator eigenvalues; make prefactors and constants explicit | discharged by canonical group-element and independent eigenvalue routes |
| A supplied coefficient may be mislabeled a predicted mass | Expose amplitude, scale, kinetic coefficient, field coordinate, and invertible reparameterization with sensitive mutations | discharged by C-BRK-001/C-CHI-002 and the quarter-kinetic counterexample |
| Local quadratic agreement may be mislabeled mechanism identity | Construct at least two globally inequivalent breaking potentials with matched vacuum curvature and distinguish higher derivatives or periodicity | discharged by the matched cosine/quadratic counterexample |
| GMOR may enter without provenance, dimensions, or free-input accounting | Audit primary scope, encode it only as a declared conditional relation, and preserve every independent input and sign premise | discharged by primary provenance and C-GMR-001's convention/free-input ledger |
| Pending S2 or physical comparator data may leak into selection | Keep accepted closure within C-SG-001/C-SYM-001/C-CHI-001 unless another accepted claim is demonstrably required | discharged; no pending unit or comparator enters any accepted dependency |
| Downstream impact and independent evidence are unknown | Complete graph impact analysis, independent rederivation, targeted replay, and claim-level source adjudication | discharged by LOW graph risk, 30 independent checks, and separate claim reviews |
| Registry, release, docs, migration queue, and durable memory are unsynchronized | Review claims individually, regenerate canonical consumers, and empty this campaign ledger | discharged by the v0.55.0 promotion transaction and canonical generators |

## Review and Promotion Plan

C-BRK-001, C-CHI-002, and C-GMR-001 received separate reviews over raw
derivatives, trace matrices, kinetic metrics, sign and dimension conventions,
free-input scaling, mutations, primary provenance, and PG2 data flow. All
three exact conditional claims move into the package and release `v0.55.0`
with generated docs and accepted memory. PG2 is qualified because its exact
declared algebra survives while its trace normalization, derived-GMOR,
physical-pion, prediction, and substrate narratives do not. The editable
migration disposition is the only hand-authored queue input; the queue is
regenerated mechanically.

## Done Gate

P061 closes with C-BRK-001, C-CHI-002, and C-GMR-001 accepted in `v0.55.0`
and PG2 qualified after the positive APIs, 36 primary and 30 independent
checks, focused and full replay, claim-level review, regenerated consumers,
and empty campaign debt ledger pass. The parent corpus migration remains
active because 159 queue units remain pending.
