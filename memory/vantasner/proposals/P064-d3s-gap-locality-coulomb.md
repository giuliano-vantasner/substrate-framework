---
description: Derive massive-kernel locality and audit D3S Coulomb selection
author: vantasner
created: '2026-08-02T22:30:00Z'
updated: '2026-08-02T23:40:00Z'
tags:
- substrate-framework
- campaign-proposal
- derivative-expansion
- migration-D3S
category: proposals
confidence: established
status: archived
---
# P064 D3S Gap, Locality, and Coulomb Audit

## Question and Positive Deliverable

P064 must deliver an importable, convention-explicit account of the exact
low-momentum expansion of a declared massive polarization kernel, a more
general gapped spectral expansion with all moment premises visible, the
leading-power classification of an inverse propagator with optional
fractional terms, and the corresponding conditional real-space Riesz Green
kernel. It must then decide whether D3S constructs those objects from accepted
framework claims or imports the loop integrand, charged ontology, gauge
kinetic term, dimension, and Coulomb dictionary. Failure of D3S's headline
cannot close the campaign; the positive kernel and exponent ledgers remain
required.

## Base Release and Provenance

The accepted base is `v0.57.0` at framework commit `36bf559`, whose scientific
transaction is `42105b1`. The pinned predecessor is `substrate@6d1f4e0`; D3S
is `/home/dan/substrate/merged-framework/bridges/phase-19/bridge_D3S_coulomb_from_sg.py`
with independently verified SHA-256
`a5ff9c760cf8776115881d7a2e5e86c562cdf461f61f36784ff95c6381d24d71`.
D3S is pending in the generated queue and names EM1, EM2, EM3, EM5, EM6,
EM7, P3D1, and QCD5. EM1, EM2, EM6, and P3D1 map only qualified accepted
content; EM3, EM5, EM7, and QCD5 remain pending. Their bridge results supply
no premise. The predecessor checkout is at the pinned commit but contains
unrelated Phase 47/48 and memory artifacts, which remain excluded. The fresh
physics-skill preflight passes seven checks, and history separates v0.57.0
science from effort synchronization. Memory found only the active frontier
and old warnings that EM5/EM7 are pending; every scientific fact was
reverified at source. After freezing the contract, the hash-pinned D3S
executable was opened, reproduced with all 13 source checks passing, and
audited check by check.

## Invariants, Conventions, and Allowed Imports

C-SG-011 supplies a dimensionless small-amplitude massive Klein--Gordon limit
of the normalized real sine-Gordon equation. It does not supply a charged
loop field, physical mass, polarization tensor, current-current correlator,
or map from 1+1 to a different dimension. C-GAU-001 supplies local U1
covariance and curvature but explicitly leaves every gauge kinetic
coefficient, Maxwell equation, photon, force, and electromagnetic dictionary
unconstrained. C-RGE-001/002 are conditional running ledgers, not an abelian
polarization derivation. Those ceilings remain invariant.

Allowed mathematics is exact rational-function and series analysis; beta,
gamma, Schwinger-parameter, and Fourier integrals under declared convergence
domains; leading-power and dimension bookkeeping; and separately declared
positive masses, coefficients, spectral weights, inverse kernels, and spatial
dimension. Euclidean `Q^2>=0` and Minkowski continuation must never be mixed.
A Feynman-parameter integrand or spectral density is an explicit conditional
input, not evidence that accepted sine-Gordon dynamics produces it. Pending
EM3/EM5/EM7/QCD5, a bare Maxwell action, charged-particle ontology, physical
Coulomb law, observed dimension, and every fitted normalization are forbidden
inputs.

## Candidate Preregistration

The candidate set is frozen before opening D3S's executable internals.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal D3S reproduction | Every claimed object is constructed and checked | Source symbols | Narrow conditional series may survive while gauge dynamics and Coulomb meaning enter by declaration | Hash-pinned execution, data-flow audit, and load-bearing mutations |
| B | Exact massive Feynman kernel | Declared positive mass/coefficient and explicit parameter integrand | `m^2`, `C`, `Q^2` | Analytic disk and beta-function coefficient sequence follow exactly; the massless limit is singular/nonuniform | Direct integration, series coefficients, singularity radius, and numerator/mass mutations |
| C | General gapped spectral expansion | Positive threshold plus finite inverse moments and subtraction convention | threshold and moment sequence | A gap supports but does not alone guarantee the analytic series or nonzero leading coefficient | Geometric-series remainder and divergent/zero-moment counterexamples |
| D | Inverse-kernel leading-power ledger | A supplied sum of fractional and analytic powers | exponents and coefficients | The smallest nonzero exponent controls the infrared; analytic loop terms cannot remove a lower fractional bare term | Exact limits under coefficient deletion, cancellation, and exponent mutation |
| E | Static Riesz Green kernel | Frozen Fourier convention, dimension, `0<s<d/2`, and nonzero coefficient | `d`, `s`, normalization | The conditional power is `r^(2s-d)`; Coulomb is only the `d=3,s=1` specialization | Independent Schwinger/Gaussian derivation, gamma normalization, and dimension/exponent probes |

## Selection Criteria and Blinding

Selection is ordered by accepted dependency closure, exact momentum/tensor/
Fourier convention consistency, separation of gap/vertex/subtraction/bare-
kernel/dimension premises, assumption and parameter economy, correct massive,
massless, threshold, fractional, coefficient-zero, and long-distance limits,
and independent coefficient and Fourier derivations. Numerical or named
Coulomb agreement is excluded. The synopsis-exposed coefficient and exponent
cannot select a sign, variable, dimension, kernel, or claim boundary. These
objects and criteria are frozen before source access.

