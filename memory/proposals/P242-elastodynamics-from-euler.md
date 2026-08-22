---
description: Derive isotropic elastodynamics from incompressible Euler coarse-graining as an exact conditional claim ladder with named, falsifiable ensemble premises, plus the simulated no-elasticity side.
author: ox-alpha
created: '2026-08-22T00:00:00+02:00'
updated: '2026-08-22T00:00:00+02:00'
tags:
- substrate-framework
- campaign-proposal
category: proposals
confidence: exploratory
status: active
---

## Question and Positive Deliverable

This campaign derives isotropic elastodynamics from constant-density
incompressible Euler dynamics as an exact conditional claim ladder. The
positive deliverable is a seven-rung ladder: an exact filtered momentum
balance with an explicit sub-filter momentum flux; a conditional bridge from a
strain-coupled closure to Navier-Cauchy dynamics with wave speeds; exact
affine homogenization of a declared frozen filament ensemble giving positive
Lame moduli; the incompressible constraint branch and regime reconciliation;
the assembled conditional emergence theorem; a numeric non-affine correction
with rigidity threshold on declared networks; and a simulation demonstrating
that unconstrained ergodic vortex ensembles produce no static strain-coupled
restoring stress. A no-go alone does not complete this campaign; the two-sided
structure is the objective.

## Base Release and Provenance

The accepted base release is v0.163.0 pinned at substrate-framework@970633a,
with campaign work based on main at e9b67af4. The registry contains no fluid
Euler or elastodynamics sector; C-VTX-001/002 are Abelian-Higgs solitons, a
different object. Memory search shows no prior elastodynamics-from-Euler
campaign; identifiers C-ELS-001 through C-ELS-007 and proposal P242 were
absent from governance/claims.yaml, proposals/, campaigns/, branches, and
durable memory at allocation time.

## Source Inventory and Access Gate

The external source gate closed before preregistration. MIT 2.25 Section 9 was
fetched 2026-08-22 and supplies circulation, Biot-Savart, Kelvin's theorem,
and frozen-in vortex lines; the logarithmic straight-line energy scale is
rederived internally as an exact lemma rather than imported. Non-affine and
Maxwell-counting contexts have open arXiv access (2602.03770, 2605.21021,
2603.27352) and contribute context only. The issue 158 PDF is secondary LLM
output held in hand; it is triage material, not a load-bearing source.

## Invariants, Conventions, and Allowed Imports

The microscopic dynamics is exactly constant-density incompressible Euler;
every elasticity statement is conditional on premises that are declared,
named, and independently falsifiable; no hidden fitted constant may appear.
Compressible and incompressible closures are never mixed inside one
computation. Exact rungs use SymPy oracles; numeric rungs use scipy with
declared refinement and mutation probes. Permitted imports are the venv
scientific stack and the classical MIT 2.25 statements.

## Candidate Preregistration

Two mechanisms are registered because the question of what carries a static
shear modulus is genuinely open at the mechanism level. Candidate A is the
frozen-connectivity affine Cauchy-Born tangle with axial line stiffness:
it predicts lambda equals mu equals E_f L_v over fifteen and survives only
while topology locks filament connectivity. Candidate B is the ergodic
Reynolds-stress closure of the issue 158 optimistic sketch: it carries no
reference-state memory, so structural analysis predicts its anisotropic
stress cannot sustain strain-proportional restoring force. The decisive test
between them is the relaxation diagnostic of C-ELS-007.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Frozen affine Cauchy-Born tangle | frozen connectivity, orientation isotropy, axial stiffness E_f = kappa T | E_f, L_v | positive moduli above threshold; recovers Navier-Cauchy exactly under declared premises | C-ELS-003 algebra plus C-ELS-006 threshold |
| B | Ergodic Reynolds-stress closure | averaging only; no topology locking | none new | anisotropic stress relaxes; no static shear modulus | C-ELS-007 simulation |

## Selection Criteria and Blinding

