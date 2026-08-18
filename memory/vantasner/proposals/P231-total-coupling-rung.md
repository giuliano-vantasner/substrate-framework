---
description: 'P231: compose C-IGR-001..003 with C-GRV-001 into the first derived usable total gravitational coupling 1/G_total = 1/G_baseline + Delta(1/G) with scheme selection, sign map, and control ledger (issue #88)'
author: vantasner
created: '2026-08-18T14:05:00+02:00'
updated: '2026-08-18T14:05:00+02:00'
tags:
- substrate-framework
- campaign-proposal
- induced-gravity
- total-coupling
category: proposals
confidence: exploratory
status: active
---

## Question and Positive Deliverable
The question is issue #88's: composing the accepted one-loop inverse-coupling
families C-IGR-001..003 with C-GRV-001's dimensional and additive-baseline
ledger, derive the framework's first usable total gravitational coupling
1/G_total = 1/G_baseline + Delta(1/G) as a governed renormalization condition
with declared substrate provenance. The positive deliverable is the derived
total-coupling statement as an importable, tested API with mutation-sensitive
oracles: the substrate-internal selection derivation that makes the usable
scheme set and its finite parts outputs of substrate structure, the additive
baseline's exact provenance and consequence map including the purely-induced
reading, the exact necessary and sufficient total-sign conditions on
(N, xi, scheme, m^2, cutoff or scale, baseline), and the control ledger for
the tau^-1 sector and nonlocal remainder. A negative intermediate finding is
append-only attempt evidence; the campaign continues with a materially
different candidate.

## Base Release and Provenance
Accepted release v0.161.0, baseline commit 7dfe89b (main), branch
research/p231-total-coupling-rung cut at that commit. Source claims read:
C-GRV-001 (v0.68.0), C-IGR-001..003 (v0.161.0) in governance/claims.yaml
with their campaigns. Canonical modules read: scalar_one_loop_mass.py
(accepted-canon implementation of the I2/I3 families), scalar_induced_newton.py
and covariant_sine_gordon_action.py (unpromoted, implementation reuse only).
Primary literature carried forward from P230: Vassilevich hep-th/0306138v3
eqs 1.16-1.20, 2.2, 4.27; Visser gr-qc/0204062v1 eqs 7-15.

## Source Inventory and Access Gate
No new external source is required: the composition consumes accepted claims
and the two approved primary imports above, both independently checked in
P230. The heat-kernel expansion organization that exhibits the tau^-1 (a4,
curvature-squared) class is part of Vassilevich's carried-forward
conventions; P231 uses the class's existence and typed slot, not a new
coefficient import.

| Source | Access status | Extracted claims (with page/eq) |
| --- | --- | --- |
| C-GRV-001 | accepted registry | additive baseline ledger, E_cut=hbar*c/a cutoff ontology |
| C-IGR-001..003 | accepted registry | exact I2/I3 families, typed shifts, scheme ceiling |
| Vassilevich hep-th/0306138v3 | open arXiv, checked in P230 | determinant/heat-kernel conventions, a0/a2/a4 class organization |
| Visser gr-qc/0204062v1 | open arXiv, checked in P230 | cutoff effective-action organization, sector retention |

## Invariants, Conventions, and Allowed Imports
All C-IGR-001 operator, determinant, mass, infrared, matching, and
local-coefficient assumptions remain in force. C-GRV-001's baseline B stays
free; B=0 is a declared premise whose downstream ceiling must be quoted. The
usable scheme set must be an output of exact substrate-internal conditions,
not a point choice; no physical regulator selection by numerical closeness;
no observed G or Planck phenomenology in selection, formulas, tolerances, or
tests; no fitted Newton constant; no borrowed Einstein-Hilbert coefficient;
no sourced geometry or radiative prediction. Accepted claims, releases, and
generated docs change only in the later promotion transaction.

## Candidate Preregistration
Registered before any composition evaluation; the four candidate structures
for the renormalization condition are in proposals/P231-total-coupling-rung/
proposal.yaml. A is the scheme-uniform usable-set composition with the
selection legs (spectral positivity, monotone decoupling, cutoff ontology)
outputting {sharp, smooth} and a scheme-bracketed normalization. B declares a
single point scheme. C adopts the power-subtracted scale as the condition. D
folds the tau^-1 sector and nonlocal form factors into the coupling itself.

## Selection Criteria and Blinding
Structural criteria frozen in the manifest: exactness, spectral positivity,
monotone large-mass decoupling, cutoff-ontology closure, scheme-uniformity of
the sign conditions, assumption economy, comparator blinding. Comparator
blinding point: no empirical gravitational value exists in this campaign at
all; internal exact evaluations (limits, spread ratios, boundary loci) are
derivations and cannot select a scheme.

## Proposed Claim Delta
C-IGR-004 (composition and selection derivation, depends on C-GRV-001,
C-IGR-001..003) and C-GRV-002 (total-coupling sign/regime statement, depends
on C-GRV-001 and C-IGR-004's composition) are candidate claims; both are
collision-searched (zero prior uses) and promoted only individually through
the later reviewed promotion transaction.

## Implementation and Oracle Plan
New module src/substrate_framework/total_gravitational_coupling.py
composing the accepted scalar_one_loop_mass API; campaign verifier
proposals/P231-total-coupling-rung/verify.py with CheckLedger; independent
rederivation reviews/independent_total_coupling_review.py importing neither
module; tests with mutation-sensitive oracles for scheme-spread
non-degeneracy, sign-map boundaries, baseline provenance, and control-ledger
entries. Exact SymPy obligations dominate; mpmath quadrature corroborates
only. Validation is impact-based scoped/full via scripts/validate_changed.py.

## Attempts and Continuation
Attempt 0001 opens with this manifest. Failures append append-only attempt
records with diagnosis and the materially different next candidate.

## Debt Ledger
Tracks undeclared premises, unresolved residuals, convention conflicts, and
broken consumers introduced by this campaign. Empty at open.

## Review and Promotion Plan
This rung PR names canonical issue #88 with Advances; non-self-merge applies
(request review from @vantasnerdan or a distinct agent). Claim promotion,
registry, release, generated docs, and accepted memory synchronization are a
later reviewed transaction. Impact-based validation rationale recorded in the
attempt manifest.

## Done Gate
The rung is complete when the derived positive object exists: importable
API, tests, mutation-sensitive oracles, evidence set, independent
rederivation, and a PR passing adversarial review. The #76 and #88 objectives
remain open until the later promotion and comparator gates.
