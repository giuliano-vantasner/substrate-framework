---
description: Derive and audit the exact SU3 winding current and hedgehog charge
author: vantasner
created: '2026-08-02T10:19:52Z'
updated: '2026-08-02T17:00:00Z'
tags:
- substrate-framework
- campaign-proposal
- su3-winding-current
- migration-WZ3
category: proposals
confidence: established
status: archived
---
# P058 WZ3 SU(3) Winding-Current Audit

## Question and Positive Deliverable

P058 must deliver a reusable exact construction of the normalized SU(3)
winding three-form, its identically conserved four-dimensional topological
current, and the charge of a smooth embedded SU(2) hedgehog under explicit
orientation and boundary hypotheses. It must separately determine whether
accepted ungauged WZW authority derives that current as a U(1) response,
identifies its integer with physical baryon number, or fixes a coefficient to
`N_c`. Reproducing a source tally or documenting a missing gauging premise does
not complete the campaign; Candidates B and C continue to the positive
mathematical object even if Candidate A or D fails.

## Base Release and Provenance

The accepted base is `v0.51.0` at framework commit `8f5850d`, whose scientific
transaction is `45e2fe9`. The pinned predecessor is `substrate@6d1f4e0`; WZ3
is `/home/dan/substrate/merged-framework/bridges/phase-17/bridge_WZ3_goldstone_wilczek_baryon_current.py`
with verified SHA-256
`30da2ac41a0d46c48bd4e1b9733c3712d0b6c1c9b4838f1a1df3c4db22cc3569`.
The predecessor worktree is dirty with later Phase 47/48 and memory artifacts,
so only the hash-pinned WZ3 file belongs to this source unit. WZ3 is pending;
its candidate dependencies NC1, S2, and S3 are also pending and supply no
premises. WZ1 and WZ2 are qualified only through C-WZW-001 and C-WZW-002.
The fresh skill preflight passed seven checks without warnings, framework git
was clean at the contract boundary, and memory supplied only the parent
frontier and accepted-claim pointers. The inventory synopsis necessarily
revealed WZ3's displayed coefficient and `n=N_c=3` conclusion; the executable,
internal derivation, profile, arithmetic, and check data flow remain unopened.

## Invariants, Conventions, and Allowed Imports

The fundamental matrices and trace use C-LIE-001's `T_a=lambda_a/2`
convention. For a smooth `U` in SU(3), the left current is
`L_mu=U^dagger*partial_mu U`; spacetime and spatial coordinates use
`epsilon^(0123)=+1` and the induced `(x,y,z)` orientation. Alternating traces
are unnormalized sums, while coordinate differential-form coefficients retain
their explicit factorial conventions. The campaign will not silently exchange
left and right currents, Hermitian and anti-Hermitian currents, or upper and
lower epsilon tensors.

Allowed imports are Maurer-Cartan calculus, smooth pullback and Stokes,
one-point compactification under declared boundary behavior, Brouwer degree,
and oriented sphere volume, plus an explicit Pauli-matrix SU(2) embedding whose
trace factors are recomputed. C-WZW-001 and C-WZW-002 may supply only their
accepted ungauged five-form, sphere period, and conditional filling lattice.
They do not supply a gauge field or descent functional. C-TOP-001 supplies only
an abstract parity character. No S2/S3 baryon ledger, NC1 color count, physical
quark assignment, experimental baryon charge, or anomaly coefficient is an
allowed derivation input.

## Candidate Preregistration

The candidate set is fixed before opening WZ3's executable internals.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal WZ3 reproduction | Every printed formula and dependency must be traced to actual operations | Source profile and constants only | May reproduce unit charges while omitting the gauged functional or inserting the desired integer | Hash-pinned run, AST/data-flow audit, and load-bearing mutations |
| B | Trace-three/degree construction | Smooth SU(3) map and standard degree theorem | No fitted parameter | Gives a metric-free closed current and integer compactified-space charge without physical semantics | Exact Maurer-Cartan expansion, explicit SU(2) generator period, orientation reversal, and trivial-map guards |
| C | Embedded hedgehog construction | Smooth radial profile, regular origin, constant vacuum at infinity | Boundary values and profile shape | Gives a derived radial density and boundary-only integer when endpoints meet the winding conditions | Explicit matrix differentiation, angular trace reduction, analytic radial integral, profile deformation, and boundary mutations |
| D | Conditional external-source coupling | A separately declared one-form source coupling `q*A wedge omega_3` | Free real coupling `q` | Its functional response is the topological current and its gauge variation is a boundary term, but accepted ungauged WZW data need not fix `q` | Functional variation, conservation, coupling mutation, and dependency audit for any WZW or `N_c` identification |

## Selection Criteria and Blinding

Selection is ordered by accepted-convention compatibility, actual off-shell
closure, independent period and hedgehog normalizations, absence of imported
answers, clean separation of mathematical and physical semantics, sensitive
orientation/normalization/boundary mutations, and minimal assumptions. The
inventory-exposed coefficient and `N_c=3` claim cannot select a sign,
normalization, embedding, or candidate. Only after the current convention,
generator integral, boundary formula, conservation oracle, mutation set, and
interpretation ceiling are frozen here may the source implementation be read.

## Proposed Claim Delta

