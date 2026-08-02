---
description: Derive a conditional induced-gravity scaling and identifiability ledger and audit AS3
author: vantasner
created: '2026-08-03T10:00:00Z'
updated: '2026-08-03T10:50:00Z'
tags:
- substrate-framework
- campaign-proposal
- induced-gravity
- migration-AS3
category: proposals
confidence: exploratory
status: archived
---
# P074 AS3 Induced-Gravity Scaling Audit

## Question and Positive Deliverable

P074 must derive an importable exact ledger for the M,L,T monomial of Newton's
constant from a declared cutoff length, speed, and action scale; the induced
inverse-coupling contribution and independent bare term; the resulting log
parameter identifiability; and an explicit source-coupling convention. It must
then terminally adjudicate whether AS3 derives an induced coefficient and
physical coupling or only supplies a conditional scaling parameterization.

## Base Release and Provenance

The accepted base is `v0.67.0` at scientific commit `3758a02`; parent-effort
synchronization is commit `dcaa01f`. The predecessor is pinned at
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`. AS3 is
`/home/dan/substrate/merged-framework/bridges/phase-21/bridge_AS3_sakharov_kappa_reduce.py`,
13023 bytes, with SHA-256
`f88cc85a3fb64d1b8aabdf53ced29168d78fce9470e586dc19564288a120903b`.
The queue marks AS3 pending and names AS1, G1, G2, G5, OD, and S5. AS1 is now
qualified through C-RGE-003; G1, G2, and G5 remain pending, while OD and S5
have only narrow accepted mappings and cannot supply the physical claims AS3
attributes to them. Release v0.67.0, C-DIM-001, C-OG-001 through C-OG-003,
C-IDN-001, their canonical modules and reviews, source dispositions, history,
and durable-memory searches were inspected on a clean tree before this
contract. Only AS3's generated queue synopsis has been opened; its source body
and all empirical comparator values remain blinded.

## Invariants, Conventions, and Allowed Imports

The base dimensions are ordered M,L,T. The declared target has
`[G]=L^3 M^-1 T^-2`; primitives are positive cutoff length `a`, speed `c`, and
action scale `hbar`, with dimensions L, L/T, and M L^2/T. Exact exponent
solving may determine powers but never a dimensionless coefficient. A cutoff
energy `E_cut=hbar*c/a`, a dimensionless induced coefficient `s`, an
independent bare inverse coupling, and any map `kappa=alpha*G` are separately
declared premises with provenance. C-OG-003 explicitly leaves its 1+1 source
coupling unnormalized. No pending G-sector equation, Sakharov field content,
regulator, subtraction prescription, observed Newton constant, lattice
ontology, or later AS operating point is an allowed import.

## Candidate Preregistration

The candidates are frozen before the AS3 source body or comparators are read.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal AS3 reproduction | Every source import and convention is coherent | Source inputs | Narrow algebra may survive; physical closure need not | Hash-pinned execution and data-flow audit |
| B | Pure dimensional monomial | Declared M,L,T dimensions only | One free dimensionless multiplier | Powers are unique but coefficient is not | Exact exponent solve and wrong-power mutations |
| C | Induced inverse contribution | Declared cutoff and regulator-dependent coefficient | `a,c,hbar,s` | `Delta(1/G)=s*hbar/(a^2*c^3)` conditionally | Substitution, units, signs, and cutoff limits |
| D | Bare-plus-induced ledger | Independent bare inverse coupling is allowed | Candidate C plus bare term | Pure `G proportional a^2` fails generically | Counterterm family and cancellation probes |
| E | Log-identifiability ledger | One supplied monomial relation | `log a,log s` | One null direction remains | Exact rank, nullspace, and inverse inference |
| F | Coupling-convention audit | A source equation and dimensional conversion are supplied | `G,alpha` | A numeric `8*pi` alone cannot identify unlike couplings | Dimension rows and normalization mutation |

## Selection Criteria and Blinding

Selection is ordered by accepted dependency closure, exact dimensions and
signs, explicit parameter and counterterm inventory, correct limits,
mutation sensitivity, natural framework fit, and assumption economy. No
empirical Newton value, cutoff length, field-count estimate, or later-source
operating point may set a coefficient, convention, threshold, or verdict.
The queue synopsis is navigation metadata only; the source body and
comparators remain closed until this contract and both representations agree.

## Proposed Claim Delta

Provisional C-GRV-001 may state the exact conditional dimensional monomial,
induced and bare inverse-coupling ledger, source-normalization guard, and
relative log-coordinate ceiling if that composition is genuinely reusable and
nonduplicate. It may not establish Sakharov's physical mechanism, a field
spectrum or regulator, a sign or coefficient, a zero bare term, 3+1 gravity,
the C-OG-003 source dictionary, an observed constant, a lattice scale, or an
absolute prediction.

## Implementation and Oracle Plan

SymPy fits the promoted obligations because all dimensions, substitutions,
rank/nullspace statements, derivatives, limits, and counterfamilies are exact.
The campaign will reuse `dimensional_analysis`, `scale_constraints`, and the
shared verification ledger. A new pure `induced_gravity` module is permitted
only for the nonduplicate composition. The independent route will rebuild the
dimension solve, bare-term counterfamily, log nullspace, and coupling-dimension
guard without importing that API. Mutations will change the cutoff power,
drop hbar or c powers, hide `s`, delete the bare term, flip the induced sign,
force `8*pi` across incompatible source dimensions, and treat an inverse map
from supplied G as prediction. No numerical integration is planned; if later
source evidence unexpectedly requires sampled quadrature, it must route
through the shared compatibility helper rather than a NumPy-version-specific
alias.

## Attempts and Continuation

Attempt 0001 reproduces all eight AS3 checks and exposes the missing
coefficient, baseline, identifiability, and source-normalization gates. Attempt
0002 preserves two verifier-representation mistakes: an expected symbol that
correctly cancels on round trip and an overconstrained nullspace basis.
Attempt 0003 repairs those tests and verifies Candidates B-F through the
canonical API, primary route, and fresh independent SymPy derivation.

## Debt Ledger

The campaign tracks dimensional, field-content, regulator, counterterm,
source-coupling, identifiability, dependency, verification, and synchronization
debt.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| Dimensions may be used to fix a coefficient | Solve exponents and retain every dimensionless factor | discharged by the exact monomial ledger |
| A cutoff may be equated to lattice granularity without derivation | Separate the declared cutoff map from physical ontology | discharged; the map remains a declared premise |
| Field content, regulator, and sign may be hidden in `s_G` | Preserve them as provenance-bearing premises or reject the physical claim | discharged by the literature and coefficient audits |
| A bare inverse coupling may be silently set to zero | Construct and test the additive counterterm family | discharged by arbitrary-total and cancellation families |
| C-OG-003's kappa may be equated to 3+1 Newton G | Audit source dimensions and require an explicit conversion factor | discharged by the source-normalization ledger |
| Scaling or coordinate reduction may be called absolute prediction | Derive the log nullspace and inverse-input ledger | discharged by the exact (2,-1) row and null direction |
| Pending dependencies may be imported as accepted physics | Audit the complete dependency closure and quarantine later narratives | discharged; no pending narrative enters C-GRV-001 |
| Sensitive verification, review, and synchronization are incomplete | Complete mutations, independent route, source disposition, claim review, replay, release, docs, queue, and memory | discharged at the v0.68.0 promotion boundary |

## Review and Promotion Plan

Any proposed claim receives independent dimensional, counterterm,
identifiability, limiting-case, and convention review. AS3 receives a terminal
disposition through `migration/dispositions.yaml` and queue regeneration.
Accepted reusable logic moves into package code with focused tests, while the
source reproduction and rejected physical interpretations remain campaign
evidence. Promotion requires claim-level review, generated synchronization,
affected-consumer replay, one unchanged full workflow boundary, and separate
`git diff --check`.

## Done Gate

P074 is complete. C-GRV-001, the canonical module, 31 focused tests, 40 primary
checks, and 26 independent checks supply the positive exact object. The
focused governance boundary passes 48 tests; the integrated workflow and the
separately required full pytest replay each pass all 689 tests. Release
`v0.68.0`, the registry, generated docs and framework memory, and the AS3
qualified disposition agree. Campaign debt is empty; parent migration debt
remains because 146 source units are pending.

## Outcome

Candidates B-F establish exact dimensional, additive inverse-coupling,
identifiability, and source-normalization ledgers. AS3 is qualified rather
than promoted wholesale: dimensions cannot derive its one-loop premise or
coefficient, the cited formula retains a baseline and further terms, free
`s_G` leaves a null direction, and pending G5 cannot normalize C-OG-003's
coupling. The campaign uses no numerical integration, deprecated `np.trapz`,
or version-specific replacement alias.
