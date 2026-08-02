---
description: Derive and audit conditional anomalous HLS vector elimination
author: vantasner
created: '2026-08-02T11:52:10Z'
updated: '2026-08-02T18:00:00Z'
tags:
- substrate-framework
- campaign-proposal
- hls-vector-elimination
- migration-WZ4
category: proposals
confidence: exploratory
status: archived
---
# P059 WZ4 HLS Vector-Elimination Audit

## Question and Positive Deliverable

P059 must deliver a reusable exact theorem for eliminating a declared massive
vector multiplet coupled to independent parity-even and parity-odd sources,
including the leading local inverse-mass term, its odd cross term, all signs,
and every free coefficient. It must separately determine whether WZ4 actually
derives a WZW functional and its normalization, or instead starts from an
anomalous HLS action whose homogeneous terms and coefficients are premises.
Reproducing a source tally or documenting absent HLS dependencies does not
complete the campaign; Candidate B continues to the positive conditional EFT
object if Candidate A, C, or D exposes an overclaim.

## Base Release and Provenance

The accepted base is `v0.52.0` at framework commit `5d81e93`, whose scientific
transaction is `ae23aea`. The pinned predecessor is `substrate@6d1f4e0`; WZ4
is `/home/dan/substrate/merged-framework/bridges/phase-17/bridge_WZ4_hls_vector_meson_anomalous.py`
with verified SHA-256
`fca6b9c1d95bdf49e99b863470c7e800880e493b3f716159aa2341f8cf963d2b`.
The predecessor worktree's later uncommitted artifacts are outside this source
unit. WZ4 is pending. Its candidate dependencies G2, G3, S3, and S4 are also
pending and supply no premises; WZ1 through WZ3 survive only through accepted
C-WZW-001, C-WZW-002, and C-TOP-002 with their strict physical ceilings. The
fresh skill preflight passed seven checks without warnings, framework git was
clean at the contract boundary, and memory supplied only accepted frontier
pointers. The inventory synopsis necessarily revealed the claimed low-momentum
HLS mechanism and four-term homogeneous anomalous basis; WZ4's executable,
internal equations, coefficient values, and checks remain unopened.

## Invariants, Conventions, and Allowed Imports

C-LIE-001 fixes the explicit fundamental SU(3) trace convention but not an HLS
connection or meson representation. C-WZW-001 and C-WZW-002 fix an ungauged
trace-five class, primitive sphere period, and conditional filling lattice,
not a gauged WZW action, anomaly polynomial, or physical level. C-TOP-002 fixes
a mathematical winding current while explicitly withholding a source-response
or physical baryon meaning. These ceilings remain invariant.

Allowed mathematical imports are exact finite-dimensional variational
calculus, completion of the square, Schur complements, parity bookkeeping,
and formal inverse-operator expansions at declared low momentum. Audited
primary papers may define the anomalous HLS basis and its coefficient freedom,
but that theory is an explicit external premise, not a derived substrate
sector. No G2/G3 gauge action, S3 baryon spectrum, S4 vector-meson closure,
physical rho/omega mass, coupling, vector-dominance choice, anomaly
coefficient, or `N_c` identification may enter as accepted authority.

## Candidate Preregistration

The candidate set is frozen before opening WZ4's executable internals.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal WZ4 reproduction | Every printed action, parity label, and dependency must be traced to an exercised operation | Source symbols and constants only | May verify algebra after declaring the desired anomalous couplings while calling the result independent | Hash-pinned execution, AST/data-flow audit, and coefficient/source mutations |
| B | Exact massive-vector Schur complement | A declared invertible symmetric quadratic kernel and even/odd source split | Kernel, even coupling, odd coupling | Produces a conditional local odd cross term with a coefficient inherited from both source couplings; selects no WZW normalization | Direct EOM substitution, completion of the square, formal inverse-mass expansion, and load-bearing mutations |
| C | Complete homogeneous anomalous-HLS basis | An externally declared HLS field content and audited primary operator definitions | Every independent homogeneous coefficient | Preserves coefficient freedom unless an additional phenomenological or dynamical premise is supplied | Basis independence, anomaly variation, special-coefficient counterexamples, and source comparison |
| D | Anomaly-class preservation under elimination | A full starting effective action split into an inhomogeneous WZW solution and gauge-invariant homogeneous/vector terms | Pre-existing WZW level plus homogeneous coefficients | Algebraic elimination changes local invariant terms but cannot independently create or fix the anomaly cohomology class it was not given | Functional variation before and after stationary substitution and a zero-WZW-level counterexample |

## Selection Criteria and Blinding

Selection is ordered by accepted-convention compatibility, completeness of the
declared quadratic action, actual stationary-field substitution, assumption
and parameter economy, parity/dimensional/symmetry correctness, sensitive
mutations, independent derivation, and a strict distinction between anomaly
class and homogeneous local terms. No numerical or phenomenological
comparator is needed to select this structural theorem. Inventory-exposed HLS
language and the desired WZW conclusion are barred from fixing the source
split, a coefficient, or an operator basis before the source gate opens.

## Proposed Claim Delta

Provisional C-EFT-001 may assert the exact conditional stationary elimination
of a finite massive vector multiplet with symmetric invertible kernel and the
resulting Schur complement. With source decomposition into parity-even and
parity-odd pieces it may state the inherited odd cross term and the leading
inverse-mass derivative expansion under explicit power counting. The claim
will keep every coupling, mass matrix, boundary/integration-by-parts premise,
and truncation remainder visible.