Provisional C-TOP-002 may assert that a precisely normalized trace-three form
on SU(3) is closed, that its Hodge-dual coordinate current is identically
conserved for smooth maps, and that an explicit embedded SU(2) hedgehog has a
derived radial density whose charge is a boundary expression and an integer
under integer endpoint conditions. The claim will state the orientation and
degree sign explicitly. A conditional declared coupling to an external
one-form may be recorded if useful, but it cannot be called a derivation from
the accepted ungauged WZW term.

The claim cannot identify the integer with a physical baryon, assert that a
U(1) variation of U produces it, derive a gauged WZW action, fix `N_c`, establish
an electromagnetic anomaly, select representations, or connect the current to
substrate dynamics. Direct consumers include WZ3, WZ4, QCD7, MK2.2, MK5, and
any later unit that cites WZ3's baryon or anomaly conclusions; only consumers
whose dependency closure is affected will be replayed now.

## Implementation and Oracle Plan

Pure canonical APIs under `src/substrate_framework/` will expose the exact
SU(2)-in-SU(3) map or Maurer-Cartan values, the normalized trace-three current,
the hedgehog radial density, and its boundary charge. Imports perform no
integration or printing. SymPy exact matrix algebra fits unitarity,
determinant, trace normalization, Maurer-Cartan closure, epsilon expansion,
radial density, boundary antiderivative, and orientation changes. A finite
Chevalley-Eilenberg closure check or direct full graded expansion must evaluate
the actual trace-three cochain rather than a literal predicate.

The independent route will rederive the SU(2) generator integral using the
unit-quaternion S3 map and boundary orientation without calling the canonical
current helper, while the hedgehog route will derive and integrate the radial
density separately. If numerical quadrature is used, it is regression evidence
only: the profile, domain, floating precision, quadrature rule, sample or order
sequence, stopping status, and scale-relative error must be declared, and the
current NumPy API is `np.trapezoid` rather than the removed `np.trapz` alias.
Mutations reverse epsilon orientation, change the `1/(24*pi^2)` normalization,
switch a left-current sign or trace convention, use a constant map, perturb
unitarity, break origin/asymptotic endpoint conditions, and replace an integer
endpoint by a noninteger one. A source-coupling response must fail when its
coefficient or conservation premise changes.

## Attempts and Continuation

Four append-only attempts complete P058. Attempt 0001 preserves the native
`np.trapz` failure, compatibility replay, source sign discontinuity, missing
gauged variation, and circular anomaly inputs. Attempt 0002 selects Candidates
B and C and passes exact trace-three cohomology, generator degree and period,
current normalization, conservation, and hedgehog charge. Attempt 0003
independently rebuilds the construction, preserves an initial representation-
oracle failure, then passes ten exact and `np.trapezoid` regression checks.
Attempt 0004 retains Candidate D only as conditional external-source coupling
algebra with a free coefficient; it is not a WZW derivation.

## Debt Ledger

This ledger tracks source provenance, current and orientation conventions,
three-form closure, generator normalization, hedgehog regularity and charge,
response-versus-topology semantics, physical interpretations, independent
evidence, consumers, and canonical synchronization.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| WZ3's literal operations, inputs, dependencies, environment behavior, and tally are unaudited | Hash-check, execute, trace each claim to its computation, and preserve output or failure | discharged by attempt 0001 and source reproduction |
| Trace-three normalization and orientation may hide a sign, factorial, or representation factor | Derive the explicit SU(2) generator period and pass sign/scale/current-convention mutations | discharged by attempts 0002/0003 and fixed-sign APIs |
| Off-shell conservation may be asserted without expanding the Maurer-Cartan and graded-cyclic terms | Evaluate the actual differential or coordinate divergence with all terms accounted for | discharged by exact CE and full graded/cyclic expansion |
| Hedgehog charge may be copied from an expected unit or depend on a special fitted profile | Derive the density from matrices, integrate analytically from boundaries, and test profile and endpoint mutations | discharged by independent Pauli trace, boundary theorem, and scale-deformation regression |
| A topological current may be mislabeled a U(1), Noether, WZW-response, or physical baryon current | Audit each construction and its required action/source transformation separately | discharged by C-TOP-002's interpretation ceiling and rejected Candidate D linkage |
| The claimed n=N_c=3 and anomaly link may import pending NC1/S2/S3 or an undeclared electromagnetic charge matrix | Inventory all inputs and exclude or separately govern unsupported physics | discharged by source audit and anomaly-consistent charge counterexample |
| Independent evidence and downstream impact are unknown | Complete independent period/charge derivation, impact analysis, and targeted consumer replay | discharged by attempt 0003, LOW graph impact, and focused replay |
| Registry, release, generated docs, migration queue, and durable memory are unsynchronized | Review claim by claim, adjudicate WZ3, regenerate canonical consumers, and empty this ledger | discharged by v0.52.0 promotion synchronization |

## Review and Promotion Plan

The trace-three closure, generator normalization, current conservation,
hedgehog density, charge, conditional response, and every physical
interpretation received separate claim-level decisions. Independent review
reimplemented the generator and hedgehog normalization without canonical WZW
helpers. C-TOP-002 is accepted in v0.52.0, while WZ3 is qualified with every
gauged-WZW, baryon, anomaly, and color subclaim preserved as unaccepted
evidence. Reusable logic and tests are canonical, and generated consumers are
synchronized before the promotion commit.

## Done Gate

P058 is accepted in v0.52.0. The exact winding-current object, independent
degree and period normalization, hedgehog boundary charge, source
adjudication, sensitivity, consumer replay, canonical synchronization, and
empty campaign debt ledger pass. The parent migration remains active and
advances to WZ4 until every queue unit is terminal.