## Proposed Claim Delta

Provisional C-LOC-001 may state an exact theorem for the declared massive
Feynman kernel and, if naturally closed, a general gapped inverse-moment
expansion with its convergence premises. Provisional C-KRN-001 may state the
exact leading-power/fractional-persistence theorem and conditional Riesz
Green kernel. Neither claim may assert that the framework derives the loop
integrand, charged matter, Maxwell term, photon, `s=1`, `d=3`, Coulomb force,
physical electric charge, absolute scale, or substrate realization. The two
claims will be reviewed independently and may be narrowed without blanket
promotion.

## Implementation and Oracle Plan

A pure additive module under `src/substrate_framework/` will expose exact
massive-kernel coefficients and convergence data, spectral moment ledgers,
inverse-kernel leading exponents, and Riesz normalization. It will execute no
integral, simulation, or print operation at import. Proposal scripts will
only call those APIs and audit D3S.

SymPy exact integration, series, residues, limits, gamma identities, and rank
analysis are the strongest oracles. An independent route will derive the
coefficient sequence from beta integrals and the Green kernel from a Schwinger
parameter plus Gaussian Fourier transform without importing the canonical
evidence objects. Mutations will alter the Feynman numerator, mass, overall
sign, subtraction, first spectral moment, bare fractional exponent,
coefficient cancellation, dimension, and Fourier normalization. The massless
and zero-momentum limits will be tested in both orders where relevant. No
numeric quadrature is required and no NumPy integration alias will be used.
GitNexus impact analysis precedes canonical edits; focused exact tests, claim
verifiers, affected consumers, one full workflow gate, and diff checks close
promotion.

## Attempts and Continuation

The append-only ledger begins with source reproduction and data-flow audit as
attempt 0001. If the literal route fails, its valid exact series will be
retained and Candidates B through E will continue according to the diagnosed
mechanism. A missing spectral moment triggers an explicit premise or a
counterexample, not an inferred coefficient. A fractional-kernel conflict
rejects the exponent-selection claim before any accepted U1 or sine-Gordon
claim is reinterpreted.

## Debt Ledger

This ledger tracks loop ontology and source provenance, momentum and tensor
conventions, mass-gap and moment premises, subtraction and regularization,
bare versus induced kernel terms, leading coefficients, fractional powers,
Fourier normalization, dimension, physical dictionaries, independent
evidence, consumers, and canonical synchronization.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| D3S's literal equations, checks, imports, and output are unaudited | Hash-check, execute, trace each subclaim to its defining kernel and dependency, and preserve output or failure | closed by attempt 0001 and the source audit |
| The positive massive-kernel and spectral expansion objects are absent | Derive coefficients, convergence domain, remainder/limit behavior, and moment premises in tested importable APIs | closed by `momentum_kernels.py` and exact tests |
| A normalized sine-Gordon gap may be relabeled as a charged loop mass | Preserve the dimensionless scalar ceiling and require an explicit loop-field/current dictionary | closed by the interpretation ceiling and D3S qualification |
| Gauge covariance may be mistaken for a gauge kinetic action | Keep C-GAU-001's no-dynamics ceiling and inventory every bare/induced inverse-kernel premise | closed by C-KRN-001's declared-kernel boundary |
| Analyticity may be asserted from a gap without moment convergence | Prove the exact domain or supply counterexamples and narrow the theorem | closed by the spectral remainder and divergent-moment counterexample |
| An analytic correction may be claimed to select `s=1` despite a fractional bare term | Classify the smallest nonzero exponent and test coefficient deletion/cancellation/fractional mutations | closed by exact leading-power mutations |
| A conditional Riesz transform may be called physical Coulomb or `d=3` | Derive the general `d,s` kernel first and retain dimension, normalization, source, and force-law premises | closed by the general Riesz theorem and endpoint ceiling |
| Downstream impact and independent review are unknown | Complete graph impact analysis, independent derivation, targeted replay, and separate claim reviews | closed by graph audit, independent verifier, and claim reviews |
| Registry, release, docs, queue, and memory are unsynchronized | Promote only reviewed claims, regenerate canonical consumers, and empty this campaign ledger | closed by the v0.58.0 promotion transaction |

## Review and Promotion Plan

C-LOC-001 and C-KRN-001 will receive separate reviews over raw integrands,
coefficient sequences, convergence domains, dimensions, limits, leading-
power mutations, Fourier normalization, and interpretation ceilings. Accepted
APIs move into the package with focused tests, a pinned release, generated
docs, and accepted memory. D3S will be qualified if exact conditional
mathematics survives but its gap-to-Coulomb physical chain does not. The
generated queue will be rebuilt only from the editable disposition registry.

## Done Gate

P064 closes only when the positive massive-kernel, leading-power, and Green-
kernel objects, strongest sensitive oracle, independent route, claim-level
reviews, downstream replay, canonical promotion, source disposition, and
empty debt ledger all pass. A failed D3S headline alone leaves the campaign
active with the next construction.

## Adjudication Outcome

P064 accepts Candidates B, C, D, and E as exact conditional mathematics and
rejects Candidate A as a physical gap-to-Coulomb derivation. C-LOC-001 and
C-KRN-001 are individually accepted in v0.58.0 after primary, independent,
mutation, focused, graph, governance, and repository replay. D3S is qualified:
its declared kernel series and Riesz endpoint survive, but its charged-loop,
bare-action, nonzero-coefficient, exponent-selection, dimensional-lift,
Coulomb, and substrate-sector headlines do not. The campaign debt ledger is
empty; the parent corpus migration remains active for later units.
