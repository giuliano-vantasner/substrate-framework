---
description: Derive axial Ward identities and audit PG4 Goldberger-Treiman claims
author: vantasner
created: '2026-08-02T21:15:00Z'
updated: '2026-08-02T22:00:00Z'
tags:
- substrate-framework
- campaign-proposal
- axial-ward-identity
- migration-PG4
category: proposals
confidence: established
status: archived
---
# P063 PG4 Axial Ward-Identity and Goldberger--Treiman Audit

## Question and Positive Deliverable

P063 must deliver an importable, convention-explicit account of an on-shell
nucleon axial-current decomposition and divergence, its pion-pole residue and
regular remainder, the distinct zero-momentum, pole-point, and chiral limits,
and the parameter ledger of any conditional Goldberger--Treiman relation. It
must then determine whether PG4 constructs those objects or imports PCAC,
pion-pole dominance, quantum states, and physical coupling dictionaries. A
source error or unsupported physical narrative cannot complete the campaign;
the positive Ward-identity, pole/remainder, and identifiability objects remain
required.

## Base Release and Provenance

The accepted base is `v0.56.0` at framework commit `756c264`, whose scientific
transaction is `60933b1`. The pinned predecessor is `substrate@6d1f4e0`; PG4
is `/home/dan/substrate/merged-framework/bridges/phase-18/bridge_PG4_goldberger_treiman.py`
with independently verified SHA-256
`e13e68536d14bedb1c8fa7ec10110172d0a1b73e08ce365863013dc7db66f1e9`.
PG4 is pending in the generated queue and names PG1, S1, and S2 as
dependencies. PG1 maps only conditional C-SYM-001/C-CHI-001 content; S1 and
S2 remain pending. The predecessor checkout is at the pinned commit but has
unrelated later Phase 47/48 and memory artifacts, which remain excluded. The
fresh physics-skill preflight passes seven checks without warnings, the
framework tree was clean before this contract, and git history separates the
v0.56.0 scientific transaction from its effort-memory sync. Memory supplies
only the accepted ceilings and PG4 pointer; every reused fact must be verified
at its source. The queue synopsis necessarily exposes the claimed GT equation,
mass-squared discrepancy, and solve-back, but PG4's executable conventions,
derivation, checks, and detailed outputs remain unopened at this boundary.

## Invariants, Conventions, and Allowed Imports

C-SYM-001 and C-CHI-001 are finite-dimensional classical coordinate-model
theorems and define no quantum current, asymptotic nucleon state, pion pole,
decay constant, or chiral Ward identity. C-CHI-002 and C-GMR-001 retain every
coordinate and free physical input and likewise supply no PCAC or pion-nucleon
coupling. Those ceilings remain invariant. A single form-factor Ward identity
constrains only a combination of functions, and algebraically solving a
conditional equation for one symbol does not predict it.

Allowed mathematics is exact Lorentz/Dirac algebra with one explicitly frozen
metric, gamma-five, momentum-transfer, generator, and on-shell spinor
convention; exact rational-function residues, limits, series, dimensions, and
free-symbol analysis; and declared form-factor, PCAC, interpolating-field, and
pion-nucleon vertex premises whose provenance remains visible. Audited primary
literature may establish the conventional scope of GT and its discrepancy but
cannot turn it into a framework derivation. Pending S1/S2, measured or fitted
couplings and masses, a physical pion/nucleon dictionary, QCD dynamics, and a
substrate map are forbidden inputs.

## Candidate Preregistration

The candidate set is frozen before opening PG4's executable internals.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal PG4 reproduction | Every headline noun resolves to an evaluated current, pole, state convention, limit, and dependency | Source symbols only | Narrow algebra may survive while PCAC, pole dominance, couplings, states, and physical identity enter by declaration | Hash-pinned execution, data-flow audit, and load-bearing mutations |
| B | General on-shell form-factor Ward identity | Lorentz covariance, on-shell equal-mass spinors, explicit gamma and isospin conventions | `G_A(q^2)`, `G_P(q^2)`, mass, momentum transfer | Divergence fixes one convention-dependent linear combination and no individual form factor | Direct Dirac-equation derivation and independent explicit-gamma spinor checks |
| C | Pion pole plus analytic remainder | Candidate B plus declared PCAC/interpolating field/vertex and an analytic remainder | Pole residue, pion mass, decay scale, coupling form factor, remainder | GT follows only under explicit normalization, regularity, and limit premises; discrepancy separates pole-point, zero-point, and regular terms | Exact residue and series plus noncommuting-limit, sign, pole, and remainder mutations |
| D | Declared chiral effective model | A specified nucleon/pion action and its transformation law | Yukawa or pseudovector coupling, vacuum scale, mass, optional axial coefficient | A model-specific GT relation may follow naturally, but its field ontology and parameters remain declared | Noether-current or field-redefinition derivation and wrong-transformation counterexample |
| E | Identifiability ledger | Only the conditional Ward/GT equations are supplied | All masses, scales, couplings, form factors, and remainder values | Continuous parameter families preserve the equation, so solve-back cannot establish prediction or physical identity | Exact nullspace/rescaling families and mutation-sensitive residuals |

## Selection Criteria and Blinding

Selection is ordered by accepted dependency closure, exact convention and
dimension consistency, explicit separation of current/pole/remainder/state
premises, assumption and parameter economy, correct zero-momentum/pole/chiral
limits, mutation sensitivity, and independent rederivation. Numerical
agreement with phenomenological `g_A`, `g_piNN`, `F_pi`, `M_N`, or a reported
discrepancy is excluded from selection. The synopsis-exposed GT equation and
factor language cannot select signs, generator factors, pole form, limits, or
claim boundaries. These objects and criteria are frozen before source access.