Selection orders framework-invariant compatibility first (fluid limit Euler,
solid limit Navier-Cauchy), then assumption economy, then limit correctness
across the compressible and incompressible branches, then implementability.
No empirical comparator enters any verdict: all claims are exact-conditional
or simulations against declared models, so comparator blinding reduces to
freezing structure before any diagnostic is read.

## Proposed Claim Delta

Seven new claims are proposed, none superseding anything. C-ELS-001 exact
filtered balance with commutator-free convolution filtering and explicit
sub-filter flux Pi. C-ELS-002 conditional elastodynamic bridge from the
strain-coupled closure premise to Navier-Cauchy dynamics with speeds.
C-ELS-003 exact affine moduli lambda equals mu equals E_f L_v over fifteen
from exact sphere moments, including the internal straight-line tension
lemma. C-ELS-004 the incompressible constraint branch and regime
reconciliation. C-ELS-005 the conditional emergence theorem assembling the
ladder. C-ELS-006 numeric non-affine correction and rigidity threshold.
C-ELS-007 simulation evidence for the no-elasticity side. Dependencies:
002 depends on 001; 003 stands alone; 004 depends on 001; 005 depends on
001-004; 006 and 007 depend on 003's model declarations. Consumers today are
none outside this ladder; future consumers include any medium-dictionary or
aether-correspondence work, which must consume these conditionally.

## Implementation and Oracle Plan

Canonical modules land under src/substrate_framework/: elasticity.py
(isotropic tensor, Hooke map, Navier-Cauchy operator, Christoffel speeds,
stability predicates), homogenization.py (exact sphere moments, affine
moduli, Cauchy-Born energy, straight-line tension lemma), averaging.py
(convolution filter moments, sub-filter flux, filtered-balance residual),
nonaffine_networks.py (periodic central-force networks, dynamical matrix,
relaxed modulus by quasistatic conjugate gradient, phonon extraction), and
vortex_dynamics.py (periodic point-vortex Hamiltonian evolution with
deviatoric kinetic-stress diagnostics). Thin verifiers
verify_els001.py through verify_els007.py live in the proposal directory,
import canonical APIs, use shared CheckLedger machinery, mutate every
load-bearing input, and exit status zero via SuccessfulCheckTally. Exact
rungs are SymPy-exact; C-ELS-006 uses sparse eigensolvers with size
refinement and two-route agreement; C-ELS-007 uses symplectic point-vortex
evolution against predeclared observables with conservation controls.

## Attempts and Continuation

Attempts accumulate append-only under attempts/000N with command, stdout,
verdict, and diagnosis. Wave 0 research and the source gate are settled; the
implementation wave consumes only declared inputs. If candidate A's threshold
analysis obstructs the emergence statement, the failure classifies per skill
Phase 4 and candidate B's rejection record sharpens the frontier without
closing the campaign.

## Debt Ledger

The debt ledger opens empty. Declared hypotheses (frozen connectivity,
affine response, quasi-static closure, identification u-bar equals d xi/dt)
are premises, not debt; each is independently falsifiable by design.
Known open frontier, not debt: the MacCullagh-Maxwell action-level
correspondence and any physical calibration of kappa remain outside this
campaign.

## Review and Promotion Plan

Each proposed claim receives one individual review against raw artifacts
before any acceptance, using memory-templates/claim-review.md; evidence
attachments keep their declared roles. On acceptance, reusable logic already
lives in canonical modules with tests; registry entries, a release manifest,
render_docs output, and accepted-memory synchronization follow the Phase 9
sequence. Validation runs scoped through scripts/validate_changed.py at the
frozen boundary with one recorded receipt; validation and commit run as
separate process invocations.

## Done Gate

The campaign closes only when every applicable AGENTS.md success gate passes:
exact rungs proven and machine-checked with mutation probes, numeric rungs
refined and two-route checked, the emergence theorem stated at full strength
with empty in-boundary debt, each claim individually reviewed into the
accepted registry, release pinned, generated docs current, and memory
synchronized. An honest intermediate failure leaves the objective active with
the next attempt queued.