The claim cannot establish an HLS realization, physical rho or omega field,
homogeneous-WZW basis, vector dominance, gauged WZW action, anomaly matching,
physical baryon current, `N_c`, or substrate mechanism without separately
closed inputs. WZ4 and later MK2/MK3-style consumers that cite vector
elimination or anomalous couplings must not inherit those meanings from the
generic conditional theorem.

## Implementation and Oracle Plan

A pure canonical module under `src/substrate_framework/` will expose exact
quadratic-source stationary elimination, on-shell effective action, parity
cross-term decomposition, and the leading inverse-mass expansion. Imports
will not print or run simulations. SymPy exact matrix algebra is the strongest
oracle for EOM residuals, square completion, Schur complement, cross-term
coefficients, scaling, and sign conventions. One route will solve the
stationary equations and substitute; an independent route will translate the
field and complete the square without calling the canonical elimination
helper.

Mutations flip the source sign, remove either source, alter a coupling, use a
nonsymmetric or singular kernel, change the one-half normalization, reverse
the odd parity label, and violate the declared low-momentum ordering. The
formal expansion must multiply back to the identity through its stated order
and retain a symbolic remainder rather than silently equating a truncation
with the exact inverse. Primary-source review will separately inspect the
actual HLS anomalous basis and variation; a printed operator name or literal
boolean is not an anomaly oracle. GitNexus impact analysis precedes any
canonical edit, followed by targeted module tests, the campaign verifier,
independent review, affected consumer replay, one promotion-boundary workflow
gate, and `git diff --check`.

## Attempts and Continuation

The append-only ledger contains four attempts. Attempt 0001 reproduces WZ4's
native nine-check tally and rejects it as a positive HLS route because no HLS
action or vector equation exists and the desired contact coefficient is an
input. Attempt 0002 implements Candidate B exactly; two initial SymPy
expression-tree comparisons failed despite zero algebraic residuals, so the
oracles were repaired to compare exact simplified differences without changing
a formula or tolerance. Attempt 0003 independently passes 23 checks without
canonical elimination helpers, including one-half, sign, source-removal,
noncommuting-residual, homogeneous-variation, arbitrary-contact, and zero-level
mutations. Attempt 0004 audits Candidate C in primary HLS sources and preserves
its four free coefficients as an external-theory ceiling. Candidates B and D
are selected; C is contextual evidence and A is rejected as the headline
mechanism.

## Debt Ledger

This ledger tracks source provenance, the complete vector action, kernel and
source conventions, parity, derivative order, coefficient freedom, anomaly
semantics, external HLS imports, independent evidence, consumers, and
canonical synchronization.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| WZ4's literal operations, imports, coefficients, environment behavior, and tally are unaudited | Hash-check, execute, trace every subclaim to its data flow, and preserve output or failure | discharged by source reproduction, audit, and attempt 0001 |
| The positive vector-elimination object is not implemented | Derive and test the exact stationary field, Schur complement, even/odd cross term, and inverse-mass expansion | discharged by `effective_actions.py`, focused tests, and attempts 0002/0003 |
| Signs and factors may be copied from a propagator slogan | Complete-square and direct-substitution routes must agree and fail appropriate sign, one-half, coupling, and mass mutations | discharged by the canonical and independent exact residual gates |
| HLS anomalous operators and coefficient freedom are unsourced | Audit the defining primary literature and distinguish the full anomaly solution from homogeneous terms | discharged by the two primary HLS sources and attempt 0004 |
| The claimed independent WZW route may assume the WZW/anomalous action it claims to derive | Track the starting functional and its anomaly variation through elimination, including a zero-level counterexample | discharged by the stationary chain-rule and arbitrary/zero-contact mutations |
| Pending G2/G3/S3/S4 or phenomenological vector data may leak into the result | Inventory every dependency and retain all unaccepted masses, couplings, field maps, and vector-dominance choices as explicit premises or exclusions | discharged by C-EFT-001's empty dependency list and explicit exclusions |
| Downstream impact and independent evidence are unknown | Complete graph impact analysis, independent rederivation, mutations, and targeted consumer replay | discharged by LOW graph risk, 23 independent checks, and the focused replay |
| Registry, release, generated docs, migration queue, and durable memory are unsynchronized | Review claim by claim, adjudicate WZ4, regenerate canonical consumers, and empty this ledger | discharged by the v0.53.0 promotion transaction and canonical generators |

## Review and Promotion Plan

The generic elimination theorem, low-momentum expansion, parity-odd cross
term, anomalous-HLS interpretation, and every physical identification will
receive separate decisions. The independent review will derive the effective
action by completion of the square without using the canonical helper and
will inspect primary HLS definitions separately from WZ4's preferred
conclusion. Any accepted conditional theorem moves into an importable module
with tests and a pinned release; WZ4 receives a structured terminal
disposition only when all surviving and rejected subclaims have durable
evidence. Migration edits will touch only `migration/dispositions.yaml` and
regenerate `migration/source-claims.yaml`; canonical docs and accepted memory
will be rendered from governance state.

## Done Gate

P059 closes with C-EFT-001 accepted in v0.53.0 and WZ4 qualified after the
positive exact elimination object, independent derivation, source
adjudication, anomaly/HLS ceiling, sensitivity, downstream replay, canonical
synchronization, and empty campaign debt ledger pass. The parent corpus
migration remains active until every queue unit is terminal.