## Proposed Claim Delta

Provisional C-WID-001 may state an exact conditional on-shell axial form-
factor divergence and its pole-plus-regular decomposition in explicitly
declared conventions. Provisional C-GTR-001 may state only the exact
conditional GT limit, discrepancy decomposition, order-of-limits guards, and
free-parameter/solve-back ledger. Provisional C-EFT-002 may state a declared-
model Noether relation only if Candidate D supplies a smaller natural closure
than merely assuming the target. No claim may assert a framework-derived
physical pion or nucleon, measured coupling, QCD PCAC, exact phenomenological
GT equality, or substrate realization. Claims will be reviewed individually
and may be narrowed or rejected without blanket promotion.

## Implementation and Oracle Plan

A pure additive module under `src/substrate_framework/` will expose exact
convention data, axial-divergence coefficients, pole/remainder decompositions,
limits, residues, discrepancy terms, and identifiability families. It will
print nothing and execute no numeric process on import. If the effective-model
candidate survives, its declared action and transformations will be separate
APIs rather than hidden premises in the Ward helper.

SymPy exact algebra is the strongest oracle for gamma anticommutation reduced
to declared on-shell identities, rational residues, substitutions, limits,
series, dimensions, and free-symbol counts. An independent route will use an
explicit gamma-matrix representation and on-shell spinors or an action-level
Noether derivation without importing the canonical evidence object. Mutations
will reverse momentum transfer, gamma-five placement, metric or pole sign,
change the isospin generator between tau and tau/2, alter the factor multiplying
the induced pseudoscalar form factor, add a regular remainder, move the
coupling between q-squared zero and the pion pole, and vary every free scale.
The q-squared-to-zero and pion-mass-to-zero limits will be evaluated in both
orders. Exact checks need no quadrature and no deprecated NumPy integration
alias. GitNexus impact analysis precedes canonical edits; focused exact tests,
claim verifiers, affected consumers, one full workflow gate, and diff checks
close promotion.

## Attempts and Continuation

The append-only ledger contains five attempts before promotion replay.
Attempt 0001 reproduces PG4 and rejects its physical headline while retaining
the conditional residual. Attempt 0002 fixes two structural SymPy comparisons
without changing physics. Attempt 0003 preserves an independent-oracle failure
caused by an unconstrained sign assumption. Attempt 0004 preserves a missing
local binding in the new spinor sign test. Attempt 0005 passes 31 primary, 20
independent, and 11 focused checks. Candidates B, C, and E are selected;
Candidate A is rejected and Candidate D is not promoted because its minimal
model fixes rather than derives a general axial coefficient.

## Debt Ledger

This ledger tracks current and state provenance, gamma/isospin conventions,
on-shell reduction, PCAC and pole assumptions, regular remainders, limit
order, coupling evaluation point, parameter identifiability, physical labels,
independent evidence, consumers, and canonical synchronization.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| PG4's literal equations, checks, imports, and output are unaudited | Hash-check, execute, trace every subclaim to its defining current, state, pole, and limit, and preserve output or failure | discharged by source reproduction, audit, attempt 0001, and source adjudication |
| The positive axial Ward-identity object is not implemented | Derive the on-shell divergence, convention conversions, pole/remainder form, residues, and limits in tested importable APIs | discharged by the canonical axial API and 31 primary plus 20 independent checks |
| PCAC, pole dominance, or a nucleon/pion dictionary may enter as an undeclared premise | Record each as a separate conditional input or reject the physical derivation and preserve the missing closure | discharged by C-WID-001's explicit conditional ceiling and PG4 qualification |
| Factor-of-two, sign, and generator conventions may be mixed | Freeze one complete convention, derive conversions, and require wrong-convention probes to fail | discharged by dimension, explicit-spinor, omitted-scale, and wrong-sign probes |
| Zero-momentum, pole-point, and chiral limits may be conflated | Evaluate all relevant limits and their order, retaining analytic remainder and coupling-point terms | discharged by exact residues, both iterated limits, proportional paths, and coupling-point separation |
| A solve-back or inserted coupling may be mislabeled a prediction | Prove the free-parameter family and distinguish derived residue constraints from invertible bookkeeping | discharged by the rank-one exponent row, three-dimensional kernel, and rescaling families |
| Downstream impact and independent review are unknown | Complete graph impact analysis, independent rederivation, targeted replay, and separate claim reviews | discharged by additive impact analysis, independent review, claim reviews, and targeted replay |
| Registry, release, docs, queue, and memory are unsynchronized | Promote only reviewed claims, regenerate canonical consumers, and empty this campaign ledger | discharged by the v0.57.0 promotion transaction and workflow replay |

## Review and Promotion Plan

C-WID-001 and C-GTR-001 are reviewed separately and accepted at exact
symbolic status. The additive package API, focused tests, immutable campaign,
v0.57.0 release, PG4 qualification, generated queue, documentation, and
accepted memory form one promotion transaction. The source's conditional
algebra survives only inside the explicit premise ceiling; its physical
derivation, discrepancy coefficient, parameter prediction, and guard do not.

## Done Gate

P063 closes with the positive convention-explicit Ward, pole/remainder,
limit-order, discrepancy, and identifiability objects accepted in v0.57.0;
the strongest sensitive oracle, independent route, claim-level reviews,
downstream replay, canonical synchronization, and empty campaign debt all
pass. The parent 218-unit migration effort remains active.
